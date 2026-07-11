"""
Dynamic Constraints Engine — STATE_0.7 пайплайна PCBO.

Параметризует абстрактные интенты под конкретные параметры.
Все числа — из YAML-конфига интента. Python-функции — blind executors.

Домены:
  - "gaming" → resolution, settings, target_fps
  - "ai_compute" → model_size, quantization, context_length
  - "data_engineering" → dataset_size, workload
"""

import yaml
from pathlib import Path
from typing import Dict, List


def evaluate_dynamic_constraints(intent_path: str, params: dict) -> dict:
    """Главная точка входа. Маршрутизация по domain интента."""
    base_dir = Path(__file__).parent.parent.parent
    full_path = base_dir / intent_path
    with open(full_path) as f:
        intent = yaml.safe_load(f)
    domain = intent.get("domain", "")
    dynamic = intent.get("dynamic_constraints", {})
    if not dynamic or not intent.get("abstract"):
        return _static_fallback(intent)
    if domain == "gaming":
        return _eval_gaming(intent, dynamic, params)
    elif domain == "ai_compute":
        return _eval_llm(intent, dynamic, params)
    elif domain == "data_engineering":
        return _eval_data(intent, dynamic, params)
    return _static_fallback(intent)


# ═══════════════════ GAMING ═══════════════════

def _eval_gaming(intent: dict, dynamic: dict, params: dict) -> dict:
    resolution = params.get("resolution", "1080p")
    settings = params.get("settings", "high")
    target_fps = params.get("target_fps", 60)

    min_vram = _vram(dynamic, resolution, settings)
    maut_r = _maut(dynamic, resolution)
    bw = _bandwidth(dynamic, resolution, settings)

    matrix = intent.get("profile_interaction_matrix", {})
    mandatory = []  # range replaces single profile
    block = [b["profile"] for b in matrix.get("strict_block", []) if "bandwidth_constrained" not in b["profile"]]
    if bw == "BLOCK":
        block.append("concepts/epistemological-profiles.md#bandwidth_constrained_vram_rich")
    warn = []
    if bw == "WARN":
        warn.append("concepts/epistemological-profiles.md#bandwidth_constrained_vram_rich")
    for w in matrix.get("warn", []):
        if w["profile"] not in warn and w["profile"] not in block:
            warn.append(w["profile"])
    if bw == "BLOCK":
        warn = [w for w in warn if "bandwidth_constrained" not in w]

    return {
        "resolved_mandatory_profiles": mandatory,
        "resolved_block_profiles": block,
        "resolved_warn_profiles": warn,
        "min_capability": _gpu_min_capability(dynamic, resolution),
        "min_vram_gb": min_vram,
        "maut_weights": maut_r["maut_weights"],
        "noise_load": maut_r.get("noise_load", "A2"),
        "thermal_state": maut_r.get("thermal_state", "T_Safe"),
        "effective_params": {"resolution": resolution, "settings": settings, "target_fps": target_fps, "bandwidth_rule": bw}
    }


def _gpu_min_capability(d: dict, res: str) -> str:
    """Get minimum GPU capability requirement for given resolution."""
    c = d.get("min_capability", {}).get("gpu", {}).get("config", {})
    return c.get(res, "mainstream_efficiency_gpu")


def _get_min_capability(d: dict, component_type: str, res: str | None = None) -> str:
    """Get minimum capability for any component type from intent config."""
    mc = d.get("min_capability", {}).get(component_type, {}).get("config", {})
    if res and res in mc:
        return mc[res]
    return mc.get("default", "unknown")


def _vram(d: dict, res: str, sett: str) -> int:
    c = d["vram_minimum_gb"]["config"]
    return c["base"].get(res, 8) + c["modifiers"].get(sett, 0)


def _gpu_prof(d: dict, res: str, fps: int) -> str:
    c = d["target_gpu_profile"]["config"]
    k = f"{res}_{fps}fps"
    if k in c and not k.endswith("_note"):
        return c[k]
    candidates = [(int(key.split("_")[-1].replace("fps", "")), val) for key, val in c.items() if key.startswith(res) and not key.endswith("_note")]
    if not candidates:
        return c.get("1080p_60fps", "concepts/epistemological-profiles.md#mainstream_efficiency_gpu")
    candidates.sort()
    for f, prof in candidates:
        if f >= fps:
            return prof
    return candidates[-1][1]


def _maut(d: dict, res: str) -> dict:
    c = d["maut_weights"]["config"].get(res, d["maut_weights"]["config"].get("1080p", {}))
    return {"maut_weights": {"cpu_weight": c.get("cpu_weight", 0.4), "gpu_weight": c.get("gpu_weight", 0.6)}, "noise_load": c.get("noise_load", "A2"), "thermal_state": c.get("thermal_state", "T_Safe")}


def _bandwidth(d: dict, res: str, sett: str) -> str:
    c = d.get("bandwidth_block_rule", {}).get("config", {})
    sc = f"{res}_{sett}"
    if sc in c.get("block_at", []):
        return "BLOCK"
    if sc in c.get("warn_at", []):
        return "WARN"
    if res == "4K" and sett in ("high", "ultra", "path_tracing"):
        return "BLOCK"
    if res == "1440p" and sett in ("ultra", "path_tracing"):
        return "BLOCK"
    return "WARN"


# ═══════════════════ AI / LLM ═══════════════════

