# ICD — Power, rails and grounding

**Status:** stub, not frozen. **Owner:** Tung. **Canonical sources:**
`contract/decisions_log.md` #7, #10, #11, #20, #25, #30, #31;
`docs/phase2/power_tree_v2.md`; `docs/phase2/system_schematic.md` §2.
The STOP scope follows #30; the rail list follows **decision #31, power tree v2
adopted 2026-11-25** (#20's part list is superseded; its adapter and one-board
intent stand).

This stub does not add requirements. Until frozen, the decisions log and the
schematic are authoritative.

## What is already fixed

- One external medical-grade 15 V / 60 W adapter (ME60A1503F01); no on-board
  mains stage.

| Rail | Source | Load | Notes |
|---|---|---|---|
| `+15V_FUSED` | ME60A1503F01 via F1/TVS/L1 | 8× LMH6321 driver rail, U147, U5 | unswitched; no E-stop contact in the field path (#30) |
| `+6V` | U147 TPSM63604, 6.0 V at 1.024 MHz synced to `BUCK_SYNC` | U144/U145/U7, U149/U146 via FL1/FL2 | `PG_6V` starts the downstream sequence |
| `+1V0_FPGA` | U144 TPS62130A | FPGA VCCINT/VCCBRAM | EN ← `PG_6V` |
| `+1V8_FPGA` | U145 TPS62130A | FPGA VCCAUX | EN ← `PG_1V0` |
| `+3.3V` | U7 TPS62130A | FPGA VCCO, AD7768 IOVDD, FT231X, logic | EN ← `PG_1V8` |
| `+5V_EXC` | U149 TPS7A4701 | DAC80508, 8× LTC1563-2 | excitation rail |
| `+5VA` | U146 TPS7A4701 | AD7768-4, 2× ADA4940-2 | receiver rail; `D_REF` clamps ADC_REF |
| `±12VA` | U5 MGJ2D151515SC → U6 LT3045-1 / U2 LT3093 | INA163, OPA192, ADR434 buffer | isolated analog |

- Removed by #31: OKI-78SR-5 (`+5V`), RV-1515D and TPS7A20 / TPS7A2033. The
  captured BRD-01 schematic and BOM Rev 0.06 already implement these rails;
  #31 closes the former contract-vs-board part conflict.
- One box with an internal shield partition. There is **no panel E-stop, K1 or
  K2** on BRD-01; `+15V_FUSED` feeds the eight LMH6321 continuously and a STOP
  never removes the field (#30). Arm STOP is active low `PICO_STOP_N` from the U755
  AND of the FPGA request (`PICO_STOP_REQ_N`, `U4.P4` + `R754` pull-down) and
  the arm latch `U753.5 (Q)` via `/power/ARM_Q`; `U753.3 (~Q)` is NC.
- Power-up/brownout (U751) and `/DRIVER_FAULT_N` (U752) clear the latch and
  assert arm STOP; SW750 arms it. The last hardware-independent stop path is
  gone — accepted explicitly in #30. **Arm motion stops in ≤100 ms while field,
  DDS/DAC and pose continue.** A genuine FPGA/ADC/driver fault still stops the
  DDS (see `icd/dac_fpga.md` §3).
- Programmable current setpoint 150–500 mA; prototype at 150 mA first; 250 mA
  fallback with rail/series-cap/heatsink changes.

## Open

- Exact connector, fuse, TVS and inrush protection part numbers.
- Chassis bonding point and single-point ground.
- Shield-can footprint and partitioning on BRD-01.
- Thermal soak and EMI test plan; TPSM63604 1.024 MHz sync lock on the bench;
  MGJ2 45 kHz spur and load margin; FPGA current vs Power Estimator.
- `TRIP_REF` divider (R710/R711 ≈ 0.53 V) vs the two driver-sheet trip notes
  (~253 mA, ~280 mA): measure before changing any resistor (power_tree_v2 §7).
- `D_REF` forward drop at the fault current: clamp is compliant only while
  Vf ≤ 0.3 V (power_tree_v2 §7 C7).

## Change control

Any change to the fixed rail list is a contract change: `contract-change` issue →
PR → two approvals → VERSION + CHANGELOG → tag.
