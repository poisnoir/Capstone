# BRD-01 wiring manifest
**Provenance (2026-11-25, base commit `ef04f63`):** generated with `kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch` (KiCad 10.0.8); regenerate after any BRD-01 netlist change — regeneration pends the uncommitted KiCad WIP, so these tables describe the committed netlist only.
Generated from the KiCad netlist of `hardware/brd-01/kicad/brd-01.kicad_sch` (KiCad 10.0.8) by `kicad-cli sch export netlist --format kicadxml`. Companion machine-readable file: `brd01_wiring_manifest.csv` (one row per sheet, net, ref and pin).

## 1. How to read it

This manifest is the complete part-to-part wiring of BRD-01, organised by hierarchical sheet. It is generated from the exported netlist, not hand-transcribed: every ref, pin, pin name/function and pin type below comes from a `<node>` element, and every sheet assignment comes from that component's `<sheetpath names=...>`. A net that appears on only one sheet is declared once, in that sheet's **Internal connections** table. A net that crosses sheets is declared once on each side in that sheet's **Inputs** or **Outputs** table and is marked `crossing`; it appears once, with the per-sheet pin counts, in the Section 4 register. Power rails are listed separately on every sheet that uses them and are never repeated in the signal tables.

Sheets are presented in page order: root (1), power (2), driver (3), receiver (4), fpga (5), connectors (6). The root sheet has no components; its only wiring is the two hierarchical sheet-pin connections (`DRIVER_FAULT_N`, `BUCK_SYNC`), which are attributed to the sheets that own the pins. For a two-pin net the ends are written `refA.pinA ↔ refB.pinB`; multi-pin nets list every end. Pin names come from `pinfunction` and the electrical type (passive / input / output / power_in / power_out / bidirectional / open_collector, optionally `+no_connect`) from `pintype`.

## 2. Sheet inventory

| Page | Sheet | Paper size | Parts | Nets |
|---|---|---|---|---|
| 1 | root | A4 | 0 | 0 |
| 2 | power | A1 portrait | 105 | 88 |
| 3 | driver | A0 | 338 | 226 |
| 4 | receiver | A1 | 107 | 109 |
| 5 | fpga | A2 | 67 | 211 |
| 6 | connectors | A3 | 23 | 40 |

## 3.1 Page 1 — root

**Purpose.** Top-level sheet: holds the five sheet instances and the two hierarchical signal pins (`DRIVER_FAULT_N`, `BUCK_SYNC`); no parts.

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 0 | not on this sheet |
| +3.3V | 0 | not on this sheet |
| GND | 0 | not on this sheet |
| +12VA | 0 | not on this sheet |
| -12VA | 0 | not on this sheet |
| +5VA | 0 | not on this sheet |
| +5V_EXC | 0 | not on this sheet |
| +1V0_FPGA | 0 | not on this sheet |
| +1V8_FPGA | 0 | not on this sheet |
| +1V8 | 0 | not present in netlist |

No crossing signal inputs.

No crossing signal outputs.

**Internal connections** (nets whose pins are all on this sheet)

No internal connections; every net on this sheet crosses a sheet boundary.

**No-connects**

None.

## 3.2 Page 2 — power

**Purpose.** Adapter entry, protection, arm STOP latch and every supply rail (digital, excitation and analog).

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 13 | source |
| +3.3V | 20 | source |
| GND | 103 | common return |
| +12VA | 6 | source |
| -12VA | 6 | source |
| +5VA | 4 | source |
| +5V_EXC | 4 | source |
| +1V0_FPGA | 4 | source |
| +1V8_FPGA | 4 | source |
| +1V8 | 0 | not present in netlist |

**Inputs** (crossing nets arriving on this sheet)

| Net | Pins on this sheet | From sheet | Signal |
|---|---|---|---|
| /BUCK_SYNC | C809.1 | fpga | 1.024 MHz buck sync: FPGA U4.R3 through C809 into U147 EN/SYNC. |
| /DRIVER_FAULT_N | U752.2 | driver | Active-low coil overcurrent bus: U600–U603 open-drain + R712 pull-up; clears U752 latch and is read by U4.R1. |
| PICO_STOP_REQ_N | R754.1, U755.1 | fpga | Active-low STOP request from FPGA U4.P4 (R754 pull-down) into U755.1. |

**Outputs** (crossing nets leaving this sheet)

| Net | Pins on this sheet | To sheet(s) | Signal |
|---|---|---|---|
| PICO_STOP_N | R753.1, U755.4 | connectors | Active-low STOP level: latch AND gate U755.4 → J123.5 (Pico pulls down). |

**Internal connections** (nets whose pins are all on this sheet)

*Entry latch and enable chains*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /power/ARM_Q | U753.5 (Q_5, output) ↔ U755.2 (—, input) |
| /power/BUCK1_FB | R190.2 (—, passive), R191.1 (—, passive), U144.5 (FB_5, input) |
| /power/CMC_POS | L1.4 (4_4, passive) ↔ Q760.2 (D_2, passive) |

*FPGA rail sequencing*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /power/PG_1V0 | R192.2 (—, passive), U144.4 (PG_4, open_collector), U144.7 (FSW_7, input), U145.13 (EN_13, input) |
| /power/PG_1V8 | R195.2 (—, passive), U145.4 (PG_4, open_collector), U7.13 (EN_13, input) |
| /power/PG_6V | R805.1 (—, passive), U144.13 (EN_13, input), U147.13 (PG_13, open_collector) |

*Local rail segments*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| +15V | C780.1 (—, passive), TP760.1 (1_1, passive), U5.7 (+VOUT_7, power_out), U6.1 (IN_1, power_in), U6.2 (IN_2, power_in), U6.4 (EN/UV_4, input), U6.7 (PGFB_7, input) |
| +6V | C180.1 (—, passive), C183.1 (—, passive), C184.1 (—, passive), C187.1 (—, passive), C805.1 (—, passive), C806.1 (—, passive), C807.1 (—, passive), C808.1 (—, passive), C810.1 (—, passive), C811.1 (—, passive), C812.1 (—, passive), L801.1 (1_1, passive), L802.1 (1_1, passive), R192.1 (—, passive), R195.1 (—, passive), R800.1 (—, passive), R805.2 (—, passive), U144.10 (VIN_10, power_in), U144.11 (VIN_11, passive), U144.12 (VIN_12, passive), U145.10 (VIN_10, power_in), U145.11 (VIN_11, passive), U145.12 (VIN_12, passive), U147.5 (VLDOIN_5, power_in), U147.8 (VOUT1_8, power_out), U147.9 (VOUT2_9, passive), U7.10 (VIN_10, power_in), U7.11 (VIN_11, passive), U7.12 (VIN_12, passive) |

*Local two-/three-pin joins*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| Net-(C755-Pad1) | C755.1 (—, passive), R752.2 (—, passive), U754.2 (—, input) |
| Net-(C818-Pad1) | C818.1 (—, passive) ↔ R808.2 (—, passive) |
| Net-(C820-Pad1) | C820.1 (—, passive) ↔ R809.2 (—, passive) |
| Net-(D760-A) | D760.2 (A_2, passive), Q760.1 (G_1, input), R770.1 (—, passive) |
| Net-(D760-K) | C770.1 (—, passive), D760.1 (K_1, passive), L760.1 (1_1, passive), Q760.3 (S_3, passive) |
| Net-(F1-Pad1) | F1.1 (—, passive) ↔ J1.1 (—, passive) |
| Net-(F1-Pad2) | F1.2 (—, passive) ↔ L1.1 (1_1, passive) |
| Net-(J1-Pad2) | J1.2 (—, passive) ↔ L1.2 (2_2, passive) |
| Net-(L140-Pad1) | L140.1 (1_1, passive), U144.1 (SW_1, output), U144.2 (SW_2, passive), U144.3 (SW_3, passive) |
| Net-(L141-Pad1) | L141.1 (1_1, passive), U145.1 (SW_1, output), U145.2 (SW_2, passive), U145.3 (SW_3, passive) |
| Net-(L800-Pad1) | L800.1 (1_1, passive), U7.1 (SW_1, output), U7.2 (SW_2, passive), U7.3 (SW_3, passive) |
| Net-(R751-Pad2) | R751.2 (—, passive), R752.1 (—, passive), SW750.1 (1_1, passive) |
| Net-(U144-SS/TR) | C181.1 (—, passive) ↔ U144.9 (SS/TR_9, input) |
| Net-(U145-FB) | R193.2 (—, passive), R194.1 (—, passive), U145.5 (FB_5, input) |
| Net-(U145-SS/TR) | C185.1 (—, passive) ↔ U145.9 (SS/TR_9, input) |
| Net-(U146-EN) | C188.1 (—, passive), L802.2 (2_2, passive), R809.1 (—, passive), U146.13 (EN_13, input), U146.15 (IN_15, power_in), U146.16 (IN_16, power_in) |
| Net-(U146-NR) | C189.1 (—, passive) ↔ U146.14 (NR_14, passive) |
| Net-(U147-EN/SYNC) | C809.2 (—, passive), R803.2 (—, passive), R804.1 (—, passive), U147.14 (EN/SYNC_14, input) |
| Net-(U147-FB) | C805.2 (—, passive), R800.2 (—, passive), R801.1 (—, passive), U147.10 (FB_10, input) |
| Net-(U147-RT) | R802.1 (—, passive) ↔ U147.12 (RT_12, passive) |
| Net-(U149-EN) | C817.1 (—, passive), L801.2 (2_2, passive), R808.1 (—, passive), U149.13 (EN_13, input), U149.15 (IN_15, power_in), U149.16 (IN_16, power_in) |
| Net-(U149-NR) | C815.1 (—, passive) ↔ U149.14 (NR_14, passive) |
| Net-(U2-ILIM) | R2.1 (—, passive) ↔ U2.6 (ILIM_6, passive) |
| Net-(U2-SET) | C3.1 (—, passive), R1.2 (—, passive), U2.8 (SET_8, passive) |
| Net-(U6-ILIM) | R4.1 (—, passive) ↔ U6.6 (ILIM_6, passive) |
| Net-(U6-SET) | C6.1 (—, passive), R3.1 (—, passive), U6.8 (SET_8, passive) |
| Net-(U7-FB) | R806.2 (—, passive), R807.1 (—, passive), U7.5 (FB_5, input) |
| Net-(U7-SS/TR) | C814.1 (—, passive) ↔ U7.9 (SS/TR_9, input) |
| Net-(U751-~{RESET}) | R750.2 (—, passive), U751.1 (~{RESET}_1, output), U752.1 (—, input) |
| Net-(U753-C) | U753.1 (C_1, input) ↔ U754.4 (—, output) |
| Net-(U753-~{CLR}) | U752.4 (—, output) ↔ U753.6 (~{CLR}_6, input) |

*No-connect stubs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| unconnected-(J1-Pad3) | J1.3 (—, passive+no_connect) |
| unconnected-(J1-Shield-PadSH) | J1.SH (Shield_SH, passive+no_connect) |
| unconnected-(J750-Pin_2-Pad2) | J750.2 (Pin_2_2, passive+no_connect) |
| unconnected-(U146-0P1V-Pad12) | U146.12 (0P1V_12, input+no_connect) |
| unconnected-(U146-0P2V-Pad11) | U146.11 (0P2V_11, input+no_connect) |
| unconnected-(U146-0P8V-Pad9) | U146.9 (0P8V_9, input+no_connect) |
| unconnected-(U146-1P6V-Pad8) | U146.8 (1P6V_8, input+no_connect) |
| unconnected-(U146-6P4V1-Pad5) | U146.5 (6P4V1_5, input+no_connect) |
| unconnected-(U146-6P4V2-Pad4) | U146.4 (6P4V2_4, input+no_connect) |
| unconnected-(U146-NC-Pad17) | U146.17 (NC_17, passive+no_connect) |
| unconnected-(U146-NC-Pad18) | U146.18 (NC_18, passive+no_connect) |
| unconnected-(U146-NC-Pad19) | U146.19 (NC_19, passive+no_connect) |
| unconnected-(U146-NC-Pad2) | U146.2 (NC_2, passive+no_connect) |
| unconnected-(U147-CBOOT-Pad3) | U147.3 (CBOOT_3, passive+no_connect) |
| unconnected-(U147-RBOOT-Pad4) | U147.4 (RBOOT_4, passive+no_connect) |
| unconnected-(U147-SW-Pad2) | U147.2 (SW_2, passive+no_connect) |
| unconnected-(U147-VCC-Pad7) | U147.7 (VCC_7, passive+no_connect) |
| unconnected-(U149-0P1V-Pad12) | U149.12 (0P1V_12, input+no_connect) |
| unconnected-(U149-0P2V-Pad11) | U149.11 (0P2V_11, input+no_connect) |
| unconnected-(U149-0P8V-Pad9) | U149.9 (0P8V_9, input+no_connect) |
| unconnected-(U149-1P6V-Pad8) | U149.8 (1P6V_8, input+no_connect) |
| unconnected-(U149-6P4V1-Pad5) | U149.5 (6P4V1_5, input+no_connect) |
| unconnected-(U149-6P4V2-Pad4) | U149.4 (6P4V2_4, input+no_connect) |
| unconnected-(U149-NC-Pad17) | U149.17 (NC_17, passive+no_connect) |
| unconnected-(U149-NC-Pad18) | U149.18 (NC_18, passive+no_connect) |
| unconnected-(U149-NC-Pad19) | U149.19 (NC_19, passive+no_connect) |
| unconnected-(U149-NC-Pad2) | U149.2 (NC_2, passive+no_connect) |
| unconnected-(U2-PG-Pad4) | U2.4 (PG_4, open_collector+no_connect) |
| unconnected-(U2-VIOC-Pad7) | U2.7 (VIOC_7, output+no_connect) |
| unconnected-(U6-PG-Pad5) | U6.5 (PG_5, open_collector+no_connect) |
| unconnected-(U6-VIOC-Pad3) | U6.3 (VIOC_3, output+no_connect) |
| unconnected-(U7-PG-Pad4) | U7.4 (PG_4, open_collector+no_connect) |
| unconnected-(U751-CT-Pad4) | U751.4 (CT_4, input+no_connect) |
| unconnected-(U753-~{Q}-Pad3) | U753.3 (~{Q}_3, output+no_connect) |
| unconnected-(U754-NC-Pad1) | U754.1 (NC_1, no_connect) |

*Regulator passives and feeders*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| -15V | C781.1 (—, passive), TP761.1 (1_1, passive), U2.1 (IN_1, power_in), U2.13 (IN_(EP)_13, passive), U2.2 (IN_2, power_in), U2.3 (EN/UV_3, input), U2.5 (PGFB_5, input), U5.5 (-VOUT_5, power_out) |

**No-connects**

