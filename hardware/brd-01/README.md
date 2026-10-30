# BRD-01 — one-board electronics

The 2026-10-28 decision (`contract/decisions_log.md` #25) puts the whole
electronics chain on one 4-layer board. Zones:

| Zone | Contents | Contract |
|---|---|---|
| Power entry / E-stop | 15 V adapter input, fuse/TVS, NC mushroom E-stop, DC-DC, LDOs | #7, #10, #20 |
| FPGA + clock | XC7A35T-1FTG256C, QSPI, 32.768 MHz TCXO, USB-UART | #26, SC-07 |
| Excitation | DAC80508, 8× LTC1563-2, 8 current loops, current sense | #19, SC-03 |
| Receiver | INA163 + ADA4940-2 + AD7768-4, reference, RC input network | #5, #17, SC-05 |
| Connectors | FG-01, pen, Pico link, E-stop, host | SC-05b, `contract/icd/pico_link.md` |

Subfolders:

- `driver/` — vendor AC current-driver reference (Rev_A) + new driver work.
- `frontend/` — vendor sensor-amplifier reference (Eagle E301) + new receiver.

Design record: `docs/phase2/system_schematic.md` (zones, pin assignment),
`docs/phase2/driver_power_requirements.md`,
`docs/phase2/frontend_requirements.md`,
`docs/phase2/adc_interface_closure.md`.

Open before layout: KiCad project, 35T→50T pin compatibility, HR-bank coverage,
shield-can footprint, connector placement, thermal path. The schematic is not
frozen until the part checks in the decisions log are closed.
