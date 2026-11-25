#!/usr/bin/env python3
"""Prove a schematic cleanup changed drawing only, not connectivity.

Usage:
    python3 tools/kicad_netlist_compare.py before.xml after.xml

Both files are `kicad-cli sch export netlist --format kicadxml` exports.
Nets are compared as sets of (reference, pin), ignoring net names, so
replacing labels with wires (which renames auto-named nets) passes, while
any merge, split or moved pin fails.

Exit code 0 = same connectivity; 1 = differences (listed).
"""
import sys
import xml.etree.ElementTree as ET


def load(path):
    root = ET.parse(path).getroot()
    nets = {}
    for net in root.iter("net"):
        pins = frozenset((n.get("ref"), n.get("pin")) for n in net.iter("node"))
        nets[pins] = net.get("name")
    return nets


def main(before_path, after_path):
    before, after = load(before_path), load(after_path)
    pin_net_a = {p: k for k in after for p in k}
    removed = [k for k in before if k not in after]
    added = [k for k in after if k not in before]
    renamed = [(before[k], after[k]) for k in before if k in after and before[k] != after[k]]

    for name_a, name_b in sorted(renamed):
        print(f"renamed (OK): {name_a} -> {name_b}")
    if not removed and not added:
        print(f"\nSAME CONNECTIVITY: {len(before)} nets, {len(renamed)} renamed")
        return 0

    print(f"\nCONNECTIVITY CHANGED: {len(removed)} nets gone, {len(added)} new")
    for k in removed:
        dest = {after.get(pin_net_a[p], "?") if p in pin_net_a else "(pin missing)" for p in k}
        print(f"  was {before[k]} ({len(k)} pins) -> now spread over: {sorted(dest)}")
    for k in added:
        print(f"  new {after[k]} ({len(k)} pins): {sorted(f'{r}.{p}' for r, p in k)[:10]}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
