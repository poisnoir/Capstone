# BRD-01 receiver reference — component → pins → wires (receiver sheet only)

> **⚠ STALE TABLES — DO NOT USE AS WIRING TRUTH (2026-11-26).** Every table
> below was generated from the `ef04f63` netlist. Commit `8d39a99` and the
> subsequent BRD-01 ERC/receiver commits through `41e3d2e` changed that
> netlist: `/power/BUCK1_FB` → `Net-(U144-FB)`,
> `/receiver/DREGCAP` → `Net-(U101-DREGCAP)`,
> `/receiver/FDA1_N` → `Net-(U105B--IN2)`,
> `/receiver/REF_RAW` → `Net-(U102-VOUT)`,
> `/receiver/REGCAPA` → `Net-(U101-REGCAPA)`,
> `/receiver/REGCAPB` → `Net-(U101-REGCAPB)`, and the 10 Ω ADC-reference
> filter resistor `R184` → `R186` (U103 OUT/IN- → `/receiver/ADC_REF`). Net
> names, part designators and the crossing/sheet classification below may have
> changed. Regenerate before relying on any table here:
> `kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch`.

**Provenance (2026-11-26; tables generated 2026-11-25 from base commit `ef04f63`):** generated with `kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch` (KiCad 10.0.8); the committed netlist changed at `8d39a99` (see banner), so these tables describe `ef04f63` only — regenerate before using them as wiring truth.
This is the **component-centric** reference for BRD-01. Its companion,
`brd01_wiring_manifest.md` (and `brd01_wiring_manifest.csv`), is **net-centric**:
net → pins. This document starts at a component and follows each pin to the other
ends of its wire. It does not duplicate the manifest's net tables; where a net has
more than eight ends it shows the nearest few and points to the manifest section
for that sheet.

Everything in Part 4 and Part 5 below is generated, not transcribed: the source is
`kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch`
(KiCad 10.0.8 Eeschema). `<comp>` supplies ref/value/footprint/libsource/sheet,
`<node>` supplies pin number, `pinfunction`, `pintype` and net membership, and
`<sheetpath names=...>` supplies the sheet. Pin coordinates for the nearest-end
ordering come from `tools/kicad_span_report.py:pin_map()`. Parts 2 and 3 are
hand-written from git history and repo evidence, as requested.

Baseline counted here: **640 components, 605 nets, 2155 node pins**; ERC was
re-run on this checkout and reports **0 errors / 0 warnings** (`Found 0
violations`). The last commit before this reference is `213ac41`
(`docs(brd-01): generate wiring manifest from netlist`).

---

Provenance: this is a receiver-sheet-only extract of `docs/phase2/brd01_component_reference.md` (its §4.1, §4.4 and §5.4 are reproduced verbatim below, stale-data banner included). Its net-centric counterpart for this sheet is `brd01_wiring_manifest.md` §3.4 (net → pins).

## How to read it

### 4.1 How to read it

- One entry per component, grouped by sheet, with ICs / modules / connectors / test points first, then transistors and diodes, then two-pin passives (R, C, L).
- `Connects to` lists the **other ends of the same net**, nearest-first by pin coordinates on the same sheet (netlist order for off-sheet pins). Nets with more than eight ends show the six nearest and the total, with a pointer to the manifest section for that sheet. A no-connect shows `no-connect (single pin)`.
- Role of a supporting passive: **primary rule** — an R/C/L is listed on a component when its supporting net (the functional net of the two, else the supply rail, else GND) touches that component's supply, set, feedback, bias or enable pin (pin name classified by the patterns in §4.1.1). Rail decoupling is attributed to every same-sheet component with a supply pin on that rail (listing is capped per component), since every rail cap otherwise applies to every IC on the board. **Secondary rule** — a passive with no primary host is attached to the nearest same-sheet component sharing one of its nets, with a filter / termination role, so that every passive has a stated host. A passive may legitimately serve more than one component (rail decoupling); it is then listed on each.
- Footprints are the netlist `<footprint>` strings. Values are netlist `<value>` strings; DNP status is a BOM decision, not a netlist property (see Part B item 13).

#### 4.1.1 Pin-role patterns (the classification rule)

| Class | Pin-name patterns | Typical role assigned |
|---|---|---|
| feedback | `FB`, `VOS`, `COMP`, `SENSE`, `PGFB`, `DEF` | feedback divider / filter |
| set | `SET`, `ILIM`, `RT`, `FSW`, `TRIM`, `GAIN`, `RG1/2`, `FORMAT`, `CLK_SEL`, `M0..M2` | gain / timing set |
| bias | `SS/TR`, `NR`, `BIAS`, `CBOOT`, `RBOOT`, `VOCM`, `VCM`, `REF`, `DREGCAP`, `CT` | soft-start / bias / reference |
| enable | `EN`, `EN/SYNC`, `EN/UV`, `MR`, `RESET`, `CLR`, `PRE`, `SHDN`, `OE`, `START`, `DISABLE`, `HALT` | enable / sequencing pull-up |
| supply | `VIN`, `VCC`, `VDD`, `VLDOIN`, `VOUT`, `VBUS`, `V+`, `V-`, `IN`, `OUT`, `SW`, `GND`, `AGND`, `AVSS`, `VCCO`, `EP`, shield | decoupling / bulk / feed |

Signals not in any class (data, analog inputs, clocks) are not "support" pins; their R/C/L neighbours fall through to the secondary rule.

## Component reference

### 4.4 Page 4 — receiver

Net-centric counterpart: `brd01_wiring_manifest.md` §3.4. 107 components on this sheet.

#### Components

#### U101 — AD7768-4BSTZ-RL7, AD7768-4BSTZ

