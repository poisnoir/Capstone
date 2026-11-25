#!/usr/bin/env python3
"""Grid-exact geometry helper for BRD-01 KiCad sheets (KiCad 10 S-expressions).

Read (no writes):
    kicad_sch_helper.py pins   SHEET [--refs U145,L141]
    kicad_sch_helper.py audit  SHEET [--bbox x1,y1,x2,y2]

Write (needs --apply):
    kicad_sch_helper.py wire  SHEET --from X,Y --to X,Y [--apply]
    kicad_sch_helper.py setpt SHEET --wire UUID --end 0|1 --to X,Y [--apply]
    kicad_sch_helper.py del   SHEET --uuids UUID[,UUID] [--apply]
    kicad_sch_helper.py nc    SHEET --at X,Y [--apply]
    kicad_sch_helper.py junction SHEET --at X,Y [--apply]
    kicad_sch_helper.py labelkind SHEET --uuids U --kind hierarchical_label|label [--apply]
    kicad_sch_helper.py label SHEET --text NAME --at X,Y [--angle A] [--apply]
    kicad_sch_helper.py sheetpin SHEET --sheet UUID --name N --at X,Y --angle A --shape S [--apply]
    kicad_sch_helper.py power SHEET --lib power:GND --at X,Y --ref '#PWR9xx' [--rot A] [--apply]
    kicad_sch_helper.py glabel SHEET --text NAME --at X,Y [--angle A] [--apply]
    kicad_sch_helper.py setrot SHEET --ref REF --rot 0|90|180|270 [--apply]
    kicad_sch_helper.py setvalue SHEET --ref REF --value TEXT [--apply]

Coordinates come from (lib_symbols) pin definitions plus each symbol's
(at x y rot) and (mirror x|y). Nothing is guessed. Grid is 1.27 mm. A wire end
must land exactly on a pin end: a wire crossing a pin mid-span does NOT
connect, which is the U145 fault this tool was built for.
"""
import re
import sys
from pathlib import Path

GRID = 1.27
TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')


def parse(text):
    stack = [[]]
    for tok in TOKEN.findall(text):
        if tok == '(':
            new = []
            stack[-1].append(new)
            stack.append(new)
        elif tok == ')':
            stack.pop()
        elif tok.startswith('"'):
            stack[-1].append(tok[1:-1])
        else:
            stack[-1].append(tok)
    return stack[0][0]


def child(node, name):
    for item in node:
        if isinstance(item, list) and item and item[0] == name:
            return item
    return None


def children(node, name):
    return [i for i in node if isinstance(i, list) and i and i[0] == name]


def lib_pins(root):
    table = {}
    libs = child(root, 'lib_symbols')
    if libs is None:
        return table
    for sym in children(libs, 'symbol'):
        pins = []
        for unit in children(sym, 'symbol'):
            for pin in children(unit, 'pin'):
                at = child(pin, 'at')
                pins.append((child(pin, 'number')[1], child(pin, 'name')[1],
                             float(at[1]), float(at[2])))
        table[sym[1]] = pins
    return table


def rotate(px, py, rot, mirror):
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
    return px, py


def instances(root):
    pins_of = lib_pins(root)
    out = []
    for sym in children(root, 'symbol'):
        lib = child(sym, 'lib_id')
        if lib is None:
            continue
        at = child(sym, 'at')
        mir = child(sym, 'mirror')
        ref = next((p[2] for p in children(sym, 'property')
                    if p[1] == 'Reference'), None)
        x, y, rot = float(at[1]), float(at[2]), int(float(at[3]))
        mirror = mir[1] if mir else None
        apins = []
        for pnum, pname, px, py in pins_of.get(lib[1], []):
            qx, qy = rotate(px, py, rot, mirror)
            apins.append((pnum, pname, round(x + qx, 4), round(y - qy, 4)))
        out.append(dict(ref=ref, lib=lib[1], x=x, y=y, rot=rot, mirror=mirror,
                        uuid=child(sym, 'uuid')[1], pins=apins))
    return out


