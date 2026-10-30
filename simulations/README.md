# simulations/ — field, solver and SPICE

| Path | What |
|---|---|
| `field_jacobian.py` | 8-coil field/Jacobian scan, ICNIRP sum, conditioning, CRLB |
| `m16/` | DAC80508 + LTC1563-2 SPICE study (`.cir`, `.log`, `FINAL_REPORT.md`, `figs/`) |

## M16

The `.cir` files are the source; `.raw` / `.op.raw` are regenerable LTspice
output and are **gitignored**. To reproduce a run:

```bash
# from simulations/m16/, with LTspice/Wine available
# open the .cir in LTspice and run, or use the project's batch command
```

The evidence that matters is tracked: `FINAL_REPORT.md`, `RESULTS.md`,
`SPICE_PLAN.md`, the `.log` files and `figs/*.png`. Do not commit `.raw`.

## Field scan

```bash
python3 simulations/field_jacobian.py
```

Outputs the 100/150/200 mm cube conditioning and the CRLB table used in
`contract/system_contract.md` §2. If you change the coil geometry or current,
re-run it and update the contract through a `contract-change` issue.
