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
| BAY | 609.60,25.40 – 736.60,76.20 | C100, C112, C115, C116, C123, C128, C130, C542, C543, C547, C562, C563, C567, U105 unit 3, U108 unit 3 | — |

Decoupling bay: `(609.60, 25.40, 736.60, 76.20)` mm, 5 columns × 3 rows at
25.4 × 15.24 mm pitch. It keeps ≥ 5.08 mm clear of CH0 (starts y 76.20),
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
| final | — | — | 13498.83 → 12586.97 mm (−911.86 mm) | G1/G2/G3/G4 pass; G5 fails on 35 residual in-block nets (see below) |

## Spans (`kicad_span_report.py --compare`, declared blocks)

- in-block ΣS **13498.83 → 12586.97 mm** (−911.86 mm); 30 improved, 27 unchanged.
- cross-block ΣS 3512.82 → 4307.84 mm (ungated; ADC/ADC_VCM hub growth, logged as INFO).
- `in-block regressions == 35`; `new in-block hops == 12`; `MOVED BLOCK == 34`.

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

## Net renames (26; pin membership proven identical by `kicad_netlist_compare.py`)

| baseline | after |
|---|---|
| /receiver/ADC_DAISY_IN | Net-(U101-DIN) |
| /receiver/ADC_SPI_STRAP | Net-(U101-FILTER/GPIO4) |
| /receiver/FDA0_OUT_P | Net-(U105A-+FB1) |
| /receiver/FDA1_OUT_P | Net-(U105B-+FB2) |
| /receiver/FDA2_N | Net-(U108A--IN1) |
| /receiver/FDA2_OUT_P | Net-(U108A-+FB1) |
| /receiver/FDA3_N | Net-(U108B--IN2) |
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
| Net-(U105A--FB1) | /receiver/FDA0_OUT_N |
| Net-(U105B--FB2) | /receiver/FDA1_OUT_N |

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
`receiver_page-1.png`, `overview.png` and the five `crop_*.png` files.
