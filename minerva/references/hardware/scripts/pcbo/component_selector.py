"""
Component Selector — STATE_2.0 through STATE_5.0 пайплайна PCBO.

Детерминированный подбор компонентов через evaluate_profiles + MAUT.
Агент НЕ «думает головой» — вызывает функции и получает ranked candidates.

Каждая функция:
  1. Загружает каталог (catalog/<type>/*.md)
  2. Вызывает evaluate_profiles для profile matching
  3. Фильтрует по constraints (VRAM, socket, form_factor, sustained_write)
  4. Сортирует по MAUT: capability × perf_weight + (1 − price/max_price) × budget_weight
  5. Возвращает ranked list с margin, price, rationale

Использование:
    from component_selector import select_gpu, select_cpu, select_ram, ...
    gpu_candidates = select_gpu(min_capability="balanced_performance_gpu",
                                 min_vram_gb=14, blocked_profiles=["sub_75w_slot_powered"],
                                 budget_remaining=120000, maut_cpu_weight=0.25)
"""

import os, re, sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent  # scripts/pcbo → scripts → KB root
CATALOG = ROOT / "catalog"
SCRIPTS = ROOT / "scripts"

# Engineering clearances (mm) — from PCBO Skill 3 (structural)
GPU_INSTALL_CLEARANCE_MM = 10    # зазор на монтаж GPU в корпус
COOLER_SIDE_PANEL_CLEARANCE_MM = 5  # зазор между кулером и боковой панелью

# Import evaluate_profiles functions
sys.path.insert(0, str(SCRIPTS))
from evaluate_profiles import (
    parse_frontmatter, evaluate_component, CAPABILITY_MAP_BY_TYPE,
    get_capability_level, VALID_INTENTS
)


@dataclass
class Candidate:
    id: str
    type: str
    title: str
    price: int
    specs: dict
    profiles: list
    margin: int = 0          # capability − min_capability (GPU only)
    maut_score: float = 0.0
    rationale: str = ""
    warnings: list = field(default_factory=list)  # completeness / ontology WARN messages


def _margin_check(profiles: dict, cmp_type: str, min_capability: str | None) -> tuple[int, int]:
    """Return (comp_level, margin) for margin analysis. margin = level − min_level.
    
    Uses capability_level from profile data first (v4.1 field),
    falls back to matching profile names against CAPABILITY_MAP_BY_TYPE (legacy GPU).
    """
    if not min_capability:
        return (0, 0)
    cap_map = CAPABILITY_MAP_BY_TYPE.get(cmp_type, {})
    comp_tiers = []
    for pname, pd in profiles.items():
        if not pd.get("criteria_met", True):
            continue
        # v4.1: explicit capability_level in profile data
        cl = pd.get("capability_level")
        if cl is not None:
            comp_tiers.append(cl)
        else:
            # Legacy: match profile name against capability map (GPU only)
            level = cap_map.get(pname)
            if level is not None:
                comp_tiers.append(level)
    if not comp_tiers:
        return (0, 0)
    comp_level = max(comp_tiers)
    # resolve min_capability: it can be a capability name (like "high_core_count_cpu") or a profile name
    min_level = cap_map.get(min_capability)
    if min_level is None:
        # Try finding the capability name in the map by its level
        # This handles when min_capability is a profile name not in the map
        return (comp_level, 0)  # can't determine margin, assume satisfies
    return (comp_level, comp_level - min_level)

