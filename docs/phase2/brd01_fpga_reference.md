# BRD-01 fpga reference — component → pins → wires (fpga sheet only)

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

Provenance: this is a fpga-sheet-only extract of `docs/phase2/brd01_component_reference.md` (its §4.1, §4.5 and §5.5 are reproduced verbatim below, stale-data banner included). Its net-centric counterpart for this sheet is `brd01_wiring_manifest.md` §3.5 (net → pins).

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

### 4.5 Page 5 — fpga

Net-centric counterpart: `brd01_wiring_manifest.md` §3.5. 67 components on this sheet.

#### Components

#### J140 — 87831-1420, AMD_Platform_Cable_USB_II_JTAG

Sheet: fpga (5) · Footprint: accubot:Molex_87831-1420 · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | NC_1 | no_connect | `unconnected-(J140-NC-Pad1)` | — (no other pins on this net) |
| 2 | VREF_2 | passive | `+3.3V` | R148.1, U141.8, Y1.4, Y1.1, R149.1, R143.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | GND_3 | passive | `GND` | J140.5, J140.7, J140.9, J140.11, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 4 | TMS_4 | passive | `/fpga/JTAG_TMS` | U4.M7 |
| 5 | GND_5 | passive | `GND` | J140.3, J140.7, J140.9, J140.11, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 6 | TCK_6 | passive | `/fpga/JTAG_TCK` | U4.L7 |
| 7 | GND_7 | passive | `GND` | J140.5, J140.9, J140.11, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 8 | TDO_8 | passive | `/fpga/JTAG_TDO` | U4.N8 |
| 9 | GND_9 | passive | `GND` | J140.11, J140.7, J140.5, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 10 | TDI_10 | passive | `/fpga/JTAG_TDI` | U4.N7 |
| 11 | GND_11 | passive | `GND` | J140.9, J140.7, J140.5, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 12 | NC_12 | no_connect | `unconnected-(J140-NC-Pad12)` | — (no other pins on this net) |
| 13 | PGND_13 | passive+no_connect | `unconnected-(J140-PGND-Pad13)` | — (no other pins on this net) |
| 14 | HALT_14 | passive+no_connect | `unconnected-(J140-HALT-Pad14)` | — (no other pins on this net) |

Supporting passives:

- soft-start / bias capacitor: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.5) on `+3.3V`

#### TP790 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-PROGRAM_B_0)` | R144.2, U4.L9 |

Supporting passives:

- pull-up resistor: R144 (4.7k) on `Net-(U4C-PROGRAM_B_0)`

#### TP791 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-INIT_B_0)` | R142.2, U4.K10 |

Supporting passives:

- pull-up resistor: R142 (4.7k) on `Net-(U4C-INIT_B_0)`

#### TP792 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-DONE_0)` | R143.2, U4.H10 |

#### U4 — XC7A35T-1FTG256C, XC7A35T-FTG256

