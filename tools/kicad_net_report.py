#!/usr/bin/env python3
"""Report how one KiCad sheet connects to the rest of the hierarchy.

Usage:
    kicad-cli sch export netlist --format kicadxml -o /tmp/net.xml hardware/brd-01/kicad/brd-01.kicad_sch
    python3 tools/kicad_net_report.py /tmp/net.xml hardware/brd-01/kicad/power.kicad_sch

Uses only the exported netlist (connectivity) and the sheet file (label
text). Classifies every net that touches the sheet:

  CROSS   leaves the sheet: power symbol (rail) or hierarchical label (signal)
  LOCAL   stays on the sheet: candidate for a direct wire
  NC      single-pin net: no-connect flag

It also flags global labels used only on this sheet and nets drawn with
both a global label and a power symbol.
"""
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


def sheet_of(comp):
    return comp.find("sheetpath").get("names").strip("/") or "root"


def main(netlist, sheet_file):
    sheet_path = Path(sheet_file)
    sheet = sheet_path.stem
    root = ET.parse(netlist).getroot()
    where = {c.get("ref"): sheet_of(c) for c in root.iter("comp")}
    value = {c.get("ref"): c.findtext("value") for c in root.iter("comp")}

    text = sheet_path.read_text()
    glabels = set(re.findall(r'\(global_label "([^"]+)"', text))
    llabels = set(re.findall(r'\n\t\(label "([^"]+)"', text))
    powers = set(re.findall(r'\(lib_id "power:([^"]+)"', text))
    others = defaultdict(set)
    for f in sheet_path.parent.glob("*.kicad_sch"):
        if f == sheet_path:
            continue
        for name in set(re.findall(r'\(global_label "([^"]+)"', f.read_text())):
            others[name].add(f.stem)

    rows = {"CROSS": [], "LOCAL": [], "NC": []}
    for net in root.iter("net"):
        nodes = [(n.get("ref"), n.get("pin"), n.get("pinfunction") or "") for n in net.iter("node")]
        by_sheet = defaultdict(list)
        for ref, pin, func in nodes:
            by_sheet[where[ref]].append(f"{ref}.{pin}" + (f"({func.split('_')[0]})" if func else ""))
        if sheet not in by_sheet:
            continue
        name = net.get("name")
        if len(nodes) == 1:
            rows["NC"].append((name, by_sheet[sheet]))
        elif len(by_sheet) > 1:
            rows["CROSS"].append((name, {s: len(v) for s, v in by_sheet.items()}))
        else:
            rows["LOCAL"].append((name, by_sheet[sheet]))

    print(f"# {sheet}: {sum(map(len, rows.values()))} nets\n")
    print("## CROSS (power symbol for rails, hierarchical label for signals)")
    for name, counts in sorted(rows["CROSS"]):
        print(f"  {name:28s} pins per sheet: {counts}")
    print("\n## LOCAL (wire directly; keep a local label only to name a PCB net)")
    for name, pins in sorted(rows["LOCAL"], key=lambda r: len(r[1])):
        short = name.split("/")[-1]
        tag = "label" if short in llabels else ("GLOBAL label" if short in glabels else "auto")
        print(f"  {name:32s} {len(pins):3d} pins [{tag}] {' '.join(pins[:8])}{' ...' if len(pins) > 8 else ''}")
    print(f"\n## NC: {len(rows['NC'])} single-pin nets (check each has a no-connect flag)")

    print("\n## Global labels used only on this sheet (make them local or wires)")
    for name in sorted(glabels):
        if not others.get(name):
            print(f"  {name}")
    print("\n## Drawn with both a global label and a power symbol (pick one)")
    for name in sorted(glabels & powers):
        print(f"  {name}")
    _ = value  # kept for callers that extend the report


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
