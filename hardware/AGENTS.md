# hardware/AGENTS.md

Scope: BRD-01, FG-01, pen and mechanical. Read `../AGENTS.md` and
`../contract/` first.

## Non-negotiables

- `vendor/` is pristine. Never edit it; it is local-only and gitignored.
- No metal within 150 mm of the tracking volume. The ICNIRP guard is a non-metal
  access barrier, not an EMF shield (SC-04b, D2).
- Closed-loop coil current is load-bearing. Verify constant-current before any
  accuracy claim (O'Donoghue 2014 §II; thesis §4.3.3).
- Do not change a locked part without a contract change: AD7768-4, INA163,
  ADA4940-2, DAC80508, LTC1563-2, the FPGA part, the power tree.
- The pen is passive; the sensor coil/tip is the tracked point.

## EDA and BOM

- KiCad project files are text; commit them. Do not commit `*-backups/`,
  `fp-info-cache`, `*.kicad_prl`, `*.bak` (gitignored).
- BOMs are `.xlsx` (binary). Keep them small; export CSV when a diff matters.
- No BOM row may ship with a placeholder supplier P/N (decisions log,
  procurement checks).
- Gerbers/fab outputs: commit only a released zip under `brd-01/fab/`, not every
  build.

## Verification

- DRC/ERC clean before a fab release.
- 150 mm metal-free check on the assembled setup.
- Field-probe scan at the accessible boundary + guard check (SC-04b).
- Constant-current test, thermal soak, E-stop/overcurrent (DRV-2).

## Do not

- Edit `contract/` in a team branch.
- Copy vendor schematics into a new board without a license check.
- Add a ferrite core to the pen because it gives +10 dB; the air-core decision
  is locked (decisions log #4).
