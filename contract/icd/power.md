# ICD — Power, rails and grounding

**Status:** stub, not frozen. **Owner:** Tung. **Canonical sources:**
`contract/decisions_log.md` #7, #10, #11, #20, #25, #30;
`docs/phase2/driver_power_requirements.md`; `docs/phase2/system_schematic.md` §2.
The STOP scope below follows #30; the rail list follows **locked #20** (see the
conflict note at the end).

This stub does not add requirements. Until frozen, the decisions log and the
schematic are authoritative.

## What is already fixed

- One external medical-grade 15 V / 60 W adapter (ME60A1503F01); no on-board
  mains stage.
- Rails per locked #20: +15 V, −15 V, +5 V, +3.3 V; isolated ±15 V module
  (RV-1515D); OKI-78SR-5/1.5 +5 V; TPS7A4701/TPS7A33 LDOs to ±12 V analog;
  TPS7A20 +3.3 V; FPGA core from its board regulator.
- One box with an internal shield partition. There is **no panel E-stop, K1 or
  K2** on BRD-01; the driver rail `+15V_FUSED` is unswitched and a STOP never
  removes the field (#30). Arm STOP is active low `PICO_STOP_N` from the U755
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

- **Power tree conflict (needs a user decision):** #20 above is **LOCKED**, but
  `docs/phase2/power_tree_v2.md:3` is **PROPOSED (2026-11-24)** and
  `docs/phase2/contract_change_20_draft.md:3` is **DRAFT, not filed**. The
  committed board implements the v2 topology (`MGJ2D151515SC` present;
  `OKI-78SR`, `RV-1515`, `TPS7A20` and `TPS7A4701` strings absent; `+5V`
  deleted, rails per `power_tree_v2.md` §9): see
  `hardware/brd-01/kicad/brd-01.kicad_sch` at `ef04f63`,
  `hardware/brd-01/kicad/bom-to-cad.md:151`,
  `docs/phase2/brd01_component_reference.md:357` and
  `docs/phase2/brd01_wiring_manifest.md` §5. No rail in this ICD is changed to
  v2 until the draft contract change lands; decide whether to ratify v2 or
  reconcile the board to #20.
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