| Pin (no-connect) | Pin name | Pin type | Reason |
|---|---|---|---|
| J1.3 |  | passive+no_connect | No reason stated in schematic |
| J1.SH | Shield_SH | passive+no_connect | No reason stated in schematic |
| J750.2 | Pin_2_2 | passive+no_connect | No reason stated in schematic |
| U146.11 | 0P2V_11 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.12 | 0P1V_12 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.17 | NC_17 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.18 | NC_18 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.19 | NC_19 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.2 | NC_2 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.4 | 6P4V2_4 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.5 | 6P4V1_5 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.8 | 1P6V_8 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U146.9 | 0P8V_9 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U147.2 | SW_2 | passive+no_connect | Boot/sync and NC pins left open (power_tree_v2 §4: internal 100 Ω; SW no connection) |
| U147.3 | CBOOT_3 | passive+no_connect | Boot/sync and NC pins left open (power_tree_v2 §4: internal 100 Ω; SW no connection) |
| U147.4 | RBOOT_4 | passive+no_connect | Boot/sync and NC pins left open (power_tree_v2 §4: internal 100 Ω; SW no connection) |
| U147.7 | VCC_7 | passive+no_connect | Boot/sync and NC pins left open (power_tree_v2 §4: internal 100 Ω; SW no connection) |
| U149.11 | 0P2V_11 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.12 | 0P1V_12 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.17 | NC_17 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.18 | NC_18 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.19 | NC_19 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.2 | NC_2 | passive+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.4 | 6P4V2_4 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.5 | 6P4V1_5 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.8 | 1P6V_8 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U149.9 | 0P8V_9 | input+no_connect | Unused TPS7A4701 ANY-OUT / NC pins left open (power_tree_v2 §4) |
| U2.4 | PG_4 | open_collector+no_connect | Analog rails are not sequenced or PG-monitored (power-tree.md §2) |
| U2.7 | VIOC_7 | output+no_connect | Analog rails are not sequenced or PG-monitored (power-tree.md §2) |
| U6.3 | VIOC_3 | output+no_connect | Analog rails are not sequenced or PG-monitored (power-tree.md §2) |
| U6.5 | PG_5 | open_collector+no_connect | Analog rails are not sequenced or PG-monitored (power-tree.md §2) |
| U7.4 | PG_4 | open_collector+no_connect | No reason stated in schematic |
| U751.4 | CT_4 | input+no_connect | No reason stated in schematic |
| U753.3 | ~{Q}_3 | output+no_connect | Latch retargeted to Q; ~Q unused (system_schematic.md §4.5) |
| U754.1 | NC_1 | no_connect | No reason stated in schematic |

## 3.3 Page 3 — driver

**Purpose.** Eight-channel DDS-command reconstruction, coil current loops, sense summer and the shared active-low fault bus.

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 28 | sink |
| +3.3V | 36 | sink |
| GND | 170 | common return |
| +12VA | 26 | sink |
| -12VA | 26 | sink |
| +5VA | 0 | not on this sheet |
| +5V_EXC | 27 | sink |
| +1V0_FPGA | 0 | not on this sheet |
| +1V8_FPGA | 0 | not on this sheet |
| +1V8 | 0 | not present in netlist |

**Inputs** (crossing nets arriving on this sheet)

| Net | Pins on this sheet | From sheet | Signal |
|---|---|---|---|
| DAC_CS | TP200.1, U10.12 | fpga | DAC80508 control input (DAC_CS): FPGA U4 → 33 Ω series resistor → U10. |
| DAC_SCLK | TP201.1, U10.13 | fpga | DAC80508 control input (DAC_SCLK): FPGA U4 → 33 Ω series resistor → U10. |
| DAC_SDI | TP202.1, U10.14 | fpga | DAC80508 control input (DAC_SDI): FPGA U4 → 33 Ω series resistor → U10. |
| FG0_RETURN | R20.1, R400.1, TP822.1 | connectors | Field-generator channel 0 coil return and 1 Ω sense: J20.2 → driver sense network. |
| FG1_RETURN | R21.1, R410.1 | connectors | Field-generator channel 1 coil return and 1 Ω sense: J21.2 → driver sense network. |
| FG2_RETURN | R22.1, R420.1 | connectors | Field-generator channel 2 coil return and 1 Ω sense: J22.2 → driver sense network. |
| FG3_RETURN | R23.1, R430.1 | connectors | Field-generator channel 3 coil return and 1 Ω sense: J23.2 → driver sense network. |
| FG4_RETURN | R24.1, R440.1 | connectors | Field-generator channel 4 coil return and 1 Ω sense: J24.2 → driver sense network. |
| FG5_RETURN | R25.1, R450.1 | connectors | Field-generator channel 5 coil return and 1 Ω sense: J25.2 → driver sense network. |
| FG6_RETURN | R26.1, R460.1 | connectors | Field-generator channel 6 coil return and 1 Ω sense: J26.2 → driver sense network. |
| FG7_RETURN | R27.1, R470.1 | connectors | Field-generator channel 7 coil return and 1 Ω sense: J27.2 → driver sense network. |

**Outputs** (crossing nets leaving this sheet)

| Net | Pins on this sheet | To sheet(s) | Signal |
|---|---|---|---|
| /DRIVER_FAULT_N | R712.2, U600.4, U600.6, U601.4, U601.6, U602.4, U602.6, U603.4, U603.6 | fpga, power | Active-low coil overcurrent bus: U600–U603 open-drain + R712 pull-up; clears U752 latch and is read by U4.R1. |
| CURRENT_SUM | R200.1, U38.1 | receiver | Eight-tone current-sum monitor: U38 OPA192 output via R200/R110 into ADC Ch0. |
| DAC_SDO | TP203.1, U10.15 | fpga | DAC80508 SDO/~ALARM status return: U10.15 → FPGA U4.M4. |
| FG0_OUT | C212.2, TP821.1 | connectors | Field-generator channel 0 drive: coupling capacitor/TP on driver → J20.1. |
| FG1_OUT | C220.2 | connectors | Field-generator channel 1 drive: coupling capacitor/TP on driver → J21.1. |
| FG2_OUT | C228.2 | connectors | Field-generator channel 2 drive: coupling capacitor/TP on driver → J22.1. |
| FG3_OUT | C236.2 | connectors | Field-generator channel 3 drive: coupling capacitor/TP on driver → J23.1. |
| FG4_OUT | C244.2 | connectors | Field-generator channel 4 drive: coupling capacitor/TP on driver → J24.1. |
| FG5_OUT | C252.2 | connectors | Field-generator channel 5 drive: coupling capacitor/TP on driver → J25.1. |
| FG6_OUT | C260.2 | connectors | Field-generator channel 6 drive: coupling capacitor/TP on driver → J26.1. |
| FG7_OUT | C268.2 | connectors | Field-generator channel 7 drive: coupling capacitor/TP on driver → J27.1. |

**Internal connections** (nets whose pins are all on this sheet)

*Comparator trip networks*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/COMP0 | C622.1 (—, passive) ↔ R623.2 (—, passive) |
| /driver/COMP1 | C632.1 (—, passive) ↔ R633.2 (—, passive) |
| /driver/COMP2 | C642.1 (—, passive) ↔ R643.2 (—, passive) |
| /driver/COMP3 | C652.1 (—, passive) ↔ R653.2 (—, passive) |
| /driver/COMP4 | C662.1 (—, passive) ↔ R663.2 (—, passive) |
| /driver/COMP5 | C672.1 (—, passive) ↔ R673.2 (—, passive) |
| /driver/COMP6 | C682.1 (—, passive) ↔ R683.2 (—, passive) |
| /driver/COMP7 | C692.1 (—, passive) ↔ R693.2 (—, passive) |
| /driver/ERR0 | R361.1 (—, passive), R622.1 (—, passive), R623.1 (—, passive), U30.1 (OUT_1, output) |
| /driver/ERR1 | R363.1 (—, passive), R632.1 (—, passive), R633.1 (—, passive), U31.1 (OUT_1, output) |
| /driver/ERR2 | R365.1 (—, passive), R642.1 (—, passive), R643.1 (—, passive), U32.1 (OUT_1, output) |
| /driver/ERR3 | R367.1 (—, passive), R652.1 (—, passive), R653.1 (—, passive), U33.1 (OUT_1, output) |
| /driver/ERR4 | R369.1 (—, passive), R662.1 (—, passive), R663.1 (—, passive), U34.1 (OUT_1, output) |
| /driver/ERR5 | R371.1 (—, passive), R672.1 (—, passive), R673.1 (—, passive), U35.1 (OUT_1, output) |
| /driver/ERR6 | R373.1 (—, passive), R682.1 (—, passive), R683.1 (—, passive), U36.1 (OUT_1, output) |
| /driver/ERR7 | R375.1 (—, passive), R692.1 (—, passive), R693.1 (—, passive), U37.1 (OUT_1, output) |
| /driver/FAULT0 | TP210.1 (1_1, passive), U60.1 (OUT_1, output), U600.1 (—, input) |
| /driver/FAULT1 | TP211.1 (1_1, passive), U600.3 (—, input), U61.1 (OUT_1, output) |
| /driver/FAULT2 | TP212.1 (1_1, passive), U601.1 (—, input), U62.1 (OUT_1, output) |
| /driver/FAULT3 | TP213.1 (1_1, passive), U601.3 (—, input), U63.1 (OUT_1, output) |
| /driver/FAULT4 | TP214.1 (1_1, passive), U602.1 (—, input), U64.1 (OUT_1, output) |
| /driver/FAULT5 | TP215.1 (1_1, passive), U602.3 (—, input), U65.1 (OUT_1, output) |
| /driver/FAULT6 | TP216.1 (1_1, passive), U603.1 (—, input), U66.1 (OUT_1, output) |
| /driver/FAULT7 | TP217.1 (1_1, passive), U603.3 (—, input), U67.1 (OUT_1, output) |

*Current-sense pickup*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/I_SENSE0 | C621.1 (—, passive), R201.1 (—, passive), R403.1 (—, passive), R720.1 (—, passive), U40.1 (OUTA_1, output) |
| /driver/I_SENSE1 | C631.1 (—, passive), R202.1 (—, passive), R413.1 (—, passive), R722.1 (—, passive), U40.7 (OUTB_7, output) |
| /driver/I_SENSE2 | C641.1 (—, passive), R203.1 (—, passive), R423.1 (—, passive), R724.1 (—, passive), U41.1 (OUTA_1, output) |
| /driver/I_SENSE3 | C651.1 (—, passive), R204.1 (—, passive), R433.1 (—, passive), R726.1 (—, passive), U41.7 (OUTB_7, output) |
| /driver/I_SENSE4 | C661.1 (—, passive), R205.1 (—, passive), R443.1 (—, passive), R728.1 (—, passive), U42.1 (OUTA_1, output) |
| /driver/I_SENSE5 | C671.1 (—, passive), R206.1 (—, passive), R453.1 (—, passive), R730.1 (—, passive), U42.7 (OUTB_7, output) |
| /driver/I_SENSE6 | C681.1 (—, passive), R207.1 (—, passive), R463.1 (—, passive), R732.1 (—, passive), U43.1 (OUTA_1, output) |
| /driver/I_SENSE7 | C691.1 (—, passive), R208.1 (—, passive), R473.1 (—, passive), R734.1 (—, passive), U43.7 (OUTB_7, output) |

*DAC command and reference*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/DAC0 | R220.1 (—, passive) ↔ U10.2 (OUT0_2, output) |
| /driver/DAC1 | R230.1 (—, passive) ↔ U10.3 (OUT1_3, output) |
| /driver/DAC2 | R240.1 (—, passive) ↔ U10.4 (OUT2_4, output) |
| /driver/DAC3 | R250.1 (—, passive) ↔ U10.5 (OUT3_5, output) |
| /driver/DAC4 | R260.1 (—, passive) ↔ U10.8 (OUT4_8, output) |
| /driver/DAC5 | R270.1 (—, passive) ↔ U10.9 (OUT5_9, output) |
| /driver/DAC6 | R280.1 (—, passive) ↔ U10.10 (OUT6_10, output) |
| /driver/DAC7 | R290.1 (—, passive) ↔ U10.11 (OUT7_11, output) |

*DAC reconstruction filters*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/FILTER0 | C620.1 (—, passive), R224.1 (—, passive), U80.15 (LPB_15, output) |
| /driver/FILTER1 | C630.1 (—, passive), R234.1 (—, passive), U81.15 (LPB_15, output) |
| /driver/FILTER2 | C640.1 (—, passive), R244.1 (—, passive), U82.15 (LPB_15, output) |
| /driver/FILTER3 | C650.1 (—, passive), R254.1 (—, passive), U83.15 (LPB_15, output) |
| /driver/FILTER4 | C660.1 (—, passive), R264.1 (—, passive), U84.15 (LPB_15, output) |
| /driver/FILTER5 | C670.1 (—, passive), R274.1 (—, passive), U85.15 (LPB_15, output) |
| /driver/FILTER6 | C680.1 (—, passive), R284.1 (—, passive), U86.15 (LPB_15, output) |
| /driver/FILTER7 | C690.1 (—, passive), R294.1 (—, passive), U87.15 (LPB_15, output) |

*Loop amplifier / command bias*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/LPA0 | R221.1 (—, passive), R223.1 (—, passive), U80.6 (LPA_6, output) |
| /driver/LPA1 | R231.1 (—, passive), R233.1 (—, passive), U81.6 (LPA_6, output) |
| /driver/LPA2 | R241.1 (—, passive), R243.1 (—, passive), U82.6 (LPA_6, output) |
| /driver/LPA3 | R251.1 (—, passive), R253.1 (—, passive), U83.6 (LPA_6, output) |
| /driver/LPA4 | R261.1 (—, passive), R263.1 (—, passive), U84.6 (LPA_6, output) |
| /driver/LPA5 | R271.1 (—, passive), R273.1 (—, passive), U85.6 (LPA_6, output) |
| /driver/LPA6 | R281.1 (—, passive), R283.1 (—, passive), U86.6 (LPA_6, output) |
| /driver/LPA7 | R291.1 (—, passive), R293.1 (—, passive), U87.6 (LPA_6, output) |

*No-connect stubs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| unconnected-(U20-EF-Pad1) | U20.1 (EF_1, open_collector+no_connect) |
| unconnected-(U20-NC-Pad8) | U20.8 (NC_8, no_connect) |
| unconnected-(U21-EF-Pad1) | U21.1 (EF_1, open_collector+no_connect) |
| unconnected-(U21-NC-Pad8) | U21.8 (NC_8, no_connect) |
| unconnected-(U22-EF-Pad1) | U22.1 (EF_1, open_collector+no_connect) |
| unconnected-(U22-NC-Pad8) | U22.8 (NC_8, no_connect) |
| unconnected-(U23-EF-Pad1) | U23.1 (EF_1, open_collector+no_connect) |
| unconnected-(U23-NC-Pad8) | U23.8 (NC_8, no_connect) |
| unconnected-(U24-EF-Pad1) | U24.1 (EF_1, open_collector+no_connect) |
| unconnected-(U24-NC-Pad8) | U24.8 (NC_8, no_connect) |
| unconnected-(U25-EF-Pad1) | U25.1 (EF_1, open_collector+no_connect) |
| unconnected-(U25-NC-Pad8) | U25.8 (NC_8, no_connect) |
| unconnected-(U26-EF-Pad1) | U26.1 (EF_1, open_collector+no_connect) |
| unconnected-(U26-NC-Pad8) | U26.8 (NC_8, no_connect) |
| unconnected-(U27-EF-Pad1) | U27.1 (EF_1, open_collector+no_connect) |
| unconnected-(U27-NC-Pad8) | U27.8 (NC_8, no_connect) |

