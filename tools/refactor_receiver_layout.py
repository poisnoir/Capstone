#!/usr/bin/env python3
"""Deterministic regenerator for the BRD-01 receiver schematic sheet.

Regenerates hardware/brd-01/kicad/receiver.kicad_sch from the committed
baseline (9f7dddb) into four left-to-right channel lanes, a reference row, an
ADC block and a decoupling bay.  All geometry is derived from lib_symbols pin
definitions through tools/kicad_sch_helper.py; no raw sheet coordinates are
guessed for pins.  Component UUIDs, references, values, footprints and all
other properties are carried over verbatim.

    python3 tools/refactor_receiver_layout.py            # regenerate
    python3 tools/refactor_receiver_layout.py --check    # verify idempotence
"""
import itertools
import re
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import kicad_sch_helper as H  # noqa: E402

SHEET = ROOT / 'hardware/brd-01/kicad/receiver.kicad_sch'
BASE = '9f7dddb:hardware/brd-01/kicad/receiver.kicad_sch'
NETLIST = Path('/tmp/baseline_netlist.xml')
G = 1.27
# FDA output riser offsets (mm), searched for zero crossings
OUT_RISER = 2.54
OUT_RUN = 25.40
NEG_RISER = 2.54
NEG_TOP = 15.24
RAILS = {'GND': 'power:GND', '+5VA': 'power:+5VA', '+12VA': 'power:+12VA',
         '-12VA': 'power:-12VA', '+3.3V': 'power:+3.3V'}


def g(v):
    return round(round(v / G) * G, 2)


def f(v):
    return H.fmt(v)


def base_text():
    return subprocess.check_output(['git', 'show', BASE], cwd=ROOT, text=True)


# ---------------------------------------------------------------------------
# Placement (all coordinates on the 1.27 mm grid)
# ---------------------------------------------------------------------------
PLACE = {}

# Shared column geometry for Ch1/Ch2/Ch3.
CX = dict(R1=114.30, D=152.40, C=190.50, Rp=228.60, Rn=381.00,
          INA=279.40, Rg=250.19, S1=335.28, F1=405.13, FDA=431.80,
          F2=458.47, Op=495.30, Co=529.59, Com=562.61)

# Role -> (ref key, fda pin map, F1 pin map) for each lane.
LANES = [
    dict(id='ch1', yc=209.55,
         refs=dict(R1='R101', R2='R102', D1='D101', D2='D102', D3='D103',
                   D4='D104', C1='C113', C2='C114', Rp='R103', Rn='R104',
                   INA='U104', Rg='R105', S1='R120', S2='R121',
                   F1='R122', F2='R123', FDA='U105:2', Op='R124', On='R125',
                   Co1='C125', Co2='C126', Com='C127', Cd1='C115', Cd2='C116',
                   pn='PEN1', ain='AIN1', g1='GAIN1', g2='GAIN2',
                   outp='FDA1', outn='FDA1'),
         fda=dict(in_p=6, in_n=7, out_p=12, out_n=13, fb_p=8, fb_n=5,
                  vocm=11),
         f1=dict(plus=1, minus=2, rot=180)),
    dict(id='ch2', yc=309.88,
         refs=dict(R1='R540', R2='R541', D1='D520', D2='D521', D3='D522',
                   D4='D523', C1='C540', C2='C541', Rp='R542', Rn='R543',
                   INA='U106', Rg='R544', S1='R548', S2='R549',
                   F1='R550', F2='R551', FDA='U108:1', Op='R552', On='R553',
                   Co1='C544', Co2='C545', Com='C546', Cd1='C542', Cd2='C543',
                   pn='PEN2', ain='AIN2', g1='PEN2_RG1', g2='PEN2_RG2',
                   outp='FDA2', outn='FDA2'),
         fda=dict(in_p=24, in_n=1, out_p=18, out_n=19, fb_p=2, fb_n=23,
                  vocm=17),
         f1=dict(plus=2, minus=1, rot=0)),
    dict(id='ch3', yc=410.21,
         refs=dict(R1='R560', R2='R561', D1='D530', D2='D531', D3='D532',
                   D4='D533', C1='C560', C2='C561', Rp='R562', Rn='R563',
                   INA='U107', Rg='R564', S1='R568', S2='R569',
                   F1='R570', F2='R571', FDA='U108:2', Op='R572', On='R573',
                   Co1='C564', Co2='C565', Com='C566', Cd1='C562', Cd2='C563',
                   pn='REF_COIL', ain='AIN3', g1='REF_COIL_RG1',
                   g2='REF_COIL_RG2', outp='FDA3', outn='FDA3'),
         fda=dict(in_p=6, in_n=7, out_p=12, out_n=13, fb_p=8, fb_n=5,
                  vocm=11),
         f1=dict(plus=2, minus=1, rot=0)),
]