def wires(root):
    out = []
    for w in children(root, 'wire'):
        xy = children(child(w, 'pts'), 'xy')
        out.append(dict(uuid=child(w, 'uuid')[1],
                        a=(float(xy[0][1]), float(xy[0][2])),
                        b=(float(xy[1][1]), float(xy[1][2]))))
    return out


def labels(root, kind):
    out = []
    for lab in children(root, kind):
        at = child(lab, 'at')
        out.append(dict(text=lab[1], uuid=child(lab, 'uuid')[1],
                        p=(float(at[1]), float(at[2]))))
    return out


def points(root, name):
    return [(float(child(j, 'at')[1]), float(child(j, 'at')[2]))
            for j in children(root, name)]


def on_wire(p, a, b, tol=1e-6):
    (px, py), (ax, ay), (bx, by) = p, a, b
    if abs((bx - ax) * (py - ay) - (by - ay) * (px - ax)) > tol:
        return False
    return (min(ax, bx) - tol <= px <= max(ax, bx) + tol
            and min(ay, by) - tol <= py <= max(ay, by) + tol)


def grade(v):
    return abs(v / GRID - round(v / GRID)) < 1e-6


def cmd_pins(path, refs):
    root = parse(Path(path).read_text())
    for inst in instances(root):
        if refs and inst['ref'] not in refs:
            continue
        print(f"\n{inst['ref']} {inst['lib']} at ({inst['x']}, {inst['y']}) "
              f"rot {inst['rot']} mirror {inst['mirror']}")
        for pnum, pname, px, py in sorted(inst['pins'], key=lambda p: (p[3], p[2])):
            flag = '' if (grade(px) and grade(py)) else '  OFF-GRID'
            print(f"   {pnum:>3s} {pname:18s} {px:9.2f} {py:9.2f}{flag}")


def cmd_audit(path, bbox):
    root = parse(Path(path).read_text())
    insts, ws = instances(root), wires(root)
    labs = (labels(root, 'label') + labels(root, 'global_label')
            + labels(root, 'hierarchical_label'))
    ncs = points(root, 'no_connect')
    pwr = [i for i in insts if i['lib'].startswith('power:')]

    def inside(p):
        if not bbox:
            return True
        x1, y1, x2, y2 = bbox
        return x1 <= p[0] <= x2 and y1 <= p[1] <= y2

    off = [(i['ref'], i['x'], i['y']) for i in insts
           if not (grade(i['x']) and grade(i['y']))]
    offw = [(w['uuid'], p) for w in ws for p in (w['a'], w['b'])
            if not (grade(p[0]) and grade(p[1]))]
    print(f"symbols {len(insts)}  wires {len(ws)}  labels {len(labs)}  "
          f"no_connect {len(ncs)}  power symbols {len(pwr)}")
    print(f"symbols off {GRID} grid: {len(off)}")
    for r, x, y in off[:20]:
        print(f"   {r} @ {x},{y}")
    print(f"wire ends off grid: {len(offw)}")
    for u, p in offw[:20]:
        print(f"   {u} @ {p}")

    print("\nopen pins (nothing at the pin end):")
    total = 0
    for inst in insts:
        for pnum, pname, px, py in inst['pins']:
            p = (px, py)
            if not inside(p):
                continue
            # endpoint coincidence only: a wire crossing a pin mid-span
            # does NOT connect in KiCad (the U145 failure mode)
            hit = any(p in (w['a'], w['b']) for w in ws)
            hit = hit or any(p in points(root, 'junction')
                             and on_wire(p, w['a'], w['b']) for w in ws)
            hit = hit or any(p == l['p'] for l in labs)
            hit = hit or any(p == n for n in ncs)
            hit = hit or any((qx, qy) == p
                             for q in pwr for _, _, qx, qy in q['pins'])
            if not hit:
                total += 1
                print(f"   {inst['ref']}.{pnum} {pname:16s} @ {px:.2f},{py:.2f}")
    print(f"   total {total}")

    print("\nhanging wire ends:")
    for i, w in enumerate(ws):
        for p in (w['a'], w['b']):
            if not inside(p):
                continue
            touch = sum(
                1 for j, o in enumerate(ws) if j != i
                and (p in (o['a'], o['b']) or on_wire(p, o['a'], o['b'])))
            touch += sum(1 for inst in insts for _, _, qx, qy in inst['pins']
                         if (qx, qy) == p)
            touch += sum(1 for l in labs if l['p'] == p)
            touch += sum(1 for n in ncs if n == p)
            if touch == 0:
                print(f"   {p} wire {w['uuid']}")

    print("\nlabels off any wire or pin:")
    for l in labs:
        if not inside(l['p']):
            continue
        onw = any(on_wire(l['p'], w['a'], w['b']) for w in ws)
        onp = any(l['p'] == (px, py) for i in insts for _, _, px, py in i['pins'])
        if not (onw or onp):
            print(f"   {l['text']:20s} @ {l['p']}  {l['uuid']}")