*Other driver-local nets*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/BIAS_DIV | C281.1 (—, passive), R380.2 (—, passive), R381.1 (—, passive), U39.3 (IN+_3, input) |
| /driver/BUFFER_VMID | R621.1 (—, passive), R631.1 (—, passive), R641.1 (—, passive), R651.1 (—, passive), R661.1 (—, passive), R671.1 (—, passive), R681.1 (—, passive), R691.1 (—, passive), U20.5 (BIAS_REF_5, input), U21.5 (BIAS_REF_5, input), U22.5 (BIAS_REF_5, input), U23.5 (BIAS_REF_5, input), U24.5 (BIAS_REF_5, input), U25.5 (BIAS_REF_5, input), U26.5 (BIAS_REF_5, input), U27.5 (BIAS_REF_5, input), U39.1 (OUT_1, output), U39.4 (IN-_4, input) |
| /driver/BUF_IN0 | R361.2 (—, passive) ↔ U20.3 (VIN_3, input) |
| /driver/BUF_IN1 | R363.2 (—, passive) ↔ U21.3 (VIN_3, input) |
| /driver/BUF_IN2 | R365.2 (—, passive) ↔ U22.3 (VIN_3, input) |
| /driver/BUF_IN3 | R367.2 (—, passive) ↔ U23.3 (VIN_3, input) |
| /driver/BUF_IN4 | R369.2 (—, passive) ↔ U24.3 (VIN_3, input) |
| /driver/BUF_IN5 | R371.2 (—, passive) ↔ U25.3 (VIN_3, input) |
| /driver/BUF_IN6 | R373.2 (—, passive) ↔ U26.3 (VIN_3, input) |
| /driver/BUF_IN7 | R375.2 (—, passive) ↔ U27.3 (VIN_3, input) |
| /driver/CMD_AC0 | C620.2 (—, passive) ↔ R620.1 (—, passive) |
| /driver/CMD_AC1 | C630.2 (—, passive) ↔ R630.1 (—, passive) |
| /driver/CMD_AC2 | C640.2 (—, passive) ↔ R640.1 (—, passive) |
| /driver/CMD_AC3 | C650.2 (—, passive) ↔ R650.1 (—, passive) |
| /driver/CMD_AC4 | C660.2 (—, passive) ↔ R660.1 (—, passive) |
| /driver/CMD_AC5 | C670.2 (—, passive) ↔ R670.1 (—, passive) |
| /driver/CMD_AC6 | C680.2 (—, passive) ↔ R680.1 (—, passive) |
| /driver/CMD_AC7 | C690.2 (—, passive) ↔ R690.1 (—, passive) |
| /driver/CMD_BIASED0 | R620.2 (—, passive), R621.2 (—, passive), U30.3 (IN+_3, input) |
| /driver/CMD_BIASED1 | R630.2 (—, passive), R631.2 (—, passive), U31.3 (IN+_3, input) |
| /driver/CMD_BIASED2 | R640.2 (—, passive), R641.2 (—, passive), U32.3 (IN+_3, input) |
| /driver/CMD_BIASED3 | R650.2 (—, passive), R651.2 (—, passive), U33.3 (IN+_3, input) |
| /driver/CMD_BIASED4 | R660.2 (—, passive), R661.2 (—, passive), U34.3 (IN+_3, input) |
| /driver/CMD_BIASED5 | R670.2 (—, passive), R671.2 (—, passive), U35.3 (IN+_3, input) |
| /driver/CMD_BIASED6 | R680.2 (—, passive), R681.2 (—, passive), U36.3 (IN+_3, input) |
| /driver/CMD_BIASED7 | R690.2 (—, passive), R691.2 (—, passive), U37.3 (IN+_3, input) |
| /driver/DAC_REF | C203.1 (—, passive) ↔ U10.1 (REF_1, bidirectional) |
| /driver/INVA0 | R222.1 (—, passive) ↔ U80.4 (INVA_4, input) |
| /driver/INVA1 | R232.1 (—, passive) ↔ U81.4 (INVA_4, input) |
| /driver/INVA2 | R242.1 (—, passive) ↔ U82.4 (INVA_4, input) |
| /driver/INVA3 | R252.1 (—, passive) ↔ U83.4 (INVA_4, input) |
| /driver/INVA4 | R262.1 (—, passive) ↔ U84.4 (INVA_4, input) |
| /driver/INVA5 | R272.1 (—, passive) ↔ U85.4 (INVA_4, input) |
| /driver/INVA6 | R282.1 (—, passive) ↔ U86.4 (INVA_4, input) |
| /driver/INVA7 | R292.1 (—, passive) ↔ U87.4 (INVA_4, input) |
| /driver/INVB0 | R225.1 (—, passive) ↔ U80.13 (INVB_13, input) |
| /driver/INVB1 | R235.1 (—, passive) ↔ U81.13 (INVB_13, input) |
| /driver/INVB2 | R245.1 (—, passive) ↔ U82.13 (INVB_13, input) |
| /driver/INVB3 | R255.1 (—, passive) ↔ U83.13 (INVB_13, input) |
| /driver/INVB4 | R265.1 (—, passive) ↔ U84.13 (INVB_13, input) |
| /driver/INVB5 | R275.1 (—, passive) ↔ U85.13 (INVB_13, input) |
| /driver/INVB6 | R285.1 (—, passive) ↔ U86.13 (INVB_13, input) |
| /driver/INVB7 | R295.1 (—, passive) ↔ U87.13 (INVB_13, input) |
| /driver/LIMIT_PROG0 | R600.2 (—, passive) ↔ U20.2 (CL_2, input) |
| /driver/LIMIT_PROG1 | R601.2 (—, passive) ↔ U21.2 (CL_2, input) |
| /driver/LIMIT_PROG2 | R602.2 (—, passive) ↔ U22.2 (CL_2, input) |
| /driver/LIMIT_PROG3 | R603.2 (—, passive) ↔ U23.2 (CL_2, input) |
| /driver/LIMIT_PROG4 | R604.2 (—, passive) ↔ U24.2 (CL_2, input) |
| /driver/LIMIT_PROG5 | R605.2 (—, passive) ↔ U25.2 (CL_2, input) |
| /driver/LIMIT_PROG6 | R606.2 (—, passive) ↔ U26.2 (CL_2, input) |
| /driver/LIMIT_PROG7 | R607.2 (—, passive) ↔ U27.2 (CL_2, input) |
| /driver/SENSE_AC0 | C621.2 (—, passive) ↔ R360.1 (—, passive) |
| /driver/SENSE_AC1 | C631.2 (—, passive) ↔ R362.1 (—, passive) |
| /driver/SENSE_AC2 | C641.2 (—, passive) ↔ R364.1 (—, passive) |
| /driver/SENSE_AC3 | C651.2 (—, passive) ↔ R366.1 (—, passive) |
| /driver/SENSE_AC4 | C661.2 (—, passive) ↔ R368.1 (—, passive) |
| /driver/SENSE_AC5 | C671.2 (—, passive) ↔ R370.1 (—, passive) |
| /driver/SENSE_AC6 | C681.2 (—, passive) ↔ R372.1 (—, passive) |
| /driver/SENSE_AC7 | C691.2 (—, passive) ↔ R374.1 (—, passive) |
| /driver/SENSE_N0 | R402.2 (—, passive), R403.2 (—, passive), U40.2 (INA-_2, input) |
| /driver/SENSE_N1 | R412.2 (—, passive), R413.2 (—, passive), U40.6 (INB-_6, input) |
| /driver/SENSE_N2 | R422.2 (—, passive), R423.2 (—, passive), U41.2 (INA-_2, input) |
| /driver/SENSE_N3 | R432.2 (—, passive), R433.2 (—, passive), U41.6 (INB-_6, input) |
| /driver/SENSE_N4 | R442.2 (—, passive), R443.2 (—, passive), U42.2 (INA-_2, input) |
| /driver/SENSE_N5 | R452.2 (—, passive), R453.2 (—, passive), U42.6 (INB-_6, input) |
| /driver/SENSE_N6 | R462.2 (—, passive), R463.2 (—, passive), U43.2 (INA-_2, input) |
| /driver/SENSE_N7 | R472.2 (—, passive), R473.2 (—, passive), U43.6 (INB-_6, input) |
| /driver/SENSE_P0 | R400.2 (—, passive), R401.1 (—, passive), U40.3 (INA+_3, input) |
| /driver/SENSE_P1 | R410.2 (—, passive), R411.1 (—, passive), U40.5 (INB+_5, input) |
| /driver/SENSE_P2 | R420.2 (—, passive), R421.1 (—, passive), U41.3 (INA+_3, input) |
| /driver/SENSE_P3 | R430.2 (—, passive), R431.1 (—, passive), U41.5 (INB+_5, input) |
| /driver/SENSE_P4 | R440.2 (—, passive), R441.1 (—, passive), U42.3 (INA+_3, input) |
| /driver/SENSE_P5 | R450.2 (—, passive), R451.1 (—, passive), U42.5 (INB+_5, input) |
| /driver/SENSE_P6 | R460.2 (—, passive), R461.1 (—, passive), U43.3 (INA+_3, input) |
| /driver/SENSE_P7 | R470.2 (—, passive), R471.1 (—, passive), U43.5 (INB+_5, input) |
| /driver/TRIP_REF | C710.1 (—, passive), R710.2 (—, passive), R711.1 (—, passive), U60.3 (IN+_3, input), U61.3 (IN+_3, input), U62.3 (IN+_3, input), U63.3 (IN+_3, input), U64.3 (IN+_3, input), U65.3 (IN+_3, input), U66.3 (IN+_3, input), U67.3 (IN+_3, input) |
| /driver/TRIP_SENSE0 | R720.2 (—, passive), R721.2 (—, passive), U60.4 (IN-_4, input) |
| /driver/TRIP_SENSE1 | R722.2 (—, passive), R723.2 (—, passive), U61.4 (IN-_4, input) |
| /driver/TRIP_SENSE2 | R724.2 (—, passive), R725.2 (—, passive), U62.4 (IN-_4, input) |
| /driver/TRIP_SENSE3 | R726.2 (—, passive), R727.2 (—, passive), U63.4 (IN-_4, input) |
| /driver/TRIP_SENSE4 | R728.2 (—, passive), R729.2 (—, passive), U64.4 (IN-_4, input) |
| /driver/TRIP_SENSE5 | R730.2 (—, passive), R731.2 (—, passive), U65.4 (IN-_4, input) |
| /driver/TRIP_SENSE6 | R732.2 (—, passive), R733.2 (—, passive), U66.4 (IN-_4, input) |
| /driver/TRIP_SENSE7 | R734.2 (—, passive), R735.2 (—, passive), U67.4 (IN-_4, input) |
| /driver/VMID_7V5 | C282.1 (—, passive), C283.1 (—, passive), R20.2 (—, passive), R21.2 (—, passive), R22.2 (—, passive), R23.2 (—, passive), R24.2 (—, passive), R25.2 (—, passive), R26.2 (—, passive), R27.2 (—, passive), R382.2 (—, passive), R383.1 (—, passive), R402.1 (—, passive), R412.1 (—, passive), R422.1 (—, passive), R432.1 (—, passive), R442.1 (—, passive), R452.1 (—, passive), R462.1 (—, passive), R472.1 (—, passive), TP823.1 (1_1, passive) |

*Per-channel analog ground returns*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/AGND0 | C211.1 (—, passive) ↔ U80.7 (AGND_7, passive) |
| /driver/AGND1 | C219.1 (—, passive) ↔ U81.7 (AGND_7, passive) |
| /driver/AGND2 | C227.1 (—, passive) ↔ U82.7 (AGND_7, passive) |
| /driver/AGND3 | C235.1 (—, passive) ↔ U83.7 (AGND_7, passive) |
| /driver/AGND4 | C243.1 (—, passive) ↔ U84.7 (AGND_7, passive) |
| /driver/AGND5 | C251.1 (—, passive) ↔ U85.7 (AGND_7, passive) |
| /driver/AGND6 | C259.1 (—, passive) ↔ U86.7 (AGND_7, passive) |
| /driver/AGND7 | C267.1 (—, passive) ↔ U87.7 (AGND_7, passive) |

*Sense shunt / feedback divider*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/SA0 | R220.2 (—, passive), R221.2 (—, passive), R222.2 (—, passive), U80.2 (SA_2, passive) |
| /driver/SA1 | R230.2 (—, passive), R231.2 (—, passive), R232.2 (—, passive), U81.2 (SA_2, passive) |
| /driver/SA2 | R240.2 (—, passive), R241.2 (—, passive), R242.2 (—, passive), U82.2 (SA_2, passive) |
| /driver/SA3 | R250.2 (—, passive), R251.2 (—, passive), R252.2 (—, passive), U83.2 (SA_2, passive) |
| /driver/SA4 | R260.2 (—, passive), R261.2 (—, passive), R262.2 (—, passive), U84.2 (SA_2, passive) |
| /driver/SA5 | R270.2 (—, passive), R271.2 (—, passive), R272.2 (—, passive), U85.2 (SA_2, passive) |
| /driver/SA6 | R280.2 (—, passive), R281.2 (—, passive), R282.2 (—, passive), U86.2 (SA_2, passive) |
| /driver/SA7 | R290.2 (—, passive), R291.2 (—, passive), R292.2 (—, passive), U87.2 (SA_2, passive) |
| /driver/SB0 | R223.2 (—, passive), R224.2 (—, passive), R225.2 (—, passive), U80.11 (SB_11, passive) |
| /driver/SB1 | R233.2 (—, passive), R234.2 (—, passive), R235.2 (—, passive), U81.11 (SB_11, passive) |
| /driver/SB2 | R243.2 (—, passive), R244.2 (—, passive), R245.2 (—, passive), U82.11 (SB_11, passive) |
| /driver/SB3 | R253.2 (—, passive), R254.2 (—, passive), R255.2 (—, passive), U83.11 (SB_11, passive) |
| /driver/SB4 | R263.2 (—, passive), R264.2 (—, passive), R265.2 (—, passive), U84.11 (SB_11, passive) |
| /driver/SB5 | R273.2 (—, passive), R274.2 (—, passive), R275.2 (—, passive), U85.11 (SB_11, passive) |
| /driver/SB6 | R283.2 (—, passive), R284.2 (—, passive), R285.2 (—, passive), U86.11 (SB_11, passive) |
| /driver/SB7 | R293.2 (—, passive), R294.2 (—, passive), R295.2 (—, passive), U87.11 (SB_11, passive) |

