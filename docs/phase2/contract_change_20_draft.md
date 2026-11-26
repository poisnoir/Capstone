# contract-change: decision #20 power parts superseded by power-tree v2

**Status: APPLIED by decision #31 (2026-11-25).** The user adopted the v2 power
tree; `contract/decisions_log.md` #31 is LOCKED, `contract/icd/power.md` and
`docs/phase2/system_schematic.md` §2 carry the adopted rails, and
`contract/VERSION` remains 1.1.0 (additive). The approval checklist below is
retained as the original draft's history, not as pending work; #20's part list
is superseded, while its adapter and one-board intent stand. The as-built board
already implemented these parts (`hardware/brd-01/kicad/brd-01.kicad_sch` at
`ef04f63`; `hardware/brd-01/kicad/bom-to-cad.md:151`;
`docs/phase2/brd01_component_reference.md:357`).
Prepared 2026-11-24; evidence is on branch `main` at `387f90e`.

## What changes and why

Decision #20 locks the power parts as OKI-78SR-5 for +5 V, an RV-1515D for
±15 V, TPS7A4701/TPS7A33 for ±12 V and a TPS7A20 for +3.3 V. The schematic
now implements different parts for the same rails, because the v1 tree could
not meet three requirements: an LDO cannot hold 5.0 V from a 4.8-5.2 V
source; the OKI's 50-75 mV switching ripple sat directly on the DAC and
LTC1563 rails; and U146 dissipated 0.8-1.5 W dropping 15 V to 5 V. The
adapter itself (ME60A1503F01, 15 V / 60 W) is unchanged.

## Rails, before and after

| Rail | v1 source (decision #20) | v2 source (as captured) | Consumers |
|---|---|---|---|
| `+5V` | OKI-78SR-5/1.5 | **deleted** | none - all loads moved |
| `+6V` | - | TPSM63604RDLR, 5.99 V, RT 1.000 MHz, synced 1.024 MHz | U144/U145/U7 inputs, U146/U149 via FL2/FL1 |
| `+5V_EXC` | - | TPS7A4701RGWR from +6V via FL1 | DAC80508, 8x LTC1563-2 |
| `+5VA` | TPS7A4701 from +15V_FUSED | TPS7A4701RGWR from +6V via FL2 | AD7768-4, 2x ADA4940-2 |
| `+3.3V` | TPS7A20 (linear) | TPS62130ARGTR buck (U7) | FPGA I/O, FT231X, AD7768-4 IOVDD, logic |
| `+15V` / `-15V` | RV-1515D | MGJ2D151515SC | U6/U2 inputs only |
| `+12VA` / `-12VA` | TPS7A4701 / TPS7A33 | LT3045EDD-1 / LT3093EMSE | driver op-amps, INA163, ADR434 |

## Decisions carried in

| # | Decision | Needs sign-off |
|---|---|---|
| D1 | 6 V pre-regulator = TPSM63604RDLR at 5.99 V, RT 1.000 MHz, synced to 1.024 MHz; replaces the OKI | power owner |
| D2 | `+5V_EXC` = 5.0 V; DDS tone kept within 0.3-4.6 V (midpoint 2.45 V), not full scale | FPGA team (DDS clamp) |
| D3 | FT231X VCC, ~RESET and 3V3OUT move to `+3.3V` | FPGA team |
| D4 | BRD-01 does not power the Pico; J123 pin 1 is a no-connect | arm repo + ICD |
| D5 | `BUCK_SYNC` on ball R3, 32.768 MHz / 32, through 1 nF to U147 EN/SYNC | FPGA team |

## Evidence

Implemented on `main`: `c485a74`, `fee267d`, `ba98c5a`, `387f90e`.
Reproduce from the repo root:

```bash
kicad-cli sch erc --format json -o /tmp/erc.json hardware/brd-01/kicad/brd-01.kicad_sch
git archive ec88cd1 | tar -x -C /tmp/golden
kicad-cli sch export netlist --format kicadxml -o /tmp/before.xml /tmp/golden/hardware/brd-01/kicad/brd-01.kicad_sch
kicad-cli sch export netlist --format kicadxml -o /tmp/after.xml  hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_netlist_compare.py /tmp/before.xml /tmp/after.xml
```

Current results: ERC 0 errors / 0 warnings; netlist compare reports the
intended rail changes only (`+5V` split into `+5V_EXC` and `+3.3V`,
`FT_3V3` merged into `+3.3V`, `BUCK_SYNC` connected, `U147.15` to GND,
`J123.1` no-connect) with parts 644 -> 645 (the receiver `D_REF`).

## Approval checklist (AGENTS.md)

- [ ] `contract-change` issue filed referencing this draft and decision #20
- [ ] PR against `contract/decisions_log.md` (#20 row) and any `system_contract.md`
      rail wording that still names the v1 parts
- [ ] two approvals: interface owner + integrator
- [ ] `contract/VERSION` bump + `CHANGELOG.md` entry
- [ ] tag `contract-vX.Y.Z`; release workflow publishes the zip/json
- [ ] arm repo pulls the release before its next firmware tag

## Still open after this change

- Relay K1/K2 selection (draft symbols, excluded from BOM and PCB).
- `D_REF` (BAS70H) bench check: cycle power with a tone applied and confirm
  the reference stays within a Schottky drop of `+5VA`. The clamped level is
  AVDD1 + Vf and the AD7768-4 absolute maximum is AVDD1 + 0.3 V, so this
  passes only if Vf <= 0.3 V at the fault current; measure it.
- Bench-only items from power_tree_v2 section 7: C1 sync lock on SW, C5 MGJ2
  45 kHz spur and load margin, C6 FPGA currents against a Power Estimator run.
