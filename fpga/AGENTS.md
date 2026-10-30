# fpga/AGENTS.md

Scope: RTL/HLS for the full-FPGA pose engine. Read `../AGENTS.md` and
`../contract/` first.

## Non-negotiables

- The pose is solved on the FPGA. Do not add a PC-side or MCU-side solver.
- The fixed interfaces are in `contract/system_contract.md` SC-03, SC-05,
  SC-07 and `contract/decisions_log.md` #19/#21. A pin, clock, frame length or
  tone change is a contract change.
- Cite equation numbers from Jaeger 2018 in comments: filament Eq.(3.17)–(3.18),
  sensor Eq.(3.19)–(3.25)/(7.1)–(7.9), cost Eq.(3.26)–(3.27).
- The 5-DOF pose is x, y, z, θ, φ. Never estimate roll.

## Working style

- One block per PR: DDS, SPI, capture, Goertzel, solver, filter/scaling.
- Every block gets a testbench and a golden-vector test against the MATLAB
  reference where one exists.
- Keep fixed-point scaling documented next to the code; a scaling change is an
  interface change if it crosses a module boundary.
- Do not commit build output (`build/`, `*.bit`, `*.dcp`, `*.jou`, `.Xil/`).

## Verification

- `verilator --lint-only -Wall` must pass once RTL exists (CI runs it).
- Solver: compare against `software/anser-matlab-ref/` on the same inputs;
  report position/orientation error and iteration count.
- Timing: the 8.633 ms pipeline budget is a gate; report worst-case, not average.

## Do not

- Edit `contract/` in a team branch. Open a `contract-change` issue.
- Copy vendor RTL or MATLAB code into `fpga/` without a license check.
- Assume a board part; the FPGA is XC7A35T-1FTG256C baseline, XC7A50T upgrade.
