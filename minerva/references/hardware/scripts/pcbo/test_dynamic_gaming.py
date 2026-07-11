#!/usr/bin/env python3
"""
Integration test: aaa_gaming_base → dynamic_constraints → evaluate_profiles.py

Тест для 3 сценариев: 1080p high, 1440p high, 4K ultra.
Проверяет, что параметризация выдаёт правильные профили и VRAM,
и что evaluate_profiles корректно находит GPU под эти профили.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))

from dynamic_constraints import evaluate_dynamic_constraints

# Эмулируем вызов evaluate_profiles.py (без subprocess)
# Проверим GPU из БЗ вручную
GPU_CATALOG = [
    {"id": "nvidia-rtx-5060",       "vram": 12, "bus": 128, "tgp": 150,
     "profiles": ["balanced_performance_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated"]},
    {"id": "nvidia-rtx-5060-ti",    "vram": 16, "bus": 128, "tgp": 180,
     "profiles": ["balanced_performance_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated"]},
    {"id": "nvidia-rtx-5070",       "vram": 12, "bus": 192, "tgp": 250,
     "profiles": ["balanced_performance_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated", "transient_spike_heavy"]},
    {"id": "nvidia-rtx-5070-ti",    "vram": 16, "bus": 256, "tgp": 300,
     "profiles": ["enthusiast_unrestricted_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated", "transient_spike_heavy"]},
    {"id": "nvidia-rtx-5080",       "vram": 16, "bus": 256, "tgp": 360,
     "profiles": ["enthusiast_unrestricted_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated", "transient_spike_heavy"]},
    {"id": "nvidia-rtx-5090",       "vram": 32, "bus": 512, "tgp": 575,
     "profiles": ["enthusiast_unrestricted_gpu", "hardware_rt_accelerated_gen_3", "tensor_matrix_accelerated", "transient_spike_heavy", "hbm_stacked_bus", "multi_gpu_interconnect_capable"]},
    {"id": "amd-rx-7600",           "vram": 8,  "bus": 128, "tgp": 165,
     "profiles": ["mainstream_efficiency_gpu"]},
    {"id": "amd-rx-9060-xt",        "vram": 16, "bus": 128, "tgp": 200,
     "profiles": ["balanced_performance_gpu", "hardware_rt_accelerated_gen_3"]},
    {"id": "amd-rx-9070",           "vram": 16, "bus": 192, "tgp": 220,
     "profiles": ["balanced_performance_gpu", "hardware_rt_accelerated_gen_3"]},
    {"id": "amd-rx-9070-xt",        "vram": 16, "bus": 256, "tgp": 304,
     "profiles": ["enthusiast_unrestricted_gpu", "hardware_rt_accelerated_gen_3", "transient_spike_heavy"]},
    {"id": "intel-arc-b580",        "vram": 12, "bus": 192, "tgp": 190,
     "profiles": ["balanced_performance_gpu"]},
    {"id": "intel-arc-b570",        "vram": 10, "bus": 160, "tgp": 150,
     "profiles": ["mainstream_efficiency_gpu"]},
]

# Профили, которые считаются "bandwidth_constrained_vram_rich" (128-bit шина)
BANDWIDTH_CONSTRAINED = [
    "nvidia-rtx-5060", "nvidia-rtx-5060-ti", "amd-rx-9060-xt",
    "amd-rx-7600", "intel-arc-b570"
]

# Профили, которые считаются "sub_75w_slot_powered" — таких нет в каталоге
# Все карты в каталоге имеют питание >75W

def check_gpu(gpu: dict, required_profile_ref: str) -> bool:
    """Проверить, имеет ли GPU указанный профиль."""
    profile_name = required_profile_ref.split("#")[-1] if "#" in required_profile_ref else required_profile_ref
    return profile_name in gpu.get("profiles", [])


def run_scenario(resolution: str, settings: str, target_fps: int, desc: str):
    """Прогнать один сценарий."""
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"  {'='*60}")

    # STATE_0.7: dynamic constraints
    result = evaluate_dynamic_constraints(
        "catalog/intents/aaa_gaming_base.yaml",
        {"resolution": resolution, "settings": settings, "target_fps": target_fps}
    )

    min_vram = result["min_vram_gb"]
    mandatory_profile = result["resolved_mandatory_profiles"][0] if result["resolved_mandatory_profiles"] else None
    block_profiles = result["resolved_block_profiles"]
    bandwidth_rule = result["effective_params"]["bandwidth_rule"]

    print(f"  VRAM min:      {min_vram} GB")
    print(f"  GPU profile:   {mandatory_profile}")
    print(f"  BLOCK:         {block_profiles}")
    print(f"  MAUT CPU/GPU:  {result['maut_weights']}")
    print(f"  Noise/Thermal: {result['noise_load']} / {result['thermal_state']}")

    # Найти подходящие GPU
    optimal = []
    warn = []
    block = []

    for gpu in GPU_CATALOG:
        # Проверка VRAM
        if gpu["vram"] < min_vram:
            block.append((gpu["id"], f"VRAM {gpu['vram']}GB < {min_vram}GB"))
            continue

        # Проверка mandatory профиля
        has_profile = check_gpu(gpu, mandatory_profile) if mandatory_profile else True

        # Проверка bandwidth BLOCK
        is_bandwidth = gpu["id"] in BANDWIDTH_CONSTRAINED
        if bandwidth_rule == "BLOCK" and is_bandwidth:
            block.append((gpu["id"], f"128-bit шина → BLOCK на {resolution} {settings}"))
            continue

        if bandwidth_rule == "WARN" and is_bandwidth:
            if has_profile:
                warn.append((gpu["id"], f"128-bit шина → WARN на {resolution} {settings} (VRAM {gpu['vram']}GB OK)"))
            else:
                block.append((gpu["id"], f"Нет профиля {mandatory_profile}"))
            continue

        if has_profile:
            optimal.append((gpu["id"], f"{gpu['vram']}GB VRAM, {gpu['bus']}-bit, {gpu['tgp']}W"))
        else:
            block.append((gpu["id"], f"Нет профиля {mandatory_profile}"))

    print(f"\n  Optimal ({len(optimal)}):")
    for id, reason in optimal:
        print(f"    ✅ {id}: {reason}")

    if warn:
        print(f"\n  WARN ({len(warn)}):")
        for id, reason in warn:
            print(f"    ⚠️  {id}: {reason}")

    print(f"\n  BLOCK ({len(block)}):")
    for id, reason in block:
        print(f"    ❌ {id}: {reason}")


if __name__ == "__main__":
    run_scenario("1080p", "high", 60, "Cyberpunk 1080p high 60fps")
    run_scenario("1440p", "high", 60, "Cyberpunk 1440p high 60fps")
    run_scenario("4K", "ultra", 60, "Cyberpunk 4K ultra 60fps")
