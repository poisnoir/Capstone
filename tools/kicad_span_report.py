#!/usr/bin/env python3
"""Net span ledger for BRD-01 sheets (pin positions, never label positions).

    python3 tools/kicad_span_report.py SHEET.kicad_sch [--netlist XML] [--sheet /receiver/]
                                      [--blocks FILE] [--hubs U101,ADC_VCM]
                                      [--top N] [--min-span MM] [--include-rails] [--json]
    python3 tools/kicad_span_report.py --compare BEFORE.kicad_sch AFTER.kicad_sch
                                      [--netlist-before XML --netlist-after XML]
                                      [--blocks FILE] [--hubs U101,ADC_VCM]
                                      [--fail-on-regression] [--tolerance MM] [--json]

Span = (max x - min x) x (max y - min y) mm; S = width + height (the §3
convention of docs/phase2/schematic_layout_rules.md). Membership comes from
the kicadxml netlist; coordinates from kicad_sch_helper, unit-aware: a
multi-unit symbol contributes each pin once, at the unit that declares it.
A netlist is auto-exported with kicad-cli when --netlist is omitted; no
schematic is ever written. --min-span filters by S (by |dS| in --compare);
--top limits the report, and in --compare never hides a regressed net.

Blocks come from --blocks (JSON or "name x0,y0,x1,y1" CSV) or are inferred
by clustering symbol positions on both axes at gaps >= 12.7 mm. A net is
in-block when all its on-sheet pins sit in one block, cross-block otherwise;
a cross-block net touching a declared hub (its pin or its block) is INFO.
In-block nets with w or h > 25.4 mm get W6-HOP. --fail-on-regression fails ONLY on an
in-block span that got worse, or a new in-block hop above 25.4 mm; cross-block
growth never fails, and any block-membership change prints as MOVED BLOCK.

Exit 0 = report OK, 1 = error or (with --fail-on-regression) an in-block
regression / new in-block hop.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kicad_sch_helper as K  # noqa: E402  (house helper; read-only primitives)

EPS = 1e-9
POWER_LIB = re.compile(r'\(lib_id "power:([^"]+)"')
SUPPLY_NAME = re.compile(r'^[+-]\d')
BLOCK_GAP = 12.7     # minimum gap that separates two blocks when inferring
HOP_MAX = 25.4       # W6: maximum in-block label hop


# --- blocks ----------------------------------------------------------------

def symbol_positions(path):
    """ref -> (x, y) of symbol origins on this sheet (not off-sheet pins)."""
    root = K.parse(Path(path).read_text(encoding='utf-8'))
    out = {}
    for sym in K.children(root, 'symbol'):
        at = K.child(sym, 'at')
        ref = next((p[2] for p in K.children(sym, 'property')
                    if p[1] == 'Reference'), None)
        if ref and at:
            out[str(ref)] = (float(at[1]), float(at[2]))
    return out


def load_blocks(path):
    """Rectangles from JSON (list or name -> corners) or CSV name x0,y0,x1,y1."""
    text = Path(path).read_text(encoding='utf-8')
    try:
        data = json.loads(text)
    except ValueError:
        data = None
    if isinstance(data, dict) and 'blocks' in data:
        data = data['blocks']
    rows = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                rows.append((str(item['name']), float(item['x0']), float(item['y0']),
                             float(item['x1']), float(item['y1'])))
            else:
                name, corners = item[0], item[1]
                rows.append((str(name), *[float(v) for v in corners]))
    elif isinstance(data, dict):
        rows = [(str(name), *[float(v) for v in corners])
                for name, corners in data.items()]
    else:
        for line in text.splitlines():
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            parts = line.replace(',', ' ').split()
            if len(parts) != 5:
                raise ValueError(f'bad --blocks line: {line!r}')
            rows.append((parts[0], *[float(v) for v in parts[1:]]))
    if not rows:
        raise ValueError(f'no blocks in {path}')
    return [(name, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
            for name, x0, y0, x1, y1 in rows]


def _clusters(values):
    vals = sorted(set(round(v, 4) for v in values))
    groups, cur = [], [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] >= BLOCK_GAP:
            groups.append(cur)
            cur = []
        cur.append(v)
    groups.append(cur)
    return groups


def infer_blocks(sheet):
    """Cross-product of x/y symbol clusters, padded by half the split gap."""
    syms = symbol_positions(sheet)
    if not syms:
        return []
    xs, ys = _clusters(v[0] for v in syms.values()), _clusters(v[1] for v in syms.values())
    pad = BLOCK_GAP / 2
    blocks = []
    for i, xg in enumerate(xs, 1):
        for j, yg in enumerate(ys, 1):
            inside = [(x, y) for x, y in syms.values() if x in xg and y in yg]
            if inside:
                blocks.append((f'I{i}.{j}', min(p[0] for p in inside) - pad,
                               min(p[1] for p in inside) - pad,
                               max(p[0] for p in inside) + pad,
                               max(p[1] for p in inside) + pad))
    return blocks


def block_of(pos, blocks):
    for name, x0, y0, x1, y1 in blocks:
        if x0 <= pos[0] <= x1 and y0 <= pos[1] <= y1:
            return name
    return None


def parse_hubs(spec):
    """Hub refs and net names; short net names match hierarchical prefixes."""
    names = [s.strip() for s in (spec or '').split(',') if s.strip()]
    return dict(refs={s.upper() for s in names},
                nets=set(names),
                short={s.rsplit('/', 1)[-1] for s in names})


def hub_blocks(local_syms, blocks, hubs):
    """Blocks holding declared hub refs; a shared hub serves its whole block."""
    return {block_of(pos, blocks) for ref, pos in local_syms.items()
            if ref.upper() in hubs['refs']} - {None}


def classify(m, local_syms, blocks, hubs, shared=None):
    """In-block / cross-block, hub INFO and W6 flags for one measured net."""
    touched, hub = set(), False
    shared = shared if shared is not None else hub_blocks(local_syms, blocks, hubs)
    for ref, _ in m['nodes']:
        pos = local_syms.get(ref)
        if pos is None:  # off-sheet pins are not part of this block layout
            continue
        block = block_of(pos, blocks) or '?'
        touched.add(block)
        if ref.upper() in hubs['refs'] or block in shared:
            hub = True
    short = m['name'].rsplit('/', 1)[-1]
    if m['name'] in hubs['nets'] or short in hubs['short']:
        hub = True
    klass = 'unscored' if not touched else ('in-block' if len(touched) == 1
                                            else 'cross-block')
    return dict(klass=klass, blocks=tuple(sorted(touched)), hub=hub,
                hop=(klass == 'in-block' and (m['w'] > HOP_MAX or m['h'] > HOP_MAX)))


# --- geometry -------------------------------------------------------------

def library_unit_pins(root):
    """lib_id -> {unit number -> {pin number -> (x, y, name)}} from (lib_symbols).

    KiCad names sub-symbols "<part>_<unit>_<body>", so unit 3 of the dual
    ADA4940-2 is the "_3_1" child. Unit 0 (if present) is common to all units.
    """
    libs = K.child(root, 'lib_symbols')
    table = {}
    for sym in K.children(libs or [], 'symbol'):
        units = defaultdict(dict)
        for sub in K.children(sym, 'symbol'):
            m = re.search(r'_(\d+)_(\d+)$', str(sub[1]))
            node = K.child(sub, 'unit')
            unit = int(m.group(1)) if m else (int(node[1]) if node else 0)
            for pin in K.children(sub, 'pin'):
                num, at = K.child(pin, 'number'), K.child(pin, 'at')
                if num is None or at is None:
                    continue
                nm = K.child(pin, 'name')
                units[unit][str(num[1])] = (
                    float(at[1]), float(at[2]), str(nm[1]) if nm else '')
        table[str(sym[1])] = units
    return table


def pin_map(path):
    """(ref, pin) -> (pin name, x, y, unit), one entry per physical pin.

    The helper's instances() emits every pin of every unit for every unit
    block, which double-counts U105/U108. Here each sheet symbol block is
    restricted to (a) its declared (unit N) and (b) the pin numbers actually
    listed on that block; the final dict also de-duplicates by (ref, pin).
    """
    root = K.parse(Path(path).read_text(encoding='utf-8'))
    lib = library_unit_pins(root)
    out = {}
    for sym in K.children(root, 'symbol'):
        libid = K.child(sym, 'lib_id')
        if libid is None:
            continue
        ref = next((p[2] for p in K.children(sym, 'property')
                    if p[1] == 'Reference'), None)
        at = K.child(sym, 'at')
        if ref is None or at is None:
            continue
        mir = K.child(sym, 'mirror')
        x, y = float(at[1]), float(at[2])
        rot = int(float(at[3])) if len(at) > 3 else 0
        mirror = mir[1] if mir else None
        unode = K.child(sym, 'unit')
        unit = int(unode[1]) if unode else 1
        units = lib.get(str(libid[1]), {})
        rel = dict(units.get(0, {}))
        rel.update(units.get(unit, {}))
        declared = [str(p[1]) for p in K.children(sym, 'pin')]
        for num in (declared or sorted(rel)):
            if num not in rel:
                continue
            px, py, pname = rel[num]
            qx, qy = K.rotate(px, py, rot, mirror)
            key = (str(ref), num)
            if key not in out:  # de-dup: first (the instantiating unit) wins
                out[key] = (pname, round(x + qx, 4), round(y - qy, 4), unit)
    return out


def measure(name, nodes, coords, sheets, power_values):
    """One net -> dict with span, pin count, corner pins and sheet paths."""
    pts = []
    for ref, num in nodes:
        hit = coords.get((ref, num))
        if hit:
            pts.append((f'{ref}.{num}', hit[1], hit[2]))
    w = round(max(p[1] for p in pts) - min(p[1] for p in pts), 2) if pts else 0.0
    h = round(max(p[2] for p in pts) - min(p[2] for p in pts), 2) if pts else 0.0
    xs = sorted(pts, key=lambda p: p[1])
    ys = sorted(pts, key=lambda p: p[2])
    pair = [xs[0][0], xs[-1][0]] if pts else []
    for cand in ((ys[0][0], ys[-1][0]) if pts else ()):
        if len(pair) >= 3:
            break
        if cand not in pair:
            pair.append(cand)
    pair = list(dict.fromkeys(pair))
    net_sheets = sorted({sheets.get(ref, '?') for ref, _ in nodes})
    return dict(name=name, w=w, h=h, s=round(w + h, 2),
                pins=len(nodes), resolved=len(pts), furthest=pair,
                nodes=tuple(sorted(nodes)), sheets=net_sheets,
                cross_sheet=len(net_sheets) > 1,
                rail=is_rail(name, power_values))


# --- netlist ---------------------------------------------------------------

def load_netlist(path):
    """(nets, comps) from a kicadxml file; comps carry sheetpath metadata."""
    root = ET.parse(path).getroot()
    nets = {}
    for net in root.iter('net'):
        nets[str(net.get('name'))] = [
            (str(n.get('ref')), str(n.get('pin')))
            for n in net.iter('node')]
    comps = {}
    for comp in root.iter('comp'):
        sp = comp.find('sheetpath')
        props = {p.get('name'): p.get('value') for p in comp.iter('property')}
        comps[str(comp.get('ref'))] = dict(
            sheetpath=(sp.get('names') if sp is not None else '') or '/',
            sheetfile=props.get('Sheetfile') or '',
            value=comp.findtext('value') or '')
    return nets, comps


def auto_netlist(sheet):
    """Export the project netlist to a temp file (never touches the sheet)."""
    sheet = Path(sheet).resolve()
    root = next((p for p in [sheet.parent, *sheet.parent.parents]
                 if (p / 'brd-01.kicad_sch').exists()), sheet)
    top = root / 'brd-01.kicad_sch' if (root / 'brd-01.kicad_sch').exists() else sheet
    out = Path(tempfile.gettempdir()) / 'opencode' / 'span-report' / f'{top.stem}.xml'
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml',
                    '-o', str(out), str(top)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


def power_values_for(sheet, netlist, comps):
    """Values of the power: symbols drawn on the sheets named by the netlist."""
    base = Path(sheet).resolve().parent
    files = set()
    for info in comps.values():
        if info['sheetfile']:
            candidate = base / info['sheetfile']
            if candidate.exists():
                files.add(candidate)
    files.add(Path(sheet).resolve())
    values = set()
    for f in sorted(files):
        values.update(POWER_LIB.findall(f.read_text(encoding='utf-8', errors='replace')))
    _ = netlist  # kept for callers that also want net-name power hints
    return values


def is_rail(name, power_values):
    short = name.rsplit('/', 1)[-1]
    return (short == 'GND' or short in power_values
            or bool(SUPPLY_NAME.match(short)))


def norm_path(path):
    return (path or '').strip('/')


def on_sheet(path, wanted):
    path, wanted = norm_path(path), norm_path(wanted)
    return path == wanted or wanted in path.split('/')


# --- reports ---------------------------------------------------------------

def load_sheet(sheet, netlist_path=None):
    sheet = Path(sheet).resolve()
    netlist_path = Path(netlist_path).resolve() if netlist_path else auto_netlist(sheet)
    nets, comps = load_netlist(netlist_path)
    files = {}
    for info in comps.values():
        if info['sheetfile']:
            candidate = sheet.parent / info['sheetfile']
            if candidate.exists():
                files[candidate] = None
    files[sheet] = None
    coords = {}
    for f in files:
        for key, val in pin_map(f).items():
            coords.setdefault(key, val)
    sheets = {ref: norm_path(info['sheetpath']) for ref, info in comps.items()}
    pvals = power_values_for(sheet, netlist_path, comps)
    return nets, coords, sheets, pvals, netlist_path


def report(sheet, netlist_path, wanted, top, min_span, include_rails,
           blocks=None, hubs=None):
    nets, coords, sheets, pvals, nl = load_sheet(sheet, netlist_path)
    if blocks is None:
        blocks = infer_blocks(sheet)
        blocks_source = f'inferred from symbol positions on {Path(sheet).name} (gap >= {BLOCK_GAP} mm)'
    else:
        blocks_source = f'declared ({len(blocks)} blocks)'
    hubs = hubs or parse_hubs(None)
    local_syms = symbol_positions(sheet)
    shared = hub_blocks(local_syms, blocks, hubs)
    rows = []
    rails = 0
    hidden_sheet = 0
    for name, nodes in nets.items():
        m = measure(name, nodes, coords, sheets, pvals)
        if wanted and not any(on_sheet(sheets.get(ref, ''), wanted)
                              for ref, _ in nodes):
            hidden_sheet += 1
            continue
        if m['rail']:
            rails += 1
            if not include_rails:
                continue
        if min_span is not None and m['s'] + EPS < min_span:
            continue
        m.update(classify(m, local_syms, blocks, hubs, shared))
        rows.append(m)
    rows.sort(key=lambda m: (-m['s'], m['name']))
    return dict(mode='report', sheet=str(sheet), netlist=str(nl),
                sheet_filter=wanted, rows=rows, rails=rails,
                hidden_sheet=hidden_sheet, top=top, blocks=blocks,
                blocks_source=blocks_source, hub_blocks=sorted(shared),
                in_block=[m for m in rows if m['klass'] == 'in-block'],
                cross_block=[m for m in rows if m['klass'] == 'cross-block'],
                hops=[m for m in rows if m['hop']])


def _pair(names):
    return ', '.join(names)


def show_report(res):
    label = res['sheet_filter'] or Path(res['sheet']).stem
    note = (f" ({res['rails']} rail{'s' if res['rails'] != 1 else ''} excluded;"
            f" --include-rails to show)") if res['rails'] else ''
    rows = res['rows']
    print(f"# {label}: {len(rows)} nets{note}")
    print(_blocks_note(res))
    if res['hidden_sheet']:
        print(f"# {res['hidden_sheet']} nets had no pins on this sheet")
    missing = sum(m['pins'] - m['resolved'] for m in rows)
    if missing:
        print(f"# WARNING: {missing} netlist pins had no coordinate on any sheet")
    print(f"# W6: in-block net with w or h > {HOP_MAX:.1f} mm is flagged W6-HOP; "
          f"cross-block nets are not flagged")
    print(f"# HUB: cross-block net touching a declared hub or its block "
          f"({', '.join(res['hub_blocks']) or 'none'}) is INFO, not a warning")
    top = res['top']
    for title, group in (('IN-BLOCK', res['in_block']), ('CROSS-BLOCK', res['cross_block'])):
        shown = group[:top] if top else group
        print(f"\n== {title}: {len(group)} nets, S = {sum(m['s'] for m in group):.2f} mm ==")
        if title == 'IN-BLOCK':
            print(f"{'net':32s} {'w x h mm':>18s} {'sum mm':>8s} {'pins':>5s} "
                  f"{'block':8s} note")
            print(f"# W6-HOP count: {len(res['hops'])}")
        else:
            print(f"{'net':32s} {'w x h mm':>18s} {'sum mm':>8s} {'pins':>5s} "
                  f"{'blocks touched':22s} note")
        for m in shown:
            if title == 'IN-BLOCK':
                mark = 'W6-HOP' if m['hop'] else ''
                print(f"{m['name'][:32]:32s} "
                      f"{m['w']:8.2f} x {m['h']:8.2f} {m['s']:8.2f} {m['pins']:5d} "
                      f"{', '.join(m['blocks'])[:8]:8s} {mark}")
            else:
                mark = 'INFO (shared-hub cross-block)' if m['hub'] else ''
                print(f"{m['name'][:32]:32s} "
                      f"{m['w']:8.2f} x {m['h']:8.2f} {m['s']:8.2f} {m['pins']:5d} "
                      f"{', '.join(m['blocks'])[:22]:22s} {mark}")
        if top and len(shown) < len(group):
            print(f"# showing top {len(shown)} of {len(group)} by S")
    unscored = len(rows) - len(res['in_block']) - len(res['cross_block'])
    if unscored:
        print(f"\n# {unscored} nets had no pins on this sheet (unscored)")
    print(f"\nTOTAL S in-block {sum(m['s'] for m in res['in_block']):.2f} mm "
          f"({len(res['in_block'])} nets); cross-block "
          f"{sum(m['s'] for m in res['cross_block']):.2f} mm "
          f"({len(res['cross_block'])} nets)")


def compare(before, after, nl_before, nl_after, wanted, top, min_span,
            include_rails, tolerance, blocks=None, hubs=None):
    a = report(before, nl_before, wanted, None, None, include_rails, blocks, hubs)
    b = report(after, nl_after, wanted, None, None, include_rails, blocks, hubs)
    amap = {m['name']: m for m in a['rows']}
    bmap = {m['name']: m for m in b['rows']}
    used = set()
    pairs = []
    for name, m in amap.items():
        if name in bmap and name not in used:
            pairs.append((name, name, m, bmap[name], False))
            used.add(name)
    # KiCad renames a net when its label is removed; pair by pin membership,
    # as kicad_netlist_compare.py does, so the trade is still measured.
    by_pins = defaultdict(list)
    for name, m in bmap.items():
        if name not in used:
            by_pins[m['nodes']].append(name)
    for name, m in amap.items():
        if name in used:
            continue
        key = m['nodes']
        if by_pins.get(key):
            other = by_pins[key].pop(0)
            pairs.append((name, other, m, bmap[other], True))
            used.add(other)
    rows = []
    for old, new, m, n, renamed in pairs:
        delta = round(n['s'] - m['s'], 2)
        status = ('worsened' if delta > tolerance + EPS else
                  'improved' if delta < -tolerance - EPS else 'unchanged')
        moved = m['klass'] != n['klass'] or m['blocks'] != n['blocks']
        gate = (n['klass'] == 'in-block' and status == 'worsened') or (
            n['hop'] and not (m['klass'] == 'in-block' and m['hop']))
        rows.append(dict(name=old, after_name=new, renamed=renamed, before=m,
                         after=n, delta=delta, status=status, moved=moved,
                         gate=gate, klass=n['klass'], hub=n['hub'], hop=n['hop']))
    rows.sort(key=lambda r: (0 if r['gate'] else 1 if r['status'] == 'worsened'
                             else 2 if r['status'] == 'improved' else 3,
                             -abs(r['delta']), r['name']))
    regs = [r for r in rows if r['status'] == 'worsened']
    shown = [r for r in rows if r['gate'] or r['status'] == 'worsened'
             or r['moved'] or min_span is None
             or abs(r['delta']) + EPS >= min_span]
    if top:
        must = {id(r) for r in shown
                if r['gate'] or r['status'] == 'worsened' or r['moved']}
        rest = [r for r in shown if id(r) not in must]
        keep = must | {id(r) for r in rest[:max(0, top - len(must))]}
        shown = [r for r in rows if id(r) in keep]
    moved = [r for r in rows if r['moved']]
    summary = dict(total_before=round(sum(r['before']['s'] for r in rows), 2),
                   total_after=round(sum(r['after']['s'] for r in rows), 2),
                   improved=sum(r['status'] == 'improved' for r in rows),
                   unchanged=sum(r['status'] == 'unchanged' for r in rows),
                   worsened=len(regs),
                   inblock_regressions=sum(r['klass'] == 'in-block'
                                           and r['status'] == 'worsened'
                                           for r in rows),
                   new_hops=sum(bool(r['gate']) and not (
                       r['klass'] == 'in-block' and r['status'] == 'worsened')
                       for r in rows),
                   moved_blocks=len(moved),
                   only_before=len(amap) - len(pairs),
                   only_after=len(bmap) - len(pairs),
                   rails=a['rails'])
    return dict(mode='compare', before=str(before), after=str(after),
                netlist_before=str(a['netlist']), netlist_after=str(b['netlist']),
                rows=rows, shown=shown, moved=moved, summary=summary,
                tolerance=tolerance, blocks=a['blocks'],
                blocks_source=a['blocks_source'], hub_blocks=a['hub_blocks'])


def _blocks_note(res):
    names = [b[0] for b in res['blocks']]
    shown = ', '.join(names[:8]) + (f' ... +{len(names) - 8} more' if len(names) > 8 else '')
    return f"# blocks: {res['blocks_source']}" + (f" -> {shown}" if shown else '')


def _compare_line(r):
    b, a = r['before'], r['after']
    name = r['name'] + (f" -> {r['after_name']} (renamed)" if r['renamed'] else '')
    if a['hop']:
        note = 'W6-HOP'
    elif a['klass'] == 'cross-block' and a['hub']:
        note = 'INFO (shared-hub cross-block)'
    else:
        note = ''
    return (f"{name[:56]:56s} "
            f"{b['w']:8.2f} x {b['h']:8.2f} {a['w']:8.2f} x {a['h']:8.2f} "
            f"{r['delta']:+9.2f} {r['status']:10s} "
            f"{', '.join(a['blocks'])[:18]:18s} {note}")


def show_compare(res):
    s = res['summary']
    print(f"# span compare: {res['before']} -> {res['after']}")
    print(f"# {s['rails']} rails excluded; {len(res['rows'])} nets in both; "
          f"tolerance {res['tolerance']:.2f} mm")
    print(_blocks_note(res))
    missing = sum(r['before']['pins'] - r['before']['resolved']
                  + r['after']['pins'] - r['after']['resolved'] for r in res['rows'])
    if missing:
        print(f"# WARNING: {missing} netlist pins had no coordinate on any sheet")
    print("# GATE: --fail-on-regression fails ONLY on an in-block span getting worse "
          "or a new in-block hop > 25.4 mm; cross-block growth never fails")
    print(f"# HUB: cross-block net touching a declared hub or its block "
          f"({', '.join(res['hub_blocks']) or 'none'}) is INFO, not a warning")
    head = (f"{'net':56s} {'before':>18s} {'after':>18s} {'dS':>9s} "
            f"{'status':10s} {'blocks':18s} note")
    for title, klass in (('IN-BLOCK', 'in-block'), ('CROSS-BLOCK', 'cross-block')):
        group = [r for r in res['shown'] if r['klass'] == klass]
        print(f"\n== {title}: {len(group)} shown, "
              f"S before {sum(r['before']['s'] for r in group):.2f} -> after "
              f"{sum(r['after']['s'] for r in group):.2f} mm ==")
        print(head)
        for r in group:
            print(_compare_line(r))
    print(f"\n== MOVED BLOCK: {s['moved_blocks']} ==")
    for r in res['moved']:
        print(f"MOVED BLOCK {r['name']}: {r['before']['klass']} "
              f"[{', '.join(r['before']['blocks']) or '-'}] -> {r['after']['klass']} "
              f"[{', '.join(r['after']['blocks']) or '-'}] "
              f"({r['delta']:+9.2f} mm)")
    print(f"\nTOTAL S before {s['total_before']:.2f} -> after {s['total_after']:.2f} mm; "
          f"improved {s['improved']}, unchanged {s['unchanged']}, "
          f"worsened {s['worsened']}")
    print(f"in-block regressions == {s['inblock_regressions']}; new in-block hops == "
          f"{s['new_hops']}; cross-block regressions (not gated) == "
          f"{s['worsened'] - s['inblock_regressions']}; moved block == {s['moved_blocks']}")
    print(f"only before: {s['only_before']}, only after: {s['only_after']} (not scored)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sheet', help='before sheet, or the only sheet to report')
    ap.add_argument('after', nargs='?', help='after sheet (with --compare)')
    ap.add_argument('--compare', action='store_true')
    ap.add_argument('--netlist')
    ap.add_argument('--netlist-before')
    ap.add_argument('--netlist-after')
    ap.add_argument('--sheet', dest='sheet_filter', help='e.g. /receiver/')
    ap.add_argument('--top', type=int)
    ap.add_argument('--min-span', type=float)
    ap.add_argument('--include-rails', action='store_true')
    ap.add_argument('--blocks', help='block rectangles: JSON or "name x0,y0,x1,y1" CSV; '
                    'omitted = infer from symbol positions (gap >= 12.7 mm)')
    ap.add_argument('--hubs', help='comma-separated net names and/or ref designators '
                    'that are shared hubs (e.g. U101,ADC_VCM); a cross-block net '
                    'touching the hub pin, its block, or the named net is INFO')
    ap.add_argument('--fail-on-regression', action='store_true',
                    help='fail ONLY on an in-block span getting worse or a new '
                    'in-block hop > 25.4 mm; cross-block growth never fails')
    ap.add_argument('--tolerance', type=float, default=0.0)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)

    if args.compare and not args.after:
        ap.error('--compare needs two sheets: BEFORE.kicad_sch AFTER.kicad_sch')
    try:
        blocks = load_blocks(args.blocks) if args.blocks else None
        hubs = parse_hubs(args.hubs)
        if args.compare:
            res = compare(args.sheet, args.after, args.netlist_before,
                          args.netlist_after, args.sheet_filter, args.top,
                          args.min_span, args.include_rails, args.tolerance,
                          blocks, hubs)
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                show_compare(res)
            return 1 if (args.fail_on_regression
                         and (res['summary']['inblock_regressions']
                              or res['summary']['new_hops'])) else 0
        res = report(args.sheet, args.netlist, args.sheet_filter, args.top,
                     args.min_span, args.include_rails, blocks, hubs)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            show_report(res)
        return 0
    except (OSError, ET.ParseError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"kicad_span_report: {exc}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
