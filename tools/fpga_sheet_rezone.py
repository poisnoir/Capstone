#!/usr/bin/env python3
"""Re-layout and rewire the BRD-01 FPGA sheet (KiCad 10 S-expressions).

    python3 tools/fpga_sheet_rezone.py [--sheet PATH] [--zones A,B,C,D,E]

Part targets are grid-snapped design decisions from the rezone brief.  Every
wire end is read from the sheet's embedded ``(lib_symbols …)`` pin table via
``kicad_span_report.pin_map`` (unit-aware) -- no pin coordinate is hard-coded.

Re-runnable: moves are absolute; deletions are by content/geometry; every new
object carries a deterministic UUID derived from its own geometry, so a second
run adds nothing.  Unrelated formatting, ``lib_symbols``, component properties,
``instances`` and ``sheet_instances`` are untouched.
"""
from __future__ import annotations

import argparse
import re
import sys
import uuid as _uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kicad_sch_helper as K                 # noqa: E402
import kicad_span_report as S                # noqa: E402

DEFAULT_SHEET = 'hardware/brd-01/kicad/fpga.kicad_sch'
GRID = 1.27
NS = _uuid.UUID('2f4d1a60-3b9c-4e51-9d2f-7a6c1e8b0d34')


def g(v: float) -> float:
    return round(round(v / GRID) * GRID, 4)


def fmt(v: float) -> str:
    return K.fmt(v)


def duuid(*parts: object) -> str:
    return str(_uuid.uuid5(NS, '|'.join(str(p) for p in parts)))


def pins_from_root(root):
    """Unit-aware (ref,pin) -> (name,x,y,unit); same rule as the span tool,
    but computed from an in-memory parse so unsaved moves are visible.
    """
    lib = S.library_unit_pins(root)
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
        un = K.child(sym, 'unit')
        unit = int(un[1]) if un else 1
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
            if key not in out:
                out[key] = (pname, round(x + qx, 4), round(y - qy, 4), unit)
    return out