for lane in LANES:
    yc = lane['yc']
    p = lane['refs']
    PLACE[p['R1']] = (CX['R1'], g(yc - 13.97), 90)
    PLACE[p['R2']] = (CX['R1'], g(yc + 13.97), 90)
    PLACE[p['D1']] = (CX['D'], g(yc - 17.78), 0)
    PLACE[p['D2']] = (CX['D'], g(yc - 10.16), 180)
    PLACE[p['D3']] = (CX['D'], g(yc + 10.16), 0)
    PLACE[p['D4']] = (CX['D'], g(yc + 17.78), 180)
    PLACE[p['C1']] = (CX['C'], g(yc - 13.97), 90)
    PLACE[p['C2']] = (CX['C'], g(yc + 13.97), 90)
    PLACE[p['Rp']] = (CX['Rp'], g(yc - 6.35), 0)
    if lane['id'] == 'ch1':
        PLACE[p['Rn']] = (CX['Rn'], g(yc + 10.16), 0)
    else:
        PLACE[p['Rn']] = (238.76, g(yc + 20.32), 0)
    PLACE[p['INA']] = (CX['INA'], yc, 0)
    PLACE[p['Rg']] = (CX['Rg'], yc, 180 if lane['id'] == 'ch1' else 0)
    PLACE[p['S1']] = (CX['S1'], g(yc - 7.62), 90)
    PLACE[p['S2']] = (g(CX['S1'] + 33.02), g(yc + 7.62), 90)
    PLACE[p['F1']] = (CX['F1'], g(yc - 16.51), lane['f1']['rot'])
    PLACE[p['FDA']] = (CX['FDA'], yc, 0)
    PLACE[p['F2']] = (CX['F2'], g(yc + 16.51), 0)
    PLACE[p['On']] = (CX['Op'], g(yc + 16.51), 90)
    PLACE[p['Op']] = (CX['Op'], g(yc - 16.51), 90)
    PLACE[p['Co2']] = (CX['Co'], g(yc + 16.51), 0)
    PLACE[p['Co1']] = (CX['Co'], g(yc - 16.51), 0)
    PLACE[p['Com']] = (CX['Com'], yc, 0)
    PLACE[p['Cd1']] = (CX['Rg'], g(yc - 12.70), 0)
    PLACE[p['Cd2']] = (CX['Rg'], g(yc + 12.70), 0)

# Ch0 / CURRENT_SUM (same template, shorter chain)
CH0 = dict(yc=118.11,
           refs=dict(R1='R110', Rp='R111', F1='R112', F2='R113',
                     FDA='U105:1', Op='R114', On='R115',
                     Co1='C120', Co2='C121', Com='C122'))
yc = CH0['yc']
p = CH0['refs']
PLACE[p['R1']] = (160.02, yc, 90)
PLACE[p['Rp']] = (227.33, g(yc + 7.62), 0)
PLACE[p['F1']] = (284.48, g(yc - 16.51), 0)
PLACE[p['FDA']] = (323.85, yc, 0)
PLACE[p['F2']] = (363.22, g(yc + 16.51), 0)
PLACE[p['On']] = (396.24, g(yc + 16.51), 90)
PLACE[p['Op']] = (396.24, g(yc - 16.51), 90)
PLACE[p['Co2']] = (429.26, g(yc + 16.51), 0)
PLACE[p['Co1']] = (429.26, g(yc - 16.51), 0)
PLACE[p['Com']] = (462.28, yc, 0)
CH0.update(outp='FDA0', outn='FDA0', fda=dict(in_p=24, in_n=1, out_p=18, out_n=19, fb_p=2, fb_n=23,
                    vocm=17), f1=dict(plus=2, minus=1, rot=0))

# Reference chain (left to right), Y 475-545.
PLACE.update({
    'U102': (442.01, 514.35, 0),
    'C131': (477.04, 502.92, 0),
    'U103': (514.35, 514.35, 0),
    'R186': (550.54, 514.35, 90),
    'D534': (585.47, 514.35, 0),
    'C101': (614.37, 502.92, 0),
    'C102': (614.37, 525.78, 0),
})

# ADC block.
PLACE.update({
    'U101': (685.80, 279.40, 0),
    'R100': (620.00, 271.78, 90),
    'R180': (609.60, 285.75, 0),
    'R181': (609.60, 311.15, 180),
    'C106': (741.68, 68.58, 90),
    'C103': (722.38, 259.08, 90),
    'C104': (722.38, 271.78, 90),
    'C105': (722.38, 284.48, 90),
    'C107': (722.38, 297.18, 90),
    'C108': (747.66, 259.08, 90),
    'C109': (747.66, 271.78, 90),
    'C110': (747.66, 284.48, 90),
    'C111': (747.66, 297.18, 90),
})

# Decoupling bay: one vertical rail ladder per rail, GND along the bottom.
BAY = dict(x0=609.60, y0=25.40, x1=759.45, y1=121.92)
GND_BUS_Y = 106.68
BAY_X0, BAY_X1 = 635.00, 745.49  # 500 G, 586 G
RAIL_COLS = {'+12VA': 627.38, '-12VA': 665.48, '+5VA': 703.26}
RAIL_ROWS = [43.18, 55.88, 68.58, 81.28, 93.98]
BAY_GROUPS = {
    '+12VA': ['C100', 'C115', 'C130', 'C542', 'C562'],
    '-12VA': ['C116', 'C543', 'C563'],
    '+5VA': ['C112', 'C123', 'C128', 'C547', 'C567'],
}
for rail, refs in BAY_GROUPS.items():
    for ref, y in zip(refs, RAIL_ROWS):
        PLACE[ref] = (RAIL_COLS[rail], y, 90)
PLACE['U105:3'] = (741.68, 43.18, 0)
PLACE['U108:3'] = (741.68, 55.88, 0)