def block_span(text, uuid):
    at = text.find(f'(uuid "{uuid}")')
    if at < 0:
        sys.exit(f"uuid not found: {uuid}")
    start = text.rfind('\n\t(', 0, at)
    if start < 0:
        start = text.rfind('(', 0, at)
    depth, i = 0, start
    while i < len(text):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    sys.exit("unbalanced parentheses")


def save(path, text, apply_):
    if apply_:
        Path(path).write_text(text)
        print(f"wrote {path}")
    else:
        print("dry run (add --apply to write)")


def fmt(v):
    s = f"{v:.6f}".rstrip('0').rstrip('.')
    return s if s else '0'


def cmd_wire(path, a, b, apply_):
    text = Path(path).read_text()
    if not all(grade(v) for v in (a[0], a[1], b[0], b[1])):
        sys.exit(f"refusing off-grid wire {a} {b}")
    import uuid as _u
    new = (f'\t(wire\n\t\t(pts\n\t\t\t(xy {fmt(a[0])} {fmt(a[1])}) '
           f'(xy {fmt(b[0])} {fmt(b[1])})\n\t\t)\n'
           f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n'
           f'\t\t(uuid "{_u.uuid4()}")\n\t)\n')
    idx = text.rstrip().rfind(')')
    save(path, text[:idx] + new + text[idx:], apply_)


def cmd_setpt(path, wire_uuid, end, to, apply_):
    text = Path(path).read_text()
    if not (grade(to[0]) and grade(to[1])):
        sys.exit(f"refusing off-grid point {to}")
    start, stop = block_span(text, wire_uuid)
    blk = text[start:stop]
    xy = re.findall(r'\(xy ([\d.-]+) ([\d.-]+)\)', blk)
    if len(xy) != 2:
        sys.exit("wire block does not have 2 points")
    xy[end] = (fmt(to[0]), fmt(to[1]))
    blk = re.sub(r'\(xy [\d.-]+ [\d.-]+\) \(xy [\d.-]+ [\d.-]+\)',
                 f'(xy {xy[0][0]} {xy[0][1]}) (xy {xy[1][0]} {xy[1][1]})', blk)
    save(path, text[:start] + blk + text[stop:], apply_)


def cmd_del(path, uuids, apply_):
    text = Path(path).read_text()
    for u in uuids:
        start, stop = block_span(text, u)
        while start > 0 and text[start - 1] in ' \t':
            start -= 1
        if start > 0 and text[start - 1] == '\n':
            start -= 1
        text = text[:start] + text[stop:]
    save(path, text, apply_)