*Sense summer and feedback*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/FEEDBACK0 | C622.2 (—, passive), R360.2 (—, passive), R622.2 (—, passive), U30.4 (IN-_4, input) |
| /driver/FEEDBACK1 | C632.2 (—, passive), R362.2 (—, passive), R632.2 (—, passive), U31.4 (IN-_4, input) |
| /driver/FEEDBACK2 | C642.2 (—, passive), R364.2 (—, passive), R642.2 (—, passive), U32.4 (IN-_4, input) |
| /driver/FEEDBACK3 | C652.2 (—, passive), R366.2 (—, passive), R652.2 (—, passive), U33.4 (IN-_4, input) |
| /driver/FEEDBACK4 | C662.2 (—, passive), R368.2 (—, passive), R662.2 (—, passive), U34.4 (IN-_4, input) |
| /driver/FEEDBACK5 | C672.2 (—, passive), R370.2 (—, passive), R672.2 (—, passive), U35.4 (IN-_4, input) |
| /driver/FEEDBACK6 | C682.2 (—, passive), R372.2 (—, passive), R682.2 (—, passive), U36.4 (IN-_4, input) |
| /driver/FEEDBACK7 | C692.2 (—, passive), R374.2 (—, passive), R692.2 (—, passive), U37.4 (IN-_4, input) |
| /driver/SUM_NODE | R200.2 (—, passive), R201.2 (—, passive), R202.2 (—, passive), R203.2 (—, passive), R204.2 (—, passive), R205.2 (—, passive), R206.2 (—, passive), R207.2 (—, passive), R208.2 (—, passive), U38.4 (IN-_4, input) |

*Single-supply buffer bias*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /driver/BUF0 | C212.1 (—, passive), TP820.1 (1_1, passive), U20.6 (VOUT_6, output) |
| /driver/BUF1 | C220.1 (—, passive) ↔ U21.6 (VOUT_6, output) |
| /driver/BUF2 | C228.1 (—, passive) ↔ U22.6 (VOUT_6, output) |
| /driver/BUF3 | C236.1 (—, passive) ↔ U23.6 (VOUT_6, output) |
| /driver/BUF4 | C244.1 (—, passive) ↔ U24.6 (VOUT_6, output) |
| /driver/BUF5 | C252.1 (—, passive) ↔ U25.6 (VOUT_6, output) |
| /driver/BUF6 | C260.1 (—, passive) ↔ U26.6 (VOUT_6, output) |
| /driver/BUF7 | C268.1 (—, passive) ↔ U27.6 (VOUT_6, output) |

**No-connects**

| Pin (no-connect) | Pin name | Pin type | Reason |
|---|---|---|---|
| U20.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U20.8 | NC_8 | no_connect | No reason stated in schematic |
| U21.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U21.8 | NC_8 | no_connect | No reason stated in schematic |
| U22.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U22.8 | NC_8 | no_connect | No reason stated in schematic |
| U23.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U23.8 | NC_8 | no_connect | No reason stated in schematic |
| U24.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U24.8 | NC_8 | no_connect | No reason stated in schematic |
| U25.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U25.8 | NC_8 | no_connect | No reason stated in schematic |
| U26.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U26.8 | NC_8 | no_connect | No reason stated in schematic |
| U27.1 | EF_1 | open_collector+no_connect | No reason stated in schematic |
| U27.8 | NC_8 | no_connect | No reason stated in schematic |

## 3.4 Page 4 — receiver

**Purpose.** Four-channel acquisition: AD7768-4 with ADR434 reference and INA163/ADA4940-2 front ends for current, pen 1, pen 2 and reference coil.

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 0 | not on this sheet |
| +3.3V | 4 | sink |
| GND | 79 | common return |
| +12VA | 16 | sink |
| -12VA | 12 | sink |
| +5VA | 26 | sink |
| +5V_EXC | 0 | not on this sheet |
| +1V0_FPGA | 0 | not on this sheet |
| +1V8_FPGA | 0 | not on this sheet |
| +1V8 | 0 | not present in netlist |

**Inputs** (crossing nets arriving on this sheet)

| Net | Pins on this sheet | From sheet | Signal |
|---|---|---|---|
| ADC_CS | U101.16 | fpga | AD7768-4 control input (ADC_CS): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_RESET_N | U101.30 | fpga | AD7768-4 control input (ADC_RESET_N): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SCLK | U101.17 | fpga | AD7768-4 control input (ADC_SCLK): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SDI | U101.18 | fpga | AD7768-4 control input (ADC_SDI): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_START_N | U101.37 | fpga | AD7768-4 control input (ADC_START_N): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SYNC_IN | U101.36 | fpga | AD7768-4 control input (ADC_SYNC_IN): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| CLOCK_32M768 | R100.1 | fpga | 32.768 MHz clock: Y1 output drives U4.D13 and, via R100, the AD7768-4 MCLK. |
| CURRENT_SUM | R110.1 | driver | Eight-tone current-sum monitor: U38 OPA192 output via R200/R110 into ADC Ch0. |
| PEN1_N | R102.1 | connectors | Sensor differential pair at J122 → 100 Ω input resistor → receiver front end. |
| PEN1_P | R101.1 | connectors | Sensor differential pair at J122 → 100 Ω input resistor → receiver front end. |
| PEN2_N | R541.1 | connectors | Sensor differential pair at J127 → 100 Ω input resistor → receiver front end. |
| PEN2_P | R540.1 | connectors | Sensor differential pair at J127 → 100 Ω input resistor → receiver front end. |
| REF_COIL_N | R561.1 | connectors | Sensor differential pair at J128 → 100 Ω input resistor → receiver front end. |
| REF_COIL_P | R560.1 | connectors | Sensor differential pair at J128 → 100 Ω input resistor → receiver front end. |

**Outputs** (crossing nets leaving this sheet)

| Net | Pins on this sheet | To sheet(s) | Signal |
|---|---|---|---|
| ADC_DCLK | U101.28 | fpga | AD7768-4 capture output (ADC_DCLK): U101 → FPGA U4. |
| ADC_DOUT0 | U101.27 | fpga | AD7768-4 capture output (ADC_DOUT0): U101 → FPGA U4. |
| ADC_DOUT1 | U101.26 | fpga | AD7768-4 capture output (ADC_DOUT1): U101 → FPGA U4. |
| ADC_DOUT2 | U101.25 | fpga | AD7768-4 capture output (ADC_DOUT2): U101 → FPGA U4. |
| ADC_DOUT3 | U101.24 | fpga | AD7768-4 capture output (ADC_DOUT3): U101 → FPGA U4. |
| ADC_DRDY_N | U101.29 | fpga | AD7768-4 capture output (ADC_DRDY_N): U101 → FPGA U4. |
| ADC_SDO | U101.19 | fpga | AD7768-4 capture output (ADC_SDO): U101 → FPGA U4. |
| ADC_SYNC_OUT | U101.38 | fpga | AD7768-4 capture output (ADC_SYNC_OUT): U101 → FPGA U4. |

**Internal connections** (nets whose pins are all on this sheet)

*ADC analog inputs and drivers*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /receiver/AIN0+ | C120.1 (—, passive), C122.1 (—, passive), R114.2 (—, passive), U101.64 (AIN0+_64, input) |
| /receiver/AIN0- | C121.1 (—, passive), C122.2 (—, passive), R115.2 (—, passive), U101.63 (AIN0-_63, input) |
| /receiver/AIN1+ | C125.1 (—, passive), C127.1 (—, passive), R124.2 (—, passive), U101.2 (AIN1+_2, input) |
| /receiver/AIN1- | C126.1 (—, passive), C127.2 (—, passive), R125.2 (—, passive), U101.1 (AIN1-_1, input) |
| /receiver/AIN2+ | C544.1 (—, passive), C546.1 (—, passive), R552.2 (—, passive), U101.49 (AIN2+_49, input) |
| /receiver/AIN2- | C545.1 (—, passive), C546.2 (—, passive), R553.2 (—, passive), U101.50 (AIN2-_50, input) |
| /receiver/AIN3+ | C564.1 (—, passive), C566.1 (—, passive), R572.2 (—, passive), U101.47 (AIN3+_47, input) |
| /receiver/AIN3- | C565.1 (—, passive), C566.2 (—, passive), R573.2 (—, passive), U101.48 (AIN3-_48, input) |
| /receiver/FDA0_N | R111.2 (—, passive), R113.2 (—, passive), U105.1 (-IN1_1, input) |
| /receiver/FDA0_OUT_N | R112.1 (—, passive), R115.1 (—, passive), U105.19 (-OUT1_19, output), U105.23 (-FB1_23, passive) |
| /receiver/FDA0_OUT_P | R113.1 (—, passive), R114.1 (—, passive), U105.18 (+OUT1_18, output), U105.2 (+FB1_2, passive) |
| /receiver/FDA1_N | R121.2 (—, passive), R123.2 (—, passive), U105.7 (-IN2_7, input) |
| /receiver/FDA1_OUT_N | R122.1 (—, passive), R125.1 (—, passive), U105.13 (-OUT2_13, output), U105.5 (-FB2_5, passive) |
| /receiver/FDA1_OUT_P | R123.1 (—, passive), R124.1 (—, passive), U105.12 (+OUT2_12, output), U105.8 (+FB2_8, passive) |
| /receiver/FDA2_N | R549.2 (—, passive), R551.2 (—, passive), U108.1 (-IN1_1, input) |
| /receiver/FDA2_OUT_N | R550.1 (—, passive), R553.1 (—, passive), U108.19 (-OUT1_19, output), U108.23 (-FB1_23, passive) |
| /receiver/FDA2_OUT_P | R551.1 (—, passive), R552.1 (—, passive), U108.18 (+OUT1_18, output), U108.2 (+FB1_2, passive) |
| /receiver/FDA3_N | R569.2 (—, passive), R571.2 (—, passive), U108.7 (-IN2_7, input) |
| /receiver/FDA3_OUT_N | R570.1 (—, passive), R573.1 (—, passive), U108.13 (-OUT2_13, output), U108.5 (-FB2_5, passive) |
| /receiver/FDA3_OUT_P | R571.1 (—, passive), R572.1 (—, passive), U108.12 (+OUT2_12, output), U108.8 (+FB2_8, passive) |

*ADC reference and support*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /receiver/ADC_DAISY_IN | R181.1 (—, passive) ↔ U101.21 (DIN_21, input) |
| /receiver/ADC_REF | C101.1 (—, passive), C102.1 (—, passive), D534.2 (A_2, passive), R184.2 (—, passive), U101.43 (REF2+_43, input), U101.6 (REF1+_6, input) |
| /receiver/ADC_SPI_STRAP | R180.2 (—, passive) ↔ U101.11 (FILTER/GPIO4_11, bidirectional) |
| /receiver/ADC_VCM | C106.1 (—, passive), U101.59 (VCM_59, output), U105.11 (VOCM2_11, input), U105.17 (VOCM1_17, input), U108.11 (VOCM2_11, input), U108.17 (VOCM1_17, input) |

*Local two-/three-pin joins*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| Net-(U104-SENSE) | R120.1 (—, passive), U104.8 (SENSE_8, input), U104.9 (VO_9, output) |
| Net-(U105A-+IN1) | R110.2 (—, passive), R112.2 (—, passive), U105.24 (+IN1_24, input) |
| Net-(U105B-+IN2) | R120.2 (—, passive), R122.2 (—, passive), U105.6 (+IN2_6, input) |
| Net-(U106-SENSE) | R548.1 (—, passive), U106.8 (SENSE_8, input), U106.9 (VO_9, output) |
| Net-(U107-SENSE) | R568.1 (—, passive), U107.8 (SENSE_8, input), U107.9 (VO_9, output) |
| Net-(U108A-+IN1) | R548.2 (—, passive), R550.2 (—, passive), U108.24 (+IN1_24, input) |
| Net-(U108B-+IN2) | R568.2 (—, passive), R570.2 (—, passive), U108.6 (+IN2_6, input) |

*No-connect stubs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| unconnected-(U101-DNC-Pad22) | U101.22 (DNC_22, no_connect) |
| unconnected-(U101-DNC-Pad23) | U101.23 (DNC_23, no_connect) |
| unconnected-(U101-DNC/DGND-Pad20) | U101.20 (DNC/DGND_20, passive+no_connect) |
| unconnected-(U101-MODE0/GPIO0-Pad12) | U101.12 (MODE0/GPIO0_12, bidirectional+no_connect) |
| unconnected-(U101-MODE1/GPIO1-Pad13) | U101.13 (MODE1/GPIO1_13, bidirectional+no_connect) |
| unconnected-(U101-MODE2/GPIO2-Pad14) | U101.14 (MODE2/GPIO2_14, bidirectional+no_connect) |
| unconnected-(U101-MODE3/GPIO3-Pad15) | U101.15 (MODE3/GPIO3_15, bidirectional+no_connect) |
| unconnected-(U102-COMP-Pad7) | U102.7 (COMP_7, passive+no_connect) |
| unconnected-(U102-DNC-Pad1) | U102.1 (DNC_1, no_connect) |
| unconnected-(U102-DNC-Pad8) | U102.8 (DNC_8, no_connect) |
| unconnected-(U102-NIC-Pad3) | U102.3 (NIC_3, no_connect) |
| unconnected-(U102-TRIM-Pad5) | U102.5 (TRIM_5, passive+no_connect) |
| unconnected-(U104-NC-Pad13) | U104.13 (NC_13, no_connect) |
| unconnected-(U104-NC-Pad2) | U104.2 (NC_2, no_connect) |
| unconnected-(U104-NC-Pad7) | U104.7 (NC_7, no_connect) |
| unconnected-(U104-VO1-Pad1) | U104.1 (VO1_1, output+no_connect) |
| unconnected-(U104-VO2-Pad14) | U104.14 (VO2_14, output+no_connect) |
| unconnected-(U106-NC-Pad13) | U106.13 (NC_13, no_connect) |
| unconnected-(U106-NC-Pad2) | U106.2 (NC_2, no_connect) |
| unconnected-(U106-NC-Pad7) | U106.7 (NC_7, no_connect) |
| unconnected-(U106-VO1-Pad1) | U106.1 (VO1_1, output+no_connect) |
| unconnected-(U106-VO2-Pad14) | U106.14 (VO2_14, output+no_connect) |
| unconnected-(U107-NC-Pad13) | U107.13 (NC_13, no_connect) |
| unconnected-(U107-NC-Pad2) | U107.2 (NC_2, no_connect) |
| unconnected-(U107-NC-Pad7) | U107.7 (NC_7, no_connect) |
| unconnected-(U107-VO1-Pad1) | U107.1 (VO1_1, output+no_connect) |
| unconnected-(U107-VO2-Pad14) | U107.14 (VO2_14, output+no_connect) |