# ---------------------------------------------------------------------------
# Sheet model derived through helper primitives
# ---------------------------------------------------------------------------
class Sheet:
    def __init__(self, text):
        self.root = H.parse(text)
        self.libpins = H.lib_pins(self.root)
        self.lib = {}
        self.key = {}
        self.uuid_of = {}
        self.inst = {}
        for s in H.children(self.root, 'symbol'):
            u = H.child(s, 'uuid')
            if u is None:
                continue
            lib = H.child(s, 'lib_id')[1]
            unit = H.child(s, 'unit')
            unit = int(unit[1]) if unit is not None else 1
            ref = next((p[2] for p in H.children(s, 'property')
                        if p[1] == 'Reference'), None)
            k = f'{ref}:{unit}' if lib == 'accubot:ADA4940-2ACPZ' else ref
            self.lib[u[1]] = lib
            self.key[u[1]] = k
            self.uuid_of.setdefault(k, u[1])
            self.inst.setdefault(k, s)

    def origin(self, key):
        at = H.child(self.inst[key], 'at')
        return float(at[1]), float(at[2]), int(float(at[3]))

    def pins(self, key):
        out = {}
        x, y, rot = self.origin(key)
        mir = H.child(self.inst[key], 'mirror')
        mirror = mir[1] if mir else None
        for num, name, px, py in self.libpins.get(self.lib[self.uuid_of[key]], []):
            qx, qy = H.rotate(px, py, rot, mirror)
            out[str(num)] = (round(x + qx, 4), round(y - qy, 4))
        return out

    def pin(self, key, num):
        return self.pins(key)[str(num)]

    def unit_pins(self, key):
        """Only the pins belonging to this instance's unit (plus common unit 0)."""
        inst = self.inst[key]
        unit = int((H.child(inst, 'unit') or [None, 1])[1])
        lib = self.lib[self.uuid_of[key]]
        libsym = next((s for s in H.children(H.child(self.root, 'lib_symbols'),
                                             'symbol') if s[1] == lib), None)
        allowed = set()
        if libsym is not None:
            for sub in H.children(libsym, 'symbol'):
                parts = sub[1].rsplit('_', 2)
                if len(parts) >= 3 and parts[-2].isdigit() \
                        and int(parts[-2]) in (0, unit):
                    allowed.update(H.child(p, 'number')[1]
                                   for p in H.children(sub, 'pin'))
        return {n: p for n, p in self.pins(key).items() if n in allowed}


# ---------------------------------------------------------------------------
# S-expression editor
# ---------------------------------------------------------------------------
class Editor:
    def __init__(self, text):
        self.t = text

    def move_symbol(self, uuid, x, y, rot):
        s, e = H.block_span(self.t, uuid)
        blk = self.t[s:e]
        m = re.search(r'\t\t\(at [\d.-]+ [\d.-]+(?: [\d.-]+)?\)', blk)
        blk = (blk[:m.start()] + f'\t\t(at {f(x)} {f(y)} {rot})'
               + blk[m.end():])
        self.t = self.t[:s] + blk + self.t[e:]

    def move_prop(self, uuid, prop, x, y, justify=None, hide=None, angle=0):
        s, e = H.block_span(self.t, uuid)
        blk = self.t[s:e]
        i = blk.find(f'(property "{prop}"')
        if i < 0:
            return
        depth, j = 0, i
        while j < len(blk):
            if blk[j] == '(':
                depth += 1
            elif blk[j] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        sub = blk[i:j + 1]
        sub = re.sub(r'\(at [\d.-]+ [\d.-]+ [\d.-]+\)',
                     f'(at {f(x)} {f(y)} {angle})', sub, count=1)
        sub = re.sub(r'\(justify [^)]*\)', '', sub)
        if justify:
            sub = sub.replace('\t\t\t)',
                              f'\t\t\t)\n\t\t\t\t(justify {justify})', 1)
        if hide is True and '(hide yes)' not in sub:
            sub = sub.replace('\t\t\t(at ', '\t\t\t(hide yes)\n\t\t\t(at ', 1)
        if hide is False:
            sub = sub.replace('\t\t\t(hide yes)\n', '')
        self.t = self.t[:s] + blk[:i] + sub + blk[j + 1:] + self.t[e:]

    def strip(self, kinds):
        hits = []
        for kind in kinds:
            hits += [(a, b) for a, b, _ in H.top_blocks(self.t, kind)]
        for a, b in sorted(hits, reverse=True):
            self.t = self.t[:a - 1] + self.t[b:]

    def append(self, block):
        i = self.t.rstrip().rfind(')')
        self.t = self.t[:i] + block + self.t[i:]


_U = [0]


def uid():
    _U[0] += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'receiver-relayout-{_U[0]}'))


