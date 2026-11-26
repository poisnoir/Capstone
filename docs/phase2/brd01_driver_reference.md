# BRD-01 driver reference — component → pins → wires (driver sheet only)

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

Provenance: this is a driver-sheet-only extract of `docs/phase2/brd01_component_reference.md` (its §4.1, §4.3 and §5.3 are reproduced verbatim below, stale-data banner included). Its net-centric counterpart for this sheet is `brd01_wiring_manifest.md` §3.3 (net → pins).

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

### 4.3 Page 3 — driver

Net-centric counterpart: `brd01_wiring_manifest.md` §3.3. 338 components on this sheet.

#### Components

#### TP200 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_CS` | U10.12, R145.2, R162.2 |

#### TP201 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SCLK` | U10.13, R146.2 |

#### TP202 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SDI` | U10.14, R147.2 |

#### TP203 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SDO` | U10.15, U4.M4 |

#### TP210 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT0` | U60.1, U600.1 |

#### TP211 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT1` | U61.1, U600.3 |

#### TP212 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT2` | U62.1, U601.1 |

#### TP213 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT3` | U63.1, U601.3 |

#### TP214 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT4` | U64.1, U602.1 |

#### TP215 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT5` | U65.1, U602.3 |

#### TP216 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT6` | U66.1, U603.1 |

#### TP217 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT7` | U67.1, U603.3 |

#### TP820 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/BUF0` | C212.1, U20.6 |

#### TP821 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `FG0_OUT` | C212.2, J20.1 |

#### TP822 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `FG0_RETURN` | R400.1, R20.1, J20.2 |

#### TP823 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/VMID_7V5` | R383.1, C283.1, R382.2, C282.1, R21.2, R412.1 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C283 (100n) on `/driver/VMID_7V5`
- pull-down resistor: R383 (10k) on `/driver/VMID_7V5`
- pull-up resistor: R382 (10k) on `/driver/VMID_7V5`
- series / termination resistor: R20 (1.00 0.1% 0.5W), R21 (1.00 0.1% 0.5W), R22 (1.00 0.1% 0.5W), R23 (1.00 0.1% 0.5W), R24 (1.00 0.1% 0.5W), R25 (1.00 0.1% 0.5W), R26 (1.00 0.1% 0.5W), R27 (1.00 0.1% 0.5W) on `/driver/VMID_7V5`

#### U10 — DAC80508MRTET

Sheet: driver (3) · Footprint: Package_DFN_QFN:Texas_RTE0016D_WQFN-16-1EP_3x3mm_P0.5mm_EP0.8x0.8mm · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | REF_1 | bidirectional | `/driver/DAC_REF` | C203.1 |
| 2 | OUT0_2 | output | `/driver/DAC0` | R220.1 |
| 3 | OUT1_3 | output | `/driver/DAC1` | R230.1 |
| 4 | OUT2_4 | output | `/driver/DAC2` | R240.1 |
| 5 | OUT3_5 | output | `/driver/DAC3` | R250.1 |
| 6 | GND_6 | power_in | `GND` | U10.17, C203.2, C200.2, U80.9, U80.3, C201.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 7 | VDD_7 | power_in | `+5V_EXC` | C200.1, C201.1, U80.1, U80.16, C210.1, U82.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | OUT4_8 | output | `/driver/DAC4` | R260.1 |
| 9 | OUT5_9 | output | `/driver/DAC5` | R270.1 |
| 10 | OUT6_10 | output | `/driver/DAC6` | R280.1 |
| 11 | OUT7_11 | output | `/driver/DAC7` | R290.1 |
| 12 | ~{CS}_12 | input | `DAC_CS` | TP200.1, R145.2, R162.2 |
| 13 | SCLK_13 | input | `DAC_SCLK` | TP201.1, R146.2 |
| 14 | SDI_14 | input | `DAC_SDI` | TP202.1, R147.2 |
| 15 | SDO/~{ALARM}_15 | output | `DAC_SDO` | TP203.1, U4.M4 |
| 16 | VIO_16 | power_in | `+3.3V` | C202.1, C290.1, C292.1, C294.1, C296.1, C291.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 17 | EP_17 | passive | `GND` | U10.6, C203.2, C200.2, U80.9, U80.3, U80.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- soft-start / bias capacitor: C203 (150n) on `/driver/DAC_REF`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply feed / filter: R220 (42.7k 0.1%) on `/driver/DAC0`
- supply feed / filter: R230 (42.7k 0.1%) on `/driver/DAC1`
- supply feed / filter: R240 (42.7k 0.1%) on `/driver/DAC2`
- supply feed / filter: R250 (42.7k 0.1%) on `/driver/DAC3`
- supply feed / filter: R260 (42.7k 0.1%) on `/driver/DAC4`
- supply feed / filter: R270 (42.7k 0.1%) on `/driver/DAC5`
- supply feed / filter: R280 (42.7k 0.1%) on `/driver/DAC6`
- supply feed / filter: R290 (42.7k 0.1%) on `/driver/DAC7`

#### U20 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U20-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG0` | R600.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN0` | R361.2 |
| 4 | V-_4 | power_in | `GND` | U20.9, C213.2, C290.2, R381.2, C280.2, C281.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U39.1, U22.5, U39.4, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF0` | TP820.1, C212.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C213.1, R600.1, R380.1, C280.1, U22.7, R382.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U20-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U20.4, C213.2, C290.2, R381.2, C280.2, C281.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-down resistor: R381 (10k) on `GND`
- pull-up resistor: R380 (10k), R600 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C212 (CAA572X7R1E107M670LJ) on `/driver/BUF0`

#### U21 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U21-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG1` | R601.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN1` | R363.2 |
| 4 | V-_4 | power_in | `GND` | U21.9, C221.2, C291.2, U23.4, C223.2, C222.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U23.5, U25.5, U27.5, U20.5, U22.5, U24.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF1` | C220.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C221.1, R601.1, U23.7, C237.1, R603.1, U25.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U21-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U21.4, C221.2, C291.2, U23.4, U23.9, C223.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R601 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C220 (CAA572X7R1E107M670LJ) on `/driver/BUF1`

#### U22 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U22-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG2` | R602.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN2` | R365.2 |
| 4 | V-_4 | power_in | `GND` | U22.9, C229.2, C290.2, C292.2, C213.2, U20.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U20.5, U24.5, U39.1, U39.4, U26.5, R631.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF2` | C228.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C229.1, R602.1, R600.1, C213.1, U20.7, U24.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U22-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U22.4, C229.2, C290.2, C292.2, C213.2, U24.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R602 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C228 (CAA572X7R1E107M670LJ) on `/driver/BUF2`

#### U23 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U23-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG3` | R603.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN3` | R367.2 |
| 4 | V-_4 | power_in | `GND` | U23.9, C237.2, C291.2, C293.2, C221.2, U21.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U21.5, U25.5, U27.5, U22.5, R631.1, U20.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF3` | C236.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C237.1, R603.1, R601.1, C221.1, U21.7, U25.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U23-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U23.4, C237.2, C291.2, C293.2, C221.2, U25.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R603 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C236 (CAA572X7R1E107M670LJ) on `/driver/BUF3`

#### U24 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U24-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG4` | R604.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN4` | R369.2 |
| 4 | V-_4 | power_in | `GND` | U24.9, C245.2, C292.2, C294.2, C229.2, U22.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U22.5, U26.5, U20.5, U39.1, U39.4, R631.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF4` | C244.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C245.1, R604.1, R602.1, C229.1, U26.7, U22.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U24-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U24.4, C245.2, C292.2, C294.2, C229.2, U26.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R604 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C244 (CAA572X7R1E107M670LJ) on `/driver/BUF4`

#### U25 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U25-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG5` | R605.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN5` | R371.2 |
| 4 | V-_4 | power_in | `GND` | U25.9, C253.2, C293.2, C295.2, C237.2, U23.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U23.5, U27.5, U21.5, R631.1, R651.1, U24.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF5` | C252.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C253.1, R605.1, R603.1, C237.1, U27.7, U23.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U25-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U25.4, C253.2, C293.2, C295.2, C237.2, U27.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R605 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C252 (CAA572X7R1E107M670LJ) on `/driver/BUF5`

#### U26 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U26-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG6` | R606.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN6` | R373.2 |
| 4 | V-_4 | power_in | `GND` | U26.9, C261.2, C294.2, C296.2, C303.2, C245.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U24.5, U22.5, R631.1, R621.1, R651.1, R641.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF6` | C260.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C261.1, R606.1, R604.1, C245.1, U24.7, R602.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U26-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U26.4, C261.2, C294.2, C296.2, C303.2, C302.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R606 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C260 (CAA572X7R1E107M670LJ) on `/driver/BUF6`

#### U27 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U27-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG7` | R607.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN7` | R375.2 |
| 4 | V-_4 | power_in | `GND` | U27.9, C269.2, C295.2, C297.2, C253.2, U25.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U25.5, U23.5, R631.1, R651.1, U21.5, R671.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF7` | C268.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C269.1, R607.1, R605.1, C253.1, U25.7, R603.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U27-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U27.4, C269.2, C295.2, C297.2, C253.2, C307.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R607 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C268 (CAA572X7R1E107M670LJ) on `/driver/BUF7`

#### U30 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR0` | R361.1, R623.1, R622.1 |
| 2 | V-_2 | power_in | `-12VA` | C215.1, U38.2, U32.2, C205.1, C231.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED0` | R621.2, R620.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK0` | R360.2, R622.2, C622.2 |
| 5 | V+_5 | power_in | `+12VA` | C214.1, C204.1, U38.5, C230.1, U32.5, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C622 (150p) on `/driver/FEEDBACK0`
- series / termination resistor: R620 (10k) on `/driver/CMD_BIASED0`
- series / termination resistor: R360 (10k) on `/driver/FEEDBACK0`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R361 (15k), R622 (10M), R623 (330k) on `/driver/ERR0`

#### U31 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR1` | R363.1, R633.1, R632.1 |
| 2 | V-_2 | power_in | `-12VA` | C223.1, U33.2, C239.1, U35.2, C255.1, U37.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED1` | R631.2, R630.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK1` | R362.2, R632.2, C632.2 |
| 5 | V+_5 | power_in | `+12VA` | C222.1, C238.1, U33.5, C254.1, U35.5, C270.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C632 (150p) on `/driver/FEEDBACK1`
- series / termination resistor: R630 (10k) on `/driver/CMD_BIASED1`
- series / termination resistor: R362 (10k) on `/driver/FEEDBACK1`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R363 (15k), R632 (10M), R633 (330k) on `/driver/ERR1`