*Receiver support nets*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /receiver/DREGCAP | C103.1 (—, passive) ↔ U101.34 (DREGCAP_34, power_out) |
| /receiver/GAIN1 | R105.1 (—, passive) ↔ U104.3 (GS1_3, passive) |
| /receiver/GAIN2 | R105.2 (—, passive) ↔ U104.12 (GS2_12, passive) |
| /receiver/MCLK | R100.2 (—, passive) ↔ U101.32 (XTAL2/MCLK_32, input) |
| /receiver/REF_BUF_OUT | R184.1 (—, passive), U103.1 (OUT_1, output), U103.4 (IN-_4, input) |
| /receiver/REF_RAW | C131.1 (—, passive), U102.6 (VOUT_6, power_out), U103.3 (IN+_3, input) |
| /receiver/REGCAPA | C104.1 (—, passive) ↔ U101.61 (REGCAPA_61, power_out) |
| /receiver/REGCAPB | C105.1 (—, passive) ↔ U101.52 (REGCAPB_52, power_out) |

*Sensor front ends*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /receiver/INA_IN_N | C114.2 (—, passive), R104.1 (—, passive), U104.4 (IN-_4, input) |
| /receiver/INA_IN_P | C113.2 (—, passive), R103.1 (—, passive), U104.5 (IN+_5, input) |
| /receiver/PEN1_PROT_N | C114.1 (—, passive), D103.2 (A_2, passive), D104.1 (K_1, passive), R102.2 (—, passive) |
| /receiver/PEN1_PROT_P | C113.1 (—, passive), D101.2 (A_2, passive), D102.1 (K_1, passive), R101.2 (—, passive) |
| /receiver/PEN2_IN_N | C541.2 (—, passive), R543.1 (—, passive), U106.4 (IN-_4, input) |
| /receiver/PEN2_IN_P | C540.2 (—, passive), R542.1 (—, passive), U106.5 (IN+_5, input) |
| /receiver/PEN2_PROT_N | C541.1 (—, passive), D522.2 (A_2, passive), D523.1 (K_1, passive), R541.2 (—, passive) |
| /receiver/PEN2_PROT_P | C540.1 (—, passive), D520.2 (A_2, passive), D521.1 (K_1, passive), R540.2 (—, passive) |
| /receiver/PEN2_RG1 | R544.1 (—, passive) ↔ U106.3 (GS1_3, passive) |
| /receiver/PEN2_RG2 | R544.2 (—, passive) ↔ U106.12 (GS2_12, passive) |
| /receiver/REF_COIL_IN_N | C561.2 (—, passive), R563.1 (—, passive), U107.4 (IN-_4, input) |
| /receiver/REF_COIL_IN_P | C560.2 (—, passive), R562.1 (—, passive), U107.5 (IN+_5, input) |
| /receiver/REF_COIL_PROT_N | C561.1 (—, passive), D532.2 (A_2, passive), D533.1 (K_1, passive), R561.2 (—, passive) |
| /receiver/REF_COIL_PROT_P | C560.1 (—, passive), D530.2 (A_2, passive), D531.1 (K_1, passive), R560.2 (—, passive) |
| /receiver/REF_COIL_RG1 | R564.1 (—, passive) ↔ U107.3 (GS1_3, passive) |
| /receiver/REF_COIL_RG2 | R564.2 (—, passive) ↔ U107.12 (GS2_12, passive) |

**No-connects**

| Pin (no-connect) | Pin name | Pin type | Reason |
|---|---|---|---|
| U101.12 | MODE0/GPIO0_12 | bidirectional+no_connect | No reason stated in schematic |
| U101.13 | MODE1/GPIO1_13 | bidirectional+no_connect | No reason stated in schematic |
| U101.14 | MODE2/GPIO2_14 | bidirectional+no_connect | No reason stated in schematic |
| U101.15 | MODE3/GPIO3_15 | bidirectional+no_connect | No reason stated in schematic |
| U101.20 | DNC/DGND_20 | passive+no_connect | No reason stated in schematic |
| U101.22 | DNC_22 | no_connect | No reason stated in schematic |
| U101.23 | DNC_23 | no_connect | No reason stated in schematic |
| U102.1 | DNC_1 | no_connect | No reason stated in schematic |
| U102.3 | NIC_3 | no_connect | No reason stated in schematic |
| U102.5 | TRIM_5 | passive+no_connect | No reason stated in schematic |
| U102.7 | COMP_7 | passive+no_connect | No reason stated in schematic |
| U102.8 | DNC_8 | no_connect | No reason stated in schematic |
| U104.1 | VO1_1 | output+no_connect | No reason stated in schematic |
| U104.13 | NC_13 | no_connect | No reason stated in schematic |
| U104.14 | VO2_14 | output+no_connect | No reason stated in schematic |
| U104.2 | NC_2 | no_connect | No reason stated in schematic |
| U104.7 | NC_7 | no_connect | No reason stated in schematic |
| U106.1 | VO1_1 | output+no_connect | No reason stated in schematic |
| U106.13 | NC_13 | no_connect | No reason stated in schematic |
| U106.14 | VO2_14 | output+no_connect | No reason stated in schematic |
| U106.2 | NC_2 | no_connect | No reason stated in schematic |
| U106.7 | NC_7 | no_connect | No reason stated in schematic |
| U107.1 | VO1_1 | output+no_connect | No reason stated in schematic |
| U107.13 | NC_13 | no_connect | No reason stated in schematic |
| U107.14 | VO2_14 | output+no_connect | No reason stated in schematic |
| U107.2 | NC_2 | no_connect | No reason stated in schematic |
| U107.7 | NC_7 | no_connect | No reason stated in schematic |

## 3.5 Page 5 — fpga

**Purpose.** Artix-7 FTG256 ball map, QSPI configuration, JTAG, 32.768 MHz clock, FT231X USB-UART and Pico signals.

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 0 | not on this sheet |
| +3.3V | 63 | sink |
| GND | 80 | common return |
| +12VA | 0 | not on this sheet |
| -12VA | 0 | not on this sheet |
| +5VA | 0 | not on this sheet |
| +5V_EXC | 0 | not on this sheet |
| +1V0_FPGA | 17 | sink |
| +1V8_FPGA | 11 | sink |
| +1V8 | 0 | not present in netlist |

**Inputs** (crossing nets arriving on this sheet)

| Net | Pins on this sheet | From sheet | Signal |
|---|---|---|---|
| /DRIVER_FAULT_N | U4.R1 | driver | Active-low coil overcurrent bus: U600–U603 open-drain + R712 pull-up; clears U752 latch and is read by U4.R1. |
| ADC_DCLK | U4.C11 | receiver | AD7768-4 capture output (ADC_DCLK): U101 → FPGA U4. |
| ADC_DOUT0 | U4.A8 | receiver | AD7768-4 capture output (ADC_DOUT0): U101 → FPGA U4. |
| ADC_DOUT1 | U4.A9 | receiver | AD7768-4 capture output (ADC_DOUT1): U101 → FPGA U4. |
| ADC_DOUT2 | U4.B9 | receiver | AD7768-4 capture output (ADC_DOUT2): U101 → FPGA U4. |
| ADC_DOUT3 | U4.A10 | receiver | AD7768-4 capture output (ADC_DOUT3): U101 → FPGA U4. |
| ADC_DRDY_N | U4.B10 | receiver | AD7768-4 capture output (ADC_DRDY_N): U101 → FPGA U4. |
| ADC_SDO | U4.B11 | receiver | AD7768-4 capture output (ADC_SDO): U101 → FPGA U4. |
| ADC_SYNC_OUT | U4.A15 | receiver | AD7768-4 capture output (ADC_SYNC_OUT): U101 → FPGA U4. |
| DAC_SDO | U4.M4 | driver | DAC80508 SDO/~ALARM status return: U10.15 → FPGA U4.M4. |
| PICO_RX | U4.N3 | connectors | UART Pico → FPGA, J123.4 (schematic text). |
| USB_DM | R161.1 | connectors | Bidirectional USB 2.0 data: J124 USB-C → ESD → 27 Ω R160/R161 → FT231X; netlist pins are passive/bidirectional. |
| USB_DP | R160.1 | connectors | Bidirectional USB 2.0 data: J124 USB-C → ESD → 27 Ω R160/R161 → FT231X; netlist pins are passive/bidirectional. |
| USB_VBUS | R158.1 | connectors | USB-C VBUS sense: J124 A4/A9/B4/B9 → R158 → FT231X CBUS2. |

**Outputs** (crossing nets leaving this sheet)

| Net | Pins on this sheet | To sheet(s) | Signal |
|---|---|---|---|
| /BUCK_SYNC | U4.R3 | power | 1.024 MHz buck sync: FPGA U4.R3 through C809 into U147 EN/SYNC. |
| ADC_CS | R164.2, U4.B12 | receiver | AD7768-4 control input (ADC_CS): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_RESET_N | R163.2, U4.A14 | receiver | AD7768-4 control input (ADC_RESET_N): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SCLK | U4.A13 | receiver | AD7768-4 control input (ADC_SCLK): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SDI | U4.A12 | receiver | AD7768-4 control input (ADC_SDI): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_START_N | R165.2, U4.B14 | receiver | AD7768-4 control input (ADC_START_N): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| ADC_SYNC_IN | R166.2, U4.C14 | receiver | AD7768-4 control input (ADC_SYNC_IN): FPGA U4 → U101, with series/pull strap on the fpga sheet. |
| CLOCK_32M768 | U4.D13, Y1.3 | receiver | 32.768 MHz clock: Y1 output drives U4.D13 and, via R100, the AD7768-4 MCLK. |
| DAC_CS | R145.2, R162.2 | driver | DAC80508 control input (DAC_CS): FPGA U4 → 33 Ω series resistor → U10. |
| DAC_SCLK | R146.2 | driver | DAC80508 control input (DAC_SCLK): FPGA U4 → 33 Ω series resistor → U10. |
| DAC_SDI | R147.2 | driver | DAC80508 control input (DAC_SDI): FPGA U4 → 33 Ω series resistor → U10. |
| PICO_HEARTBEAT | U4.P3 | connectors | 100 Hz heartbeat level from FPGA U4.P3 → J123.6. |
| PICO_STOP_REQ_N | U4.P4 | power | Active-low STOP request from FPGA U4.P4 (R754 pull-down) into U755.1. |
| PICO_TX | U4.N2 | connectors | UART FPGA → Pico (schematic text: FPGA transmits, Pico receives), J123.3. |

**Internal connections** (nets whose pins are all on this sheet)

*FPGA support nets*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /fpga/DAC_CS_SRC | R145.1 (—, passive) ↔ U4.M2 (IO_L2P_T0_34_M2, bidirectional) |
| /fpga/DAC_SCLK_SRC | R146.1 (—, passive) ↔ U4.M1 (IO_L2N_T0_34_M1, bidirectional) |
| /fpga/DAC_SDI_SRC | R147.1 (—, passive) ↔ U4.L4 (IO_L1P_T0_34_L4, bidirectional) |

*JTAG and configuration straps*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /fpga/CFGBVS | R154.2 (—, passive) ↔ U4.E7 (CFGBVS_0_E7, bidirectional) |
| /fpga/JTAG_TCK | J140.6 (TCK_6, passive) ↔ U4.L7 (TCK_0_L7, bidirectional) |
| /fpga/JTAG_TDI | J140.10 (TDI_10, passive) ↔ U4.N7 (TDI_0_N7, bidirectional) |
| /fpga/JTAG_TDO | J140.8 (TDO_8, passive) ↔ U4.N8 (TDO_0_N8, bidirectional) |
| /fpga/JTAG_TMS | J140.4 (TMS_4, passive) ↔ U4.M7 (TMS_0_M7, bidirectional) |
| /fpga/MODE0 | R155.2 (—, passive) ↔ U4.M9 (M0_0_M9, bidirectional) |
| /fpga/MODE1 | R156.2 (—, passive) ↔ U4.M10 (M1_0_M10, bidirectional) |
| /fpga/MODE2 | R157.2 (—, passive) ↔ U4.M11 (M2_0_M11, bidirectional) |
| /fpga/PUDC_N | R141.2 (—, passive) ↔ U4.L15 (IO_L3P_T0_DQS_PUDC_B_14_L15, bidirectional) |

*Local two-/three-pin joins*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| Net-(U141-CLK) | R790.2 (—, passive) ↔ U141.6 (CLK_6, input) |
| Net-(U4C-CCLK_0) | R790.1 (—, passive) ↔ U4.E8 (CCLK_0_E8, bidirectional) |
| Net-(U4C-DONE_0) | R143.2 (—, passive), TP792.1 (1_1, passive), U4.H10 (DONE_0_H10, bidirectional) |
| Net-(U4C-INIT_B_0) | R142.2 (—, passive), TP791.1 (1_1, passive), U4.K10 (INIT_B_0_K10, bidirectional) |
| Net-(U4C-PROGRAM_B_0) | R144.2 (—, passive), TP790.1 (1_1, passive), U4.L9 (PROGRAM_B_0_L9, bidirectional) |