Sheet: receiver (4) · Footprint: Package_QFP:LQFP-64_10x10mm_P0.5mm · 64 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | AIN1-_1 | input | `/receiver/AIN1-` | R125.2, C127.2, C126.1 |
| 2 | AIN1+_2 | input | `/receiver/AIN1+` | R124.2, C127.1, C125.1 |
| 3 | AVSS1A_3 | power_in | `GND` | U101.55, U101.46, U101.33, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | AVDD1A_4 | power_in | `+5VA` | U101.45, U101.60, U101.53, C107.1, C108.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | REF1-_5 | input | `GND` | U101.44, U101.31, U101.58, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 6 | REF1+_6 | input | `/receiver/ADC_REF` | U101.43, C102.1, R184.2, C101.1, D534.2 |
| 7 | AVSS_7 | power_in | `GND` | U101.8, U101.51, U101.62, U101.9, U101.10, U101.46 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 8 | AVSS_8 | power_in | `GND` | U101.7, U101.9, U101.51, U101.10, U101.62, U101.39 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 9 | AVSS_9 | power_in | `GND` | U101.10, U101.8, U101.39, U101.7, U101.40, U101.51 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | AVSS_10 | power_in | `GND` | U101.39, U101.9, U101.40, U101.8, U101.41, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | FILTER/GPIO4_11 | bidirectional | `/receiver/ADC_SPI_STRAP` | R180.2 |
| 12 | MODE0/GPIO0_12 | bidirectional+no_connect | `unconnected-(U101-MODE0/GPIO0-Pad12)` | — (no other pins on this net) |
| 13 | MODE1/GPIO1_13 | bidirectional+no_connect | `unconnected-(U101-MODE1/GPIO1-Pad13)` | — (no other pins on this net) |
| 14 | MODE2/GPIO2_14 | bidirectional+no_connect | `unconnected-(U101-MODE2/GPIO2-Pad14)` | — (no other pins on this net) |
| 15 | MODE3/GPIO3_15 | bidirectional+no_connect | `unconnected-(U101-MODE3/GPIO3-Pad15)` | — (no other pins on this net) |
| 16 | ST0/~{CS}_16 | input | `ADC_CS` | R164.2, U4.B12 |
| 17 | SCLK_17 | input | `ADC_SCLK` | U4.A13 |
| 18 | DEC1/SDI_18 | input | `ADC_SDI` | U4.A12 |
| 19 | DEC0/SDO_19 | bidirectional | `ADC_SDO` | U4.B11 |
| 20 | DNC/DGND_20 | passive+no_connect | `unconnected-(U101-DNC/DGND-Pad20)` | — (no other pins on this net) |
| 21 | DIN_21 | input | `/receiver/ADC_DAISY_IN` | R181.1 |
| 22 | DNC_22 | no_connect | `unconnected-(U101-DNC-Pad22)` | — (no other pins on this net) |
| 23 | DNC_23 | no_connect | `unconnected-(U101-DNC-Pad23)` | — (no other pins on this net) |
| 24 | DOUT3_24 | output | `ADC_DOUT3` | U4.A10 |
| 25 | DOUT2_25 | output | `ADC_DOUT2` | U4.B9 |
| 26 | DOUT1_26 | output | `ADC_DOUT1` | U4.A9 |
| 27 | DOUT0_27 | output | `ADC_DOUT0` | U4.A8 |
| 28 | DCLK_28 | output | `ADC_DCLK` | U4.C11 |
| 29 | ~{DRDY}_29 | output | `ADC_DRDY_N` | U4.B10 |
| 30 | ~{RESET}_30 | input | `ADC_RESET_N` | R163.2, U4.A14 |
| 31 | XTAL1_31 | input | `GND` | U101.44, U101.58, U101.5, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 32 | XTAL2/MCLK_32 | input | `/receiver/MCLK` | R100.2 |
| 33 | DGND_33 | power_in | `GND` | U101.55, U101.3, U101.46, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 34 | DREGCAP_34 | power_out | `/receiver/DREGCAP` | C103.1 |
| 35 | IOVDD_35 | power_in | `+3.3V` | C111.1, U101.57, R180.1, C140.1, C141.1, C142.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 36 | SYNC_IN_36 | input | `ADC_SYNC_IN` | R166.2, U4.C14 |
| 37 | ~{START}_37 | input | `ADC_START_N` | R165.2, U4.B14 |
| 38 | SYNC_OUT_38 | output | `ADC_SYNC_OUT` | U4.A15 |
| 39 | AVSS_39 | power_in | `GND` | U101.10, U101.40, U101.9, U101.41, U101.42, U101.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 40 | AVSS_40 | power_in | `GND` | U101.39, U101.41, U101.10, U101.42, U101.54, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 41 | AVSS_41 | power_in | `GND` | U101.42, U101.40, U101.54, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 42 | AVSS_42 | power_in | `GND` | U101.41, U101.54, U101.40, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 43 | REF2+_43 | input | `/receiver/ADC_REF` | U101.6, C102.1, R184.2, C101.1, D534.2 |
| 44 | REF2-_44 | input | `GND` | U101.31, U101.5, U101.58, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 45 | AVDD1B_45 | power_in | `+5VA` | U101.4, U101.60, U101.53, C108.1, C107.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 46 | AVSS1B_46 | power_in | `GND` | U101.3, U101.62, U101.51, U101.55, U101.33, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 47 | AIN3+_47 | input | `/receiver/AIN3+` | C564.1, C566.1, R572.2 |
| 48 | AIN3-_48 | input | `/receiver/AIN3-` | C566.2, C565.1, R573.2 |
| 49 | AIN2+_49 | input | `/receiver/AIN2+` | C544.1, C546.1, R552.2 |
| 50 | AIN2-_50 | input | `/receiver/AIN2-` | C546.2, C545.1, R553.2 |
| 51 | AVSS2B_51 | power_in | `GND` | U101.62, U101.7, U101.46, U101.8, U101.3, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 52 | REGCAPB_52 | power_out | `/receiver/REGCAPB` | C105.1 |
| 53 | AVDD2B_53 | power_in | `+5VA` | U101.60, U101.45, U101.4, C110.1, C109.1, C108.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 54 | AVSS_54 | power_in | `GND` | U101.42, U101.41, U101.40, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 55 | DGND_55 | power_in | `GND` | U101.3, U101.33, U101.46, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 56 | FORMAT0_56 | input | `GND` | U101.58, U101.31, U101.44, U101.5, U101.3, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 57 | PIN/SPI_57 | input | `+3.3V` | U101.35, C111.1, R180.1, C140.1, C141.1, C142.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 58 | CLK_SEL_58 | input | `GND` | U101.31, U101.44, U101.56, U101.5, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 59 | VCM_59 | output | `/receiver/ADC_VCM` | C106.1, U108.17, U105.11, U105.17, U108.11 |
| 60 | AVDD2A_60 | power_in | `+5VA` | U101.45, U101.53, U101.4, C109.1, C108.1, C110.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 61 | REGCAPA_61 | power_out | `/receiver/REGCAPA` | C104.1 |
| 62 | AVSS2A_62 | power_in | `GND` | U101.51, U101.46, U101.7, U101.3, U101.8, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 63 | AIN0-_63 | input | `/receiver/AIN0-` | C121.1, R115.2, C122.2 |
| 64 | AIN0+_64 | input | `/receiver/AIN0+` | C120.1, R114.2, C122.1 |