def wire_block(a, b):
    return (f'\t(wire\n\t\t(pts\n\t\t\t(xy {f(a[0])} {f(a[1])}) '
            f'(xy {f(b[0])} {f(b[1])})\n\t\t)\n'
            f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')


def junction_block(p):
    return (f'\t(junction\n\t\t(at {f(p[0])} {f(p[1])})\n'
            f'\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')


def nc_block(p):
    return (f'\t(no_connect\n\t\t(at {f(p[0])} {f(p[1])})\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')


def label_block(kind, text, p, angle=0, shape='passive'):
    just = 'right' if angle in (180, 270) else 'left'
    out = [f'\t({kind} "{text}"']
    if kind != 'label':
        out.append(f'\t\t(shape {shape})')
    out += [f'\t\t(at {f(p[0])} {f(p[1])} {angle})',
            '\t\t(effects', '\t\t\t(font', '\t\t\t\t(size 1 1)',
            '\t\t\t)', f'\t\t\t(justify {just})', '\t\t)',
            f'\t\t(uuid "{uid()}")']
    if kind == 'global_label':
        out += [f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"',
                f'\t\t\t(at {f(p[0])} {f(p[1])} 0)',
                '\t\t\t(hide yes)', '\t\t\t(show_name no)',
                '\t\t\t(do_not_autoplace no)', '\t\t\t(effects',
                '\t\t\t\t(font', '\t\t\t\t\t(size 1.27 1.27)',
                '\t\t\t\t)\n\t\t\t)\n\t\t)']
    out.append('\t)')
    return '\n'.join(out) + '\n'


def power_block(lib, ref, p, rot, text_at, field_angle=0):
    name = lib.split(':')[1]
    desc = ('Power symbol creates a global label with name '
            f'\\"{name}\\" , power')
    out = [
        '\t(symbol', f'\t\t(lib_id "{lib}")',
        f'\t\t(at {f(p[0])} {f(p[1])} {rot})',
        '\t\t(unit 1)', '\t\t(body_style 1)',
        '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)',
        '\t\t(on_board yes)', '\t\t(in_pos_files yes)', '\t\t(dnp no)',
        '\t\t(fields_autoplaced yes)', f'\t\t(uuid "{uid()}")',
        f'\t\t(property "Reference" "{ref}"',
        f'\t\t\t(at {f(p[0])} {f(p[1])} 0)', '\t\t\t(hide yes)',
        '\t\t\t(show_name no)', '\t\t\t(do_not_autoplace no)',
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)',
        f'\t\t(property "Value" "{name}"',
        f'\t\t\t(at {f(text_at[0])} {f(text_at[1])} {field_angle})',
        '\t\t\t(show_name no)', '\t\t\t(do_not_autoplace no)',
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)',
        f'\t\t(property "Footprint" ""\n\t\t\t(at {f(p[0])} {f(p[1])} 0)',
        '\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)',
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)',
        f'\t\t(property "Datasheet" ""\n\t\t\t(at {f(p[0])} {f(p[1])} 0)',
        '\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)',
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)',
        f'\t\t(property "Description" "{desc}"\n\t\t\t(at {f(p[0])} {f(p[1])} 0)',
        '\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)',
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)',
        f'\t\t(pin "1"\n\t\t\t(uuid "{uid()}")\n\t\t)',
        '\t\t(instances\n\t\t\t(project "brd-01"',
        '\t\t\t\t(path "/bcf11a9e-584a-4da7-9f85-9c74b718d606/0fb3cf57-3d6d-4e45-b58e-c90ee5551265"',
        f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)',
    ]
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
class Router:
    def __init__(self, ed, sh):
        self.ed, self.sh = ed, sh
        self.junc = set()

    def w(self, a, b):
        a = (round(a[0], 4), round(a[1], 4))
        b = (round(b[0], 4), round(b[1], 4))
        if a == b:
            return
        assert abs(a[0] - b[0]) < 1e-6 or abs(a[1] - b[1]) < 1e-6, (a, b)
        for v in (a[0], a[1], b[0], b[1]):
            assert abs(v / G - round(v / G)) < 1e-6, (a, b)
        self.ed.append(wire_block(a, b))

    def poly(self, pts):
        for a, b in zip(pts, pts[1:]):
            self.w(a, b)

    def L(self, a, b, order='hv'):
        """Orthogonal L route from a to b via one bend, grid-derived."""
        if a[0] == b[0] or a[1] == b[1]:
            self.w(a, b)
        elif order == 'hv':
            self.poly([a, (b[0], a[1]), b])
        else:
            self.poly([a, (a[0], b[1]), b])

    def tee(self, p):
        p = (round(p[0], 4), round(p[1], 4))
        if p not in self.junc:
            self.junc.add(p)
            self.ed.append(junction_block(p))

    def P(self, key, num):
        return self.sh.pin(key, num)

    def label(self, kind, text, p, angle=0):
        self.ed.append(label_block(kind, text, p, angle))


# ---------------------------------------------------------------------------
# Netlist-derived pin -> net map and NC pin resolve
# ---------------------------------------------------------------------------
def pin_net_map():
    root = ET.parse(NETLIST).getroot()
    out = {}
    for net in root.iter('net'):
        for n in net.iter('node'):
            out[(n.get('ref'), n.get('pin'))] = net.get('name')
    return out


def baseline_nc_pins(base_sh):
    """Map each of the 16 baseline no_connect markers to its pin."""
    root = base_sh.root
    pts = [(float(a[1]), float(a[2])) for a in H.children(root, 'no_connect')
           for a in [H.child(a, 'at')]]
    found = []
    insts = H.instances(root)
    for p in pts:
        hit = None
        for inst in insts:
            for num, name, x, y in inst['pins']:
                if abs(x - p[0]) < 1e-6 and abs(y - p[1]) < 1e-6:
                    key = inst['ref']  # all baseline NC pins are on single-unit parts
                    hit = (key, num)
                    break
            if hit:
                break
        found.append((p, hit))
    return found


# ---------------------------------------------------------------------------
# Routing: channel lanes
# ---------------------------------------------------------------------------
def fda_section(r, p, f, lanecfg, refcfg, plus_src, minus_src, dplus, dminus,
                f2_in=True):
    """Route one FDA amplifier with crossing-free input and output runs.

    The ADA4940 pinout interleaves +OUT/-OUT/+FB/-FB on one side.  The +OUT
    pair is joined by a tight loop; the -OUT net uses four short local labels
    so the two nets never cross.  This is the only label class kept outside
    the ADC reference/VCM/AIN taps.
    """
    P = r.P
    fi = lanecfg['f1']
    fp, in_p = P(p['F1'], fi['plus']), P(p['FDA'], f['in_p'])
    x4 = g(plus_src[0] + dplus)
    x5 = g(in_p[0] - 5.08)
    r.poly([plus_src, (x4, plus_src[1]), (x4, fp[1]), fp])
    r.poly([fp, (x5, fp[1]), (x5, in_p[1]), in_p])

    in_n = P(p['FDA'], f['in_n'])
    if f2_in:
        f2m = P(p['F2'], 2)
        x11 = g(minus_src[0] + dminus)
        x12 = g(in_n[0] - 24.13)
        r.poly([minus_src, (x11, minus_src[1]), (x11, f2m[1]), f2m])
        r.tee((x12, f2m[1]))
        r.poly([(x12, f2m[1]), (x12, in_n[1]), in_n])
    else:
        r.poly([minus_src, (g(minus_src[0] + dminus), minus_src[1]),
                (g(minus_src[0] + dminus), in_n[1]), in_n])

    # +OUT: tight loop on the pin column, then down to F2 and the AIN resistor
    f2p, out_p, fb_p = P(p['F2'], 1), P(p['FDA'], f['out_p']), P(p['FDA'], f['fb_p'])
    x9 = g(out_p[0] + OUT_RISER)
    x10 = g(out_p[0] + OUT_RUN)
    r.poly([out_p, (x9, out_p[1]), (x9, fb_p[1]), fb_p])
    r.poly([(x9, out_p[1]), (x10, out_p[1]), (x10, f2p[1]), f2p])
    r.poly([f2p, (g(f2p[0] + 19.05), f2p[1]),
            (g(f2p[0] + 19.05), P(p['Op'], 1)[1]), P(p['Op'], 1)])

    # -OUT: join -OUT/-FB on a riser beyond the +OUT exit, then run the net
    # above the body to F1 and right of the output resistor to On.  No local
    # labels: all four FDA*_OUT_N fragments become continuous wire.
    out_n, fb_n = P(p['FDA'], f['out_n']), P(p['FDA'], f['fb_n'])
    fn = P(p['F1'], fi['minus'])
    on = P(p['On'], 1)
    xr = g(out_n[0] + NEG_RISER)
    ytop = g(min(out_n[1], fb_n[1]) - NEG_TOP)
    xleft = fn[0]
    xright = g(P(p['Op'], 2)[0] - 5.08)
    r.poly([out_n, (xr, out_n[1]), (xr, fb_n[1]), fb_n])
    r.poly([(xr, out_n[1]), (xr, ytop), (xleft, ytop), fn])
    r.poly([(xr, ytop), (xright, ytop), (xright, on[1]), on])
    if not f2_in:
        f2m = P(p['F2'], 2)
        xf = g(f2m[0] + 7.62)
        r.poly([f2m, (xf, f2m[1]), (xf, on[1]), on])

    aplus, aminus = P(p['Op'], 2), P(p['On'], 2)
    c1p, c2p = P(p['Co1'], 1), P(p['Co2'], 1)
    m1, m2 = P(p['Com'], 1), P(p['Com'], 2)
    xa, xb = g(aplus[0] + 15.24), g(c1p[0] + 10.67)
    xc, xd = g(aminus[0] + 15.24), g(c2p[0] + 22.86)
    r.poly([aplus, (xa, aplus[1]), (xa, c1p[1]), c1p])
    r.poly([c1p, (xb, c1p[1]), (xb, m1[1]), m1])
    r.poly([aminus, (xc, aminus[1]), (xc, c2p[1]), c2p])
    r.poly([c2p, (xd, c2p[1]), (xd, m2[1]), m2])


