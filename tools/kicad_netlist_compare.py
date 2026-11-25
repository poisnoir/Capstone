#!/usr/bin/env python3
"""Prove a schematic edit changed drawing only, not connectivity.

    kicad_netlist_compare.py before.xml after.xml

Both files come from `kicad-cli sch export netlist --format kicadxml`.
Compares three things:

1. Connectivity as pin-membership sets, ignoring net names (dropping facing
   labels renames auto-nets, which must not count as a change).
2. Splits and merges separately: a merge is one old net whose pins land on
   fewer new nets; a split is the reverse. Both are reported by name.
3. Part set equality: reference, value, library part and footprint.

Exit 0 = same connectivity and same parts, 1 = anything else.
"""
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def nets_of(path):
    root = ET.parse(path).getroot()
    nets = {}
    for net in root.iter('net'):
        pins = frozenset((n.get('ref'), n.get('pin')) for n in net.iter('node'))
        nets[pins] = net.get('name')
    return nets


def parts_of(path):
    root = ET.parse(path).getroot()
    out = {}
    for comp in root.iter('comp'):
        src = comp.find('libsource')
        out[comp.get('ref')] = (
            comp.findtext('value') or '',
            f"{src.get('lib')}:{src.get('part')}" if src is not None else '',
            comp.findtext('footprint') or '',
        )
    return out


def destinations(pins, pin_net):
    return sorted({pin_net.get(p, '?') for p in pins})


def main(before_path, after_path):
    a, b = nets_of(before_path), nets_of(after_path)
    pin_net = {p: k for k in b for p in k}
    removed = [k for k in a if k not in b]
    added = [k for k in b if k not in a]
    renamed = sorted((a[k], b[k]) for k in a if k in b and a[k] != b[k])

    for old, new in renamed:
        print(f"renamed (OK): {old} -> {new}")

    merges, splits = [], []
    for k in removed:
        dest = destinations(k, pin_net)
        (merges if len(dest) < len(k) and all(k) else splits).append((a[k], k, dest))
    for k in added:
        origin = sorted({a.get({p: n for n in a for p in n}.get(p), '?')
                         for p in k}) if k else []
        if not origin:
            continue
        _ = origin

    print()
    if not removed and not added:
        print(f"CONNECTIVITY SAME: {len(a)} nets, {len(renamed)} renamed")
    else:
        print(f"CONNECTIVITY CHANGED: {len(removed)} nets gone, {len(added)} new")
        for name, pins, dest in removed:
            label = "MERGE" if len(dest) == 1 else "SPLIT"
            print(f"  {label:5s} {name} ({len(pins)} pins) -> {dest}")
        for k in added:
            print(f"  new   {b[k]} ({len(k)} pins): "
                  f"{sorted(f'{r}.{p}' for r, p in k)[:10]}")

    pa, pb = parts_of(before_path), parts_of(after_path)
    only_a = sorted(set(pa) - set(pb), key=_refkey)
    only_b = sorted(set(pb) - set(pa), key=_refkey)
    changed = sorted((r for r in set(pa) & set(pb) if pa[r] != pb[r]), key=_refkey)
    print()
    if only_a or only_b or changed:
        print(f"PARTS CHANGED: {len(pa)} -> {len(pb)}")
        for r in only_a:
            print(f"  removed {r} {pa[r]}")
        for r in only_b:
            print(f"  added   {r} {pb[r]}")
        for r in changed:
            print(f"  changed {r}: {pa[r]} -> {pb[r]}")
    else:
        print(f"PARTS SAME: {len(pa)} components")

    return 0 if (not removed and not added and not only_a and not only_b
                 and not changed) else 1


def _refkey(ref):
    digits = ''.join(c for c in ref if c.isdigit())
    return (''.join(c for c in ref if not c.isdigit()), int(digits or 0))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
