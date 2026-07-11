---
id: "hardware-rtx-5090-cuda-cores"
title: "RTX 5090 CUDA Cores: 20480"
type: Specification
status: draft
tags: [nvidia, blackwell, gb202, cuda, compute]
context: "hardware"
created: "2026-07-11"
updated: "2026-07-11"
value: "20480"
unit: "CUDA cores"
source: "NVIDIA GeForce RTX 5090 Whitepaper"
source_url: "https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/"
subject: "nvidia-geforce-rtx-5090"
---

# RTX 5090 CUDA Cores: 20480

Максимальная конфигурация GB202: полный кристалл без урезаний. 20480 CUDA-ядер распределены по 80 Streaming Multiprocessors (SM) — по 256 на SM.

## Контекст

RTX 4090 (AD102) имела 16384 CUDA — прирост +25%. Это не максимальный теоретический прирост для смены поколения (обычно +40-60%), но Blackwell фокусируется на пропускной способности памяти и RT/ML-ускорении, а не на сырой растеризации.

## Инженерное значение

20480 CUDA при 2.52 GHz дают ~103 TFLOPS FP32 (теоретический пик). Для сравнения: RTX 4090 — ~82 TFLOPS. Разница в 25% на практике транслируется в 20-30% прирост в играх при 4K.
