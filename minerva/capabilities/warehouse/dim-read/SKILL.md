---
capability: dim-read
layer: warehouse
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware', 'memory'"
      - name: dim_type
        type: string
        required: true
        description: "Тип dimension: gpu, game_title, resolution, graphics_preset, driver_version, cpu"
      - name: dim_id
        type: string
        required: true
        description: "ID dimension: nvidia-rtx-5060, cyberpunk-2077, ..."
  out:
    result: dimension_data
  errors:
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
    - code: DIM_NOT_FOUND
      meaning: "Dimension не существует"
    - code: INVALID_DIM_TYPE
      meaning: "Тип dimension не зарегистрирован в bus-matrix"
idempotency: "read"
---

# dim-read — прочитать Dimension по id

## Model

Dimensions — описательные атрибуты в dimensional model. Хранятся в `warehouse/{domain}/dim/{dim_type}/{dim_id}.yaml`. Типы dimensions и их атрибуты зарегистрированы в bus matrix домена.

## Invariants

- dim_type зарегистрирован в `warehouse/{domain}/bus-matrix.yaml` (секция `dimensions`)
- Файл `warehouse/{domain}/dim/{dim_type}/{dim_id}.yaml` существует
- Если SCD Type 2 — возвращается актуальная версия (current_version)

## Пример

```
dim-read(domain="hardware", dim_type="gpu", dim_id="nvidia-rtx-5060")
→ warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml
→ dimension_data {id: "nvidia-rtx-5060", canonical_name: "NVIDIA GeForce RTX 5060 8GB", ...}
```
