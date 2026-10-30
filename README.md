# EM AccuBot — Team 25 (ELEC/COEN 490)

FPGA-based electromagnetic motion controller for precision teleoperation.
A pen-shaped 5-DOF hand controller drives a micro-positioning follower at
20:1–1000:1 (default 100:1) with tremor filtering (6–12 Hz → ≥20 dB),
targeting ≤25 µm tool error at 100:1.

**Agents: read `AGENTS.md` first.** It is the authoritative handoff.

## Start here (30 minutes)

1. `contract/README.md` — the shared contract, current version and change process.
2. `contract/system_contract.md` — SC-01…SC-10 and decisions D1–D4.
3. `contract/decisions_log.md` — every locked decision with its source.
4. Your team's `AGENTS.md` + `README.md`.
5. `docs/phase2/design_order.md` — the stage gates (SC-0 → FG-1 → … → INT-7).

If you only read one thing before building: **`contract/system_contract.md`**.
If you are about to change an interface: read `contract/README.md` first.

## Teams and ownership

| Team | People | Owns |
|---|---|---|
| FPGA | Kevin, William (+ Amirmohammad for filter/scaling) | `fpga/` — DDS, ADC capture, demod, LM/TRF solver, filter/scaling |
| Hardware | Tung | `hardware/` — BRD-01, FG-01, pen, mechanical, BOMs |
| Robot arm | Tristan, Joyal | separate arm repo (Pico firmware, motor config, mechanics); `robot-arm/` here is the integration stub |
| Integration / contract | leads + contract owner | `contract/`, `docs/`, `tools/`, cross-team gates |

Ownership is expressed in `CODEOWNERS`; the contract is the one shared write
surface. Team folders are owned by their team.

## Repo map

```
contract/     canonical contract: SC, decisions, ICDs, requirements
fpga/         HDL/HLS: DDS, ADC sync, demod, LM/TRF solver
hardware/     BRD-01, FG-01, pen, mechanical, BOMs
robot-arm/    integration stub + handshake kit for the separate arm repo
software/     host tools: logging, calibration, viz (no pose solve)
simulations/  field/solver/filter sims (.raw outputs are gitignored)
docs/         phase1/, phase2/, handoff/, reference/, meetings/, setup/
tools/        checkers, manifest generator, extract script
.github/      issue/PR templates + CI
```

## The contract is versioned

- Current version: `contract/VERSION` (tag `contract-v1.0.0`).
- On every push to `main` that changes `contract/`, CI publishes
  `contract-vX.Y.Z.zip` + `contract-vX.Y.Z.json` as a GitHub Release, plus a
  rolling `contract-latest`.
- The arm repo pins a version and pulls the release with a read-only token; see
  `robot-arm/README.md`.
- A contract change requires a `contract-change` issue, a PR, two approvals, a
  `VERSION` bump and a `CHANGELOG.md` entry.

## References are not in the repo

Third-party PDFs, datasheets and the vendor snapshot are **not committed**
(copyright and size). Every excluded file has an entry in
`docs/reference/MANIFEST.md` saying what it is, which docs use it, and how to
obtain it. Run `python3 tools/check_references.py` to verify coverage.

## Status

Phase 2 design. Full-FPGA pose locked 2026-10-12; one-board BRD-01 and PS-less
Artix-7 locked 2026-10-28; M16 DAC/filter selected 2026-10-27. See
`contract/decisions_log.md` for the full record.

## Working rules

- `main` is integration; use short-lived branches (`fpga/…`, `hw/…`, `arm/…`,
  `contract/…`, `docs/…`) and open a PR.
- Run `python3 tools/check_doc_paths.py`, `python3 tools/check_references.py`
  and `python3 tools/contract_ci.py check` before pushing.
- Never commit a third-party PDF, datasheet, vendor file or `.raw` output.
- Do not edit `contract/` without a written deviation and a contract PR.

Details: `CONTRIBUTING.md`.