def cmd_glabel(path, text, at, angle, apply_):
    t = Path(path).read_text()
    if not all(grade(v) for v in at):
        sys.exit(f"refusing off-grid label {at}")
    import uuid as _u
    just = 'left' if angle in (0, 90) else 'right'
    new = (f'\t(global_label "{text}"\n\t\t(shape passive)\n'
           f'\t\t(at {fmt(at[0])} {fmt(at[1])} {angle})\n\t\t(effects\n'
           f'\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t)\n'
           f'\t\t\t(justify {just})\n\t\t)\n'
           f'\t\t(uuid "{_u.uuid4()}")\n'
           f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} 0)\n'
           f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
           f'\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n'
           f'\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n'
           f'\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
    idx = t.rstrip().rfind(')')
    save(path, t[:idx] + new + t[idx:], apply_)


def cmd_setvalue(path, ref, value, apply_):
    t = Path(path).read_text()
    for inst in instances(parse(t)):
        if inst['ref'] != ref:
            continue
        start, stop = block_span(t, inst['uuid'])
        blk = t[start:stop]
        new = re.sub(r'\(property "Value" "[^"]*"', f'(property "Value" "{value}"',
                     blk, count=1)
        if new == blk:
            sys.exit(f"no Value property on {ref}")
        save(path, t[:start] + new + t[stop:], apply_)
        return
    sys.exit(f"ref not found: {ref}")


def cmd_setrot(path, ref, rot, apply_):
    t = Path(path).read_text()
    root = parse(t)
    for inst in instances(root):
        if inst['ref'] != ref:
            continue
        start = t.find(f'(uuid "{inst["uuid"]}")')
        head = t.rfind('\n\t(symbol', 0, start)
        at = t.find('(at ', head)
        line_end = t.find(')', at)
        old = t[at:line_end]
        parts = old[4:].split()
        new_at = f'(at {parts[0]} {parts[1]} {rot}'
        save(path, t[:at] + new_at + t[line_end:], apply_)
        return
    sys.exit(f"ref not found: {ref}")


def _label_block(kind, text, at, angle, shape):
    just = 'right' if angle in (180, 270) else 'left'
    out = [f'\t({kind} "{text}"']
    if kind != 'label':
        out.append(f'\t\t(shape {shape})')
    out += [f'\t\t(at {fmt(at[0])} {fmt(at[1])} {angle})',
            '\t\t(effects', '\t\t\t(font', '\t\t\t\t(size 1 1)',
            '\t\t\t)', f'\t\t\t(justify {just})', '\t\t)']
    return '\n'.join(out)


def cmd_labelkind(path, uuids, kind, apply_, shape_override=None):
    """Rewrite labels in place: global_label -> hierarchical_label or label.

    A hierarchical label also names the net inside its own sheet, so the rest
    of that sheet keeps connecting by name with plain local labels.
    """
    t = Path(path).read_text()
    root = parse(t)
    found = {}
    for k in ('global_label', 'label', 'hierarchical_label'):
        for lab in labels(root, k):
            found[lab['uuid']] = (k, lab['text'], lab['p'])
    for u in uuids:
        if u not in found:
            sys.exit(f"label uuid not found: {u}")
        kind_old, text, pt = found[u]
        start, stop = block_span(t, u)
        blk = t[start:stop]
        ang = int(float(re.search(r'\(at [\d.-]+ [\d.-]+ ([\d.-]+)\)', blk).group(1)))
        shape = shape_override or 'passive'
        m = re.search(r'\(shape (\w+)\)', blk)
        if m and not shape_override:
            shape = m.group(1)
        import uuid as _u
        new = _label_block(kind, text, pt, ang, shape)
        new += f'\n\t\t(uuid "{_u.uuid4()}")\n\t)'
        t = t[:start] + new + t[stop:]
        print(f"  {text:18s} {kind_old} -> {kind} at {pt} angle {ang} shape {shape}")
    save(path, t, apply_)