*No-connect stubs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| unconnected-(J140-HALT-Pad14) | J140.14 (HALT_14, passive+no_connect) |
| unconnected-(J140-NC-Pad1) | J140.1 (NC_1, no_connect) |
| unconnected-(J140-NC-Pad12) | J140.12 (NC_12, no_connect) |
| unconnected-(J140-PGND-Pad13) | J140.13 (PGND_13, passive+no_connect) |
| unconnected-(U142-CBUS0-Pad15) | U142.15 (CBUS0_15, bidirectional+no_connect) |
| unconnected-(U142-CBUS1-Pad14) | U142.14 (CBUS1_14, bidirectional+no_connect) |
| unconnected-(U142-CBUS3-Pad16) | U142.16 (CBUS3_16, bidirectional+no_connect) |
| unconnected-(U142-~{DTR}-Pad18) | U142.18 (~{DTR}_18, output+no_connect) |
| unconnected-(U142-~{RTS}-Pad19) | U142.19 (~{RTS}_19, output+no_connect) |
| unconnected-(U4A-IO_0_14-PadK12) | U4.K12 (IO_0_14_K12, bidirectional+no_connect) |
| unconnected-(U4A-IO_0_15-PadD10) | U4.D10 (IO_0_15_D10, bidirectional+no_connect) |
| unconnected-(U4A-IO_25_14-PadP6) | U4.P6 (IO_25_14_P6, bidirectional+no_connect) |
| unconnected-(U4A-IO_25_15-PadG11) | U4.G11 (IO_25_15_G11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L10N_T1_AD11N_15-PadB16) | U4.B16 (IO_L10N_T1_AD11N_15_B16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L10N_T1_D15_14-PadT15) | U4.T15 (IO_L10N_T1_D15_14_T15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L10P_T1_AD11P_15-PadC16) | U4.C16 (IO_L10P_T1_AD11P_15_C16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L10P_T1_D14_14-PadT14) | U4.T14 (IO_L10P_T1_D14_14_T14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L11N_T1_SRCC_14-PadP13) | U4.P13 (IO_L11N_T1_SRCC_14_P13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L11N_T1_SRCC_15-PadC12) | U4.C12 (IO_L11N_T1_SRCC_15_C12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L11P_T1_SRCC_14-PadN13) | U4.N13 (IO_L11P_T1_SRCC_14_N13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L12N_T1_MRCC_14-PadP14) | U4.P14 (IO_L12N_T1_MRCC_14_P14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L12N_T1_MRCC_15-PadC13) | U4.C13 (IO_L12N_T1_MRCC_15_C13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L12P_T1_MRCC_14-PadN14) | U4.N14 (IO_L12P_T1_MRCC_14_N14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L13N_T2_MRCC_14-PadN12) | U4.N12 (IO_L13N_T2_MRCC_14_N12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L13N_T2_MRCC_15-PadE13) | U4.E13 (IO_L13N_T2_MRCC_15_E13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L13P_T2_MRCC_14-PadN11) | U4.N11 (IO_L13P_T2_MRCC_14_N11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L13P_T2_MRCC_15-PadE12) | U4.E12 (IO_L13P_T2_MRCC_15_E12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L14N_T2_SRCC_14-PadP11) | U4.P11 (IO_L14N_T2_SRCC_14_P11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L14N_T2_SRCC_15-PadD11) | U4.D11 (IO_L14N_T2_SRCC_15_D11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L14P_T2_SRCC_14-PadP10) | U4.P10 (IO_L14P_T2_SRCC_14_P10, bidirectional+no_connect) |
| unconnected-(U4A-IO_L14P_T2_SRCC_15-PadE11) | U4.E11 (IO_L14P_T2_SRCC_15_E11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L15N_T2_DQS_ADV_B_15-PadD15) | U4.D15 (IO_L15N_T2_DQS_ADV_B_15_D15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L15N_T2_DQS_DOUT_CSO_B_14-PadT12) | U4.T12 (IO_L15N_T2_DQS_DOUT_CSO_B_14_T12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L15P_T2_DQS_15-PadD14) | U4.D14 (IO_L15P_T2_DQS_15_D14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L15P_T2_DQS_RDWR_B_14-PadR12) | U4.R12 (IO_L15P_T2_DQS_RDWR_B_14_R12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L16N_T2_A15_D31_14-PadT13) | U4.T13 (IO_L16N_T2_A15_D31_14_T13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L16N_T2_A27_15-PadF13) | U4.F13 (IO_L16N_T2_A27_15_F13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L16P_T2_A28_15-PadF12) | U4.F12 (IO_L16P_T2_A28_15_F12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L16P_T2_CSI_B_14-PadR13) | U4.R13 (IO_L16P_T2_CSI_B_14_R13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L17N_T2_A13_D29_14-PadR11) | U4.R11 (IO_L17N_T2_A13_D29_14_R11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L17N_T2_A25_15-PadD16) | U4.D16 (IO_L17N_T2_A25_15_D16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L17P_T2_A14_D30_14-PadR10) | U4.R10 (IO_L17P_T2_A14_D30_14_R10, bidirectional+no_connect) |
| unconnected-(U4A-IO_L17P_T2_A26_15-PadE16) | U4.E16 (IO_L17P_T2_A26_15_E16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L18N_T2_A11_D27_14-PadP9) | U4.P9 (IO_L18N_T2_A11_D27_14_P9, bidirectional+no_connect) |
| unconnected-(U4A-IO_L18N_T2_A23_15-PadE15) | U4.E15 (IO_L18N_T2_A23_15_E15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L18P_T2_A12_D28_14-PadN9) | U4.N9 (IO_L18P_T2_A12_D28_14_N9, bidirectional+no_connect) |
| unconnected-(U4A-IO_L18P_T2_A24_15-PadF15) | U4.F15 (IO_L18P_T2_A24_15_F15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L19N_T3_A09_D25_VREF_14-PadN6) | U4.N6 (IO_L19N_T3_A09_D25_VREF_14_N6, bidirectional+no_connect) |
| unconnected-(U4A-IO_L19N_T3_A21_VREF_15-PadG12) | U4.G12 (IO_L19N_T3_A21_VREF_15_G12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L19P_T3_A10_D26_14-PadM6) | U4.M6 (IO_L19P_T3_A10_D26_14_M6, bidirectional+no_connect) |
| unconnected-(U4A-IO_L19P_T3_A22_15-PadH11) | U4.H11 (IO_L19P_T3_A22_15_H11, bidirectional+no_connect) |
| unconnected-(U4A-IO_L1N_T0_AD0N_15-PadC9) | U4.C9 (IO_L1N_T0_AD0N_15_C9, bidirectional+no_connect) |
| unconnected-(U4A-IO_L1P_T0_AD0P_15-PadC8) | U4.C8 (IO_L1P_T0_AD0P_15_C8, bidirectional+no_connect) |
| unconnected-(U4A-IO_L20N_T3_A07_D23_14-PadR8) | U4.R8 (IO_L20N_T3_A07_D23_14_R8, bidirectional+no_connect) |
| unconnected-(U4A-IO_L20N_T3_A19_15-PadH13) | U4.H13 (IO_L20N_T3_A19_15_H13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L20P_T3_A08_D24_14-PadP8) | U4.P8 (IO_L20P_T3_A08_D24_14_P8, bidirectional+no_connect) |
| unconnected-(U4A-IO_L20P_T3_A20_15-PadH12) | U4.H12 (IO_L20P_T3_A20_15_H12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L21N_T3_DQS_A06_D22_14-PadT8) | U4.T8 (IO_L21N_T3_DQS_A06_D22_14_T8, bidirectional+no_connect) |
| unconnected-(U4A-IO_L21N_T3_DQS_A18_15-PadF14) | U4.F14 (IO_L21N_T3_DQS_A18_15_F14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L21P_T3_DQS_14-PadT7) | U4.T7 (IO_L21P_T3_DQS_14_T7, bidirectional+no_connect) |
| unconnected-(U4A-IO_L21P_T3_DQS_15-PadG14) | U4.G14 (IO_L21P_T3_DQS_15_G14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L22N_T3_A04_D20_14-PadT10) | U4.T10 (IO_L22N_T3_A04_D20_14_T10, bidirectional+no_connect) |
| unconnected-(U4A-IO_L22N_T3_A16_15-PadG16) | U4.G16 (IO_L22N_T3_A16_15_G16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L22P_T3_A05_D21_14-PadT9) | U4.T9 (IO_L22P_T3_A05_D21_14_T9, bidirectional+no_connect) |
| unconnected-(U4A-IO_L22P_T3_A17_15-PadH16) | U4.H16 (IO_L22P_T3_A17_15_H16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L23N_T3_A02_D18_14-PadT5) | U4.T5 (IO_L23N_T3_A02_D18_14_T5, bidirectional+no_connect) |
| unconnected-(U4A-IO_L23N_T3_FWE_B_15-PadJ16) | U4.J16 (IO_L23N_T3_FWE_B_15_J16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L23P_T3_A03_D19_14-PadR5) | U4.R5 (IO_L23P_T3_A03_D19_14_R5, bidirectional+no_connect) |
| unconnected-(U4A-IO_L23P_T3_FOE_B_15-PadJ15) | U4.J15 (IO_L23P_T3_FOE_B_15_J15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L24N_T3_A00_D16_14-PadR7) | U4.R7 (IO_L24N_T3_A00_D16_14_R7, bidirectional+no_connect) |
| unconnected-(U4A-IO_L24N_T3_RS0_15-PadG15) | U4.G15 (IO_L24N_T3_RS0_15_G15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L24P_T3_A01_D17_14-PadR6) | U4.R6 (IO_L24P_T3_A01_D17_14_R6, bidirectional+no_connect) |
| unconnected-(U4A-IO_L24P_T3_RS1_15-PadH14) | U4.H14 (IO_L24P_T3_RS1_15_H14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L3N_T0_DQS_EMCCLK_14-PadM15) | U4.M15 (IO_L3N_T0_DQS_EMCCLK_14_M15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L4N_T0_D05_14-PadM14) | U4.M14 (IO_L4N_T0_D05_14_M14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L4P_T0_D04_14-PadL14) | U4.L14 (IO_L4P_T0_D04_14_L14, bidirectional+no_connect) |
| unconnected-(U4A-IO_L5N_T0_D07_14-PadL13) | U4.L13 (IO_L5N_T0_D07_14_L13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L5P_T0_D06_14-PadK13) | U4.K13 (IO_L5P_T0_D06_14_K13, bidirectional+no_connect) |
| unconnected-(U4A-IO_L6N_T0_D08_VREF_14-PadM12) | U4.M12 (IO_L6N_T0_D08_VREF_14_M12, bidirectional+no_connect) |
| unconnected-(U4A-IO_L6N_T0_VREF_15-PadD9) | U4.D9 (IO_L6N_T0_VREF_15_D9, bidirectional+no_connect) |
| unconnected-(U4A-IO_L6P_T0_15-PadD8) | U4.D8 (IO_L6P_T0_15_D8, bidirectional+no_connect) |
| unconnected-(U4A-IO_L7N_T1_D10_14-PadN16) | U4.N16 (IO_L7N_T1_D10_14_N16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L7P_T1_D09_14-PadM16) | U4.M16 (IO_L7P_T1_D09_14_M16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L8N_T1_D12_14-PadP16) | U4.P16 (IO_L8N_T1_D12_14_P16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L8P_T1_D11_14-PadP15) | U4.P15 (IO_L8P_T1_D11_14_P15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L9N_T1_DQS_D13_14-PadR16) | U4.R16 (IO_L9N_T1_DQS_D13_14_R16, bidirectional+no_connect) |
| unconnected-(U4A-IO_L9P_T1_DQS_14-PadR15) | U4.R15 (IO_L9P_T1_DQS_14_R15, bidirectional+no_connect) |
| unconnected-(U4A-IO_L9P_T1_DQS_AD3P_15-PadB15) | U4.B15 (IO_L9P_T1_DQS_AD3P_15_B15, bidirectional+no_connect) |
| unconnected-(U4B-IO_0_34-PadL5) | U4.L5 (IO_0_34_L5, bidirectional+no_connect) |
| unconnected-(U4B-IO_0_35-PadE6) | U4.E6 (IO_0_35_E6, bidirectional+no_connect) |
| unconnected-(U4B-IO_25_35-PadK5) | U4.K5 (IO_25_35_K5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L10N_T1_AD15N_35-PadD1) | U4.D1 (IO_L10N_T1_AD15N_35_D1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L10P_T1_34-PadP5) | U4.P5 (IO_L10P_T1_34_P5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L10P_T1_AD15P_35-PadE2) | U4.E2 (IO_L10P_T1_AD15P_35_E2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L11N_T1_SRCC_35-PadD3) | U4.D3 (IO_L11N_T1_SRCC_35_D3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L11P_T1_SRCC_35-PadE3) | U4.E3 (IO_L11P_T1_SRCC_35_E3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L12N_T1_MRCC_35-PadC4) | U4.C4 (IO_L12N_T1_MRCC_35_C4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L12P_T1_MRCC_35-PadD4) | U4.D4 (IO_L12P_T1_MRCC_35_D4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L13N_T2_MRCC_35-PadE5) | U4.E5 (IO_L13N_T2_MRCC_35_E5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L13P_T2_MRCC_35-PadF5) | U4.F5 (IO_L13P_T2_MRCC_35_F5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L14N_T2_SRCC_35-PadF3) | U4.F3 (IO_L14N_T2_SRCC_35_F3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L14P_T2_SRCC_35-PadF4) | U4.F4 (IO_L14P_T2_SRCC_35_F4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L15N_T2_DQS_35-PadE1) | U4.E1 (IO_L15N_T2_DQS_35_E1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L15P_T2_DQS_35-PadF2) | U4.F2 (IO_L15P_T2_DQS_35_F2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L16N_T2_35-PadG4) | U4.G4 (IO_L16N_T2_35_G4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L16P_T2_35-PadG5) | U4.G5 (IO_L16P_T2_35_G5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L17N_T2_35-PadG1) | U4.G1 (IO_L17N_T2_35_G1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L17P_T2_35-PadG2) | U4.G2 (IO_L17P_T2_35_G2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L18N_T2_35-PadH4) | U4.H4 (IO_L18N_T2_35_H4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L18P_T2_35-PadH5) | U4.H5 (IO_L18P_T2_35_H5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L19N_T3_VREF_35-PadJ4) | U4.J4 (IO_L19N_T3_VREF_35_J4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L19P_T3_35-PadJ5) | U4.J5 (IO_L19P_T3_35_J5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L1N_T0_AD4N_35-PadA7) | U4.A7 (IO_L1N_T0_AD4N_35_A7, bidirectional+no_connect) |
| unconnected-(U4B-IO_L1P_T0_AD4P_35-PadB7) | U4.B7 (IO_L1P_T0_AD4P_35_B7, bidirectional+no_connect) |
| unconnected-(U4B-IO_L20N_T3_35-PadH1) | U4.H1 (IO_L20N_T3_35_H1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L20P_T3_35-PadH2) | U4.H2 (IO_L20P_T3_35_H2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L21N_T3_DQS_35-PadH3) | U4.H3 (IO_L21N_T3_DQS_35_H3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L21P_T3_DQS_35-PadJ3) | U4.J3 (IO_L21P_T3_DQS_35_J3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L22N_T3_35-PadJ1) | U4.J1 (IO_L22N_T3_35_J1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L22P_T3_35-PadK1) | U4.K1 (IO_L22P_T3_35_K1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L23N_T3_35-PadL2) | U4.L2 (IO_L23N_T3_35_L2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L23P_T3_35-PadL3) | U4.L3 (IO_L23P_T3_35_L3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L24N_T3_35-PadK2) | U4.K2 (IO_L24N_T3_35_K2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L24P_T3_35-PadK3) | U4.K3 (IO_L24P_T3_35_K3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L2N_T0_AD12N_35-PadB5) | U4.B5 (IO_L2N_T0_AD12N_35_B5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L2P_T0_AD12P_35-PadB6) | U4.B6 (IO_L2P_T0_AD12P_35_B6, bidirectional+no_connect) |
| unconnected-(U4B-IO_L3N_T0_DQS_AD5N_35-PadA4) | U4.A4 (IO_L3N_T0_DQS_AD5N_35_A4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L3P_T0_DQS_AD5P_35-PadA5) | U4.A5 (IO_L3P_T0_DQS_AD5P_35_A5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L4N_T0_35-PadA3) | U4.A3 (IO_L4N_T0_35_A3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L4P_T0_35-PadB4) | U4.B4 (IO_L4P_T0_35_B4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L5N_T0_AD13N_35-PadC6) | U4.C6 (IO_L5N_T0_AD13N_35_C6, bidirectional+no_connect) |
| unconnected-(U4B-IO_L5P_T0_AD13P_35-PadC7) | U4.C7 (IO_L5P_T0_AD13P_35_C7, bidirectional+no_connect) |
| unconnected-(U4B-IO_L6N_T0_VREF_34-PadN4) | U4.N4 (IO_L6N_T0_VREF_34_N4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L6N_T0_VREF_35-PadD5) | U4.D5 (IO_L6N_T0_VREF_35_D5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L6P_T0_34-PadM5) | U4.M5 (IO_L6P_T0_34_M5, bidirectional+no_connect) |
| unconnected-(U4B-IO_L6P_T0_35-PadD6) | U4.D6 (IO_L6P_T0_35_D6, bidirectional+no_connect) |
| unconnected-(U4B-IO_L7N_T1_AD6N_35-PadC2) | U4.C2 (IO_L7N_T1_AD6N_35_C2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L7P_T1_34-PadR2) | U4.R2 (IO_L7P_T1_34_R2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L7P_T1_AD6P_35-PadC3) | U4.C3 (IO_L7P_T1_AD6P_35_C3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L8N_T1_34-PadT2) | U4.T2 (IO_L8N_T1_34_T2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L8N_T1_AD14N_35-PadA2) | U4.A2 (IO_L8N_T1_AD14N_35_A2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L8P_T1_AD14P_35-PadB2) | U4.B2 (IO_L8P_T1_AD14P_35_B2, bidirectional+no_connect) |
| unconnected-(U4B-IO_L9N_T1_DQS_34-PadT3) | U4.T3 (IO_L9N_T1_DQS_34_T3, bidirectional+no_connect) |
| unconnected-(U4B-IO_L9N_T1_DQS_AD7N_35-PadB1) | U4.B1 (IO_L9N_T1_DQS_AD7N_35_B1, bidirectional+no_connect) |
| unconnected-(U4B-IO_L9P_T1_DQS_34-PadT4) | U4.T4 (IO_L9P_T1_DQS_34_T4, bidirectional+no_connect) |
| unconnected-(U4B-IO_L9P_T1_DQS_AD7P_35-PadC1) | U4.C1 (IO_L9P_T1_DQS_AD7P_35_C1, bidirectional+no_connect) |
| unconnected-(U4C-DXN_0-PadK7) | U4.K7 (DXN_0_K7, bidirectional+no_connect) |
| unconnected-(U4C-DXP_0-PadK8) | U4.K8 (DXP_0_K8, bidirectional+no_connect) |

