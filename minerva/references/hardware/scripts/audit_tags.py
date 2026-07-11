#!/usr/bin/env python3
"""Механическая проверка предикатов engineering-tags на всех entry в каталоге.

Usage:
  python scripts/audit_tags.py              # проверить всё
  python scripts/audit_tags.py --type gpu   # только GPU
  python scripts/audit_tags.py --entry nvidia-rtx-5060-ti  # один entry
  python scripts/audit_tags.py --tag local-llm-viable       # проверить один тег
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"


def parse_frontmatter(filepath: Path) -> dict[str, Any]:
    """Extract frontmatter from markdown file into flat dict."""
    text = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    # Simple YAML-ish parser — handles nested specs: block
    # If no closing ---, treat \n\n# (markdown heading) as implicit boundary
    raw = m.group(1)
    if "---" not in raw[-20:]:  # heuristic: no dedicated close delimiter
        # Split at first markdown heading
        heading_idx = re.search(r"\n\n#+\s", raw)
        if heading_idx:
            raw = raw[: heading_idx.start()]
    result: dict[str, Any] = {}
    current_section: dict[str, Any] | None = None

    for line in raw.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect section header (specs:, links:, price_ru:)
        if not line.startswith(" ") and stripped.endswith(":"):
            key = stripped[:-1].strip()
            if key in ("specs", "price_ru"):
                current_section = {}
                result[key] = current_section
            else:
                current_section = None
                result[key] = None  # will be filled
            continue

        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()

            # Parse quoted / raw values
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val == "null":
                val = None
            elif val == "true":
                val = True
            elif val == "false":
                val = False
            elif val.startswith("[") and val.endswith("]"):
                # Simple list
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]

            if current_section is not None and key in current_section:
                pass  # already set
            elif current_section is not None:
                current_section[key] = val
            else:
                result[key] = val

    return result


def extract_numeric(value: Any) -> float | None:
    """Extract numeric value from strings like '180W', '448 GB/s', '16 GB GDDR7 (128-bit)'."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, bool):
        return None
    # Find first number in string
    m = re.search(r"(\d+(?:\.\d+)?)", str(value))
    return float(m.group(1)) if m else None


def extract_number_from_field(specs: dict, field: str, prefix: str | None = None) -> float | None:
    """Extract a number from a specs field, optionally stripping a prefix."""
    raw = specs.get(field)
    if raw is None:
        return None
    s = str(raw)
    if prefix and s.startswith(prefix):
        s = s[len(prefix):]
    return extract_numeric(s)


# ── Predicate definitions ────────────────────────────────────────────

GPU_PREDICATES = {
    "local-llm-viable": {
        "description": "Подходит для локального запуска LLM (13B-модель в 4-bit)",
        "check": lambda s: (
            extract_number_from_field(s, "vram", "VRAM:") is not None
            and extract_number_from_field(s, "vram_bandwidth", "BW:") is not None
            and extract_number_from_field(s, "vram", "VRAM:") >= 16
            and extract_number_from_field(s, "vram_bandwidth", "BW:") >= 448
        ),
    },
    "silent-viable": {
        "description": "Бесшумная работа (<30 dBA под нагрузкой, fan-stop в idle)",
        "check": lambda s: (
            extract_number_from_field(s, "tbp", "TBP:") is not None
            and extract_number_from_field(s, "tbp", "TBP:") <= 150
        ),
    },
}

CPU_PREDICATES = {
    "frametime-optimized": {
        "description": "Минимизация frametime-спайков (3D V-Cache)",
        "check": lambda s: extract_number_from_field(s, "l3_cache", "L3:") is not None
        and extract_number_from_field(s, "l3_cache", "L3:") >= 96,
    },
    "productivity-workhorse": {
        "description": "Рабочая станция: 12+ ядер",
        "check": lambda s: extract_number_from_field(s, "cores", "Cores:") is not None
        and extract_number_from_field(s, "cores", "Cores:") >= 12,
    },
    "silent-viable": {
        "description": "Бесшумная работа с воздушным охлаждением (TDP ≤ 65W)",
        "check": lambda s: extract_number_from_field(s, "tdp", "TDP:") is not None
        and extract_number_from_field(s, "tdp", "TDP:") <= 65,
    },
}


