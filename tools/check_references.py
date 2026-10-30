#!/usr/bin/env python3
"""Check that every external file referenced in a doc has a manifest row.

Exit 1 if a doc references a third-party asset (pdf/docx/xlsx/zip/raw) that is
not covered by docs/reference/manifest.yml.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/reference/manifest.yml"
EXTERNAL_SUFFIXES = (".pdf", ".zip", ".raw", ".op.raw")
SKIP_DIRS = {".git", "vendor", "reference-cache", "__pycache__", ".venv", "node_modules"}

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
TICK_RE = re.compile(r"`([^`\n]+)`")


def candidates(text: str) -> set[str]:
    found: set[str] = set()
    for match in LINK_RE.findall(text):
        found.add(match)
    for match in TICK_RE.findall(text):
        found.add(match)
    return found


def normalize(raw: str) -> str | None:
    value = raw.strip().strip("<>")
    value = value.split("#", 1)[0].split("?", 1)[0]
    value = value.replace("%20", " ")
    if not value or value.startswith(("#", ".", "http://", "https://", "mailto:", "~", "/home", "/tmp")):
        return None
    if any(ch in value for ch in "*{}<>$…|\\"):
        return None
    if "..." in value or "X.Y.Z" in value:
        return None
    if value.startswith("contract-") and value.endswith((".zip", ".json")):
        return None
    if any(ch.isspace() for ch in value):
        return None
    if value.startswith("./"):
        value = value[2:]
    return value


def main() -> int:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    basenames: set[str] = set()
    prefixes: list[str] = []
    ids: set[str] = set()
    problems: list[str] = []

    for e in entries:
        eid = str(e.get("id", ""))
        if eid in ids:
            problems.append(f"duplicate manifest id: {eid}")
        ids.add(eid)
        f = str(e.get("file", "")).strip()
        if not f:
            problems.append(f"{eid}: empty file")
            continue
        if f.endswith("/"):
            prefixes.append(f)
            basenames.add(Path(f.rstrip("/")).name)
        else:
            basenames.add(Path(f).name)

    vendor_basenames: set[str] = set()
    vendor_root = ROOT / "vendor"
    if vendor_root.exists():
        vendor_basenames = {p.name for p in vendor_root.rglob("*") if p.is_file()}

    external_refs: set[str] = set()
    missing: list[tuple[str, str]] = []

    for doc in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in doc.parts):
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        for raw in candidates(text):
            value = normalize(raw)
            if value is None:
                continue
            if not value.endswith(EXTERNAL_SUFFIXES):
                continue
            external_refs.add(value)
            local_candidates = [doc.parent / value, ROOT / value]
            local = next((p for p in local_candidates if p.exists()), None)
            covered = (
                Path(value).name in basenames
                or Path(value).name in vendor_basenames
                or any(value == p.rstrip("/") or value.startswith(p) for p in prefixes)
            )
            if covered:
                continue
            if "/" not in value and "vendor/" in text:
                # A bare vendor filename listed in a doc that points at vendor/.
                # The vendor snapshot is covered by its own manifest entry.
                continue
            if local is None:
                missing.append((str(doc.relative_to(ROOT)), value))
            elif value.startswith(("vendor/", "reference-cache/", "docs/extracts/")) or "/" not in value:
                # A local external asset (root PDF, vendor file, extract) with no
                # manifest row. Tracked own-work files under team folders are fine.
                missing.append((str(doc.relative_to(ROOT)), value))

    print(f"external refs: {len(external_refs)}")
    print(f"manifest entries: {len(entries)}")
    if problems:
        print("\nmanifest problems:")
        for p in problems:
            print(f"  - {p}")
    if missing:
        print("\nreferenced but not covered by the manifest:")
        for doc, value in sorted(set(missing)):
            print(f"  - {doc}: {value}")
        print("\nAdd an entry to docs/reference/manifest.yml, then run:")
        print("  python3 tools/gen_reference_manifest.py")
        return 1
    print("all external references are covered")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