Sheet: fpga (5) · Footprint: Package_BGA:Xilinx_FTG256 · 256 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| A1 | GND_A1 | power_in | `GND` | U4.A11, U4.B8, U4.C5, U4.C15, U4.D2, U4.F8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A2 | IO_L8N_T1_AD14N_35_A2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8N_T1_AD14N_35-PadA2)` | — (no other pins on this net) |
| A3 | IO_L4N_T0_35_A3 | bidirectional+no_connect | `unconnected-(U4B-IO_L4N_T0_35-PadA3)` | — (no other pins on this net) |
| A4 | IO_L3N_T0_DQS_AD5N_35_A4 | bidirectional+no_connect | `unconnected-(U4B-IO_L3N_T0_DQS_AD5N_35-PadA4)` | — (no other pins on this net) |
| A5 | IO_L3P_T0_DQS_AD5P_35_A5 | bidirectional+no_connect | `unconnected-(U4B-IO_L3P_T0_DQS_AD5P_35-PadA5)` | — (no other pins on this net) |
| A6 | VCCO_35_A6 | power_in | `+3.3V` | U4.B3, U4.D7, U4.E4, U4.F1, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A7 | IO_L1N_T0_AD4N_35_A7 | bidirectional+no_connect | `unconnected-(U4B-IO_L1N_T0_AD4N_35-PadA7)` | — (no other pins on this net) |
| A8 | IO_L2P_T0_AD8P_15_A8 | bidirectional | `ADC_DOUT0` | U101.27 |
| A9 | IO_L2N_T0_AD8N_15_A9 | bidirectional | `ADC_DOUT1` | U101.26 |
| A10 | IO_L3N_T0_DQS_AD1N_15_A10 | bidirectional | `ADC_DOUT3` | U101.24 |
| A11 | GND_A11 | power_in | `GND` | U4.A1, U4.B8, U4.C5, U4.C15, U4.D2, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A12 | IO_L5N_T0_AD9N_15_A12 | bidirectional | `ADC_SDI` | U101.18 |
| A13 | IO_L7P_T1_AD2P_15_A13 | bidirectional | `ADC_SCLK` | U101.17 |
| A14 | IO_L7N_T1_AD2N_15_A14 | bidirectional | `ADC_RESET_N` | R163.2, U101.30 |
| A15 | IO_L9N_T1_DQS_AD3N_15_A15 | bidirectional | `ADC_SYNC_OUT` | U101.38 |
| A16 | VCCO_15_A16 | power_in | `+3.3V` | U4.B13, U4.C10, U4.E14, U4.H15, U4.J12, U4.T11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B1 | IO_L9N_T1_DQS_AD7N_35_B1 | bidirectional+no_connect | `unconnected-(U4B-IO_L9N_T1_DQS_AD7N_35-PadB1)` | — (no other pins on this net) |
| B2 | IO_L8P_T1_AD14P_35_B2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8P_T1_AD14P_35-PadB2)` | — (no other pins on this net) |
| B3 | VCCO_35_B3 | power_in | `+3.3V` | U4.D7, U4.A6, U4.E4, U4.F1, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B4 | IO_L4P_T0_35_B4 | bidirectional+no_connect | `unconnected-(U4B-IO_L4P_T0_35-PadB4)` | — (no other pins on this net) |
| B5 | IO_L2N_T0_AD12N_35_B5 | bidirectional+no_connect | `unconnected-(U4B-IO_L2N_T0_AD12N_35-PadB5)` | — (no other pins on this net) |
| B6 | IO_L2P_T0_AD12P_35_B6 | bidirectional+no_connect | `unconnected-(U4B-IO_L2P_T0_AD12P_35-PadB6)` | — (no other pins on this net) |
| B7 | IO_L1P_T0_AD4P_35_B7 | bidirectional+no_connect | `unconnected-(U4B-IO_L1P_T0_AD4P_35-PadB7)` | — (no other pins on this net) |
| B8 | GND_B8 | power_in | `GND` | U4.C5, U4.A11, U4.C15, U4.A1, U4.D2, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B9 | IO_L3P_T0_DQS_AD1P_15_B9 | bidirectional | `ADC_DOUT2` | U101.25 |
| B10 | IO_L4P_T0_15_B10 | bidirectional | `ADC_DRDY_N` | U101.29 |
| B11 | IO_L4N_T0_15_B11 | bidirectional | `ADC_SDO` | U101.19 |
| B12 | IO_L5P_T0_AD9P_15_B12 | bidirectional | `ADC_CS` | R164.2, U101.16 |
| B13 | VCCO_15_B13 | power_in | `+3.3V` | U4.C10, U4.A16, U4.E14, U4.H15, U4.J12, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B14 | IO_L8N_T1_AD10N_15_B14 | bidirectional | `ADC_START_N` | R165.2, U101.37 |
| B15 | IO_L9P_T1_DQS_AD3P_15_B15 | bidirectional+no_connect | `unconnected-(U4A-IO_L9P_T1_DQS_AD3P_15-PadB15)` | — (no other pins on this net) |
| B16 | IO_L10N_T1_AD11N_15_B16 | bidirectional+no_connect | `unconnected-(U4A-IO_L10N_T1_AD11N_15-PadB16)` | — (no other pins on this net) |
| C1 | IO_L9P_T1_DQS_AD7P_35_C1 | bidirectional+no_connect | `unconnected-(U4B-IO_L9P_T1_DQS_AD7P_35-PadC1)` | — (no other pins on this net) |
| C2 | IO_L7N_T1_AD6N_35_C2 | bidirectional+no_connect | `unconnected-(U4B-IO_L7N_T1_AD6N_35-PadC2)` | — (no other pins on this net) |
| C3 | IO_L7P_T1_AD6P_35_C3 | bidirectional+no_connect | `unconnected-(U4B-IO_L7P_T1_AD6P_35-PadC3)` | — (no other pins on this net) |
| C4 | IO_L12N_T1_MRCC_35_C4 | bidirectional+no_connect | `unconnected-(U4B-IO_L12N_T1_MRCC_35-PadC4)` | — (no other pins on this net) |
| C5 | GND_C5 | power_in | `GND` | U4.B8, U4.C15, U4.D2, U4.A11, U4.A1, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C6 | IO_L5N_T0_AD13N_35_C6 | bidirectional+no_connect | `unconnected-(U4B-IO_L5N_T0_AD13N_35-PadC6)` | — (no other pins on this net) |
| C7 | IO_L5P_T0_AD13P_35_C7 | bidirectional+no_connect | `unconnected-(U4B-IO_L5P_T0_AD13P_35-PadC7)` | — (no other pins on this net) |
| C8 | IO_L1P_T0_AD0P_15_C8 | bidirectional+no_connect | `unconnected-(U4A-IO_L1P_T0_AD0P_15-PadC8)` | — (no other pins on this net) |
| C9 | IO_L1N_T0_AD0N_15_C9 | bidirectional+no_connect | `unconnected-(U4A-IO_L1N_T0_AD0N_15-PadC9)` | — (no other pins on this net) |
| C10 | VCCO_15_C10 | power_in | `+3.3V` | U4.B13, U4.E14, U4.A16, U4.H15, U4.J12, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C11 | IO_L11P_T1_SRCC_15_C11 | bidirectional | `ADC_DCLK` | U101.28 |
| C12 | IO_L11N_T1_SRCC_15_C12 | bidirectional+no_connect | `unconnected-(U4A-IO_L11N_T1_SRCC_15-PadC12)` | — (no other pins on this net) |
| C13 | IO_L12N_T1_MRCC_15_C13 | bidirectional+no_connect | `unconnected-(U4A-IO_L12N_T1_MRCC_15-PadC13)` | — (no other pins on this net) |
| C14 | IO_L8P_T1_AD10P_15_C14 | bidirectional | `ADC_SYNC_IN` | R166.2, U101.36 |
| C15 | GND_C15 | power_in | `GND` | U4.C5, U4.D2, U4.B8, U4.D12, U4.A11, U4.E9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C16 | IO_L10P_T1_AD11P_15_C16 | bidirectional+no_connect | `unconnected-(U4A-IO_L10P_T1_AD11P_15-PadC16)` | — (no other pins on this net) |
| D1 | IO_L10N_T1_AD15N_35_D1 | bidirectional+no_connect | `unconnected-(U4B-IO_L10N_T1_AD15N_35-PadD1)` | — (no other pins on this net) |
| D2 | GND_D2 | power_in | `GND` | U4.C15, U4.D12, U4.C5, U4.E9, U4.B8, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D3 | IO_L11N_T1_SRCC_35_D3 | bidirectional+no_connect | `unconnected-(U4B-IO_L11N_T1_SRCC_35-PadD3)` | — (no other pins on this net) |
| D4 | IO_L12P_T1_MRCC_35_D4 | bidirectional+no_connect | `unconnected-(U4B-IO_L12P_T1_MRCC_35-PadD4)` | — (no other pins on this net) |
| D5 | IO_L6N_T0_VREF_35_D5 | bidirectional+no_connect | `unconnected-(U4B-IO_L6N_T0_VREF_35-PadD5)` | — (no other pins on this net) |
| D6 | IO_L6P_T0_35_D6 | bidirectional+no_connect | `unconnected-(U4B-IO_L6P_T0_35-PadD6)` | — (no other pins on this net) |
| D7 | VCCO_35_D7 | power_in | `+3.3V` | U4.B3, U4.E4, U4.F1, U4.A6, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D8 | IO_L6P_T0_15_D8 | bidirectional+no_connect | `unconnected-(U4A-IO_L6P_T0_15-PadD8)` | — (no other pins on this net) |
| D9 | IO_L6N_T0_VREF_15_D9 | bidirectional+no_connect | `unconnected-(U4A-IO_L6N_T0_VREF_15-PadD9)` | — (no other pins on this net) |
| D10 | IO_0_15_D10 | bidirectional+no_connect | `unconnected-(U4A-IO_0_15-PadD10)` | — (no other pins on this net) |
| D11 | IO_L14N_T2_SRCC_15_D11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14N_T2_SRCC_15-PadD11)` | — (no other pins on this net) |
| D12 | GND_D12 | power_in | `GND` | U4.E9, U4.D2, U4.C15, U4.F6, U4.F10, U4.C5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D13 | IO_L12P_T1_MRCC_15_D13 | bidirectional | `CLOCK_32M768` | Y1.3, R100.1 |
| D14 | IO_L15P_T2_DQS_15_D14 | bidirectional+no_connect | `unconnected-(U4A-IO_L15P_T2_DQS_15-PadD14)` | — (no other pins on this net) |
| D15 | IO_L15N_T2_DQS_ADV_B_15_D15 | bidirectional+no_connect | `unconnected-(U4A-IO_L15N_T2_DQS_ADV_B_15-PadD15)` | — (no other pins on this net) |
| D16 | IO_L17N_T2_A25_15_D16 | bidirectional+no_connect | `unconnected-(U4A-IO_L17N_T2_A25_15-PadD16)` | — (no other pins on this net) |
| E1 | IO_L15N_T2_DQS_35_E1 | bidirectional+no_connect | `unconnected-(U4B-IO_L15N_T2_DQS_35-PadE1)` | — (no other pins on this net) |
| E2 | IO_L10P_T1_AD15P_35_E2 | bidirectional+no_connect | `unconnected-(U4B-IO_L10P_T1_AD15P_35-PadE2)` | — (no other pins on this net) |
| E3 | IO_L11P_T1_SRCC_35_E3 | bidirectional+no_connect | `unconnected-(U4B-IO_L11P_T1_SRCC_35-PadE3)` | — (no other pins on this net) |
| E4 | VCCO_35_E4 | power_in | `+3.3V` | U4.D7, U4.F1, U4.B3, U4.J2, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E5 | IO_L13N_T2_MRCC_35_E5 | bidirectional+no_connect | `unconnected-(U4B-IO_L13N_T2_MRCC_35-PadE5)` | — (no other pins on this net) |
| E6 | IO_0_35_E6 | bidirectional+no_connect | `unconnected-(U4B-IO_0_35-PadE6)` | — (no other pins on this net) |
| E7 | CFGBVS_0_E7 | bidirectional | `/fpga/CFGBVS` | R154.2 |
| E8 | CCLK_0_E8 | bidirectional | `Net-(U4C-CCLK_0)` | R790.1 |
| E9 | GND_E9 | power_in | `GND` | U4.D12, U4.F6, U4.F10, U4.D2, U4.C15, U4.F16 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E10 | VCCBRAM_E10 | power_in | `+1V0_FPGA` | U4.F11, U4.L8, U4.K9, U4.J6, U4.H9, U4.G6 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E11 | IO_L14P_T2_SRCC_15_E11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14P_T2_SRCC_15-PadE11)` | — (no other pins on this net) |
| E12 | IO_L13P_T2_MRCC_15_E12 | bidirectional+no_connect | `unconnected-(U4A-IO_L13P_T2_MRCC_15-PadE12)` | — (no other pins on this net) |
| E13 | IO_L13N_T2_MRCC_15_E13 | bidirectional+no_connect | `unconnected-(U4A-IO_L13N_T2_MRCC_15-PadE13)` | — (no other pins on this net) |
| E14 | VCCO_15_E14 | power_in | `+3.3V` | U4.C10, U4.H15, U4.B13, U4.J12, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E15 | IO_L18N_T2_A23_15_E15 | bidirectional+no_connect | `unconnected-(U4A-IO_L18N_T2_A23_15-PadE15)` | — (no other pins on this net) |
| E16 | IO_L17P_T2_A26_15_E16 | bidirectional+no_connect | `unconnected-(U4A-IO_L17P_T2_A26_15-PadE16)` | — (no other pins on this net) |
| F1 | VCCO_35_F1 | power_in | `+3.3V` | U4.E4, U4.J2, U4.D7, U4.B3, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F2 | IO_L15P_T2_DQS_35_F2 | bidirectional+no_connect | `unconnected-(U4B-IO_L15P_T2_DQS_35-PadF2)` | — (no other pins on this net) |
| F3 | IO_L14N_T2_SRCC_35_F3 | bidirectional+no_connect | `unconnected-(U4B-IO_L14N_T2_SRCC_35-PadF3)` | — (no other pins on this net) |
| F4 | IO_L14P_T2_SRCC_35_F4 | bidirectional+no_connect | `unconnected-(U4B-IO_L14P_T2_SRCC_35-PadF4)` | — (no other pins on this net) |
| F5 | IO_L13P_T2_MRCC_35_F5 | bidirectional+no_connect | `unconnected-(U4B-IO_L13P_T2_MRCC_35-PadF5)` | — (no other pins on this net) |
| F6 | GND_F6 | power_in | `GND` | U4.F10, U4.E9, U4.F16, U4.D12, U4.G3, U4.D2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F7 | VCCINT_F7 | power_in | `+1V0_FPGA` | U4.F9, U4.G6, U4.H9, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F8 | VCCBATT_0_F8 | power_in | `GND` | U4.G7, U4.A1, U4.A11, U4.B8, U4.C5, U4.C15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F9 | VCCINT_F9 | power_in | `+1V0_FPGA` | U4.F7, U4.G6, U4.H9, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F10 | GND_F10 | power_in | `GND` | U4.F6, U4.F16, U4.E9, U4.G3, U4.D12, U4.G9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F11 | VCCBRAM_F11 | power_in | `+1V0_FPGA` | U4.E10, U4.L8, U4.K9, U4.J6, U4.H9, U4.G6 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F12 | IO_L16P_T2_A28_15_F12 | bidirectional+no_connect | `unconnected-(U4A-IO_L16P_T2_A28_15-PadF12)` | — (no other pins on this net) |
| F13 | IO_L16N_T2_A27_15_F13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16N_T2_A27_15-PadF13)` | — (no other pins on this net) |
| F14 | IO_L21N_T3_DQS_A18_15_F14 | bidirectional+no_connect | `unconnected-(U4A-IO_L21N_T3_DQS_A18_15-PadF14)` | — (no other pins on this net) |
| F15 | IO_L18P_T2_A24_15_F15 | bidirectional+no_connect | `unconnected-(U4A-IO_L18P_T2_A24_15-PadF15)` | — (no other pins on this net) |
| F16 | GND_F16 | power_in | `GND` | U4.F10, U4.G3, U4.F6, U4.G9, U4.E9, U4.G13 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G1 | IO_L17N_T2_35_G1 | bidirectional+no_connect | `unconnected-(U4B-IO_L17N_T2_35-PadG1)` | — (no other pins on this net) |
| G2 | IO_L17P_T2_35_G2 | bidirectional+no_connect | `unconnected-(U4B-IO_L17P_T2_35-PadG2)` | — (no other pins on this net) |
| G3 | GND_G3 | power_in | `GND` | U4.G9, U4.F16, U4.G13, U4.F10, U4.H6, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G4 | IO_L16N_T2_35_G4 | bidirectional+no_connect | `unconnected-(U4B-IO_L16N_T2_35-PadG4)` | — (no other pins on this net) |
| G5 | IO_L16P_T2_35_G5 | bidirectional+no_connect | `unconnected-(U4B-IO_L16P_T2_35-PadG5)` | — (no other pins on this net) |
| G6 | VCCINT_G6 | power_in | `+1V0_FPGA` | U4.F9, U4.H9, U4.F7, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G7 | GNDADC_0_G7 | power_in | `GND` | U4.F8, U4.A1, U4.A11, U4.B8, U4.C5, U4.C15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G8 | VCCADC_0_G8 | power_in | `+1V8_FPGA` | U4.L10, U4.K11, U4.J10, U4.G10, C158.1, C159.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G9 | GND_G9 | power_in | `GND` | U4.G3, U4.G13, U4.F16, U4.H6, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G10 | VCCAUX_G10 | power_in | `+1V8_FPGA` | U4.J10, U4.K11, U4.L10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G11 | IO_25_15_G11 | bidirectional+no_connect | `unconnected-(U4A-IO_25_15-PadG11)` | — (no other pins on this net) |
| G12 | IO_L19N_T3_A21_VREF_15_G12 | bidirectional+no_connect | `unconnected-(U4A-IO_L19N_T3_A21_VREF_15-PadG12)` | — (no other pins on this net) |
| G13 | GND_G13 | power_in | `GND` | U4.H6, U4.G9, U4.G3, U4.F16, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G14 | IO_L21P_T3_DQS_15_G14 | bidirectional+no_connect | `unconnected-(U4A-IO_L21P_T3_DQS_15-PadG14)` | — (no other pins on this net) |
| G15 | IO_L24N_T3_RS0_15_G15 | bidirectional+no_connect | `unconnected-(U4A-IO_L24N_T3_RS0_15-PadG15)` | — (no other pins on this net) |
| G16 | IO_L22N_T3_A16_15_G16 | bidirectional+no_connect | `unconnected-(U4A-IO_L22N_T3_A16_15-PadG16)` | — (no other pins on this net) |
| H1 | IO_L20N_T3_35_H1 | bidirectional+no_connect | `unconnected-(U4B-IO_L20N_T3_35-PadH1)` | — (no other pins on this net) |
| H2 | IO_L20P_T3_35_H2 | bidirectional+no_connect | `unconnected-(U4B-IO_L20P_T3_35-PadH2)` | — (no other pins on this net) |
| H3 | IO_L21N_T3_DQS_35_H3 | bidirectional+no_connect | `unconnected-(U4B-IO_L21N_T3_DQS_35-PadH3)` | — (no other pins on this net) |
| H4 | IO_L18N_T2_35_H4 | bidirectional+no_connect | `unconnected-(U4B-IO_L18N_T2_35-PadH4)` | — (no other pins on this net) |
| H5 | IO_L18P_T2_35_H5 | bidirectional+no_connect | `unconnected-(U4B-IO_L18P_T2_35-PadH5)` | — (no other pins on this net) |
| H6 | GND_H6 | power_in | `GND` | U4.G13, U4.G9, U4.G3, U4.F16, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H7 | VREFN_0_H7 | bidirectional | `/fpga/XADC_VNREF` | R150.1 |
| H8 | VP_0_H8 | bidirectional | `/fpga/XADC_VP` | R151.1 |
| H9 | VCCINT_H9 | power_in | `+1V0_FPGA` | U4.J6, U4.G6, U4.K9, U4.F9, U4.L8, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H10 | DONE_0_H10 | bidirectional | `Net-(U4C-DONE_0)` | TP792.1, R143.2 |
| H11 | IO_L19P_T3_A22_15_H11 | bidirectional+no_connect | `unconnected-(U4A-IO_L19P_T3_A22_15-PadH11)` | — (no other pins on this net) |
| H12 | IO_L20P_T3_A20_15_H12 | bidirectional+no_connect | `unconnected-(U4A-IO_L20P_T3_A20_15-PadH12)` | — (no other pins on this net) |
| H13 | IO_L20N_T3_A19_15_H13 | bidirectional+no_connect | `unconnected-(U4A-IO_L20N_T3_A19_15-PadH13)` | — (no other pins on this net) |
| H14 | IO_L24P_T3_RS1_15_H14 | bidirectional+no_connect | `unconnected-(U4A-IO_L24P_T3_RS1_15-PadH14)` | — (no other pins on this net) |
| H15 | VCCO_15_H15 | power_in | `+3.3V` | U4.J12, U4.E14, U4.C10, U4.B13, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H16 | IO_L22P_T3_A17_15_H16 | bidirectional+no_connect | `unconnected-(U4A-IO_L22P_T3_A17_15-PadH16)` | — (no other pins on this net) |
| J1 | IO_L22N_T3_35_J1 | bidirectional+no_connect | `unconnected-(U4B-IO_L22N_T3_35-PadJ1)` | — (no other pins on this net) |
| J2 | VCCO_35_J2 | power_in | `+3.3V` | U4.F1, U4.E4, U4.D7, U4.B3, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J3 | IO_L21P_T3_DQS_35_J3 | bidirectional+no_connect | `unconnected-(U4B-IO_L21P_T3_DQS_35-PadJ3)` | — (no other pins on this net) |
| J4 | IO_L19N_T3_VREF_35_J4 | bidirectional+no_connect | `unconnected-(U4B-IO_L19N_T3_VREF_35-PadJ4)` | — (no other pins on this net) |
| J5 | IO_L19P_T3_35_J5 | bidirectional+no_connect | `unconnected-(U4B-IO_L19P_T3_35-PadJ5)` | — (no other pins on this net) |
| J6 | VCCINT_J6 | power_in | `+1V0_FPGA` | U4.H9, U4.K9, U4.L8, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J7 | VN_0_J7 | bidirectional | `/fpga/XADC_VN` | R152.1 |
| J8 | VREFP_0_J8 | bidirectional | `/fpga/XADC_VPREF` | R153.1 |
| J9 | GND_J9 | power_in | `GND` | U4.J11, U4.K4, U4.K6, U4.K14, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J10 | VCCAUX_J10 | power_in | `+1V8_FPGA` | U4.G10, U4.K11, U4.L10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J11 | GND_J11 | power_in | `GND` | U4.J9, U4.K4, U4.K6, U4.K14, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J12 | VCCO_15_J12 | power_in | `+3.3V` | U4.H15, U4.E14, U4.C10, U4.B13, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J13 | IO_L1P_T0_D00_MOSI_14_J13 | bidirectional | `/fpga/QSPI_D0` | U141.5 |
| J14 | IO_L1N_T0_D01_DIN_14_J14 | bidirectional | `/fpga/QSPI_D1` | U141.2 |
| J15 | IO_L23P_T3_FOE_B_15_J15 | bidirectional+no_connect | `unconnected-(U4A-IO_L23P_T3_FOE_B_15-PadJ15)` | — (no other pins on this net) |
| J16 | IO_L23N_T3_FWE_B_15_J16 | bidirectional+no_connect | `unconnected-(U4A-IO_L23N_T3_FWE_B_15-PadJ16)` | — (no other pins on this net) |
| K1 | IO_L22P_T3_35_K1 | bidirectional+no_connect | `unconnected-(U4B-IO_L22P_T3_35-PadK1)` | — (no other pins on this net) |
| K2 | IO_L24N_T3_35_K2 | bidirectional+no_connect | `unconnected-(U4B-IO_L24N_T3_35-PadK2)` | — (no other pins on this net) |
| K3 | IO_L24P_T3_35_K3 | bidirectional+no_connect | `unconnected-(U4B-IO_L24P_T3_35-PadK3)` | — (no other pins on this net) |
| K4 | GND_K4 | power_in | `GND` | U4.K6, U4.J11, U4.K14, U4.J9, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K5 | IO_25_35_K5 | bidirectional+no_connect | `unconnected-(U4B-IO_25_35-PadK5)` | — (no other pins on this net) |
| K6 | GND_K6 | power_in | `GND` | U4.K14, U4.K4, U4.L1, U4.J11, U4.J9, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K7 | DXN_0_K7 | bidirectional+no_connect | `unconnected-(U4C-DXN_0-PadK7)` | — (no other pins on this net) |
| K8 | DXP_0_K8 | bidirectional+no_connect | `unconnected-(U4C-DXP_0-PadK8)` | — (no other pins on this net) |
| K9 | VCCINT_K9 | power_in | `+1V0_FPGA` | U4.J6, U4.L8, U4.H9, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K10 | INIT_B_0_K10 | bidirectional | `Net-(U4C-INIT_B_0)` | TP791.1, R142.2 |
| K11 | VCCAUX_K11 | power_in | `+1V8_FPGA` | U4.J10, U4.L10, U4.G10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K12 | IO_0_14_K12 | bidirectional+no_connect | `unconnected-(U4A-IO_0_14-PadK12)` | — (no other pins on this net) |
| K13 | IO_L5P_T0_D06_14_K13 | bidirectional+no_connect | `unconnected-(U4A-IO_L5P_T0_D06_14-PadK13)` | — (no other pins on this net) |
| K14 | GND_K14 | power_in | `GND` | U4.K6, U4.L1, U4.K4, U4.L11, U4.J11, U4.M8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K15 | IO_L2P_T0_D02_14_K15 | bidirectional | `/fpga/QSPI_D2` | U141.3, R148.2 |
| K16 | IO_L2N_T0_D03_14_K16 | bidirectional | `/fpga/QSPI_D3` | U141.7, R149.2 |
| L1 | GND_L1 | power_in | `GND` | U4.K14, U4.L11, U4.K6, U4.M8, U4.K4, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L2 | IO_L23N_T3_35_L2 | bidirectional+no_connect | `unconnected-(U4B-IO_L23N_T3_35-PadL2)` | — (no other pins on this net) |
| L3 | IO_L23P_T3_35_L3 | bidirectional+no_connect | `unconnected-(U4B-IO_L23P_T3_35-PadL3)` | — (no other pins on this net) |
| L4 | IO_L1P_T0_34_L4 | bidirectional | `/fpga/DAC_SDI_SRC` | R147.1 |
| L5 | IO_0_34_L5 | bidirectional+no_connect | `unconnected-(U4B-IO_0_34-PadL5)` | — (no other pins on this net) |
| L6 | VCCO_0_L6 | power_in | `+3.3V` | U4.J12, U4.H15, U4.E14, U4.C10, U4.B13, U4.A16 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L7 | TCK_0_L7 | bidirectional | `/fpga/JTAG_TCK` | J140.6 |
| L8 | VCCINT_L8 | power_in | `+1V0_FPGA` | U4.K9, U4.J6, U4.H9, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L9 | PROGRAM_B_0_L9 | bidirectional | `Net-(U4C-PROGRAM_B_0)` | TP790.1, R144.2 |
| L10 | VCCAUX_L10 | power_in | `+1V8_FPGA` | U4.K11, U4.J10, U4.G8, U4.G10, C158.1, C157.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L11 | GND_L11 | power_in | `GND` | U4.M8, U4.L1, U4.K14, U4.N5, U4.N15, U4.K6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L12 | IO_L6P_T0_FCS_B_14_L12 | bidirectional | `/fpga/QSPI_CS` | R140.2, U141.1 |
| L13 | IO_L5N_T0_D07_14_L13 | bidirectional+no_connect | `unconnected-(U4A-IO_L5N_T0_D07_14-PadL13)` | — (no other pins on this net) |
| L14 | IO_L4P_T0_D04_14_L14 | bidirectional+no_connect | `unconnected-(U4A-IO_L4P_T0_D04_14-PadL14)` | — (no other pins on this net) |
| L15 | IO_L3P_T0_DQS_PUDC_B_14_L15 | bidirectional | `/fpga/PUDC_N` | R141.2 |
| L16 | VCCO_14_L16 | power_in | `+3.3V` | U4.M13, U4.N10, U4.P7, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M1 | IO_L2N_T0_34_M1 | bidirectional | `/fpga/DAC_SCLK_SRC` | R146.1 |
| M2 | IO_L2P_T0_34_M2 | bidirectional | `/fpga/DAC_CS_SRC` | R145.1 |
| M3 | VCCO_34_M3 | power_in | `+3.3V` | U4.R4, U4.T1, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M4 | IO_L1N_T0_34_M4 | bidirectional | `DAC_SDO` | TP203.1, U10.15 |
| M5 | IO_L6P_T0_34_M5 | bidirectional+no_connect | `unconnected-(U4B-IO_L6P_T0_34-PadM5)` | — (no other pins on this net) |
| M6 | IO_L19P_T3_A10_D26_14_M6 | bidirectional+no_connect | `unconnected-(U4A-IO_L19P_T3_A10_D26_14-PadM6)` | — (no other pins on this net) |
| M7 | TMS_0_M7 | bidirectional | `/fpga/JTAG_TMS` | J140.4 |
| M8 | GND_M8 | power_in | `GND` | U4.L11, U4.N5, U4.N15, U4.L1, U4.K14, U4.P2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M9 | M0_0_M9 | bidirectional | `/fpga/MODE0` | R155.2 |
| M10 | M1_0_M10 | bidirectional | `/fpga/MODE1` | R156.2 |
| M11 | M2_0_M11 | bidirectional | `/fpga/MODE2` | R157.2 |
| M12 | IO_L6N_T0_D08_VREF_14_M12 | bidirectional+no_connect | `unconnected-(U4A-IO_L6N_T0_D08_VREF_14-PadM12)` | — (no other pins on this net) |
| M13 | VCCO_14_M13 | power_in | `+3.3V` | U4.L16, U4.N10, U4.P7, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M14 | IO_L4N_T0_D05_14_M14 | bidirectional+no_connect | `unconnected-(U4A-IO_L4N_T0_D05_14-PadM14)` | — (no other pins on this net) |
| M15 | IO_L3N_T0_DQS_EMCCLK_14_M15 | bidirectional+no_connect | `unconnected-(U4A-IO_L3N_T0_DQS_EMCCLK_14-PadM15)` | — (no other pins on this net) |
| M16 | IO_L7P_T1_D09_14_M16 | bidirectional+no_connect | `unconnected-(U4A-IO_L7P_T1_D09_14-PadM16)` | — (no other pins on this net) |
| N1 | IO_L4P_T0_34_N1 | bidirectional | `HOST_TX` | U142.1 |
| N2 | IO_L3N_T0_DQS_34_N2 | bidirectional | `PICO_TX` | J123.3 |
| N3 | IO_L3P_T0_DQS_34_N3 | bidirectional | `PICO_RX` | J123.4 |
| N4 | IO_L6N_T0_VREF_34_N4 | bidirectional+no_connect | `unconnected-(U4B-IO_L6N_T0_VREF_34-PadN4)` | — (no other pins on this net) |
| N5 | GND_N5 | power_in | `GND` | U4.N15, U4.M8, U4.P2, U4.L11, U4.P12, U4.L1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N6 | IO_L19N_T3_A09_D25_VREF_14_N6 | bidirectional+no_connect | `unconnected-(U4A-IO_L19N_T3_A09_D25_VREF_14-PadN6)` | — (no other pins on this net) |
| N7 | TDI_0_N7 | bidirectional | `/fpga/JTAG_TDI` | J140.10 |
| N8 | TDO_0_N8 | bidirectional | `/fpga/JTAG_TDO` | J140.8 |
| N9 | IO_L18P_T2_A12_D28_14_N9 | bidirectional+no_connect | `unconnected-(U4A-IO_L18P_T2_A12_D28_14-PadN9)` | — (no other pins on this net) |
| N10 | VCCO_14_N10 | power_in | `+3.3V` | U4.M13, U4.P7, U4.L16, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N11 | IO_L13P_T2_MRCC_14_N11 | bidirectional+no_connect | `unconnected-(U4A-IO_L13P_T2_MRCC_14-PadN11)` | — (no other pins on this net) |
| N12 | IO_L13N_T2_MRCC_14_N12 | bidirectional+no_connect | `unconnected-(U4A-IO_L13N_T2_MRCC_14-PadN12)` | — (no other pins on this net) |
| N13 | IO_L11P_T1_SRCC_14_N13 | bidirectional+no_connect | `unconnected-(U4A-IO_L11P_T1_SRCC_14-PadN13)` | — (no other pins on this net) |
| N14 | IO_L12P_T1_MRCC_14_N14 | bidirectional+no_connect | `unconnected-(U4A-IO_L12P_T1_MRCC_14-PadN14)` | — (no other pins on this net) |
| N15 | GND_N15 | power_in | `GND` | U4.N5, U4.P2, U4.M8, U4.P12, U4.L11, U4.R9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N16 | IO_L7N_T1_D10_14_N16 | bidirectional+no_connect | `unconnected-(U4A-IO_L7N_T1_D10_14-PadN16)` | — (no other pins on this net) |
| P1 | IO_L4N_T0_34_P1 | bidirectional | `HOST_RX` | U142.17 |
| P2 | GND_P2 | power_in | `GND` | U4.N15, U4.P12, U4.N5, U4.R9, U4.M8, U4.T6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P3 | IO_L5N_T0_34_P3 | bidirectional | `PICO_HEARTBEAT` | J123.6 |
| P4 | IO_L5P_T0_34_P4 | bidirectional | `PICO_STOP_REQ_N` | R754.1, U755.1 |
| P5 | IO_L10P_T1_34_P5 | bidirectional+no_connect | `unconnected-(U4B-IO_L10P_T1_34-PadP5)` | — (no other pins on this net) |
| P6 | IO_25_14_P6 | bidirectional+no_connect | `unconnected-(U4A-IO_25_14-PadP6)` | — (no other pins on this net) |
| P7 | VCCO_14_P7 | power_in | `+3.3V` | U4.R14, U4.N10, U4.T11, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P8 | IO_L20P_T3_A08_D24_14_P8 | bidirectional+no_connect | `unconnected-(U4A-IO_L20P_T3_A08_D24_14-PadP8)` | — (no other pins on this net) |
| P9 | IO_L18N_T2_A11_D27_14_P9 | bidirectional+no_connect | `unconnected-(U4A-IO_L18N_T2_A11_D27_14-PadP9)` | — (no other pins on this net) |
| P10 | IO_L14P_T2_SRCC_14_P10 | bidirectional+no_connect | `unconnected-(U4A-IO_L14P_T2_SRCC_14-PadP10)` | — (no other pins on this net) |
| P11 | IO_L14N_T2_SRCC_14_P11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14N_T2_SRCC_14-PadP11)` | — (no other pins on this net) |
| P12 | GND_P12 | power_in | `GND` | U4.R9, U4.P2, U4.T6, U4.N15, U4.T16, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P13 | IO_L11N_T1_SRCC_14_P13 | bidirectional+no_connect | `unconnected-(U4A-IO_L11N_T1_SRCC_14-PadP13)` | — (no other pins on this net) |
| P14 | IO_L12N_T1_MRCC_14_P14 | bidirectional+no_connect | `unconnected-(U4A-IO_L12N_T1_MRCC_14-PadP14)` | — (no other pins on this net) |
| P15 | IO_L8P_T1_D11_14_P15 | bidirectional+no_connect | `unconnected-(U4A-IO_L8P_T1_D11_14-PadP15)` | — (no other pins on this net) |
| P16 | IO_L8N_T1_D12_14_P16 | bidirectional+no_connect | `unconnected-(U4A-IO_L8N_T1_D12_14-PadP16)` | — (no other pins on this net) |
| R1 | IO_L7N_T1_34_R1 | bidirectional | `/DRIVER_FAULT_N` | R712.2, U600.4, U600.6, U601.4, U601.6, U602.4 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R2 | IO_L7P_T1_34_R2 | bidirectional+no_connect | `unconnected-(U4B-IO_L7P_T1_34-PadR2)` | — (no other pins on this net) |
| R3 | IO_L8P_T1_34_R3 | bidirectional | `/BUCK_SYNC` | C809.1 |
| R4 | VCCO_34_R4 | power_in | `+3.3V` | U4.M3, U4.T1, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R5 | IO_L23P_T3_A03_D19_14_R5 | bidirectional+no_connect | `unconnected-(U4A-IO_L23P_T3_A03_D19_14-PadR5)` | — (no other pins on this net) |
| R6 | IO_L24P_T3_A01_D17_14_R6 | bidirectional+no_connect | `unconnected-(U4A-IO_L24P_T3_A01_D17_14-PadR6)` | — (no other pins on this net) |
| R7 | IO_L24N_T3_A00_D16_14_R7 | bidirectional+no_connect | `unconnected-(U4A-IO_L24N_T3_A00_D16_14-PadR7)` | — (no other pins on this net) |
| R8 | IO_L20N_T3_A07_D23_14_R8 | bidirectional+no_connect | `unconnected-(U4A-IO_L20N_T3_A07_D23_14-PadR8)` | — (no other pins on this net) |
| R9 | GND_R9 | power_in | `GND` | U4.P12, U4.T6, U4.P2, U4.T16, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R10 | IO_L17P_T2_A14_D30_14_R10 | bidirectional+no_connect | `unconnected-(U4A-IO_L17P_T2_A14_D30_14-PadR10)` | — (no other pins on this net) |
| R11 | IO_L17N_T2_A13_D29_14_R11 | bidirectional+no_connect | `unconnected-(U4A-IO_L17N_T2_A13_D29_14-PadR11)` | — (no other pins on this net) |
| R12 | IO_L15P_T2_DQS_RDWR_B_14_R12 | bidirectional+no_connect | `unconnected-(U4A-IO_L15P_T2_DQS_RDWR_B_14-PadR12)` | — (no other pins on this net) |
| R13 | IO_L16P_T2_CSI_B_14_R13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16P_T2_CSI_B_14-PadR13)` | — (no other pins on this net) |
| R14 | VCCO_14_R14 | power_in | `+3.3V` | U4.P7, U4.T11, U4.N10, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R15 | IO_L9P_T1_DQS_14_R15 | bidirectional+no_connect | `unconnected-(U4A-IO_L9P_T1_DQS_14-PadR15)` | — (no other pins on this net) |
| R16 | IO_L9N_T1_DQS_D13_14_R16 | bidirectional+no_connect | `unconnected-(U4A-IO_L9N_T1_DQS_D13_14-PadR16)` | — (no other pins on this net) |
| T1 | VCCO_34_T1 | power_in | `+3.3V` | U4.R4, U4.M3, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T2 | IO_L8N_T1_34_T2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8N_T1_34-PadT2)` | — (no other pins on this net) |
| T3 | IO_L9N_T1_DQS_34_T3 | bidirectional+no_connect | `unconnected-(U4B-IO_L9N_T1_DQS_34-PadT3)` | — (no other pins on this net) |
| T4 | IO_L9P_T1_DQS_34_T4 | bidirectional+no_connect | `unconnected-(U4B-IO_L9P_T1_DQS_34-PadT4)` | — (no other pins on this net) |
| T5 | IO_L23N_T3_A02_D18_14_T5 | bidirectional+no_connect | `unconnected-(U4A-IO_L23N_T3_A02_D18_14-PadT5)` | — (no other pins on this net) |
| T6 | GND_T6 | power_in | `GND` | U4.T16, U4.R9, U4.P12, U4.P2, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T7 | IO_L21P_T3_DQS_14_T7 | bidirectional+no_connect | `unconnected-(U4A-IO_L21P_T3_DQS_14-PadT7)` | — (no other pins on this net) |
| T8 | IO_L21N_T3_DQS_A06_D22_14_T8 | bidirectional+no_connect | `unconnected-(U4A-IO_L21N_T3_DQS_A06_D22_14-PadT8)` | — (no other pins on this net) |
| T9 | IO_L22P_T3_A05_D21_14_T9 | bidirectional+no_connect | `unconnected-(U4A-IO_L22P_T3_A05_D21_14-PadT9)` | — (no other pins on this net) |
| T10 | IO_L22N_T3_A04_D20_14_T10 | bidirectional+no_connect | `unconnected-(U4A-IO_L22N_T3_A04_D20_14-PadT10)` | — (no other pins on this net) |
| T11 | VCCO_14_T11 | power_in | `+3.3V` | U4.R14, U4.P7, U4.N10, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T12 | IO_L15N_T2_DQS_DOUT_CSO_B_14_T12 | bidirectional+no_connect | `unconnected-(U4A-IO_L15N_T2_DQS_DOUT_CSO_B_14-PadT12)` | — (no other pins on this net) |
| T13 | IO_L16N_T2_A15_D31_14_T13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16N_T2_A15_D31_14-PadT13)` | — (no other pins on this net) |
| T14 | IO_L10P_T1_D14_14_T14 | bidirectional+no_connect | `unconnected-(U4A-IO_L10P_T1_D14_14-PadT14)` | — (no other pins on this net) |
| T15 | IO_L10N_T1_D15_14_T15 | bidirectional+no_connect | `unconnected-(U4A-IO_L10N_T1_D15_14-PadT15)` | — (no other pins on this net) |
| T16 | GND_T16 | power_in | `GND` | U4.T6, U4.R9, U4.P12, U4.P2, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: R100 (33) on `CLOCK_32M768`
- gain / feedback-set resistor: R155 (0) on `/fpga/MODE0`
- gain / feedback-set resistor: R156 (0) on `/fpga/MODE1`
- gain / feedback-set resistor: R157 (0) on `/fpga/MODE2`
- pull-down resistor: R152 (0) on `/fpga/XADC_VN`
- pull-down resistor: R150 (0) on `/fpga/XADC_VNREF`
- pull-down resistor: R151 (0) on `/fpga/XADC_VP`
- pull-down resistor: R153 (0) on `/fpga/XADC_VPREF`
- pull-up resistor: R140 (4.7k) on `+3.3V`
- pull-up resistor: R141 (4.7k) on `/fpga/PUDC_N`
- series / termination resistor: R145 (33) on `/fpga/DAC_CS_SRC`
- series / termination resistor: R146 (33) on `/fpga/DAC_SCLK_SRC`
- series / termination resistor: R147 (33) on `/fpga/DAC_SDI_SRC`
- supply decoupling: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.5) on `+1V0_FPGA`
- supply decoupling: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on `+1V8_FPGA`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### U141 — W25Q64JVSSIQ

Sheet: fpga (5) · Footprint: Package_SO:SOIC-8_5.3x5.3mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | ~{CS}_1 | input | `/fpga/QSPI_CS` | U4.L12, R140.2 |
| 2 | IO1/DO_2 | bidirectional | `/fpga/QSPI_D1` | U4.J14 |
| 3 | IO2/~{WP}_3 | bidirectional | `/fpga/QSPI_D2` | R148.2, U4.K15 |
| 4 | GND_4 | power_in | `GND` | J140.3, J140.5, J140.7, J140.9, J140.11, Y1.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 5 | IO0/DI_5 | bidirectional | `/fpga/QSPI_D0` | U4.J13 |
| 6 | CLK_6 | input | `Net-(U141-CLK)` | R790.2 |
| 7 | IO3_7 | bidirectional | `/fpga/QSPI_D3` | R149.2, U4.K16 |
| 8 | VCC_8 | power_in | `+3.3V` | J140.2, Y1.4, Y1.1, U4.L6, R148.1, R143.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- series / termination resistor: R790 (0) on `Net-(U141-CLK)`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### U142 — FT231XQ

Sheet: fpga (5) · Footprint: Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 21 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | RXD_1 | input | `HOST_TX` | U4.N1 |
| 2 | ~{RI}_2 | input | `+3.3V` | U142.5, U142.4, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | GND_3 | power_in | `GND` | U142.13, U142.21, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 4 | ~{DSR}_4 | input | `+3.3V` | U142.5, U142.2, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 5 | ~{DCD}_5 | input | `+3.3V` | U142.4, U142.2, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 6 | ~{CTS}_6 | input | `+3.3V` | U142.4, U142.5, U142.2, U142.20, U142.12, U142.10 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 7 | CBUS2_7 | bidirectional | `/fpga/VBUS_SENSE` | R158.2, R159.1 |
| 8 | USBDP_8 | bidirectional | `/fpga/FT_DP` | C173.1, R160.2 |
| 9 | USBDM_9 | bidirectional | `/fpga/FT_DM` | C174.1, R161.2 |
| 10 | 3V3OUT_10 | passive | `+3.3V` | U142.11, U142.12, U142.20, U142.6, R166.1, U142.4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 11 | ~{RESET}_11 | input | `+3.3V` | U142.10, U142.12, U142.20, U142.5, U142.4, U142.2 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 12 | VCC_12 | power_in | `+3.3V` | U142.20, U142.10, R166.1, U142.6, U142.11, U142.4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 13 | GND_13 | power_in | `GND` | U142.21, U142.3, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 14 | CBUS1_14 | bidirectional+no_connect | `unconnected-(U142-CBUS1-Pad14)` | — (no other pins on this net) |
| 15 | CBUS0_15 | bidirectional+no_connect | `unconnected-(U142-CBUS0-Pad15)` | — (no other pins on this net) |
| 16 | CBUS3_16 | bidirectional+no_connect | `unconnected-(U142-CBUS3-Pad16)` | — (no other pins on this net) |
| 17 | TXD_17 | output | `HOST_RX` | U4.P1 |
| 18 | ~{DTR}_18 | output+no_connect | `unconnected-(U142-~{DTR}-Pad18)` | — (no other pins on this net) |
| 19 | ~{RTS}_19 | output+no_connect | `unconnected-(U142-~{RTS}-Pad19)` | — (no other pins on this net) |
| 20 | VCCIO_20 | power_in | `+3.3V` | U142.12, U142.6, U142.10, R166.1, U142.4, U142.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 21 | GND_21 | power_in | `GND` | U142.13, U142.3, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on `+3.3V`
- filter capacitor to ground: C174 (47p) on `/fpga/FT_DM`
- filter capacitor to ground: C173 (47p) on `/fpga/FT_DP`
- pull-down resistor: R159 (10k) on `/fpga/VBUS_SENSE`
- pull-up resistor: R154 (0), R162 (10k), R164 (10k), R166 (10k) on `+3.3V`
- series / termination resistor: R161 (27) on `/fpga/FT_DM`
- series / termination resistor: R160 (27) on `/fpga/FT_DP`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### Y1 — CSX750FBC32.768M-UT

Sheet: fpga (5) · Footprint: Oscillator:Oscillator_SMD_SeikoEpson_SG8002CA-4Pin_7.0x5.0mm · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OE_1 | input | `+3.3V` | Y1.4, R143.1, R142.1, R144.1, R148.1, R149.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 2 | GND_2 | power_in | `GND` | J140.11, J140.9, J140.7, J140.5, J140.3, C140.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | OUT_3 | output | `CLOCK_32M768` | U4.D13, R100.1 |
| 4 | VDD_4 | power_in | `+3.3V` | Y1.1, R143.1, R142.1, R144.1, R148.1, R149.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on `+3.3V`
- pull-up resistor: R143 (4.7k), R148 (4.7k), R149 (4.7k) on `+3.3V`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`
- supply feed / filter: R100 (33) on `CLOCK_32M768`