def route_lane(r, lane, sh0):
    yc = lane['yc']
    p = lane['refs']
    f = lane['fda']
    P = r.P
    xd = P(p['D1'], 2)[0]
    # protect rails: P and N clamp nodes
    for hi, lo, r1, d1, d2, c1 in (
            ('D1', 'D2', 'R1', 'D1', 'D2', 'C1'),
            ('D3', 'D4', 'R2', 'D3', 'D4', 'C2')):
        y = P(p[r1], 2)[1]
        r.poly([P(p[r1], 2), (xd, y), P(p[c1], 1)])
        r.poly([P(p[d1], 2), P(p[d2], 1)])
        r.tee((xd, y))

    # input coupling P -> INA IN+
    rp = P(p['Rp'], 1)
    inap = P(p['INA'], 5)
    r.poly([P(p['C1'], 2), (rp[0], P(p['C1'], 2)[1]), rp])
    r.poly([rp, (inap[0], rp[1]), inap])

    # gain set resistor GS1/GS2
    if lane['id'] == 'ch1':
        rg1, rg2 = P(p['Rg'], 2), P(p['Rg'], 1)
    else:
        rg1, rg2 = P(p['Rg'], 1), P(p['Rg'], 2)
    gs1, gs2 = P(p['INA'], 3), P(p['INA'], 12)
    x1 = g(gs1[0] - 10.16)
    x2 = g(gs2[0] - 5.08)
    r.poly([gs1, (x1, gs1[1]), (x1, rg1[1]), rg1])
    r.poly([gs2, (x2, gs2[1]), (x2, rg2[1]), rg2])

    # INA SENSE -> VO
    vo, sense, s1 = P(p['INA'], 9), P(p['INA'], 8), P(p['S1'], 1)
    x3 = g(vo[0] + 27.94)
    r.poly([vo, s1])
    r.poly([sense, (x3, sense[1]), (x3, vo[1])])
    r.tee((x3, vo[1]))

    # differential input nets and FDA outputs
    fda_section(r, p, lane['fda'], lane, p, P(p['S1'], 2), P(p['S2'], 2),
                11.43, 16.51)

    # inverting input: INA IN- -> pulldown -> coupling cap (Ch2/Ch3 only;
    # Ch1 grounds INA IN- and biases C114/R104 from +12VA in the baseline)
    if lane['id'] != 'ch1':
        rn1 = P(p['Rn'], 1)
        xi = g(P(p['INA'], 4)[0] - 26.67)
        r.poly([P(p['INA'], 4), (xi, P(p['INA'], 4)[1]),
                (xi, rn1[1]), rn1])
        xc2 = g(P(p['C2'], 2)[0] + 16.51)
        r.poly([P(p['C2'], 2), (xc2, P(p['C2'], 2)[1]),
                (xc2, rn1[1]), rn1])
        r.tee(rn1)


def route_ch0(r):
    lane = CH0
    p = lane['refs']
    f = lane['fda']
    P = r.P
    fda_section(r, p, CH0['fda'], CH0, CH0, P(p['R1'], 2), P(p['Rp'], 2),
                33.02, 25.40, f2_in=False)


def route_reference(r):
    P = r.P
    u6, c1 = P('U102', 6), P('C131', 1)
    r.poly([u6, (g(u6[0] + 14.0), u6[1]), (g(u6[0] + 14.0), c1[1]), c1])
    v3 = P('U103', 3)
    r.poly([c1, (v3[0], c1[1]), v3])
    o1, i4, r1 = P('U103', 1), P('U103', 4), P('R186', 1)
    xa, xb = g(o1[0] + 10.16), g(r1[0] - 6.35)
    r.poly([o1, (xa, o1[1]), (xa, r1[1]), (xb, r1[1])])
    r.poly([i4, (g(i4[0] - 7.62), i4[1]), (g(i4[0] - 7.62), g(r1[1] + 6.35)),
            (xb, g(r1[1] + 6.35)), (xb, r1[1])])
    r.tee((xb, r1[1]))
    r.w((xb, r1[1]), r1)
    r2, d2 = P('R186', 2), P('D534', 2)
    yb = g(d2[1] + 6.35)
    r.poly([r2, (r2[0], yb), (d2[0], yb), d2])
    c101, c102 = P('C101', 1), P('C102', 1)
    r.poly([d2, (g(d2[0] + 10.16), d2[1]), (g(d2[0] + 10.16), c101[1]), c101])
    r.poly([d2, (g(c102[0] + 7.62), d2[1]), (g(c102[0] + 7.62), c102[1]), c102])


