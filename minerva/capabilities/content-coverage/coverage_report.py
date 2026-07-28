#!/usr/bin/env python3
"""
coverage_report.py — Content Production Coverage Report

Соединяет данные из двух складов (keyword-research + gaming DWH)
и возвращает сводку готовности к производству для контент-отдела.

Usage:
    python3 coverage_report.py --cpu amd-ryzen-7-9800x3d
"""

import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────
DWH_ROOT = Path(__file__).resolve().parent.parent.parent  # minerva/
KW_ROOT = Path("/root/projects/minerva-keyword-research")
PRICING_ROOT = Path("/root/.hermes/skills/warehouses/warehouse-pricing")

# ── 7 Decision Types ───────────────────────────────────────────────
DECISION_TYPES = {
    "UseCase": {
        "description": "Оправдан ли CPU для сценария",
        "mandatory_evidence": ["benchmark_at_stated_settings", "context_modifier"],
    },
    "ComponentChoice": {
        "description": "X против прямого конкурента",
        "mandatory_evidence": ["comparative_benchmark", "non_benchmark_tradeoff"],
    },
    "Timing": {
        "description": "Брать сейчас или ждать",
        "mandatory_evidence": ["price_history", "roadmap_or_successor_status"],
    },
    "UpgradePath": {
        "description": "Апгрейд с текущего CPU",
        "mandatory_evidence": ["generational_delta_benchmark", "socket_or_platform_reuse_check"],
    },
    "Constraint": {
        "description": "Укладывается ли в ограничение",
        "mandatory_evidence": ["thermal_or_power_measurement", "real_world_throttling_report"],
    },
    "PlatformCommitment": {
        "description": "Заходить на платформу сейчас или нет",
        "mandatory_evidence": ["platform_total_cost_estimate", "socket_lifecycle_roadmap"],
    },
    "MicroVariant": {
        "description": "Переплачивать за старший субвариант",
        "mandatory_evidence": ["price_delta", "performance_delta_equal_power", "user_tuning_required"],
    },
}

# ── Keyword → CPU mapping ─────────────────────────────────────────
CPU_SLUG_MAP = {
    "ryzen-7-9800x3d": "amd-ryzen-7-9800x3d",
    "ryzen-5-7500f": "amd-ryzen-5-7500f",
    "ryzen-5-7600x": "amd-ryzen-5-7600x",
    "ryzen-7-7800x3d": "amd-ryzen-7-7800x3d",
    "core-ultra-5-225f": "intel-core-ultra-5-225f",
    "ryzen-5-9600x": "amd-ryzen-5-9600x",
    "ryzen-7-7700": "amd-ryzen-7-7700",
    "core-ultra-7-265f": "intel-core-ultra-7-265f",
    "i5-14600kf": "intel-core-i5-14600k",
    "ryzen-9-7950x3d": "amd-ryzen-9-7950x3d",
    "i9-14900k": "intel-core-i9-14900k",
    "i5-13400f": "intel-core-i5-13400f",
    "i5-12400f": "intel-core-i5-12400f",
    "i5-12600kf": "intel-core-i5-12600k",
    "i5-14400f": "intel-core-i5-14400f",
}


def load_keywords():
    """Load all keywords from keyword-research DWH."""
    ctx = yaml.safe_load((KW_ROOT / "references/context-map.yaml").read_text())
    keywords = {}
    for k in ctx["context_map"]["dimensions"]["keyword"]["entities"]:
        dim_file = KW_ROOT / "warehouse/keyword-research/dim/keyword" / f"{k['id']}.yaml"
        if dim_file.exists():
            dim = yaml.safe_load(dim_file.read_text())
            attrs = dim.get("attributes", {})
            keywords[k["id"]] = {
                "canonical": k["canonical_name"],
                "volume": attrs.get("search_volume_estimate", 0),
                "intent": attrs.get("intent", "unknown"),
                "language": k.get("language", "en"),
            }
    return keywords


def load_gaming_observations(cpu_id: str):
    """Load all gaming observations for a CPU from Minerva gaming DWH."""
    obs_dir = DWH_ROOT / "warehouse/hardware/fact/cpu_observations"
    observations = []
    for f in obs_dir.glob(f"{cpu_id}*.yaml"):
        raw = yaml.safe_load(f.read_text())
        s = raw.get("source", {})
        m = raw.get("measures", {})
        meta = raw.get("meta", {})
        fps_avg = m.get("fps_avg")
        if fps_avg is None:
            continue  # skip synthetic-only
        observations.append({
            "game": s.get("game_title", "unknown"),
            "resolution": s.get("resolution", "unknown"),
            "preset": s.get("graphics_preset", "unknown"),
            "fps_avg": fps_avg,
            "fps_1pct_low": m.get("fps_1pct_low"),
            "confidence": meta.get("confidence", 0),
            "basis": meta.get("confidence_basis", "unknown"),
        })
    return observations