#### U32 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR2` | R365.1, R643.1, R642.1 |
| 2 | V-_2 | power_in | `-12VA` | C231.1, C215.1, U34.2, U30.2, C247.1, U38.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED2` | R641.2, R640.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK2` | R364.2, R642.2, C642.2 |
| 5 | V+_5 | power_in | `+12VA` | C230.1, C246.1, U30.5, U34.5, C214.1, C204.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C642 (150p) on `/driver/FEEDBACK2`
- series / termination resistor: R640 (10k) on `/driver/CMD_BIASED2`
- series / termination resistor: R364 (10k) on `/driver/FEEDBACK2`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R365 (15k), R642 (10M), R643 (330k) on `/driver/ERR2`

#### U33 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR3` | R367.1, R653.1, R652.1 |
| 2 | V-_2 | power_in | `-12VA` | C239.1, C223.1, U35.2, U31.2, C255.1, U37.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED3` | R651.2, R650.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK3` | R366.2, R652.2, C652.2 |
| 5 | V+_5 | power_in | `+12VA` | C238.1, C254.1, U31.5, U35.5, C222.1, C270.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C652 (150p) on `/driver/FEEDBACK3`
- series / termination resistor: R650 (10k) on `/driver/CMD_BIASED3`
- series / termination resistor: R366 (10k) on `/driver/FEEDBACK3`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R367 (15k), R652 (10M), R653 (330k) on `/driver/ERR3`

#### U34 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR4` | R369.1, R663.1, R662.1 |
| 2 | V-_2 | power_in | `-12VA` | C247.1, C231.1, U36.2, U32.2, C263.1, U41.4 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED4` | R661.2, R660.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK4` | R368.2, R662.2, C662.2 |
| 5 | V+_5 | power_in | `+12VA` | C246.1, C262.1, U36.5, U32.5, C230.1, U41.8 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C662 (150p) on `/driver/FEEDBACK4`
- series / termination resistor: R660 (10k) on `/driver/CMD_BIASED4`
- series / termination resistor: R368 (10k) on `/driver/FEEDBACK4`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R369 (15k), R662 (10M), R663 (330k) on `/driver/ERR4`

#### U35 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR5` | R371.1, R673.1, R672.1 |
| 2 | V-_2 | power_in | `-12VA` | C255.1, C239.1, U37.2, U33.2, C271.1, C307.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED5` | R671.2, R670.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK5` | R370.2, R672.2, C672.2 |
| 5 | V+_5 | power_in | `+12VA` | C254.1, C270.1, U37.5, U33.5, C238.1, C306.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C672 (150p) on `/driver/FEEDBACK5`
- series / termination resistor: R670 (10k) on `/driver/CMD_BIASED5`
- series / termination resistor: R370 (10k) on `/driver/FEEDBACK5`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R371 (15k), R672 (10M), R673 (330k) on `/driver/ERR5`

#### U36 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR6` | R373.1, R683.1, R682.1 |
| 2 | V-_2 | power_in | `-12VA` | C263.1, U41.4, C247.1, U34.2, C301.1, C303.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED6` | R681.2, R680.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK6` | R372.2, R682.2, C682.2 |
| 5 | V+_5 | power_in | `+12VA` | C262.1, U41.8, C302.1, U34.5, C246.1, C300.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C682 (150p) on `/driver/FEEDBACK6`
- series / termination resistor: R680 (10k) on `/driver/CMD_BIASED6`
- series / termination resistor: R372 (10k) on `/driver/FEEDBACK6`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R373 (15k), R682 (10M), R683 (330k) on `/driver/ERR6`

#### U37 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR7` | R375.1, R693.1, R692.1 |
| 2 | V-_2 | power_in | `-12VA` | C271.1, C307.1, C255.1, U35.2, U43.4, C305.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED7` | R691.2, R690.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK7` | R374.2, R692.2, C692.2 |
| 5 | V+_5 | power_in | `+12VA` | C270.1, C306.1, U35.5, U43.8, C254.1, C304.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C692 (150p) on `/driver/FEEDBACK7`
- series / termination resistor: R690 (10k) on `/driver/CMD_BIASED7`
- series / termination resistor: R374 (10k) on `/driver/FEEDBACK7`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R375 (15k), R692 (10M), R693 (330k) on `/driver/ERR7`

#### U38 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `CURRENT_SUM` | R200.1, R110.1 |
| 2 | V-_2 | power_in | `-12VA` | C205.1, U30.2, C215.1, U32.2, C231.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `GND` | C204.2, C205.2, C281.2, U39.2, C280.2, C202.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/SUM_NODE` | R204.2, R200.2, R208.2, R205.2, R201.2, R206.2 — 9 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | V+_5 | power_in | `+12VA` | C204.1, C214.1, U30.5, C230.1, U32.5, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R201 (10k 0.1%), R202 (10k 0.1%), R203 (10k 0.1%), R204 (10k 0.1%), R205 (10k 0.1%), R206 (10k 0.1%), R207 (10k 0.1%), R208 (10k 0.1%) on `/driver/SUM_NODE`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R200 (20k 0.1%) on `CURRENT_SUM`

#### U39 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/BUFFER_VMID` | U39.4, U20.5, U22.5, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | V-_2 | power_in | `GND` | C280.2, C281.2, C204.2, C214.2, U38.3, C205.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/BIAS_DIV` | C281.1, R380.2, R381.1 |
| 4 | IN-_4 | input | `/driver/BUFFER_VMID` | U39.1, U20.5, U22.5, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | V+_5 | power_in | `+15V_FUSED` | C280.1, R380.1, R600.1, C213.1, U20.7, U22.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C281 (100n) on `/driver/BIAS_DIV`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`