def select_gpu(
    min_capability: str,
    min_vram_gb: int,
    blocked_profiles: list[str],
    budget_remaining: int,
    maut_gpu_weight: float = 0.75,
    intents: list[str] | None = None,
) -> list[Candidate]:
    """
    STATE_2.0: подбор GPU.
    
    Фильтры:
      - VRAM ≥ min_vram_gb
      - capability_level ≥ min_capability (margin ≥ 0 = satisfies)
      - НЕ имеет blocked_profiles
      - Цена ≤ budget_remaining
    
    Сортировка: MAUT = (margin=0 → +1) × maut_gpu_weight + (1 − price/max_price) × (1−maut_gpu_weight)
    """
    candidates = []
    gpu_dir = CATALOG / "gpu"
    if not gpu_dir.exists():
        return candidates

    for f in sorted(gpu_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "gpu":
            continue

        specs = fm.get("specs", {})
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        # VRAM check
        vram_raw = specs.get("vram", "0")
        vram_match = re.search(r"(\d+)", str(vram_raw))
        vram_gb = int(vram_match.group(1)) if vram_match else 0
        if vram_gb < min_vram_gb:
            continue

        # Profile check
        profiles = fm.get("profiles", {})
        cap_map = CAPABILITY_MAP_BY_TYPE.get("gpu", {})
        comp_tiers = []
        for pname, pd in profiles.items():
            level = cap_map.get(pname)
            if level is not None and pd.get("criteria_met", True):
                comp_tiers.append((pname, level))

        if not comp_tiers:
            continue

        comp_level = max(t for _, t in comp_tiers)
        min_level = cap_map.get(min_capability, 1)
        margin = comp_level - min_level

        if margin < 0:
            continue  # FAIL

        # Blocked profiles check
        blocked = False
        for bp in blocked_profiles:
            bp_short = bp.split("#")[-1] if "#" in bp else bp
            if bp_short in profiles and profiles[bp_short].get("criteria_met", True):
                blocked = True
                break
        if blocked:
            continue

        # MAUT score: margin=0 → highest, higher margin → penalty
        # perfect = margin 0, цена минимальна
        maut = (1.0 / (1 + margin)) * maut_gpu_weight  # margin penalty
        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="gpu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"vram": vram_gb, "bus": _extract_bus(specs), "tgp": _extract_tgp(specs)},
            profiles=[p for p, _ in comp_tiers],
            margin=margin,
            maut_score=0,  # filled below
            rationale=f"margin={margin:+d}, VRAM={vram_gb}GB"
        ))

    if not candidates:
        return []

    # Normalize MAUT with price component
    max_price = max(c.price for c in candidates)
    for c in candidates:
        price_score = 1.0 - (c.price / max_price) if max_price > 0 else 1.0
        margin_score = 1.0 / (1 + c.margin)  # margin=0 → 1.0, margin=1 → 0.5, margin=2 → 0.33
        c.maut_score = margin_score * maut_gpu_weight + price_score * (1 - maut_gpu_weight)

    candidates.sort(key=lambda c: c.maut_score, reverse=True)
    return candidates


# ═══════════════════ CPU ═══════════════════

def select_cpu(
    socket: str = "AM5",
    budget_remaining: int = 999999,
    maut_cpu_weight: float = 0.25,
    min_capability: str | None = None,
    preferred_profiles: list[str] | None = None,
    blocked_profiles: list[str] | None = None,
) -> list[Candidate]:
    """
    STATE_3.0: подбор CPU под сокет, бюджет и profile matching.
    """
    candidates = []
    cpu_dir = CATALOG / "cpu"
    if not cpu_dir.exists():
        return candidates

    for f in sorted(cpu_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "cpu":
            continue
        specs = fm.get("specs", {})
        if socket.upper() not in specs.get("socket", "").upper():
            continue

        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        profiles = fm.get("profiles", {})
        profile_list = [p for p, pd in profiles.items() if pd.get("criteria_met", True)]

        # Margin analysis (v4.1)
        comp_level, margin = _margin_check(profiles, "cpu", min_capability)
        if margin < 0:
            continue  # FAIL

        # Check blocked
        if blocked_profiles:
            if any(bp.split("#")[-1] in profiles for bp in blocked_profiles):
                continue

        cores = _extract_cores(specs)
        perf_score = min(cores / 16, 1.0)
        margin_penalty = 1.0 / (1 + margin) if margin > 0 else 1.0

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="cpu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"cores": cores, "tdp": _extract_tdp(specs), "socket": socket},
            profiles=profile_list,
            margin=margin,
            maut_score=0,
            rationale=f"{cores} ядер, TDP {_extract_tdp(specs)}W, margin={margin:+d}"
        ))

    if not candidates:
        return []

    max_price = max(c.price for c in candidates) if candidates else 1
    for c in candidates:
        cores = c.specs.get("cores", 1)
        perf_score = min(cores / 16, 1.0)
        price_score = 1.0 - (c.price / max_price) if max_price > 0 else 1.0
        margin_score = 1.0 / (1 + c.margin) if c.margin >= 0 else 0
        c.maut_score = margin_score * 0.3 + perf_score * maut_cpu_weight + price_score * (1 - maut_cpu_weight - 0.3)

    candidates.sort(key=lambda c: c.maut_score, reverse=True)
    return candidates