#### C140 — 100n, C

C140 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C141 — 100n, C

C141 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C142 — 100n, C

C142 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C143 — 100n, C

C143 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C144 — 100n, C

C144 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C145 — 4.7u, C

C145 — 4.7u, C_0805_2012Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C150 — 100n, C

C150 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C151 — 100n, C

C151 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C152 — 100n, C

C152 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C153 — 100n, C

C153 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C154 — 100n, C

C154 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C155 — 100n, C

C155 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C156 — 100n, C

C156 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C157 — 100n, C

C157 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C158 — 100n, C

C158 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C159 — 100n, C

C159 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C160 — 100n, C

C160 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C161 — 100n, C

C161 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C162 — 100n, C

C162 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C163 — 100n, C

C163 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C164 — 100n, C

C164 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C165 — 100n, C

C165 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C166 — 100n, C

C166 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C167 — 100n, C

C167 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C168 — 100n, C

C168 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C169 — 100n, C

C169 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C170 — 10u, C

C170 — 10u, C_0805_2012Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C171 — 10u, C

C171 — 10u, C_0805_2012Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C172 — 10u, C

C172 — 10u, C_0805_2012Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C173 — 47p, C

C173 — 47p, C_0603_1608Metric — `/fpga/FT_DP` ↔ `GND` — filter capacitor to ground for U142 (pin 1 → 2).