class Rezone:
    def __init__(self, path: str):
        self.path = Path(path)
        self.text = self.path.read_text(encoding='utf-8')
        self.refresh()

    def refresh(self):
        self.root = K.parse(self.text)
        self.pins = pins_from_root(self.root)

    def save(self):
        self.path.write_text(self.text, encoding='utf-8')

    def pin(self, ref: str, num: str) -> tuple[float, float]:
        if (ref, str(num)) not in self.pins:
            raise KeyError(f'pin not found: {ref}.{num}')
        _n, x, y, _u = self.pins[(ref, str(num))]
        return (round(x, 4), round(y, 4))

    def pins_of(self, ref: str) -> set[tuple[float, float]]:
        return {(round(v[1], 4), round(v[2], 4))
                for (r, _n), v in self.pins.items() if r == ref}

    # ---- raw block manipulation --------------------------------------
    def del_span(self, start: int, end: int):
        self.text = self.text[:start] + self.text[end:]

    def del_uuid(self, uid: str) -> bool:
        if f'(uuid "{uid}")' not in self.text:
            return False
        start, stop = K.block_span(self.text, uid)
        while start > 0 and self.text[start - 1] in ' \t':
            start -= 1
        if start > 0 and self.text[start - 1] == '\n':
            start -= 1
        self.del_span(start, stop)
        return True

    def del_point(self, kind: str, point: tuple[float, float]) -> int:
        hits = []
        for s, e, _ in K.top_blocks(self.text, kind):
            m = re.search(r'\(at ([\d.-]+) ([\d.-]+)', self.text[s:e])
            if m and (abs(float(m.group(1)) - point[0]) < 1e-6
                      and abs(float(m.group(2)) - point[1]) < 1e-6):
                hits.append((s, e))
        for s, e in sorted(hits, reverse=True):
            self.del_span(s, e)
        return len(hits)

    def del_label_text(self, kind: str, text: str) -> int:
        hits = [(s, e) for s, e, _ in K.top_blocks(self.text, kind)
                if self.text[s:e].startswith(f'({kind} "{text}"')]
        for s, e in sorted(hits, reverse=True):
            self.del_span(s, e)
        return len(hits)

    def del_wire(self, a, b) -> int:
        """Delete the wire whose two ends are exactly a and b (either order)."""
        a = (g(a[0]), g(a[1])); b = (g(b[0]), g(b[1]))
        hits = []
        for s, e, _ in K.top_blocks(self.text, 'wire'):
            xy = re.findall(r'\(xy ([\d.-]+) ([\d.-]+)\)', self.text[s:e])
            if len(xy) != 2:
                continue
            p, q = (float(xy[0][0]), float(xy[0][1])), (float(xy[1][0]), float(xy[1][1]))
            if (p, q) in ((a, b), (b, a)):
                hits.append((s, e))
        for s, e in sorted(hits, reverse=True):
            self.del_span(s, e)
        return len(hits)

    def del_label_at(self, kind: str, text: str, at) -> int:
        at = (g(at[0]), g(at[1]))
        hits = []
        for s, e, _ in K.top_blocks(self.text, kind):
            blk = self.text[s:e]
            if not blk.startswith(f'({kind} "{text}"'):
                continue
            m = re.search(r'\(at ([\d.-]+) ([\d.-]+)', blk)
            if m and (abs(float(m.group(1)) - at[0]) < 1e-6
                      and abs(float(m.group(2)) - at[1]) < 1e-6):
                hits.append((s, e))
        for s, e in sorted(hits, reverse=True):
            self.del_span(s, e)
        return len(hits)

    def insert(self, block: str):
        idx = self.text.rstrip().rfind(')')
        self.text = self.text[:idx] + block + self.text[idx:]

    # ---- creators -----------------------------------------------------
    def wire(self, a, b, tag=''):
        a = (g(a[0]), g(a[1])); b = (g(b[0]), g(b[1]))
        if a == b:
            return
        assert abs(a[0] - b[0]) < 1e-6 or abs(a[1] - b[1]) < 1e-6, (a, b)
        uid = duuid('wire', a, b, tag)
        if f'(uuid "{uid}")' in self.text:
            return
        self.insert(
            f'\t(wire\n\t\t(pts\n\t\t\t(xy {fmt(a[0])} {fmt(a[1])}) '
            f'(xy {fmt(b[0])} {fmt(b[1])})\n\t\t)\n'
            f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n'
            f'\t\t(uuid "{uid}")\n\t)\n')

    def junction(self, at):
        at = (g(at[0]), g(at[1]))
        uid = duuid('junction', at)
        if f'(uuid "{uid}")' in self.text:
            return
        self.insert(
            f'\t(junction\n\t\t(at {fmt(at[0])} {fmt(at[1])})\n'
            f'\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n'
            f'\t\t(uuid "{uid}")\n\t)\n')

    def nc(self, at):
        at = (g(at[0]), g(at[1]))
        uid = duuid('no_connect', at)
        if f'(uuid "{uid}")' in self.text:
            return
        self.insert(f'\t(no_connect\n\t\t(at {fmt(at[0])} {fmt(at[1])})\n'
                    f'\t\t(uuid "{uid}")\n\t)\n')

    def label(self, kind: str, text: str, at, angle: int = 0, shape: str = 'passive'):
        at = (g(at[0]), g(at[1]))
        uid = duuid(kind, text, at, angle)
        if f'(uuid "{uid}")' in self.text:
            return
        just = 'right' if angle in (180, 270) else 'left'
        head = f'\t({kind} "{text}"\n'
        if kind != 'label':
            head += f'\t\t(shape {shape})\n'
        block = (head + f'\t\t(at {fmt(at[0])} {fmt(at[1])} {angle})\n'
                 '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t)\n'
                 f'\t\t\t(justify {just})\n\t\t)\n'
                 f'\t\t(uuid "{uid}")\n')
        if kind == 'global_label':
            block += (f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n'
                      f'\t\t\t(at {fmt(at[0])} {fmt(at[1])} 0)\n'
                      '\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
                      '\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n'
                      '\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n'
                      '\t\t\t)\n\t\t)\n')
        self.insert(block + '\t)\n')

    def glabel(self, text, at, angle=0):
        self.label('global_label', text, at, angle)

    def llabel(self, text, at, angle=0):
        self.label('label', text, at, angle)

    # ---- cleanup ------------------------------------------------------
    def normalize_text_sizes(self):
        """Undo the round-1 undersized text; the sheet's normal size is 1 mm."""
        self.text = re.sub(r'\(size 0\.8 0\.8\)', '(size 1 1)', self.text)

    def prune_dangling_labels(self):
        """Drop labels left behind by deleted wires (they would be ERC errors).

        A label is valid when its (at …) is at a pin end or on a wire segment;
        this is the same test the helper's `audit` uses.
        """
        root = K.parse(self.text)
        wires = K.wires(root)
        pinpts = {(round(v[1], 4), round(v[2], 4)) for v in self.pins.values()}
        for kind in ('label', 'global_label', 'hierarchical_label'):
            for lab in list(K.labels(root, kind)):
                p = lab['p']
                if p in pinpts:
                    continue
                if any(K.on_wire(p, w['a'], w['b']) for w in wires):
                    continue
                self.del_uuid(lab['uuid'])
        self.refresh()

    # ---- symbol placement --------------------------------------------
    def sym_uuid(self, ref: str) -> str:
        for sym in K.children(self.root, 'symbol'):
            r = next((p[2] for p in K.children(sym, 'property')
                      if p[1] == 'Reference'), None)
            if r == ref:
                return K.child(sym, 'uuid')[1]
        raise KeyError(f'symbol not found: {ref}')

    def move(self, ref: str, to, rot: int | None = None, mirror: str | None = None):
        to = (g(to[0]), g(to[1]))
        uid = self.sym_uuid(ref)
        pos = self.text.find(f'(uuid "{uid}")')
        head = self.text.rfind('\n\t(symbol', 0, pos)
        at = self.text.find('(at ', head)
        end = self.text.find(')', at)
        fields = self.text[at + 4:end].split()
        dx, dy = to[0] - float(fields[0]), to[1] - float(fields[1])
        r = str(rot) if rot is not None else (fields[2] if len(fields) > 2 else '0')
        self.text = self.text[:at] + f'(at {fmt(to[0])} {fmt(to[1])} {r}' + self.text[end:]
        # Property text coordinates are absolute: translate them with the part.
        bs, be = K.block_span(self.text, uid)
        blk = self.text[bs:be]
        prop = re.compile(r'(\(property "[^"]*" "[^"]*"\s*\(at )([-\d.]+) ([-\d.]+)([^)]*)\)')
        def flat(m):
            # Property text is always horizontal; rotating it with the body is
            # the source of every unreadable refdes/value on this sheet.
            return (m.group(1) + fmt(float(m.group(2)) + dx) + ' '
                    + fmt(float(m.group(3)) + dy) + ' 0)')
        blk = prop.sub(flat, blk)
        self.text = self.text[:bs] + blk + self.text[be:]
        if mirror is not None:
            blk_start, blk_end = K.block_span(self.text, uid)
            blk = self.text[blk_start:blk_end]
            if re.search(r'\(mirror [xy]\)', blk):
                blk = re.sub(r'\(mirror [xy]\)', f'(mirror {mirror})', blk, count=1)
            elif mirror in ('x', 'y'):
                ins = blk.find('\n\t\t(at ')
                line = f'\n\t\t(mirror {mirror})'
                blk = blk[:ins + 1] + line + blk[ins + 1:]
            self.text = self.text[:blk_start] + blk + self.text[blk_end:]
        self.refresh()

    def label_at(self, kind: str, text: str, at, new_at, angle=None):
        """Move an existing label and/or change its angle, in place."""
        new_at = (g(new_at[0]), g(new_at[1]))
        for s, e, _ in K.top_blocks(self.text, kind):
            blk = self.text[s:e]
            if not blk.startswith(f'({kind} "{text}"'):
                continue
            m = re.search(r'\(at ([\d.-]+) ([\d.-]+)(?: ([\d.-]+))?\)', blk)
            if not m:
                continue
            p = (float(m.group(1)), float(m.group(2)))
            if abs(p[0] - at[0]) > 1e-6 or abs(p[1] - at[1]) > 1e-6:
                continue
            a = int(float(m.group(3))) if m.group(3) else 0
            if angle is not None:
                a = angle
            nb = blk[:m.start()] + f'(at {fmt(new_at[0])} {fmt(new_at[1])} {a})' + blk[m.end():]
            if angle is not None:
                nb = re.sub(r'\(justify (?:left|right)\)',
                            f'(justify {"right" if angle in (180, 270) else "left"})',
                            nb, count=1)
            self.text = self.text[:s] + nb + self.text[e:]
            self.refresh()
            return

    def prop_pos(self, ref: str, prop: str, to, angle: int = 0):
        """Place one symbol property (Reference/Value) at an absolute point."""
        to = (g(to[0]), g(to[1]))
        uid = self.sym_uuid(ref)
        bs, be = K.block_span(self.text, uid)
        blk = self.text[bs:be]
        # KiCad adds the symbol rotation to the property angle at draw time;
        # compensate so the requested angle is what actually renders.
        sm = re.search(r'\n\t\t\(at [\d.-]+ [\d.-]+ ([\d.-]+)\)', blk)
        rot = int(float(sm.group(1))) if sm else 0
        angle = (angle - rot) % 360
        pat = re.compile(r'(\(property "' + re.escape(prop)
                         + r'" "[^"]*"\s*\(at )([-\d.]+) ([-\d.]+)([^)]*)\)')
        found = False

        def sub(m):
            nonlocal found
            found = True
            tail = re.sub(r'\s[\d.-]+$', '', m.group(4))
            return (m.group(1) + fmt(to[0]) + ' ' + fmt(to[1]) + ' '
                    + str(angle) + tail + ')')

        blk = pat.sub(sub, blk, count=1)
        if not found:
            raise ValueError(f'{ref}.{prop} not found')
        self.text = self.text[:bs] + blk + self.text[be:]

    def textpos(self, snippet: str, to, angle: int = 0):
        to = (g(to[0]), g(to[1]))
        hits = [(s, e) for s, e, _ in K.top_blocks(self.text, 'text')
                if snippet in self.text[s:e]]
        if len(hits) != 1:
            raise ValueError(f'text {snippet!r}: {len(hits)} matches')
        s, e = hits[0]
        blk = re.sub(r'\(at [\d.-]+ [\d.-]+ [\d.-]+\)',
                     f'(at {fmt(to[0])} {fmt(to[1])} {angle})',
                     self.text[s:e], count=1)
        self.text = self.text[:s] + blk + self.text[e:]

    def set_rect(self, start, end):
        hits = K.top_blocks(self.text, 'rectangle')
        if len(hits) != 1:
            raise ValueError(f'{len(hits)} rectangles on sheet')
        s, e, _ = hits[0]
        blk = re.sub(r'\(start [\d.-]+ [\d.-]+\)',
                     f'(start {fmt(start[0])} {fmt(start[1])})', self.text[s:e], 1)
        blk = re.sub(r'\(end [\d.-]+ [\d.-]+\)',
                     f'(end {fmt(end[0])} {fmt(end[1])})', blk, 1)
        self.text = self.text[:s] + blk + self.text[e:]

    # ---- detach -------------------------------------------------------
    def detach(self, refs, extra_labels=(), extra_glabels=()):
        """Delete wires and their end-attached objects for a set of parts."""
        pts = set()
        for ref in refs:
            pts |= self.pins_of(ref)
        wuid = [w['uuid'] for w in K.wires(self.root)
                if w['a'] in pts or w['b'] in pts]
        ends = set()
        for w in K.wires(self.root):
            if w['uuid'] in wuid:
                ends |= {w['a'], w['b']}
        for uid in wuid:
            self.del_uuid(uid)
        targets = pts | ends
        for kind in ('label', 'global_label', 'hierarchical_label'):
            for lab in K.labels(self.root, kind):
                if lab['p'] in targets:
                    self.del_uuid(lab['uuid'])
        for kind in ('junction', 'no_connect'):
            for p in sorted(targets):
                self.del_point(kind, p)
        for text in extra_labels:
            self.del_label_text('label', text)
        for text, at in extra_glabels:
            self.del_label_at('global_label', text, at)
        self.refresh()


