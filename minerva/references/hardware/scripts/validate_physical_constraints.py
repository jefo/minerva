"""
Skill 9: Validate Physical Constraints

Проверяет бинарные физические стереотипы компонентов сборки против
физических ограничений интента. В отличие от evaluate_profiles.py
(поведенческие профили — BLOCK/WARN с весами), этот навык работает
с детерминированными бинарными предикатами.

Использование:
    from validate_physical_constraints import validate
    result = validate(physical_check_input)

physical_check_input = {
    "components": {
        "psu": {
            "id": "deepcool-pn750d",
            "physical_stereotypes": {
                "atx_form_factor": True,
                "sfx_form_factor_locked": False
            }
        },
        "motherboard": {
            "id": "msi-b650-tomahawk",
            "physical_stereotypes": {
                "itx_form_factor": False,
                "8_layer_daisy_chain": False,
                "6_layer_budget_pcb": True
            }
        },
        "gpu": {
            "id": "nvidia-rtx-5090",
            "specs": {"length_mm": 348, "thickness_slots": 3.5}
        },
        "cooler": {
            "id": "deepcool-ak620",
            "specs": {"height_mm": 160}
        }
    },
    "constraints": {
        "gpu_max_length_mm": 320,
        "gpu_max_thickness_slots": 3.0,
        "cooler_max_height_mm": 155,
        "required_stereotypes": {
            "psu": ["sfx_form_factor_locked"],
            "motherboard": ["itx_form_factor"]
        },
        "forbidden_stereotypes": {
            "psu": ["atx_form_factor"],
            "motherboard": ["atx_form_factor", "matx_form_factor"]
        },
        "power_budget_max_w": 750
    }
}

Returns: {
    "pass": bool,
    "checks": [
        {"component": "psu", "check": "form_factor", "status": "FAIL",
         "detail": "required SFX, found ATX"},
        {"component": "gpu", "check": "length", "status": "FAIL",
         "detail": "348mm > 320mm limit"}
    ],
    "blocking_failures": int,
    "warnings": int
}
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PhysicalConstraintResult:
    pass_: bool  # True если все required-stereotypes присутствуют и все forbidden отсутствуют
    checks: List[dict] = field(default_factory=list)
    blocking_failures: int = 0
    warnings: int = 0


def validate(check_input: dict) -> dict:
    """
    Главная точка входа для Skill 9.
    Принимает словарь с компонентами и constraints, возвращает результат.
    """
    components = check_input.get("components", {})
    constraints = check_input.get("constraints", {})

    checks = []

    # 1. Проверить required стереотипы
    required = constraints.get("required_stereotypes", {})
    for component_type, stereotypes in required.items():
        comp = components.get(component_type)
        if not comp:
            checks.append({
                "component": component_type,
                "check": "required_stereotype",
                "status": "FAIL",
                "detail": f"Component of type '{component_type}' not provided"
            })
            continue
        comp_stereotypes = comp.get("physical_stereotypes", {})
        for stereotype in stereotypes:
            if not comp_stereotypes.get(stereotype):
                checks.append({
                    "component": component_type,
                    "check": f"required:{stereotype}",
                    "status": "FAIL",
                    "detail": f"Required stereotype '{stereotype}' missing on {comp.get('id', component_type)}"
                })
                continue
            checks.append({
                "component": component_type,
                "check": f"required:{stereotype}",
                "status": "PASS",
                "detail": f"{stereotype} confirmed on {comp.get('id', component_type)}"
            })

    # 2. Проверить forbidden стереотипы
    forbidden = constraints.get("forbidden_stereotypes", {})
    for component_type, stereotypes in forbidden.items():
        comp = components.get(component_type)
        if not comp:
            continue
        comp_stereotypes = comp.get("physical_stereotypes", {})
        for stereotype in stereotypes:
            if comp_stereotypes.get(stereotype):
                checks.append({
                    "component": component_type,
                    "check": f"forbidden:{stereotype}",
                    "status": "FAIL",
                    "detail": f"Forbidden stereotype '{stereotype}' present on {comp.get('id', component_type)}"
                })
                continue
            checks.append({
                "component": component_type,
                "check": f"forbidden:{stereotype}",
                "status": "PASS",
                "detail": f"{stereotype} absent (OK)"
            })

    # 3. Проверить габаритные ограничения (GPU, cooler)
    gpu = components.get("gpu", {})
    gpu_specs = gpu.get("specs", {})

    if "gpu_max_length_mm" in constraints and gpu_specs.get("length_mm"):
        actual = gpu_specs["length_mm"]
        limit = constraints["gpu_max_length_mm"]
        if actual > limit:
            checks.append({
                "component": "gpu",
                "check": "length",
                "status": "FAIL",
                "detail": f"GPU length {actual}mm > {limit}mm limit"
            })
        else:
            checks.append({
                "component": "gpu",
                "check": "length",
                "status": "PASS",
                "detail": f"{actual}mm ≤ {limit}mm"
            })

    if "gpu_max_thickness_slots" in constraints and gpu_specs.get("thickness_slots"):
        actual = gpu_specs["thickness_slots"]
        limit = constraints["gpu_max_thickness_slots"]
        if actual > limit:
            checks.append({
                "component": "gpu",
                "check": "thickness",
                "status": "FAIL",
                "detail": f"GPU thickness {actual} slots > {limit} slots limit"
            })
        else:
            checks.append({
                "component": "gpu",
                "check": "thickness",
                "status": "PASS",
                "detail": f"{actual} slots ≤ {limit} slots"
            })

    cooler = components.get("cooler", {})
    cooler_specs = cooler.get("specs", {})

    if "cooler_max_height_mm" in constraints and cooler_specs.get("height_mm"):
        actual = cooler_specs["height_mm"]
        limit = constraints["cooler_max_height_mm"]
        if actual > limit:
            checks.append({
                "component": "cooler",
                "check": "height",
                "status": "FAIL",
                "detail": f"Cooler height {actual}mm > {limit}mm limit"
            })
        else:
            checks.append({
                "component": "cooler",
                "check": "height",
                "status": "PASS",
                "detail": f"{actual}mm ≤ {limit}mm"
            })

    # 4. Подсчитать результаты
    blocking = sum(1 for c in checks if c["status"] == "FAIL")
    warnings = sum(1 for c in checks if c["status"] == "WARN")
    pass_ = blocking == 0

    return {
        "pass": pass_,
        "checks": checks,
        "blocking_failures": blocking,
        "warnings": warnings
    }


# --- Self-test ---
if __name__ == "__main__":
    test_sff = {
        "components": {
            "psu": {
                "id": "deepcool-pn750d",
                "physical_stereotypes": {
                    "atx_form_factor": True,
                    "sfx_form_factor_locked": False
                }
            },
            "motherboard": {
                "id": "msi-b650-tomahawk",
                "physical_stereotypes": {
                    "itx_form_factor": False,
                    "8_layer_daisy_chain": False
                }
            },
            "gpu": {
                "id": "nvidia-rtx-5090",
                "specs": {"length_mm": 348, "thickness_slots": 3.5}
            },
            "cooler": {
                "id": "deepcool-ak620",
                "specs": {"height_mm": 160}
            }
        },
        "constraints": {
            "gpu_max_length_mm": 320,
            "gpu_max_thickness_slots": 3.0,
            "cooler_max_height_mm": 155,
            "required_stereotypes": {
                "psu": ["sfx_form_factor_locked"],
                "motherboard": ["itx_form_factor"]
            },
            "forbidden_stereotypes": {
                "psu": ["atx_form_factor"]
            }
        }
    }

    result = validate(test_sff)
    print(f"PASS: {result['pass']} (expected: False)")
    print(f"Failures: {result['blocking_failures']} (expected: 6 — all should fail)")
    for c in result["checks"]:
        print(f"  [{c['status']}] {c['component']}: {c['check']} — {c['detail']}")

    # Test all-pass scenario
    test_pass = {
        "components": {
            "psu": {
                "id": "corsair-sf750",
                "physical_stereotypes": {
                    "atx_form_factor": False,
                    "sfx_form_factor_locked": True
                }
            },
            "motherboard": {
                "id": "asrock-b650e-pg-itx",
                "physical_stereotypes": {
                    "itx_form_factor": True
                }
            },
            "gpu": {
                "id": "nvidia-rtx-5060",
                "specs": {"length_mm": 242, "thickness_slots": 2.0}
            },
            "cooler": {
                "id": "noctua-nh-l9a",
                "specs": {"height_mm": 37}
            }
        },
        "constraints": {
            "gpu_max_length_mm": 320,
            "gpu_max_thickness_slots": 3.0,
            "cooler_max_height_mm": 155,
            "required_stereotypes": {
                "psu": ["sfx_form_factor_locked"],
                "motherboard": ["itx_form_factor"]
            },
            "forbidden_stereotypes": {
                "psu": ["atx_form_factor"]
            }
        }
    }

    print()
    result2 = validate(test_pass)
    print(f"PASS: {result2['pass']} (expected: True)")
    for c in result2["checks"]:
        print(f"  [{c['status']}] {c['component']}: {c['check']} — {c['detail']}")