#### C174 — 47p, C

C174 — 47p, C_0603_1608Metric — `/fpga/FT_DM` ↔ `GND` — filter capacitor to ground for U142 (pin 1 → 2).

#### R140 — 4.7k, R

R140 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_CS` — pull-up resistor for U4 (pin 1 → 2).

#### R141 — 4.7k, R

R141 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/PUDC_N` — pull-up resistor for U4 (pin 1 → 2).

#### R142 — 4.7k, R

R142 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-INIT_B_0)` — pull-up resistor for TP791 (pin 1 → 2).

#### R143 — 4.7k, R

R143 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-DONE_0)` — pull-up resistor for Y1 (pin 1 → 2).

#### R144 — 4.7k, R

R144 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-PROGRAM_B_0)` — pull-up resistor for TP790 (pin 1 → 2).

#### R145 — 33, R

R145 — 33, R_0603_1608Metric — `/fpga/DAC_CS_SRC` ↔ `DAC_CS` — series / termination resistor for U4 (pin 1 → 2).

#### R146 — 33, R

R146 — 33, R_0603_1608Metric — `/fpga/DAC_SCLK_SRC` ↔ `DAC_SCLK` — series / termination resistor for U4 (pin 1 → 2).

#### R147 — 33, R

R147 — 33, R_0603_1608Metric — `/fpga/DAC_SDI_SRC` ↔ `DAC_SDI` — series / termination resistor for U4 (pin 1 → 2).

#### R148 — 4.7k, R

R148 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_D2` — pull-up resistor for Y1 (pin 1 → 2).