# ---------------------------------------------------------------------------
# Zone transforms
# ---------------------------------------------------------------------------
BANKS = {
    '+1V0_FPGA': ['C150', 'C151', 'C152', 'C153', 'C154', 'C155', 'C156', 'C170'],
    '+1V8_FPGA': ['C157', 'C158', 'C159', 'C160', 'C161', 'C171'],
    '+3.3V': ['C162', 'C163', 'C164', 'C165', 'C166', 'C167',
              'C168', 'C169', 'C172'],
}
BANK_ROWS = {'+1V0_FPGA': 215.90, '+1V8_FPGA': 248.92, '+3.3V': 281.94}
BANK_X0 = 139.70


def zone_d(rz: Rezone):
    """One clean parallel rail/GND ladder per decoupling bank."""
    refs = [r for caps in BANKS.values() for r in caps]
    rz.detach(refs)
    # restore the GND flags detached with the old cap wires (identity only)
    for y in (205.74, 215.90, 226.06, 236.22, 246.38, 256.54):
        rz.glabel('GND', (41.91, y), 0)
    for bank, caps in BANKS.items():
        row_y = BANK_ROWS[bank]
        rail_y, gnd_y = row_y - 10.16, row_y + 10.16
        xs = [BANK_X0 + i * 10.16 for i in range(len(caps))]
        for ref, cx in zip(caps, xs):
            rz.move(ref, (cx, row_y), rot=0)
        x0, x1 = xs[0], xs[-1]          # ends land on the outer cap stubs
        rz.wire((x0, rail_y), (x1, rail_y), bank + 'rail')
        rz.wire((x0, gnd_y), (x1, gnd_y), bank + 'gnd')
        for cx in xs:
            rz.wire((cx, rail_y), (cx, row_y - 3.81), bank + 'rs')
            rz.wire((cx, gnd_y), (cx, row_y + 3.81), bank + 'gs')
            rz.junction((cx, rail_y))
            rz.junction((cx, gnd_y))
        rz.glabel(bank, (x0, rail_y), 180)
        rz.glabel('GND', (x1, gnd_y), 0)
    rz.set_rect((25.40, 285.75), (127.00, 328.93))


def zone_a(rz: Rezone):
    """DAC SPI series resistors and the CS pull-up beside U4 unit 2."""
    rz.detach(['R145', 'R146', 'R147', 'R162'],
              extra_labels=('DAC_CS_SRC', 'DAC_SCLK_SRC', 'DAC_SDI_SRC'))
    # the old FPGA-pin-to-label stubs are no longer used
    for ball in ('L4', 'M2', 'M1'):
        px, py = rz.pin('U4', ball)
        rz.del_wire((px, py), (px - 5.08, py))
    # clear stale vertical jog wires from an earlier row assignment
    for w in list(K.wires(rz.root)):
        if abs(w['a'][0] - w['b'][0]) < 1e-6 and w['a'][0] in (20.32, 22.86, 24.13):
            rz.del_wire(w['a'], w['b'])
    # Vertical bodies at 5.08 mm pitch in the clear area above the DAC pins;
    # Reference left / Value right, orthogonal jogs back down to the balls.
    for ref, ball, net, row, jx in (('R147', 'L4', 'DAC_SDI', 49.53, 24.13),
                                    ('R145', 'M2', 'DAC_CS', 40.64, 22.86),
                                    ('R146', 'M1', 'DAC_SCLK', 63.50, 20.32)):
        px, py = rz.pin('U4', ball)          # FPGA pin end, from lib_symbols
        rz.move(ref, (19.05, row), rot=0)
        p1, p2 = rz.pin(ref, '1'), rz.pin(ref, '2')
        # p1 faces the FPGA (upper pin), p2 the net (lower pin)
        jog_y = p1[1]                       # above the body, never through it
        rz.wire((px, py), (jx, py), ref + 'in')
        if abs(jog_y - py) > 1e-6:
            rz.wire((jx, py), (jx, jog_y), ref + 'jog')
        rz.junction((jx, py))
        rz.junction((jx, jog_y))
        rz.wire((jx, jog_y), p1, ref + 'top')
        lab = (15.24, p2[1]) if ref != 'R147' else (8.89, p2[1])
        rz.wire(p2, lab, ref + 'labstub')
        rz.glabel(net, lab, 180 if ref in ('R145', 'R146') else 0)
        rz.prop_pos(ref, 'Reference', (15.24, row), 0)
        rz.prop_pos(ref, 'Value', (22.86, row), 0)
    # keep the pre-existing DAC_SDO flag on its own pin, off the new jog wire
    rz.label_at('global_label', 'DAC_SDO', (21.59, 57.15), (21.59, 57.15), 180)
    rz.label_at('global_label', 'PICO_RX', (21.59, 64.77), (21.59, 64.77), 0)
    rz.label_at('global_label', 'PICO_TX', (21.59, 67.31), (21.59, 67.31), 0)
    rz.move('R162', (15.24, 31.75), rot=0)
    p1, p2 = rz.pin('R162', '1'), rz.pin('R162', '2')
    rz.glabel('+3.3V', (p1[0], p1[1] - 3.81), 90)
    rz.wire(p1, (p1[0], p1[1] - 3.81), 'r162rail')
    rz.wire(p2, (20.32, p2[1]), 'r162cs')
    rz.glabel('DAC_CS', (20.32, p2[1]), 0)


def zone_b(rz: Rezone):
    """ADC pull-ups, 32.768 MHz oscillator and bypass beside U4 unit 1."""
    rz.detach(['R163', 'R164', 'R165', 'R166', 'Y1', 'C141'])
    rz.del_wire((440.69, 73.66), (440.69, 113.03))   # old clock dog-leg
    rz.del_wire((447.04, 115.57), (447.04, 96.52))
    for y in (81.28, 83.82, 86.36, 91.44, 93.98, 96.52, 99.06, 101.60, 116.84):
        rz.del_wire((290.83, y), (295.91, y))        # old FPGA-to-jog stubs
    for net, y in (('ADC_SDI', 83.82), ('ADC_SCLK', 91.44)):
        rz.del_label_at('global_label', net, (295.91, y))
        rz.del_label_at('global_label', net, (290.83, y))
        rz.del_label_at('global_label', net, (287.02, y))
        rz.del_wire((290.83, y), (287.02, y))          # stale stub
        anchor = (292.10, 88.90) if net == 'ADC_SCLK' else (290.83, y)
        if anchor != (290.83, y):
            rz.wire((290.83, y), (292.10, y), net + 'stub')
            rz.wire((292.10, y), anchor, net + 'drop')
        rz.glabel(net, anchor, 0)                   # flag on a wire/pin end
    # 5.08 mm pitch rows give Reference/Value room at the sheet's normal 1 mm text.
    rows = {'R164': 86.36, 'R163': 91.44, 'R166': 96.52, 'R165': 101.60}
    for ref, ball, net in (('R163', 'A14', 'ADC_RESET_N'),
                           ('R164', 'B12', 'ADC_CS'),
                           ('R165', 'B14', 'ADC_START_N'),
                           ('R166', 'C14', 'ADC_SYNC_IN')):
        px, py = rz.pin('U4', ball)
        rz.del_label_at('global_label', net, (295.91, py))   # superseded flag
        row = rows[ref]
        rz.del_label_at('global_label', net, (303.53, row))   # mid-wire flag
        cx = 317.50
        rz.move(ref, (cx, row), rot=270)
        p1, p2 = rz.pin(ref, '1'), rz.pin(ref, '2')
        knee = (300.99, row)
        rz.del_wire((295.91, py), (295.91, row))
        rz.wire((px, py), (300.99, py), ref + 'in')
        if abs(row - py) > 1e-6:
            rz.wire((300.99, py), knee, ref + 'jog')
        rz.wire(knee, p2, ref + 'out')
        rail_end = (p1[0] + 5.08, row)           # stub out of the resistor body
        rz.wire(p1, rail_end, ref + 'rail')
        rz.glabel('+3.3V', rail_end, 0)
        rz.glabel(net, p2, 180)                  # anchored at the wire/pin end
        rz.prop_pos(ref, 'Reference', (cx, row - 3.81))
        rz.prop_pos(ref, 'Value', (cx, row + 3.81))
    px, py = rz.pin('U4', 'D13')
    rz.del_label_at('global_label', 'CLOCK_32M768', (295.91, py))
    rz.move('Y1', (321.31, py - 2.54), rot=180)
    out = rz.pin('Y1', '3')
    rz.wire(out, (px, py), 'clk')
    rz.glabel('CLOCK_32M768', (px, py), 0)
    for pin_no, net in (('1', '+3.3V'), ('4', '+3.3V'), ('2', 'GND')):
        p = rz.pin('Y1', pin_no)
        end = (p[0] + 5.08, p[1])
        rz.wire(p, end, 'clkpwr' + pin_no)
        rz.glabel(net, end, 0)
    rz.move('C141', (321.31, py + 12.70), rot=0)
    rz.glabel('+3.3V', rz.pin('C141', '1'), 0)
    rz.glabel('GND', rz.pin('C141', '2'), 0)
    rz.textpos('Clock branch termination', (295.91, py + 24.13))