Supporting passives:

- enable pull-up: R163 (10k) on `ADC_RESET_N`
- enable pull-up: R165 (10k) on `ADC_START_N`
- filter capacitor to ground: C544 (470p), C545 (470p), C564 (470p), C565 (470p) on `GND`
- input / output filter capacitor: C122 (100p) on `/receiver/AIN0-`
- input / output filter capacitor: C127 (100p) on `/receiver/AIN1-`
- input / output filter capacitor: C546 (100p) on `/receiver/AIN2-`
- input / output filter capacitor: C566 (100p) on `/receiver/AIN3-`
- pull-down resistor: R181 (10k) on `/receiver/ADC_DAISY_IN`
- pull-up resistor: R180 (10k) on `/receiver/ADC_SPI_STRAP`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- soft-start / bias capacitor: C103 (10u) on `/receiver/DREGCAP`
- soft-start / bias capacitor: C104 (1u) on `/receiver/REGCAPA`
- soft-start / bias capacitor: C105 (1u) on `/receiver/REGCAPB`
- supply decoupling: C111 (100n) on `+3.3V`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`

#### U102 — ADR434BRZ

Sheet: receiver (4) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | DNC_1 | no_connect | `unconnected-(U102-DNC-Pad1)` | — (no other pins on this net) |
| 2 | VIN_2 | power_in | `+12VA` | C130.1, U103.5, C100.1, U104.11, U106.11, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 3 | NIC_3 | no_connect | `unconnected-(U102-NIC-Pad3)` | — (no other pins on this net) |
| 4 | GND_4 | power_in | `GND` | C130.2, C131.2, C120.2, C101.2, C102.2, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | TRIM_5 | passive+no_connect | `unconnected-(U102-TRIM-Pad5)` | — (no other pins on this net) |
| 6 | VOUT_6 | power_out | `/receiver/REF_RAW` | C131.1, U103.3 |
| 7 | COMP_7 | passive+no_connect | `unconnected-(U102-COMP-Pad7)` | — (no other pins on this net) |
| 8 | DNC_8 | no_connect | `unconnected-(U102-DNC-Pad8)` | — (no other pins on this net) |

Supporting passives:

- filter capacitor to ground: C101 (10u), C102 (100n), C120 (470p), C121 (470p) on `GND`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C131 (100n) on `/receiver/REF_RAW`

#### U103 — OPA192IDBVR

Sheet: receiver (4) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/receiver/REF_BUF_OUT` | U103.4, R184.1 |
| 2 | V-_2 | power_in | `GND` | C106.2, C103.2, C104.2, C105.2, C131.2, C107.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 3 | IN+_3 | input | `/receiver/REF_RAW` | U102.6, C131.1 |
| 4 | IN-_4 | input | `/receiver/REF_BUF_OUT` | U103.1, R184.1 |
| 5 | V+_5 | power_in | `+12VA` | U102.2, C130.1, C100.1, U104.11, U106.11, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply feed / filter: R184 (10) on `/receiver/REF_BUF_OUT`

#### U104 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U104-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U104-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/GAIN1` | R105.1 |
| 4 | IN-_4 | input | `/receiver/INA_IN_N` | R104.1, C114.2 |
| 5 | IN+_5 | input | `/receiver/INA_IN_P` | R103.1, C113.2 |
| 6 | V-_6 | power_in | `-12VA` | C116.1, D104.2, D102.2, D523.2, U106.6, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U104-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U104-SENSE)` | U104.9, R120.1 |
| 9 | VO_9 | output | `Net-(U104-SENSE)` | U104.8, R120.1 |
| 10 | REF_10 | input | `GND` | C116.2, C115.2, R121.1, R111.1, R104.2, R103.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | C115.1, D103.1, D101.1, U106.11, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/GAIN2` | R105.2 |
| 13 | NC_13 | no_connect | `unconnected-(U104-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U104-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R103 (10k 0.1%) on `/receiver/INA_IN_P`
- pull-down resistor: R104 (10k 0.1%), R111 (1k), R121 (499) on `GND`
- series / termination resistor: R105 (176) on `/receiver/GAIN2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U105 — ADA4940-2ACPZ