#### U40 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE0` | R403.1, R201.1, C621.1, R720.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N0` | R402.2, R403.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P0` | R400.2, R401.1 |
| 4 | V-_4 | power_in | `-12VA` | C301.1, U41.4, C263.1, U36.2, C247.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P1` | R410.2, R411.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N1` | R412.2, R413.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE1` | R413.1, R202.1, C631.1, R722.1 |
| 8 | V+_8 | power_in | `+12VA` | C300.1, U41.8, C262.1, U36.5, C302.1, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C621 (100n) on `/driver/I_SENSE0`
- input / output filter capacitor: C631 (100n) on `/driver/I_SENSE1`
- pull-down resistor: R401 (10k 0.1%) on `/driver/SENSE_P0`
- pull-down resistor: R411 (10k 0.1%) on `/driver/SENSE_P1`
- series / termination resistor: R403 (10k 0.1%) on `/driver/I_SENSE0`
- series / termination resistor: R413 (10k 0.1%) on `/driver/I_SENSE1`
- series / termination resistor: R402 (10k 0.1%) on `/driver/SENSE_N0`
- series / termination resistor: R412 (10k 0.1%) on `/driver/SENSE_N1`
- series / termination resistor: R400 (10k 0.1%) on `/driver/SENSE_P0`
- series / termination resistor: R410 (10k 0.1%) on `/driver/SENSE_P1`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U41 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE2` | R423.1, R203.1, C641.1, R724.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N2` | R422.2, R423.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P2` | R420.2, R421.1 |
| 4 | V-_4 | power_in | `-12VA` | C263.1, C301.1, U36.2, C303.1, U40.4, U42.4 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P3` | R430.2, R431.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N3` | R432.2, R433.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE3` | R433.1, R204.1, C651.1, R726.1 |
| 8 | V+_8 | power_in | `+12VA` | C302.1, U36.5, C262.1, C300.1, U40.8, U42.8 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C641 (100n) on `/driver/I_SENSE2`
- input / output filter capacitor: C651 (100n) on `/driver/I_SENSE3`
- pull-down resistor: R421 (10k 0.1%) on `/driver/SENSE_P2`
- pull-down resistor: R431 (10k 0.1%) on `/driver/SENSE_P3`
- series / termination resistor: R423 (10k 0.1%) on `/driver/I_SENSE2`
- series / termination resistor: R433 (10k 0.1%) on `/driver/I_SENSE3`
- series / termination resistor: R422 (10k 0.1%) on `/driver/SENSE_N2`
- series / termination resistor: R432 (10k 0.1%) on `/driver/SENSE_N3`
- series / termination resistor: R420 (10k 0.1%) on `/driver/SENSE_P2`
- series / termination resistor: R430 (10k 0.1%) on `/driver/SENSE_P3`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U42 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE4` | R443.1, C661.1, R205.1, R728.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N4` | R442.2, R443.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P4` | R440.2, R441.1 |
| 4 | V-_4 | power_in | `-12VA` | C303.1, C305.1, U43.4, U41.4, U36.2, C263.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P5` | R450.2, R451.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N5` | R452.2, R453.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE5` | R453.1, C671.1, R206.1, R730.1 |
| 8 | V+_8 | power_in | `+12VA` | C304.1, C302.1, U43.8, U41.8, U36.5, C262.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C661 (100n) on `/driver/I_SENSE4`
- input / output filter capacitor: C671 (100n) on `/driver/I_SENSE5`
- pull-down resistor: R441 (10k 0.1%) on `/driver/SENSE_P4`
- pull-down resistor: R451 (10k 0.1%) on `/driver/SENSE_P5`
- series / termination resistor: R443 (10k 0.1%) on `/driver/I_SENSE4`
- series / termination resistor: R453 (10k 0.1%) on `/driver/I_SENSE5`
- series / termination resistor: R442 (10k 0.1%) on `/driver/SENSE_N4`
- series / termination resistor: R452 (10k 0.1%) on `/driver/SENSE_N5`
- series / termination resistor: R440 (10k 0.1%) on `/driver/SENSE_P4`
- series / termination resistor: R450 (10k 0.1%) on `/driver/SENSE_P5`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U43 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE6` | R463.1, C681.1, R207.1, R732.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N6` | R462.2, R463.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P6` | R460.2, R461.1 |
| 4 | V-_4 | power_in | `-12VA` | C305.1, C271.1, C307.1, U37.2, U42.4, C255.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P7` | R470.2, R471.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N7` | R472.2, R473.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE7` | R473.1, C691.1, R208.1, R734.1 |
| 8 | V+_8 | power_in | `+12VA` | C306.1, U37.5, C270.1, C304.1, U42.8, U35.5 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C681 (100n) on `/driver/I_SENSE6`
- input / output filter capacitor: C691 (100n) on `/driver/I_SENSE7`
- pull-down resistor: R461 (10k 0.1%) on `/driver/SENSE_P6`
- pull-down resistor: R471 (10k 0.1%) on `/driver/SENSE_P7`
- series / termination resistor: R463 (10k 0.1%) on `/driver/I_SENSE6`
- series / termination resistor: R473 (10k 0.1%) on `/driver/I_SENSE7`
- series / termination resistor: R462 (10k 0.1%) on `/driver/SENSE_N6`
- series / termination resistor: R472 (10k 0.1%) on `/driver/SENSE_N7`
- series / termination resistor: R460 (10k 0.1%) on `/driver/SENSE_P6`
- series / termination resistor: R470 (10k 0.1%) on `/driver/SENSE_P7`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U60 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT0` | TP210.1, U600.1 |
| 2 | GND_2 | power_in | `GND` | U61.2, U600.2, U62.2, U63.2, C711.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U61.3, U62.3, U63.3, R710.2, R711.1, U64.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE0` | R721.2, R720.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U61.5, R729.1, U600.5, R721.1, C711.1, U62.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R729 (100k 0.1%) on `+3.3V`
- pull-up resistor: R721 (100k 0.1%) on `/driver/TRIP_SENSE0`
- series / termination resistor: R720 (10k 0.1%) on `/driver/TRIP_SENSE0`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U61 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT1` | TP211.1, U600.3 |
| 2 | GND_2 | power_in | `GND` | U60.2, U600.2, C711.2, U63.2, U62.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U60.3, U63.3, U62.3, R710.2, R711.1, U65.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE1` | R723.2, R722.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U60.5, U600.5, R729.1, C711.1, U63.5, U62.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R722 (10k 0.1%) on `/driver/TRIP_SENSE1`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U62 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT2` | TP212.1, U601.1 |
| 2 | GND_2 | power_in | `GND` | U63.2, C711.2, U600.2, U601.2, U60.2, U64.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U63.3, U60.3, U64.3, U61.3, U65.3, R711.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE2` | R725.2, R724.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U63.5, C711.1, R731.1, U600.5, U601.5, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-down resistor: R711 (10k 0.1%) on `/driver/TRIP_REF`
- pull-up resistor: R723 (100k 0.1%), R731 (100k 0.1%) on `+3.3V`
- pull-up resistor: R710 (52.3k 0.1%) on `/driver/TRIP_REF`
- series / termination resistor: R724 (10k 0.1%) on `/driver/TRIP_SENSE2`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U63 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT3` | TP213.1, U601.3 |
| 2 | GND_2 | power_in | `GND` | U62.2, C711.2, U600.2, U601.2, C712.2, U61.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U62.3, U61.3, U65.3, U60.3, U64.3, R711.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE3` | R727.2, R726.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U62.5, C711.1, U600.5, U601.5, R731.1, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R726 (10k 0.1%) on `/driver/TRIP_SENSE3`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U64 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT4` | TP214.1, U602.1 |
| 2 | GND_2 | power_in | `GND` | U65.2, C712.2, U601.2, U602.2, U62.2, U66.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U65.3, U62.3, U66.3, U63.3, U67.3, C710.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE4` | R729.2, R728.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U65.5, C712.1, U601.5, R733.1, U602.5, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R725 (100k 0.1%), R733 (100k 0.1%) on `+3.3V`
- series / termination resistor: R728 (10k 0.1%) on `/driver/TRIP_SENSE4`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U65 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT5` | TP215.1, U602.3 |
| 2 | GND_2 | power_in | `GND` | U64.2, C712.2, U601.2, U602.2, C713.2, U63.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U64.3, U63.3, U67.3, U62.3, U66.3, C710.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE5` | R731.2, R730.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U64.5, C712.1, U601.5, U602.5, R733.1, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R730 (10k 0.1%) on `/driver/TRIP_SENSE5`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U66 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT6` | TP216.1, U603.1 |
| 2 | GND_2 | power_in | `GND` | U67.2, C713.2, U602.2, U603.2, U64.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U67.3, U64.3, U65.3, C710.1, U62.3, U63.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE6` | R733.2, R732.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U67.5, C713.1, U602.5, R735.1, U603.5, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C710 (100n) on `/driver/TRIP_REF`
- pull-up resistor: R727 (100k 0.1%), R735 (100k 0.1%) on `+3.3V`
- series / termination resistor: R732 (10k 0.1%) on `/driver/TRIP_SENSE6`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U67 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT7` | TP217.1, U603.3 |
| 2 | GND_2 | power_in | `GND` | U66.2, C713.2, U602.2, U603.2, C714.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U66.3, U65.3, U64.3, C710.1, U63.3, U62.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE7` | R735.2, R734.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U66.5, C713.1, U602.5, U603.5, R735.1, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R734 (10k 0.1%) on `/driver/TRIP_SENSE7`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U80 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U80.16, C210.1, U10.7, U82.1, C200.1, U82.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA0` | R222.2, R220.2, R221.2 |
| 3 | NC_3 | passive | `GND` | U80.5, U80.10, U80.12, U80.14, U80.9, U80.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA0` | R222.1 |
| 5 | NC_5 | passive | `GND` | U80.10, U80.3, U80.12, U80.14, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA0` | R221.1, R223.1 |
| 7 | AGND_7 | passive | `/driver/AGND0` | C211.1 |
| 8 | V-_8 | power_in | `GND` | U80.9, U80.14, U80.12, U80.10, C210.2, U80.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U80.8, U80.3, U80.5, U80.10, U80.12, U80.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U80.12, U80.5, U80.14, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB0` | R224.2, R223.2, R225.2 |
| 12 | NC_12 | passive | `GND` | U80.10, U80.14, U80.5, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB0` | R225.1 |
| 14 | NC_14 | passive | `GND` | U80.12, U80.10, U80.5, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER0` | R224.1, C620.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U80.1, C210.1, U82.1, U10.7, U82.16, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C620 (1u) on `/driver/FILTER0`
- series / termination resistor: R224 (42.7k 0.1%) on `/driver/FILTER0`
- series / termination resistor: R222 (42.7k 0.1%) on `/driver/INVA0`
- series / termination resistor: R225 (42.7k 0.1%) on `/driver/INVB0`
- series / termination resistor: R221 (42.7k 0.1%), R223 (42.7k 0.1%) on `/driver/LPA0`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C211 (100n) on `/driver/AGND0`

#### U81 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U81.16, C218.1, U83.1, U83.16, C234.1, U85.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA1` | R232.2, R230.2, R231.2 |
| 3 | NC_3 | passive | `GND` | U81.5, U81.10, U81.12, U81.14, U81.9, U81.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA1` | R232.1 |
| 5 | NC_5 | passive | `GND` | U81.10, U81.3, U81.12, U81.14, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA1` | R231.1, R233.1 |
| 7 | AGND_7 | passive | `/driver/AGND1` | C219.1 |
| 8 | V-_8 | power_in | `GND` | U81.9, U81.14, U81.12, U81.10, C218.2, U81.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U81.8, U81.3, U81.5, U81.10, U81.12, U81.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U81.12, U81.5, U81.14, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB1` | R234.2, R233.2, R235.2 |
| 12 | NC_12 | passive | `GND` | U81.10, U81.14, U81.5, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB1` | R235.1 |
| 14 | NC_14 | passive | `GND` | U81.12, U81.10, U81.5, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER1` | R234.1, C630.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U81.1, C218.1, U83.1, U83.16, C234.1, U85.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C282 (EEUFR1E102) on `GND`
- input / output filter capacitor: C630 (1u) on `/driver/FILTER1`
- series / termination resistor: R234 (42.7k 0.1%) on `/driver/FILTER1`
- series / termination resistor: R232 (42.7k 0.1%) on `/driver/INVA1`
- series / termination resistor: R235 (42.7k 0.1%) on `/driver/INVB1`
- series / termination resistor: R231 (42.7k 0.1%), R233 (42.7k 0.1%) on `/driver/LPA1`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C219 (100n) on `/driver/AGND1`

#### U82 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U82.16, C226.1, C210.1, U80.16, U84.1, U80.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA2` | R242.2, R240.2, R241.2 |
| 3 | NC_3 | passive | `GND` | U82.5, U82.10, U82.12, U82.14, U82.9, U82.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA2` | R242.1 |
| 5 | NC_5 | passive | `GND` | U82.10, U82.3, U82.12, U82.14, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA2` | R241.1, R243.1 |
| 7 | AGND_7 | passive | `/driver/AGND2` | C227.1 |
| 8 | V-_8 | power_in | `GND` | U82.9, U82.14, C226.2, U82.12, U82.10, U82.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U82.8, U82.3, U82.5, U82.10, U82.12, U82.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U82.12, U82.5, U82.14, U82.3, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB2` | R244.2, R243.2, R245.2 |
| 12 | NC_12 | passive | `GND` | U82.10, U82.14, U82.5, U82.3, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB2` | R245.1 |
| 14 | NC_14 | passive | `GND` | U82.12, U82.10, U82.5, U82.3, U82.8, C226.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER2` | R244.1, C640.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U82.1, C226.1, C210.1, U84.1, U80.16, U84.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C640 (1u) on `/driver/FILTER2`
- series / termination resistor: R244 (42.7k 0.1%) on `/driver/FILTER2`
- series / termination resistor: R242 (42.7k 0.1%) on `/driver/INVA2`
- series / termination resistor: R245 (42.7k 0.1%) on `/driver/INVB2`
- series / termination resistor: R241 (42.7k 0.1%), R243 (42.7k 0.1%) on `/driver/LPA2`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C227 (100n) on `/driver/AGND2`

#### U83 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U83.16, C234.1, C218.1, U81.16, U85.1, U81.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA3` | R252.2, R250.2, R251.2 |
| 3 | NC_3 | passive | `GND` | U83.5, U83.10, U83.12, U83.14, U83.9, U83.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA3` | R252.1 |
| 5 | NC_5 | passive | `GND` | U83.10, U83.3, U83.12, U83.14, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA3` | R251.1, R253.1 |
| 7 | AGND_7 | passive | `/driver/AGND3` | C235.1 |
| 8 | V-_8 | power_in | `GND` | U83.9, U83.14, C234.2, U83.12, U83.10, U83.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U83.8, U83.3, U83.5, U83.10, U83.12, U83.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U83.12, U83.5, U83.14, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB3` | R254.2, R253.2, R255.2 |
| 12 | NC_12 | passive | `GND` | U83.10, U83.14, U83.5, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB3` | R255.1 |
| 14 | NC_14 | passive | `GND` | U83.12, U83.10, U83.5, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER3` | R254.1, C650.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U83.1, C234.1, C218.1, U85.1, U81.16, U85.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C650 (1u) on `/driver/FILTER3`
- series / termination resistor: R254 (42.7k 0.1%) on `/driver/FILTER3`
- series / termination resistor: R252 (42.7k 0.1%) on `/driver/INVA3`
- series / termination resistor: R255 (42.7k 0.1%) on `/driver/INVB3`
- series / termination resistor: R251 (42.7k 0.1%), R253 (42.7k 0.1%) on `/driver/LPA3`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C235 (100n) on `/driver/AGND3`

#### U84 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U84.16, C242.1, C226.1, U82.16, U86.1, U82.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA4` | R262.2, R260.2, R261.2 |
| 3 | NC_3 | passive | `GND` | U84.5, U84.10, U84.12, U84.14, U84.9, U84.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA4` | R262.1 |
| 5 | NC_5 | passive | `GND` | U84.3, U84.10, U84.12, U84.14, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA4` | R261.1, R263.1 |
| 7 | AGND_7 | passive | `/driver/AGND4` | C243.1 |
| 8 | V-_8 | power_in | `GND` | U84.9, U84.14, U84.12, C242.2, U84.10, U84.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U84.8, U84.3, U84.5, U84.10, U84.12, U84.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U84.12, U84.5, U84.14, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB4` | R264.2, R263.2, R265.2 |
| 12 | NC_12 | passive | `GND` | U84.14, U84.10, U84.5, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB4` | R265.1 |
| 14 | NC_14 | passive | `GND` | U84.12, U84.10, U84.5, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER4` | R264.1, C660.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U84.1, C242.1, C226.1, U86.1, U86.16, U82.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C660 (1u) on `/driver/FILTER4`
- series / termination resistor: R264 (42.7k 0.1%) on `/driver/FILTER4`
- series / termination resistor: R262 (42.7k 0.1%) on `/driver/INVA4`
- series / termination resistor: R265 (42.7k 0.1%) on `/driver/INVB4`
- series / termination resistor: R261 (42.7k 0.1%), R263 (42.7k 0.1%) on `/driver/LPA4`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C243 (100n) on `/driver/AGND4`

#### U85 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U85.16, C250.1, C234.1, U83.16, U87.1, U83.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA5` | R272.2, R270.2, R271.2 |
| 3 | NC_3 | passive | `GND` | U85.5, U85.10, U85.12, U85.14, U85.9, U85.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA5` | R272.1 |
| 5 | NC_5 | passive | `GND` | U85.3, U85.10, U85.12, U85.14, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA5` | R271.1, R273.1 |
| 7 | AGND_7 | passive | `/driver/AGND5` | C251.1 |
| 8 | V-_8 | power_in | `GND` | U85.9, U85.14, C250.2, U85.12, U85.10, U85.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U85.8, U85.3, U85.5, U85.10, U85.12, U85.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U85.12, U85.5, U85.14, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB5` | R274.2, R273.2, R275.2 |
| 12 | NC_12 | passive | `GND` | U85.14, U85.10, U85.5, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB5` | R275.1 |
| 14 | NC_14 | passive | `GND` | U85.12, U85.10, U85.5, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER5` | R274.1, C670.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U85.1, C250.1, C234.1, U87.1, U87.16, U83.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C670 (1u) on `/driver/FILTER5`
- series / termination resistor: R274 (42.7k 0.1%) on `/driver/FILTER5`
- series / termination resistor: R272 (42.7k 0.1%) on `/driver/INVA5`
- series / termination resistor: R275 (42.7k 0.1%) on `/driver/INVB5`
- series / termination resistor: R271 (42.7k 0.1%), R273 (42.7k 0.1%) on `/driver/LPA5`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C251 (100n) on `/driver/AGND5`

#### U86 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U86.16, C258.1, C242.1, U84.16, U84.1, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA6` | R282.2, R280.2, R281.2 |
| 3 | NC_3 | passive | `GND` | U86.5, U86.10, U86.12, U86.14, U86.9, U86.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA6` | R282.1 |
| 5 | NC_5 | passive | `GND` | U86.10, U86.3, U86.12, U86.14, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA6` | R281.1, R283.1 |
| 7 | AGND_7 | passive | `/driver/AGND6` | C259.1 |
| 8 | V-_8 | power_in | `GND` | U86.9, U86.14, C258.2, U86.12, U86.10, U86.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U86.8, U86.3, U86.5, U86.10, U86.12, U86.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U86.12, U86.5, U86.14, U86.3, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB6` | R284.2, R283.2, R285.2 |
| 12 | NC_12 | passive | `GND` | U86.10, U86.14, U86.5, U86.3, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB6` | R285.1 |
| 14 | NC_14 | passive | `GND` | U86.12, U86.10, U86.5, U86.3, U86.8, C258.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER6` | R284.1, C680.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U86.1, C258.1, C242.1, U84.16, U84.1, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C680 (1u) on `/driver/FILTER6`
- series / termination resistor: R284 (42.7k 0.1%) on `/driver/FILTER6`
- series / termination resistor: R282 (42.7k 0.1%) on `/driver/INVA6`
- series / termination resistor: R285 (42.7k 0.1%) on `/driver/INVB6`
- series / termination resistor: R281 (42.7k 0.1%), R283 (42.7k 0.1%) on `/driver/LPA6`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C259 (100n) on `/driver/AGND6`

#### U87 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U87.16, C266.1, C250.1, U85.16, U85.1, C234.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA7` | R292.2, R290.2, R291.2 |
| 3 | NC_3 | passive | `GND` | U87.5, U87.10, U87.12, U87.14, U87.9, U87.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA7` | R292.1 |
| 5 | NC_5 | passive | `GND` | U87.10, U87.3, U87.12, U87.14, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA7` | R291.1, R293.1 |
| 7 | AGND_7 | passive | `/driver/AGND7` | C267.1 |
| 8 | V-_8 | power_in | `GND` | U87.9, U87.14, C266.2, U87.12, U87.10, U87.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U87.8, U87.3, U87.5, U87.10, U87.12, U87.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U87.12, U87.5, U87.14, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB7` | R294.2, R293.2, R295.2 |
| 12 | NC_12 | passive | `GND` | U87.10, U87.14, U87.5, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB7` | R295.1 |
| 14 | NC_14 | passive | `GND` | U87.12, U87.10, U87.5, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER7` | R294.1, C690.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U87.1, C266.1, C250.1, U85.16, U85.1, C234.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C690 (1u) on `/driver/FILTER7`
- series / termination resistor: R294 (42.7k 0.1%) on `/driver/FILTER7`
- series / termination resistor: R292 (42.7k 0.1%) on `/driver/INVA7`
- series / termination resistor: R295 (42.7k 0.1%) on `/driver/INVB7`
- series / termination resistor: R291 (42.7k 0.1%), R293 (42.7k 0.1%) on `/driver/LPA7`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C267 (100n) on `/driver/AGND7`

#### U600 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT0` | TP210.1, U60.1 |
| 2 | GND_2 | power_in | `GND` | C711.2, U63.2, U61.2, U62.2, U60.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT1` | TP211.1, U61.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U600.6, U601.4, U601.6, R712.2, U602.4, U602.6 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C711.1, U63.5, U62.5, U61.5, U60.5, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U600.4, U601.6, U601.4, R712.2, U602.6, U602.4 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U601 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT2` | TP212.1, U62.1 |
| 2 | GND_2 | power_in | `GND` | C712.2, U65.2, C711.2, U63.2, U64.2, U62.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT3` | TP213.1, U63.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U601.6, U600.4, U602.4, U600.6, U602.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C712.1, U65.5, U64.5, U63.5, U62.5, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U601.4, U600.6, U602.6, U600.4, U602.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R712 (4.7k) on `/DRIVER_FAULT_N`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U602 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT4` | TP214.1, U64.1 |
| 2 | GND_2 | power_in | `GND` | C713.2, U67.2, C712.2, U65.2, U66.2, U64.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT5` | TP215.1, U65.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U602.6, U603.4, U601.4, U603.6, U601.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C713.1, U67.5, U66.5, U65.5, U64.5, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U602.4, U603.6, U601.6, U603.4, U601.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U603 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT6` | TP216.1, U66.1 |
| 2 | GND_2 | power_in | `GND` | C714.2, C713.2, U67.2, U66.2, U602.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT7` | TP217.1, U67.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U603.6, U602.4, U602.6, U601.4, U601.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C714.1, U67.5, U66.5, R735.1, C713.1, U602.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U603.4, U602.6, U602.4, U601.6, U601.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### C200 — 100n, C

C200 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C201 — 1u, C

C201 — 1u, C_0805_2012Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C202 — 100n, C

C202 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C203 — 150n, C

C203 — 150n, C_0603_1608Metric — `/driver/DAC_REF` ↔ `GND` — soft-start / bias capacitor for U10 (pin 1 → 2).

#### C204 — 100n, C

C204 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C205 — 100n, C

C205 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C210 — 100n, C

C210 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C211 — 100n, C

C211 — 100n, C_0603_1608Metric — `/driver/AGND0` ↔ `GND` — supply decoupling for U80 (pin 1 → 2).

#### C212 — CAA572X7R1E107M670LJ, C

C212 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF0` ↔ `FG0_OUT` — supply feed / filter for U20 (pin 1 → 2).

