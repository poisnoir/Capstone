#!/usr/bin/env python3
"""Verify a KiCad schematic refactor changed only layout, not the circuit.

    python3 tools/verify_driver_refactor.py --before OLD.xml --after NEW.xml \\
        [--schematic SHEET.kicad_sch ...] [--font-aspect 0.7]
        [--detour-ratio 3.0] [--detour-max 10]

Netlists come from `kicad-cli sch export netlist --format kicadxml -o ...`.
Net names and pin functions are deliberately ignored: replacing a wire run
with labels renames nets, which is not an electrical change.

Schematic checks: forbidden power rail global labels, unjunctioned wire
crossings, bbox overlaps (text/text, text/wire, text/pin, text/body,
wire/body, wire/pin-midspan), and every item inside the frame+15mm inset and
clear of the title block. Text bboxes are an APPROXIMATION: width =
--font-aspect * font width * number of characters, height = font height,
centred on the anchor unless (justify left/right/top/bottom) says otherwise.
Tune --font-aspect if the overlap counts look wrong. Symbol bodies come from
embedded lib_symbols graphics/pins transformed by (at x y angle)/(mirror);
an unresolvable symbol is reported as UNRESOLVED and fails the gate.
Hierarchical (sheet ...) blocks and their pins are checked under category
`sheetpin`. Detour ratio and wire-bound nets are ADVISORY only: they never
change the exit code.

Exit 0 = all pass, 1 = mismatch, 2 = bad input.
"""
import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

RAILS = {'GND', '+3.3V', '+5V_EXC', '+15V_FUSED', '+12VA', '-12VA'}
FRAME_INSET = 10.16          # docs/phase2/schematic_layout_rules.md §2, 8 grid steps
TEXT_MARGIN = 15.0           # required clearance inside that frame
TITLE_W, TITLE_H = 180.0, 36.0  # KiCad default bottom-right title block
DETAIL = 20                  # cap output per issue category
EPS = 1e-6
TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')
SIZES = {'A0': (1189, 841), 'A1': (841, 594), 'A2': (594, 420),
         'A3': (420, 297), 'A4': (297, 210), 'A5': (210, 148)}
TEXT_KINDS = ('text', 'label', 'global_label', 'hierarchical_label', 'netclass_flag')
LABEL_KINDS = ('label', 'global_label', 'hierarchical_label', 'netclass_flag')
CATEGORIES = ('rail', 'wire/wire', 'text/text', 'text/wire', 'text/pin',
              'text/body', 'wire/body', 'wire/pin', 'sheetpin', 'margin',
              'title', 'unresolved')


def sexpr(text):
    """Minimal KiCad s-expression reader: lists of tokens/strings/lists."""
    stack = [[]]
    for tok in TOKEN.findall(text):
        if tok == '(':
            node = []
            stack[-1].append(node)
            stack.append(node)
        elif tok == ')':
            stack.pop()
        elif tok.startswith('"'):
            stack[-1].append(tok[1:-1])
        else:
            stack[-1].append(tok)
    return stack[0][0]


def child(node, name):
    return next((n for n in node if isinstance(n, list) and n and n[0] == name), None)


def children(node, name):
    return [n for n in node if isinstance(n, list) and n and n[0] == name]


def point(node, name='at'):
    at = child(node, name)
    return (float(at[1]), float(at[2])) if at is not None else None


def coords(node):
    return (float(node[1]), float(node[2]))


def netlist(path):
    root = ET.parse(path).getroot()
    comps = {c.get('ref'): (c.findtext('value') or '', c.findtext('footprint') or '')
             for c in root.iter('comp')}
    nets = {}
    for net in root.iter('net'):
        pins = frozenset(f"{n.get('ref')}.{n.get('pin')}" for n in net.iter('node'))
        nets.setdefault(pins, net.get('name') or f"net {net.get('code')}")
    return comps, nets


def show_net(pins):
    names = sorted(pins)
    return ', '.join(names[:8]) + (f' ... (+{len(names) - 8})' if len(names) > 8 else '')