def check_entry(filepath: Path, entry_type: str) -> dict[str, list[str]]:
    """Check an entry against predicates. Returns {tag: [debug_info]}."""
    frontmatter = parse_frontmatter(filepath)
    specs = frontmatter.get("specs", {})

    predicates = GPU_PREDICATES if entry_type == "gpu" else CPU_PREDICATES
    results: dict[str, list[str]] = {}

    for tag, pred in predicates.items():
        try:
            if pred["check"](specs):
                results[tag] = ["✓"]
            else:
                results[tag] = ["✗"]
        except Exception as e:
            results[tag] = [f"ERROR: {e}"]

    return results


def find_entries(catalog_path: Path, entry_type: str | None = None) -> list[tuple[Path, str]]:
    """Find all entry files (not index.md) in catalog."""
    entries: list[tuple[Path, str]] = []
    for root, dirs, files in os.walk(catalog_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".md") or f == "index.md":
                continue
            filepath = Path(root) / f
            fm = parse_frontmatter(filepath)
            etype = fm.get("type", "unknown")
            if entry_type and etype != entry_type:
                continue
            if etype in ("gpu", "cpu"):
                entries.append((filepath, etype))
    return sorted(entries, key=lambda e: e[0].name)


def main():
    entry_type = None
    target_entry = None
    target_tag = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            entry_type = args[i + 1]
            i += 2
        elif args[i] == "--entry" and i + 1 < len(args):
            target_entry = args[i + 1]
            i += 2
        elif args[i] == "--tag" and i + 1 < len(args):
            target_tag = args[i + 1]
            i += 2
        else:
            i += 1

    entries = find_entries(CATALOG, entry_type)

    if target_entry:
        entries = [e for e in entries if e[0].stem == target_entry or e[0].name == target_entry]

    if not entries:
        print("Нет entry для проверки.")
        sys.exit(0)

    # Collect results
    all_results: dict[str, dict[str, list[str]]] = {}
    for filepath, etype in entries:
        rel = filepath.relative_to(ROOT)
        all_results[str(rel)] = check_entry(filepath, etype)

    # Output
    if target_tag:
        print(f"\n# Предикат: {target_tag}\n")
        matched = 0
        unmatched = 0
        for path, tags in all_results.items():
            if target_tag in tags:
                status = tags[target_tag][0]
                if "✓" in status:
                    print(f"  ✓ {path}")
                    matched += 1
                else:
                    print(f"  ✗ {path}")
                    unmatched += 1
        print(f"\n  Всего: {matched} подходят, {unmatched} не подходят")
        return

    # Full report
    print(f"\n# Аудит предикатов ({len(entries)} entry)\n")
    for path, tags in all_results.items():
        etype = path.split("/")[1]  # catalog/{type}/...
        preds = GPU_PREDICATES if etype == "gpu" else CPU_PREDICATES
        tag_summary = " | ".join(
            f"{'✓' if '✓' in tags[t][0] else '✗'} {t}"
            for t in preds
        )
        print(f"  {path}")
        print(f"    {tag_summary}")

    # Summary stats
    print(f"\n# Сводка\n")
    all_tags = set()
    for tags in all_results.values():
        all_tags.update(tags.keys())

    for tag in sorted(all_tags):
        matched = sum(1 for tags in all_results.values() if tag in tags and "✓" in tags[tag][0])
        total = sum(1 for tags in all_results.values() if tag in tags)
        pred = GPU_PREDICATES.get(tag) or CPU_PREDICATES.get(tag) or {}
        desc = pred.get("description", "")
        print(f"  {tag}: {matched}/{total}  — {desc}")


if __name__ == "__main__":
    main()