#### C213 — 100n, C

C213 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C214 — 100n, C

C214 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C215 — 100n, C

C215 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C218 — 100n, C

C218 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C219 — 100n, C

C219 — 100n, C_0603_1608Metric — `/driver/AGND1` ↔ `GND` — supply decoupling for U81 (pin 1 → 2).

#### C220 — CAA572X7R1E107M670LJ, C

C220 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF1` ↔ `FG1_OUT` — supply feed / filter for U21 (pin 1 → 2).

#### C221 — 100n, C

C221 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C222 — 100n, C

C222 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C223 — 100n, C

C223 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C226 — 100n, C

C226 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C227 — 100n, C

C227 — 100n, C_0603_1608Metric — `/driver/AGND2` ↔ `GND` — supply decoupling for U82 (pin 1 → 2).

#### C228 — CAA572X7R1E107M670LJ, C

C228 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF2` ↔ `FG2_OUT` — supply feed / filter for U22 (pin 1 → 2).

#### C229 — 100n, C

C229 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C230 — 100n, C

C230 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C231 — 100n, C

C231 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C234 — 100n, C

C234 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C235 — 100n, C

C235 — 100n, C_0603_1608Metric — `/driver/AGND3` ↔ `GND` — supply decoupling for U83 (pin 1 → 2).

#### C236 — CAA572X7R1E107M670LJ, C

C236 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF3` ↔ `FG3_OUT` — supply feed / filter for U23 (pin 1 → 2).

#### C237 — 100n, C

C237 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C238 — 100n, C

C238 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C239 — 100n, C

C239 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C242 — 100n, C

C242 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C243 — 100n, C

C243 — 100n, C_0603_1608Metric — `/driver/AGND4` ↔ `GND` — supply decoupling for U84 (pin 1 → 2).

#### C244 — CAA572X7R1E107M670LJ, C

C244 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF4` ↔ `FG4_OUT` — supply feed / filter for U24 (pin 1 → 2).

#### C245 — 100n, C

C245 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C246 — 100n, C

C246 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C247 — 100n, C

C247 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C250 — 100n, C

C250 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C251 — 100n, C

C251 — 100n, C_0603_1608Metric — `/driver/AGND5` ↔ `GND` — supply decoupling for U85 (pin 1 → 2).

#### C252 — CAA572X7R1E107M670LJ, C