*QSPI / USB-UART*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /fpga/FT_DM | C174.1 (—, passive), R161.2 (—, passive), U142.9 (USBDM_9, bidirectional) |
| /fpga/FT_DP | C173.1 (—, passive), R160.2 (—, passive), U142.8 (USBDP_8, bidirectional) |
| /fpga/QSPI_CS | R140.2 (—, passive), U141.1 (~{CS}_1, input), U4.L12 (IO_L6P_T0_FCS_B_14_L12, bidirectional) |
| /fpga/QSPI_D0 | U141.5 (IO0/DI_5, bidirectional) ↔ U4.J13 (IO_L1P_T0_D00_MOSI_14_J13, bidirectional) |
| /fpga/QSPI_D1 | U141.2 (IO1/DO_2, bidirectional) ↔ U4.J14 (IO_L1N_T0_D01_DIN_14_J14, bidirectional) |
| /fpga/QSPI_D2 | R148.2 (—, passive), U141.3 (IO2/~{WP}_3, bidirectional), U4.K15 (IO_L2P_T0_D02_14_K15, bidirectional) |
| /fpga/QSPI_D3 | R149.2 (—, passive), U141.7 (IO3_7, bidirectional), U4.K16 (IO_L2N_T0_D03_14_K16, bidirectional) |
| /fpga/VBUS_SENSE | R158.2 (—, passive), R159.1 (—, passive), U142.7 (CBUS2_7, bidirectional) |
| HOST_RX | U142.17 (TXD_17, output) ↔ U4.P1 (IO_L4N_T0_34_P1, bidirectional) |
| HOST_TX | U142.1 (RXD_1, input) ↔ U4.N1 (IO_L4P_T0_34_N1, bidirectional) |

*XADC straps*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /fpga/XADC_VN | R152.1 (—, passive) ↔ U4.J7 (VN_0_J7, bidirectional) |
| /fpga/XADC_VNREF | R150.1 (—, passive) ↔ U4.H7 (VREFN_0_H7, bidirectional) |
| /fpga/XADC_VP | R151.1 (—, passive) ↔ U4.H8 (VP_0_H8, bidirectional) |
| /fpga/XADC_VPREF | R153.1 (—, passive) ↔ U4.J8 (VREFP_0_J8, bidirectional) |

**No-connects**

| Pin (no-connect) | Pin name | Pin type | Reason |
|---|---|---|---|
| J140.1 | NC_1 | no_connect | Unused JTAG header pins; no reason stated in schematic |
| J140.12 | NC_12 | no_connect | Unused JTAG header pins; no reason stated in schematic |
| J140.13 | PGND_13 | passive+no_connect | Unused JTAG header pins; no reason stated in schematic |
| J140.14 | HALT_14 | passive+no_connect | Unused JTAG header pins; no reason stated in schematic |
| U142.14 | CBUS1_14 | bidirectional+no_connect | Unused FT231X modem/CBUS pins; no reason stated in schematic |
| U142.15 | CBUS0_15 | bidirectional+no_connect | Unused FT231X modem/CBUS pins; no reason stated in schematic |
| U142.16 | CBUS3_16 | bidirectional+no_connect | Unused FT231X modem/CBUS pins; no reason stated in schematic |
| U142.18 | ~{DTR}_18 | output+no_connect | Unused FT231X modem/CBUS pins; no reason stated in schematic |
| U142.19 | ~{RTS}_19 | output+no_connect | Unused FT231X modem/CBUS pins; no reason stated in schematic |
| U4.A2 | IO_L8N_T1_AD14N_35_A2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.A3 | IO_L4N_T0_35_A3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.A4 | IO_L3N_T0_DQS_AD5N_35_A4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.A5 | IO_L3P_T0_DQS_AD5P_35_A5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.A7 | IO_L1N_T0_AD4N_35_A7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B1 | IO_L9N_T1_DQS_AD7N_35_B1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B15 | IO_L9P_T1_DQS_AD3P_15_B15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B16 | IO_L10N_T1_AD11N_15_B16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B2 | IO_L8P_T1_AD14P_35_B2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B4 | IO_L4P_T0_35_B4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B5 | IO_L2N_T0_AD12N_35_B5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B6 | IO_L2P_T0_AD12P_35_B6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.B7 | IO_L1P_T0_AD4P_35_B7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C1 | IO_L9P_T1_DQS_AD7P_35_C1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C12 | IO_L11N_T1_SRCC_15_C12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C13 | IO_L12N_T1_MRCC_15_C13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C16 | IO_L10P_T1_AD11P_15_C16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C2 | IO_L7N_T1_AD6N_35_C2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C3 | IO_L7P_T1_AD6P_35_C3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C4 | IO_L12N_T1_MRCC_35_C4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C6 | IO_L5N_T0_AD13N_35_C6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C7 | IO_L5P_T0_AD13P_35_C7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C8 | IO_L1P_T0_AD0P_15_C8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.C9 | IO_L1N_T0_AD0N_15_C9 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D1 | IO_L10N_T1_AD15N_35_D1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D10 | IO_0_15_D10 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D11 | IO_L14N_T2_SRCC_15_D11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D14 | IO_L15P_T2_DQS_15_D14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D15 | IO_L15N_T2_DQS_ADV_B_15_D15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D16 | IO_L17N_T2_A25_15_D16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D3 | IO_L11N_T1_SRCC_35_D3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D4 | IO_L12P_T1_MRCC_35_D4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D5 | IO_L6N_T0_VREF_35_D5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D6 | IO_L6P_T0_35_D6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D8 | IO_L6P_T0_15_D8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.D9 | IO_L6N_T0_VREF_15_D9 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E1 | IO_L15N_T2_DQS_35_E1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E11 | IO_L14P_T2_SRCC_15_E11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E12 | IO_L13P_T2_MRCC_15_E12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E13 | IO_L13N_T2_MRCC_15_E13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E15 | IO_L18N_T2_A23_15_E15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E16 | IO_L17P_T2_A26_15_E16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E2 | IO_L10P_T1_AD15P_35_E2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E3 | IO_L11P_T1_SRCC_35_E3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E5 | IO_L13N_T2_MRCC_35_E5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.E6 | IO_0_35_E6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F12 | IO_L16P_T2_A28_15_F12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F13 | IO_L16N_T2_A27_15_F13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F14 | IO_L21N_T3_DQS_A18_15_F14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F15 | IO_L18P_T2_A24_15_F15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F2 | IO_L15P_T2_DQS_35_F2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F3 | IO_L14N_T2_SRCC_35_F3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F4 | IO_L14P_T2_SRCC_35_F4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.F5 | IO_L13P_T2_MRCC_35_F5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G1 | IO_L17N_T2_35_G1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G11 | IO_25_15_G11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G12 | IO_L19N_T3_A21_VREF_15_G12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G14 | IO_L21P_T3_DQS_15_G14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G15 | IO_L24N_T3_RS0_15_G15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G16 | IO_L22N_T3_A16_15_G16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G2 | IO_L17P_T2_35_G2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G4 | IO_L16N_T2_35_G4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.G5 | IO_L16P_T2_35_G5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H1 | IO_L20N_T3_35_H1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H11 | IO_L19P_T3_A22_15_H11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H12 | IO_L20P_T3_A20_15_H12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H13 | IO_L20N_T3_A19_15_H13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H14 | IO_L24P_T3_RS1_15_H14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H16 | IO_L22P_T3_A17_15_H16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H2 | IO_L20P_T3_35_H2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H3 | IO_L21N_T3_DQS_35_H3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H4 | IO_L18N_T2_35_H4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.H5 | IO_L18P_T2_35_H5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J1 | IO_L22N_T3_35_J1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J15 | IO_L23P_T3_FOE_B_15_J15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J16 | IO_L23N_T3_FWE_B_15_J16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J3 | IO_L21P_T3_DQS_35_J3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J4 | IO_L19N_T3_VREF_35_J4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.J5 | IO_L19P_T3_35_J5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K1 | IO_L22P_T3_35_K1 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K12 | IO_0_14_K12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K13 | IO_L5P_T0_D06_14_K13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K2 | IO_L24N_T3_35_K2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K3 | IO_L24P_T3_35_K3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K5 | IO_25_35_K5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K7 | DXN_0_K7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.K8 | DXP_0_K8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.L13 | IO_L5N_T0_D07_14_L13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.L14 | IO_L4P_T0_D04_14_L14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.L2 | IO_L23N_T3_35_L2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.L3 | IO_L23P_T3_35_L3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.L5 | IO_0_34_L5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M12 | IO_L6N_T0_D08_VREF_14_M12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M14 | IO_L4N_T0_D05_14_M14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M15 | IO_L3N_T0_DQS_EMCCLK_14_M15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M16 | IO_L7P_T1_D09_14_M16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M5 | IO_L6P_T0_34_M5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.M6 | IO_L19P_T3_A10_D26_14_M6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N11 | IO_L13P_T2_MRCC_14_N11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N12 | IO_L13N_T2_MRCC_14_N12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N13 | IO_L11P_T1_SRCC_14_N13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N14 | IO_L12P_T1_MRCC_14_N14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N16 | IO_L7N_T1_D10_14_N16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N4 | IO_L6N_T0_VREF_34_N4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N6 | IO_L19N_T3_A09_D25_VREF_14_N6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.N9 | IO_L18P_T2_A12_D28_14_N9 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P10 | IO_L14P_T2_SRCC_14_P10 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P11 | IO_L14N_T2_SRCC_14_P11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P13 | IO_L11N_T1_SRCC_14_P13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P14 | IO_L12N_T1_MRCC_14_P14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P15 | IO_L8P_T1_D11_14_P15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P16 | IO_L8N_T1_D12_14_P16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P5 | IO_L10P_T1_34_P5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P6 | IO_25_14_P6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P8 | IO_L20P_T3_A08_D24_14_P8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.P9 | IO_L18N_T2_A11_D27_14_P9 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R10 | IO_L17P_T2_A14_D30_14_R10 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R11 | IO_L17N_T2_A13_D29_14_R11 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R12 | IO_L15P_T2_DQS_RDWR_B_14_R12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R13 | IO_L16P_T2_CSI_B_14_R13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R15 | IO_L9P_T1_DQS_14_R15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R16 | IO_L9N_T1_DQS_D13_14_R16 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R2 | IO_L7P_T1_34_R2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R5 | IO_L23P_T3_A03_D19_14_R5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R6 | IO_L24P_T3_A01_D17_14_R6 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R7 | IO_L24N_T3_A00_D16_14_R7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.R8 | IO_L20N_T3_A07_D23_14_R8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T10 | IO_L22N_T3_A04_D20_14_T10 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T12 | IO_L15N_T2_DQS_DOUT_CSO_B_14_T12 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T13 | IO_L16N_T2_A15_D31_14_T13 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T14 | IO_L10P_T1_D14_14_T14 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T15 | IO_L10N_T1_D15_14_T15 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T2 | IO_L8N_T1_34_T2 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T3 | IO_L9N_T1_DQS_34_T3 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T4 | IO_L9P_T1_DQS_34_T4 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T5 | IO_L23N_T3_A02_D18_14_T5 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T7 | IO_L21P_T3_DQS_14_T7 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T8 | IO_L21N_T3_DQS_A06_D22_14_T8 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |
| U4.T9 | IO_L22P_T3_A05_D21_14_T9 | bidirectional+no_connect | Unassigned Artix-7 I/O; no connection assigned in the captured schematic |

## 3.6 Page 6 — connectors

**Purpose.** Board-to-world interfaces: eight FG headers, pen/reference harness blocks, Pico and USB-C connectors, CC ESD and chassis bond.

**Power rails** (global rails shown on every sheet that uses them)

| Rail | Pins on this sheet | Role here |
|---|---|---|
| +15V_FUSED | 0 | not on this sheet |
| +3.3V | 0 | not on this sheet |
| GND | 11 | common return |
| +12VA | 0 | not on this sheet |
| -12VA | 0 | not on this sheet |
| +5VA | 0 | not on this sheet |
| +5V_EXC | 0 | not on this sheet |
| +1V0_FPGA | 0 | not on this sheet |
| +1V8_FPGA | 0 | not on this sheet |
| +1V8 | 0 | not present in netlist |

**Inputs** (crossing nets arriving on this sheet)

