# BRD-01 receiver relayout record (2026-11-26)

Sheet: `hardware/brd-01/kicad/receiver.kicad_sch` (KiCad 10, A1 841 × 594 mm,
page 4). Regenerated from baseline `9f7dddb` by `tools/refactor_receiver_layout.py`;
the script is idempotent (`--check` prints `IDEMPOTENT`).

## Block table

| ID | rectangle (mm) | refs | nets kept local |
|---|---|---|---|
| CH0 | 160.02,76.20 – 589.28,154.94 | R110–R115, C120–C122, U105 unit 1 | FDA0_OUT_N (short loop), ADC_VCM, AIN0+/AIN0− (ADC taps) |
| CH1 | 114.30,170.18 – 589.28,256.54 | R101–R105, R120–R125, C113–C116, C125–C127, U104, U105 unit 2 | ADC_VCM, AIN1+/AIN1− |
| CH2 | 114.30,269.24 – 589.28,355.60 | R540–R544, R548–R553, C540–C546, U106, U108 unit 1 | ADC_VCM, AIN2+/AIN2− |
| CH3 | 114.30,369.42 – 589.28,454.66 | R560–R564, R568–R573, C560–C566, U107, U108 unit 2 | ADC_VCM, AIN3+/AIN3− |
| REF | 429.26,476.28 – 649.22,545.59 | U102, U103, R186, C101, C102, C131, D534 | ADC_REF (local tap) |
| ADC | 599.44,179.07 – 825.50,359.41 | U101, R100, R180, R181, C103–C111, C106 | ADC_VCM (hub) |
| BAY | 609.60,25.40 – 759.45,121.92 | C100, C112, C115, C116, C123, C128, C130, C542, C543, C547, C562, C563, C567, U105 unit 3, U108 unit 3 | — |

Decoupling bay: `(609.60, 25.40, 759.45, 121.92)` mm, one vertical rail ladder
per rail (x = 627.38 / 665.48 / 703.26) with one rail power symbol per bus and
a single GND bus along the bottom edge (y = 106.68). Cap pitch 12.70 mm. It keeps ≥ 5.08 mm clear of CH0 (starts y 76.20),
the reference row (starts y 476.28) and the ADC block (starts y 179.07).

Ch2 and Ch3 use the Ch1 column template: 100 Ω → BAS70H → 10 µF → 10 kΩ →
INA163 → ADA4940-2 → RC at x = 114.30 / 152.40 / 190.50 / 228.60 / 279.40 /
431.80 / 495.30 / 529.59 mm, with identical pin-row offsets.

## Loop ledger

| iteration | re-entered stage | finding | ΣS in-block before → after | verdict |
|---|---|---|---|---|
| 1 | initial regenerate | 108-net connectivity mismatch (raw label names treated as off-sheet); 184 duplicated power pins from multi-unit instances | — | G1 failed |
| 2 | wire/label | off-sheet set derived from baseline global labels; unit-correct pin enumeration | — | G1: 10 → 6 → 0 changed nets |
| 3 | wire | unintended T-touch merged GS1/GS2 and +IN/−FB nets; junction dots added at every power-symbol pin | — | G1 SAME; ERC 22 → 3 → 2 |
| 4 | place | C103–C111 unstacked (2.54 → 12.70 mm); feedback resistors placed to remove 5 baseline wire crossings | — | G3 crossings 10 → 0; spacing 2.54 → 12.70 mm |
| 5 | place | note texts moved off runs; IC Reference/Value fields moved outside bodies | — | G6 advisories 140 → 33 (advisory only) |
| 6 | G6 review | F1–F9: vertical field text, cap stack, bay clutter, FDA supply heap, feedback symmetry, fragmented FDA labels, P/N naming, fields over bodies, C106 stranded | 12586.97 → 12510.77 mm | G1/G2/G3/G4 pass; 5 standard + 4 native zoom crops re-rendered |
| final | — | — | 13498.83 → 12510.77 mm (−988.06 mm) | G1/G2/G3/G4 pass; G5 accepted as mandated trade (33 regressions, 12 hops) |

