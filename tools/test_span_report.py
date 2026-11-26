#!/usr/bin/env python3
"""Self-check for tools/kicad_span_report.py (stdlib only, no test framework).

    python3 tools/test_span_report.py

Builds tiny synthetic sheets/netlists in a temp dir: a known two-pin-net span,
a multi-unit part whose duplicate pin must be de-duplicated, rail exclusion,
and the in-block / cross-block / hub / moved-block gate rules. Exits non-zero
on any failed assertion.
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

        # 4. An in-block worse net gates CI even if the total improves.
        before = d / 'before.kicad_sch'
        after = d / 'after.kicad_sch'
        blocksfile = d / 'blocks.csv'
        blocksfile.write_text('BIG 0,0,100,100\n')
        blocks = S.load_blocks(blocksfile)
        before.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                                + inst('R2', 'test:R', 30.5, 10, 1, ['1', '2'])))
        after.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                               + inst('R2', 'test:R', 50, 10, 1, ['1', '2'])))
        xmlfile.write_text(netlist([('SIG', [('R1', '1'), ('R2', '2')])], ['R1', 'R2']))
        cmp = S.compare(before, after, xmlfile, xmlfile, None, None,
                        None, False, 0.0, blocks)
        row = cmp['rows'][0]
        check(row['status'] == 'worsened' and row['delta'] == 19.5,
              'compare flags a moved pin as worsened by 19.50 mm')
        check(row['klass'] == 'in-block' and cmp['summary']['inblock_regressions'] == 1,
              'declared block makes the net in-block')
        with contextlib.redirect_stdout(io.StringIO()):
            rc = S.main(['--compare', str(before), str(after),
                         '--netlist-before', str(xmlfile),
                         '--netlist-after', str(xmlfile),
                         '--blocks', str(blocksfile),
                         '--fail-on-regression', '--json'])
        check(rc == 1, '--fail-on-regression exits 1 on an in-block regression')

        # 5. In-block hop > 25.4 mm is flagged; inference reports itself.
        hopfile = d / 'hop.kicad_sch'
        hopfile.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1'])
                                 + inst('R2', 'test:R', 45, 10, 1, ['2'])))
        hopxml = d / 'hop.xml'
        hopxml.write_text(netlist([('HOP', [('R1', '1'), ('R2', '2')])], ['R1', 'R2']))
        res = S.report(hopfile, hopxml, None, None, None, False, blocks)
        check(res['rows'][0]['klass'] == 'in-block' and res['rows'][0]['hop'],
              'in-block span of 35.00 mm gets W6-HOP')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            S.show_report(res)
        check('W6-HOP' in out.getvalue(), 'report prints W6-HOP')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            inferred = S.report(hopfile, hopxml, None, None, None, False)
            check(inferred['blocks_source'].startswith('inferred'),
                  'omitting --blocks infers blocks from symbol positions')
            S.show_report(inferred)
        check('inferred' in out.getvalue(),
              'report states clearly that blocks were inferred')

        # 6. A cross-block net touching a declared hub is INFO, not a warning.
        blocksfile.write_text('A 0,0,60,60\nB 60,0,160,60\n')
        blocks = S.load_blocks(blocksfile)
        hubfile = d / 'hub.kicad_sch'
        hubfile.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1'])
                                 + inst('U1', 'test:R', 100, 10, 1, ['2'])))
        hubxml = d / 'hub.xml'
        hubxml.write_text(netlist([('TO_HUB', [('R1', '1'), ('U1', '2')])],
                                  ['R1', 'U1']))
        hubs = S.parse_hubs('U1')
        res = S.report(hubfile, hubxml, None, None, None, False, blocks, hubs)
        m = res['rows'][0]
        check(m['klass'] == 'cross-block' and m['hub'] and not m['hop'],
              'hub net is cross-block and INFO, not W6-HOP')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            S.show_report(res)
        check('INFO (shared-hub cross-block)' in out.getvalue(),
              'report prints INFO (shared-hub cross-block)')

        # 7. Cross-block growth never fails; membership changes always print.
        xbefore = d / 'xb.kicad_sch'
        xafter = d / 'xa.kicad_sch'
        xbefore.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                                 + inst('U1', 'test:R', 100, 10, 1, ['2'])
                                 + inst('R2', 'test:R', 45, 10, 1, ['1'])))
        xafter.write_text(sheet(lib, inst('R1', 'test:R', 10, 10, 1, ['1', '2'])
                                + inst('U1', 'test:R', 110, 10, 1, ['2'])
                                + inst('R2', 'test:R', 70, 10, 1, ['1'])))
        xxml = d / 'x.xml'
        xxml.write_text(netlist([('TO_HUB', [('R1', '1'), ('U1', '2')]),
                                 ('MOVED', [('R1', '2'), ('R2', '1')])],
                                ['R1', 'U1', 'R2']))
        args = ['--compare', str(xbefore), str(xafter),
                '--netlist-before', str(xxml), '--netlist-after', str(xxml),
                '--blocks', str(blocksfile), '--hubs', 'U1',
                '--fail-on-regression']
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = S.main(args)
        check(rc == 0, 'cross-block growth does not fail the gate')
        text = out.getvalue()
        check('MOVED BLOCK MOVED: in-block [A] -> cross-block [A, B]' in text,
              'block-membership change prints as MOVED BLOCK even when gate passes')
        cmp = S.compare(xbefore, xafter, xxml, xxml, None, None, None, False,
                        0.0, blocks, hubs)
        check(cmp['summary']['worsened'] >= 1
              and cmp['summary']['inblock_regressions'] == 0,
              'cross-block regression is counted but not gated')

    print('all checks passed')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
