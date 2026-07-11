# GPU Entity Type Schema v1.0

Тип сущности GPU в pc_hardware_knowledge_base. Определяет структурированные метаданные для аналитического слоя.

## Блок 1: Физические спецификации (generic — все вендоры)

```yaml
specs:
  gpu: string                          # Die codename + архитектура
  lithography: string                  # Техпроцесс

  vram:
    size_gb: number                    # 8, 12, 16, 32
    type: string                       # GDDR6 | GDDR6X | GDDR7
    bus_width_bit: number              # 128, 192, 256, 512
    bandwidth_gb_s: number             # Пропускная способность

  clock:
    boost_ghz: number                  # Boost clock
    game_ghz: number | null            # Game clock (AMD-specific)

  tbp_w: number                        # Total Board Power
  power_connector: string              # "1× 8-pin" | "12V-2×6" | ...
  pcie: string                         # "PCIe 5.0 x16" | ...
  display_outputs: string
  msrp_usd: number

  cache:
    size_mb: number
    type: string                       # "L2" | "Infinity Cache"

  manufacturing:                       # Опционально
    die_area_mm2: number | null
    transistors_billion: number | null

  engineering_notes: string
```

## Блок 2: Вычислительные блоки (generic-ключи, vendor-specific значения)

```yaml
compute:
  unit:
    type: string                       # "CUDA Core" | "Stream Processor" | "Xe Core"
    count: number

  rt:
    type: string                       # "RT Core" | "Ray Accelerator" | "RT Unit"
    count: number
    generation: number                 # 4, 3, 2

  ml:
    type: string                       # "Tensor Core" | "AI Accelerator" | "XMX Engine"
    count: number
    generation: number | null
```

## Блок 3: Софтверный стек (generic-ключи, vendor-specific значения)

```yaml
software:
  upscaler: string                     # "DLSS 4" | "FSR 4" | "XeSS 2"
  frame_gen: string | null             # "MFG" | "AFMF 2" | "XeSS FG" | null
  encoder: string                      # "NVENC 9th gen" | "AMF/VCE" | "QSV"
  compute_api: string                  # "CUDA" | "ROCm" | "oneAPI"
  driver_features: [string]            # ["SAM", "HYPR-RX"] | ["Game Ready"] | [...]
```

## Примеры

### NVIDIA RTX 5060

```yaml
specs:
  vram:
    size_gb: 8
    type: "GDDR7"
    bus_width_bit: 128
    bandwidth_gb_s: 448
  clock:
    boost_ghz: 2.50
    game_ghz: null
  cache:
    size_mb: 24
    type: "L2"
compute:
  unit:  { type: "CUDA Core", count: 3840 }
  rt:    { type: "RT Core", count: 30, generation: 4 }
  ml:    { type: "Tensor Core", count: 120, generation: 5 }
software:
  upscaler: "DLSS 4"
  frame_gen: "MFG"
  encoder: "NVENC 9th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]
```

### AMD RX 9070

```yaml
specs:
  vram:
    size_gb: 16
    type: "GDDR6"
    bus_width_bit: 256
    bandwidth_gb_s: 640
  clock:
    boost_ghz: 2.80
    game_ghz: 2.45
  cache:
    size_mb: 64
    type: "Infinity Cache"
compute:
  unit:  { type: "Stream Processor", count: 5632 }
  rt:    { type: "Ray Accelerator", count: 88, generation: 3 }
  ml:    { type: "AI Accelerator", count: 176, generation: null }
software:
  upscaler: "FSR 4"
  frame_gen: "AFMF 2"
  encoder: "AMF/VCE"
  compute_api: "ROCm"
  driver_features: ["SAM", "HYPR-RX"]
```

### Intel Arc B580

```yaml
specs:
  vram:
    size_gb: 12
    type: "GDDR6"
    bus_width_bit: 192
    bandwidth_gb_s: 456
  manufacturing:
    die_area_mm2: 272
    transistors_billion: 19.6
compute:
  unit:  { type: "Xe Core", count: 20 }
  rt:    { type: "RT Unit", count: 20, generation: 2 }
  ml:    { type: "XMX Engine", count: 160, generation: null }
software:
  upscaler: "XeSS 2"
  frame_gen: "XeSS FG"
  encoder: "QSV"
  compute_api: "oneAPI"
  driver_features: []
```

## Migration Status

| Vendor | GPU | Status |
|---|---|---|
| NVIDIA | RTX 5060 | ✅ migrated |
| NVIDIA | RTX 5060 Ti | ⚠️ migrated (rt/ml counts null — not in KB) |
| NVIDIA | RTX 5070 | ✅ migrated |
| NVIDIA | RTX 5070 Ti | ✅ migrated |
| NVIDIA | RTX 5080 | ✅ migrated |
| NVIDIA | RTX 5090 | ✅ migrated |
| NVIDIA | RTX 4060 | ✅ migrated |
| NVIDIA | RTX 4060 Ti | ✅ migrated |
| NVIDIA | RTX 4070 | ✅ migrated |
| AMD | RX 7600 | ✅ migrated |
| AMD | RX 9060 XT | ✅ migrated |
| AMD | RX 9070 | ✅ migrated |
| AMD | RX 9070 XT | ✅ migrated |
| Intel | Arc B570 | ✅ migrated |
| Intel | Arc B580 | ✅ migrated |