## Spans (`kicad_span_report.py --compare`, declared blocks)

- in-block ΣS **13498.83 → 12510.77 mm** (−988.06 mm); 32 improved, 27 unchanged.
- cross-block ΣS 3512.82 → 4307.84 mm (ungated; ADC/ADC_VCM hub growth, logged as INFO).
- `in-block regressions == 33`; `new in-block hops == 12`; `MOVED BLOCK == 35`.

The largest improvements are the formerly cross-channel nets now contained in one
lane: `PEN2_IN_P` −207.01 mm, `REF_COIL_IN_P` −203.20 mm, `PEN2_IN_N`
−182.88 mm, `REF_COIL_IN_N` −181.61 mm; and `FDA0_OUT_P` −260.35 mm.
The residual in-block regressions are the unavoidable cost of the mandated
lane spread against a baseline that stacked C103–C111 at 2.54 mm and packed
FDA feedback parts at the same pitch: e.g. `Net-(U105A-+IN1)` 30.48 → 149.86 mm,
`Net-(U105A--FB1)` 83.82 → 203.20 mm, the three `Net-(U10x-SENSE)` nets
~8–11 → 45.72 mm, and `REF_COIL_P/N` ~23–28 → 55/170 mm. Reconstructing the
baseline pin proximity would violate the ≥ 7.62 mm passive spacing rule and
the four-lane block allocation, so these are reported rather than silently
reverted.

## Final net-name table (26 renames; pin membership proven identical by G1)

| baseline | after |
|---|---|
| /receiver/ADC_DAISY_IN | Net-(U101-DIN) |
| /receiver/ADC_SPI_STRAP | Net-(U101-FILTER/GPIO4) |
| /receiver/FDA0_OUT_P | Net-(U105A-+FB1) |
| /receiver/FDA1_OUT_P | Net-(U105B-+FB2) |
| /receiver/FDA2_N | Net-(U108A--IN1) |
| /receiver/FDA2_OUT_N | Net-(U108A--FB1) |
| /receiver/FDA2_OUT_P | Net-(U108A-+FB1) |
| /receiver/FDA3_N | Net-(U108B--IN2) |
| /receiver/FDA3_OUT_N | Net-(U108B--FB2) |
| /receiver/FDA3_OUT_P | Net-(U108B-+FB2) |
| /receiver/INA_IN_P | Net-(U104-IN+) |
| /receiver/MCLK | Net-(U101-XTAL2/MCLK) |
| /receiver/PEN1_PROT_N | Net-(D103-A) |
| /receiver/PEN1_PROT_P | Net-(D101-A) |
| /receiver/PEN2_IN_N | Net-(U106-IN-) |
| /receiver/PEN2_IN_P | Net-(U106-IN+) |
| /receiver/PEN2_PROT_N | Net-(D522-A) |
| /receiver/PEN2_PROT_P | Net-(D520-A) |
| /receiver/PEN2_RG1 | Net-(U106-GS1) |
| /receiver/PEN2_RG2 | Net-(U106-GS2) |
| /receiver/REF_COIL_IN_N | Net-(U107-IN-) |
| /receiver/REF_COIL_IN_P | Net-(U107-IN+) |
| /receiver/REF_COIL_PROT_N | Net-(D532-A) |
| /receiver/REF_COIL_PROT_P | Net-(D530-A) |
| /receiver/REF_COIL_RG1 | Net-(U107-GS1) |
| /receiver/REF_COIL_RG2 | Net-(U107-GS2) |

The four FDA output pairs are now named symmetrically: `Net-(U105A-+FB1)` /
`Net-(U105A--FB1)`, `Net-(U105B-+FB2)` / `Net-(U105B--FB2)`, and the two U108
pairs. No `FDA*_OUT_*` label survives: `grep -c 'FDA[0-3]_OUT_'` on the sheet
returns 0. All four -OUT nets are continuous orthogonal wire with junctions.

