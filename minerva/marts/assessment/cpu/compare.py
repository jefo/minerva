#!/usr/bin/env python3
"""
compare.py — Pairwise CPU Comparison using Comparison Framework.

Loads two profiles + comparison_framework.yaml → computes comparison view.
Demonstrates that the DSS atoms + molecules pattern works.

Usage:
    python3 compare.py amd-ryzen-7-7800x3d intel-core-i9-14900k
"""

import sys
import yaml
from pathlib import Path
from typing import Optional

MART_ROOT = Path(__file__).resolve().parent
PROFILES_DIR = MART_ROOT / "profiles"
FRAMEWORK_FILE = MART_ROOT / "comparison_framework.yaml"


def load_profile(cpu_id: str) -> dict:
    path = PROFILES_DIR / f"{cpu_id}.yaml"
    if not path.exists():
        print(f"ERROR: profile not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def load_framework() -> dict:
    with open(FRAMEWORK_FILE) as f:
        data = yaml.safe_load(f)
    return data["framework"]


def get_workload_value(profile: dict, workload_id: str, metric: str) -> Optional[float]:
    """Extract a metric value from a profile's workload."""
    wl = profile.get("assessment", {}).get("workloads", {}).get(workload_id, {})
    
    # Direct field (geekbench_st, geekbench_mt, blender_classroom_sec)
    if metric in wl:
        val = wl[metric]
        if isinstance(val, (int, float)):
            return float(val)
    
    # From measurements.summary (primary source for gaming metrics)
    measurements = wl.get("measurements", {})
    summary = measurements.get("summary", {})
    
    if metric == "fps_avg_mean":
        return summary.get("fps_avg", {}).get("mean")
    if metric == "fps_1pct_low_mean":
        result = summary.get("fps_1pct_low", {}).get("mean")
        if result is not None:
            return result
    
    # Fallback: direct field in workload (streaming-gaming)
    if metric == "fps_1pct_low_mean":
        return wl.get("gaming_1pct_low_mean")
    
    return None


def delta_pct(a: float, b: float) -> float:
    """Percentage delta: positive = A leads, negative = B leads."""
    if a is None or b is None or b == 0:
        return None
    return round((a - b) / b * 100, 1)


def classify_magnitude(delta: float, metric_type: str, thresholds: dict) -> str:
    """Classify delta magnitude: decisive, significant, noticeable, marginal."""
    abs_delta = abs(delta)
    t = thresholds.get(metric_type, thresholds.get("gaming_fps", {}))
    
    if abs_delta >= t.get("decisive", 15):
        return "decisive"
    elif abs_delta >= t.get("significant", 8):
        return "significant"
    elif abs_delta >= t.get("noticeable", 3):
        return "noticeable"
    else:
        return "marginal"


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 compare.py <cpu_id_a> <cpu_id_b>")
        print("Example: python3 compare.py amd-ryzen-7-7800x3d intel-core-i9-14900k")
        sys.exit(1)
    
    cpu_a_id = sys.argv[1]
    cpu_b_id = sys.argv[2]
    
    profile_a = load_profile(cpu_a_id)
    profile_b = load_profile(cpu_b_id)
    fw = load_framework()
    
    a = profile_a["assessment"]
    b = profile_b["assessment"]
    
    a_label = a["cpu_label"]
    b_label = b["cpu_label"]
    
    print(f"\n{'='*70}")
    print(f"  {a_label}")
    print(f"  vs")
    print(f"  {b_label}")
    print(f"{'='*70}\n")
    
    # ── Data quality warning ──────────────────────────────────
    print("DATA QUALITY")
    print(f"  {a_label}: coverage={a['data_quality']['coverage']}, confidence={a['data_quality']['confidence']}")
    print(f"  {b_label}: coverage={b['data_quality']['coverage']}, confidence={b['data_quality']['confidence']}")
    
    integrity_rules = fw.get("comparison_integrity", [])
    for rule in integrity_rules:
        if rule["rule"] == "same_source":
            if a["data_quality"]["basis"] == b["data_quality"]["basis"] == "training_data":
                print(f"  ⚠ {rule['action']}")
        if rule["rule"] == "coverage_asymmetry":
            a_has = a["data_quality"]["coverage"] != "none"
            b_has = b["data_quality"]["coverage"] != "none"
            if a_has != b_has:
                print(f"  ⚠ {rule['action']}")
    
    # ── Metric deltas per workload ────────────────────────────
    workloads_to_compare = [
        {
            "id": "competitive-gaming",
            "section": "COMPETITIVE GAMING",
            "metric": "fps_1pct_low_mean",
            "metric_label": "1% Low FPS (mean across games)",
            "unit": "fps",
            "scenario_label": a.get("workloads", {}).get("competitive-gaming", {}).get("scenario", ""),
            "threshold_type": "gaming_fps",
        },
        {
            "id": "aaa-gaming",
            "section": "AAA GAMING",
            "metric": "fps_1pct_low_mean",
            "metric_label": "1% Low FPS (mean across games)",
            "unit": "fps",
            "scenario_label": a.get("workloads", {}).get("aaa-gaming", {}).get("scenario", ""),
            "threshold_type": "gaming_fps",
        },
    {
        "id": "content-creation",
        "section": "CONTENT CREATION",
        "metric": "geekbench_mt",
        "metric_label": "Geekbench 6 MT",
        "unit": "score",
        "scenario_label": "",
        "threshold_type": "synthetic_score",
    },
    {
        "id": "content-creation",
        "section": "EFFICIENCY",
        "metric": "perf_per_watt",
        "metric_label": "Perf/Watt (Geekbench MT / power draw)",
        "unit": "score/W",
        "scenario_label": "",
        "threshold_type": "synthetic_score",
    },
        {
            "id": "software-development",
            "section": "SOFTWARE DEVELOPMENT",
            "metric": "geekbench_st",
            "metric_label": "Geekbench 6 ST (IDE responsiveness)",
            "unit": "score",
            "scenario_label": "",
            "threshold_type": "synthetic_score",
        },
    ]
    
    for wl in workloads_to_compare:
        wid = wl["id"]
        wl_a = a.get("workloads", {}).get(wid, {})
        wl_b = b.get("workloads", {}).get(wid, {})
        
        if wl_a.get("data_status") == "blocked" or wl_b.get("data_status") == "blocked":
            continue
        
        val_a = get_workload_value(profile_a, wid, wl["metric"])
        val_b = get_workload_value(profile_b, wid, wl["metric"])
        
        if val_a is None or val_b is None:
            continue
        
        delta = delta_pct(val_a, val_b)
        if delta is None:
            continue
        
        magnitude = classify_magnitude(delta, wl["threshold_type"], fw["delta_thresholds"])
        
        leader = a_label if delta > 0 else b_label if delta < 0 else "—"
        direction = abs(delta)
        
        print(f"\n── {wl['section']} ──")
        if wl["scenario_label"]:
            print(f"   Scenario: {wl['scenario_label']}")
        print(f"   {wl['metric_label']}:")
        print(f"     {a_label:35s} {val_a:>8.1f} {wl['unit']}")
        print(f"     {b_label:35s} {val_b:>8.1f} {wl['unit']}")
        print(f"     Delta: {delta:+.1f}% → {leader} leads ({magnitude})")
        
        # Per-game dispersion for gaming workloads
        if wid in ("competitive-gaming", "aaa-gaming"):
            measurements = wl_a.get("measurements", {})
            games_a = measurements.get("games", [])
            measurements_b = wl_b.get("measurements", {})
            games_b = measurements_b.get("games", [])
            
            if games_a and games_b:
                # Build lookup for B
                b_lookup = {g.get("title", "").lower(): g for g in games_b}
                
                a_wins = 0
                total = 0
                print(f"\n   Per-game 1% Low:")
                for ga in games_a:
                    title = ga.get("title", "")
                    gb = b_lookup.get(title.lower())
                    if gb:
                        total += 1
                        a_val = ga.get("fps_1pct_low")
                        b_val = gb.get("fps_1pct_low")
                        if a_val and b_val:
                            g_delta = delta_pct(a_val, b_val)
                            if g_delta and g_delta > 0:
                                a_wins += 1
                            leader_mark = "←" if (g_delta and g_delta > 0) else "→" if (g_delta and g_delta < 0) else "="
                            print(f"     {title:30s} {a_val:>5.0f} vs {b_val:<5.0f}  {g_delta:+5.1f}%  {leader_mark}")
                
                if total > 0:
                    a_win_pct = a_wins / total * 100
                    for dc in fw.get("dispersion_classification", {}).values():
                        rule = dc["rule"]
                        if "≥80%" in rule and a_win_pct >= 80:
                            disp = dc
                            break
                        elif "50-80%" in rule and 50 <= a_win_pct < 80:
                            disp = dc
                            break
                        else:
                            disp = dc
                    print(f"   Dispersion: {a_wins}/{total} games ({a_win_pct:.0f}%) → {disp['label']}")
                    print(f"     {disp['interpretation']}")
    
    # ── Tradeoff axes ─────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("TRADEOFF AXES")
    
    for axis in fw.get("tradeoff_axes", []):
        axis_id = axis["id"]
        axis_a_wl = axis["axis_a"]["workloads"][0]
        axis_a_metric = axis["axis_a"]["metric"]
        axis_b_wl = axis["axis_b"]["workloads"][0]
        axis_b_metric = axis["axis_b"]["metric"]
        
        val_a_a = get_workload_value(profile_a, axis_a_wl, axis_a_metric)
        val_b_a = get_workload_value(profile_b, axis_a_wl, axis_a_metric)
        val_a_b = get_workload_value(profile_a, axis_b_wl, axis_b_metric)
        val_b_b = get_workload_value(profile_b, axis_b_wl, axis_b_metric)
        
        if None in (val_a_a, val_b_a, val_a_b, val_b_b):
            continue
        
        d_a = delta_pct(val_a_a, val_b_a)   # positive = A leads on gaming
        d_b = delta_pct(val_a_b, val_b_b)   # positive = A leads on productivity
        
        # Check if there's a genuine tradeoff: different leaders on different axes
        if (d_a is not None and d_b is not None) and ((d_a > 5 and d_b < -5) or (d_a < -5 and d_b > 5)):
            gaming_leader = a_label if d_a > 0 else b_label
            prod_leader = a_label if d_b > 0 else b_label
            
            print(f"\n  {axis['label']}:")
            print(f"    {axis['axis_a']['label']}: {gaming_leader} leads by {abs(d_a):.1f}%")
            print(f"    {axis['axis_b']['label']}: {prod_leader} leads by {abs(d_b):.1f}%")
            print(f"    Type: strong tradeoff — решение зависит от приоритета пользователя")
    
    # ── Platform divergence ────────────────────────────────────
    print(f"\n{'─'*70}")
    print("PLATFORM DIVERGENCE")
    
    pa = a.get("platform", {})
    pb = b.get("platform", {})
    
    for aspect in fw.get("platform_aspects", []):
        aid = aspect["id"]
        
        if aid == "socket_longevity":
            sa = pa.get("socket_lifecycle", "")
            sb = pb.get("socket_lifecycle", "")
            if sa != sb:
                print(f"\n  Socket: {pa.get('socket','')} ({sa}) vs {pb.get('socket','')} ({sb})")
                if pa.get("socket_upgrade_note"):
                    print(f"    {a_label}: {pa['socket_upgrade_note']}")
                if pb.get("socket_upgrade_note"):
                    print(f"    {b_label}: {pb['socket_upgrade_note']}")
        
        if aid == "memory_type":
            ma = pa.get("memory", "")
            mb = pb.get("memory", "")
            if ma and mb and ma != mb:
                print(f"\n  Memory: {ma} vs {mb}")
                print(f"    DDR4-совместимость снижает стоимость сборки на ~5-8K ₽")
        
        if aid == "cooling_requirements":
            pa_power = pa.get("power_draw_mt_w")
            pb_power = pb.get("power_draw_mt_w")
            pa_temp = pa.get("temp_mt_c")
            pb_temp = pb.get("temp_mt_c")
            
            if pa_power and pb_power:
                print(f"\n  Power (real MT load draw):")
                print(f"    {a_label:35s} {pa_power:>4d}W / {pa_temp}°C")
                print(f"    {b_label:35s} {pb_power:>4d}W / {pb_temp}°C")
                delta_w = abs(pa_power - pb_power)
                leader = a_label if pa_power < pb_power else b_label
                print(f"    Delta: {delta_w}W — {leader} экономичнее")
                if delta_w > 50:
                    hotter = a_label if pa_power > pb_power else b_label
                    cooler = b_label if pa_power > pb_power else a_label
                    print(f"    {hotter} может потребовать СЖО. {cooler} соберётся с башенным кулером.")
            elif pa_power or pb_power:
                # Asymmetric: one CPU has real data, other doesn't
                print(f"\n  Power (данные неполные):")
                if pa_power:
                    print(f"    {a_label:35s} {pa_power:>4d}W / {pa_temp}°C (реальные замеры)")
                    print(f"    {b_label:35s} {pb.get('tdp_w','?')}W TDP (спецификация — нет замеров)")
                else:
                    print(f"    {a_label:35s} {pa.get('tdp_w','?')}W TDP (спецификация — нет замеров)")
                    print(f"    {b_label:35s} {pb_power:>4d}W / {pb_temp}°C (реальные замеры)")
                print(f"    ⚠ Сравнение неточное: реальные замеры vs спецификация.")
            else:
                ta = pa.get("tdp_w")
                tb = pb.get("tdp_w")
                print(f"\n  Power (spec TDP — нет реальных замеров):")
                print(f"    {a_label:35s} {ta}W TDP")
                print(f"    {b_label:35s} {tb}W TDP")
                print(f"    ⚠ TDP из спецификации. Intel PL2 может быть вдвое выше заявленного.")
        
        if aid == "igpu_presence":
            # Not in current profiles — gap
            pass
    
    # ── Decision boundaries ────────────────────────────────────
    print(f"\n{'─'*70}")
    print("DECISION BOUNDARIES")
    print("  (условия при которых выбор меняется на противоположный)")
    
    for boundary in fw.get("decision_boundaries", []):
        bid = boundary["id"]
        computable = boundary.get("computable", False)
        
        if not computable:
            continue
        
        if bid == "esports_only":
            # Check if competitive delta is decisive
            val_a = get_workload_value(profile_a, "competitive-gaming", "fps_1pct_low_mean")
            val_b = get_workload_value(profile_b, "competitive-gaming", "fps_1pct_low_mean")
            if val_a and val_b:
                d = abs(delta_pct(val_a, val_b))
                if d and d > 25:
                    print(f"\n  ⚡ Если пользователь играет ТОЛЬКО в киберспорт:")
                    print(f"     {boundary['effect']}")
        
        if bid == "mixed_use":
            # Check if gaming/productivity tradeoff is strong
            val_a_g = get_workload_value(profile_a, "competitive-gaming", "fps_1pct_low_mean")
            val_b_g = get_workload_value(profile_b, "competitive-gaming", "fps_1pct_low_mean")
            val_a_p = get_workload_value(profile_a, "content-creation", "geekbench_mt")
            val_b_p = get_workload_value(profile_b, "content-creation", "geekbench_mt")
            
            if all([val_a_g, val_b_g, val_a_p, val_b_p]):
                d_g = delta_pct(val_a_g, val_b_g)
                d_p = delta_pct(val_a_p, val_b_p)
                if d_g and d_p and ((d_g > 15 and d_p < -15) or (d_g < -15 and d_p > 15)):
                    print(f"\n  ⚡ Если пользователь И играет И работает:")
                    print(f"     {boundary['effect']}")
    
    print(f"\n{'='*70}")
    print("Note: All values are training_data estimates (confidence ~0.75).")
    print("Real benchmarks may differ ±10-15%.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