C252 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF5` ↔ `FG5_OUT` — supply feed / filter for U25 (pin 1 → 2).

#### C253 — 100n, C

C253 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C254 — 100n, C

C254 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C255 — 100n, C

C255 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C258 — 100n, C

C258 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C259 — 100n, C

C259 — 100n, C_0603_1608Metric — `/driver/AGND6` ↔ `GND` — supply decoupling for U86 (pin 1 → 2).

#### C260 — CAA572X7R1E107M670LJ, C

C260 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF6` ↔ `FG6_OUT` — supply feed / filter for U26 (pin 1 → 2).

#### C261 — 100n, C

C261 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C262 — 100n, C

C262 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C263 — 100n, C

C263 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C266 — 100n, C

C266 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C267 — 100n, C

C267 — 100n, C_0603_1608Metric — `/driver/AGND7` ↔ `GND` — supply decoupling for U87 (pin 1 → 2).

#### C268 — CAA572X7R1E107M670LJ, C

C268 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF7` ↔ `FG7_OUT` — supply feed / filter for U27 (pin 1 → 2).

#### C269 — 100n, C

C269 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C270 — 100n, C

C270 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C271 — 100n, C

C271 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C280 — 100n, C

C280 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C281 — 100n, C

C281 — 100n, C_0603_1608Metric — `/driver/BIAS_DIV` ↔ `GND` — filter capacitor to ground for U39 (pin 1 → 2).

#### C282 — EEUFR1E102, C_Polarized

C282 — EEUFR1E102, CP_Radial_D10.0mm_P5.00mm — `/driver/VMID_7V5` ↔ `GND` — filter capacitor to ground for U81 (pin 1 → 2).

#### C283 — 100n, C

C283 — 100n, C_0603_1608Metric — `/driver/VMID_7V5` ↔ `GND` — filter capacitor to ground for TP823 (pin 1 → 2).

#### C290 — 100n, C

C290 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C291 — 100n, C

C291 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C292 — 100n, C

C292 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C293 — 100n, C

C293 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C294 — 100n, C

C294 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C295 — 100n, C

C295 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C296 — 100n, C

C296 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C297 — 100n, C

C297 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C300 — 100n, C

C300 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C301 — 100n, C

C301 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C302 — 100n, C

C302 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C303 — 100n, C

C303 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C304 — 100n, C

C304 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C305 — 100n, C

C305 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C306 — 100n, C

C306 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C307 — 100n, C

C307 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C620 — 1u, C

C620 — 1u, C_0805_2012Metric — `/driver/FILTER0` ↔ `/driver/CMD_AC0` — input / output filter capacitor for U80 (pin 1 → 2).

#### C621 — 100n, C

C621 — 100n, C_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SENSE_AC0` — input / output filter capacitor for U40 (pin 1 → 2).

#### C622 — 150p, C

C622 — 150p, C_0603_1608Metric — `/driver/COMP0` ↔ `/driver/FEEDBACK0` — input / output filter capacitor for U30 (pin 1 → 2).

#### C630 — 1u, C

C630 — 1u, C_0805_2012Metric — `/driver/FILTER1` ↔ `/driver/CMD_AC1` — input / output filter capacitor for U81 (pin 1 → 2).

#### C631 — 100n, C

C631 — 100n, C_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SENSE_AC1` — input / output filter capacitor for U40 (pin 1 → 2).

#### C632 — 150p, C

C632 — 150p, C_0603_1608Metric — `/driver/COMP1` ↔ `/driver/FEEDBACK1` — input / output filter capacitor for U31 (pin 1 → 2).

#### C640 — 1u, C

C640 — 1u, C_0805_2012Metric — `/driver/FILTER2` ↔ `/driver/CMD_AC2` — input / output filter capacitor for U82 (pin 1 → 2).

#### C641 — 100n, C

C641 — 100n, C_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SENSE_AC2` — input / output filter capacitor for U41 (pin 1 → 2).

#### C642 — 150p, C

C642 — 150p, C_0603_1608Metric — `/driver/COMP2` ↔ `/driver/FEEDBACK2` — input / output filter capacitor for U32 (pin 1 → 2).

#### C650 — 1u, C

C650 — 1u, C_0805_2012Metric — `/driver/FILTER3` ↔ `/driver/CMD_AC3` — input / output filter capacitor for U83 (pin 1 → 2).

#### C651 — 100n, C

C651 — 100n, C_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SENSE_AC3` — input / output filter capacitor for U41 (pin 1 → 2).

#### C652 — 150p, C

C652 — 150p, C_0603_1608Metric — `/driver/COMP3` ↔ `/driver/FEEDBACK3` — input / output filter capacitor for U33 (pin 1 → 2).

#### C660 — 1u, C

C660 — 1u, C_0805_2012Metric — `/driver/FILTER4` ↔ `/driver/CMD_AC4` — input / output filter capacitor for U84 (pin 1 → 2).

#### C661 — 100n, C

C661 — 100n, C_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SENSE_AC4` — input / output filter capacitor for U42 (pin 1 → 2).

#### C662 — 150p, C

C662 — 150p, C_0603_1608Metric — `/driver/COMP4` ↔ `/driver/FEEDBACK4` — input / output filter capacitor for U34 (pin 1 → 2).

#### C670 — 1u, C

C670 — 1u, C_0805_2012Metric — `/driver/FILTER5` ↔ `/driver/CMD_AC5` — input / output filter capacitor for U85 (pin 1 → 2).

#### C671 — 100n, C

C671 — 100n, C_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SENSE_AC5` — input / output filter capacitor for U42 (pin 1 → 2).

#### C672 — 150p, C

C672 — 150p, C_0603_1608Metric — `/driver/COMP5` ↔ `/driver/FEEDBACK5` — input / output filter capacitor for U35 (pin 1 → 2).

#### C680 — 1u, C

C680 — 1u, C_0805_2012Metric — `/driver/FILTER6` ↔ `/driver/CMD_AC6` — input / output filter capacitor for U86 (pin 1 → 2).

#### C681 — 100n, C

C681 — 100n, C_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SENSE_AC6` — input / output filter capacitor for U43 (pin 1 → 2).

#### C682 — 150p, C

C682 — 150p, C_0603_1608Metric — `/driver/COMP6` ↔ `/driver/FEEDBACK6` — input / output filter capacitor for U36 (pin 1 → 2).

#### C690 — 1u, C

C690 — 1u, C_0805_2012Metric — `/driver/FILTER7` ↔ `/driver/CMD_AC7` — input / output filter capacitor for U87 (pin 1 → 2).

#### C691 — 100n, C

C691 — 100n, C_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SENSE_AC7` — input / output filter capacitor for U43 (pin 1 → 2).

#### C692 — 150p, C

C692 — 150p, C_0603_1608Metric — `/driver/COMP7` ↔ `/driver/FEEDBACK7` — input / output filter capacitor for U37 (pin 1 → 2).

#### C710 — 100n, C

C710 — 100n, C_0603_1608Metric — `/driver/TRIP_REF` ↔ `GND` — filter capacitor to ground for U66 (pin 1 → 2).

#### C711 — 100n, C

C711 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C712 — 100n, C

C712 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C713 — 100n, C

C713 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C714 — 100n, C

C714 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### R20 — 1.00 0.1% 0.5W, R

R20 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG0_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R21 — 1.00 0.1% 0.5W, R

R21 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG1_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R22 — 1.00 0.1% 0.5W, R

R22 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG2_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R23 — 1.00 0.1% 0.5W, R

R23 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG3_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R24 — 1.00 0.1% 0.5W, R

R24 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG4_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R25 — 1.00 0.1% 0.5W, R

R25 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG5_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R26 — 1.00 0.1% 0.5W, R

R26 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG6_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R27 — 1.00 0.1% 0.5W, R

R27 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG7_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R200 — 20k 0.1%, R

R200 — 20k 0.1%, R_0603_1608Metric — `CURRENT_SUM` ↔ `/driver/SUM_NODE` — supply feed / filter for U38 (pin 1 → 2).

#### R201 — 10k 0.1%, R

R201 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R202 — 10k 0.1%, R

R202 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R203 — 10k 0.1%, R

R203 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R204 — 10k 0.1%, R

R204 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R205 — 10k 0.1%, R

R205 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R206 — 10k 0.1%, R

R206 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R207 — 10k 0.1%, R

R207 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R208 — 10k 0.1%, R

R208 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R220 — 42.7k 0.1%, R

R220 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC0` ↔ `/driver/SA0` — supply feed / filter for U10 (pin 1 → 2).

#### R221 — 42.7k 0.1%, R

R221 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA0` ↔ `/driver/SA0` — series / termination resistor for U80 (pin 1 → 2).

#### R222 — 42.7k 0.1%, R

R222 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA0` ↔ `/driver/SA0` — series / termination resistor for U80 (pin 1 → 2).

#### R223 — 42.7k 0.1%, R

R223 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R224 — 42.7k 0.1%, R

R224 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R225 — 42.7k 0.1%, R

R225 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R230 — 42.7k 0.1%, R

R230 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC1` ↔ `/driver/SA1` — supply feed / filter for U10 (pin 1 → 2).

#### R231 — 42.7k 0.1%, R

R231 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA1` ↔ `/driver/SA1` — series / termination resistor for U81 (pin 1 → 2).

#### R232 — 42.7k 0.1%, R

R232 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA1` ↔ `/driver/SA1` — series / termination resistor for U81 (pin 1 → 2).

#### R233 — 42.7k 0.1%, R

R233 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R234 — 42.7k 0.1%, R

R234 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R235 — 42.7k 0.1%, R

R235 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R240 — 42.7k 0.1%, R

R240 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC2` ↔ `/driver/SA2` — supply feed / filter for U10 (pin 1 → 2).

#### R241 — 42.7k 0.1%, R

R241 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA2` ↔ `/driver/SA2` — series / termination resistor for U82 (pin 1 → 2).

#### R242 — 42.7k 0.1%, R

R242 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA2` ↔ `/driver/SA2` — series / termination resistor for U82 (pin 1 → 2).

#### R243 — 42.7k 0.1%, R

R243 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R244 — 42.7k 0.1%, R

R244 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R245 — 42.7k 0.1%, R

R245 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R250 — 42.7k 0.1%, R

R250 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC3` ↔ `/driver/SA3` — supply feed / filter for U10 (pin 1 → 2).

#### R251 — 42.7k 0.1%, R

R251 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA3` ↔ `/driver/SA3` — series / termination resistor for U83 (pin 1 → 2).

#### R252 — 42.7k 0.1%, R

R252 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA3` ↔ `/driver/SA3` — series / termination resistor for U83 (pin 1 → 2).

#### R253 — 42.7k 0.1%, R

R253 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R254 — 42.7k 0.1%, R

R254 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R255 — 42.7k 0.1%, R

R255 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R260 — 42.7k 0.1%, R

R260 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC4` ↔ `/driver/SA4` — supply feed / filter for U10 (pin 1 → 2).

#### R261 — 42.7k 0.1%, R

R261 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA4` ↔ `/driver/SA4` — series / termination resistor for U84 (pin 1 → 2).

#### R262 — 42.7k 0.1%, R

R262 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA4` ↔ `/driver/SA4` — series / termination resistor for U84 (pin 1 → 2).

