#!/usr/bin/env python3
"""
Query layer for PC Hardware Knowledge Base.

Reads all .md files in catalog/, extracts YAML frontmatter,
builds in-memory index, provides query capabilities.

Usage:
    python query.py --type motherboard --socket am5
    python query.py --vendor msi
    python query.py --tag ddr5 --tag atx
    python query.py --links-to catalog/memory/ddr5.md
    python query.py --status verified --type cpu
    python query.py --list-types
    python query.py --id msi-b650-tomahawk
    python query.py --search "RTX 5060"

Output: list of relative file paths (one per line).
"""

import argparse
import os
import sys
import yaml
from pathlib import Path
from typing import Any


KB_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(filepath: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(filepath) as f:
            content = f.read()
    except OSError:
        return None

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not isinstance(fm, dict):
        return None

    fm["_path"] = str(filepath.relative_to(KB_ROOT))
    return fm


def collect_entries(root: Path) -> list[dict[str, Any]]:
    """Walk catalog/ and concepts/, collect all entries with frontmatter."""
    entries = []
    for md_file in root.rglob("*.md"):
        if md_file.name == "index.md":
            continue  # indexes are structural, not queryable entries
        fm = parse_frontmatter(md_file)
        if fm and fm.get("id"):
            entries.append(fm)
    return entries


def matches(entry: dict[str, Any], args: argparse.Namespace) -> bool:
    """Check if an entry matches query parameters."""
    # Filter by type
    if args.type and entry.get("type") != args.type:
        return False

    # Filter by vendor
    if args.vendor:
        entry_vendor = entry.get("vendor")
        if not entry_vendor or entry_vendor.lower() != args.vendor.lower():
            return False

    # Filter by status
    if args.status and entry.get("status") != args.status:
        return False

    # Filter by id
    if args.id and entry.get("id") != args.id:
        return False

    # Filter by tags (all must match)
    if args.tag:
        entry_tags = entry.get("tags", [])
        if not entry_tags:
            return False
        entry_tags_lower = [t.lower() for t in entry_tags]
        for tag in args.tag:
            if tag.lower() not in entry_tags_lower:
                return False

    # Filter by socket (look in tags and specs)
    if args.socket:
        entry_tags = [t.lower() for t in entry.get("tags", [])]
        specs = entry.get("specs", {})
        socket_val = ""
        if isinstance(specs, dict):
            socket_val = specs.get("socket", "").lower()
        if (args.socket.lower() not in entry_tags and
                args.socket.lower() not in socket_val):
            return False

    # Filter by links-to: which entries link TO the given path
    if args.links_to:
        links = entry.get("links", {})
        if not links:
            return False
        target = args.links_to.strip("/")
        found = False
        if isinstance(links, dict):
            for v in links.values():
                if isinstance(v, str) and target in v:
                    found = True
                    break
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str) and target in item:
                            found = True
                            break
        if not found:
            return False

    # Fuzzy search: match substring in title or id (case-insensitive)
    if args.search:
        query = args.search.lower()
        title = entry.get("title", "").lower()
        eid = entry.get("id", "").lower()
        if query not in title and query not in eid:
            return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Query PC Hardware Knowledge Base"
    )
    parser.add_argument("--type", help="Filter by component type (cpu, gpu, motherboard, ...)")
    parser.add_argument("--vendor", help="Filter by vendor (amd, nvidia, msi, ...)")
    parser.add_argument("--status", help="Filter by status (draft, review, verified)")
    parser.add_argument("--tag", action="append", help="Filter by tag (repeatable, all must match)")
    parser.add_argument("--socket", help="Filter by socket (am5, lga1700, ...)")
    parser.add_argument("--id", help="Find exact entry by id")
    parser.add_argument("--links-to", help="Find entries that link TO the given relative path")
    parser.add_argument("--search", help="Fuzzy search: match substring in title or id (case-insensitive)")
    parser.add_argument("--list-types", action="store_true", help="List all component types in the KB")
    parser.add_argument("--list-tags", action="store_true", help="List all tags")
    parser.add_argument("--list-vendors", action="store_true", help="List all vendors")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show title and type alongside path")

    args = parser.parse_args()

    entries = collect_entries(KB_ROOT)

    if not entries:
        print("No entries found. Check that catalog/ contains .md files with frontmatter.", file=sys.stderr)
        sys.exit(1)

    # Meta-queries
    if args.list_types:
        types = sorted({e.get("type", "unknown") for e in entries if e.get("type") != "index"})
        for t in types:
            count = sum(1 for e in entries if e.get("type") == t)
            print(f"{t} ({count})")
        return

    if args.list_tags:
        all_tags: set[str] = set()
        for e in entries:
            for tag in e.get("tags", []):
                all_tags.add(tag)
        for tag in sorted(all_tags):
            count = sum(1 for e in entries if tag in e.get("tags", []))
            print(f"{tag} ({count})")
        return

    if args.list_vendors:
        vendors = sorted({e["vendor"] for e in entries if e.get("vendor")})
        for v in vendors:
            print(v)
        return

    # Standard query
    results = [e for e in entries if matches(e, args)]

    if args.verbose:
        for e in results:
            print(f"{e['_path']}  # {e.get('title', '?')} [{e.get('type', '?')}]")
    else:
        for e in results:
            print(e["_path"])

    if not results:
        print("No entries matched.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