def _eval_llm(intent: dict, dynamic: dict, params: dict) -> dict:
    model = params.get("model_size", "7B")
    quant = params.get("quantization", "q4")
    ctx = params.get("context_length", "4K")

    lc = dynamic["llm_vram"]["config"]
    base_vram = lc["model_vram_base"].get(model, {"q4": 5}).get(quant, 5)
    ctx_oh = lc["context_overhead_gb"].get(ctx, 0)
    min_vram = base_vram + ctx_oh

    gpu_prof = None
    for b in lc["gpu_profile_by_vram"]:
        if min_vram <= b["max_vram"]:
            gpu_prof = b["profile"]
            break

    min_ram = lc["min_ram_by_model_size"].get(model, 32)
    matrix = intent.get("profile_interaction_matrix", {})
    block = [b["profile"] for b in matrix.get("strict_block", [])]
    mandatory = ["concepts/epistemological-profiles.md#tensor_matrix_accelerated"]
    if gpu_prof and gpu_prof not in mandatory:
        mandatory.append(gpu_prof)
    warn = []
    if 10 <= min_vram <= 16:
        warn.append("concepts/epistemological-profiles.md#bandwidth_constrained_vram_rich")

    return {
        "resolved_mandatory_profiles": mandatory,
        "resolved_block_profiles": block,
        "resolved_warn_profiles": warn,
        "min_vram_gb": min_vram,
        "min_ram_gb": min_ram,
        "maut_weights": {"cpu_weight": 0.1, "gpu_weight": 0.9},
        "noise_load": "A3",
        "thermal_state": "T_Warm",
        "effective_params": {"model_size": model, "quantization": quant, "context_length": ctx, "gpu_profile": gpu_prof}
    }


# ═══════════════════ DATA ENGINEERING ═══════════════════

def _eval_data(intent: dict, dynamic: dict, params: dict) -> dict:
    ds = params.get("dataset_size", "50GB")
    wl = params.get("workload", "ETL")

    dc = dynamic["ram_and_storage"]["config"]
    min_ram = dc["ram_by_dataset"].get(ds, {"min": 64})["min"]
    sustained = dc["sustained_write_by_workload"].get(wl, {"required": True})["required"]
    thermal = dc["thermal_by_dataset"].get(ds, "T_Warm")

    matrix = intent.get("profile_interaction_matrix", {})
    mandatory = [m["profile"] for m in matrix.get("mandatory_steel_man", [])]
    block = [b["profile"] for b in matrix.get("strict_block", [])]

    return {
        "resolved_mandatory_profiles": mandatory,
        "resolved_block_profiles": block,
        "resolved_warn_profiles": [],
        "min_ram_gb": min_ram,
        "min_storage_sustained_write": sustained,
        "maut_weights": {"cpu_weight": 0.7, "gpu_weight": 0.3},
        "noise_load": "A3",
        "thermal_state": thermal,
        "effective_params": {"dataset_size": ds, "workload": wl}
    }


def _static_fallback(intent: dict) -> dict:
    m = intent.get("profile_interaction_matrix", {})
    return {
        "resolved_mandatory_profiles": [x["profile"] for x in m.get("mandatory_steel_man", [])],
        "resolved_block_profiles": [x["profile"] for x in m.get("strict_block", [])],
        "resolved_warn_profiles": [x["profile"] for x in m.get("warn", [])],
        "min_vram_gb": 0, "maut_weights": {}, "noise_load": "A2", "thermal_state": "T_Safe",
        "effective_params": {"note": "static intent — no dynamic resolution"},
    }


# ═══════════════════ SELF-TEST ═══════════════════

if __name__ == "__main__":
    print("=== GAMING ===")
    tests_gaming = [
        ("1080p", "high", 60, "1080p high 60fps"),
        ("1440p", "high", 60, "1440p high 60fps"),
        ("1440p", "ultra", 60, "1440p ultra 60fps"),
        ("4K", "ultra", 60, "4K ultra 60fps"),
    ]
    for res, sett, fps, desc in tests_gaming:
        r = evaluate_dynamic_constraints("catalog/intents/aaa_gaming_base.yaml", {"resolution": res, "settings": sett, "target_fps": fps})
        print(f"  {desc}: VRAM={r['min_vram_gb']}GB profile={r['resolved_mandatory_profiles'][0] if r['resolved_mandatory_profiles'] else 'none'} bw={r['effective_params'].get('bandwidth_rule','N/A')}")

    print("\n=== AI INFERENCE ===")
    tests_llm = [
        ("7B", "q4", "4K", "Llama-3 7B Q4 4K"),
        ("13B", "q4", "32K", "Qwen 13B Q4 32K"),
        ("32B", "q4", "4K", "Qwen 32B Q4 4K"),
        ("70B", "q4", "4K", "Llama-3 70B Q4 4K"),
        ("32B", "fp16", "128K", "Mixtral 32B FP16 128K"),
    ]
    for model, quant, ctx, desc in tests_llm:
        r = evaluate_dynamic_constraints("catalog/intents/ai_inference_base.yaml", {"model_size": model, "quantization": quant, "context_length": ctx})
        print(f"  {desc}: VRAM={r['min_vram_gb']}GB RAM={r.get('min_ram_gb','?')}GB profile={[p.split('#')[-1] for p in r['resolved_mandatory_profiles']]}")

    print("\n=== DATA ENGINEERING ===")
    tests_data = [
        ("50GB", "ETL", "50GB ETL"),
        ("200GB", "SQL_analytics", "200GB SQL analytics"),
        ("500GB", "ETL", "500GB ETL"),
        ("50GB", "ML_preprocessing", "50GB ML preprocessing"),
    ]
    for ds, wl, desc in tests_data:
        r = evaluate_dynamic_constraints("catalog/intents/data_engineering_base.yaml", {"dataset_size": ds, "workload": wl})
        print(f"  {desc}: RAM={r['min_ram_gb']}GB sustained_write={r.get('min_storage_sustained_write','?')} thermal={r['thermal_state']}")