#### R263 — 42.7k 0.1%, R

R263 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R264 — 42.7k 0.1%, R

R264 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R265 — 42.7k 0.1%, R

R265 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R270 — 42.7k 0.1%, R

R270 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC5` ↔ `/driver/SA5` — supply feed / filter for U10 (pin 1 → 2).

#### R271 — 42.7k 0.1%, R

R271 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA5` ↔ `/driver/SA5` — series / termination resistor for U85 (pin 1 → 2).

#### R272 — 42.7k 0.1%, R

R272 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA5` ↔ `/driver/SA5` — series / termination resistor for U85 (pin 1 → 2).

#### R273 — 42.7k 0.1%, R

R273 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R274 — 42.7k 0.1%, R

R274 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R275 — 42.7k 0.1%, R

R275 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R280 — 42.7k 0.1%, R

R280 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC6` ↔ `/driver/SA6` — supply feed / filter for U10 (pin 1 → 2).

#### R281 — 42.7k 0.1%, R

R281 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA6` ↔ `/driver/SA6` — series / termination resistor for U86 (pin 1 → 2).

#### R282 — 42.7k 0.1%, R

R282 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA6` ↔ `/driver/SA6` — series / termination resistor for U86 (pin 1 → 2).

#### R283 — 42.7k 0.1%, R

R283 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R284 — 42.7k 0.1%, R

R284 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R285 — 42.7k 0.1%, R

R285 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R290 — 42.7k 0.1%, R

R290 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC7` ↔ `/driver/SA7` — supply feed / filter for U10 (pin 1 → 2).

#### R291 — 42.7k 0.1%, R

R291 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA7` ↔ `/driver/SA7` — series / termination resistor for U87 (pin 1 → 2).

#### R292 — 42.7k 0.1%, R

R292 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA7` ↔ `/driver/SA7` — series / termination resistor for U87 (pin 1 → 2).

#### R293 — 42.7k 0.1%, R

R293 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R294 — 42.7k 0.1%, R

R294 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R295 — 42.7k 0.1%, R

R295 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R360 — 10k, R

R360 — 10k, R_0603_1608Metric — `/driver/SENSE_AC0` ↔ `/driver/FEEDBACK0` — series / termination resistor for U30 (pin 1 → 2).

#### R361 — 15k, R

R361 — 15k, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/BUF_IN0` — supply feed / filter for U30 (pin 1 → 2).

#### R362 — 10k, R

R362 — 10k, R_0603_1608Metric — `/driver/SENSE_AC1` ↔ `/driver/FEEDBACK1` — series / termination resistor for U31 (pin 1 → 2).

#### R363 — 15k, R

R363 — 15k, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/BUF_IN1` — supply feed / filter for U31 (pin 1 → 2).

#### R364 — 10k, R

R364 — 10k, R_0603_1608Metric — `/driver/SENSE_AC2` ↔ `/driver/FEEDBACK2` — series / termination resistor for U32 (pin 1 → 2).

#### R365 — 15k, R

R365 — 15k, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/BUF_IN2` — supply feed / filter for U32 (pin 1 → 2).

#### R366 — 10k, R

R366 — 10k, R_0603_1608Metric — `/driver/SENSE_AC3` ↔ `/driver/FEEDBACK3` — series / termination resistor for U33 (pin 1 → 2).

#### R367 — 15k, R

R367 — 15k, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/BUF_IN3` — supply feed / filter for U33 (pin 1 → 2).

#### R368 — 10k, R

R368 — 10k, R_0603_1608Metric — `/driver/SENSE_AC4` ↔ `/driver/FEEDBACK4` — series / termination resistor for U34 (pin 1 → 2).

#### R369 — 15k, R

R369 — 15k, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/BUF_IN4` — supply feed / filter for U34 (pin 1 → 2).

#### R370 — 10k, R

R370 — 10k, R_0603_1608Metric — `/driver/SENSE_AC5` ↔ `/driver/FEEDBACK5` — series / termination resistor for U35 (pin 1 → 2).

#### R371 — 15k, R

R371 — 15k, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/BUF_IN5` — supply feed / filter for U35 (pin 1 → 2).

#### R372 — 10k, R

R372 — 10k, R_0603_1608Metric — `/driver/SENSE_AC6` ↔ `/driver/FEEDBACK6` — series / termination resistor for U36 (pin 1 → 2).

#### R373 — 15k, R

R373 — 15k, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/BUF_IN6` — supply feed / filter for U36 (pin 1 → 2).

#### R374 — 10k, R

R374 — 10k, R_0603_1608Metric — `/driver/SENSE_AC7` ↔ `/driver/FEEDBACK7` — series / termination resistor for U37 (pin 1 → 2).

#### R375 — 15k, R

R375 — 15k, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/BUF_IN7` — supply feed / filter for U37 (pin 1 → 2).

#### R380 — 10k, R

R380 — 10k, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/BIAS_DIV` — pull-up resistor for U20 (pin 1 → 2).

#### R381 — 10k, R

R381 — 10k, R_0603_1608Metric — `/driver/BIAS_DIV` ↔ `GND` — pull-down resistor for U20 (pin 1 → 2).

#### R382 — 10k, R

R382 — 10k, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/VMID_7V5` — pull-up resistor for TP823 (pin 1 → 2).

#### R383 — 10k, R

R383 — 10k, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `GND` — pull-down resistor for TP823 (pin 1 → 2).

#### R400 — 10k 0.1%, R

R400 — 10k 0.1%, R_0603_1608Metric — `FG0_RETURN` ↔ `/driver/SENSE_P0` — series / termination resistor for U40 (pin 1 → 2).

#### R401 — 10k 0.1%, R

R401 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P0` ↔ `GND` — pull-down resistor for U40 (pin 1 → 2).

#### R402 — 10k 0.1%, R

R402 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N0` — series / termination resistor for U40 (pin 1 → 2).

#### R403 — 10k 0.1%, R

R403 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SENSE_N0` — series / termination resistor for U40 (pin 1 → 2).

#### R410 — 10k 0.1%, R

R410 — 10k 0.1%, R_0603_1608Metric — `FG1_RETURN` ↔ `/driver/SENSE_P1` — series / termination resistor for U40 (pin 1 → 2).

#### R411 — 10k 0.1%, R

R411 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P1` ↔ `GND` — pull-down resistor for U40 (pin 1 → 2).

#### R412 — 10k 0.1%, R

R412 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N1` — series / termination resistor for U40 (pin 1 → 2).

#### R413 — 10k 0.1%, R

R413 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SENSE_N1` — series / termination resistor for U40 (pin 1 → 2).

#### R420 — 10k 0.1%, R

R420 — 10k 0.1%, R_0603_1608Metric — `FG2_RETURN` ↔ `/driver/SENSE_P2` — series / termination resistor for U41 (pin 1 → 2).

#### R421 — 10k 0.1%, R

R421 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P2` ↔ `GND` — pull-down resistor for U41 (pin 1 → 2).

#### R422 — 10k 0.1%, R

R422 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N2` — series / termination resistor for U41 (pin 1 → 2).

#### R423 — 10k 0.1%, R

R423 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SENSE_N2` — series / termination resistor for U41 (pin 1 → 2).

#### R430 — 10k 0.1%, R

R430 — 10k 0.1%, R_0603_1608Metric — `FG3_RETURN` ↔ `/driver/SENSE_P3` — series / termination resistor for U41 (pin 1 → 2).

#### R431 — 10k 0.1%, R

R431 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P3` ↔ `GND` — pull-down resistor for U41 (pin 1 → 2).

#### R432 — 10k 0.1%, R

R432 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N3` — series / termination resistor for U41 (pin 1 → 2).

#### R433 — 10k 0.1%, R

R433 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SENSE_N3` — series / termination resistor for U41 (pin 1 → 2).

#### R440 — 10k 0.1%, R

R440 — 10k 0.1%, R_0603_1608Metric — `FG4_RETURN` ↔ `/driver/SENSE_P4` — series / termination resistor for U42 (pin 1 → 2).

#### R441 — 10k 0.1%, R

R441 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P4` ↔ `GND` — pull-down resistor for U42 (pin 1 → 2).

#### R442 — 10k 0.1%, R

R442 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N4` — series / termination resistor for U42 (pin 1 → 2).

#### R443 — 10k 0.1%, R

R443 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SENSE_N4` — series / termination resistor for U42 (pin 1 → 2).

#### R450 — 10k 0.1%, R

R450 — 10k 0.1%, R_0603_1608Metric — `FG5_RETURN` ↔ `/driver/SENSE_P5` — series / termination resistor for U42 (pin 1 → 2).

#### R451 — 10k 0.1%, R

R451 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P5` ↔ `GND` — pull-down resistor for U42 (pin 1 → 2).

#### R452 — 10k 0.1%, R

R452 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N5` — series / termination resistor for U42 (pin 1 → 2).

#### R453 — 10k 0.1%, R

R453 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SENSE_N5` — series / termination resistor for U42 (pin 1 → 2).

#### R460 — 10k 0.1%, R

R460 — 10k 0.1%, R_0603_1608Metric — `FG6_RETURN` ↔ `/driver/SENSE_P6` — series / termination resistor for U43 (pin 1 → 2).

#### R461 — 10k 0.1%, R

R461 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P6` ↔ `GND` — pull-down resistor for U43 (pin 1 → 2).

#### R462 — 10k 0.1%, R

R462 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N6` — series / termination resistor for U43 (pin 1 → 2).

#### R463 — 10k 0.1%, R

R463 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SENSE_N6` — series / termination resistor for U43 (pin 1 → 2).

#### R470 — 10k 0.1%, R

R470 — 10k 0.1%, R_0603_1608Metric — `FG7_RETURN` ↔ `/driver/SENSE_P7` — series / termination resistor for U43 (pin 1 → 2).

#### R471 — 10k 0.1%, R

R471 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P7` ↔ `GND` — pull-down resistor for U43 (pin 1 → 2).

#### R472 — 10k 0.1%, R

R472 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N7` — series / termination resistor for U43 (pin 1 → 2).

#### R473 — 10k 0.1%, R

R473 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SENSE_N7` — series / termination resistor for U43 (pin 1 → 2).

#### R600 — 10.7k 1%, R

R600 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG0` — pull-up resistor for U20 (pin 1 → 2).

#### R601 — 10.7k 1%, R

R601 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG1` — pull-up resistor for U21 (pin 1 → 2).

#### R602 — 10.7k 1%, R

R602 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG2` — pull-up resistor for U22 (pin 1 → 2).

#### R603 — 10.7k 1%, R

R603 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG3` — pull-up resistor for U23 (pin 1 → 2).

#### R604 — 10.7k 1%, R

R604 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG4` — pull-up resistor for U24 (pin 1 → 2).

