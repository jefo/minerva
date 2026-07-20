#!/usr/bin/env python3
"""
compute.py — DWH → CPU Assessment Profiles

Reads cpu_observations and dim/cpu from DWH, computes per-workload
assessments, writes profile YAML to marts/assessment/cpu/profiles/.

Scenarios handled:
  - 1080p-low, 1440p-ultra, 720p-low (gaming)
  - Geekbench 6 ST / MT (synthetic — valid data)
  - Cinebench R23 (synthetic — DEFECTIVE, skipped)
  - Blender, 7-Zip (productivity)

Usage:
    python3 compute.py --domain hardware
    python3 compute.py --domain hardware --cpu amd-ryzen-7-7800x3d
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────
DWH_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # minerva/
MART_ROOT = DWH_ROOT / "marts" / "assessment" / "cpu"
PROFILES_DIR = MART_ROOT / "profiles"

OBSERVATIONS_DIR = DWH_ROOT / "warehouse" / "hardware" / "fact" / "cpu_observations"
DIM_CPU_DIR = DWH_ROOT / "warehouse" / "hardware" / "dim" / "cpu"

# ── Parsing ────────────────────────────────────────────────────────

def parse_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def classify_observation(data: dict, filename: str = "") -> str:
    """Return scenario classification."""
    source = data.get("source", {})
    measures = data.get("measures", {})
    scenario = str(source.get("benchmark_scenario", "")).lower()
    
    # Detect power-thermal by measures or filename
    if "power_draw_w" in measures and "temp_c" in measures:
        return "meta-power"
    if "power-thermal" in filename.lower():
        return "meta-power"
    
    if "1080p" in scenario and "low" in scenario:
        return "gaming-1080p"
    if "1440p" in scenario and "ultra" in scenario:
        return "gaming-1440p"
    if "720p" in scenario and "low" in scenario:
        return "gaming-720p"
    if "geekbench" in scenario:
        return "synthetic-geekbench-st" if "st" in scenario else "synthetic-geekbench-mt"
    if "cinebench" in scenario:
        return "synthetic-cinebench-st" if "1t" in scenario else "synthetic-cinebench-mt"
    if "blender" in scenario:
        return "productivity-blender"
    if "7zip" in scenario or "7-zip" in scenario:
        return "productivity-7zip"
    return "unknown"


def parse_observation(path: Path) -> Optional[dict]:
    """Parse a cpu_observation file. Returns dict with classification."""
    try:
        data = parse_yaml(path)
    except Exception:
        return None
    
    fact = data.get("fact", {})
    source = data.get("source", {})
    measures = data.get("measures", {})
    meta = data.get("meta", {})
    
    # Normalize measure names
    normalized = {}
    for key, val in measures.items():
        if key == "fps_1_percent_low":
            normalized["fps_1pct_low"] = val
        elif key == "score":
            # Detect Cinebench defect
            if isinstance(val, str) and not val.replace(".", "").replace("-", "").isdigit():
                normalized["score"] = None
                normalized["_defect"] = val
            else:
                normalized["score"] = val
        else:
            normalized[key] = val
    
    scenario = classify_observation(data, str(path))
    
    # Extract game name from gaming observations
    game = str(source.get("game_title", ""))
    
    # Normalize game titles across ETL sources
    GAME_TITLE_NORMALIZE = {
        "baldurs gate 3": "Baldur's Gate 3",
        "baldur's gate 3": "Baldur's Gate 3",
        "counter strike 2": "Counter-Strike 2",
        "counter-strike 2": "Counter-Strike 2",
        "cyberpunk 2077": "Cyberpunk 2077",
        "hogwarts legacy": "Hogwarts Legacy",
        "starfield": "Starfield",
    }
    game_lower = game.strip().lower()
    if game_lower in GAME_TITLE_NORMALIZE:
        game = GAME_TITLE_NORMALIZE[game_lower]
    
    return {
        "cpu_id": source.get("cpu", ""),
        "fact_type": fact.get("type", ""),
        "scenario": scenario,
        "game": str(game),
        "measures": normalized,
        "confidence": meta.get("confidence"),
        "confidence_basis": str(meta.get("confidence_basis", "")),
        "note": str(meta.get("note", "")),
        "path": str(path),
    }


def parse_cpu_dim(path: Path) -> Optional[dict]:
    """Parse a dim/cpu YAML file."""
    try:
        data = parse_yaml(path)
    except Exception:
        return None
    
    dim = data.get("dimension", {})
    attrs = data.get("attributes", {})
    compute = attrs.get("compute", {})
    cache = attrs.get("cache", {})
    memory = attrs.get("memory", {})
    pcie = attrs.get("pcie", {})
    power = attrs.get("power", {})
    release = attrs.get("release", {})
    oc = attrs.get("platform", {}).get("overclocking", {})
    
    # Handle hybrid architecture (Intel P-core + E-core)
    p_cores = compute.get("p_cores")
    e_cores = compute.get("e_cores")
    total_cores = compute.get("total_cores") or compute.get("cores")
    threads = compute.get("threads")
    
    if p_cores is not None and e_cores is not None:
        core_label = f"{p_cores}P+{e_cores}E ({total_cores}C/{threads}T)"
        architecture_note = "Гибридная архитектура: P-cores для нагрузки, E-cores для фона."
    else:
        core_label = f"{total_cores}C/{threads}T" if total_cores else "?C/?T"
        architecture_note = ""
    
    return {
        "id": dim.get("id", ""),
        "label": dim.get("canonical_name", ""),
        "vendor": attrs.get("vendor", ""),
        "family": attrs.get("family", ""),
        "generation": attrs.get("generation"),
        "socket": attrs.get("socket", ""),
        "architecture": attrs.get("architecture", ""),
        "cores": total_cores,
        "p_cores": p_cores,
        "e_cores": e_cores,
        "threads": threads,
        "core_label": core_label,
        "architecture_note": architecture_note,
        "base_clock_mhz": compute.get("base_clock_mhz") or compute.get("p_core_base_clock_mhz"),
        "boost_clock_mhz": compute.get("boost_clock_mhz") or compute.get("p_core_boost_clock_mhz"),
        "tdp_w": power.get("tdp_w"),
        "cache_l3_kb": cache.get("l3_kb"),
        "cache_l3_type": cache.get("l3_type"),
        "memory_type": memory.get("type"),
        "pcie_version": pcie.get("version"),
        "release_date": release.get("date"),
        "msrp_usd": release.get("msrp_usd"),
        "oc_cpu_ratio": oc.get("cpu_ratio"),
        "oc_note": oc.get("notes"),
    }


# ── Aggregation ────────────────────────────────────────────────────

def stats(values: list) -> dict:
    """Compute mean, min, max, stdev."""
    if not values:
        return {"mean": None, "min": None, "max": None, "stdev": None}
    n = len(values)
    mean = sum(values) / n
    mn, mx = min(values), max(values)
    stdev = ((sum((v - mean)**2 for v in values) / (n - 1)) ** 0.5) if n > 1 else 0.0
    return {
        "mean": round(mean, 1),
        "min": round(mn, 1),
        "max": round(mx, 1),
        "stdev": round(stdev, 1),
    }


def aggregate_gaming_scenario(observations: list, scenario_tag: str) -> dict:
    """Aggregate gaming observations for a specific scenario (1080p, 1440p, 720p)."""
    matching = [o for o in observations if o["scenario"] == scenario_tag]
    
    if not matching:
        return {"games_tested": 0, "note": f"no {scenario_tag} data"}
    
    games = []
    fps_avg_vals, fps_1pct_vals = [], []
    
    for obs in matching:
        m = obs["measures"]
        avg, low = m.get("fps_avg"), m.get("fps_1pct_low")
        if avg is None or low is None:
            continue
        fps_avg_vals.append(avg)
        fps_1pct_vals.append(low)
        games.append({"title": obs["game"], "fps_avg": avg, "fps_1pct_low": low})
    
    if not games:
        return {"games_tested": 0, "note": f"no valid {scenario_tag} measurements"}
    
    return {
        "games_tested": len(games),
        "games": games,
        "summary": {
            "fps_avg": stats(fps_avg_vals),
            "fps_1pct_low": stats(fps_1pct_vals),
        }
    }


def margin_pct(current, threshold):
    if current is None or threshold is None or threshold == 0:
        return None
    return round((current - threshold) / threshold * 100, 1)


def target_margins(stats_dict: dict, games: list, targets: list) -> list:
    """For each target threshold, compute mean margin + worst/best game margins."""
    results = []
    for t in targets:
        metric = t["metric"]
        threshold = t["value"]
        mean_val = stats_dict.get("mean") if stats_dict else None
        
        entry = {
            "id": t["id"],
            "label": t["label"],
            "metric": metric,
            "threshold": threshold,
            "unit": t.get("unit", ""),
        }
        
        if mean_val is not None:
            entry["mean"] = mean_val
            entry["margin_pct"] = margin_pct(mean_val, threshold)
        
        # Per-game worst/best
        if games:
            key = "fps_1pct_low" if "1pct" in metric or "1_percent" in metric else "fps_avg"
            game_vals = [(g["title"], g[key]) for g in games if g.get(key) is not None]
            if game_vals:
                worst = min(game_vals, key=lambda x: x[1])
                best = max(game_vals, key=lambda x: x[1])
                entry["worst_game"] = {"game": worst[0], "value": worst[1], "margin_pct": margin_pct(worst[1], threshold)}
                if worst != best:
                    entry["best_game"] = {"game": best[0], "value": best[1], "margin_pct": margin_pct(best[1], threshold)}
        
        results.append(entry)
    return results


# ── Main compute ───────────────────────────────────────────────────

COMPETITIVE_TARGETS = [
    {"id": "144hz", "label": "Плавный геймплей (144Hz)", "metric": "fps_1pct_low", "value": 144, "unit": "fps"},
    {"id": "240hz", "label": "Киберспорт (240Hz)", "metric": "fps_1pct_low", "value": 240, "unit": "fps"},
    {"id": "360hz", "label": "Профессиональный (360Hz)", "metric": "fps_1pct_low", "value": 360, "unit": "fps"},
]

AAA_TARGETS = [
    {"id": "60fps", "label": "Минимально играбельно", "metric": "fps_1pct_low", "value": 60, "unit": "fps"},
    {"id": "120fps", "label": "Плавно (120Hz)", "metric": "fps_1pct_low", "value": 120, "unit": "fps"},
]


def compute_profiles(domain: str, cpu_filter: Optional[str] = None):
    
    obs_dir = DWH_ROOT / f"warehouse/{domain}/fact/cpu_observations"
    dim_dir = DWH_ROOT / f"warehouse/{domain}/dim/cpu"
    
    # ── Parse observations ────────────────────────────────────
    obs_by_cpu = defaultdict(list)
    for path in sorted(obs_dir.glob("*.yaml")):
        obs = parse_observation(path)
        if obs and obs["cpu_id"]:
            if cpu_filter and obs["cpu_id"] != cpu_filter:
                continue
            obs_by_cpu[obs["cpu_id"]].append(obs)
    
    # ── Parse dims ────────────────────────────────────────────
    dims = {}
    for path in sorted(dim_dir.glob("*.yaml")):
        dim = parse_cpu_dim(path)
        if dim and dim["id"]:
            dims[dim["id"]] = dim
    
    # ── Parse socket dims (for lifecycle) ─────────────────────
    socket_dir = DWH_ROOT / f"warehouse/{domain}/dim/socket"
    socket_dims = {}
    if socket_dir.exists():
        for path in sorted(socket_dir.glob("*.yaml")):
            try:
                data = parse_yaml(path)
                sid = data.get("dimension", {}).get("id", "")
                lifecycle = data.get("attributes", {}).get("lifecycle", {})
                if sid and lifecycle:
                    socket_dims[sid] = lifecycle
            except Exception:
                pass
    
    print(f"Parsed {sum(len(v) for v in obs_by_cpu.values())} observations for {len(obs_by_cpu)} CPUs, {len(dims)} dims, {len(socket_dims)} socket lifecycles")
    
    # ── Generate profiles ─────────────────────────────────────
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    generated = 0
    
    for cpu_id in sorted(obs_by_cpu.keys()):
        observations = obs_by_cpu[cpu_id]
        dim = dims.get(cpu_id)
        if not dim:
            continue
        
        # ── Classify observations ─────────────────────────────
        by_scenario = defaultdict(list)
        for o in observations:
            by_scenario[o["scenario"]].append(o)
        
        # Gaming scenarios
        g1080 = aggregate_gaming_scenario(observations, "gaming-1080p")
        g1440 = aggregate_gaming_scenario(observations, "gaming-1440p")
        g720  = aggregate_gaming_scenario(observations, "gaming-720p")
        
        has_gaming = g1080["games_tested"] > 0
        
        # Geekbench
        gb_st_obs = [o for o in observations if o["scenario"] == "synthetic-geekbench-st"]
        gb_mt_obs = [o for o in observations if o["scenario"] == "synthetic-geekbench-mt"]
        gb_st = gb_st_obs[0]["measures"].get("score") if gb_st_obs else None
        gb_mt = gb_mt_obs[0]["measures"].get("score") if gb_mt_obs else None
        
        has_synthetic = gb_st is not None or gb_mt is not None
        
        # Productivity
        blender_obs = [o for o in observations if o["scenario"] == "productivity-blender"]
        zip7_obs    = [o for o in observations if o["scenario"] == "productivity-7zip"]
        blender_sec = blender_obs[0]["measures"].get("score") if blender_obs else None
        zip7_score  = zip7_obs[0]["measures"].get("score") if zip7_obs else None
        
        has_productivity = blender_sec is not None or zip7_score is not None
        
        # Power & Thermal (from power-thermal observations under MT load)
        power_obs = [o for o in observations if o["scenario"] == "meta-power"]
        power_draw = power_obs[0]["measures"].get("power_draw_w") if power_obs else None
        temp_c = power_obs[0]["measures"].get("temp_c") if power_obs else None
        has_power = power_draw is not None
        
        # Cinebench — defective
        has_cinebench_defect = any("synthetic-cinebench" in o["scenario"] for o in observations)
        
        # ── Data quality ──────────────────────────────────────
        confidences = [o["confidence"] for o in observations if o["confidence"] is not None]
        mean_conf = round(sum(confidences) / len(confidences), 2) if confidences else None
        
        gaps = []
        if not has_gaming:
            gaps.append("no gaming data")
        if not has_synthetic:
            gaps.append("no synthetic (Geekbench) data")
        if has_cinebench_defect:
            gaps.append("Cinebench R23 data defective — string labels in score field")
        if not has_productivity:
            gaps.append("no productivity data")
        
        coverage = "none"
        if has_gaming or has_synthetic:
            coverage = "partial"
            if has_gaming and has_synthetic and has_productivity:
                coverage = "good"
        
        dq = {
            "coverage": coverage,
            "gaps": gaps,
            "confidence": mean_conf,
            "basis": "training_data",
            "note": "Все значения — training data estimates. Реальные бенчмарки могут отличаться на ±10-15%."
        }
        
        # ── Platform ──────────────────────────────────────────
        socket_lifecycle = socket_dims.get(dim.get("socket", ""), {})
        platform = {
            "socket": dim.get("socket", ""),
            "socket_lifecycle": socket_lifecycle.get("status", "unknown"),
            "socket_upgrade_note": socket_lifecycle.get("upgrade_note", ""),
            "architecture": dim.get("architecture", ""),
            "architecture_note": dim.get("architecture_note", ""),
            "cores": dim.get("cores"),
            "p_cores": dim.get("p_cores"),
            "e_cores": dim.get("e_cores"),
            "threads": dim.get("threads"),
            "core_label": dim.get("core_label", "?C/?T"),
            "base_clock_mhz": dim.get("base_clock_mhz"),
            "boost_clock_mhz": dim.get("boost_clock_mhz"),
            "tdp_w": dim.get("tdp_w"),
            "power_draw_mt_w": power_draw,
            "temp_mt_c": temp_c,
            "power_note": (
                f"Спецификация TDP: {dim.get('tdp_w', '?')}W. "
                f"Реальное потребление под MT-нагрузкой: {power_draw}W. "
                f"Разница: {power_draw - dim.get('tdp_w', 0):+d}W."
            ) if has_power and dim.get("tdp_w") else (
                "Нет данных о реальном энергопотреблении. TDP из спецификации."
            ),
            "cache_l3": f"{dim.get('cache_l3_kb','?')//1024 if dim.get('cache_l3_kb') else '?'}MB" + (f" ({dim['cache_l3_type']})" if dim.get("cache_l3_type") else ""),
            "memory": dim.get("memory_type", ""),
            "pcie": dim.get("pcie_version", ""),
            "release": dim.get("release_date", ""),
            "msrp_usd": dim.get("msrp_usd"),
        }
        
        # ── Assemble profile ──────────────────────────────────
        workloads = {}
        
        # Competitive gaming
        if has_gaming:
            # Prefer 1080p for competitive, fall back to whatever exists
            primary = g1080 if g1080["games_tested"] > 0 else g720 if g720["games_tested"] > 0 else g1440
            s = primary.get("summary", {})
            gl = primary.get("games", [])
            low_stats = s.get("fps_1pct_low", {})
            
            workloads["competitive-gaming"] = {
                "scenario": "1080p Low (CPU-bound)" if g1080["games_tested"] > 0 else "720p Low (extreme CPU-bound)" if g720["games_tested"] > 0 else "1440p Ultra",
                "measurements": primary,
                "targets": target_margins(low_stats, gl, COMPETITIVE_TARGETS),
            }
            
            # AAA gaming — prefer 1440p ultra, fall back to 1080p
            aaa_primary = g1440 if g1440["games_tested"] > 0 else g1080
            aaa_s = aaa_primary.get("summary", {})
            aaa_gl = aaa_primary.get("games", [])
            aaa_low_stats = aaa_s.get("fps_1pct_low", {})
            
            workloads["aaa-gaming"] = {
                "scenario": "1440p Ultra (mixed-bound)" if g1440["games_tested"] > 0 else "1080p Low (CPU-bound)",
                "measurements": aaa_primary,
                "targets": target_margins(aaa_low_stats, aaa_gl, AAA_TARGETS),
                "note": "1440p Ultra — GPU частично ограничивает, разница между CPU сжата." if g1440["games_tested"] > 0 else "1080p Low — верхняя граница CPU-производительности. На высоких настройках разница меньше.",
            }
        else:
            workloads["competitive-gaming"] = {"data_status": "blocked", "note": "no gaming data"}
            workloads["aaa-gaming"] = {"data_status": "blocked", "note": "no gaming data"}
        
        # Content creation (Geekbench MT + Blender)
        cc = {}
        if gb_mt is not None:
            cc["geekbench_mt"] = gb_mt
        if blender_sec is not None:
            cc["blender_classroom_sec"] = blender_sec
            cc["blender_note"] = "Секунды на рендер сцены Classroom. Меньше = лучше."
        if zip7_score is not None:
            cc["zip7_mips"] = zip7_score
        if gb_mt is not None and power_draw is not None:
            cc["perf_per_watt"] = round(gb_mt / power_draw, 1)
            cc["perf_per_watt_note"] = "Баллов Geekbench MT на 1 Ватт реального потребления. Выше = эффективнее. Training data estimate."
        if cc:
            cc["data_status"] = "partial"
            workloads["content-creation"] = cc
        else:
            workloads["content-creation"] = {"data_status": "blocked", "note": "no Geekbench MT or productivity data"}
        
        # Software development (Geekbench ST + MT)
        sd = {}
        if gb_st is not None:
            sd["geekbench_st"] = gb_st
        if gb_mt is not None:
            sd["geekbench_mt"] = gb_mt
        if sd:
            sd["data_status"] = "partial"
            sd["note"] = "Geekbench 6 ST — прокси отзывчивости IDE. MT — прокси времени компиляции."
            workloads["software-development"] = sd
        else:
            workloads["software-development"] = {"data_status": "blocked", "note": "no Geekbench data"}
        
        # Streaming gaming
        gaming_ref = None
        if has_gaming:
            primary = g1080 if g1080["games_tested"] > 0 else g1440
            s = primary.get("summary", {})
            gaming_ref = s.get("fps_1pct_low", {}).get("mean")
        
        workloads["streaming-gaming"] = {
            "data_status": "partial",
            "note": "Нет прямых замеров gaming+OBS. Ядра — прокси многозадачности.",
            "cores": dim.get("cores"),
            "threads": dim.get("threads"),
            "gaming_1pct_low_mean": gaming_ref,
        }
        
        # Budget gaming
        workloads["budget-gaming"] = {
            "data_status": "blocked",
            "note": "Pricing warehouse не заполнен. FPS/₽ недоступен.",
            "gaming_fps_avg_mean": g1080.get("summary", {}).get("fps_avg", {}).get("mean") if has_gaming else None,
        }
        
        # Defects section
        defects = []
        if has_cinebench_defect:
            defects.append({
                "type": "synthetic_data_defect",
                "affected": "Cinebench R23 ST/MT",
                "detail": "Поле score содержит строки-лейблы ('synthetic-mt', 'synthetic-1t') вместо чисел. Geekbench 6 используется как замена.",
            })
        
        profile = {
            "assessment": {
                "cpu_id": cpu_id,
                "cpu_label": dim.get("label", cpu_id),
                "generated": datetime.utcnow().strftime("%Y-%m-%d"),
                "dwh_observations": len(observations),
                "data_quality": dq,
                "defects": defects,
                "platform": platform,
                "workloads": workloads,
            }
        }
        
        # Write
        out_path = PROFILES_DIR / f"{cpu_id}.yaml"
        with open(out_path, "w") as f:
            f.write(f"# CPU Assessment Profile — {dim.get('label', cpu_id)}\n")
            f.write(f"# Auto-generated from DWH by compute.py\n")
            f.write(f"# Generated: {datetime.utcnow().isoformat()}\n\n")
            yaml.dump(profile, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        
        generated += 1
        g = g1080["games_tested"] + g1440["games_tested"] + g720["games_tested"]
        gb_st_str = str(gb_st) if gb_st is not None else '--'
        gb_mt_str = str(gb_mt) if gb_mt is not None else '--'
        bl_str = str(blender_sec) if blender_sec is not None else '--'
        print(f"  OK  {cpu_id:45s} g={g:2d} gb_st={gb_st_str:>5s} gb_mt={gb_mt_str:>5s} bl={bl_str:>5s}")
    
    print(f"\nGenerated {generated} profiles → {PROFILES_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DWH → CPU Assessment Profiles")
    parser.add_argument("--domain", default="hardware", help="DWH domain")
    parser.add_argument("--cpu", help="Single CPU ID")
    args = parser.parse_args()
    compute_profiles(args.domain, args.cpu)
