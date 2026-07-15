---
name: warehouse-{domain}
description: "Data Warehouse for {domain}: {description}. Operating context — LLM reads this file to understand the DWH."
dwh: {domain}
mission: "Maintain analytical integrity of the {domain_title} DWH."
customer: "Content Team"
success:
  - "Coverage"
  - "Consistency"
  - "Traceability"
authority:
  - read
  - write_observation
  - create_dimension
  - update_context_map
  - update_bus_matrix
must_not:
  - "Invent data sources"
  - "Violate contracts"
sources_of_truth:
  - "context-map.yaml → read first"
  - "bus-matrix.yaml → schema"
  - "contracts/ → invariants"
tools:
  - "compile-context-map → python3 tools/compile-context-map/generate.py"
---

# {domain_title} DWH

You are attached to this DWH. Read `references/context-map.yaml` before any action.

## Authoritative Sources
1. context-map.yaml — current state
2. bus-matrix.yaml — schema + aliases
3. contracts/ — invariants

## Structure
```
warehouse/{domain}/
├── bus-matrix.yaml
├── dim/
├── fact/
└── definitions/

marts/{domain}/
├── laws/
├── patterns/
└── comparisons/

references/
├── context-map.yaml      ← auto-generated
├── ontology.md
├── mental-models.md
├── terminology.md
└── contracts/

tools/
└── compile-context-map/
```

## After Any Data Change
```
python3 tools/compile-context-map/generate.py --warehouse-root . --output references/context-map.yaml
```

Scaffolded by Minerva on {date}.
