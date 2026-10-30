# fpga/ — FPGA pose engine

Owner: Kevin (DDS/solver) + William (capture/demod) + Amirmohammad
(filter/scaling). Read `../contract/` first; the contract is not negotiable in a
team branch.

## What lives here

| Path | Contents |
|---|---|
| `rtl/` | SystemVerilog/Verilog: DDS, SPI master, ADC capture, Goertzel, solver datapath |
| `hls/` | HLS sources for the LM/TRF solver and any matrix kernels |
| `tb/` | Testbenches and golden-vector tests |
| `constraints/` | XDC pin/timing constraints (once the board is pinned) |
| `scripts/` | Build, lint, simulation and bitstream scripts |

## Fixed interfaces (from the contract)

- 8 tones at 20, 22, 24, 26, 28, 30, 32, 34 kHz; integer-J frames
  (`contract/system_contract.md` SC-03).
- ADC: AD7768-4, 4 channels, 4 DOUT lanes, DCLK 8.192 MHz, 32-bit frames,
  256 kSPS (`SC-05`).
- DAC: DAC80508, SPI 49.152 MHz, 216-bit frame, software TRIGGER
  (`contract/decisions_log.md` #19).
- Clock: one TCXO → PLL → clk_dds + MCLK_adc; single sync reset (`SC-07`).
- Pose output: x, y, z, θ, φ + validity/status + age; ≥100 Hz
  (`contract/icd/pico_link.md`).
- Budget: 2.000 ms acquisition + 0.133 ms ADC delay + 0.5 ms demod + 5.0 ms
  solve + 1.0 ms overhead = 8.633 ms (`SC-08`).

## Current status

No RTL committed yet. The MATLAB golden model is in
`../software/anser-matlab-ref/`; the port map is in its README. Start with the
filament kernel (Eq.3.17–3.18), then the cost function (Eq.3.26–3.27), then the
bounded solver.

## Rules

- Cite the thesis equation numbers in code comments (AGENTS.md).
- No PC-side pose solver; no MATLAB-in-loop.
- Do not change a pin, clock, frame length or tone without a contract change.
- Keep generated build output out of git (`build/`, `*.bit`, `*.dcp`, `*.jou`).
