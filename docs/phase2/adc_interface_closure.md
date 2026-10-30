# Phase 2 — ADC-5 interface closure (desk)

**Status:** desk closure 2026-10-27. Hardware verification is pending the FE-4
board. The ADC part/contract was already locked; this file closes the interface
items that do not need the board.

**Part:** AD7768-4BSTZ-RL7 (qty 2: build + spare), ADR434BRZ 4.096 V reference.
Datasheet: `docs/ad7768-ad7768-4.pdf` (real Rev.D; the old 5.8 KB HTML stub was
replaced).

| Item | Closure |
|---|---|
| Input range | Differential ±VREF = ±4.096 V; VCM output; precharge buffer on |
| Input network | External RC/charge reservoirs per AD7768 Figure 87/AN-1384; exact values at schematic. The 73 pF coil budget is cable + connector + **preamp input**, not the ADC switched-cap network |
| Reference | ADR434 4.096 V; absolute ref range 1 V–AVDD1; decoupling/buffer per datasheet |
| Clock | MCLK ≤32.768 MHz; fast mode ×32; ODR 256 kSPS; wideband filter; group delay 34/ODR = 133 µs; jitter target 30 ps for 104 dB (1 ns = 73.4 dB) |
| Control | SYNC_IN/START/SYNC_OUT/DRDY; no CONVST; one-time START/SYNC; discard first 68 samples (266 µs); count DRDY |
| Data | DCLK/DOUT lanes, not SPI; SPI configuration only; 3 active ch × 32-bit × 256 kSPS = 24.576 Mbit/s; 4 lanes → 6.144 MHz; 2 lanes → 12.288 MHz |
| Pin budget | 4 DOUT + DCLK + DRDY + SYNC/START + MCLK + RESET = 10, plus SPI config; 2×6 Pmod (8 I/O) insufficient; use 2×8/custom header |
| Power | +5 V AVDD1/AVDD2; +3.3 V IOVDD; C1 medical-grade PSU; FPGA core via its board regulator |
| BOM | U1 AD7768-4BSTZ-RL7 qty 2; U2 ADR434BRZ qty 1; verify RL7/RL qty-1 price, ADI lifecycle, exact supplier P/N |
| Tests | Code density; FFT/SINAD/THD; CMRR; reference noise; lane capture; 1-hour zero dropped frames |

**Open (schematic/BOM):** exact AD7768 RC/charge-reservoir values from AN-1384;
2×8 header pinout; FPGA pin budget; BOM order/lifecycle; ADC input network
settling with the FE-4 differential driver.

**Next:** DIG-6 (DDS/capture/demod/timing) desk design; ADC-5 hardware test
after the FE-4 board.