def cmd_label(path, text, at, angle, apply_):
    t = Path(path).read_text()
    if not all(grade(v) for v in at):
        sys.exit(f"refusing off-grid label {at}")
    import uuid as _u
    new = _label_block('label', text, at, angle, 'passive')
    new += f'\n\t\t(uuid "{_u.uuid4()}")\n\t)\n'
    idx = t.rstrip().rfind(')')
    save(path, t[:idx] + new + t[idx:], apply_)


def cmd_sheetpin(path, sheet_uuid, name, at, angle, shape, apply_):
    t = Path(path).read_text()
    # no grid assert: a sheet pin has to sit on the sheet border, and borders
    # are drawn on whole millimetres, not on the 1.27 mm grid
    start, stop = block_span(t, sheet_uuid)
    blk = t[start:stop]
    import uuid as _u
    just = 'right' if angle in (180, 90) else 'left'
    pin = (f'\t\t(pin "{name}" {shape}\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} {angle})\n'
           f'\t\t\t(uuid "{_u.uuid4()}")\n'
           f'\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n'
           f'\t\t\t\t)\n\t\t\t\t(justify {just})\n\t\t\t)\n\t\t)\n')
    at_inst = blk.find('\t\t(instances')
    if at_inst < 0:
        sys.exit("sheet has no (instances) block")
    blk = blk[:at_inst] + pin + blk[at_inst:]
    save(path, t[:start] + blk + t[stop:], apply_)


def cmd_power(path, lib, at, rot, ref, apply_):
    """Place a power symbol with its pin exactly on `at`."""
    t = Path(path).read_text()
    if not all(grade(v) for v in at):
        sys.exit(f"refusing off-grid power symbol {at}")
    name = lib.split(':')[1]
    # reuse the sheet instance path from an existing power symbol: a symbol
    # with the wrong (path ...) is silently ignored by KiCad
    paths = re.findall(r'\(path "(/[^"]+)"', t)
    deep = [x for x in paths if x.count('/') >= 2]
    sheet_path = deep[0] if deep else "/bcf11a9e-584a-4da7-9f85-9c74b718d606"
    import uuid as _u
    u = _u.uuid4()
    new = (f'\t(symbol\n\t\t(lib_id "{lib}")\n'
           f'\t\t(at {fmt(at[0])} {fmt(at[1])} {rot})\n'
           f'\t\t(unit 1)\n\t\t(body_style 1)\n'
           f'\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n'
           f'\t\t(in_pos_files yes)\n\t\t(dnp no)\n'
           f'\t\t(uuid "{u}")\n'
           f'\t\t(property "Reference" "{ref}"\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1] + 3.81)} 0)\n'
           f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
           f'\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n'
           f'\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
           f'\t\t(property "Value" "{name}"\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1] - 3.81)} 0)\n'
           f'\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
           f'\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
           f'\t\t(property "Footprint" ""\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} 0)\n'
           f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
           f'\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
           f'\t\t(property "Datasheet" ""\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} 0)\n'
           f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
           f'\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
           f'\t\t(property "Description" ""\n'
           f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} 0)\n'
           f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
           f'\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
           f'\t\t(pin "1"\n\t\t\t(uuid "{_u.uuid4()}")\n\t\t)\n'
           f'\t\t(instances\n\t\t\t(project "brd-01"\n'
           f'\t\t\t\t(path "{sheet_path}"\n'
           f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n'
           f'\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
    idx = t.rstrip().rfind(')')
    save(path, t[:idx] + new + t[idx:], apply_)


def cmd_junction(path, at, apply_):
    t = Path(path).read_text()
    if not all(grade(v) for v in at):
        sys.exit(f"refusing off-grid junction {at}")
    import uuid as _u
    new = (f'\t(junction\n\t\t(at {fmt(at[0])} {fmt(at[1])})\n'
           f'\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n'
           f'\t\t(uuid "{_u.uuid4()}")\n\t)\n')
    idx = t.rstrip().rfind(')')
    save(path, t[:idx] + new + t[idx:], apply_)


