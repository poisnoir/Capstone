# ICD — ADC ↔ FPGA capture

**Status:** stub, not frozen. **Owners:** Tung (hardware/ADC), William (FPGA
capture). **Canonical sources:** `contract/system_contract.md` SC-05, SC-05a,
SC-05b, SC-05c, SC-06, SC-07; `docs/phase2/adc_justification.md`;
`docs/phase2/adc_interface_closure.md`; `docs/phase2/system_schematic.md` §6.

This stub exists so the repo has one place per interface. It does not add
requirements. Until it is frozen, the SC rows above are authoritative.

## What is already fixed

- Part: AD7768-4BSTZ-RL7 (build + spare).
- 4 active channels, 4 DOUT lanes, DCLK 8.192 MHz, 32-bit frames, 256 kSPS.
- MCLK ≤32.768 MHz; fast mode, decimation ×32; wideband filter; group delay
  34/ODR = 133 µs.
- DRDY, SYNC/START (no CONVST); SPI configuration only.
- Channel map D3-A: Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference.
- Connector: 2×8/custom header (a 2×6 Pmod is insufficient).
- RC start values: R_IN = 20 Ω, C1 = C2 = 470 pF, C3 = 100 pF (tune at ADC-5).

## Open (must close before calling this ICD frozen)

- Exact pin assignment on the 2×8 header and the FPGA bank.
- Lane-to-channel mapping and frame bit order.
- SYNC/START polarity and the one-time start sequence.
- Precharge-buffer network and reference distribution.
- Test vectors: code density, FFT/SINAD/THD, zero dropped frames over 1 hour.

## Change control

Any change to the fixed list above is a contract change: `contract-change`
issue + PR + `VERSION` bump. Do not change it in a team branch.