def zone_c(rz: Rezone):
    """QSPI flash, source termination, JTAG header and bring-up notes."""
    rz.detach(['U141', 'R790', 'R140', 'R148', 'R149', 'C140', 'J140'])
    rz.del_wire((419.10, 113.03), (440.69, 113.03))   # old CCLK dog-leg
    cclk = rz.pin('U4', 'E8')
    rz.move('R790', (431.80, cclk[1]), rot=90)   # pin 1 faces the FPGA
    rz.wire(rz.pin('R790', '1'), cclk, 'cclk')
    rz.move('U141', (445.77, cclk[1] + 1.27), rot=0)
    fy = cclk[1] + 1.27
    rz.prop_pos('U141', 'Reference', (445.77, fy - 8.89))
    rz.prop_pos('U141', 'Value', (445.77, fy + 6.35))
    rz.wire(rz.pin('R790', '2'), rz.pin('U141', '6'), 'flashclk')
    # QSPI nets are local labels on this sheet in the baseline netlist.
    for net, fpin, side in (('QSPI_CS', '1', -1), ('QSPI_D0', '5', 1),
                            ('QSPI_D1', '2', 1), ('QSPI_D2', '3', 1),
                            ('QSPI_D3', '7', 1)):
        p = rz.pin('U141', fpin)
        end = (p[0] + side * 5.08, p[1])   # stub clears the body and pin name
        rz.wire(p, end, 'flash' + net)
        rz.llabel(net, end, 0 if side > 0 else 180)
    for pin_no, net in (('8', '+3.3V'), ('4', 'GND')):
        p = rz.pin('U141', pin_no)
        end = (p[0] - 5.08, p[1])
        rz.wire(p, end, 'flashpwr' + pin_no)
        rz.glabel(net, end, 180)
    for ref, net, at in (('R140', 'QSPI_CS', (444.50, cclk[1] - 16.51)),
                         ('R148', 'QSPI_D2', (477.50, cclk[1] + 12.70)),
                         ('R149', 'QSPI_D3', (477.50, cclk[1] + 25.40)),
                         ('C140', None, (435.61, cclk[1] + 15.24))):
        rz.move(ref, at, rot=0)
        if net:
            ry = at[1]
            rp = rz.pin(ref, '1')
            rz.del_label_at('global_label', '+3.3V', rp)
            rail_end = (rp[0] - 5.08, rp[1])
            rz.wire(rp, rail_end, ref + 'rail')
            rz.glabel('+3.3V', rail_end, 180)           # stub, off the body
            rz.llabel(net, rz.pin(ref, '2'), 180)       # text left of the body
            rz.prop_pos(ref, 'Reference', (at[0], ry - 6.35))
            rz.prop_pos(ref, 'Value', (at[0], ry + 6.35))
        else:
            rz.glabel('+3.3V', rz.pin(ref, '1'), 0)
            rz.glabel('GND', rz.pin(ref, '2'), 0)
    # JTAG header level with the JTAG balls; labels keep the four nets straight.
    jy = g(rz.pin('U4', 'L7')[1] - 2.54)
    rz.move('J140', (518.16, jy), rot=0, mirror='y')
    for jp, ball, net in (('6', 'L7', 'JTAG_TCK'),
                          ('4', 'M7', 'JTAG_TMS'),
                          ('10', 'N7', 'JTAG_TDI'),
                          ('8', 'N8', 'JTAG_TDO')):
        p = rz.pin('J140', jp)
        end = (p[0] - 5.08, p[1])          # stub clears the pin name
        rz.wire(p, end, 'jtag' + net)
        rz.llabel(net, end, 180)
        rz.llabel(net, rz.pin('U4', ball), 0)
    for jp, net in [('2', '+3.3V')] + [(p, 'GND') for p in ('3', '5', '7', '9', '11')]:
        p = rz.pin('J140', jp)
        end = (p[0] + (-5.08 if p[0] < 518.16 else 5.08), p[1])
        rz.wire(p, end, 'jtagpwr' + jp)
        rz.glabel(net, end, 0)
    for jp in ('1', '12', '13', '14'):
        rz.nc(rz.pin('J140', jp))
    rz.textpos('Configuration bring-up', (444.50, cclk[1] - 24.13))
    rz.textpos('Place R790 at the FPGA', (480.06, cclk[1] + 38.10))


def zone_e(rz: Rezone):
    """USB-UART VBUS divider, bypass group and spaced DP/DM resistors."""
    rz.detach(['R158', 'R159', 'C143', 'C144', 'C145', 'R160', 'R161'])
    rz.del_wire((431.80, 298.45), (431.80, 307.34))   # old VBUS divider stub
    rz.del_wire((330.20, 292.10), (335.28, 292.10))   # old CBUS2 label stub
    cb2 = rz.pin('U142', '7')
    rz.del_label_at('label', 'VBUS_SENSE', cb2)       # superseded pin-side flag
    rz.del_label_at('label', 'VBUS_SENSE', (335.28, cb2[1]))
    tap = (342.90, cb2[1])
    rz.move('R158', (342.90, cb2[1] - 3.81), rot=0)
    rz.move('R159', (342.90, cb2[1] + 3.81), rot=0)
    rz.glabel('USB_VBUS', rz.pin('R158', '1'), 0)
    rz.wire(rz.pin('R158', '2'), tap, 'vbus-top')
    rz.wire(cb2, tap, 'vbus-tap')
    rz.wire(rz.pin('R159', '1'), tap, 'vbus-bot')
    rz.junction(tap)
    rz.glabel('GND', rz.pin('R159', '2'), 0)
    # Sense flag on a stub end, clear of both the junction dot and CBUS2 text.
    sense_end = (tap[0] + 7.62, tap[1])
    rz.wire(tap, sense_end, 'vbus-sense-stub')
    rz.llabel('VBUS_SENSE', sense_end, 0)
    for i, ref in enumerate(('C143', 'C144', 'C145')):
        rz.move(ref, (254.00, 250.19 + i * 10.16), rot=0)
        rz.glabel('+3.3V', rz.pin(ref, '1'), 0)
        rz.glabel('GND', rz.pin(ref, '2'), 0)
    for ref, net, ft, y in (('R160', 'USB_DP', 'FT_DP', 275.59),
                            ('R161', 'USB_DM', 'FT_DM', 270.51)):
        rz.move(ref, (266.70, y), rot=90)
        rz.glabel(net, rz.pin(ref, '1'), 180)
        rz.llabel(ft, rz.pin(ref, '2'), 0)
    # Restore the bridge-side loading caps (C173/C174 stay in this group).
    for cap, bp, ft, uy in (('C173', '8', 'FT_DP', 274.32),
                            ('C174', '9', 'FT_DM', 271.78)):
        cp = rz.pin(cap, '1')
        up = rz.pin('U142', bp)
        rz.wire(cp, (cp[0], uy), cap)
        rz.wire((cp[0], uy), up, cap + 'u')
    rz.textpos('Configure CBUS2', (342.90, cb2[1] + 13.97))