Sheet: receiver (4) · Footprint: Package_CSP:LFCSP-24-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 25 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | -IN1_1 | input | `/receiver/FDA0_N` | R113.2, R111.2 |
| 2 | +FB1_2 | passive | `/receiver/FDA0_OUT_P` | U105.18, R113.1, R114.1 |
| 3 | +VS1_3 | power_in | `+5VA` | U105.20, U105.4, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | +VS1_4 | power_in | `+5VA` | U105.3, U105.20, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | -FB2_5 | passive | `/receiver/FDA1_OUT_N` | U105.13, R122.1, R125.1 |
| 6 | +IN2_6 | input | `Net-(U105B-+IN2)` | R122.2, R120.2 |
| 7 | -IN2_7 | input | `/receiver/FDA1_N` | R123.2, R121.2 |
| 8 | +FB2_8 | passive | `/receiver/FDA1_OUT_P` | U105.12, R123.1, R124.1 |
| 9 | +VS2_9 | power_in | `+5VA` | U105.14, U105.10, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | +VS2_10 | power_in | `+5VA` | U105.9, U105.14, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | VOCM2_11 | input | `/receiver/ADC_VCM` | U105.17, U108.17, U101.59, C106.1, U108.11 |
| 12 | +OUT2_12 | output | `/receiver/FDA1_OUT_P` | U105.8, R123.1, R124.1 |
| 13 | -OUT2_13 | output | `/receiver/FDA1_OUT_N` | U105.5, R122.1, R125.1 |
| 14 | ~{DISABLE2}_14 | input | `+5VA` | U105.9, U105.10, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 15 | -VS2_15 | power_in | `GND` | U105.16, U105.22, U105.21, R121.1, R111.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 16 | -VS2_16 | power_in | `GND` | U105.15, U105.22, U105.21, R121.1, R111.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 17 | VOCM1_17 | input | `/receiver/ADC_VCM` | U105.11, U108.17, U101.59, C106.1, U108.11 |
| 18 | +OUT1_18 | output | `/receiver/FDA0_OUT_P` | U105.2, R113.1, R114.1 |
| 19 | -OUT1_19 | output | `/receiver/FDA0_OUT_N` | U105.23, R112.1, R115.1 |
| 20 | ~{DISABLE1}_20 | input | `+5VA` | U105.3, U105.4, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 21 | -VS1_21 | power_in | `GND` | U105.22, U105.15, U105.16, R111.1, R121.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 22 | -VS1_22 | power_in | `GND` | U105.21, U105.15, U105.16, R111.1, R121.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 23 | -FB1_23 | passive | `/receiver/FDA0_OUT_N` | U105.19, R112.1, R115.1 |
| 24 | +IN1_24 | input | `Net-(U105A-+IN1)` | R112.2, R110.2 |
| 25 | EP_25 | passive | `GND` | U108.25, C130.2, C120.2, C101.2, U102.4, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- enable / sequencing network: C190 (47u / 16V X7R) on `+5VA`
- feedback divider: R115 (20) on `/receiver/FDA0_OUT_N`
- feedback divider: R113 (1k), R114 (20) on `/receiver/FDA0_OUT_P`
- feedback divider: R125 (20) on `/receiver/FDA1_OUT_N`
- feedback divider: R123 (1k), R124 (20) on `/receiver/FDA1_OUT_P`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`
- supply feed / filter: R110 (1k), R112 (1k) on `Net-(U105A-+IN1)`
- supply feed / filter: R120 (499), R122 (1k) on `Net-(U105B-+IN2)`

#### U106 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U106-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U106-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/PEN2_RG1` | R544.1 |
| 4 | IN-_4 | input | `/receiver/PEN2_IN_N` | C541.2, R543.1 |
| 5 | IN+_5 | input | `/receiver/PEN2_IN_P` | R542.1, C540.2 |
| 6 | V-_6 | power_in | `-12VA` | D523.2, C543.1, D521.2, D533.2, U107.6, U104.6 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U106-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U106-SENSE)` | U106.9, R548.1 |
| 9 | VO_9 | output | `Net-(U106-SENSE)` | U106.8, R548.1 |
| 10 | REF_10 | input | `GND` | R549.1, U108.21, U108.22, C543.2, C542.2, R542.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | D522.1, C542.1, U107.11, U104.11, D532.1, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/PEN2_RG2` | R544.2 |
| 13 | NC_13 | no_connect | `unconnected-(U106-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U106-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R543 (10k 0.1%) on `/receiver/PEN2_IN_N`
- pull-down resistor: R542 (10k 0.1%) on `/receiver/PEN2_IN_P`
- pull-down resistor: R549 (499) on `GND`
- series / termination resistor: R544 (176) on `/receiver/PEN2_RG2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U107 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U107-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U107-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/REF_COIL_RG1` | R564.1 |
| 4 | IN-_4 | input | `/receiver/REF_COIL_IN_N` | C561.2, R563.1 |
| 5 | IN+_5 | input | `/receiver/REF_COIL_IN_P` | R562.1, C560.2 |
| 6 | V-_6 | power_in | `-12VA` | D533.2, C563.1, D531.2, U106.6, C543.1, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U107-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U107-SENSE)` | U107.9, R568.1 |
| 9 | VO_9 | output | `Net-(U107-SENSE)` | U107.8, R568.1 |
| 10 | REF_10 | input | `GND` | R569.1, U108.15, U108.16, C563.2, C562.2, R562.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | D532.1, C562.1, U106.11, D530.1, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/REF_COIL_RG2` | R564.2 |
| 13 | NC_13 | no_connect | `unconnected-(U107-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U107-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R563 (10k 0.1%) on `/receiver/REF_COIL_IN_N`
- pull-down resistor: R562 (10k 0.1%) on `/receiver/REF_COIL_IN_P`
- pull-down resistor: R569 (499) on `GND`
- series / termination resistor: R564 (176) on `/receiver/REF_COIL_RG2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U108 — ADA4940-2ACPZ

Sheet: receiver (4) · Footprint: Package_CSP:LFCSP-24-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 25 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | -IN1_1 | input | `/receiver/FDA2_N` | R551.2, R549.2 |
| 2 | +FB1_2 | passive | `/receiver/FDA2_OUT_P` | U108.18, R551.1, R552.1 |
| 3 | +VS1_3 | power_in | `+5VA` | U108.4, U108.20, U105.10, U108.14, U108.9, U105.9 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | +VS1_4 | power_in | `+5VA` | U108.3, U108.20, U108.14, U108.9, U105.10, U108.10 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | -FB2_5 | passive | `/receiver/FDA3_OUT_N` | U108.13, R570.1, R573.1 |
| 6 | +IN2_6 | input | `Net-(U108B-+IN2)` | R570.2, R568.2 |
| 7 | -IN2_7 | input | `/receiver/FDA3_N` | R571.2, R569.2 |
| 8 | +FB2_8 | passive | `/receiver/FDA3_OUT_P` | U108.12, R571.1, R572.1 |
| 9 | +VS2_9 | power_in | `+5VA` | U108.14, U108.10, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | +VS2_10 | power_in | `+5VA` | U108.9, U108.14, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | VOCM2_11 | input | `/receiver/ADC_VCM` | U108.17, U105.11, U101.59, C106.1, U105.17 |
| 12 | +OUT2_12 | output | `/receiver/FDA3_OUT_P` | U108.8, R571.1, R572.1 |
| 13 | -OUT2_13 | output | `/receiver/FDA3_OUT_N` | U108.5, R570.1, R573.1 |
| 14 | ~{DISABLE2}_14 | input | `+5VA` | U108.9, U108.10, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 15 | -VS2_15 | power_in | `GND` | U108.16, R569.1, U107.10, C563.2, U108.22, U108.21 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 16 | -VS2_16 | power_in | `GND` | U108.15, R569.1, U107.10, C563.2, U108.22, U108.21 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 17 | VOCM1_17 | input | `/receiver/ADC_VCM` | U105.11, U108.11, U105.17, U101.59, C106.1 |
| 18 | +OUT1_18 | output | `/receiver/FDA2_OUT_P` | U108.2, R551.1, R552.1 |
| 19 | -OUT1_19 | output | `/receiver/FDA2_OUT_N` | U108.23, R550.1, R553.1 |
| 20 | ~{DISABLE1}_20 | input | `+5VA` | U108.3, U108.4, U105.10, U105.9, U105.14, U108.14 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 21 | -VS1_21 | power_in | `GND` | U108.22, R549.1, U106.10, C543.2, C125.2, U105.16 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 22 | -VS1_22 | power_in | `GND` | U108.21, R549.1, U106.10, C543.2, C125.2, R569.1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 23 | -FB1_23 | passive | `/receiver/FDA2_OUT_N` | U108.19, R550.1, R553.1 |
| 24 | +IN1_24 | input | `Net-(U108A-+IN1)` | R550.2, R548.2 |
| 25 | EP_25 | passive | `GND` | U105.25, C130.2, C101.2, C120.2, U102.4, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- enable / sequencing network: C190 (47u / 16V X7R) on `+5VA`
- feedback divider: R553 (20) on `/receiver/FDA2_OUT_N`
- feedback divider: R551 (1k), R552 (20) on `/receiver/FDA2_OUT_P`
- feedback divider: R573 (20) on `/receiver/FDA3_OUT_N`
- feedback divider: R571 (1k), R572 (20) on `/receiver/FDA3_OUT_P`
- filter capacitor to ground: C125 (470p), C126 (470p) on `GND`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`
- supply feed / filter: R548 (499), R550 (1k) on `Net-(U108A-+IN1)`
- supply feed / filter: R568 (499), R570 (1k) on `Net-(U108B-+IN2)`

#### D101 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | D103.1, C115.1, U104.11, D520.1, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN1_PROT_P` | D102.1, R101.2, C113.1 |

Supporting passives:

- series / termination resistor: R101 (100) on `/receiver/PEN1_PROT_P`

#### D102 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN1_PROT_P` | D101.2, C113.1, R101.2 |
| 2 | A_2 | passive | `-12VA` | D104.2, C116.1, U104.6, D521.2, D523.2, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- input / output filter capacitor: C113 (10u) on `/receiver/PEN1_PROT_P`

#### D103 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | D101.1, C115.1, D520.1, D522.1, U104.11, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN1_PROT_N` | D104.1, R102.2, C114.1 |

Supporting passives:

- series / termination resistor: R102 (100) on `/receiver/PEN1_PROT_N`

#### D104 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN1_PROT_N` | D103.2, C114.1, R102.2 |
| 2 | A_2 | passive | `-12VA` | D102.2, C116.1, U104.6, D521.2, D523.2, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- input / output filter capacitor: C114 (10u) on `/receiver/PEN1_PROT_N`

#### D520 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C542.1, D522.1, D103.1, D530.1, D101.1, D532.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN2_PROT_P` | C540.1, R540.2, D521.1 |

Supporting passives:

- input / output filter capacitor: C540 (10u) on `/receiver/PEN2_PROT_P`
- series / termination resistor: R540 (100) on `/receiver/PEN2_PROT_P`

#### D521 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN2_PROT_P` | D520.2, R540.2, C540.1 |
| 2 | A_2 | passive | `-12VA` | C543.1, D523.2, U106.6, D104.2, D531.2, D102.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D522 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C542.1, D520.1, U106.11, D532.1, D103.1, C562.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN2_PROT_N` | D523.1, R541.2, C541.1 |

Supporting passives:

- input / output filter capacitor: C541 (10u) on `/receiver/PEN2_PROT_N`
- series / termination resistor: R541 (100) on `/receiver/PEN2_PROT_N`

#### D523 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN2_PROT_N` | D522.2, R541.2, C541.1 |
| 2 | A_2 | passive | `-12VA` | C543.1, U106.6, D521.2, C116.1, U104.6, D533.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D530 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C562.1, D532.1, C542.1, D520.1, D522.1, U107.11 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/REF_COIL_PROT_P` | C560.1, R560.2, D531.1 |

Supporting passives:

- input / output filter capacitor: C560 (10u) on `/receiver/REF_COIL_PROT_P`
- series / termination resistor: R560 (100) on `/receiver/REF_COIL_PROT_P`

#### D531 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/REF_COIL_PROT_P` | D530.2, R560.2, C560.1 |
| 2 | A_2 | passive | `-12VA` | C563.1, D533.2, U107.6, C543.1, D521.2, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D532 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C562.1, D530.1, U107.11, C542.1, D522.1, U106.11 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/REF_COIL_PROT_N` | D533.1, R561.2, C561.1 |

Supporting passives:

- input / output filter capacitor: C561 (10u) on `/receiver/REF_COIL_PROT_N`
- series / termination resistor: R561 (100) on `/receiver/REF_COIL_PROT_N`

#### D533 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/REF_COIL_PROT_N` | D532.2, R561.2, C561.1 |
| 2 | A_2 | passive | `-12VA` | C563.1, U107.6, D531.2, U106.6, C543.1, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D534 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+5VA` | C128.1, U101.4, C112.1, U101.45, C107.1, U101.60 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/ADC_REF` | C102.1, C101.1, R184.2, U101.6, U101.43 |

#### C100 — 100n, C

C100 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C101 — 10u, C

C101 — 10u, C_1206_3216Metric — `/receiver/ADC_REF` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C102 — 100n, C

C102 — 100n, C_0603_1608Metric — `/receiver/ADC_REF` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C103 — 10u, C

C103 — 10u, C_1206_3216Metric — `/receiver/DREGCAP` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C104 — 1u, C

C104 — 1u, C_0805_2012Metric — `/receiver/REGCAPA` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C105 — 1u, C

C105 — 1u, C_0805_2012Metric — `/receiver/REGCAPB` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C106 — 100n, C

C106 — 100n, C_0603_1608Metric — `/receiver/ADC_VCM` ↔ `GND` — soft-start / bias capacitor for U101, U105, U108 (pin 1 → 2).

#### C107 — 100n, C

C107 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C108 — 100n, C

C108 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C109 — 100n, C

C109 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C110 — 100n, C

C110 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C111 — 100n, C

C111 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U101, U142, U751, U753, Y1 (pin 1 → 2).

#### C112 — 10u, C

C112 — 10u, C_1206_3216Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C113 — 10u, C

C113 — 10u, C_1206_3216Metric — `/receiver/PEN1_PROT_P` ↔ `/receiver/INA_IN_P` — input / output filter capacitor for D102 (pin 1 → 2).

#### C114 — 10u, C

C114 — 10u, C_1206_3216Metric — `/receiver/PEN1_PROT_N` ↔ `/receiver/INA_IN_N` — input / output filter capacitor for D104 (pin 1 → 2).

#### C115 — 100n, C

C115 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C116 — 100n, C

C116 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C120 — 470p, C

C120 — 470p, C_0603_1608Metric — `/receiver/AIN0+` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C121 — 470p, C

C121 — 470p, C_0603_1608Metric — `/receiver/AIN0-` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C122 — 100p, C

C122 — 100p, C_0603_1608Metric — `/receiver/AIN0+` ↔ `/receiver/AIN0-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C123 — 100n, C

C123 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C125 — 470p, C

C125 — 470p, C_0603_1608Metric — `/receiver/AIN1+` ↔ `GND` — filter capacitor to ground for U108 (pin 1 → 2).

#### C126 — 470p, C

C126 — 470p, C_0603_1608Metric — `/receiver/AIN1-` ↔ `GND` — filter capacitor to ground for U108 (pin 1 → 2).

#### C127 — 100p, C

C127 — 100p, C_0603_1608Metric — `/receiver/AIN1+` ↔ `/receiver/AIN1-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C128 — 100n, C

C128 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C130 — 100n, C

C130 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C131 — 100n, C

C131 — 100n, C_0603_1608Metric — `/receiver/REF_RAW` ↔ `GND` — supply decoupling for U102 (pin 1 → 2).

#### C540 — 10u, C

C540 — 10u, C_1206_3216Metric — `/receiver/PEN2_PROT_P` ↔ `/receiver/PEN2_IN_P` — input / output filter capacitor for D520 (pin 1 → 2).

#### C541 — 10u, C

C541 — 10u, C_1206_3216Metric — `/receiver/PEN2_PROT_N` ↔ `/receiver/PEN2_IN_N` — input / output filter capacitor for D522 (pin 1 → 2).

#### C542 — 100n, C

C542 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C543 — 100n, C

C543 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C544 — 470p, C

C544 — 470p, C_0603_1608Metric — `/receiver/AIN2+` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C545 — 470p, C

C545 — 470p, C_0603_1608Metric — `/receiver/AIN2-` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C546 — 100p, C

C546 — 100p, C_0603_1608Metric — `/receiver/AIN2+` ↔ `/receiver/AIN2-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C547 — 100n, C

C547 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C560 — 10u, C

C560 — 10u, C_1206_3216Metric — `/receiver/REF_COIL_PROT_P` ↔ `/receiver/REF_COIL_IN_P` — input / output filter capacitor for D530 (pin 1 → 2).

#### C561 — 10u, C

C561 — 10u, C_1206_3216Metric — `/receiver/REF_COIL_PROT_N` ↔ `/receiver/REF_COIL_IN_N` — input / output filter capacitor for D532 (pin 1 → 2).

#### C562 — 100n, C

C562 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C563 — 100n, C

C563 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C564 — 470p, C

C564 — 470p, C_0603_1608Metric — `/receiver/AIN3+` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C565 — 470p, C

C565 — 470p, C_0603_1608Metric — `/receiver/AIN3-` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C566 — 100p, C

C566 — 100p, C_0603_1608Metric — `/receiver/AIN3+` ↔ `/receiver/AIN3-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C567 — 100n, C

C567 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### R100 — 33, R

R100 — 33, R_0603_1608Metric — `CLOCK_32M768` ↔ `/receiver/MCLK` — enable / sequencing network, supply feed / filter for U4, Y1 (pin 1 → 2).

#### R101 — 100, R

R101 — 100, R_0603_1608Metric — `PEN1_P` ↔ `/receiver/PEN1_PROT_P` — series / termination resistor for D101 (pin 1 → 2).

#### R102 — 100, R

R102 — 100, R_0603_1608Metric — `PEN1_N` ↔ `/receiver/PEN1_PROT_N` — series / termination resistor for D103 (pin 1 → 2).

#### R103 — 10k 0.1%, R

R103 — 10k 0.1%, R_0603_1608Metric — `/receiver/INA_IN_P` ↔ `GND` — pull-down resistor for U104 (pin 1 → 2).

#### R104 — 10k 0.1%, R

R104 — 10k 0.1%, R_0603_1608Metric — `/receiver/INA_IN_N` ↔ `GND` — pull-down resistor for U104 (pin 1 → 2).

#### R105 — 176, R

R105 — 176, R_0603_1608Metric — `/receiver/GAIN1` ↔ `/receiver/GAIN2` — series / termination resistor for U104 (pin 1 → 2).

#### R110 — 1k, R

R110 — 1k, R_0603_1608Metric — `CURRENT_SUM` ↔ `Net-(U105A-+IN1)` — supply feed / filter for U105 (pin 1 → 2).

#### R111 — 1k, R

R111 — 1k, R_0603_1608Metric — `GND` ↔ `/receiver/FDA0_N` — pull-down resistor for U104 (pin 1 → 2).

#### R112 — 1k, R

R112 — 1k, R_0603_1608Metric — `/receiver/FDA0_OUT_N` ↔ `Net-(U105A-+IN1)` — supply feed / filter for U105 (pin 1 → 2).

#### R113 — 1k, R

R113 — 1k, R_0603_1608Metric — `/receiver/FDA0_OUT_P` ↔ `/receiver/FDA0_N` — feedback divider for U105 (pin 1 → 2).

#### R114 — 20, R

R114 — 20, R_0603_1608Metric — `/receiver/FDA0_OUT_P` ↔ `/receiver/AIN0+` — feedback divider for U105 (pin 1 → 2).

#### R115 — 20, R

R115 — 20, R_0603_1608Metric — `/receiver/FDA0_OUT_N` ↔ `/receiver/AIN0-` — feedback divider for U105 (pin 1 → 2).

#### R120 — 499, R

R120 — 499, R_0603_1608Metric — `Net-(U104-SENSE)` ↔ `Net-(U105B-+IN2)` — supply feed / filter for U105 (pin 1 → 2).

#### R121 — 499, R

R121 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA1_N` — pull-down resistor for U104 (pin 1 → 2).

#### R122 — 1k, R

R122 — 1k, R_0603_1608Metric — `/receiver/FDA1_OUT_N` ↔ `Net-(U105B-+IN2)` — supply feed / filter for U105 (pin 1 → 2).

#### R123 — 1k, R

R123 — 1k, R_0603_1608Metric — `/receiver/FDA1_OUT_P` ↔ `/receiver/FDA1_N` — feedback divider for U105 (pin 1 → 2).

#### R124 — 20, R

R124 — 20, R_0603_1608Metric — `/receiver/FDA1_OUT_P` ↔ `/receiver/AIN1+` — feedback divider for U105 (pin 1 → 2).

#### R125 — 20, R

R125 — 20, R_0603_1608Metric — `/receiver/FDA1_OUT_N` ↔ `/receiver/AIN1-` — feedback divider for U105 (pin 1 → 2).

#### R180 — 10k, R

R180 — 10k, R_0603_1608Metric — `+3.3V` ↔ `/receiver/ADC_SPI_STRAP` — pull-up resistor for U101 (pin 1 → 2).

#### R181 — 10k, R

R181 — 10k, R_0603_1608Metric — `/receiver/ADC_DAISY_IN` ↔ `GND` — pull-down resistor for U101 (pin 1 → 2).

#### R184 — 10, R

R184 — 10, R_0603_1608Metric — `/receiver/REF_BUF_OUT` ↔ `/receiver/ADC_REF` — supply feed / filter for U103 (pin 1 → 2).

#### R540 — 100, R

R540 — 100, R_0603_1608Metric — `PEN2_P` ↔ `/receiver/PEN2_PROT_P` — series / termination resistor for D520 (pin 1 → 2).

#### R541 — 100, R

R541 — 100, R_0603_1608Metric — `PEN2_N` ↔ `/receiver/PEN2_PROT_N` — series / termination resistor for D522 (pin 1 → 2).

#### R542 — 10k 0.1%, R

R542 — 10k 0.1%, R_0603_1608Metric — `/receiver/PEN2_IN_P` ↔ `GND` — pull-down resistor for U106 (pin 1 → 2).

#### R543 — 10k 0.1%, R

R543 — 10k 0.1%, R_0603_1608Metric — `/receiver/PEN2_IN_N` ↔ `GND` — pull-down resistor for U106 (pin 1 → 2).

#### R544 — 176, R

R544 — 176, R_0603_1608Metric — `/receiver/PEN2_RG1` ↔ `/receiver/PEN2_RG2` — series / termination resistor for U106 (pin 1 → 2).

#### R548 — 499, R

R548 — 499, R_0603_1608Metric — `Net-(U106-SENSE)` ↔ `Net-(U108A-+IN1)` — supply feed / filter for U108 (pin 1 → 2).

#### R549 — 499, R

R549 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA2_N` — pull-down resistor for U106 (pin 1 → 2).

#### R550 — 1k, R

R550 — 1k, R_0603_1608Metric — `/receiver/FDA2_OUT_N` ↔ `Net-(U108A-+IN1)` — supply feed / filter for U108 (pin 1 → 2).

#### R551 — 1k, R

R551 — 1k, R_0603_1608Metric — `/receiver/FDA2_OUT_P` ↔ `/receiver/FDA2_N` — feedback divider for U108 (pin 1 → 2).

#### R552 — 20, R

R552 — 20, R_0603_1608Metric — `/receiver/FDA2_OUT_P` ↔ `/receiver/AIN2+` — feedback divider for U108 (pin 1 → 2).

#### R553 — 20, R

R553 — 20, R_0603_1608Metric — `/receiver/FDA2_OUT_N` ↔ `/receiver/AIN2-` — feedback divider for U108 (pin 1 → 2).

#### R560 — 100, R

R560 — 100, R_0603_1608Metric — `REF_COIL_P` ↔ `/receiver/REF_COIL_PROT_P` — series / termination resistor for D530 (pin 1 → 2).

#### R561 — 100, R

R561 — 100, R_0603_1608Metric — `REF_COIL_N` ↔ `/receiver/REF_COIL_PROT_N` — series / termination resistor for D532 (pin 1 → 2).

#### R562 — 10k 0.1%, R

R562 — 10k 0.1%, R_0603_1608Metric — `/receiver/REF_COIL_IN_P` ↔ `GND` — pull-down resistor for U107 (pin 1 → 2).

#### R563 — 10k 0.1%, R

R563 — 10k 0.1%, R_0603_1608Metric — `/receiver/REF_COIL_IN_N` ↔ `GND` — pull-down resistor for U107 (pin 1 → 2).

#### R564 — 176, R

R564 — 176, R_0603_1608Metric — `/receiver/REF_COIL_RG1` ↔ `/receiver/REF_COIL_RG2` — series / termination resistor for U107 (pin 1 → 2).

#### R568 — 499, R

R568 — 499, R_0603_1608Metric — `Net-(U107-SENSE)` ↔ `Net-(U108B-+IN2)` — supply feed / filter for U108 (pin 1 → 2).

#### R569 — 499, R

R569 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA3_N` — pull-down resistor for U107 (pin 1 → 2).

#### R570 — 1k, R

R570 — 1k, R_0603_1608Metric — `/receiver/FDA3_OUT_N` ↔ `Net-(U108B-+IN2)` — supply feed / filter for U108 (pin 1 → 2).

#### R571 — 1k, R

R571 — 1k, R_0603_1608Metric — `/receiver/FDA3_OUT_P` ↔ `/receiver/FDA3_N` — feedback divider for U108 (pin 1 → 2).

#### R572 — 20, R

R572 — 20, R_0603_1608Metric — `/receiver/FDA3_OUT_P` ↔ `/receiver/AIN3+` — feedback divider for U108 (pin 1 → 2).

#### R573 — 20, R

R573 — 20, R_0603_1608Metric — `/receiver/FDA3_OUT_N` ↔ `/receiver/AIN3-` — feedback divider for U108 (pin 1 → 2).


## Dependency summary

## 5. Per-sheet support summary

Page 1 — root has no components, so no support rows.

Component → the passives that exist to serve it. `—` means no R/C/L was found by either rule on that sheet. Counts are per component, not per net.


### 5.4 receiver

| Component | Passives that serve it |
|---|---|
| U101 | enable pull-up: R163 (10k) on ADC_RESET_N; enable pull-up: R165 (10k) on ADC_START_N; filter capacitor to ground: C544 (470p), C545 (470p), C564 (470p), C565 (470p) on GND; input / output filter capacitor: C122 (100p) on /receiver/AIN0-; input / output filter capacitor: C127 (100p) on /receiver/AIN1-; input / output filter capacitor: C546 (100p) on /receiver/AIN2-; input / output filter capacitor: C566 (100p) on /receiver/AIN3-; pull-down resistor: R181 (10k) on /receiver/ADC_DAISY_IN; pull-up resistor: R180 (10k) on /receiver/ADC_SPI_STRAP; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; soft-start / bias capacitor: C103 (10u) on /receiver/DREGCAP; soft-start / bias capacitor: C104 (1u) on /receiver/REGCAPA; soft-start / bias capacitor: C105 (1u) on /receiver/REGCAPB; supply decoupling: C111 (100n) on +3.3V; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA |
| U102 | filter capacitor to ground: C101 (10u), C102 (100n), C120 (470p), C121 (470p) on GND; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C131 (100n) on /receiver/REF_RAW |
| U103 | supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply feed / filter: R184 (10) on /receiver/REF_BUF_OUT |
| U104 | pull-down resistor: R103 (10k 0.1%) on /receiver/INA_IN_P; pull-down resistor: R104 (10k 0.1%), R111 (1k), R121 (499) on GND; series / termination resistor: R105 (176) on /receiver/GAIN2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U105 | enable / sequencing network: C190 (47u / 16V X7R) on +5VA; feedback divider: R115 (20) on /receiver/FDA0_OUT_N; feedback divider: R113 (1k), R114 (20) on /receiver/FDA0_OUT_P; feedback divider: R125 (20) on /receiver/FDA1_OUT_N; feedback divider: R123 (1k), R124 (20) on /receiver/FDA1_OUT_P; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA; supply feed / filter: R110 (1k), R112 (1k) on Net-(U105A-+IN1); supply feed / filter: R120 (499), R122 (1k) on Net-(U105B-+IN2) |
| U106 | pull-down resistor: R543 (10k 0.1%) on /receiver/PEN2_IN_N; pull-down resistor: R542 (10k 0.1%) on /receiver/PEN2_IN_P; pull-down resistor: R549 (499) on GND; series / termination resistor: R544 (176) on /receiver/PEN2_RG2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U107 | pull-down resistor: R563 (10k 0.1%) on /receiver/REF_COIL_IN_N; pull-down resistor: R562 (10k 0.1%) on /receiver/REF_COIL_IN_P; pull-down resistor: R569 (499) on GND; series / termination resistor: R564 (176) on /receiver/REF_COIL_RG2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U108 | enable / sequencing network: C190 (47u / 16V X7R) on +5VA; feedback divider: R553 (20) on /receiver/FDA2_OUT_N; feedback divider: R551 (1k), R552 (20) on /receiver/FDA2_OUT_P; feedback divider: R573 (20) on /receiver/FDA3_OUT_N; feedback divider: R571 (1k), R572 (20) on /receiver/FDA3_OUT_P; filter capacitor to ground: C125 (470p), C126 (470p) on GND; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA; supply feed / filter: R548 (499), R550 (1k) on Net-(U108A-+IN1); supply feed / filter: R568 (499), R570 (1k) on Net-(U108B-+IN2) |
| D101 | series / termination resistor: R101 (100) on /receiver/PEN1_PROT_P |
| D102 | input / output filter capacitor: C113 (10u) on /receiver/PEN1_PROT_P |
| D103 | series / termination resistor: R102 (100) on /receiver/PEN1_PROT_N |
| D104 | input / output filter capacitor: C114 (10u) on /receiver/PEN1_PROT_N |
| D520 | input / output filter capacitor: C540 (10u) on /receiver/PEN2_PROT_P; series / termination resistor: R540 (100) on /receiver/PEN2_PROT_P |
| D521 | — |
| D522 | input / output filter capacitor: C541 (10u) on /receiver/PEN2_PROT_N; series / termination resistor: R541 (100) on /receiver/PEN2_PROT_N |
| D523 | — |
| D530 | input / output filter capacitor: C560 (10u) on /receiver/REF_COIL_PROT_P; series / termination resistor: R560 (100) on /receiver/REF_COIL_PROT_P |
| D531 | — |
| D532 | input / output filter capacitor: C561 (10u) on /receiver/REF_COIL_PROT_N; series / termination resistor: R561 (100) on /receiver/REF_COIL_PROT_N |
| D533 | — |
| D534 | — |