def route_adc(r):
    P = r.P
    # reference taps into U101 are labelled at the ADC pin (bus tap)
    for num in (6, 43):
        a = P('U101', num)
        tip = (g(a[0] - 7.62), a[1])
        r.poly([a, tip])
        r.label('label', 'ADC_REF', tip)
    r.w(P('U101', 34), P('C103', 1))
    for num, ref, xt in ((61, 'C104', 713.74), (52, 'C105', 706.12)):
        a, b = P('U101', num), P(ref, 1)
        r.poly([a, (xt, a[1]), (xt, b[1]), b])
    # control resistors sit on the ADC's left edge, next to their pins
    for ref, num, pin in (('R180', 11, 2), ('R181', 21, 1)):
        r.poly([P(ref, pin), P('U101', num)])
    r.poly([P('R100', 2), P('U101', 32)])


# ---------------------------------------------------------------------------
# Power symbols, labels, no-connects
# ---------------------------------------------------------------------------
def place_power(r, ed, sh, pinmap, ncbase, sh0):
    """Rail symbols on clean buses: one per rail per bay/FDA/ADC cluster.

    A short bus wire joins every supply pin of a cluster; a single power
    symbol sits on that bus.  All symbols are unrotated so their value text
    stays horizontal and clear of neighbours.
    """
    reuse = [u for u, lib in sh.lib.items() if lib.startswith('power:')]
    counter = [0]

    placed = set()

    def sym(net, p, text_at, rot=0):
        sig = (net, round(p[0], 4), round(p[1], 4))
        if sig in placed:
            return
        placed.add(sig)
        counter[0] += 1
        ref = f'#PWR{counter[0]:03d}'
        lib = RAILS[net]
        if reuse and lib == 'power:GND':
            u = reuse.pop()
            a, b = H.block_span(ed.t, u)
            blk = ed.t[a:b]
            blk = re.sub(r'\t\t\(at [\d.-]+ [\d.-]+ [\d.-]+\)',
                         f'\t\t(at {f(p[0])} {f(p[1])} 0)', blk, count=1)
            blk = re.sub(r'\(property "Reference" "[^"]*"',
                         f'(property "Reference" "{ref}"', blk, count=1)
            blk = re.sub(r'\(reference "[^"]*"',
                         f'(reference "{ref}"', blk, count=1)
            m = re.search(r'\(property "Value" "GND"\s*\n\s*\(at [\d.-]+ [\d.-]+ [\d.-]+\)',
                          blk)
            if m:
                blk = blk[:m.start()] + re.sub(
                    r'\(at [\d.-]+ [\d.-]+ [\d.-]+\)',
                    f'(at {f(text_at[0])} {f(text_at[1])} 0)', m.group(0)) \
                    + blk[m.end():]
            ed.t = ed.t[:a] + blk + ed.t[b:]
        else:
            ed.append(power_block(lib, ref, p, rot, text_at,
                                  90 if rot in (90, 270) else 0))
        ed.append(junction_block(p))

    # --- decoupling bay: one vertical bus per rail, GND along the bottom ---
    for rail, col in RAIL_COLS.items():
        bx = g(col - 7.62)
        hi, lo = 38.10, max(RAIL_ROWS[:len(BAY_GROUPS[rail])])
        r.w((bx, hi), (bx, lo))
        top = (bx, g(hi - 2.54))
        r.w((bx, hi), top)
        sym(rail, top, (g(bx - 5.08), top[1]))
        r.tee((bx, hi))
        for key in BAY_GROUPS[rail]:
            pin = sh.pin(key, 1)
            r.w(pin, (bx, pin[1]))
            r.tee((bx, pin[1]))
            gpin = sh.pin(key, 2)
            gx = g(col + 7.62)
            r.w(gpin, (gx, gpin[1]))
            r.w((gx, gpin[1]), (gx, GND_BUS_Y))
            r.tee((gx, gpin[1]))
            r.tee((gx, GND_BUS_Y))
    for key in ('U105:3', 'U108:3'):
        pin = sh.pin(key, 25)
        r.w(pin, (pin[0], GND_BUS_Y))
        r.tee((pin[0], GND_BUS_Y))
    c106g = sh.pin('C106', 2)
    r.w(c106g, (c106g[0], GND_BUS_Y))
    r.tee((c106g[0], GND_BUS_Y))
    r.w((BAY_X0, GND_BUS_Y), (BAY_X1, GND_BUS_Y))
    gbottom = (BAY_X1, g(GND_BUS_Y + 2.54))
    r.w((BAY_X1, GND_BUS_Y), gbottom)
    sym('GND', gbottom, (BAY_X1, g(gbottom[1] + 3.81)))

    # --- ADA4940 units: individual symbols, unrotated horizontal text ---
    for key in ('U105:1', 'U105:2', 'U108:1', 'U108:2'):
        ref = key.split(':')[0]
        ox, oy, _ = sh.origin(key)
        for num, p_ in sorted(sh.unit_pins(key).items(), key=lambda kv: int(kv[0])):
            net = pinmap.get((ref, num))
            if net not in RAILS:
                continue
            sgn = -1 if p_[0] < ox else 1
            sym(net, p_, (g(p_[0] + sgn * 5.08), p_[1]),
                270 if sgn < 0 else 90)

    # --- U101: one bus per rail on each side of the 64-pin body ---
    ux, _, _ = sh.origin('U101')
    upins = sh.unit_pins('U101')
    for side, bx in (('right', 704.85), ('left', 619.76)):
        sel = {n: p for n, p in upins.items()
               if (p[0] > ux) == (side == 'right')}
        for net in ('+5VA', 'GND'):
            group = [p for n, p in sel.items()
                     if pinmap.get(('U101', n)) == net]
            if not group:
                continue
            y0, y1 = g(min(p[1] for p in group)), g(max(p[1] for p in group))
            r.w((bx, y0), (bx, y1))
            for p_ in group:
                r.w(p_, (bx, p_[1]))
                r.tee((bx, p_[1]))
            tx = g(bx - 5.08) if side == 'right' else g(bx + 5.08)
            ta = (g(bx + 5.08), y0) if net == 'GND' and side == 'right' else (bx, g(y0 - 3.81))
            sym(net, (bx, y0), ta)
            r.tee((bx, y0))
    # +3.3V pins: one symbol each side, clear of the two rail buses
    for q in [p for n, p in upins.items()
              if pinmap.get(('U101', n)) == '+3.3V']:
        sgn = 1 if q[0] > ux else -1
        sym('+3.3V', q, (g(q[0] + sgn * 5.08), q[1]))

    # --- remaining rail pins: one symbol each, unrotated horizontal text ---
    skip = set(BAY_GROUPS['+12VA'] + BAY_GROUPS['-12VA'] + BAY_GROUPS['+5VA'])
    skip |= {'U105:3', 'U108:3', 'C106', 'U101'}
    for key in sorted(sh.inst):
        if key in skip or sh.lib[sh.uuid_of[key]].startswith('power:'):
            continue
        ref = key.split(':')[0]
        for num, p_ in sorted(sh.unit_pins(key).items(), key=lambda kv: int(kv[0])):
            net = pinmap.get((ref, num))
            if net not in RAILS:
                continue
            ox, oy, _ = sh.origin(key)
            sgn = -1 if p_[0] < ox else 1
            rotated = sh.lib[sh.uuid_of[key]] in ('Device:C', 'Device:R') \
                and sh.origin(key)[2] in (90, 270)
            tx = g(p_[0] + (10.16 if rotated and net == 'GND' else sgn * 5.08))
            ty = g(p_[1] + (2.54 if net != 'GND' else -2.54)) \
                if sh.lib[sh.uuid_of[key]] == 'Device:D_Schottky' else \
                (p_[1] if net != 'GND' else g(p_[1] + 3.81))
            sym(net, p_, (tx, ty))
    print(f'  power symbols placed: {counter[0]} (reused {17 - len(reuse)})')