MOVED_REFS = [
    'R145', 'R146', 'R147', 'R162',
    'R163', 'R164', 'R165', 'R166', 'Y1', 'C141',
    'R790', 'U141', 'R140', 'R148', 'R149', 'C140', 'J140',
    'R158', 'R159', 'C143', 'C144', 'C145', 'R160', 'R161',
] + [r for caps in BANKS.values() for r in caps]


def finalize_property_text(rz: Rezone):
    """All moved parts get horizontal Reference/Value clear of body and wire."""
    root = K.parse(rz.text)
    special_side = {'C140', 'C141', 'C143', 'C144', 'C145', 'Y1', 'U141',
                    'J140', 'R158', 'R159'}
    # dense clusters need explicit (ref, value) anchor points
    fixed = {
        'U141': ((445.77, 105.41), (445.77, 123.19)),
        'J140': ((518.16, 93.98), (518.16, 118.11)),
        'Y1': ((321.31, 105.41), (321.31, 126.365)),
        'R142': ((443.23, 130.81), (443.23, 135.89)),
        'R143': ((443.23, 122.555), (443.23, 127.635)),
        'R144': ((443.23, 138.43), (443.23, 143.51)),
        'R146': ((24.13, 60.96), (24.13, 66.04)),
        'TP790': ((421.65, 139.70), (421.65, 142.24)),
        'TP791': ((421.65, 132.08), (421.65, 134.62)),
        'TP792': ((421.65, 124.46), (421.65, 127.00)),
        'C142': ((388.62, 241.30), (388.62, 248.92)),
        'C140': ((435.61, 135.89), (435.61, 138.43)),
        'C145': ((254.00, 269.24), (248.92, 270.51)),
        'R160': ((258.32, 274.32), (258.32, 276.86)),
        'R161': ((258.32, 269.24), (258.32, 271.78)),
        'R148': ((477.50, 119.38), (477.50, 132.08)),
        'R149': ((477.50, 134.62), (477.50, 147.32)),
    }
    fixed['R162'] = ((15.24, 27.94), (20.32, 27.94))
    for ref in ('R145', 'R147'):
        for sym in K.children(root, 'symbol'):
            r = next((p[2] for p in K.children(sym, 'property')
                      if p[1] == 'Reference'), None)
            if r == ref:
                y = float(K.child(sym, 'at')[2])
                fixed[ref] = ((15.24, y), (25.40, y))
                break
    for ref, ball, tx in (('R163', 'A14', 328.93), ('R164', 'B12', 328.93),
                          ('R165', 'B14', 328.93), ('R166', 'C14', 340.16)):
        py = rz.pin('U4', ball)[1]
        fixed[ref] = ((tx, py - 1.27), (tx, py + 1.27))
    for sym in K.children(root, 'symbol'):
        ref = next((p[2] for p in K.children(sym, 'property')
                    if p[1] == 'Reference'), None)
        lib = K.child(sym, 'lib_id')
        if ref is None or lib is None or ref == 'U4':
            continue
        at = K.child(sym, 'at')
        x, y = float(at[1]), float(at[2])
        rot = int(float(at[3])) if len(at) > 3 else 0
        if ref in fixed:
            rz.prop_pos(ref, 'Reference', fixed[ref][0], 0)
            rz.prop_pos(ref, 'Value', fixed[ref][1], 0)
            continue
        if ref in special_side or ref.startswith('U'):
            gap = {'Y1': 10.16, 'U141': 10.16, 'J140': 10.16,
                   'U142': 19.05}.get(ref, 6.35)
            if ref == 'U142':   # text above/below the QFN body
                rz.prop_pos(ref, 'Reference', (312.42, 252.73), 0)
                rz.prop_pos(ref, 'Value', (312.42, 309.88), 0)
                continue
            rz.prop_pos(ref, 'Reference', (x - gap, y), 0)
            rz.prop_pos(ref, 'Value', (x + gap, y), 0)
        elif ref.startswith('C'):
            # two stacked lines in one column beside the lead, never touching
            # the neighbouring cap at 10.16 mm pitch
            rz.prop_pos(ref, 'Reference', (x - 3.81, y - 1.27), 0)
            rz.prop_pos(ref, 'Value', (x - 3.81, y + 1.27), 0)
        elif rot in (90, 270) or ref.startswith('TP'):
            rz.prop_pos(ref, 'Reference', (x, y - 3.81), 0)
            rz.prop_pos(ref, 'Value', (x, y + 3.81), 0)
        else:
            rz.prop_pos(ref, 'Reference', (x - 3.81, y), 0)
            rz.prop_pos(ref, 'Value', (x + 3.81, y), 0)
    # Keep labels off wire interiors: move the two bridge labels and the XADC
    # tap to wire corners, and alternate the dense top rail flags.
    rz.label_at('label', 'FT_DP', (289.56, 274.32), (276.86, 274.32))
    rz.label_at('label', 'FT_DM', (289.56, 271.78), (276.86, 271.78))
    # XADC_VP stays at its baseline anchor: (427.99,140.97) belongs to
    # PROGRAM_B_0, so relocating the flag there would merge two nets.
    # Restore baseline angles on the dense +3.3V flag bank at y=33.02.
    rails = sorted((l for l in K.labels(rz.root, 'global_label')
                    if l['text'] == '+3.3V' and abs(l['p'][1] - 33.02) < 0.1),
                   key=lambda l: l['p'][0])
    for lab in rails:
        rz.label_at('global_label', '+3.3V', lab['p'], lab['p'], 0)