# ═══════════════════ RAM ═══════════════════

def select_ram(
    min_capacity_gb: int = 32,
    budget_remaining: int = 999999,
    ecc: bool = False,
    min_capability: str | None = None,
    blocked_profiles: list[str] | None = None,
) -> list[Candidate]:
    """STATE_4a: подбор RAM с profile matching."""
    candidates = []
    ram_dir = CATALOG / "memory"
    if not ram_dir.exists():
        return candidates

    for f in sorted(ram_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "memory":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        cap = _extract_ram_capacity(specs)
        if cap < min_capacity_gb:
            continue

        profiles = fm.get("profiles", {})
        
        # Blocked profiles check
        if blocked_profiles:
            blocked = False
            for bp in blocked_profiles:
                if bp in profiles and profiles[bp].get("criteria_met", True):
                    blocked = True
                    break
            if blocked:
                continue
        
        comp_level, margin = _margin_check(profiles, "memory", min_capability)
        if margin < 0:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="memory",
            title=fm.get("title", f.stem),
            price=price,
            specs={"capacity": int(cap), "speed": specs.get("speed", ""), "type": specs.get("type", "DDR5")},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            margin=margin,
            rationale=f"{int(cap)}GB {specs.get('speed', '')}, margin={margin:+d}"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Storage ═══════════════════

def select_storage(
    sustained_write_required: bool = False,
    budget_remaining: int = 999999,
    min_capability: str | None = None,
) -> list[Candidate]:
    """STATE_4b: подбор SSD с profile matching. Если sustained_write — исключает DRAM-less и QLC."""
    candidates = []
    storage_dir = CATALOG / "storage" / "nvme"
    if not storage_dir.exists():
        return candidates

    for f in sorted(storage_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "storage":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        profiles = fm.get("profiles", {})
        if sustained_write_required:
            if "dram_less_hmb_cached" in profiles and profiles["dram_less_hmb_cached"].get("criteria_met", True):
                continue
            if "read_heavy_static" in profiles and profiles["read_heavy_static"].get("criteria_met", True):
                continue

        comp_level, margin = _margin_check(profiles, "storage", min_capability)
        if margin < 0:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="storage",
            title=fm.get("title", f.stem),
            price=price,
            specs={"capacity": fm.get("specs", {}).get("capacity", "")},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            margin=margin,
            rationale=f"{'sustained_write' if sustained_write_required else 'client'}, margin={margin:+d}"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Motherboard ═══════════════════

def select_mb(
    socket: str = "AM5",
    form_factor: str = "ATX",
    budget_remaining: int = 999999,
    ecc_required: bool = False,
    no_bifurcation_required: bool = False,
    min_capability: str | None = None,
) -> list[Candidate]:
    """STATE_5a: подбор материнской платы с profile matching."""
    candidates = []
    mb_dir = CATALOG / "motherboard"
    if not mb_dir.exists():
        return candidates

    for root, dirs, files in os.walk(mb_dir):
        for fname in files:
            if not fname.endswith(".md") or fname == "index.md":
                continue
            f = Path(root) / fname
            fm = parse_frontmatter(f)
            if not fm or fm.get("type") != "motherboard":
                continue
            specs = fm.get("specs", {})
            if socket.upper() not in specs.get("socket", "").upper():
                continue

            price_data = fm.get("price_ru", {})
            price = price_data.get("median", 0)
            if not price or price > budget_remaining:
                continue

            profiles = fm.get("profiles", {})
            if no_bifurcation_required:
                bif = profiles.get("bifurcation_shared_lanes", {})
                if bif.get("criteria_met", False):
                    continue

            comp_level, margin = _margin_check(profiles, "motherboard", min_capability)
            if margin < 0:
                continue

            candidates.append(Candidate(
                id=fm.get("id", f.stem),
                type="motherboard",
                title=fm.get("title", f.stem),
                price=price,
                specs={"socket": socket, "form_factor": specs.get("form_factor", "ATX")},
                profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
                margin=margin,
                rationale=f"{specs.get('chipset', '')} {specs.get('form_factor', '')}, margin={margin:+d}"
            ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ PSU ═══════════════════

def select_psu(
    min_wattage: int = 550,
    atx3x_required: bool = False,
    sfx_required: bool = False,
    budget_remaining: int = 999999,
    min_capability: str | None = None,
    max_acoustic_class: str | None = None,  # "semi_passive" | "active_low_noise" | None
) -> list[Candidate]:
    """STATE_5b: подбор БП с profile matching и акустическим фильтром.

    max_acoustic_class — максимально допустимый уровень шума:
      - "semi_passive": только БП с fan-stop (0 dBA в idle)
      - "active_low_noise": допускается тихий вентилятор (FDB/Hydro)
      - None (default): без фильтрации
    Фильтр relative: semi_passive < active_low_noise < active_standard.
    При max_acoustic_class="active_low_noise" пропускаются semi_passive И active_low_noise.
    """
    candidates = []
    psu_dir = CATALOG / "psu"
    if not psu_dir.exists():
        return candidates

    for f in sorted(psu_dir.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "psu":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        wattage = _extract_number(specs.get("wattage", "0"))
        if wattage < min_wattage:
            continue

        profiles = fm.get("profiles", {})
        if atx3x_required:
            if "atx_3x_transient_capable" not in profiles:
                continue

        # Acoustic filter
        ACOUSTIC_RANK = {"semi_passive": 1, "active_low_noise": 2, "active_standard": 3}
        psu_acoustic = specs.get("acoustic_profile")
        # Completeness check: PSU is acoustic_emitter per domain_impact_matrix →
        # if KB entry missing acoustic_profile → assign worst-case, record WARN
        completeness_warnings = []
        if psu_acoustic is None:
            psu_acoustic = "active_standard"  # worst-case per completeness_rules
            completeness_warnings.append(
                f"KB entry '{f.stem}' missing acoustic_profile — "
                f"assigned worst-case 'active_standard' (rank 3). "
                f"Update KB entry with actual acoustic data."
            )

        if max_acoustic_class:
            max_rank = ACOUSTIC_RANK.get(max_acoustic_class, 3)
            psu_rank = ACOUSTIC_RANK.get(psu_acoustic, 3)
            if psu_rank > max_rank:
                continue

        comp_level, margin = _margin_check(profiles, "psu", min_capability)
        if margin < 0:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="psu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"wattage": int(wattage), "atx_version": specs.get("atx_version", "")},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            margin=margin,
            rationale=f"{int(wattage)}W {specs.get('atx_version', '')}, margin={margin:+d}",
            warnings=completeness_warnings
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Cooling ═══════════════════

def select_cooler(
    cpu_tdp_w: int = 65,
    max_height_mm: int = 999,
    budget_remaining: int = 999999,
    min_capability: str | None = None,
) -> list[Candidate]:
    """STATE_5c: подбор кулера с profile matching."""
    candidates = []
    for sub in ["air", "liquid"]:
        cool_dir = CATALOG / "cooling" / sub
        if not cool_dir.exists():
            continue
        for f in sorted(cool_dir.glob("*.md")):
            if f.name == "index.md":
                continue
            fm = parse_frontmatter(f)
            if not fm or fm.get("type") != "cooling":
                continue
            price_data = fm.get("price_ru", {})
            price = price_data.get("median", 0)
            if not price or price > budget_remaining:
                continue

            specs = fm.get("specs", {})
            tdp_rating = _extract_number(specs.get("tdp_rating_w", specs.get("tdp", "0")))
            height = _extract_number(specs.get("height_mm", "0"))
            if height > max_height_mm:
                continue
            if tdp_rating < cpu_tdp_w:
                continue

            profiles = fm.get("profiles", {})
            comp_level, margin = _margin_check(profiles, "cooling", min_capability)
            if margin < 0:
                continue

            candidates.append(Candidate(
                id=fm.get("id", f.stem),
                type="cooling",
                title=fm.get("title", f.stem),
                price=price,
                specs={"tdp_rating": int(tdp_rating), "height_mm": int(height), "type": sub},
                profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
                margin=margin,
                rationale=f"TDP {int(tdp_rating)}W, {int(height)}mm, {sub}, margin={margin:+d}"
            ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Case ═══════════════════

def select_case(
    gpu_length_mm: int = 300,
    cooler_height_mm: int = 155,
    form_factor: str = "ATX",
    budget_remaining: int = 999999,
    min_capability: str | None = None,
) -> list[Candidate]:
    """STATE_5d: подбор корпуса с profile matching."""
    candidates = []
    case_dir = CATALOG / "case"
    if not case_dir.exists():
        return candidates

    for f in sorted(case_dir.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "case":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        max_gpu = _extract_number(specs.get("max_gpu_mm", "0"))
        max_cooler = _extract_number(specs.get("max_cooler_mm", "0"))
        if max_gpu < gpu_length_mm + GPU_INSTALL_CLEARANCE_MM:
            continue
        if max_cooler < cooler_height_mm + COOLER_SIDE_PANEL_CLEARANCE_MM:
            continue

        profiles = fm.get("profiles", {})
        comp_level, margin = _margin_check(profiles, "case", min_capability)
        if margin < 0:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="case",
            title=fm.get("title", f.stem),
            price=price,
            specs={"max_gpu_mm": int(max_gpu), "max_cooler_mm": int(max_cooler)},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            margin=margin,
            rationale=f"GPU ≤{int(max_gpu)}mm, cooler ≤{int(max_cooler)}mm, margin={margin:+d}"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Helpers ═══════════════════

def _extract_number(raw: Any) -> float:
    if raw is None:
        return 0
    if isinstance(raw, (int, float)):
        return float(raw)
    m = re.search(r"(\d+(?:\.\d+)?)", str(raw))
    return float(m.group(1)) if m else 0


def _extract_ram_capacity(specs: dict) -> int:
    """Extract total RAM capacity in GB from specs.
    Handles '32 GB (2×16 GB)', '2×16 GB (32 GB)', '32GB', etc.
    """
    raw = specs.get("capacity_gb", specs.get("capacity", "0"))
    if isinstance(raw, (int, float)):
        return int(raw)
    s = str(raw)
    # Try to find number in parentheses first (total capacity)
    m = re.search(r"\((\d+)\s*GB\)", s, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Then try "XX GB" pattern
    m = re.search(r"(\d+)\s*GB", s, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Fallback: first number
    return int(_extract_number(s))


def _extract_bus(specs: dict) -> int:
    bus_raw = specs.get("vram_bandwidth", specs.get("bus", ""))
    m = re.search(r"(\d+)-bit", str(bus_raw))
    return int(m.group(1)) if m else 0


def _extract_tgp(specs: dict) -> int:
    return int(_extract_number(specs.get("tbp") or specs.get("tgp") or specs.get("tdp") or 0))


def _extract_tdp(specs: dict) -> int:
    return int(_extract_number(specs.get("tdp") or 0))


def _extract_cores(specs: dict) -> int:
    cores_raw = specs.get("cores", specs.get("core_count", "0"))
    return int(_extract_number(cores_raw))


# ═══════════════════ Physical Compatibility Validation ═══════════════════

@dataclass
class PhysicalViolation:
    check: str          # e.g. "gpu_length"
    severity: str       # "BLOCK" | "WARN"
    message: str
    component: str      # component id
    constraint: str     # what was required
    actual: str         # what the component provides


def validate_physical_compatibility(
    gpu: dict | None = None,      # {"id": ..., "specs": {"length_mm": ..., "thickness_slots": ...}}
    cooler: dict | None = None,   # {"id": ..., "specs": {"height_mm": ...}}
    case: dict | None = None,     # {"id": ..., "specs": {"max_gpu_mm": ..., "max_cooler_mm": ..., "form_factor": ...}}
    mb: dict | None = None,       # {"id": ..., "specs": {"form_factor": ...}}
    psu: dict | None = None,      # {"id": ..., "specs": {"form_factor": ..., "sfx": bool}}
    sfx_required: bool = False,
) -> list[PhysicalViolation]:
    """Validate physical compatibility between components in a build.

    Checks (in order of severity):
      1. GPU length vs case max_gpu_mm (with install clearance)
      2. Cooler height vs case max_cooler_mm (with side panel clearance)
      3. MB form_factor vs case form_factor compatibility
      4. PSU form_factor vs case/sff requirement
      5. PCIe slot spacing vs GPU thickness (deferred to Skill 9)

    Returns list of PhysicalViolation. Empty list = PASS.
    """
    violations = []

    # 1. GPU length vs case
    if gpu and case:
        gpu_len = float(gpu.get("specs", {}).get("length_mm", gpu.get("specs", {}).get("length", 0)) or 0)
        case_max = float(case.get("specs", {}).get("max_gpu_mm", 0) or 0)
        if gpu_len > 0 and case_max > 0:
            required = gpu_len + GPU_INSTALL_CLEARANCE_MM
            if case_max < required:
                violations.append(PhysicalViolation(
                    check="gpu_length",
                    severity="BLOCK",
                    message=f"GPU {gpu['id']} ({gpu_len:.0f}mm) + {GPU_INSTALL_CLEARANCE_MM}mm clearance = {required:.0f}mm > case max {case_max:.0f}mm",
                    component=gpu.get("id", "?"),
                    constraint=f"max_gpu_mm ≥ {required:.0f}",
                    actual=f"case max_gpu_mm = {case_max:.0f}"
                ))

    # 2. Cooler height vs case
    if cooler and case:
        cooler_h = float(cooler.get("specs", {}).get("height_mm", 0) or 0)
        case_cooler_max = float(case.get("specs", {}).get("max_cooler_mm", 0) or 0)
        if cooler_h > 0 and case_cooler_max > 0:
            required = cooler_h + COOLER_SIDE_PANEL_CLEARANCE_MM
            if case_cooler_max < required:
                violations.append(PhysicalViolation(
                    check="cooler_height",
                    severity="BLOCK",
                    message=f"Cooler {cooler['id']} ({cooler_h:.0f}mm) + {COOLER_SIDE_PANEL_CLEARANCE_MM}mm clearance = {required:.0f}mm > case max {case_cooler_max:.0f}mm",
                    component=cooler.get("id", "?"),
                    constraint=f"max_cooler_mm ≥ {required:.0f}",
                    actual=f"case max_cooler_mm = {case_cooler_max:.0f}"
                ))

    # 3. MB form_factor vs case
    if mb and case:
        mb_ff = str(mb.get("specs", {}).get("form_factor", "")).upper()
        case_ff_raw = case.get("specs", {}).get("form_factor", "")
        # case form_factor may be a list like ["ATX", "mATX", "ITX"]
        if isinstance(case_ff_raw, list):
            case_ffs = [f.upper() for f in case_ff_raw]
        else:
            case_ffs = [str(case_ff_raw).upper()]
        if mb_ff and case_ffs and case_ffs != ['']:
            # ITX fits everywhere; mATX fits ATX/mATX; ATX only fits ATX
            if mb_ff == "ITX":
                pass  # always compatible
            elif mb_ff == "MATX" and "MATX" not in case_ffs and "ATX" not in case_ffs:
                violations.append(PhysicalViolation(
                    check="mb_form_factor",
                    severity="BLOCK",
                    message=f"MB {mb['id']} is {mb_ff} but case supports {case_ffs}",
                    component=mb.get("id", "?"),
                    constraint=f"case form_factor includes {mb_ff}",
                    actual=f"case form_factors = {case_ffs}"
                ))
            elif mb_ff == "ATX" and "ATX" not in case_ffs:
                violations.append(PhysicalViolation(
                    check="mb_form_factor",
                    severity="BLOCK",
                    message=f"MB {mb['id']} is {mb_ff} but case supports {case_ffs}",
                    component=mb.get("id", "?"),
                    constraint=f"case form_factor includes ATX",
                    actual=f"case form_factors = {case_ffs}"
                ))

    # 4. PSU form_factor vs case / SFF requirement
    if psu:
        psu_sfx = bool(psu.get("specs", {}).get("sfx", False))
        psu_ff = str(psu.get("specs", {}).get("form_factor", "")).upper()
        if sfx_required and not psu_sfx and "SFX" not in psu_ff:
            violations.append(PhysicalViolation(
                check="psu_form_factor",
                severity="BLOCK",
                message=f"SFF build requires SFX PSU but {psu['id']} is {psu_ff}",
                component=psu.get("id", "?"),
                constraint="PSU must be SFX form factor",
                actual=f"PSU form_factor = {psu_ff}"
            ))

    return violations


# ═══════════════════ Self-test ═══════════════════

if __name__ == "__main__":
    print("=== GPU (1440p ultra, 120K) ===")
    gpus = select_gpu(
        min_capability="balanced_performance_gpu",
        min_vram_gb=14,
        blocked_profiles=["sub_75w_slot_powered"],
        budget_remaining=120000,
        maut_gpu_weight=0.75
    )
    for g in gpus:
        print(f"  [{g.maut_score:.3f}] {g.id:25s} {g.price:>7,d}₽  margin={g.margin:+d}  {g.rationale}")

    print("\n=== CPU (AM5, 58K budget) ===")
    cpus = select_cpu(socket="AM5", budget_remaining=58000, maut_cpu_weight=0.25)
    for c in cpus[:5]:
        print(f"  [{c.maut_score:.3f}] {c.id:25s} {c.price:>7,d}₽  {c.rationale}")

    print("\n=== Storage (no sustained write, 10K) ===")
    ssds = select_storage(sustained_write_required=False, budget_remaining=10000)
    for s in ssds:
        print(f"  {s.id:30s} {s.price:>7,d}₽  {s.rationale}")

    print("\n=== PSU (750W+, ATX 3.x, 12K) ===")
    psus = select_psu(min_wattage=700, atx3x_required=False, budget_remaining=12000)
    for p in psus:
        print(f"  {p.id:30s} {p.price:>7,d}₽  {p.rationale}")

    print("\n=== Physical Compatibility Test ===")
    # Test 1: GPU barely fits (304 + 10 = 314 > 310)
    v = validate_physical_compatibility(
        gpu={"id": "rtx-5070", "specs": {"length_mm": 304}},
        case={"id": "tight-case", "specs": {"max_gpu_mm": 310}}
    )
    print(f"  GPU 304mm + 10mm > case 310mm: {'BLOCK' if v else 'PASS (unexpected)'}")

    # Test 2: GPU way too long
    v = validate_physical_compatibility(
        gpu={"id": "rtx-5090", "specs": {"length_mm": 348}},
        case={"id": "sff-case", "specs": {"max_gpu_mm": 320}}
    )
    print(f"  GPU 348mm + 10mm > case 320mm: {'BLOCK' if v else 'PASS (unexpected)'}")

    # Test 3: Cooler won't fit (160 + 5 = 165 > 158)
    v = validate_physical_compatibility(
        cooler={"id": "ak620", "specs": {"height_mm": 160}},
        case={"id": "tight-case", "specs": {"max_cooler_mm": 158}}
    )
    print(f"  Cooler 160mm + 5mm > case 158mm: {'BLOCK' if v else 'PASS (unexpected)'}")

    # Test 4: ATX PSU for SFF build
    v = validate_physical_compatibility(
        psu={"id": "pn850d", "specs": {"form_factor": "ATX"}},
        sfx_required=True
    )
    print(f"  ATX PSU for SFF build: {'BLOCK' if v else 'PASS (unexpected)'}")

    # Test 5: All good — PASS
    v = validate_physical_compatibility(
        gpu={"id": "rx-9070", "specs": {"length_mm": 285}},
        cooler={"id": "ak400", "specs": {"height_mm": 155}},
        case={"id": "cc560", "specs": {"max_gpu_mm": 380, "max_cooler_mm": 165, "form_factor": "ATX"}},
        mb={"id": "b650-s2h", "specs": {"form_factor": "mATX"}},
        psu={"id": "pn850d", "specs": {"form_factor": "ATX"}},
    )
    print(f"  Full compatibility: {'PASS' if not v else f'{len(v)} violations'}")