def place_nc(r, ed, sh, ncbase):
    n = 0
    for _old, hit in ncbase:
        if not hit:
            continue
        key, num = hit
        if key not in sh.inst:
            continue
        ed.append(nc_block(sh.pin(key, num)))
        n += 1
    print(f'  no_connect markers placed: {n}')


def place_labels(r, ed, sh, pinmap, offsheet):
    """Global labels only for baseline off-sheet nets; local for VCM/AIN taps."""
    ng = nl = 0
    for key, s in sorted(sh.inst.items()):
        if sh.lib[sh.uuid_of[key]].startswith('power:'):
            continue
        ref = key.split(':')[0]
        ox, oy, _ = sh.origin(key)
        for num, p in sorted(sh.unit_pins(key).items(), key=lambda kv: int(kv[0])):
            net = pinmap.get((ref, num))
            if net is None:
                continue
            base = net.split('/')[-1]
            if net in offsheet:
                dx = p[0] - ox
                sgn = 1 if dx >= 0 else -1
                ang = 0 if sgn > 0 else 180
                tip = (g(p[0] + sgn * 5.08), p[1])
                r.w(p, tip)
                ed.append(label_block('global_label', net, tip, ang))
                ng += 1
            elif base == 'ADC_VCM':
                sgn = -1 if p[0] < ox else 1
                tip = (g(p[0] + sgn * 5.08), p[1])
                r.w(p, tip)
                ed.append(label_block('label', 'ADC_VCM', tip,
                                      0 if sgn > 0 else 180))
                nl += 1
            elif base.startswith('AIN') and ref == 'U101':
                ed.append(label_block('label', base, p, 180))
                nl += 1
    # lane-end AIN taps, one per differential cap
    for lane in LANES:
        p = lane['refs']
        for cap, net in (('Com', lane['refs']['ain'] + '+'), ('Co2', lane['refs']['ain'] + '-')):
            pt = sh.pin(p[cap], 1 if cap == 'Com' else 1)
            ed.append(label_block('label', net, pt, 0))
            nl += 1
    for cap, net in (('Com', 'AIN0+'), ('Co2', 'AIN0-')):
        pt = sh.pin(CH0['refs'][cap], 1)
        ed.append(label_block('label', net, pt, 0))
        nl += 1
    # ADC reference tap at the chain (matches U101 REF pins)
    ed.append(label_block('label', 'ADC_REF', sh.pin('D534', 2), 0))
    nl += 1
    print(f'  global labels: {ng}  local labels: {nl}')


# ---------------------------------------------------------------------------
# lib_symbols additions for the four rail power symbols
# ---------------------------------------------------------------------------
def _lib_symbols_end(text):
    """Index just past the closing parenthesis of (lib_symbols ...)."""
    i = text.index('(lib_symbols')
    depth, j, quoted = 0, i, False
    while j < len(text):
        c = text[j]
        if quoted:
            if c == '\\':
                j += 2
                continue
            if c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return j  # index of the closing ')' of lib_symbols
        j += 1
    raise ValueError('unbalanced lib_symbols')


