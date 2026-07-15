#!/usr/bin/env python3
"""
Compile Context Map — generates context-map.yaml for a DWH.

Walks the warehouse directory tree, extracts semantic index:
  - dimensions (grouped by type, key attributes)
  - observations (counts, coverage: games, resolutions, GPUs/CPUs)
  - marts (laws, patterns with statements)
  - capabilities (available SKILL.md)

Usage:
  python3 generate.py --warehouse-root /path/to/dwh --output references/context-map.yaml
"""

import argparse
import yaml
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict


def load_yaml(path: str) -> dict | None:
    """Load a YAML file, return None on any error."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"WARNING: skipping {path}: {e}", file=sys.stderr)
        return None


def collect_dimensions(warehouse_root: Path) -> dict:
    """Walk dim/ directory, group entities by dimension type."""
    dim_root = warehouse_root / "warehouse" / "hardware" / "dim"
    if not dim_root.exists():
        return {}

    result = {}
    for dim_type_dir in sorted(dim_root.iterdir()):
        if not dim_type_dir.is_dir():
            continue
        dim_type = dim_type_dir.name
        entities = []
        for yaml_file in sorted(dim_type_dir.glob("*.yaml")):
            data = load_yaml(str(yaml_file))
            if not data:
                continue
            dim = data.get("dimension", {})
            attrs = data.get("attributes", {})
            entity = {
                "id": dim.get("id", yaml_file.stem),
                "canonical_name": dim.get("canonical_name", ""),
            }
            # Add type-specific key attributes
            if dim_type == "gpu":
                entity["vendor"] = attrs.get("vendor", "")
                entity["architecture"] = attrs.get("architecture", "")
                vram = attrs.get("vram", {})
                entity["vram"] = f"{vram.get('size_gb', '?')}GB {vram.get('type', '?')}"
            elif dim_type == "cpu":
                entity["vendor"] = attrs.get("vendor", "")
                entity["architecture"] = attrs.get("architecture", "")
                entity["socket"] = attrs.get("socket", "")
                entity["cores"] = attrs.get("compute", {}).get("cores", "")
            elif dim_type == "architecture":
                entity["vendor"] = attrs.get("vendor", "")
            elif dim_type == "game_title":
                entity["genre"] = attrs.get("genre", "")
            entities.append(entity)

        result[dim_type] = {
            "count": len(entities),
            "entities": entities,
        }
    return result


def collect_observations(warehouse_root: Path) -> dict:
    """Walk all fact/*/ subdirectories, group by GPU/CPU, collect games/resolutions/presets."""
    fact_root = warehouse_root / "warehouse" / "hardware" / "fact"
    if not fact_root.exists():
        return {"total": 0}

    all_observations = []
    # Walk all subdirectories: observations/, cpu_observations/
    for subdir in sorted(fact_root.iterdir()):
        if not subdir.is_dir():
            continue
        for yaml_file in sorted(subdir.glob("*.yaml")):
            data = load_yaml(str(yaml_file))
            if not data:
                continue
            fact = data.get("fact", {})
            source = data.get("source", {})
            measures = data.get("measures", {})
            conditions = data.get("conditions", {})
            meta = data.get("meta", {})

            # Handle both GPU and CPU observation formats
            component = source.get("gpu") or source.get("cpu") or ""
            obs = {
                "file": yaml_file.name,
                "id": fact.get("id", yaml_file.stem),
                "type": fact.get("type", "observation"),
                "component": str(component),
                "game_title": source.get("game_title", ""),
                "resolution": str(source.get("resolution", "")),
                "graphics_preset": str(source.get("graphics_preset", "")),
                "upscaler": str(conditions.get("upscaler", "native")),
                "frame_gen": str(conditions.get("frame_gen", "false")),
                "measures": list(measures.keys()) if measures else [],
                "confidence": meta.get("confidence"),
                "confidence_basis": meta.get("confidence_basis", ""),
            }
            all_observations.append(obs)

    # Aggregate statistics
    games = sorted(set(o["game_title"] for o in all_observations if o["game_title"]))
    resolutions = sorted(set(o["resolution"] for o in all_observations if o["resolution"]))
    presets = sorted(set(o["graphics_preset"] for o in all_observations if o["graphics_preset"]))
    components = sorted(set(o["component"] for o in all_observations if o["component"]))

    # Group by component for quick lookup
    by_component = defaultdict(list)
    for o in all_observations:
        if o["component"]:
            by_component[o["component"]].append(o["id"])

    return {
        "total": len(all_observations),
        "games_covered": games,
        "resolutions": resolutions,
        "graphics_presets": presets,
        "component_count": len(components),
        "components": components,
        "by_component": {comp: {"count": len(ids), "sample_ids": ids[:5]} for comp, ids in sorted(by_component.items())},
    }


def collect_marts(warehouse_root: Path) -> dict:
    """Walk marts/ directory, collect laws and patterns."""
    marts_root = warehouse_root / "marts"
    if not marts_root.exists():
        return {}

    result = {}
    # Laws
    laws = []
    for law_file in sorted(marts_root.rglob("laws/*.yaml")):
        data = load_yaml(str(law_file))
        if not data:
            continue
        df = data.get("derived_fact", {})
        lineage = data.get("lineage", {})
        laws.append({
            "id": df.get("id", law_file.stem),
            "type": df.get("type", "law"),
            "statement": df.get("statement", ""),
            "confidence": df.get("confidence"),
            "confidence_basis": df.get("confidence_basis", ""),
            "evidence_count": len(lineage.get("nodes", [])),
        })
    result["laws"] = {"count": len(laws), "items": laws}

    # Patterns
    patterns = []
    for pat_file in sorted(marts_root.rglob("patterns/*.yaml")):
        data = load_yaml(str(pat_file))
        if not data:
            continue
        df = data.get("derived_fact", {})
        patterns.append({
            "id": df.get("id", pat_file.stem),
            "statement": df.get("statement", ""),
        })
    result["patterns"] = {"count": len(patterns), "items": patterns}

    return result


def collect_capabilities(warehouse_root: Path) -> list:
    """Scan capabilities/ for SKILL.md files, return their names."""
    caps_root = warehouse_root / "capabilities"
    if not caps_root.exists():
        return []

    capabilities = []
    for skill_file in sorted(caps_root.rglob("SKILL.md")):
        # Extract capability name: parent directory name
        cap_dir = skill_file.parent
        # Get relative path from capabilities root
        rel = cap_dir.relative_to(caps_root)
        capabilities.append(str(rel))
    return capabilities


def main():
    parser = argparse.ArgumentParser(description="Compile context map for a DWH")
    parser.add_argument("--warehouse-root", required=True, help="Root directory of the DWH")
    parser.add_argument("--output", required=True, help="Output YAML file path")
    args = parser.parse_args()

    root = Path(args.warehouse_root).resolve()
    if not root.exists():
        print(f"ERROR: warehouse root does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    # Read warehouse name from bus-matrix
    bus_matrix_path = root / "warehouse" / "hardware" / "bus-matrix.yaml"
    warehouse_name = root.name
    if bus_matrix_path.exists():
        bm = load_yaml(str(bus_matrix_path))
        if bm:
            warehouse_name = bm.get("bus_matrix", {}).get("domain", root.name)

    context_map = {
        "context_map": {
            "warehouse": warehouse_name,
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "dimensions": collect_dimensions(root),
            "observations": collect_observations(root),
            "marts": collect_marts(root),
            "capabilities": collect_capabilities(root),
        }
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(context_map, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Context map written: {output_path}")
    total_dims = sum(v["count"] for v in context_map["context_map"]["dimensions"].values())
    total_obs = context_map["context_map"]["observations"]["total"]
    total_laws = context_map["context_map"]["marts"].get("laws", {}).get("count", 0)
    print(f"  Dimensions: {len(context_map['context_map']['dimensions'])} types, {total_dims} entities")
    print(f"  Observations: {total_obs}")
    print(f"  Laws: {total_laws}")
    cap_count = len(context_map["context_map"]["capabilities"])
    print(f"  Capabilities: {cap_count}")


if __name__ == "__main__":
    main()
