# ICD — Power, E-stop and grounding

**Status:** stub, not frozen. **Owner:** Tung. **Canonical sources:**
`contract/decisions_log.md` #7, #10, #11, #20, #25;
`docs/phase2/driver_power_requirements.md`; `docs/phase2/system_schematic.md`.

This stub does not add requirements. Until frozen, the decisions log and the
schematic are authoritative.

## What is already fixed

- One external medical-grade 15 V / 60 W adapter; no on-board mains stage.
- Rails: +15 V, −15 V, +5 V, +3.3 V; isolated ±15 V module; LDOs to ±12 V
  analog; FPGA core from its board regulator.
- One box with an internal shield partition; hardware NC mushroom E-stop in the
  driver enable chain, independent of the FPGA; opto status; software watchdog.
- Programmable current setpoint 150–500 mA; prototype at 150 mA first; 250 mA
  fallback with rail/series-cap/heatsink changes.
- Follower stop ≤100 ms; hardware E-stop is the safety path, not the UART.

## Open

- Exact connector, fuse, TVS and inrush protection.
- Chassis bonding point and single-point ground.
- Shield-can footprint and partitioning on BRD-01.
- Thermal soak and EMI test plan.
- E-stop part choice (Schneider XB4BS8444 or AutomationDirect GCX1131).

## Change control

Any change to the fixed list is a contract change.
