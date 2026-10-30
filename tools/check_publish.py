#!/usr/bin/env python3
"""Pre-public / hygiene check.

Default: report warnings, fail on hard policy violations (tracked PDFs,
vendor/reference-cache files, .raw output, files > 20 MB).

--public: also fail on student IDs and the Phase 1 report (use for the public
repo).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 20 * 1024 * 1024
STUDENT_ID_RE = re.compile(r"\b40\d{6}\b")
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".yml", ".yaml", ".json", ".csv"}


def tracked_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"])
        return [p for p in out.decode().split("\0") if p]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            str(p.relative_to(ROOT))
            for p in ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts
        ]


def main() -> int:
    public = "--public" in sys.argv
    hard: list[str] = []
    soft: list[str] = []

    for rel in tracked_files():
        path = ROOT / rel
        if not path.is_file():
            continue
        size = path.stat().st_size
        if rel.lower().endswith(".pdf"):
            hard.append(f"tracked PDF: {rel}")
        if rel.startswith(("vendor/", "reference-cache/")):
            hard.append(f"local-only directory tracked: {rel}")
        if rel.endswith((".raw", ".op.raw")):
            hard.append(f"generated simulation output tracked: {rel}")
        if size > MAX_BYTES:
            hard.append(f"file over 20 MB: {rel} ({size / 1048576:.1f} MB)")
        if "Phase 1 Report" in rel:
            (hard if public else soft).append(f"Phase 1 report with student IDs: {rel}")
        if path.suffix in TEXT_SUFFIXES:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            ids = sorted(set(STUDENT_ID_RE.findall(text)))
            if ids:
                (hard if public else soft).append(
                    f"student ID(s) in {rel}: {', '.join(ids)}"
                )

    if soft:
        print("warnings:")
        for item in sorted(set(soft)):
            print(f"  - {item}")
    if hard:
        print("hard failures:")
        for item in sorted(set(hard)):
            print(f"  - {item}")
        return 1

    print("publish check: clean")
    if not public:
        print("(default mode; use --public for the public-repo check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