def check_parts(before, after):
    a, b = set(before), set(after)
    missing, extra = sorted(a - b), sorted(b - a)
    changed = sorted(r for r in a & b if before[r] != after[r])
    if not (missing or extra or changed):
        print(f"Component identity: IDENTICAL ({len(a)} components)")
        return True
    print(f"Component identity: DIFFERENT ({len(a)} -> {len(b)} components)")
    for ref in missing[:DETAIL]:
        print(f"  MISSING  {ref}: {before[ref]}")
    for ref in extra[:DETAIL]:
        print(f"  EXTRA    {ref}: {after[ref]}")
    for ref in changed[:DETAIL]:
        print(f"  CHANGED  {ref}: value {before[ref][0]!r}->{after[ref][0]!r}, "
              f"footprint {before[ref][1]!r}->{after[ref][1]!r}")
    return False


def check_nets(before, after):
    removed, added = set(before) - set(after), set(after) - set(before)
    if not (removed or added):
        print(f"Connectivity: IDENTICAL ({len(before)} nets, names ignored)")
        return True
    print(f"Connectivity: DIFFERENT ({len(removed)} removed, {len(added)} added)")
    for pins in sorted(removed, key=show_net)[:DETAIL]:
        print(f"  REMOVED  {before[pins]} [{len(pins)} pins]: {show_net(pins)}")
    for pins in sorted(added, key=show_net)[:DETAIL]:
        print(f"  ADDED    {after[pins]} [{len(pins)} pins]: {show_net(pins)}")
    return False


def paper_size(root):
    paper = child(root, 'paper')
    if paper is None:
        raise ValueError('sheet has no (paper ...) header')
    name = paper[1]
    if name == 'User':
        size = (float(paper[2]), float(paper[3]))
    else:
        size = SIZES[name]
    if 'portrait' in paper:
        size = size[::-1]
    return size


def crossings(wires, junctions):
    """Interior crossings of one horizontal and one vertical wire, no junction."""
    out = []
    for i, (a, b) in enumerate(wires):
        horiz = a[1] == b[1]
        for c, d in wires[i + 1:]:
            if horiz == (c[1] == d[1]):   # parallel or degenerate: no crossing
                continue
            p = (c[0], a[1]) if horiz else (a[0], c[1])
            if not (min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS
                    and min(c[1], d[1]) - EPS <= p[1] <= max(c[1], d[1]) + EPS
                    and min(c[0], d[0]) - EPS <= p[0] <= max(c[0], d[0]) + EPS
                    and min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS):
                continue
            if p in (a, b, c, d):        # shared end or T-junction = connected
                continue
            if any(abs(p[0] - j[0]) < EPS and abs(p[1] - j[1]) < EPS
                   for j in junctions):
                continue
            out.append((p, (a, b), (c, d)))
    return out


# --- geometry helpers -------------------------------------------------------

def box_hit(a, b, tol=EPS):
    """Positive-area overlap, not edge touching."""
    return (min(a[2], b[2]) - max(a[0], b[0]) > tol
            and min(a[3], b[3]) - max(a[1], b[1]) > tol)


def box_at(p, box):
    return (box[0] - EPS <= p[0] <= box[2] + EPS
            and box[1] - EPS <= p[1] <= box[3] + EPS)


def bbox(points):
    return (min(p[0] for p in points), min(p[1] for p in points),
            max(p[0] for p in points), max(p[1] for p in points))


def shrink(box, amount):
    return (box[0] + amount, box[1] + amount, box[2] - amount, box[3] - amount)


def seg_box(a, b, box):
    """First segment/box intersection point (Liang-Barsky), or None."""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - box[0]), (dx, box[2] - a[0]),
                 (-dy, a[1] - box[1]), (dy, box[3] - a[1])):
        if abs(p) < EPS:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return (a[0] + t0 * dx, a[1] + t0 * dy)


