# Interface control documents (ICDs)

An ICD freezes one interface: the physical layer, the information that crosses,
the rates/limits, the failsafe behaviour, and what is left to the implementers.
Each ICD names an owner on each side.

| ICD | Interface | Status | Owners |
|---|---|---|---|
| `pico_link.md` | BRD-01 (FPGA) ↔ Pico 2 follower | **Rev B, 2026-11-26**; STOP scope clarified 2026-11-25 (#30); pin 1 = NC by #32 | FPGA engineer / follower firmware |
| `adc_fpga.md` | AD7768-4 ↔ FPGA capture | Stub — see SC-05/SC-05a–c, SC-07; on-board nets (#21/#25) | Tung / William |
| `dac_fpga.md` | DAC80508 ↔ FPGA DDS/SPI | **FROZEN Rev A, 2026-11-02**; safe-state clause clarified 2026-11-25 (#30) | Tung / Kevin |
| `power.md` | Power entry, rails, grounding, arm STOP | Stub — see #7/#10/#20/#25/#30/#31; v2 rails adopted by #31 | Tung |
| `mechanical.md` | FG/pen/enclosure/arm mounts, 150 mm rule | Stub — see SC-01c, SC-04b, D2 | Tung / Tristan |

**A stub is not a frozen interface.** Until an ICD is marked frozen, the
`system_contract.md` rows and the decisions log are the contract. Do not build a
new interface against a stub without a written deviation.

The `pico_link/vectors/` folder holds shared conformance vectors once the Pico
side chooses a frame encoding (ICD §5 leaves encoding, field widths and CRC to
the implementers).