#### R605 — 10.7k 1%, R

R605 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG5` — pull-up resistor for U25 (pin 1 → 2).

#### R606 — 10.7k 1%, R

R606 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG6` — pull-up resistor for U26 (pin 1 → 2).

#### R607 — 10.7k 1%, R

R607 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG7` — pull-up resistor for U27 (pin 1 → 2).

#### R620 — 10k, R

R620 — 10k, R_0603_1608Metric — `/driver/CMD_AC0` ↔ `/driver/CMD_BIASED0` — series / termination resistor for U30 (pin 1 → 2).

#### R621 — 1.40k, R

R621 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED0` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R622 — 10M, R

R622 — 10M, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/FEEDBACK0` — supply feed / filter for U30 (pin 1 → 2).

#### R623 — 330k, R

R623 — 330k, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/COMP0` — supply feed / filter for U30 (pin 1 → 2).

#### R630 — 10k, R

R630 — 10k, R_0603_1608Metric — `/driver/CMD_AC1` ↔ `/driver/CMD_BIASED1` — series / termination resistor for U31 (pin 1 → 2).

#### R631 — 1.40k, R

R631 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED1` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R632 — 10M, R

R632 — 10M, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/FEEDBACK1` — supply feed / filter for U31 (pin 1 → 2).

#### R633 — 330k, R

R633 — 330k, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/COMP1` — supply feed / filter for U31 (pin 1 → 2).

#### R640 — 10k, R

R640 — 10k, R_0603_1608Metric — `/driver/CMD_AC2` ↔ `/driver/CMD_BIASED2` — series / termination resistor for U32 (pin 1 → 2).

#### R641 — 1.40k, R

R641 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED2` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R642 — 10M, R

R642 — 10M, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/FEEDBACK2` — supply feed / filter for U32 (pin 1 → 2).

#### R643 — 330k, R

R643 — 330k, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/COMP2` — supply feed / filter for U32 (pin 1 → 2).

#### R650 — 10k, R

R650 — 10k, R_0603_1608Metric — `/driver/CMD_AC3` ↔ `/driver/CMD_BIASED3` — series / termination resistor for U33 (pin 1 → 2).

#### R651 — 1.40k, R

R651 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED3` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R652 — 10M, R

R652 — 10M, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/FEEDBACK3` — supply feed / filter for U33 (pin 1 → 2).

#### R653 — 330k, R

R653 — 330k, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/COMP3` — supply feed / filter for U33 (pin 1 → 2).

#### R660 — 10k, R

R660 — 10k, R_0603_1608Metric — `/driver/CMD_AC4` ↔ `/driver/CMD_BIASED4` — series / termination resistor for U34 (pin 1 → 2).

#### R661 — 1.40k, R

R661 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED4` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R662 — 10M, R

R662 — 10M, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/FEEDBACK4` — supply feed / filter for U34 (pin 1 → 2).

#### R663 — 330k, R

R663 — 330k, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/COMP4` — supply feed / filter for U34 (pin 1 → 2).

#### R670 — 10k, R

R670 — 10k, R_0603_1608Metric — `/driver/CMD_AC5` ↔ `/driver/CMD_BIASED5` — series / termination resistor for U35 (pin 1 → 2).

#### R671 — 1.40k, R

R671 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED5` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R672 — 10M, R

R672 — 10M, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/FEEDBACK5` — supply feed / filter for U35 (pin 1 → 2).

#### R673 — 330k, R

R673 — 330k, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/COMP5` — supply feed / filter for U35 (pin 1 → 2).

#### R680 — 10k, R

R680 — 10k, R_0603_1608Metric — `/driver/CMD_AC6` ↔ `/driver/CMD_BIASED6` — series / termination resistor for U36 (pin 1 → 2).

#### R681 — 1.40k, R

R681 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED6` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R682 — 10M, R

R682 — 10M, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/FEEDBACK6` — supply feed / filter for U36 (pin 1 → 2).

#### R683 — 330k, R

R683 — 330k, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/COMP6` — supply feed / filter for U36 (pin 1 → 2).

#### R690 — 10k, R

R690 — 10k, R_0603_1608Metric — `/driver/CMD_AC7` ↔ `/driver/CMD_BIASED7` — series / termination resistor for U37 (pin 1 → 2).

#### R691 — 1.40k, R

R691 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED7` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R692 — 10M, R

R692 — 10M, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/FEEDBACK7` — supply feed / filter for U37 (pin 1 → 2).

#### R693 — 330k, R

R693 — 330k, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/COMP7` — supply feed / filter for U37 (pin 1 → 2).

#### R710 — 52.3k 0.1%, R

R710 — 52.3k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_REF` — pull-up resistor for U62 (pin 1 → 2).

#### R711 — 10k 0.1%, R

R711 — 10k 0.1%, R_0603_1608Metric — `/driver/TRIP_REF` ↔ `GND` — pull-down resistor for U62 (pin 1 → 2).

#### R712 — 4.7k, R

R712 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/DRIVER_FAULT_N` — pull-up resistor for U601 (pin 1 → 2).

#### R720 — 10k 0.1%, R

R720 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/TRIP_SENSE0` — series / termination resistor for U60 (pin 1 → 2).

#### R721 — 100k 0.1%, R

R721 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE0` — pull-up resistor for U60 (pin 1 → 2).

#### R722 — 10k 0.1%, R

R722 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/TRIP_SENSE1` — series / termination resistor for U61 (pin 1 → 2).

#### R723 — 100k 0.1%, R

R723 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE1` — pull-up resistor for U62 (pin 1 → 2).

#### R724 — 10k 0.1%, R

R724 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/TRIP_SENSE2` — series / termination resistor for U62 (pin 1 → 2).

#### R725 — 100k 0.1%, R

R725 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE2` — pull-up resistor for U64 (pin 1 → 2).

#### R726 — 10k 0.1%, R

R726 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/TRIP_SENSE3` — series / termination resistor for U63 (pin 1 → 2).

#### R727 — 100k 0.1%, R

R727 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE3` — pull-up resistor for U66 (pin 1 → 2).

#### R728 — 10k 0.1%, R

R728 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/TRIP_SENSE4` — series / termination resistor for U64 (pin 1 → 2).

#### R729 — 100k 0.1%, R

R729 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE4` — pull-up resistor for U60 (pin 1 → 2).

#### R730 — 10k 0.1%, R

R730 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/TRIP_SENSE5` — series / termination resistor for U65 (pin 1 → 2).

#### R731 — 100k 0.1%, R

R731 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE5` — pull-up resistor for U62 (pin 1 → 2).

#### R732 — 10k 0.1%, R

R732 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/TRIP_SENSE6` — series / termination resistor for U66 (pin 1 → 2).

#### R733 — 100k 0.1%, R

R733 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE6` — pull-up resistor for U64 (pin 1 → 2).

#### R734 — 10k 0.1%, R

R734 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/TRIP_SENSE7` — series / termination resistor for U67 (pin 1 → 2).

#### R735 — 100k 0.1%, R

