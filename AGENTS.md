# AGENTS.md — EM AccuBot (Team 25, ELEC/COEN 490)

> Authoritative agent handoff. `README.md` is the human pointer; this file is the
> source of truth for agents working in this repo.

## What this is

FPGA-based EM motion controller for precision teleoperation ("EM AccuBot").
A pen-shaped 5-DOF hand controller (x, y, z + pitch/yaw, no roll) drives a
micro-positioning follower at 20:1–1000:1 (default 100:1) with tremor filtering.
Success = operator hits 9/10 × 200 µm targets using the magnified view only.

The Phase 1 report (`docs/phase1/`) and Concordia `Capstone_Manual_2026.pdf`
(local-only; see `docs/reference/MANIFEST.md`) define the specs. This file does
not restate the full spec.

Key numbers (default test: 100:1, filter on, no metal within 150 mm, 18–28 °C):

- Hand error ≤2 mm / ≤1°, pose rate ≥100 Hz, tracking volume 100 mm minimum /
  Phase 2 target 150 mm (200 mm stretch, final by jitter gate), ±45° pitch/yaw
- Tool error ≤25 µm @100:1 (≤100 µm @20:1), repeatability ≤10 µm, workspace
  ≥5 mm cube
- Tremor 6–12 Hz attenuated ≥20 dB, deliberate motion <1 Hz attenuated ≤3 dB
- Latency ≤100 ms (filter on) / ≤20 ms (filter off); stop/tracking-lost halt
  ≤100 ms
- Field at operator ≤27 µT (ICNIRP); controller ≤50 g; one pair ≤1000 CAD

## Read order (agents and humans)

1. `contract/README.md` — the shared contract, current version, change process.
2. `contract/system_contract.md` — SC-01…SC-10, D1–D4.
3. `contract/decisions_log.md` — every locked decision with its source.
4. `contract/icd/pico_link.md` — the FPGA ↔ robot-arm interface.
5. `contract/requirements/manipulator.md` — RQ-M1…M17, what the follower must do.
6. Your team's `AGENTS.md` + `README.md`.
7. `docs/phase2/design_order.md` — the stage gates.

**Never edit `contract/` without a `contract-change` issue + PR.** The contract is
the one shared write surface; team folders are owned by their team.

## Reference model — Jaeger 2018 filament + hand-wound sensor (do not re-derive)

Baseline is an **8-coil planar PCB field generator + a single hand-wound 5-DOF
coil sensor**. Implement the sensor tracker from these extracts first; cite
equation numbers in code comments.

- Full thesis (local-only, 282 pp): `HAJ_Thesis_2018.pdf` (Jaeger, UCC, 2018).
  Obtain it via `docs/reference/MANIFEST.md` REF-01; it is **not** in the repo.
- Agent-ready text extracts (local-only; regenerate with `tools/extract_jaeger.sh`):
  - `docs/extracts/Jaeger2018_filament-sensor-model_Ch3_extract.txt` — Ch.3 model/solver
  - `docs/extracts/Jaeger2018_bespoke-sensor_Ch7_extract.txt` — Ch.7 coil design
- The 27-page PDF crop (`docs/extracts/Jaeger2018_filament-sensor-model_extract.pdf`)
  is local-only; regenerate with `tools/extract_jaeger.sh` from the full thesis.
- Supporting papers (local-only; manifest REF-02/REF-03):
  `AnserEMT-onlineversion.pdf` (Jaeger et al. 2017, 1.14 mm / 0.04°, 8 frequencies
  20.5–27.5 kHz @1 kHz spacing, closed-loop current driver); `Catheter Position
  Tracking System ... ODonoghue et al.pdf` (2014, filament method + driver detail).

Model equations (thesis doc pp. / PDF pp.):

- Filament B-field (Biot-Savart, per straight PCB trace): Eq.(3.17)–(3.18),
  doc p.52–53. `B_coil = Σ B(ri)` over k-1 filaments; parallelizable; Ncoil=8
  minimum for planar.
- Sensor flux/voltage: Eq.(3.19)–(3.25) + Ch.7 Eq.(7.1)–(7.9), doc p.53–55 /
  166–168. Point-sensor approx `Φ=µa·B·A·n̂`, `n̂=[sinθcosφ,sinθsinφ,cosθ]`
  valid only for a small cross-section; large coils need the integrated form
  (7.2). Ferrite core (µr≈2300, 3C90, 12×6 mm) gives ~+10 dB gain but adds
  nonlinearity + Barkhausen noise — Eqs.(7.5)–(7.7).