def seg_seg(a, b, c, d):
    """Intersection point and parameters (t on ab, u on cd), or None."""
    r, s = (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])
    denom = r[0] * s[1] - r[1] * s[0]
    if abs(denom) < EPS:
        # Collinear overlap (a wire running along a pin) still intersects.
        if abs(r[0] * (c[1] - a[1]) - r[1] * (c[0] - a[0])) > EPS:
            return None
        axis = 0 if abs(r[0]) > abs(r[1]) else 1
        lo = max(min(a[axis], b[axis]), min(c[axis], d[axis]))
        hi = min(max(a[axis], b[axis]), max(c[axis], d[axis]))
        if hi - lo <= EPS:
            return None
        q = (lo + hi) / 2
        p = (q, a[1]) if axis == 0 else (a[0], q)
        t = (q - a[axis]) / r[axis]
        u = (q - c[axis]) / s[axis]
        return (p, t, u)
    q = (c[0] - a[0], c[1] - a[1])
    t = (q[0] * s[1] - q[1] * s[0]) / denom
    u = (q[0] * r[1] - q[1] * r[0]) / denom
    if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
        return ((a[0] + t * r[0], a[1] + t * r[1]), t, u)
    return None


def near(p, q, tol=0.02):
    return abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol


def font_size(node):
    eff = child(node, 'effects')
    font = child(eff, 'font') if eff else None
    size = child(font, 'size') if font else None
    return (float(size[1]), float(size[2])) if size else (1.27, 1.27)


def text_box(node, kind, aspect):
    """Approximate the glyph box; see module docstring."""
    at = child(node, 'at')
    if at is None:
        return None
    anchor = (float(at[1]), float(at[2]))
    angle = float(at[3]) if len(at) > 3 else 0.0
    h, w = font_size(node)
    if int(round(angle)) % 180 == 90:
        h, w = w, h
    idx = 2 if kind == 'property' else 1
    value = node[idx] if len(node) > idx and isinstance(node[idx], str) else ''
    width = max(aspect * w * len(value), h * 0.5)
    eff = child(node, 'effects')
    just = child(eff, 'justify') if eff else None
    j = just[1:] if just else []
    x1 = anchor[0] - (width if 'right' in j else 0 if 'left' in j else width / 2)
    y1 = anchor[1] - (0 if 'bottom' in j else h if 'top' in j else h / 2)
    return dict(name=f'{kind} "{value}"', box=(x1, y1, x1 + width, y1 + h),
                anchor=anchor, kind=kind, owner=None,
                annotation=kind in LABEL_KINDS)


def lib_units(root):
    libs = child(root, 'lib_symbols')
    out = {}
    for sym in children(libs, 'symbol') if libs else []:
        units = children(sym, 'symbol')
        out[sym[1]] = units if units else [sym]
    return out


def select_units(units, unit_no):
    picked = []
    for unit in units:
        name = unit[1] if len(unit) > 1 else ''
        m = re.search(r'_(\d+)_(\d+)$', name)
        if m is None or int(m.group(1)) in (0, unit_no):
            picked.append(unit)
    return picked or units


