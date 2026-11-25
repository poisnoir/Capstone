#!/usr/bin/env python3
"""Self-check for tools/kicad_span_report.py (stdlib only, no test framework).

    python3 tools/test_span_report.py

Builds three tiny synthetic sheets/netlists in a temp dir: a known two-pin-net
span, a multi-unit part whose duplicate pin must be de-duplicated, and rail
exclusion. Exits non-zero on any failed assertion.
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kicad_span_report as S  # noqa: E402


def pin(num, x, y):
    return (f'(pin passive line (at {x} {y} 0) (length 1.27) '
            f'(name "P{num}" (effects (font (size 1 1)))) '
            f'(number "{num}" (effects (font (size 1 1)))))')


def inst(ref, lib, x, y, unit, pins):
    decl = ' '.join(f'(pin "{p}" (uuid "u-{ref}-{p}-{unit}"))' for p in pins)
    return (f'(symbol (lib_id "{lib}") (at {x} {y} 0) (unit {unit}) '
            f'(uuid "i-{ref}-{unit}") (property "Reference" "{ref}" (at {x} {y} 0)) '
            f'{decl})')


def sheet(library, symbols, extra=''):
    return ('(kicad_sch (version 20250114) (generator "selftest") '
            '(uuid "root") (paper "A4") '
            f'(lib_symbols {library}) {symbols} {extra})')


def netlist(nets, refs):
    nodes = ''.join(f'<net code="{i}" name="{name}">'
                    + ''.join(f'<node ref="{r}" pin="{p}"/>' for r, p in nodes_)
                    + '</net>' for i, (name, nodes_) in enumerate(nets, 1))
    comps = ''.join(f'<comp ref="{r}"><value>V</value>'
                    f'<property name="Sheetfile" value="sheet.kicad_sch"/>'
                    f'<sheetpath names="/"/></comp>' for r in refs)
    return f'<export>{nodes}{comps}</export>'


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print(f'ok - {msg}')


def main():
    with tempfile.TemporaryDirectory(prefix='span-selftest-') as td:
        d = Path(td)
        sheetfile = d / 'sheet.kicad_sch'
        xmlfile = d / 'net.xml'

        # 1. Two-part net with known coordinates: (10,10) -> (30.5,7.46).
        lib = f'(symbol "test:R" (symbol "R_1_1" {pin(1, 0, 0)} {pin(2, 0, 2.54)}))'
        syms = inst('R1', 'test:R', 10, 10, 1, ['1', '2']) + \
               inst('R2', 'test:R', 30.5, 10, 1, ['1', '2'])
        sheetfile.write_text(sheet(lib, syms))
        xmlfile.write_text(netlist([('SIG', [('R1', '1'), ('R2', '2')])], ['R1', 'R2']))
        res = S.report(sheetfile, xmlfile, None, None, None, False)
        m = res['rows'][0]
        check((m['w'], m['h'], m['s']) == (20.5, 2.54, 23.04),
              'known two-part span 20.50 x 2.54, S 23.04')

        # 2. Multi-unit part: pin 1 exists in units 1 and 2 at different
        #    coordinates; only the pin declared by unit 1 may be counted.
        lib2 = (f'(symbol "test:R" (symbol "R_1_1" {pin(1, 0, 0)} {pin(2, 0, 2.54)}))'
                + '(symbol "test:DUAL" '
                f'(symbol "DUAL_1_1" {pin(1, 0, 0)} {pin(2, 0, 2.54)}) '
                f'(symbol "DUAL_2_1" {pin(1, 0, 5.08)} {pin(3, 0, 7.62)}))')
        syms2 = (inst('U1', 'test:DUAL', 10, 10, 1, ['1', '2'])
                 + inst('U1', 'test:DUAL', 50, 10, 2, ['1', '3'])
                 + inst('R1', 'test:R', 10, 10, 1, ['1']))
        sheetfile.write_text(sheet(lib2, syms2))
        xmlfile.write_text(netlist([
            ('DEDUPE', [('U1', '1'), ('R1', '1')]),
            ('UNIT2', [('U1', '3'), ('R1', '1')]),
        ], ['U1', 'R1']))
        pm = S.pin_map(sheetfile)
        check(len([k for k in pm if k[0] == 'U1']) == 3,
              'multi-unit U1 contributes 3 pins, not 4')
        check(pm[('U1', '1')][1:3] == (10.0, 10.0),
              'U1 pin 1 resolves to the unit that declares it (10.00, 10.00)')
        rows = {r['name']: r for r in S.report(sheetfile, xmlfile, None, None,
                                               None, False)['rows']}
        check(rows['DEDUPE']['w'] == 0 and rows['DEDUPE']['h'] == 0,
              'de-duplicated pin gives zero span to a coincident net')
        check(rows['UNIT2']['w'] == 40,
              'unit-2-only pin still resolves at its own coordinate')

        # 3. Rails excluded by name and by power: symbol value; count printed.
        sheetfile.write_text(sheet(lib2, syms2, '(lib_id "power:+5V")'))
        xmlfile.write_text(netlist([
            ('SIG', [('U1', '1'), ('R1', '1')]),
            ('GND', [('U1', '2'), ('R1', '1')]),
            ('+3.3V', [('U1', '3'), ('R1', '1')]),
            ('+5V', [('R1', '1'), ('R1', '2')]),
        ], ['U1', 'R1']))
        res = S.report(sheetfile, xmlfile, None, None, None, False)
        check(res['rails'] == 3, '3 rails excluded (GND, +3.3V, +5V)')
        check([r['name'] for r in res['rows']] == ['SIG'],
              'rail exclusion leaves only SIG')
        res_all = S.report(sheetfile, xmlfile, None, None, None, True)
        check(len(res_all['rows']) == 4, '--include-rails restores all 4 nets')

        # 4. A worse net is reported and gates CI even if the total improves.
        before = d / 'before.kicad_sch'
        after = d / 'after.kicad_sch'
        before.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                                + inst('R2', 'test:R', 30.5, 10, 1, ['1', '2'])))
        after.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                               + inst('R2', 'test:R', 50, 10, 1, ['1', '2'])))
        xmlfile.write_text(netlist([('SIG', [('R1', '1'), ('R2', '2')])], ['R1', 'R2']))
        cmp = S.compare(before, after, xmlfile, xmlfile, None, None,
                        None, False, 0.0)
        row = cmp['rows'][0]
        check(row['status'] == 'worsened' and row['delta'] == 19.5,
              'compare flags a moved pin as worsened by 19.50 mm')
        with contextlib.redirect_stdout(io.StringIO()):
            rc = S.main(['--compare', str(before), str(after),
                         '--netlist-before', str(xmlfile),
                         '--netlist-after', str(xmlfile),
                         '--fail-on-regression', '--json'])
        check(rc == 1, '--fail-on-regression exits 1 on a regression')

    print('all checks passed')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