def text_collision_data(path: str):
    """Detailed text collisions for one sheet; shared by --verify and baseline compare."""
    root = K.parse(Path(path).read_text(encoding='utf-8'))
    wires = K.wires(root)
    pins = pins_from_root(root)

    def boxes():
        lib = S.library_unit_pins(root)
        libs = K.child(root, 'lib_symbols')
        rects = {}
        for sym in K.children(libs or [], 'symbol'):
            r = {}
            for sub in K.children(sym, 'symbol'):
                m = re.search(r'_(\d+)_(\d+)$', str(sub[1]))
                un = K.child(sub, 'unit')
                u = int(m.group(1)) if m else (int(un[1]) if un else 0)
                rr = K.child(sub, 'rectangle')
                if rr is not None:
                    r[u] = (float(K.child(rr, 'start')[1]),
                            float(K.child(rr, 'start')[2]),
                            float(K.child(rr, 'end')[1]),
                            float(K.child(rr, 'end')[2]))
            rects[str(sym[1])] = r
        out = []
        for sym in K.children(root, 'symbol'):
            libid = K.child(sym, 'lib_id')
            at = K.child(sym, 'at')
            if libid is None or at is None:
                continue
            ref = next((p[2] for p in K.children(sym, 'property')
                        if p[1] == 'Reference'), None)
            x, y = float(at[1]), float(at[2])
            rot = int(float(at[3])) if len(at) > 3 else 0
            mir = K.child(sym, 'mirror')
            un = K.child(sym, 'unit')
            u = int(un[1]) if un else 1
            rr = rects.get(str(libid[1]), {})
            r = rr.get(u) or rr.get(0)
            if not r:
                continue
            corners = []
            for px, py in ((r[0], r[1]), (r[2], r[3])):
                qx, qy = K.rotate(px, py, rot, mir[1] if mir else None)
                corners.append((x + qx, y - qy))
            out.append((ref, min(c[0] for c in corners), min(c[1] for c in corners),
                        max(c[0] for c in corners), max(c[1] for c in corners)))
        return out

    bs = boxes()

    def text_items():
        out = []

        def add(owner, txt, at, size, angle, kind, justify=None):
            w = 0.6 * size * max(len(str(txt)), 1)
            h = size
            if int(round(angle)) in (90, 270):
                w, h = h, w
            x, y = float(at[1]), float(at[2])
            if justify == 'right':
                x0, x1 = x - w, x
            elif justify == 'left':
                x0, x1 = x, x + w
            else:
                x0, x1 = x - w / 2, x + w / 2
            if int(round(angle)) in (90, 270):
                y0, y1 = (y - h, y) if int(round(angle)) == 90 else (y, y + h)
            else:
                y0, y1 = y - h / 2, y + h / 2
            out.append((owner, str(txt), kind, x0, y0, x1, y1, (x, y)))

        sym_rot = {}
        for sym in K.children(root, 'symbol'):
            ref = next((p[2] for p in K.children(sym, 'property')
                        if p[1] == 'Reference'), '?')
            at = K.child(sym, 'at')
            sym_rot[ref] = int(float(at[3])) if at is not None and len(at) > 3 else 0
        for sym in K.children(root, 'symbol'):
            ref = next((p[2] for p in K.children(sym, 'property')
                        if p[1] == 'Reference'), '?')
            for p in K.children(sym, 'property'):
                if p[1] not in ('Reference', 'Value'):
                    continue
                at = K.child(p, 'at')
                size = 1.0
                eff = K.child(p, 'effects')
                if eff is not None:
                    font = K.child(eff, 'font')
                    if font is not None:
                        sz = K.child(font, 'size')
                        if sz is not None:
                            size = float(sz[1])
                pr = (float(at[3]) if len(at) > 3 else 0) + sym_rot.get(ref, 0)
                add(f'{ref}.{p[1]}', p[2], at, size, pr % 360, 'property')
        for kind in ('label', 'global_label', 'text'):
            for node in K.children(root, kind):
                at = K.child(node, 'at')
                eff = K.child(node, 'effects')
                size = 1.0
                if eff is not None:
                    font = K.child(eff, 'font')
                    if font is not None:
                        sz = K.child(font, 'size')
                        if sz is not None:
                            size = float(sz[1])
                just = None
                if eff is not None:
                    jn = K.child(eff, 'justify')
                    if jn is not None:
                        just = 'right' if 'right' in jn else ('left' if 'left' in jn else None)
                add(f'{kind}:{node[1]}', node[1], at, size,
                    float(at[3]) if len(at) > 3 else 0, kind, just)
        touched = set(MOVED_REFS)
        for (ref, num), (nm, px, py, _u) in pins.items():
            if ref in touched and nm:
                add(f'{ref}.{num}:pin', nm, ['at', px, py, 0], 1.0, 0, 'pin')
        return out

    def overlap(a, b, eps=1e-6):
        return (min(a[5], b[5]) - max(a[3], b[3]) > eps
                and min(a[6], b[6]) - max(a[4], b[4]) > eps)

    def seg_hits_box(w, t):
        ax, ay = w['a']; bx, by = w['b']
        if abs(ay - by) < 1e-6:
            lo, hi = sorted((ax, bx))
            return (max(lo, t[3]) < min(hi, t[5]) and t[4] < ay < t[6])
        if abs(ax - bx) < 1e-6:
            lo, hi = sorted((ay, by))
            return (max(lo, t[4]) < min(hi, t[6]) and t[3] < ax < t[5])
        return False

    ti = text_items()
    records = []
    for i, a in enumerate(ti):
        for b in ti[i + 1:]:
            if overlap(a, b):
                records.append(dict(kind='text-text', a=a[0], apos=a[7],
                                    b=b[0], bpos=b[7],
                                    key=('tt', tuple(sorted((a[0], b[0]))))))
        for ref, x0, y0, x1, y1 in bs:
            # a pin name drawn inside its own body is normal KiCad rendering
            if a[2] == 'pin' and a[0].split('.')[0] == ref:
                continue
            if (min(a[5], x1) - max(a[3], x0) > 1e-6
                    and min(a[6], y1) - max(a[4], y0) > 1e-6):
                records.append(dict(kind='text-body', a=a[0], apos=a[7],
                                    b=ref, bpos=None,
                                    key=('tb', a[0], ref)))
        for w in wires:
            if any(abs(a[7][0] - e[0]) < 0.2 and abs(a[7][1] - e[1]) < 0.2
                   for e in (w['a'], w['b'])):
                continue
            if seg_hits_box(w, a):
                records.append(dict(kind='text-wire', a=a[0], apos=a[7],
                                    b=str(w['a']), bpos=str(w['b']),
                                    key=('tw', a[0], w['a'], w['b'])))
    return records


LABEL_ZONES = {'A': (8, 42, 44, 88), 'B': (283, 74, 330, 122),
               'C': (430, 88, 505, 150)}


def label_bbox(text: str, at, size: float, angle: float):
    """KiCad label flag: starts at the anchor and extends one way, with padding."""
    w = 0.9 * size * max(len(str(text)), 1) + 2.54
    h = 1.6 * size
    a = int(round(angle)) % 360
    if a in (90, 270):
        w, h = h, w
    x, y = float(at[1]), float(at[2])
    if a == 180:
        return (x - w, y - h / 2, x, y + h / 2)
    if a == 90:
        return (x - w / 2, y - h, x + w / 2, y)
    if a == 270:
        return (x - w / 2, y, x + w / 2, y + h)
    return (x, y - h / 2, x + w, y + h / 2)