def find_competitor_in_dwh(cpu_id: str, keyword_canonical: str) -> str | None:
    """Check if a competitor CPU exists in DWH observations."""
    obs_dir = DWH_ROOT / "warehouse/hardware/fact/cpu_observations"
    # Try common competitor patterns from keyword names
    competitors = {
        "amd-ryzen-7-7800x3d": "7800x3d",
        "intel-core-i9-14900k": "14900k",
        "amd-ryzen-9-7950x3d": "7950x3d",
        "amd-ryzen-9-7950x": "7950x",
    }
    for comp_id, pattern in competitors.items():
        if pattern in keyword_canonical.lower():
            # Check if any observations exist for this competitor
            files = list(obs_dir.glob(f"{comp_id}*.yaml"))
            gaming_files = [f for f in files if f.name.count("-") >= 5]  # game observations
            if gaming_files:
                return comp_id
    return None


def classify_decision_type(kw_id: str, kw_data: dict) -> str:
    """Classify a keyword into one of 7 Decision types."""
    name = kw_id.lower().replace("-", " ")
    intent = kw_data.get("intent", "unknown")

    if "vs" in name:
        return "ComponentChoice"
    if intent in ("use_case_fitness", "performance_investigation"):
        return "UseCase"
    if "benchmark" in name or "gaming" in name or "test" in name:
        return "UseCase"
    if "motherboard" in name or "cooler" in name or "ram" in name or "build" in name:
        return "PlatformCommitment"
    if "bottleneck" in name or "pair" in name:
        return "PlatformCommitment"
    if "temperature" in name or "overclock" in name or "undervolt" in name:
        return "Constraint"
    if "underperforming" in name:
        return "Constraint"
    if "price" in name or "цена" in name:
        return "Timing"
    if "worth" in name or "buy" in name or "стоит" in name:
        if "vs" in name:
            return "ComponentChoice"
        return "Timing"
    if "review" in name:
        return "UseCase"
    # Default: product name only → UseCase (covers main product queries)
    return "UseCase"


def check_evidence(cpu_id: str, decision_type: str, observations: list, kw_data: dict) -> dict:
    """Check mandatory evidence for a Decision type."""
    mandatory = DECISION_TYPES[decision_type]["mandatory_evidence"]
    checks = {}

    has_gaming = len(observations) > 0
    has_1pct = any(o["fps_1pct_low"] is not None for o in observations)
    is_training = all(o["basis"] == "training_data" for o in observations)

    # Helper: check if any price data exists for a CPU
    def _has_price(cpu: str) -> bool:
        if PRICING_ROOT.exists():
            price_dir = PRICING_ROOT / "warehouse/pricing/fact/price"
            return len(list(price_dir.glob(f"{cpu}*.yaml"))) > 0
        return False

    # Helper: get socket for a CPU from dim/cpu
    def _get_socket(cpu: str) -> str | None:
        cpu_dim = DWH_ROOT / "warehouse/hardware/dim/cpu" / f"{cpu}.yaml"
        if cpu_dim.exists():
            dim = yaml.safe_load(cpu_dim.read_text())
            return dim.get("attributes", {}).get("socket")
        return None

    # Helper: check if socket has lifecycle roadmap
    def _socket_has_lifecycle(cpu: str) -> bool:
        socket_name = _get_socket(cpu)
        if not socket_name:
            return False
        socket_file = DWH_ROOT / "warehouse/hardware/dim/socket" / f"{socket_name}.yaml"
        if socket_file.exists():
            dim = yaml.safe_load(socket_file.read_text())
            lifecycle = dim.get("attributes", {}).get("lifecycle", {})
            return lifecycle.get("status") is not None and lifecycle.get("upgrade_note") is not None
        return False

    # Helper: check platform cost estimate (CPU price data exists)
    def _has_platform_cost(cpu: str) -> bool:
        return _has_price(cpu)

    if "benchmark_at_stated_settings" in mandatory:
        checks["benchmark_at_stated_settings"] = has_gaming
    if "comparative_benchmark" in mandatory:
        checks["comparative_benchmark"] = has_gaming
    if "generational_delta_benchmark" in mandatory:
        checks["generational_delta_benchmark"] = has_gaming
    if "performance_delta_equal_power" in mandatory:
        checks["performance_delta_equal_power"] = has_gaming
    if "thermal_or_power_measurement" in mandatory:
        pt_dir = DWH_ROOT / "warehouse/hardware/fact/power-thermal"
        pt_files = list(pt_dir.glob(f"{cpu_id}*.yaml")) if pt_dir.exists() else []
        checks["thermal_or_power_measurement"] = len(pt_files) > 0
    if "real_world_throttling_report" in mandatory:
        checks["real_world_throttling_report"] = False
    if "price_history" in mandatory:
        checks["price_history"] = _has_price(cpu_id)
    if "roadmap_or_successor_status" in mandatory:
        checks["roadmap_or_successor_status"] = _socket_has_lifecycle(cpu_id)
    if "platform_total_cost_estimate" in mandatory:
        # Check for motherboard dim entries for this socket
        cpu_socket = _get_socket(cpu_id)
        mb_dir = DWH_ROOT / "warehouse/hardware/dim/motherboard"
        mb_count = 0
        if mb_dir.exists() and cpu_socket:
            for mb_file in mb_dir.glob("*.yaml"):
                dim = yaml.safe_load(mb_file.read_text())
                if dim.get("attributes", {}).get("socket", "").lower() == cpu_socket.lower():
                    mb_count += 1
        checks["platform_total_cost_estimate"] = mb_count >= 1 and _has_price(cpu_id)
    if "socket_lifecycle_roadmap" in mandatory:
        checks["socket_lifecycle_roadmap"] = _socket_has_lifecycle(cpu_id)
    if "price_delta" in mandatory:
        checks["price_delta"] = _has_price(cpu_id)
    if "user_tuning_required" in mandatory:
        checks["user_tuning_required"] = False
    if "non_benchmark_tradeoff" in mandatory:
        checks["non_benchmark_tradeoff"] = has_gaming
    if "socket_or_platform_reuse_check" in mandatory:
        checks["socket_or_platform_reuse_check"] = _socket_has_lifecycle(cpu_id)
    if "context_modifier" in mandatory:
        checks["context_modifier"] = has_gaming and len([o for o in observations if o["resolution"] == "720p"]) > 0

    all_ok = all(checks.values())
    return {"status": "ready" if all_ok else "partial" if any(checks.values()) else "missing", "checks": checks, "note": "training_data" if is_training and has_gaming else ""}