#### R149 — 4.7k, R

R149 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_D3` — pull-up resistor for Y1 (pin 1 → 2).

#### R150 — 0, R

R150 — 0, R_0603_1608Metric — `/fpga/XADC_VNREF` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R151 — 0, R

R151 — 0, R_0603_1608Metric — `/fpga/XADC_VP` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R152 — 0, R

R152 — 0, R_0603_1608Metric — `/fpga/XADC_VN` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R153 — 0, R

R153 — 0, R_0603_1608Metric — `/fpga/XADC_VPREF` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R154 — 0, R

R154 — 0, R_0603_1608Metric — `+3.3V` ↔ `/fpga/CFGBVS` — pull-up resistor for U142 (pin 1 → 2).

#### R155 — 0, R

R155 — 0, R_0603_1608Metric — `+3.3V` ↔ `/fpga/MODE0` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R156 — 0, R

R156 — 0, R_0603_1608Metric — `GND` ↔ `/fpga/MODE1` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R157 — 0, R

R157 — 0, R_0603_1608Metric — `GND` ↔ `/fpga/MODE2` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R158 — 4.7k, R

R158 — 4.7k, R_0603_1608Metric — `USB_VBUS` ↔ `/fpga/VBUS_SENSE` — supply feed / filter for J124 (pin 1 → 2).

#### R159 — 10k, R

R159 — 10k, R_0603_1608Metric — `/fpga/VBUS_SENSE` ↔ `GND` — pull-down resistor for U142 (pin 1 → 2).

#### R160 — 27, R

R160 — 27, R_0603_1608Metric — `USB_DP` ↔ `/fpga/FT_DP` — series / termination resistor for U142 (pin 1 → 2).

#### R161 — 27, R

R161 — 27, R_0603_1608Metric — `USB_DM` ↔ `/fpga/FT_DM` — series / termination resistor for U142 (pin 1 → 2).

#### R162 — 10k, R

R162 — 10k, R_0603_1608Metric — `+3.3V` ↔ `DAC_CS` — pull-up resistor for U142 (pin 1 → 2).

#### R163 — 10k, R

R163 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_RESET_N` — enable pull-up for U101 (pin 1 → 2).