def check_label_rules(path: str):
    """R1-R4 label placement rules plus an A/B clearance table."""
    root = K.parse(Path(path).read_text(encoding='utf-8'))
    wires = K.wires(root)
    pins = pins_from_root(root)
    pinpts = {(round(v[1], 4), round(v[2], 4)) for v in pins.values()}
    ends = set()
    for w in wires:
        ends.add((round(w['a'][0], 4), round(w['a'][1], 4)))
        ends.add((round(w['b'][0], 4), round(w['b'][1], 4)))

    labels = []
    for kind in ('label', 'global_label'):
        for node in K.children(root, kind):
            at = K.child(node, 'at')
            eff = K.child(node, 'effects')
            size = 1.0
            if eff is not None:
                font = K.child(eff, 'font')
                if font is not None:
                    sz = K.child(font, 'size')
                    if sz is not None:
                        size = float(sz[1])
            angle = float(at[3]) if len(at) > 3 else 0
            anchor = (round(float(at[1]), 4), round(float(at[2]), 4))
            bb = label_bbox(node[1], at, size, angle)
            labels.append(dict(text=node[1], kind=kind, anchor=anchor,
                               angle=angle, bb=bb))

    # symbol body boxes
    lib = S.library_unit_pins(root)
    libs = K.child(root, 'lib_symbols')
    rects = {}
    for sym in K.children(libs or [], 'symbol'):
        r = {}
        for sub in K.children(sym, 'symbol'):
            m = re.search(r'_(\d+)_(\d+)$', str(sub[1]))
            un = K.child(sub, 'unit')
            u = int(m.group(1)) if m else (int(un[1]) if un else 0)
            rr = K.child(sub, 'rectangle')
            if rr is not None:
                r[u] = (float(K.child(rr, 'start')[1]),
                        float(K.child(rr, 'start')[2]),
                        float(K.child(rr, 'end')[1]),
                        float(K.child(rr, 'end')[2]))
        rects[str(sym[1])] = r
    bodies = []
    for sym in K.children(root, 'symbol'):
        libid = K.child(sym, 'lib_id')
        at = K.child(sym, 'at')
        if libid is None or at is None:
            continue
        ref = next((p[2] for p in K.children(sym, 'property')
                    if p[1] == 'Reference'), None)
        x, y = float(at[1]), float(at[2])
        rot = int(float(at[3])) if len(at) > 3 else 0
        mir = K.child(sym, 'mirror')
        un = K.child(sym, 'unit')
        u = int(un[1]) if un else 1
        rr = rects.get(str(libid[1]), {})
        b = rr.get(u) or rr.get(0)
        if not b:
            continue
        cs = []
        for px, py in ((b[0], b[1]), (b[2], b[3])):
            qx, qy = K.rotate(px, py, rot, mir[1] if mir else None)
            cs.append((x + qx, y - qy))
        bodies.append((ref, min(c[0] for c in cs), min(c[1] for c in cs),
                       max(c[0] for c in cs), max(c[1] for c in cs)))

    def ov(a, b):
        return (min(a[2], b[2]) - max(a[0], b[0]) > 1e-6
                and min(a[3], b[3]) - max(a[1], b[1]) > 1e-6)

    def seg_box(w, b):
        ax, ay = w['a']; bx, by = w['b']
        if abs(ay - by) < 1e-6:
            return max(min(ax, bx), b[0]) < min(max(ax, bx), b[2]) and b[1] < ay < b[3]
        if abs(ax - bx) < 1e-6:
            return max(min(ay, by), b[1]) < min(max(ay, by), b[3]) and b[0] < ax < b[2]
        return False

    def seg_dist(w, b):
        """Distance from an axis-aligned wire segment to a text box."""
        ax, ay = w['a']; bx, by = w['b']
        if abs(ay - by) < 1e-6:
            dx = max(min(ax, bx) - b[2], b[0] - max(ax, bx), 0.0)
            dy = max(b[1] - ay, ay - b[3], 0.0)
        else:
            dx = max(b[0] - ax, ax - b[2], 0.0)
            dy = max(min(ay, by) - b[3], b[1] - max(ay, by), 0.0)
        return (dx * dx + dy * dy) ** 0.5

    r1 = [l for l in labels if l['anchor'] not in ends and l['anchor'] not in pinpts]
    r2 = []
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            if ov(a['bb'], b['bb']):
                r2.append((a['text'], b['text']))
    r3 = []
    for l in labels:
        for w in wires:
            # exempt ONLY the single segment whose end is this label's anchor
            if l['anchor'] == w['a'] or l['anchor'] == w['b']:
                continue
            if seg_box(w, l['bb']):
                r3.append((l['text'], w['a'], w['b']))
    r4 = []
    for l in labels:
        for ref, x0, y0, x1, y1 in bodies:
            if ov(l['bb'], (x0, y0, x1, y1)):
                r4.append((l['text'], ref))
    print(f'R1 anchors off wire/pin ends = {len(r1)}')
    for l in r1[:20]:
        print('   ', l['text'], l['anchor'])
    print(f'R2 overlapping label boxes = {len(r2)}')
    for p in r2[:20]:
        print('   ', p)
    print(f'R3 wires through label boxes = {len(r3)}')
    for p in r3[:20]:
        print('   ', p)
    print(f'R4 labels over symbol bodies = {len(r4)}')
    for p in r4[:20]:
        print('   ', p)

    # R5 -- pin-number and pin-name text boxes
    size = 1.0
    bmap = {b[0]: b[1:] for b in bodies}
    pintext = []
    for (ref, num), (nm, px, py, _u) in pins.items():
        b = bmap.get(ref)
        if b is None:
            continue
        x0, y0, x1, y1 = b
        if px <= x0 + 1e-6:            # left edge, horizontal pin line
            mid = ((px + x0) / 2, py)
            name_at = (x0 + 0.6 * 0.9 * size * max(len(nm), 1), py)
            off = (0, -0.5 * size)
        elif px >= x1 - 1e-6:          # right edge
            mid = ((px + x1) / 2, py)
            name_at = (x1 - 0.6 * 0.9 * size * max(len(nm), 1), py)
            off = (0, -0.5 * size)
        elif py <= y0 + 1e-6:          # top edge, vertical pin line
            mid = (px, (py + y0) / 2)
            name_at = (px, y0 + 0.6 * 0.9 * size * max(len(nm), 1))
            off = (0.5 * size, 0)
        else:                          # bottom edge
            mid = (px, (py + y1) / 2)
            name_at = (px, y1 - 0.6 * 0.9 * size * max(len(nm), 1))
            off = (0.5 * size, 0)
        for label, value, where in (('no', str(num), (mid[0] + off[0], mid[1] + off[1])),
                                    ('pn', nm, name_at)):
            w = 0.9 * size * max(len(value), 1)
            bb = (where[0] - w / 2, where[1] - size / 2,
                  where[0] + w / 2, where[1] + size / 2)
            pintext.append(dict(text=value, owner=f'{ref}.{num}:{label}',
                                bb=bb, anchor=where))
    # text boxes from properties and notes
    others = []
    sym_rot = {}
    for sym in K.children(root, 'symbol'):
        rr = next((p[2] for p in K.children(sym, 'property')
                   if p[1] == 'Reference'), '?')
        a0 = K.child(sym, 'at')
        sym_rot[rr] = int(float(a0[3])) if a0 is not None and len(a0) > 3 else 0
    for sym in K.children(root, 'symbol'):
        ref = next((p[2] for p in K.children(sym, 'property')
                    if p[1] == 'Reference'), '?')
        for p in K.children(sym, 'property'):
            if p[1] not in ('Reference', 'Value'):
                continue
            at = K.child(p, 'at')
            rot = sym_rot.get(ref, 0)
            a = (float(at[3]) if len(at) > 3 else 0) + rot
            others.append((f'{ref}.{p[1]}', label_bbox(p[2], at, 1.1, a % 360), (float(at[1]), float(at[2]))))
    for node in K.children(root, 'text'):
        at = K.child(node, 'at')
        others.append((f'text:{node[1][:22]}',
                       label_bbox(node[1], at, 1.0, float(at[3]) if len(at) > 3 else 0),
                       (float(at[1]), float(at[2]))))
    others += [(l['text'], l['bb'], l['anchor']) for l in labels]
    r5 = []
    for o, obb, oanchor in others:
        for pt in pintext:
            if ov(obb, pt['bb']):
                r5.append((o, pt['owner']))
    print(f'R5 text over pin numbers/names = {len(r5)}')
    for p in r5[:25]:
        print('   ', p)

    # R6 -- frame margin: text boxes and bodies inside the inset frame
    fx0, fy0, fx1, fy1 = 10.16, 10.16, 583.84, 409.84
    gaps = []
    for name, box in ([(t, b) for t, b, _a in others]
                      + [(l['text'], l['bb']) for l in labels]
                      + [(b[0], (b[1], b[2], b[3], b[4])) for b in bodies]):
        gaps.append((name, min(box[0] - fx0, box[1] - fy0,
                               fx1 - box[2], fy1 - box[3])))
    r6 = [(n, d) for n, d in gaps if d < 1.27]
    print(f'R6 objects inside 1.27 mm frame margin = {len(r6)}')
    for n, d in r6[:20]:
        print(f'    {n:24s} {d:6.2f} mm')

    # per-label clearance table for zones A and B, including nearest pin number
    for zname, (x0, y0, x1, y1) in LABEL_ZONES.items():
        sel = [l for l in labels if x0 <= l['anchor'][0] <= x1 and y0 <= l['anchor'][1] <= y1]
        print(f'--- zone {zname}: label | anchor | w x h | nearest label | clearance mm ---')
        for l in sorted(sel, key=lambda d: (d['anchor'][1], d['anchor'][0])):
            b = l['bb']
            best, gap = '', float('inf')
            for o in sel:
                if o is l:
                    continue
                ob = o['bb']
                dx = max(ob[0] - b[2], b[0] - ob[2], 0.0)
                dy = max(ob[1] - b[3], b[1] - ob[3], 0.0)
                d = (dx * dx + dy * dy) ** 0.5
                if d < gap:
                    gap, best = d, o['text']
            wbest, wgap = '', float('inf')
            for w in wires:
                if l['anchor'] in (w['a'], w['b']):
                    continue
                d = seg_dist(w, b)
                if d < wgap:
                    wgap, wbest = d, str(w['a'])
            pbest, pgap = '', float('inf')
            for pt in pintext:
                if not (x0 <= pt['anchor'][0] <= x1 and y0 <= pt['anchor'][1] <= y1):
                    continue
                pb = pt['bb']
                dx = max(pb[0] - b[2], b[0] - pb[2], 0.0)
                dy = max(pb[1] - b[3], b[1] - pb[3], 0.0)
                d = (dx * dx + dy * dy) ** 0.5
                if d < pgap:
                    pgap, pbest = d, pt['owner']
            print(f"   {l['text']:18s} | {l['anchor']} | {b[2]-b[0]:5.2f} x {b[3]-b[1]:4.2f}"
                  f" | {best:18s} | {gap:5.2f} | pin: {pbest:16s} {pgap:5.2f}"
                  f" | wire: {wbest:16s} {wgap:5.2f}"
                  f" | frame: {b[0]-fx0:5.2f}")
    return len(r1) + len(r2) + len(r3) + len(r4) + len(r5) + len(r6)