def local_geometry(units):
    """Graphic points (body), all points, pin segments and pin numbers (local)."""
    body, allpts, pins, numbers = [], [], [], []
    for unit in units:
        for shape in (children(unit, 'polyline') + children(unit, 'rectangle')
                      + children(unit, 'arc') + children(unit, 'circle')):
            pts = []
            xy = child(shape, 'pts')
            if xy is not None:
                pts = [coords(p) for p in children(xy, 'xy')]
            for key in ('start', 'end', 'mid'):
                node = child(shape, key)
                if node is not None:
                    pts.append(coords(node))
            center = child(shape, 'center')
            if center is not None:
                c = coords(center)
                radius = child(shape, 'radius')
                r = float(radius[1]) if radius else 0.0
                pts += [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
            body += pts
            allpts += pts
        for pin in children(unit, 'pin'):
            at = child(pin, 'at')
            length = child(pin, 'length')
            if at is None or length is None:
                continue
            x, y = float(at[1]), float(at[2])
            ang = float(at[3]) if len(at) > 3 else 0.0
            tip = (x, y)
            inner = (x + float(length[1]) * math.cos(math.radians(ang)),
                     y + float(length[1]) * math.sin(math.radians(ang)))
            pins.append((tip, inner))
            number = child(pin, 'number')
            numbers.append(number[1] if number and len(number) > 1 else '')
            allpts += [tip, inner]
    if not allpts:
        return None
    return body, allpts, pins, numbers


def transform(p, x, y, rot, mirror):
    px, py = p
    if mirror == 'x':
        py = -py
    elif mirror == 'y':
        px = -px
    if rot == 90:
        px, py = -py, px
    elif rot == 180:
        px, py = -px, -py
    elif rot == 270:
        px, py = py, -px
    return (x + px, y - py)


def placed_symbols(root, aspect, issues):
    units_map = lib_units(root)
    out = []
    for sym in children(root, 'symbol'):
        lib = child(sym, 'lib_id')
        at = child(sym, 'at')
        if lib is None or at is None:
            continue
        ref = next((p[2] for p in children(sym, 'property')
                    if len(p) > 2 and p[1] == 'Reference'), '?')
        x, y = float(at[1]), float(at[2])
        rot = int(float(at[3])) if len(at) > 3 else 0
        mir = child(sym, 'mirror')
        mirror = mir[1] if mir else None
        unit_no = child(sym, 'unit')
        geom = local_geometry(select_units(units_map.get(lib[1], []),
                                           int(unit_no[1]) if unit_no else 1))
        if geom is None:
            issues['unresolved'].append(f'UNRESOLVED geometry for {ref} ({lib[1]})')
            continue
        body_local, all_local, pin_local, number_local = geom
        tf = lambda p: transform(p, x, y, rot, mirror)
        allpts = [tf(p) for p in all_local]
        bodypts = [tf(p) for p in body_local]
        pins = [(tf(tip), tf(inner)) for tip, inner in pin_local]
        pin_numbers = [(num, tf(tip)) for num, (tip, _) in zip(number_local, pin_local)]
        props = []
        for prop in children(sym, 'property'):
            if (child(prop, 'hide') is not None or len(prop) < 4
                    or not isinstance(prop[2], str) or not prop[2]):
                continue  # hidden or empty fields are not drawn
            item = text_box(prop, 'property', aspect)
            if item is not None:
                item['owner'] = ref
                item['annotation'] = False
                item['name'] = f'property {prop[1]} of {ref}'
                props.append(item)
        out.append(dict(ref=ref, box=bbox(allpts),
                        body=bbox(bodypts) if bodypts else None,
                        pins=pins, pin_numbers=pin_numbers, props=props))
    return out


def box_inside(a, b):
    return (b[0] - EPS <= a[0] and b[1] - EPS <= a[1]
            and a[2] <= b[2] + EPS and a[3] <= b[3] + EPS)


def near_border(p, box, tol=0.5):
    return (abs(p[0] - box[0]) < tol or abs(p[0] - box[2]) < tol
            or abs(p[1] - box[1]) < tol or abs(p[1] - box[3]) < tol)


def on_segment(p, a, b, tol=0.02):
    if abs((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) > tol:
        return False
    return (min(a[0], b[0]) - tol <= p[0] <= max(a[0], b[0]) + tol
            and min(a[1], b[1]) - tol <= p[1] <= max(a[1], b[1]) + tol)


def sheet_blocks(root, aspect):
    out = []
    for node in children(root, 'sheet'):
        at, size = child(node, 'at'), child(node, 'size')
        if at is None or size is None:
            continue
        x, y = float(at[1]), float(at[2])
        rect = (x, y, x + float(size[1]), y + float(size[2]))
        name = next((p[2] for p in children(node, 'property')
                     if len(p) > 2 and p[1] == 'Sheetname'), '?')
        pins = []
        for pin in children(node, 'pin'):
            item = text_box(pin, 'sheetpin', aspect)
            if item is not None:
                item['name'] = f'sheetpin "{pin[1]}" of {name}'
                item['owner'] = name
                pins.append(item)
        out.append(dict(rect=rect, name=name, pins=pins))
    return out


def wire_components(wires):
    """Group wires joined at exact endpoints; crossings without junctions do not join."""
    parent = list(range(len(wires)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, (a, b) in enumerate(wires):
        for j in range(i + 1, len(wires)):
            c, d = wires[j]
            if (near(a, c, EPS) or near(a, d, EPS)
                    or near(b, c, EPS) or near(b, d, EPS)):
                parent[find(j)] = find(i)
    groups = defaultdict(list)
    for i, wire in enumerate(wires):
        groups[find(i)].append(wire)
    return list(groups.values())


def advisory_metrics(root, wires, syms, sheets, pin_net, aspect, ratio_limit, max_find):
    """Report wire detours and label-only wiring; never affects the exit code."""
    labels = []
    for kind in LABEL_KINDS:
        for node in children(root, kind):
            item = text_box(node, kind, aspect)
            if item is not None:
                labels.append(item)
    comps = wire_components(wires)
    points = [[] for _ in comps]
    label_comps = defaultdict(set)
    conn = [(pos, 'pin', f"{s['ref']}.{num}")
            for s in syms for num, pos in s['pin_numbers']]
    conn += [(sp['anchor'], 'sheetpin', sp['name'])
             for sh in sheets for sp in sh['pins']]
    conn += [(lab['anchor'], 'label', lab['name']) for lab in labels]
    for pos, kind, name in conn:
        for i, segs in enumerate(comps):
            if any(on_segment(pos, a, b) for a, b in segs):
                points[i].append((pos, kind, name))
                if kind == 'label':
                    label_comps[name].add(i)

    detours = []
    for segs, hits in zip(comps, points):
        pts = [p for a, b in segs for p in (a, b)]
        lengths = [math.dist(a, b) for a, b in segs]
        total = sum(lengths)
        box = bbox(pts)
        diag = math.dist((box[0], box[1]), (box[2], box[3]))
        if diag <= EPS or total / diag <= ratio_limit:
            continue
        names = [n for _, kind, n in hits if kind == 'label']
        if not names:
            names = [pin_net.get(n, n) for _, kind, n in hits
                     if kind == 'pin' and n in pin_net]
        name = names[0] if names else f'net@{box[0]:.0f},{box[1]:.0f}'
        detours.append((total / diag, total, diag, name, lengths))
    detours.sort(key=lambda d: d[0], reverse=True)
    for ratio, total, diag, name, lengths in detours[:max_find]:
        parts = ', '.join(f'{x:.2f}' for x in lengths)
        print(f'ADVISORY DETOUR {name} ratio={ratio:.2f} length={total:.2f}mm '
              f'diag={diag:.2f}mm segments=[{parts}]')

    wired = {i for i, hits in enumerate(points)
             if len({(round(p[0], 3), round(p[1], 3)) for p, _, _ in hits}) >= 2}
    bound = {name for name, ids in label_comps.items() if ids & wired}
    print(f'wire-bound nets: {len(bound)} / {len(set(lab["name"] for lab in labels))}')


def check_schematic(path, aspect, pin_net=None, ratio_limit=3.0, detour_max=10):
    """Return (ok, issue-count, wire-count, skipped, category-counts)."""
    if not Path(path).is_file():
        print(f"Schematic {path}: SKIPPED (file not found)")
        return True, 0, 0, True, {}
    try:
        root = sexpr(Path(path).read_text())
    except (OSError, IndexError, ValueError) as exc:
        print(f"Schematic {path}: ERROR (cannot parse: {exc})")
        return False, 1, 0, False, {'unresolved': 1}
    issues = defaultdict(list)

    for lab in children(root, 'global_label'):
        if len(lab) > 1 and lab[1] in RAILS:
            issues['rail'].append(f"rail global_label {lab[1]} at {point(lab)}")

    wires = []
    for w in children(root, 'wire'):
        pts = child(w, 'pts')
        xy = children(pts, 'xy') if pts is not None else []
        if len(xy) != 2:
            continue
        wires.append((coords(xy[0]), coords(xy[1])))
    junctions = [p for p in (point(j) for j in children(root, 'junction')) if p]
    axis = [(a, b) for a, b in wires if a[0] == b[0] or a[1] == b[1]]
    for p, seg1, seg2 in crossings(axis, junctions):
        issues['wire/wire'].append(
            f"wire crossing @ {p}: {seg1} x {seg2} (no junction)")
    texts = []
    for kind in TEXT_KINDS:
        for node in children(root, kind):
            item = text_box(node, kind, aspect)
            if item is not None:
                texts.append(item)
    syms = placed_symbols(root, aspect, issues)
    for sym in syms:
        texts.extend(sym['props'])

    try:
        w, h = paper_size(root)
    except (ValueError, KeyError, IndexError) as exc:
        issues['unresolved'].append(f"cannot determine paper size: {exc}")
        w = h = 0
    inset = (FRAME_INSET + TEXT_MARGIN, FRAME_INSET + TEXT_MARGIN,
             w - FRAME_INSET - TEXT_MARGIN, h - FRAME_INSET - TEXT_MARGIN)
    title = (w - FRAME_INSET - TITLE_W, h - FRAME_INSET - TITLE_H,
             w - FRAME_INSET, h - FRAME_INSET)

    def geometry_check(box, name):
        if (box[0] < inset[0] - EPS or box[1] < inset[1] - EPS
                or box[2] > inset[2] + EPS or box[3] > inset[3] + EPS):
            issues['margin'].append(f'OUTSIDE {name} box {box}')
        if box_hit(box, title):
            cy = (max(box[1], title[1]) + min(box[3], title[3])) / 2
            cx = (max(box[0], title[0]) + min(box[2], title[2])) / 2
            issues['title'].append(f'TITLE-BLOCK {name} @ ({cx:.2f}, {cy:.2f})')

    for item in texts:
        geometry_check(item['box'], item['name'])
    for sym in syms:
        geometry_check(sym['box'], f'symbol {sym["ref"]}')
    for a, b in wires:
        geometry_check((min(a[0], b[0]), min(a[1], b[1]),
                        max(a[0], b[0]), max(a[1], b[1])),
                       f'wire {a}-{b}')

    for i, first in enumerate(texts):
        for second in texts[i + 1:]:
            if box_hit(first['box'], second['box']):
                p = (max(first['box'][0], second['box'][0]),
                     max(first['box'][1], second['box'][1]))
                issues['text/text'].append(
                    f'OVERLAP {first["name"]} x {second["name"]} @ ({p[0]:.2f}, {p[1]:.2f})')

    for item in texts:
        for a, b in wires:
            if (max(a[0], b[0]) < item['box'][0] - EPS
                    or min(a[0], b[0]) > item['box'][2] + EPS
                    or max(a[1], b[1]) < item['box'][1] - EPS
                    or min(a[1], b[1]) > item['box'][3] + EPS):
                continue
            hit = seg_box(a, b, item['box'])
            if hit is None:
                continue
            # A label on its own wire endpoint is annotation, not a collision.
            if item['annotation'] and any(box_at(p, item['box']) for p in (a, b)):
                continue
            issues['text/wire'].append(
                f'OVERLAP {item["name"]} x wire {a}-{b} @ ({hit[0]:.2f}, {hit[1]:.2f})')
        for sym in syms:
            for tip, inner in sym['pins']:
                for pin_pos in (tip, inner):
                    if not box_at(pin_pos, item['box']):
                        continue
                    if near(pin_pos, item['anchor']):
                        continue
                    issues['text/pin'].append(
                        f'OVERLAP {item["name"]} x pin {sym["ref"]} @ {pin_pos}')
            if sym['body'] and box_hit(item['box'], sym['body']):
                p = (max(item['box'][0], sym['body'][0]),
                     max(item['box'][1], sym['body'][1]))
                issues['text/body'].append(
                    f'OVERLAP {item["name"]} x body {sym["ref"]} @ ({p[0]:.2f}, {p[1]:.2f})')

    for a, b in wires:
        for sym in syms:
            body = shrink(sym['body'], 0.2) if sym['body'] else None
            if body and (min(a[0], b[0]) <= body[2] and max(a[0], b[0]) >= body[0]
                         and min(a[1], b[1]) <= body[3] and max(a[1], b[1]) >= body[1]):
                hit = seg_box(a, b, body)
                if hit is not None and not any(near(hit, p)
                                               for seg in sym['pins'] for p in seg):
                    issues['wire/body'].append(
                        f'OVERLAP wire {a}-{b} x body {sym["ref"]} @ ({hit[0]:.2f}, {hit[1]:.2f})')
            for tip, inner in sym['pins']:
                if (max(a[0], b[0]) < min(tip[0], inner[0]) - EPS
                        or min(a[0], b[0]) > max(tip[0], inner[0]) + EPS
                        or max(a[1], b[1]) < min(tip[1], inner[1]) - EPS
                        or min(a[1], b[1]) > max(tip[1], inner[1]) + EPS):
                    continue
                hit = seg_seg(a, b, tip, inner)
                if hit and 0.02 < hit[1] < 0.98 and 0.02 < hit[2] < 0.98:
                    p = hit[0]
                    issues['wire/pin'].append(
                        f'OVERLAP wire {a}-{b} x pin {sym["ref"]}-midspan @ ({p[0]:.2f}, {p[1]:.2f})')

    sheets = sheet_blocks(root, aspect)
    sheetpins = [sp for sh in sheets for sp in sh['pins']]
    for i, sp in enumerate(sheetpins):
        for other in sheetpins[i + 1:]:
            if box_hit(sp['box'], other['box']):
                p = (max(sp['box'][0], other['box'][0]),
                     max(sp['box'][1], other['box'][1]))
                issues['sheetpin'].append(
                    f'OVERLAP {sp["name"]} x {other["name"]} @ ({p[0]:.2f}, {p[1]:.2f})')
        for item in texts:
            if box_hit(sp['box'], item['box']):
                p = (max(sp['box'][0], item['box'][0]),
                     max(sp['box'][1], item['box'][1]))
                issues['sheetpin'].append(
                    f'OVERLAP {sp["name"]} x {item["name"]} @ ({p[0]:.2f}, {p[1]:.2f})')
        for a, b in wires:
            if (max(a[0], b[0]) < sp['box'][0] or min(a[0], b[0]) > sp['box'][2]
                    or max(a[1], b[1]) < sp['box'][1] or min(a[1], b[1]) > sp['box'][3]):
                continue
            hit = seg_box(a, b, sp['box'])
            if hit is not None and not near(hit, sp['anchor']):
                issues['sheetpin'].append(
                    f'OVERLAP {sp["name"]} x wire {a}-{b} @ ({hit[0]:.2f}, {hit[1]:.2f})')
        for sh in sheets:
            rect = sh['rect']
            overlap = box_hit(sp['box'], rect)
            if sh['name'] == sp['owner']:
                if overlap and not box_inside(sp['box'], rect) and not near_border(sp['anchor'], rect):
                    issues['sheetpin'].append(
                        f'OVERLAP {sp["name"]} x its sheet border {sh["name"]} @ {sp["anchor"]}')
                if not overlap and not box_at(sp['anchor'], rect):
                    issues['sheetpin'].append(
                        f'OUTSIDE {sp["name"]} its sheet block {sh["name"]} @ {sp["anchor"]}')
            elif overlap and not box_inside(sp['box'], rect):
                issues['sheetpin'].append(
                    f'OVERLAP {sp["name"]} x sheet block {sh["name"]} @ {sp["anchor"]}')
            elif box_inside(sp['box'], rect):
                issues['sheetpin'].append(
                    f'INSIDE {sp["name"]} foreign sheet block {sh["name"]} @ {sp["anchor"]}')

    for i, sh in enumerate(sheets):
        for other in sheets[i + 1:]:
            if box_hit(sh['rect'], other['rect']):
                p = (max(sh['rect'][0], other['rect'][0]),
                     max(sh['rect'][1], other['rect'][1]))
                issues['sheetpin'].append(
                    f'OVERLAP sheet block {sh["name"]} x {other["name"]} @ ({p[0]:.2f}, {p[1]:.2f})')
        for sym in syms:
            if box_hit(sh['rect'], sym['box']):
                p = (max(sh['rect'][0], sym['box'][0]),
                     max(sh['rect'][1], sym['box'][1]))
                issues['sheetpin'].append(
                    f'OVERLAP sheet block {sh["name"]} x symbol {sym["ref"]} @ ({p[0]:.2f}, {p[1]:.2f})')
        for item in texts:
            if box_hit(sh['rect'], item['box']):
                p = (max(sh['rect'][0], item['box'][0]),
                     max(sh['rect'][1], item['box'][1]))
                issues['sheetpin'].append(
                    f'OVERLAP sheet block {sh["name"]} x {item["name"]} @ ({p[0]:.2f}, {p[1]:.2f})')
        for a, b in wires:
            hit = seg_box(a, b, shrink(sh['rect'], 0.2))
            if hit is None:
                continue
            if any(near(hit, sp['anchor']) for sp in sh['pins']):
                continue
            if any(near(hit, p) for sym in syms for seg in sym['pins'] for p in seg):
                continue
            issues['sheetpin'].append(
                f'OVERLAP sheet block {sh["name"]} x wire {a}-{b} @ ({hit[0]:.2f}, {hit[1]:.2f})')

    counts = {cat: len(issues[cat]) for cat in CATEGORIES if issues[cat]}
    total = sum(counts.values())
    for cat in CATEGORIES:
        for line in issues[cat][:DETAIL]:
            print(f'  {path}: {line}')
        if len(issues[cat]) > DETAIL:
            print(f'  {path}: ... and {len(issues[cat]) - DETAIL} more {cat} issues')
    detail = ', '.join(f'{k} {v}' for k, v in counts.items()) or 'none'
    print(f"Schematic {path}: {'PASS' if not total else 'FAIL'} "
          f"({total} issues [{detail}], {len(wires)} wires)")
    advisory_metrics(root, wires, syms, sheets, pin_net or {}, aspect,
                     ratio_limit, detour_max)
    return not total, total, len(wires), False, counts


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--before', required=True, help='baseline kicadxml netlist')
    ap.add_argument('--after', required=True, help='refactored kicadxml netlist')
    ap.add_argument('--schematic', action='append', default=[],
                    help='schematic to check (repeatable, optional)')
    ap.add_argument('--font-aspect', type=float, default=0.7,
                    help='text width = aspect * font width * characters (default: 0.7)')
    ap.add_argument('--detour-ratio', type=float, default=3.0,
                    help='advisory: flag wire paths longer than ratio * bbox diagonal (default: 3.0)')
    ap.add_argument('--detour-max', type=int, default=10,
                    help='advisory: maximum detour findings per sheet (default: 10)')
    args = ap.parse_args(argv)
    if not 0.1 <= args.font_aspect <= 3.0:
        print('error: --font-aspect must be between 0.1 and 3.0', file=sys.stderr)
        return 2
    if args.detour_ratio < 1 or args.detour_max < 0:
        print('error: --detour-ratio must be >= 1 and --detour-max >= 0', file=sys.stderr)
        return 2
    try:
        comps_a, nets_a = netlist(args.before)
        comps_b, nets_b = netlist(args.after)
        ok = [check_parts(comps_a, comps_b), check_nets(nets_a, nets_b)]
    except (OSError, ET.ParseError, TypeError) as exc:
        print(f"error: cannot read netlist: {exc}", file=sys.stderr)
        return 2

    pin_net = {pin: name for name, pins in nets_b.items() for pin in pins}
    for sheet in args.schematic:
        good, _, _, skipped, _ = check_schematic(sheet, args.font_aspect,
                                                 pin_net, args.detour_ratio,
                                                 args.detour_max)
        if not skipped:
            ok.append(good)

    passed = all(ok)
    print(f"\nSUMMARY: {'IDENTICAL — all checks passed' if passed else 'DIFFERENT — see findings above'} "
          f"({sum(ok)}/{len(ok)} checks passed)")
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