#### R164 — 10k, R

R164 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_CS` — pull-up resistor for U142 (pin 1 → 2).

#### R165 — 10k, R

R165 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_START_N` — enable pull-up for U101 (pin 1 → 2).

#### R166 — 10k, R

R166 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_SYNC_IN` — pull-up resistor for U142 (pin 1 → 2).

#### R790 — 0, R

R790 — 0, R_0603_1608Metric — `Net-(U4C-CCLK_0)` ↔ `Net-(U141-CLK)` — series / termination resistor for U141 (pin 1 → 2).


## Dependency summary

## 5. Per-sheet support summary

Page 1 — root has no components, so no support rows.

Component → the passives that exist to serve it. `—` means no R/C/L was found by either rule on that sheet. Counts are per component, not per net.


### 5.5 fpga

| Component | Passives that serve it |
|---|---|
| J140 | soft-start / bias capacitor: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.5) on +3.3V |
| TP790 | pull-up resistor: R144 (4.7k) on Net-(U4C-PROGRAM_B_0) |
| TP791 | pull-up resistor: R142 (4.7k) on Net-(U4C-INIT_B_0) |
| TP792 | — |
| U4 | enable / sequencing network: R100 (33) on CLOCK_32M768; gain / feedback-set resistor: R155 (0) on /fpga/MODE0; gain / feedback-set resistor: R156 (0) on /fpga/MODE1; gain / feedback-set resistor: R157 (0) on /fpga/MODE2; pull-down resistor: R152 (0) on /fpga/XADC_VN; pull-down resistor: R150 (0) on /fpga/XADC_VNREF; pull-down resistor: R151 (0) on /fpga/XADC_VP; pull-down resistor: R153 (0) on /fpga/XADC_VPREF; pull-up resistor: R140 (4.7k) on +3.3V; pull-up resistor: R141 (4.7k) on /fpga/PUDC_N; series / termination resistor: R145 (33) on /fpga/DAC_CS_SRC; series / termination resistor: R146 (33) on /fpga/DAC_SCLK_SRC; series / termination resistor: R147 (33) on /fpga/DAC_SDI_SRC; supply decoupling: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.5) on +1V0_FPGA; supply decoupling: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on +1V8_FPGA; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| U141 | series / termination resistor: R790 (0) on Net-(U141-CLK); supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| U142 | enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on +3.3V; filter capacitor to ground: C174 (47p) on /fpga/FT_DM; filter capacitor to ground: C173 (47p) on /fpga/FT_DP; pull-down resistor: R159 (10k) on /fpga/VBUS_SENSE; pull-up resistor: R154 (0), R162 (10k), R164 (10k), R166 (10k) on +3.3V; series / termination resistor: R161 (27) on /fpga/FT_DM; series / termination resistor: R160 (27) on /fpga/FT_DP; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| Y1 | enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on +3.3V; pull-up resistor: R143 (4.7k), R148 (4.7k), R149 (4.7k) on +3.3V; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V; supply feed / filter: R100 (33) on CLOCK_32M768 |