- Solver cost: Eq.(3.26)–(3.27), doc p.56–57. Minimize
  `F(x,y,z,θ,φ)=Vd−κ·Vm` (Vd measured, Vm model, κ per-coil calibration scalar)
  via Levenberg-Marquardt or trust-region, bounded `lb≤p≤ub`. Python framework
  modules (`daq.py / filter.py / model.py / solver.py` + `pyIGTLink.py`,
  Fig.3.21); MATLAB golden baseline in `software/anser-matlab-ref/` (see its
  README for the port map).
- Coils to replicate: Table 7.1 (Ch.7 extract ~line 173): A–E, e.g. C: 120 turns,
  0.32 mm wire, 12 mm long, 9/12.2 mm ID/OD; D/E ferrite-cored. Calibration =
  7×7 grid fit for κ (Sec.7.2.2); accuracy metric = RMS over 98 points @85.6/152 mm
  heights, Eq.(7.10).

## Upstream Anser snapshot — `vendor/anser-osf` (pristine, do not edit)

Downloaded 2026-10-13 from OSF node `47q8q` (35 files, ~43 MB; see
`vendor/anser-osf/PROVENANCE.md`). **`vendor/` is local-only and gitignored**;
the tracked provenance summary is `docs/reference/anser-osf-provenance.md`.
Incorporated as:

- `software/anser-matlab-ref/` — unpacked `P&O Code/Matlab/MatlabCode.zip`
  (MATLAB golden model) + port map in its README. Upstream next rev:
  `https://github.com/BioDesignUCC/AnserEMT` (from `Latest Code.txt`, unverified).
- `hardware/fg-01/` — pointer to `Design Files/Field Generator Board/` +
  `Emitter Coil/CAD/Gerbers/Transmitter Coil PCB Gerber.zip` (8-coil PCB).
- `hardware/brd-01/driver/` — pointer to `Design Files/AC Current Driver/`
  (Rev_A sch/pcb, Gerbers, LM7171 et al. datasheets).
- `hardware/brd-01/frontend/` — pointer to `Design Files/Sensor Amplifier/`
  (Eagle E301).
- `docs/reference/` — pointer to `System Manual/Manual.pdf` (23 pp, 2017).

Rule: never edit `vendor/`; regen `software/anser-matlab-ref/` via unzip (command
in its README).

## Architecture decisions (overrides Phase 1 where noted)

- **Full-FPGA pose (2026-10-12, overrides Phase 1 §1):** DDS excitation + ADC
  sync + demodulation + LM/TRF pose solver all in HDL/HLS on the FPGA. No
  PC-side pose solver; no MATLAB-in-loop. The Phase 1 report says "pose on PC"
  — stale; follow this file.
- **Electronics = one board (BRD-01, 2026-10-28):** power entry/E-stop/DC-DC,
  FPGA + clock, DAC80508 + 8× LTC1563-2 + 8 current loops + current sense,
  receiver (INA163 + ADA4940-2 + AD7768-4), and the FG/pen connectors are zones
  of one 4-layer board. FG-01 stays a separate passive coil PCB; the pen stays
  passive.
- **FPGA = PS-less Artix-7 on BRD-01 (option D, 2026-10-28):**
  XC7A35T-1FTG256C baseline, XC7A50T-1FTG256C same-footprint upgrade; QSPI
  config, USB-UART host link, no DDR3/Linux. Part checks before layout: HR
  (3.3 V) banks, 35T→50T pin compatibility, HLS fit. See
  `docs/phase2/fpga_integration_options.md`;
  `docs/phase2/system_schematic.md` §6.0.
- **Excitation selected 2026-10-27 (M16):** 1× DAC80508 (16-bit, 8 ch,
  200 kSPS) + 8× LTC1563-2 (4th-order Butterworth, 60 kHz); DAC update
  199.805 kSPS (32.768 MHz ÷164), SPI 49.152 MHz, 8×24-bit (192 bits); 8 tones
  20–34 kHz. See `contract/decisions_log.md` #19,
  `simulations/m16/FINAL_REPORT.md`, `docs/handoff/m16-fpga-handoff.md`,
  `docs/handoff/m16-section-diagram.png`.
