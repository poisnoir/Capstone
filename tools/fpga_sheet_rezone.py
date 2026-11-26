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
        prop = re.compile(r'(\(property "[^"]*" "[^"]*"\s*\(at )([-\d.]+) ([-\d.]+)([^)]*\))')
        blk = prop.sub(lambda m: (m.group(1) + fmt(float(m.group(2)) + dx) + ' '
                                  + fmt(float(m.group(3)) + dy) + m.group(4)), blk)
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

    def prop_pos(self, ref: str, prop: str, to, angle: int = 0):
        """Place one symbol property (Reference/Value) at an absolute point."""
        to = (g(to[0]), g(to[1]))
        uid = self.sym_uuid(ref)
        bs, be = K.block_span(self.text, uid)
        blk = self.text[bs:be]
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
    for ref, ball, net in (('R147', 'L4', 'DAC_SDI'),
                           ('R145', 'M2', 'DAC_CS'),
                           ('R146', 'M1', 'DAC_SCLK')):
        px, py = rz.pin('U4', ball)          # FPGA pin end, from lib_symbols
        rz.move(ref, (21.59, py), rot=270)   # pin 1 faces the FPGA, pin 2 the net
        p1, p2 = rz.pin(ref, '1'), rz.pin(ref, '2')
        rz.wire(p1, (px, py), ref)
        rz.glabel(net, p2, 180)
    rz.move('R162', (15.24, 48.26), rot=90)
    p1, p2 = rz.pin('R162', '1'), rz.pin('R162', '2')
    rz.glabel('+3.3V', p1, 90)
    rz.wire(p2, (24.13, p2[1]), 'r162cs')
    rz.glabel('DAC_CS', (24.13, p2[1]), 0)


def zone_b(rz: Rezone):
    """ADC pull-ups, 32.768 MHz oscillator and bypass beside U4 unit 1."""
    rz.detach(['R163', 'R164', 'R165', 'R166', 'Y1', 'C141'])
    rz.del_wire((440.69, 73.66), (440.69, 113.03))   # old clock dog-leg
    rz.del_wire((447.04, 115.57), (447.04, 96.52))
    for y in (81.28, 83.82, 91.44, 93.98, 96.52, 99.06, 116.84):
        rz.del_wire((290.83, y), (295.91, y))        # old FPGA-to-label stubs
    for net, y in (('ADC_SDI', 83.82), ('ADC_SCLK', 91.44)):
        rz.del_label_at('global_label', net, (295.91, y))
        rz.glabel(net, (290.83, y), 0)               # same flag, at the pin
    # 5.08 mm pitch rows give Reference/Value room at the sheet's normal 1 mm text.
    rows = {'R164': 86.36, 'R163': 91.44, 'R166': 96.52, 'R165': 101.60}
    for ref, ball, net in (('R163', 'A14', 'ADC_RESET_N'),
                           ('R164', 'B12', 'ADC_CS'),
                           ('R165', 'B14', 'ADC_START_N'),
                           ('R166', 'C14', 'ADC_SYNC_IN')):
        px, py = rz.pin('U4', ball)
        rz.del_label_at('global_label', net, (295.91, py))   # superseded flag
        row = rows[ref]
        cx = 317.50
        rz.move(ref, (cx, row), rot=270)
        p1, p2 = rz.pin(ref, '1'), rz.pin(ref, '2')
        knee = (295.91, row)
        rz.wire((px, py), (295.91, py), ref + 'in')
        if abs(row - py) > 1e-6:
            rz.wire((295.91, py), knee, ref + 'jog')
        rz.wire(knee, p2, ref + 'out')
        rz.glabel('+3.3V', p1, 0)
        rz.glabel(net, (303.53, row), 0)         # clear of the old ADC flags
        rz.prop_pos(ref, 'Reference', (cx, row - 3.81))
        rz.prop_pos(ref, 'Value', (cx, row + 3.81))
    px, py = rz.pin('U4', 'D13')
    rz.del_label_at('global_label', 'CLOCK_32M768', (295.91, py))
    rz.move('Y1', (321.31, py - 2.54), rot=180)
    out = rz.pin('Y1', '3')
    rz.wire(out, (px, py), 'clk')
    rz.glabel('CLOCK_32M768', (px, py), 0)
    rz.glabel('+3.3V', rz.pin('Y1', '1'), 0)
    rz.glabel('+3.3V', rz.pin('Y1', '4'), 0)
    rz.glabel('GND', rz.pin('Y1', '2'), 0)
    rz.move('C141', (321.31, py + 12.70), rot=0)
    rz.glabel('+3.3V', rz.pin('C141', '1'), 0)
    rz.glabel('GND', rz.pin('C141', '2'), 0)
    rz.textpos('Clock branch termination', (335.28, py + 24.13))


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
    for net, fpin in (('QSPI_CS', '1'), ('QSPI_D0', '5'), ('QSPI_D1', '2'),
                      ('QSPI_D2', '3'), ('QSPI_D3', '7')):
        rz.llabel(net, rz.pin('U141', fpin), 0)
    rz.glabel('+3.3V', rz.pin('U141', '8'), 0)
    rz.glabel('GND', rz.pin('U141', '4'), 180)
    for ref, net, at in (('R140', 'QSPI_CS', (444.50, cclk[1] - 16.51)),
                         ('R148', 'QSPI_D2', (466.09, cclk[1] + 12.70)),
                         ('R149', 'QSPI_D3', (466.09, cclk[1] + 25.40)),
                         ('C140', None, (435.61, cclk[1] + 15.24))):
        rz.move(ref, at, rot=0)
        if net:
            ry = at[1]
            rz.glabel('+3.3V', rz.pin(ref, '1'), 180)   # text left of the body
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
        rz.llabel(net, rz.pin('J140', jp), 180)
        rz.llabel(net, rz.pin('U4', ball), 0)
    rz.glabel('+3.3V', rz.pin('J140', '2'), 180)
    for jp in ('3', '5', '7', '9', '11'):
        rz.glabel('GND', rz.pin('J140', jp), 0)
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
    # Put the sense flag on the divider tap, clear of U142's CBUS2 pin text.
    rz.llabel('VBUS_SENSE', tap, 0)
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


def verify(path: str) -> int:
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
    print(f'VERIFY: {"FAIL" if bad else "PASS"} ({len(bad)} violation classes)')
    return len(bad)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sheet', default=DEFAULT_SHEET)
    ap.add_argument('--zones', default='A,B,C,D,E')
    ap.add_argument('--verify', action='store_true',
                    help='run the geometry assertion pass on --sheet and exit')
    args = ap.parse_args()
    if args.verify:
        raise SystemExit(verify(args.sheet))
    rz = Rezone(args.sheet)
    zones = [z.strip().upper() for z in args.zones.split(',') if z.strip()]
    fn = {'A': zone_a, 'B': zone_b, 'C': zone_c, 'D': zone_d, 'E': zone_e}
    for z in zones:
        fn[z](rz)
        rz.save()
    rz.prune_dangling_labels()
    rz.normalize_text_sizes()
    rz.save()
    print(f'rezoned {args.sheet}: zones {",".join(zones)}')


if __name__ == '__main__':
    main()
