# Phase 2 — Design (EM AccuBot, Team 25)

> **Contract note:** the canonical contract (SC-01…SC-10, decisions, ICDs,
> manipulator requirements) now lives in `contract/`. This folder is the design
> record that supports it. If this folder and `contract/` disagree, the contract
> wins.

Distillation of what Phase 2 must deliver and design, from authoritative sources only.
No new spec numbers invented here — every number traces to a source below.

Sources (frozen, do not edit):
- `Capstone_Manual_2026.pdf` pp.13–14 — official Phase 2 definition (report + presentation).
- `Phase 1 Report - Team 25 (ELEC-COEN 490).docx` (local-only; see `docs/phase1/README.md`) — team specs (#1–25), success criteria, tasks, schedule, budget.
- `AGENTS.md` (2026-10-12 architecture decision) — **full-FPGA pose overrides Phase 1 §1** ("pose on PC" is stale).
- `docs/phase2/anser-baseline-findings.md` — Anser baseline vs Phase 1 gap analysis (pose rate, jitter, spur budget).
- `software/anser-matlab-ref/README.md` — MATLAB golden-model port map for the FPGA solver.

## 1. Official Phase 2 deliverables (manual p.13)

**Group report, 15–20 pages.** Must contain:
1. Abstract.
2. Review of design specifications (OIQ `{3.2.11, 3.3.14}`) — i.e. revisit Phase 1 Tables 2–4 (#1–25), confirm or revise with justification.
3. Design review of work done to date, with block diagrams, flow charts, graphs, schematics (IEEE 315 / IEC 60617; software may use ANSI/IEEE SRS instead).
4. Alternatives at **component level** (OIQ `{3.1.2}`): list, analyze, state trade-offs explicitly, justify choice **with numbers** (weighted matrix as in Phase 1 Tables 5–6). Manual FAQ Q5: Phase 1 = system level (EM vs stereo vs QR vs IMU vs linkage — done), Phase 2 = component level (coil geometry, driver, ADC/DAC, demod, solver, filter, leadscrew, camera, etc.).
5. Developing the solution selected (OIQ `{3.1.4}`) + design development (`{3.2.4}`).
6. Deviations from Phase 1 task allocation/schedule, discussed and justified + **updated schedule/plan** (final deliverables are evaluated against the *revised* plan).
7. Per-student 1–2 page contribution summary (6 members → 6–12 pages inside the page count; be concise).
8. Appendix A: first ELSEE assignment (see capstone ELSEE Moodle page).
9. Appendix B: "Life-Long Learning" form per student (from Moodle "Forms", one copy each).

Report mechanics (manual pp.6, 12–13): Concordia Form and Style Guide Ch.2–7; sample title page from Appendix 7 for all submissions; submit electronically via Moodle **plus** email copy to supervisor (Dr. Amir Aghdam); 10% of full grade penalty per day late; signed Expectations of Originality (ink, no e-signature).

**Presentation, 40 min per group:** 20 min present + 15 min Q&A + 5 min setup/logoff, over Zoom. Rules:
- Those who did **not** present Phase 1 **must** present Phase 2; every member must still accumulate ≥5 min talk across Phases 1–4.
- Based on the report: main design/implementation results, problems deferred to Phase 3, justification of any scope/spec/schedule changes vs Phase 1.
- A working demo of part of the project is encouraged but not mandatory (good candidates: §5).

## 2. Frozen Phase 1 baseline Phase 2 must design against

Default test conditions (apply to every spec row unless the row says otherwise): indoor lab; 18–28 °C; 30–60 % RH non-condensing; **no conductive/ferromagnetic objects except the system within 150 mm of tracking volume**; controller inside tracking volume; scaling 100:1; tremor filter on; 120 V ±10 %, 60 Hz wall power.

Input specs (#1–7): 1–2 pen controllers; 5-DOF each (x,y,z + pitch/yaw, **no roll** — single coil physics); **100 mm cube minimum; Phase 2 target 150 mm (200 mm stretch), final by jitter gate SC-01d**; ±45° pitch/yaw from rest; hand error ≤2 mm position (typ 1 mm) / ≤1° orientation on reference grid; scaling selectable 20:1–1000:1.

Output specs (#8–18): tool workspace ≥5 mm cube; tool error ≤100 µm @20:1, **≤25 µm @100:1** vs scaled hand motion; repeatability ≤10 µm (10 approaches); tremor attenuation **≥20 dB @6–12 Hz**, deliberate-motion attenuation **≤3 dB below 1 Hz** (tested 0.5 + 1 Hz sine); latency **≤20 ms filter-off / ≤100 ms filter-on**; pose rate **≥100 Hz**; stop (command or tracking-loss) **≤100 ms**; on-screen magnification **≥50×**.

Operator/safety/env (#19–25): pen ≤50 g; field at operator **≤27 µT** anywhere in tracking volume (ICNIRP); supply 108/120/132 V @60 Hz; material cost **≤1000 CAD per controller+follower pair**; operating 18–28 °C; storage −10–40 °C; RH ≤80 % non-condensing.

Measurement of success (all under default conditions): 9/10 × 200 µm targets hit on magnified view only; pen ≤2 mm / ≤1°; ≥100 Hz; ≤25 µm tool + ≤10 µm repeatability @100:1; 20 dB / 3 dB tremor split; ≤100 ms latency filter-on.

Functional (8): track 1–2 pens; scaled follow; tremor reduction; engage/disengage (hand relocates, tool stays); emergency stop; live enlarged view; timestamped pose log; status reporting incl. tracking-lost.
Non-functional (7): micrometre-level precise/repeatable tool; no disruptive delay; no mechanical linkage (thin sensor cable OK); fail-safe halt on tracking/field fault; ICNIRP field; in-budget; ordinary lab + wall outlet.

Committed deliverable = **one** controller-and-follower pair; second pair only after first meets spec. Subsystems: pen(s) with 5-DOF coil in 3D-printed shell (product); coil array + drivers (placement by simulation, ICNIRP-capped); receiver front-end + ADC; FPGA DDS + ADC-sync + demod; 5-DOF estimator + scaling + tremor filter + robot command; PMS XYZ stage (MicroManipulatorStepper + Pico 2 boards, test-bed not product, but team designs/builds/characterizes it); camera+display magnifier. Stretch only: 2nd pair, VR view, on-device outlier rejection.

## 3. Architecture override (design to this, document the deviation)

`AGENTS.md` 2026-10-12: **full-FPGA pose** — DDS excitation + ADC sync + demod + LM/TRF solver all in HDL/HLS. No PC-side solver, no MATLAB-in-loop. Phase 2 report must carry this as an explicit Phase 1 deviation with rationale: Anser baseline only reaches 15 Hz (paper) / 50–72 Hz MATLAB (see `anser-baseline-findings.md` §4–5) — Nyquist 7.5 Hz misses the 6–12 Hz tremor band — so ≥100 Hz needs common-clock DDS+ADC, streaming demod (Goertzel in HDL, matrix form kept as Python golden-check), parallel filament kernel (thesis Eq.3.17–3.18), relaxed TolFun, ping-pong acq/solve, Fs >100 kHz. Cite Eq.(3.17)–(3.27), (7.1)–(7.9) in code comments per AGENTS.md.

## 4. Component-level design work (owner in brackets, from Phase 1 Table 8)

- Field generator coil array + placement simulation [Tung Lam Ha]: 8-coil planar PCB baseline (`hardware/fg-01/` → vendor Gerbers); filament-model sim (`simulations/`, cf. `field_jacobian.py`); Phase 2 tone plan = 20–34 kHz @2 kHz, 8 tones (`docs/phase2/tone_plan.md`); volume target 150 mm (100 mm min / 200 mm stretch, SC-01d); verify ≤27 µT at operator.
- Closed-loop current drivers [Tung]: load-bearing — temperature/inductance drift breaks κ calibration (O'Donoghue 2014 §II, thesis §4.3.3). Constant-current test is a Phase 2 must-pass before any accuracy claim.
- Receiver front-end + ADC interface [Tung]: INA128/INA163-class amp heritage (`hardware/brd-01/frontend/` → vendor Eagle E301); Helmholtz-calibrated Asens(f); AD7768-4 contract = differential ±4.096 V, MCLK/DCLK, SYNC/START/DRDY, simultaneous; SPI is config-only; ns-level jitter OK.
- FPGA DDS + excitation [Kevin Michel Mandiouba]: multichannel DDS, one TCXO → PLL → clk_dds + clk_adc, integer-J frames, single DAQ_phase_offset + per-coil κ absorb group delay.
- FPGA sampling + demod + pose-estimate interface [William White]: Goertzel-per-tone streaming; spur budget ~60–70 dB below tone (recompute with pen N/Ac, Iout when FG changes); port map in `software/anser-matlab-ref/README.md`.
- 5-DOF solver port → HDL/HLS LM/TRF [Kevin + William, with Tristan]: cost F=Vd−κ·Vm (Eq.3.26–3.27), bounded lb≤p≤ub, retry +[0,0,0,π,π]; κ via 7×7 grid fit (Sec.7.2.2), RMS metric Eq.(7.10) over 98 pts @85.6/152 mm; coils Table 7.1 A–E (e.g. C: 120T/0.32 mm/12 mm/9/12.2 mm ID/OD; D/E ferrite 3C90 µr≈2300, +10 dB but Barkhausen — Eqs.7.5–7.7).
- Tremor filter + motion scaling + schedule tracking [Amirmohammad Gharibipour]: Kalman from Oct→Mar; 20 dB / 3 dB split; scaling 20:1–1000:1 (default 100:1); tool_error = hand_error/S.
- PMS mechanics/fabrication/assembly/characterization [Tristan Ovesson]: MicroManipulatorStepper XYZ; resolution test (~10 µm/full-step @2 mm lead baseline; backlash/microstep error budget vs 10 µm repeatability).
- PMS firmware/motor/host-comm/tracker integration [Joyal Biju Kulangara]: homing/limits (Nov–Jan), host commands, engage/disengage + stop watchdog (≤100 ms), status states (tracking / out-of-volume / stopped / fault).
- Magnified view + logging + failsafes [shared]: ≥50× camera/display; timestamped ≥100 Hz pose log; volume-excursion halt+alarm; excess-tremor halt; field-instability halt; comm-loss watchdog.

**Design order and stage gates:** `docs/phase2/design_order.md` — SC-0 system contract → FG-1 field/ICNIRP/current → {DRV-2 driver/power, PEN-3 pen coil} → FE-4 front end → ADC-5 interface → DIG-6 digital/demod → INT-7 integration/calibration. Do not start a stage before its upstream gate is frozen. FPGA core: `docs/phase2/fpga_justification_and_requirements.md`; compute case: `docs/phase2/fpga_vs_mcu_compute_budget.md`.

**M16 selected (2026-10-27):** 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8× LTC1563-2 (4th-order, 60 kHz); DAC update 199.805 kSPS, SPI 49.152 MHz. Verification: `simulations/m16/FINAL_REPORT.md`; FPGA handoff: `docs/handoff/m16-fpga-handoff.md`; block diagram: `docs/handoff/m16-section-diagram.png`; decision: `contract/decisions_log.md` #19.

Phase 1 test plan items that become Phase 2 design-verification hooks: XYZ tracking test; pitch/yaw test (beat paper's angle test); tremor sim/test; constant-current test; robot resolution test. Rule from manual: **every spec number needs a test-case idea** — §6 table enforces this.

## 5. Suggested partial demo (encouraged, not mandatory)

Any subset proving the chain, e.g.: single-coil field sense on scope/FFT (SFDR check); DDS+ADC common-clock sync; Goertzel tone decode vs MATLAB golden; static 5-DOF solve on prerecorded frame; tremor-filter sim (6–12 Hz in, attenuated out); single-axis PMS move from scaled synthetic pose. All non-metal fixtures; log conditions.

## 6. Traceability (spec → Phase 2 section → verification idea)

| # | Spec | Design section | Test idea |
|---|---|---|---|
| 1–2 | 1–2 pens, 5-DOF (no roll) | Pen coil + solver DOF | Two-pen arbitration; show roll unobservable by construction |
| 3–4 | 100 mm min / 150 mm target, ±45° | FG placement sim | Reference-grid sweep, known steps |
| 5–6 | ≤2 mm / ≤1° hand | FG + driver + front-end + solver + κ cal | 7×7 grid @2 heights, RMS Eq.(7.10); NDI-610099-style jitter run |
| 7 | 20:1–1000:1 scaling | Scaling block | Command-vs-motion ratio check at 20:1/100:1/1000:1 |
| 8 | ≥5 mm workspace | PMS mechanics | Micrometer travel measurement |
| 9–10 | ≤100/≤25 µm tool | Error budget hand/S + stage | Scaled-hand follow error @20:1 and 100:1 |
| 11 | ≤10 µm repeat | Stage + filter steady-state | 10 approaches, spread |
| 12–13 | 20 dB / 3 dB | Kalman/tremor filter | Sine sweep 6–12 Hz + 0.5/1 Hz, dB in/out |
| 14–15 | ≤20/≤100 ms latency | Pipeline TL+Tsolv budget | Hand-onset → tool-onset timing, filter on/off |
| 16 | ≥100 Hz pose | Full-FPGA pipeline | Timed pose loop, moving-sensor case |
| 17 | ≤100 ms stop | Watchdog + engage/stop | Stop cmd / tracking-loss → halt timing |
| 18 | ≥50× view | Camera/display | Stage-micrometer on-screen calibration |
| 19–20 | ≤50 g, ≤27 µT | Pen mech + FG drive | Scale; AC field probe in volume |
| 21–25 | Power/cost/env | PSU + BOM + lab procedure | Outlet tolerance, BOM ≤1000 CAD/pair, temp/RH log |

## 7. Schedule + budget update (what Phase 2 must revise)

Phase 1 Gantt (Sept 2026–Apr 2027, appendix): Sept–Oct research/architecture; Oct–Nov component select + procure; Oct–Jan FPGA + Kalman start; Nov–Jan firmware/host; Dec assembly; Jan–Feb integration; **Feb 15 pre-demo teleop prototype**; latency/EMC/full-system tests; in-lab demo week of Mar 22; Apr 2 report. Second controller + VR only after core validates. Phase 2 report must show the revised Gantt, what slipped, and corrective action.

Budget: ~C$962 materials per controller+PMS pair (~4 % of commercial equivalent C$25.5k); + camera/test C$75 + 15 % contingency → **C$1,193**; funded by C$500 department + team remainder. FPGA board already owned (Phase 1 basis; Phase 2 puts the FPGA on BRD-01, decision #26). FX: 1 USD=1.425 / 1 EUR=1.604 CAD (Oct 2026). Phase 2 replaces top-down analogy with selected-part costs; procurement via Design approval + Components Request Procedure (manual pp.22–25).

## 8. Report scaffold (proposal — adjust to Form and Style)

1. Abstract · 2. Spec review (tables #1–25, changes justified) · 3. System design review (block diagram Fig.1-class + per-subsystem) · 4. Component alternatives + weighted matrices + trade-offs · 5. Detailed design per §4 (equations, sims, schematics, HDL partitions, filter, firmware states) · 6. Verification results to date (§6 hooks) · 7. Deviations + updated Gantt/budget · 8. Phase 3 plan (integration → Feb 15 prototype → Mar 22 demo) · 9. Per-student contributions (1–2 pp each) · App. A ELSEE · App. B Life-Long Learning ×6 · Refs (OIQ GPP, IEEE 315/IEC 60617, Jaeger 2018 eqs., O'Donoghue 2014, ICNIRP).

## 9. Definition of done for this folder

- [ ] Component alternatives with numeric matrices filed per subsystem.
- [ ] Every spec #1–25 has an owner + test idea (§6 row filled with data or date).
- [ ] Closed-loop current verified before any accuracy claim is written.
- [ ] Full-FPGA deviation documented with ≥100 Hz budget (TL+Tsolv <10 ms).
- [ ] Revised Gantt + selected-part BOM replace Phase 1 estimates.
- [ ] 6× contribution summaries + ELSEE + Life-Long Learning forms collected.
- [ ] Presentation roster satisfies "non-Phase-1 presenters must present" rule.