R735 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE7` — pull-up resistor for U66 (pin 1 → 2).


## Dependency summary

## 5. Per-sheet support summary

Page 1 — root has no components, so no support rows.

Component → the passives that exist to serve it. `—` means no R/C/L was found by either rule on that sheet. Counts are per component, not per net.


### 5.3 driver

| Component | Passives that serve it |
|---|---|
| TP200 | — |
| TP201 | — |
| TP202 | — |
| TP203 | — |
| TP210 | — |
| TP211 | — |
| TP212 | — |
| TP213 | — |
| TP214 | — |
| TP215 | — |
| TP216 | — |
| TP217 | — |
| TP820 | — |
| TP821 | — |
| TP822 | — |
| TP823 | filter capacitor to ground: C283 (100n) on /driver/VMID_7V5; pull-down resistor: R383 (10k) on /driver/VMID_7V5; pull-up resistor: R382 (10k) on /driver/VMID_7V5; series / termination resistor: R20 (1.00 0.1% 0.5W), R21 (1.00 0.1% 0.5W), R22 (1.00 0.1% 0.5W), R23 (1.00 0.1% 0.5W), R24 (1.00 0.1% 0.5W), R25 (1.00 0.1% 0.5W), R26 (1.00 0.1% 0.5W), R27 (1.00 0.1% 0.5W) on /driver/VMID_7V5 |
| U10 | soft-start / bias capacitor: C203 (150n) on /driver/DAC_REF; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply feed / filter: R220 (42.7k 0.1%) on /driver/DAC0; supply feed / filter: R230 (42.7k 0.1%) on /driver/DAC1; supply feed / filter: R240 (42.7k 0.1%) on /driver/DAC2; supply feed / filter: R250 (42.7k 0.1%) on /driver/DAC3; supply feed / filter: R260 (42.7k 0.1%) on /driver/DAC4; supply feed / filter: R270 (42.7k 0.1%) on /driver/DAC5; supply feed / filter: R280 (42.7k 0.1%) on /driver/DAC6; supply feed / filter: R290 (42.7k 0.1%) on /driver/DAC7 |
| U20 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-down resistor: R381 (10k) on GND; pull-up resistor: R380 (10k), R600 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C212 (CAA572X7R1E107M670LJ) on /driver/BUF0 |
| U21 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R601 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C220 (CAA572X7R1E107M670LJ) on /driver/BUF1 |
| U22 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R602 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C228 (CAA572X7R1E107M670LJ) on /driver/BUF2 |
| U23 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R603 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C236 (CAA572X7R1E107M670LJ) on /driver/BUF3 |
| U24 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R604 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C244 (CAA572X7R1E107M670LJ) on /driver/BUF4 |
| U25 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R605 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C252 (CAA572X7R1E107M670LJ) on /driver/BUF5 |
| U26 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R606 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C260 (CAA572X7R1E107M670LJ) on /driver/BUF6 |
| U27 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R607 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C268 (CAA572X7R1E107M670LJ) on /driver/BUF7 |
| U30 | input / output filter capacitor: C622 (150p) on /driver/FEEDBACK0; series / termination resistor: R620 (10k) on /driver/CMD_BIASED0; series / termination resistor: R360 (10k) on /driver/FEEDBACK0; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R361 (15k), R622 (10M), R623 (330k) on /driver/ERR0 |
| U31 | input / output filter capacitor: C632 (150p) on /driver/FEEDBACK1; series / termination resistor: R630 (10k) on /driver/CMD_BIASED1; series / termination resistor: R362 (10k) on /driver/FEEDBACK1; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R363 (15k), R632 (10M), R633 (330k) on /driver/ERR1 |
| U32 | input / output filter capacitor: C642 (150p) on /driver/FEEDBACK2; series / termination resistor: R640 (10k) on /driver/CMD_BIASED2; series / termination resistor: R364 (10k) on /driver/FEEDBACK2; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R365 (15k), R642 (10M), R643 (330k) on /driver/ERR2 |
| U33 | input / output filter capacitor: C652 (150p) on /driver/FEEDBACK3; series / termination resistor: R650 (10k) on /driver/CMD_BIASED3; series / termination resistor: R366 (10k) on /driver/FEEDBACK3; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R367 (15k), R652 (10M), R653 (330k) on /driver/ERR3 |
| U34 | input / output filter capacitor: C662 (150p) on /driver/FEEDBACK4; series / termination resistor: R660 (10k) on /driver/CMD_BIASED4; series / termination resistor: R368 (10k) on /driver/FEEDBACK4; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R369 (15k), R662 (10M), R663 (330k) on /driver/ERR4 |
| U35 | input / output filter capacitor: C672 (150p) on /driver/FEEDBACK5; series / termination resistor: R670 (10k) on /driver/CMD_BIASED5; series / termination resistor: R370 (10k) on /driver/FEEDBACK5; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R371 (15k), R672 (10M), R673 (330k) on /driver/ERR5 |
| U36 | input / output filter capacitor: C682 (150p) on /driver/FEEDBACK6; series / termination resistor: R680 (10k) on /driver/CMD_BIASED6; series / termination resistor: R372 (10k) on /driver/FEEDBACK6; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R373 (15k), R682 (10M), R683 (330k) on /driver/ERR6 |
| U37 | input / output filter capacitor: C692 (150p) on /driver/FEEDBACK7; series / termination resistor: R690 (10k) on /driver/CMD_BIASED7; series / termination resistor: R374 (10k) on /driver/FEEDBACK7; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R375 (15k), R692 (10M), R693 (330k) on /driver/ERR7 |
| U38 | series / termination resistor: R201 (10k 0.1%), R202 (10k 0.1%), R203 (10k 0.1%), R204 (10k 0.1%), R205 (10k 0.1%), R206 (10k 0.1%), R207 (10k 0.1%), R208 (10k 0.1%) on /driver/SUM_NODE; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R200 (20k 0.1%) on CURRENT_SUM |
| U39 | filter capacitor to ground: C281 (100n) on /driver/BIAS_DIV; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID |
| U40 | input / output filter capacitor: C621 (100n) on /driver/I_SENSE0; input / output filter capacitor: C631 (100n) on /driver/I_SENSE1; pull-down resistor: R401 (10k 0.1%) on /driver/SENSE_P0; pull-down resistor: R411 (10k 0.1%) on /driver/SENSE_P1; series / termination resistor: R403 (10k 0.1%) on /driver/I_SENSE0; series / termination resistor: R413 (10k 0.1%) on /driver/I_SENSE1; series / termination resistor: R402 (10k 0.1%) on /driver/SENSE_N0; series / termination resistor: R412 (10k 0.1%) on /driver/SENSE_N1; series / termination resistor: R400 (10k 0.1%) on /driver/SENSE_P0; series / termination resistor: R410 (10k 0.1%) on /driver/SENSE_P1; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U41 | input / output filter capacitor: C641 (100n) on /driver/I_SENSE2; input / output filter capacitor: C651 (100n) on /driver/I_SENSE3; pull-down resistor: R421 (10k 0.1%) on /driver/SENSE_P2; pull-down resistor: R431 (10k 0.1%) on /driver/SENSE_P3; series / termination resistor: R423 (10k 0.1%) on /driver/I_SENSE2; series / termination resistor: R433 (10k 0.1%) on /driver/I_SENSE3; series / termination resistor: R422 (10k 0.1%) on /driver/SENSE_N2; series / termination resistor: R432 (10k 0.1%) on /driver/SENSE_N3; series / termination resistor: R420 (10k 0.1%) on /driver/SENSE_P2; series / termination resistor: R430 (10k 0.1%) on /driver/SENSE_P3; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U42 | input / output filter capacitor: C661 (100n) on /driver/I_SENSE4; input / output filter capacitor: C671 (100n) on /driver/I_SENSE5; pull-down resistor: R441 (10k 0.1%) on /driver/SENSE_P4; pull-down resistor: R451 (10k 0.1%) on /driver/SENSE_P5; series / termination resistor: R443 (10k 0.1%) on /driver/I_SENSE4; series / termination resistor: R453 (10k 0.1%) on /driver/I_SENSE5; series / termination resistor: R442 (10k 0.1%) on /driver/SENSE_N4; series / termination resistor: R452 (10k 0.1%) on /driver/SENSE_N5; series / termination resistor: R440 (10k 0.1%) on /driver/SENSE_P4; series / termination resistor: R450 (10k 0.1%) on /driver/SENSE_P5; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U43 | input / output filter capacitor: C681 (100n) on /driver/I_SENSE6; input / output filter capacitor: C691 (100n) on /driver/I_SENSE7; pull-down resistor: R461 (10k 0.1%) on /driver/SENSE_P6; pull-down resistor: R471 (10k 0.1%) on /driver/SENSE_P7; series / termination resistor: R463 (10k 0.1%) on /driver/I_SENSE6; series / termination resistor: R473 (10k 0.1%) on /driver/I_SENSE7; series / termination resistor: R462 (10k 0.1%) on /driver/SENSE_N6; series / termination resistor: R472 (10k 0.1%) on /driver/SENSE_N7; series / termination resistor: R460 (10k 0.1%) on /driver/SENSE_P6; series / termination resistor: R470 (10k 0.1%) on /driver/SENSE_P7; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U60 | pull-up resistor: R729 (100k 0.1%) on +3.3V; pull-up resistor: R721 (100k 0.1%) on /driver/TRIP_SENSE0; series / termination resistor: R720 (10k 0.1%) on /driver/TRIP_SENSE0; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U61 | series / termination resistor: R722 (10k 0.1%) on /driver/TRIP_SENSE1; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U62 | pull-down resistor: R711 (10k 0.1%) on /driver/TRIP_REF; pull-up resistor: R723 (100k 0.1%), R731 (100k 0.1%) on +3.3V; pull-up resistor: R710 (52.3k 0.1%) on /driver/TRIP_REF; series / termination resistor: R724 (10k 0.1%) on /driver/TRIP_SENSE2; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U63 | series / termination resistor: R726 (10k 0.1%) on /driver/TRIP_SENSE3; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U64 | pull-up resistor: R725 (100k 0.1%), R733 (100k 0.1%) on +3.3V; series / termination resistor: R728 (10k 0.1%) on /driver/TRIP_SENSE4; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U65 | series / termination resistor: R730 (10k 0.1%) on /driver/TRIP_SENSE5; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U66 | filter capacitor to ground: C710 (100n) on /driver/TRIP_REF; pull-up resistor: R727 (100k 0.1%), R735 (100k 0.1%) on +3.3V; series / termination resistor: R732 (10k 0.1%) on /driver/TRIP_SENSE6; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U67 | series / termination resistor: R734 (10k 0.1%) on /driver/TRIP_SENSE7; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U80 | input / output filter capacitor: C620 (1u) on /driver/FILTER0; series / termination resistor: R224 (42.7k 0.1%) on /driver/FILTER0; series / termination resistor: R222 (42.7k 0.1%) on /driver/INVA0; series / termination resistor: R225 (42.7k 0.1%) on /driver/INVB0; series / termination resistor: R221 (42.7k 0.1%), R223 (42.7k 0.1%) on /driver/LPA0; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C211 (100n) on /driver/AGND0 |
| U81 | filter capacitor to ground: C282 (EEUFR1E102) on GND; input / output filter capacitor: C630 (1u) on /driver/FILTER1; series / termination resistor: R234 (42.7k 0.1%) on /driver/FILTER1; series / termination resistor: R232 (42.7k 0.1%) on /driver/INVA1; series / termination resistor: R235 (42.7k 0.1%) on /driver/INVB1; series / termination resistor: R231 (42.7k 0.1%), R233 (42.7k 0.1%) on /driver/LPA1; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C219 (100n) on /driver/AGND1 |
| U82 | input / output filter capacitor: C640 (1u) on /driver/FILTER2; series / termination resistor: R244 (42.7k 0.1%) on /driver/FILTER2; series / termination resistor: R242 (42.7k 0.1%) on /driver/INVA2; series / termination resistor: R245 (42.7k 0.1%) on /driver/INVB2; series / termination resistor: R241 (42.7k 0.1%), R243 (42.7k 0.1%) on /driver/LPA2; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C227 (100n) on /driver/AGND2 |
| U83 | input / output filter capacitor: C650 (1u) on /driver/FILTER3; series / termination resistor: R254 (42.7k 0.1%) on /driver/FILTER3; series / termination resistor: R252 (42.7k 0.1%) on /driver/INVA3; series / termination resistor: R255 (42.7k 0.1%) on /driver/INVB3; series / termination resistor: R251 (42.7k 0.1%), R253 (42.7k 0.1%) on /driver/LPA3; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C235 (100n) on /driver/AGND3 |
| U84 | input / output filter capacitor: C660 (1u) on /driver/FILTER4; series / termination resistor: R264 (42.7k 0.1%) on /driver/FILTER4; series / termination resistor: R262 (42.7k 0.1%) on /driver/INVA4; series / termination resistor: R265 (42.7k 0.1%) on /driver/INVB4; series / termination resistor: R261 (42.7k 0.1%), R263 (42.7k 0.1%) on /driver/LPA4; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C243 (100n) on /driver/AGND4 |
| U85 | input / output filter capacitor: C670 (1u) on /driver/FILTER5; series / termination resistor: R274 (42.7k 0.1%) on /driver/FILTER5; series / termination resistor: R272 (42.7k 0.1%) on /driver/INVA5; series / termination resistor: R275 (42.7k 0.1%) on /driver/INVB5; series / termination resistor: R271 (42.7k 0.1%), R273 (42.7k 0.1%) on /driver/LPA5; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C251 (100n) on /driver/AGND5 |
| U86 | input / output filter capacitor: C680 (1u) on /driver/FILTER6; series / termination resistor: R284 (42.7k 0.1%) on /driver/FILTER6; series / termination resistor: R282 (42.7k 0.1%) on /driver/INVA6; series / termination resistor: R285 (42.7k 0.1%) on /driver/INVB6; series / termination resistor: R281 (42.7k 0.1%), R283 (42.7k 0.1%) on /driver/LPA6; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C259 (100n) on /driver/AGND6 |
| U87 | input / output filter capacitor: C690 (1u) on /driver/FILTER7; series / termination resistor: R294 (42.7k 0.1%) on /driver/FILTER7; series / termination resistor: R292 (42.7k 0.1%) on /driver/INVA7; series / termination resistor: R295 (42.7k 0.1%) on /driver/INVB7; series / termination resistor: R291 (42.7k 0.1%), R293 (42.7k 0.1%) on /driver/LPA7; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C267 (100n) on /driver/AGND7 |
| U600 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U601 | pull-up resistor: R712 (4.7k) on /DRIVER_FAULT_N; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U602 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U603 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