| Net | Pins on this sheet | From sheet | Signal |
|---|---|---|---|
| FG0_OUT | J20.1 | driver | Field-generator channel 0 drive: coupling capacitor/TP on driver → J20.1. |
| FG1_OUT | J21.1 | driver | Field-generator channel 1 drive: coupling capacitor/TP on driver → J21.1. |
| FG2_OUT | J22.1 | driver | Field-generator channel 2 drive: coupling capacitor/TP on driver → J22.1. |
| FG3_OUT | J23.1 | driver | Field-generator channel 3 drive: coupling capacitor/TP on driver → J23.1. |
| FG4_OUT | J24.1 | driver | Field-generator channel 4 drive: coupling capacitor/TP on driver → J24.1. |
| FG5_OUT | J25.1 | driver | Field-generator channel 5 drive: coupling capacitor/TP on driver → J25.1. |
| FG6_OUT | J26.1 | driver | Field-generator channel 6 drive: coupling capacitor/TP on driver → J26.1. |
| FG7_OUT | J27.1 | driver | Field-generator channel 7 drive: coupling capacitor/TP on driver → J27.1. |
| PICO_HEARTBEAT | J123.6 | fpga | 100 Hz heartbeat level from FPGA U4.P3 → J123.6. |
| PICO_STOP_N | J123.5 | power | Active-low STOP level: latch AND gate U755.4 → J123.5 (Pico pulls down). |
| PICO_TX | J123.3 | fpga | UART FPGA → Pico (schematic text: FPGA transmits, Pico receives), J123.3. |

**Outputs** (crossing nets leaving this sheet)

| Net | Pins on this sheet | To sheet(s) | Signal |
|---|---|---|---|
| FG0_RETURN | J20.2 | driver | Field-generator channel 0 coil return and 1 Ω sense: J20.2 → driver sense network. |
| FG1_RETURN | J21.2 | driver | Field-generator channel 1 coil return and 1 Ω sense: J21.2 → driver sense network. |
| FG2_RETURN | J22.2 | driver | Field-generator channel 2 coil return and 1 Ω sense: J22.2 → driver sense network. |
| FG3_RETURN | J23.2 | driver | Field-generator channel 3 coil return and 1 Ω sense: J23.2 → driver sense network. |
| FG4_RETURN | J24.2 | driver | Field-generator channel 4 coil return and 1 Ω sense: J24.2 → driver sense network. |
| FG5_RETURN | J25.2 | driver | Field-generator channel 5 coil return and 1 Ω sense: J25.2 → driver sense network. |
| FG6_RETURN | J26.2 | driver | Field-generator channel 6 coil return and 1 Ω sense: J26.2 → driver sense network. |
| FG7_RETURN | J27.2 | driver | Field-generator channel 7 coil return and 1 Ω sense: J27.2 → driver sense network. |
| PEN1_N | J122.2 | receiver | Sensor differential pair at J122 → 100 Ω input resistor → receiver front end. |
| PEN1_P | J122.1 | receiver | Sensor differential pair at J122 → 100 Ω input resistor → receiver front end. |
| PEN2_N | J127.2 | receiver | Sensor differential pair at J127 → 100 Ω input resistor → receiver front end. |
| PEN2_P | J127.1 | receiver | Sensor differential pair at J127 → 100 Ω input resistor → receiver front end. |
| PICO_RX | J123.4 | fpga | UART Pico → FPGA, J123.4 (schematic text). |
| REF_COIL_N | J128.2 | receiver | Sensor differential pair at J128 → 100 Ω input resistor → receiver front end. |
| REF_COIL_P | J128.1 | receiver | Sensor differential pair at J128 → 100 Ω input resistor → receiver front end. |
| USB_DM | D750.2, J124.A7, J124.B7 | fpga | Bidirectional USB 2.0 data: J124 USB-C → ESD → 27 Ω R160/R161 → FT231X; netlist pins are passive/bidirectional. |
| USB_DP | D750.1, J124.A6, J124.B6 | fpga | Bidirectional USB 2.0 data: J124 USB-C → ESD → 27 Ω R160/R161 → FT231X; netlist pins are passive/bidirectional. |
| USB_VBUS | J124.A4, J124.A9, J124.B4, J124.B9 | fpga | USB-C VBUS sense: J124 A4/A9/B4/B9 → R158 → FT231X CBUS2. |

**Internal connections** (nets whose pins are all on this sheet)

*Chassis and harness support*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /connectors/CHASSIS | C191.1 (—, passive), J120.1 (SHIELD_1, passive), J120.SH (SHELL_SH, passive), J124.SH (SHIELD_SH, passive), J125.1 (SHIELD_1, passive), J125.SH (SHELL_SH, passive), R185.1 (—, passive) |

*No-connect stubs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| unconnected-(J123-Pin_1-Pad1) | J123.1 (Pin_1_1, passive+no_connect) |
| unconnected-(J124-SBU1-PadA8) | J124.A8 (SBU1_A8, bidirectional+no_connect) |
| unconnected-(J124-SBU2-PadB8) | J124.B8 (SBU2_B8, bidirectional+no_connect) |

*Panel harness pairs*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /connectors/PEN1_PANEL_N | J120.3 (CONTACT_3_3, passive) ↔ J121.2 (Pin_2_2, passive) |
| /connectors/PEN1_PANEL_P | J120.2 (CONTACT_2_2, passive) ↔ J121.1 (Pin_1_1, passive) |
| /connectors/PEN2_PANEL_N | J125.3 (CONTACT_3_3, passive) ↔ J126.2 (Pin_2_2, passive) |
| /connectors/PEN2_PANEL_P | J125.2 (CONTACT_2_2, passive) ↔ J126.1 (Pin_1_1, passive) |

*USB-C CC / shield*

| Net | Ends (ref.pin (pin name, pin type)) |
|---|---|
| /connectors/USB_CC1 | D751.1 (D+_1, passive), J124.A5 (CC1_A5, bidirectional), R182.1 (—, passive) |
| /connectors/USB_CC2 | D751.2 (D-_2, passive), J124.B5 (CC2_B5, bidirectional), R183.1 (—, passive) |

**No-connects**

| Pin (no-connect) | Pin name | Pin type | Reason |
|---|---|---|---|
| J123.1 | Pin_1_1 | passive+no_connect | BRD-01 does not supply 3V3 to the Pico (connectors sheet text; power_tree_v2 §7 D4) |
| J124.A8 | SBU1_A8 | bidirectional+no_connect | USB-C SBU pins unused; no reason stated in schematic |
| J124.B8 | SBU2_B8 | bidirectional+no_connect | USB-C SBU pins unused; no reason stated in schematic |

## 4. Cross-sheet net register

Every net whose pins land on more than one sheet. Pin counts are the `<node>` count with that component's `<sheetpath>` on the named sheet.

| Net | Sheets (pin count) | Total pins |
|---|---|---|
| +12VA | power (6), driver (26), receiver (16) | 48 |
| +15V_FUSED | power (13), driver (28) | 41 |
| +1V0_FPGA | power (4), fpga (17) | 21 |
| +1V8_FPGA | power (4), fpga (11) | 15 |
| +3.3V | power (20), driver (36), receiver (4), fpga (63) | 123 |
| +5VA | power (4), receiver (26) | 30 |
| +5V_EXC | power (4), driver (27) | 31 |
| -12VA | power (6), driver (26), receiver (12) | 44 |
| /BUCK_SYNC | power (1), fpga (1) | 2 |
| /DRIVER_FAULT_N | power (1), driver (9), fpga (1) | 11 |
| ADC_CS | receiver (1), fpga (2) | 3 |
| ADC_DCLK | receiver (1), fpga (1) | 2 |
| ADC_DOUT0 | receiver (1), fpga (1) | 2 |
| ADC_DOUT1 | receiver (1), fpga (1) | 2 |
| ADC_DOUT2 | receiver (1), fpga (1) | 2 |
| ADC_DOUT3 | receiver (1), fpga (1) | 2 |
| ADC_DRDY_N | receiver (1), fpga (1) | 2 |
| ADC_RESET_N | receiver (1), fpga (2) | 3 |
| ADC_SCLK | receiver (1), fpga (1) | 2 |
| ADC_SDI | receiver (1), fpga (1) | 2 |
| ADC_SDO | receiver (1), fpga (1) | 2 |
| ADC_START_N | receiver (1), fpga (2) | 3 |
| ADC_SYNC_IN | receiver (1), fpga (2) | 3 |
| ADC_SYNC_OUT | receiver (1), fpga (1) | 2 |
| CLOCK_32M768 | receiver (1), fpga (2) | 3 |
| CURRENT_SUM | driver (2), receiver (1) | 3 |
| DAC_CS | driver (2), fpga (2) | 4 |
| DAC_SCLK | driver (2), fpga (1) | 3 |
| DAC_SDI | driver (2), fpga (1) | 3 |
| DAC_SDO | driver (2), fpga (1) | 3 |
| FG0_OUT | driver (2), connectors (1) | 3 |
| FG0_RETURN | driver (3), connectors (1) | 4 |
| FG1_OUT | driver (1), connectors (1) | 2 |
| FG1_RETURN | driver (2), connectors (1) | 3 |
| FG2_OUT | driver (1), connectors (1) | 2 |
| FG2_RETURN | driver (2), connectors (1) | 3 |
| FG3_OUT | driver (1), connectors (1) | 2 |
| FG3_RETURN | driver (2), connectors (1) | 3 |
| FG4_OUT | driver (1), connectors (1) | 2 |
| FG4_RETURN | driver (2), connectors (1) | 3 |
| FG5_OUT | driver (1), connectors (1) | 2 |
| FG5_RETURN | driver (2), connectors (1) | 3 |
| FG6_OUT | driver (1), connectors (1) | 2 |
| FG6_RETURN | driver (2), connectors (1) | 3 |
| FG7_OUT | driver (1), connectors (1) | 2 |
| FG7_RETURN | driver (2), connectors (1) | 3 |
| GND | power (103), driver (170), receiver (79), fpga (80), connectors (11) | 443 |
| PEN1_N | receiver (1), connectors (1) | 2 |
| PEN1_P | receiver (1), connectors (1) | 2 |
| PEN2_N | receiver (1), connectors (1) | 2 |
| PEN2_P | receiver (1), connectors (1) | 2 |
| PICO_HEARTBEAT | fpga (1), connectors (1) | 2 |
| PICO_RX | fpga (1), connectors (1) | 2 |
| PICO_STOP_N | power (2), connectors (1) | 3 |
| PICO_STOP_REQ_N | power (2), fpga (1) | 3 |
| PICO_TX | fpga (1), connectors (1) | 2 |
| REF_COIL_N | receiver (1), connectors (1) | 2 |
| REF_COIL_P | receiver (1), connectors (1) | 2 |
| USB_DM | fpga (1), connectors (3) | 4 |
| USB_DP | fpga (1), connectors (3) | 4 |
| USB_VBUS | fpga (1), connectors (4) | 5 |

## 5. Consistency notes

1. **Latch polarity — document stale.** `docs/phase2/system_schematic.md` §4.5 lines 214, 219–223 and `hardware/brd-01/kicad/README.md` lines 107–108 say `U755` ANDs the FPGA request with `U753.~Q` (pin 3) and that `U753.Q` is an unused/no-connect. The netlist has `<net code="227" name="/power/ARM_Q">` at net.xml line 19303; `<net code="369" name="PICO_STOP_N">` at net.xml line 20440; `<net code="370" name="PICO_STOP_REQ_N">` at net.xml line 20445; `<net code="604" name="unconnected-(U753-~{Q}-Pad3)">` at net.xml line 21162: `U753.5 (Q, output)` drives U755.2 through `/power/ARM_Q`, `U755.4 (output)` drives `PICO_STOP_N`, and `U753.3 (~Q)` is the no-connect. The Pico split in `docs/handoff/brd01_io_handoff.md` §3/§5 matches the netlist; this Q/~Q prose does not.

2. **STOP connector pin 1 — contract not yet updated.** `contract/icd/pico_link.md` §2 line 25 lists the 6-pin Pico connector pin 1 as 3V3. The netlist has `<net code="379" name="unconnected-(J123-Pin_1-Pad1)">` at net.xml line 20487 with `J123.1 (passive+no_connect)`, and the connectors sheet says BRD-01 does not supply 3V3 to the Pico (power_tree_v2 §7 D4). This is an open contract change, not a wiring defect.

3. **`+15V_DRV` / `+5V` / panel K1-K2 — old power tree.** `hardware/brd-01/kicad/power-tree.md` §§2–5 still tabulates `+15V_DRV`, `+5V`, a K2 contact and `ESTOP_ASSERTED` to `U4.R2`; `docs/handoff/brd01_io_handoff.md` §5 line 232 also still lists `+15V_DRV`. None of those nets exists in the netlist. The captured rail is `<net code="9" name="+15V_FUSED">` at net.xml line 18123; `<net code="5" name="+5V_EXC">` at net.xml line 18000: `+15V_FUSED` has 41 pins on power and driver (the field rail is unswitched) and the excitation rail is `+5V_EXC` (31 pins on power and driver). The handoff also says "57 global-label cross-sheet nets"; the netlist has 59 global plus the 2 hierarchical labels (61 total). Its list substitutes `+15V_DRV` for `+15V_FUSED` and omits `+5V_EXC`.

4. **Direction implied by names.** `PICO_STOP_N` reads as a FPGA/Pico-level stop line, but its only driver is the power-sheet latch: `<net code="369" name="PICO_STOP_N">` at net.xml line 20440 shows `U755.4 (output)` → `J123.5`, with no FPGA pin on that net. The FPGA request is the separate `PICO_STOP_REQ_N` (`<net code="370" name="PICO_STOP_REQ_N">` at net.xml line 20445: `U4.P4 (bidirectional)` → `U755.1 (input)`), whose name could be read as a request *from* the Pico; it is driven by the FPGA. Both halves must be checked by the FPGA and arm teams.

5. **Direction not provable from pin types.** All Artix-7 signal balls in the netlist are typed `bidirectional` (for example `U4.P4`, `U4.R3`, `U4.M4`), and all USB-C data pins are typed `bidirectional` or `passive`. The FAULT/SYNC/ADC/DAC/PICO directions in Sections 3 and 4 are therefore taken from the other end's pin type and the handoff text, not from the FPGA pin type. `HOST_TX` / `HOST_RX` are named from the board side: `<net code="319" name="HOST_TX">` at net.xml line 20202; `<net code="318" name="HOST_RX">` at net.xml line 20198 shows `HOST_TX` driven by `U4.N1` into `U142.1 (RXD)` and `HOST_RX` driven by `U142.17 (TXD)` into `U4.P1`.

6. **J123.1 and SBU no-connects.** `<net code="379" name="unconnected-(J123-Pin_1-Pad1)">` at net.xml line 20487; `<net code="380" name="unconnected-(J124-SBU1-PadA8)">` at net.xml line 20490; `<net code="381" name="unconnected-(J124-SBU2-PadB8)">` at net.xml line 20493 confirm the Pico 3V3 and USB-C SBU pins are deliberately open; only the Pico pin has a reason in the schematic text.

Counts: netlist nets 605; single-sheet nets in Section 3 internal tables 544; cross-sheet nets in Section 4 61; 544 + 61 = 605. Netlist nodes 2155; pins in CSV 2155.