- **Follower = separate repo:** the Pico 2 firmware, motor config and arm
  mechanics live in the robot-arm repo, not here. This repo owns the ICD
  (`contract/icd/pico_link.md`), the requirements
  (`contract/requirements/manipulator.md`) and the integration stub
  (`robot-arm/`). See `robot-arm/README.md`.

## Repo layout (team-first, 2026-10-29)

```
contract/                  <- canonical contract: SC, decisions, ICDs, requirements
fpga/                      <- HDL/HLS: DDS, ADC sync, demod, LM/TRF solver
hardware/                  <- BRD-01, FG-01, pen, mechanical, BOMs
robot-arm/                 <- integration stub for the separate arm repo
software/                  <- host tools: logging, calibration, viz (no pose solve)
simulations/               <- field/solver/filter sims; .raw outputs are gitignored
docs/
  phase1/                  <- Phase 1 report (local-only; student IDs; not in repo)
  phase2/                  <- design record: design_order, tone_plan, schematics
  handoff/                 <- M16 + solver handoffs and diagrams
  reference/               <- manifest.yml + generated MANIFEST.md (no big PDFs)
  meetings/                <- weekly interface sync notes
  setup/                   <- git workflow, desktop link
tools/                     <- checkers, manifest generator, extract script
.github/                   <- issue/PR templates + CI workflows
```

Local-only, gitignored, never committed: `vendor/`, `reference-cache/`, the root
PDFs, `docs/extracts/*.pdf`, `docs/ad7768-ad7768-4.pdf`,
`docs/Materials procurement.pdf`, and `simulations/**/*.raw`. Every excluded file
has an acquisition entry in `docs/reference/MANIFEST.md`.

## Checks (run before pushing)

```bash
python3 tools/check_doc_paths.py      # every internal path resolves
python3 tools/check_references.py     # every external file has a manifest row
python3 tools/contract_ci.py check    # contract IDs, status tags, version
```

CI runs the same checks plus `contract-guard`, `contract-release`,
`large-file-guard`, `docs`, `python` and (once RTL exists) `hdl`.

## Gotchas for agents

- 5-DOF single coil cannot sense roll about its own axis — do not try to
  estimate it; 6-DOF needs 2 orthogonal coils (Fig.7.1).
- Dipole model is invalid close to large/planar coils — use the filament model
  (3.17), not (3.15).
- Closed-loop coil-current driver is load-bearing (O'Donoghue 2014 §II + thesis
  §4.3.3): temperature/inductance drift breaks κ calibration; verify
  constant-current first.
- Metal within 150 mm invalidates all accuracy claims; ferrite-core gain ≠ free
  accuracy (linearity/noise tradeoff). ICNIRP field cap constrains FG drive.
- The arm repo is separate. Do not duplicate Pico firmware here; use
  `robot-arm/` for integration tests and the pinned contract.
- Never commit a third-party PDF, datasheet, vendor file or `.raw` output. Add a
  `docs/reference/manifest.yml` entry instead.
- Still NOT fetched (needs manual check): `https://openemt.org` Python framework
  (`daq.py/filter.py/model.py/solver.py`, `python-anser`/`qt-anser`/`Matlab-Anser`
  repos), the CORA thesis page (local copy used instead), and the
  `BioDesignUCC/AnserEMT` next-rev pointer from `Latest Code.txt`. The OSF
  `47q8q` snapshot is in `vendor/anser-osf/` (2026-10-13, local-only).

## Team workflow and client setup

- Remote: `git@github.com:poisnoir/Capstone.git` (public).
- Branches: `main` is integration; use short-lived branches named
  `fpga/…`, `hw/…`, `arm/…`, `contract/…`, `docs/…`.
- Contract changes: `contract-change` issue → PR → 2 approvals (interface owner
  + integrator) → bump `contract/VERSION` + `CHANGELOG.md` → tag
  `contract-vX.Y.Z`. The release workflow publishes the zip/json; the arm repo
  pulls it.
- The old SFTP folder sync is replaced by git: clone on each machine and
  push/pull through GitHub. Keep the Tailscale link for remote desktop, not
  file sync. Details: `docs/setup/git-workflow.md`.
- The team's internal desktop/Tailscale notes are kept locally and are not in
  the repo. Public setup docs: `docs/setup/README.md`.
- Private/local-only files are gitignored: the Phase 1 report (student IDs),
  `docs/setup/CLIENT_SETUP.md`, and the thesis `.txt` extracts (copyright).
