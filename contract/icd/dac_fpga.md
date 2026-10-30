# ICD — DAC80508 ↔ FPGA DDS/SPI

**Status:** stub, not frozen. **Owners:** Tung (hardware/DAC), Kevin (FPGA DDS).
**Canonical sources:** `contract/decisions_log.md` #19 and #21;
`contract/system_contract.md` SC-03 and SC-07; `docs/phase2/system_schematic.md`;
`simulations/m16/FINAL_REPORT.md`; `docs/handoff/m16-fpga-handoff.md`.

This stub does not add requirements. Until frozen, decision #19 and the SC rows
are authoritative.

## What is already fixed (M16)

- 1× DAC80508 (16-bit, 8 channels, 200 kSPS, SPI, internal 2.5 V reference).
- 8× LTC1563-2, 4th-order Butterworth, 60 kHz, one resistor per channel.
- DAC update 199.805 kSPS = 32.768 MHz ÷ 164.
- SPI 49.152 MHz; 8×24-bit data + 24-bit TRIGGER = 216 bits = 4.394 µs.
- TRIGGER is software (`TRIGGER 0x05` bit 4); the part has no LDAC pin.
- 8 tones at 20, 22, 24, 26, 28, 30, 32, 34 kHz; integer-J frames.
- One TCXO → FPGA PLL → clk_dds + MCLK_adc; single sync reset.

## Open

- Exact 2×20 IDC pinout and FPGA bank assignment.
- SPI mode, word order and CS timing at 49.152 MHz.
- TRIGGER cadence relative to the ADC frame.
- Power-up/down sequence and safe state (all channels zero).
- Bench verification: one-channel constant current, 8-tone EVM, THD/IMD.

## Change control

Any change to the fixed list is a contract change. Do not change it in a team
branch.