def verify(path: str, baseline: str | None = None) -> int:
    """Assertion pass over the finished sheet. Returns the violation count."""
    root = K.parse(Path(path).read_text(encoding='utf-8'))
    pins = pins_from_root(root)
    wires = K.wires(root)
    bad: list[str] = []

    # 1 -- every coordinate on the 1.27 mm grid
    off = []
    for node in root:
        if not isinstance(node, list) or not node:
            continue
        if str(node[0]) in ('at', 'xy', 'start', 'end'):
            vals = node[1:3]
            for v in vals:
                try:
                    x = float(v)
                except (TypeError, ValueError):
                    continue
                if abs(x / GRID - round(x / GRID)) > 1e-6:
                    off.append((node[0], vals))
    print(f'grid: off-grid coordinates = {len(off)}')
    for o in off[:10]:
        print('  ', o)
        bad.append('off-grid')

    # 2 -- axis-aligned wires
    diag = [w for w in wires
            if abs(w['a'][0] - w['b'][0]) > 1e-6
            and abs(w['a'][1] - w['b'][1]) > 1e-6]
    print(f'wires: {len(wires)} total, {len(diag)} non-axis-aligned')
    for w in diag[:10]:
        print('  ', w['a'], w['b'])
        bad.append('diagonal wire')

    # 3 -- symbol body boxes do not overlap
    def boxes():
        lib = S.library_unit_pins(root)
        libs = K.child(root, 'lib_symbols')
        rects = {}
        for sym in K.children(libs or [], 'symbol'):
            r = {}
            for sub in K.children(sym, 'symbol'):
                m = re.search(r'_(\d+)_(\d+)$', str(sub[1]))
                un = K.child(sub, 'unit')
                u = int(m.group(1)) if m else (int(un[1]) if un else 0)
                rr = K.child(sub, 'rectangle')
                if rr is not None:
                    r[u] = (float(K.child(rr, 'start')[1]),
                            float(K.child(rr, 'start')[2]),
                            float(K.child(rr, 'end')[1]),
                            float(K.child(rr, 'end')[2]))
            rects[str(sym[1])] = r
        out = []
        for sym in K.children(root, 'symbol'):
            libid = K.child(sym, 'lib_id')
            at = K.child(sym, 'at')
            if libid is None or at is None:
                continue
            ref = next((p[2] for p in K.children(sym, 'property')
                        if p[1] == 'Reference'), None)
            x, y = float(at[1]), float(at[2])
            rot = int(float(at[3])) if len(at) > 3 else 0
            mir = K.child(sym, 'mirror')
            un = K.child(sym, 'unit')
            u = int(un[1]) if un else 1
            rr = rects.get(str(libid[1]), {})
            r = rr.get(u) or rr.get(0)
            if not r:
                continue
            corners = []
            for px, py in ((r[0], r[1]), (r[2], r[3])):
                qx, qy = K.rotate(px, py, rot, mir[1] if mir else None)
                corners.append((x + qx, y - qy))
            out.append((ref, min(c[0] for c in corners), min(c[1] for c in corners),
                        max(c[0] for c in corners), max(c[1] for c in corners)))
        return out

    bs = boxes()
    overlaps = []
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i], bs[j]
            if (min(a[2], b[2]) - max(a[1], b[1]) > 1e-6
                    and min(a[3], b[3]) - max(a[2], b[2]) > 1e-6):
                overlaps.append((a[0], b[0]))
    print(f'bodies: {len(bs)} boxes, {len(overlaps)} overlapping pairs')
    for o in overlaps[:10]:
        print('  ', o)
        bad.append('body overlap')

    # 4 -- wire interior must not cross a body
    crossing = []
    for w in wires:
        for ref, x0, y0, x1, y1 in bs:
            ax, ay = w['a']; bx, by = w['b']
            if abs(ay - by) < 1e-6:
                lo, hi = sorted((ax, bx))
                if max(lo, x0) < min(hi, x1) and y0 < ay < y1:
                    crossing.append((ref, w['a'], w['b']))
            elif abs(ax - bx) < 1e-6:
                lo, hi = sorted((ay, by))
                if max(lo, y0) < min(hi, y1) and x0 < ax < x1:
                    crossing.append((ref, w['a'], w['b']))
    print(f'wire-through-body crossings = {len(crossing)}')
    for c in crossing[:10]:
        print('  ', c)
        bad.append('wire through body')

    # 5 -- no wire passes a pin mid-span
    mid = []
    for (ref, num), (_n, px, py, _u) in pins.items():
        for w in wires:
            if (px, py) in (w['a'], w['b']):
                continue
            if K.on_wire((px, py), w['a'], w['b']):
                mid.append((ref, num, w['a'], w['b']))
    print(f'pins at a wire mid-span = {len(mid)}')
    for m in mid[:10]:
        print('  ', m)
        bad.append('pin mid-span')

    # 6 -- junctions where a wire end lands inside another wire / >=3 wires meet
    junctions = {(round(p[0], 4), round(p[1], 4)) for p in K.points(root, 'junction')}
    missing = set()
    for i, w in enumerate(wires):
        for p in (w['a'], w['b']):
            for j, o in enumerate(wires):
                if i == j:
                    continue
                if p in (o['a'], o['b']):
                    continue
                if K.on_wire(p, o['a'], o['b']) and p not in junctions:
                    missing.add((round(p[0], 4), round(p[1], 4)))
    print(f'missing junctions at T-joins = {len(missing)}')
    for p in sorted(missing)[:10]:
        print('  ', p)
        bad.append('missing junction')

    # 7 -- text bounding boxes, with optional baseline classification
    records = text_collision_data(path)
    tc = {k: 0 for k in ('text-text', 'text-body', 'text-wire')}
    for r in records:
        tc[r['kind']] += 1
    total_tc = len(records)
    print('text collisions: ' + ' '.join(f'{k} = {v}' for k, v in tc.items())
          + f'; total = {total_tc}')
    if baseline:
        base = text_collision_data(baseline)
        base_keys = {r['key'] for r in base}
        base_wires = {r.get('bpos') for r in base if r['kind'] == 'text-wire'}
        pre, new = [], []
        for r in records:
            moved = (r['a'].split('.')[0] in MOVED_REFS
                     or r['b'].split('.')[0] in MOVED_REFS)
            same = r['key'] in base_keys
            if r['kind'] == 'text-wire':
                same = same and r.get('bpos') in base_wires
            (pre if same and not moved else new).append(r)
        print(f'baseline comparison: {baseline}')
        print(f'  pre-existing: {len(pre)}   new: {len(new)}')
        for k in tc:
            print('    ' + k + ': '
                  + str(sum(1 for r in pre if r['kind'] == k)) + ' pre-existing, '
                  + str(sum(1 for r in new if r['kind'] == k)) + ' new')
        for r in new[:60]:
            print('    NEW', r['kind'], r['a'], r['apos'], 'vs', r['b'], r['bpos'])
        if new:
            bad.append('new text collisions')
    elif total_tc:
        for r in records[:60]:
            print('   ', r['kind'], r['a'], r['apos'], 'vs', r['b'], r['bpos'])
        bad.append('text collisions')
    check_label_rules(path)
    print(f'VERIFY: {"FAIL" if bad else "PASS"} ({len(bad)} violation classes)')
    return len(bad)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sheet', default=DEFAULT_SHEET)
    ap.add_argument('--zones', default='A,B,C,D,E')
    ap.add_argument('--verify', action='store_true',
                    help='run the geometry assertion pass on --sheet and exit')
    ap.add_argument('--compare-baseline', metavar='SHEET', default=None,
                    help='classify text collisions as pre-existing vs new')
    args = ap.parse_args()
    if args.verify:
        raise SystemExit(verify(args.sheet, args.compare_baseline))
    rz = Rezone(args.sheet)
    zones = [z.strip().upper() for z in args.zones.split(',') if z.strip()]
    fn = {'A': zone_a, 'B': zone_b, 'C': zone_c, 'D': zone_d, 'E': zone_e}
    for z in zones:
        fn[z](rz)
        rz.save()
    rz.prune_dangling_labels()
    finalize_property_text(rz)
    rz.normalize_text_sizes()
    rz.save()
    print(f'rezoned {args.sheet}: zones {",".join(zones)}')


if __name__ == '__main__':
    main()