def add_lib_symbols(text):
    root = H.parse(text)
    libs = H.child(root, 'lib_symbols')
    have = {s[1] for s in H.children(libs, 'symbol')}
    # Copy the symbols verbatim from the installed KiCad power library so ERC's
    # lib_symbol_mismatch check sees the stock definitions.
    power_sheet = Path('/usr/share/kicad/symbols/power.kicad_sym').read_text()
    need = ['power:+5VA', 'power:+12VA', 'power:+3.3V', 'power:-12VA']
    added = []
    for name in need:
        if name in have:
            continue
        template = name.split(':')[1]
        s = power_sheet.index(f'(symbol "{template}"')
        depth, j, quoted = 0, s, False
        while j < len(power_sheet):
            c = power_sheet[j]
            if quoted:
                if c == '\\':
                    j += 2
                    continue
                if c == '"':
                    quoted = False
            elif c == '"':
                quoted = True
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    e = j + 1
                    break
            j += 1
        else:
            raise KeyError(template)
        blk = power_sheet[s:e]
        blk = blk.replace(f'(symbol "{template}"', f'(symbol "{name}"', 1)
        idx = _lib_symbols_end(text)
        text = text[:idx] + '\n\t\t' + blk + text[idx:]
        added.append(name)
    print(f'  added lib_symbols: {added}')
    return text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
NOTE_POS = {
    'Pen 1 | INA163': (90.17, 163.83),
    'Ch0 unity-gain': (199.85, 262.89),
    'Ch2 is wired': (199.85, 270.51),
    'Ch2 | PEN2': (92.71, 277.99),
    'Ch3 | REF_COIL': (94.85, 365.76),
    'Reference fed': (429.26, 462.28),
    'R184 isolates': (429.26, 469.90),
    '+5VA source': (429.26, 477.52),
}


def move_notes(ed):
    """Move the free-text notes off the signal runs (grid-snapped)."""
    blocks = list(H.top_blocks(ed.t, 'text'))
    for start, end, _name in reversed(blocks):
        blk = ed.t[start:end]
        m = re.search(r'\(text "([^"]*)"', blk)
        if not m:
            continue
        key = next((k for k in NOTE_POS if blk.startswith(f'(text "{k}')), None)
        if key is None:
            continue
        x, y = NOTE_POS[key]
        at = re.search(r'\(at [\d.-]+ [\d.-]+', blk)
        blk = blk[:at.start()] + f'(at {f(x)} {f(y)}' + blk[at.end():]
        ed.t = ed.t[:start] + blk + ed.t[end:]


def regenerate(text):
    _U[0] = 0
    base_sh = Sheet(text)
    # placement must be applied before pin coordinates are queried
    ed = Editor(text)
    for key, (x, y, rot) in PLACE.items():
        if key not in base_sh.inst:
            raise KeyError(f'no baseline instance for {key}')
        x, y = g(x), g(y)
        u = base_sh.uuid_of[key]
        ed.move_symbol(u, x, y, rot)
        # Fields are never inside a body outline.  For a rotated passive the
        # KiCad field angle is set to 90 so the composed text stays horizontal,
        # and the anchors are offset along x with outward justification.
        if rot in (90, 270):
            ed.move_prop(u, 'Reference', g(x - 7.62), g(y - 3.81),
                         justify='right', angle=90)
            ed.move_prop(u, 'Value', g(x + 7.62), g(y + 3.81),
                         justify='left', angle=90)
        elif key.startswith('U105:') or key.startswith('U108:'):
            ed.move_prop(u, 'Reference', g(x - 20.32), g(y - 10.16),
                         justify='right')
            ed.move_prop(u, 'Value', g(x + 20.32), g(y + 10.16),
                         justify='left')
        elif base_sh.lib[base_sh.uuid_of[key]] == 'Device:D_Schottky':
            ed.move_prop(u, 'Reference', g(x - 15.24), y)
            ed.move_prop(u, 'Value', g(x + 15.24), y)
        elif key in ('U104', 'U106', 'U107'):
            ed.move_prop(u, 'Reference', x, g(y - 15.24))
            ed.move_prop(u, 'Value', x, g(y + 15.24))
        elif key == 'U101':
            ed.move_prop(u, 'Reference', g(x + 55.88), g(y - 73.66))
            ed.move_prop(u, 'Value', g(x + 55.88), g(y - 69.85))
        elif key in ('U102', 'U103'):
            ed.move_prop(u, 'Reference', x, g(y - 10.16))
            ed.move_prop(u, 'Value', x, g(y + 10.16))
        else:
            ed.move_prop(u, 'Reference', x, g(y - 6.35))
            ed.move_prop(u, 'Value', x, g(y + 6.35))
    text = ed.t
    sh = Sheet(text)
    pinmap = pin_net_map()
    ncbase = baseline_nc_pins(base_sh)

    ed = Editor(text)
    ed.strip(['wire', 'label', 'global_label', 'hierarchical_label',
              'junction', 'no_connect'])
    r = Router(ed, sh)
    route_ch0(r)
    for lane in LANES:
        route_lane(r, lane, base_sh)
    route_reference(r)
    route_adc(r)
    place_power(r, ed, sh, pinmap, ncbase, base_sh)
    place_nc(r, ed, sh, ncbase)
    offsheet = {l['text'] for l in H.labels(base_sh.root, 'global_label')
                if l['text'] not in RAILS}
    place_labels(r, ed, sh, pinmap, offsheet)
    move_notes(ed)
    text = add_lib_symbols(ed.t)
    return text


def main():
    args = sys.argv[1:]
    if '--check' in args:
        cur = SHEET.read_text()
        out = regenerate(base_text())
        print('IDEMPOTENT' if cur == out else 'DIFFERS')
        return 0 if cur == out else 1
    out = regenerate(base_text())
    if SHEET.exists() and SHEET.read_text() == out:
        print('no change (idempotent)')
    else:
        SHEET.write_text(out)
        print(f'wrote {SHEET}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