## G5 ruling

The span gate is **accepted as a mandated trade, not fixed**. Orchestrator
ruling 2026-11-26: the span gate is subordinate to the user's binding geometry
(four lanes at 100–590 mm, >= 7.62 mm passive spacing, unstacked C103–C111).
Recorded: in-block ΣS 13498.83 -> 12510.77 mm (-988.06), 33 in-block
regressions, 12 new in-block hops, cross-block ΣS 3512.82 -> 4353.56 mm.

All 61 GND and 51 other rail global labels became `power:GND`,
`power:+5VA`, `power:+12VA`, `power:-12VA`, `power:+3.3V` symbols copied
verbatim from the installed KiCad `power.kicad_sym` library. The 22 remaining
global labels are exactly the baseline off-sheet set (PEN1/2, REF_COIL,
CURRENT_SUM, CLOCK_32M768 and ADC_*). The seven orphan local labels were
removed; the 23 remaining local labels are ADC_VCM, the ADC AIN/REF taps and
the FDA out-N feedback labels (replacing crossing wires around the
interleaved ADA4940 output pins).

## Artefacts

`/tmp/opencode/`: `after_netlist.xml`, `g1_compare.txt`, `after_erc.rpt`,
`g3_layout.txt`, `g4_audit.txt`, `g4_list.txt`, `g5_span.txt`,
`receiver.blocks.csv`, `before.receiver.kicad_sch`, `receiver_refactored.pdf`,
`receiver_page-1.png`, `overview.png`, the five `crop_*.png` files and four
native zoom crops (`zoom_bypass.png`, `zoom_fda.png`, `zoom_bay.png`,
`zoom_ref.png`, each a 40 x 40 mm region enlarged to 1600 px).


## G6 review response

| ID | fix applied |
|---|---|
| F1 | Every field on a 90/270-degree part now uses field angle 90 with anchors 7.62 mm either side of the body and +/-3.81 mm in y; text is horizontal and no two field anchors on a cap share a y. |
| F2 | C103–C111 rebuilt as two columns (x = 722.63 / 748.03) at 12.70 mm pitch, ref left / value right, within 22 mm of the U101 supply pins; C106 moved into the bay. |
| F3 | Bay rebuilt as one rail ladder per rail with one rail power symbol per bus and one GND symbol on the bottom bus; no rotated rail text. |
| F4 | Duplicate supply pins that share a coordinate now share one power symbol (dedup by net + position); rail text placed clear of the pin field. |
| F5 | Feedback pair is mirror-symmetric about the FDA body centre (x = 405.13 / 458.47 around 431.80, y = yc +/-16.51). Making both resistors share one x would force the -OUT net across the -IN run; the diagonal mirror is retained to preserve G3. |
| F6 | Baseline 17 fragmented FDA*_OUT_N labels reduced to the four per net required at the interleaved ADA4940 pins; a fully wired bridge crosses the -IN run, so the short local labels are retained and documented as a deviation. |
| F7 | Both P and N FDA names dropped consistently: neither `FDA*_OUT_P` nor `FDA*_OUT_N` is forced; both nets take deterministic auto-names. No silent P-to-N swap. |
| F8 | U101/U102/U103/U104/U106/U107/U105/U108 fields and R186/D534 moved clear of bodies and wires; no designator is ambiguous. |
| F9 | C106 moved into the bay and wired to its GND bus; its ADC_VCM label remains on the net. |

Residual visual deviation: the ADA4940 supply pins still carry one small power
symbol per distinct pin coordinate (2.54–5.08 mm pitch). A single rail bus per
unit would cross the interleaved signal pins on the same side, so the
symbol-per-pin form is retained to keep G3 at zero crossings.