def run(cpu_id: str):
    keywords = load_keywords()
    observations = load_gaming_observations(cpu_id)

    # Find matching keywords
    cpu_keywords = []
    for kw_id, kw_data in keywords.items():
        for kw_slug, mapped_id in CPU_SLUG_MAP.items():
            if mapped_id == cpu_id and kw_slug in kw_id.lower():
                cpu_keywords.append((kw_id, kw_data))
                break

    if not cpu_keywords:
        # Try generic match
        cpu_label = cpu_id.replace("-", " ").lower()
        for kw_id, kw_data in keywords.items():
            if cpu_label in kw_data["canonical"].lower():
                cpu_keywords.append((kw_id, kw_data))

    # Group by Decision type
    groups = defaultdict(list)
    for kw_id, kw_data in cpu_keywords:
        dtype = classify_decision_type(kw_id, kw_data)
        groups[dtype].append((kw_id, kw_data))

    # Print report
    has_any = len(cpu_keywords) > 0
    has_gaming = len(observations) > 0
    has_1pct = any(o["fps_1pct_low"] for o in observations)

    print(f"COVERAGE REPORT — {cpu_id}")
    print(f"Keyword DWH: {len(cpu_keywords)} queries found")
    print(f"Gaming DWH: {len(observations)} observations ({len(set(o['game'] for o in observations))} games)")
    print(f"Confidence: {'training_data' if all(o['basis']=='training_data' for o in observations) else 'mixed'}")
    print(f"1% Low available: {'yes' if has_1pct else 'no'}")

    total_f = sum(kw[1]["volume"] for kw in cpu_keywords)
    ready_f = 0
    partial_f = 0
    missing_f = 0

    for dtype in DECISION_TYPES:
        items = groups.get(dtype, [])
        if not items:
            continue

        dt = DECISION_TYPES[dtype]
        evidence = check_evidence(cpu_id, dtype, observations, items[0][1])
        status_icon = {"ready": "✅", "partial": "⚠️", "missing": "❌"}[evidence["status"]]
        f_total = sum(kw_data["volume"] for _, kw_data in items)

        print(f"\n{status_icon} {dtype} — {dt['description']} ({len(items)} queries, F={f_total:,})")

        if evidence["status"] == "ready":
            ready_f += f_total
        elif evidence["status"] == "partial":
            partial_f += f_total
        else:
            missing_f += f_total

        for kw_id, kw_data in sorted(items, key=lambda x: x[1]["volume"], reverse=True):
            print(f"    [{kw_data['language']}] {kw_data['canonical']} (F={kw_data['volume']:,})")

        # Show evidence gaps
        gaps = [k for k, v in evidence["checks"].items() if not v]
        if gaps:
            print(f"    → missing: {', '.join(gaps)}")
        if evidence["note"]:
            print(f"    → note: {evidence['note']}")

    print(f"\n{'═' * 60}")
    print(f"SUMMARY: Total F={total_f:,} | Ready: {ready_f:,} | Partial: {partial_f:,} | Missing: {missing_f:,}")
    print(f"Ready for production: {ready_f * 100 // total_f if total_f else 0}% of search demand")

    if not has_gaming:
        print("\n❌ BLOCKED: No gaming data in DWH — all Decision types require benchmark acquisition first")
    elif has_gaming and not has_1pct:
        print("\n⚠️ Gaming data present but 1% Low values missing — UseCase and ComponentChoice partial only")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Content Production Coverage Report")
    parser.add_argument("--cpu", required=True, help="CPU ID (e.g., amd-ryzen-7-9800x3d)")
    args = parser.parse_args()
    run(args.cpu)
