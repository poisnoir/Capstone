# BRD-01 — one-board electronics

The 2026-10-28 decision (`contract/decisions_log.md` #25) puts the whole
electronics chain on one 4-layer board. Zones:

| Zone | Contents | Contract |
|---|---|---|
| Power entry / arm STOP | 15 V adapter input, fuse/TVS, arm STOP latch (no relay), DC-DC, LDOs | #7, #10, #31 (supersedes #20 part list), #25 |
| FPGA + clock | XC7A35T-1FTG256C, QSPI, 32.768 MHz XO, USB-UART | #21, #26, SC-07 |
| Excitation | DAC80508, 8× LTC1563-2, 8 current loops, current sense | #19, SC-03 |
| Receiver | INA163 + ADA4940-2 + AD7768-4, reference, RC input network | #5, #17, SC-05 |
| Connectors | FG-01, pen, Pico link (J123.1 no-connect), host | SC-05b, `contract/icd/pico_link.md` |

Subfolders:

- [KiCad project and BOM-to-CAD mapping](kicad/README.md) — five populated draft sheets, release holds and verified library mappings.
- `driver/` — vendor AC current-driver reference (Rev_A) + new driver work.
- `frontend/` — vendor sensor-amplifier reference (Eagle E301) + new receiver.

Design record: `docs/phase2/system_schematic.md` (zones, pin assignment),
`docs/phase2/driver_power_requirements.md`,
`docs/phase2/frontend_requirements.md`,
`docs/phase2/adc_interface_closure.md`.

Open before layout: the BOM-to-CAD release checks, 35T→50T pin compatibility,
HR-bank coverage, shield-can footprint, connector placement and thermal path.
There is no E-stop relay to select (K1/K2 were removed; arm STOP is a latch). Schematic rev 0.1 is fully captured with zero ERC
violations; it is not frozen until the decisions-log part checks are closed.
