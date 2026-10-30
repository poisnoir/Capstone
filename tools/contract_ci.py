#!/usr/bin/env python3
"""Contract validation, hashing and release artifacts.

Commands:
    check                     validate VERSION, CHANGELOG, IDs, ICD status
    hash [--rev REV]          deterministic tree hash of contract/
    zip OUT                   deterministic zip of contract/
    json OUT                  release metadata (version, commit, hashes)
    release-notes OUT         changelog section for the current version
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contract"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def read_version() -> str:
    return (CONTRACT / "VERSION").read_text(encoding="utf-8").strip()


def changelog_text() -> str:
    return (CONTRACT / "CHANGELOG.md").read_text(encoding="utf-8")


def changelog_section(version: str) -> str:
    text = changelog_text()
    match = re.search(
        rf"^##\s+{re.escape(version)}\b.*?$(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    return (match.group(0)).strip()


def check() -> int:
    errors: list[str] = []
    version = read_version()
    if not VERSION_RE.match(version):
        errors.append(f"contract/VERSION is not semver: {version!r}")

    if not changelog_section(version):
        errors.append(f"contract/CHANGELOG.md has no '## {version}' section")

    sc_text = (CONTRACT / "system_contract.md").read_text(encoding="utf-8")
    sc_ids = re.findall(r"^\|\s*(SC-\d{2}[a-z]?)\s*\|", sc_text, re.MULTILINE)
    if not sc_ids:
        errors.append("contract/system_contract.md: no SC-xx rows found")
    dup_sc = sorted({x for x in sc_ids if sc_ids.count(x) > 1})
    if dup_sc:
        errors.append(f"duplicate SC ids: {', '.join(dup_sc)}")

    dec_text = (CONTRACT / "decisions_log.md").read_text(encoding="utf-8")
    dec_ids = re.findall(r"^\|\s*(\d+)\s*\|", dec_text, re.MULTILINE)
    if not dec_ids:
        errors.append("contract/decisions_log.md: no numbered rows found")
    dup_dec = sorted({x for x in dec_ids if dec_ids.count(x) > 1})
    if dup_dec:
        errors.append(f"duplicate decision numbers: {', '.join(dup_dec)}")

    for icd in sorted((CONTRACT / "icd").glob("*.md")):
        if icd.name == "README.md":
            continue
        if "**Status:**" not in icd.read_text(encoding="utf-8"):
            errors.append(f"{icd.relative_to(ROOT)}: missing '**Status:**' line")

    if errors:
        print("contract check failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"contract {version}: {len(sc_ids)} SC rows, {len(dec_ids)} decisions, ICDs OK")
    return 0


def _working_files() -> list[tuple[str, Path]]:
    """Contract files as (relative posix path, path), sorted by the string path.

    Sorting by Path objects puts a directory before a same-named file
    (`pico_link/` before `pico_link.md`); sorting by the relative string keeps
    the hash stable across the working tree and a git revision.
    """
    items: list[tuple[str, Path]] = []
    for path in CONTRACT.rglob("*"):
        if path.is_dir() or "__pycache__" in path.parts:
            continue
        items.append((path.relative_to(CONTRACT).as_posix(), path))
    return sorted(items)


def tree_hash(rev: str | None = None) -> str:
    digest = hashlib.sha256()
    if rev:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", rev, "contract"],
            text=True,
        )
        items: list[tuple[str, str]] = []
        for path in out.splitlines():
            if path.startswith("contract/"):
                items.append((path[len("contract/"):], path))
        for rel, path in sorted(items):
            content = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{rev}:{path}"])
            digest.update(rel.encode())
            digest.update(b"\0")
            digest.update(content)
            digest.update(b"\0")
        return digest.hexdigest()

    for rel, path in _working_files():
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def per_file_hashes() -> dict[str, str]:
    return {
        rel: hashlib.sha256(path.read_bytes()).hexdigest()
        for rel, path in _working_files()
    }


def make_zip(out: Path) -> None:
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(CONTRACT.rglob("*")):
            if path.is_dir() or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(CONTRACT).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return "unknown"


def make_json(out: Path) -> None:
    version = read_version()
    data = {
        "version": version,
        "tag": f"contract-v{version}",
        "commit": git_head(),
        "tree_sha256": tree_hash(),
        "files": per_file_hashes(),
        "published_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_notes(out: Path) -> None:
    version = read_version()
    section = changelog_section(version) or f"Contract {version}"
    out.write_text(section + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check", "hash", "zip", "json", "release-notes"])
    parser.add_argument("output", nargs="?")
    parser.add_argument("--rev", default=None)
    args = parser.parse_args()

    if args.command == "check":
        return check()
    if args.command == "hash":
        print(tree_hash(args.rev))
        return 0
    if not args.output:
        parser.error(f"{args.command} requires an output path")
    out = Path(args.output)
    if args.command == "zip":
        make_zip(out)
    elif args.command == "json":
        make_json(out)
    else:
        write_notes(out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
