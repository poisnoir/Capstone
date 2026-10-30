#!/usr/bin/env python3
"""Check that every internal path/link mentioned in a markdown doc resolves.

Scans backtick paths and markdown links. External files covered by
docs/reference/manifest.yml are accepted. Paths under local-only directories
(vendor/, reference-cache/, robot-arm/vendor/) are accepted.

Exit 1 if a path is missing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/reference/manifest.yml"
SKIP_DIRS = {".git", "vendor", "reference-cache", "__pycache__", ".venv", "node_modules"}
LOCAL_ONLY_PREFIXES = (
    "vendor/",
    "reference-cache/",
    "robot-arm/vendor/",
    "docs/extracts/",
)
KNOWN_EXT = (
    ".md", ".py", ".sh", ".yml", ".yaml", ".json", ".toml", ".txt",
    ".pdf", ".docx", ".xlsx", ".xls", ".zip", ".raw", ".op.raw",
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".csv", ".cir", ".log",
    ".m", ".v", ".sv", ".vhd", ".xdc", ".kicad_pcb", ".kicad_sch",
    ".kicad_pro", ".step", ".stl",
)
COMMAND_PREFIXES = (
    "python", "python3", "git", "gs", "pdftotext", "pdfunite", "unzip", "zip",
    "find", "rg", "cd", "mkdir", "cp", "mv", "tar", "ssh", "curl", "gh",
    "pip", "sudo", "make", "cmake", "verilator", "vivado", "kicad-cli",
)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
TICK_RE = re.compile(r"`([^`\n]+)`")


def normalize(raw: str) -> str | None:
    value = raw.strip().strip("<>")
    value = value.split("#", 1)[0].split("?", 1)[0]
    value = value.replace("%20", " ")
    value = value.rstrip(".,;:")
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "~", "/home", "/tmp")):
        return None
    if any(ch in value for ch in "*{}<>$…|\\"):
        return None
    if any(ch.isspace() for ch in value):
        return None
    if value.startswith(COMMAND_PREFIXES):
        return None
    if not value.endswith(KNOWN_EXT) and not value.endswith("/"):
        return None
    if not ("/" in value or value.endswith(KNOWN_EXT)):
        return None
    if value.startswith("./"):
        value = value[2:]
    return value


def main() -> int:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    basenames = {Path(str(e.get("file", "")).rstrip("/")).name for e in entries}
    prefixes = [str(e.get("file", "")) for e in entries if str(e.get("file", "")).endswith("/")]

    checked = 0
    external = 0
    missing: list[tuple[str, str]] = []

    for doc in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in doc.parts):
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        raw_values = set(LINK_RE.findall(text)) | set(TICK_RE.findall(text))
        for raw in raw_values:
            value = normalize(raw)
            if value is None:
                continue
            top_level = (
                "contract/", "docs/", "fpga/", "hardware/", "robot-arm/",
                "software/", "simulations/", "tools/", ".github/",
            )
            if not value.startswith(top_level) and not value.startswith("../"):
                # Bare filenames and prose shorthand are not paths unless they
                # resolve next to the doc. Only flag real repo paths / links.
                if not (doc.parent / value).exists():
                    continue
            checked += 1
            if value.startswith(LOCAL_ONLY_PREFIXES):
                external += 1
                continue
            candidates = [
                (doc.parent / value),
                (ROOT / value),
            ]
            if any(c.exists() for c in candidates):
                continue
            if Path(value).name in basenames or any(value.startswith(p) for p in prefixes):
                external += 1
                continue
            missing.append((str(doc.relative_to(ROOT)), value))

    print(f"checked: {checked} paths")
    print(f"external/local-only: {external}")
    if missing:
        print("\nmissing paths:")
        for doc, value in sorted(set(missing)):
            print(f"  - {doc}: {value}")
        return 1
    print("all internal paths resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