def cmd_nc(path, at, apply_):
    text = Path(path).read_text()
    if not all(grade(v) for v in at):
        sys.exit(f"refusing off-grid no_connect {at}")
    import uuid as _u
    new = (f'\t(no_connect\n\t\t(at {fmt(at[0])} {fmt(at[1])})\n'
           f'\t\t(uuid "{_u.uuid4()}")\n\t)\n')
    idx = text.rstrip().rfind(')')
    save(path, text[:idx] + new + text[idx:], apply_)


def pair(s):
    x, y = s.split(',')
    return (float(x), float(y))


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd, path, rest = argv[1], argv[2], argv[3:]
    apply_ = '--apply' in rest
    rest = [r for r in rest if r != '--apply']
    try:
        if cmd == 'pins':
            refs = None
            if '--refs' in rest:
                refs = set(rest[rest.index('--refs') + 1].split(','))
            cmd_pins(path, refs)
        elif cmd == 'audit':
            bbox = None
            if '--bbox' in rest:
                bbox = [float(v) for v in
                        rest[rest.index('--bbox') + 1].split(',')]
            cmd_audit(path, bbox)
        elif cmd == 'wire':
            cmd_wire(path, pair(rest[rest.index('--from') + 1]),
                     pair(rest[rest.index('--to') + 1]), apply_)
        elif cmd == 'setpt':
            cmd_setpt(path, rest[rest.index('--wire') + 1],
                      int(rest[rest.index('--end') + 1]),
                      pair(rest[rest.index('--to') + 1]), apply_)
        elif cmd == 'del':
            cmd_del(path, rest[rest.index('--uuids') + 1].split(','), apply_)
        elif cmd == 'glabel':
            cmd_glabel(path, rest[rest.index('--text') + 1],
                       pair(rest[rest.index('--at') + 1]),
                       int(rest[rest.index('--angle') + 1]) if '--angle' in rest else 0,
                       apply_)
        elif cmd == 'setvalue':
            cmd_setvalue(path, rest[rest.index('--ref') + 1],
                         rest[rest.index('--value') + 1], apply_)
        elif cmd == 'setrot':
            cmd_setrot(path, rest[rest.index('--ref') + 1],
                       int(rest[rest.index('--rot') + 1]), apply_)
        elif cmd == 'labelkind':
            cmd_labelkind(path, rest[rest.index('--uuids') + 1].split(','),
                          rest[rest.index('--kind') + 1], apply_,
                          rest[rest.index('--shape') + 1]
                          if '--shape' in rest else None)
        elif cmd == 'label':
            cmd_label(path, rest[rest.index('--text') + 1],
                      pair(rest[rest.index('--at') + 1]),
                      int(rest[rest.index('--angle') + 1]) if '--angle' in rest else 0,
                      apply_)
        elif cmd == 'sheetpin':
            cmd_sheetpin(path, rest[rest.index('--sheet') + 1],
                         rest[rest.index('--name') + 1],
                         pair(rest[rest.index('--at') + 1]),
                         int(rest[rest.index('--angle') + 1]),
                         rest[rest.index('--shape') + 1] if '--shape' in rest
                         else 'passive', apply_)
        elif cmd == 'power':
            cmd_power(path, rest[rest.index('--lib') + 1],
                      pair(rest[rest.index('--at') + 1]),
                      int(rest[rest.index('--rot') + 1]) if '--rot' in rest else 0,
                      rest[rest.index('--ref') + 1], apply_)
        elif cmd == 'junction':
            cmd_junction(path, pair(rest[rest.index('--at') + 1]), apply_)
        elif cmd == 'nc':
            cmd_nc(path, pair(rest[rest.index('--at') + 1]), apply_)
        else:
            sys.exit(__doc__)
    except ValueError as exc:
        sys.exit(f"bad argument: {exc}")


if __name__ == '__main__':
    main(sys.argv)
