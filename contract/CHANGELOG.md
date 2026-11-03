# Contract changelog

All notable contract changes. Versioning: MAJOR = breaking interface change,
MINOR = additive, PATCH = clarification.

## Unreleased

- `icd/dac_fpga.md` — frozen Rev A (2026-11-02): 216-bit burst, TRIGGER cadence, CS gaps,
  CPOL/CPHA, SDI +2.5 ns delay, readback/CRC limits.
- `decisions_log.md` — #18, #20, #22, #23 promoted to LOCKED; #21 updated for the PS-less
  Artix-7 on BRD-01 (no 2×20 IDC); #27 FG-01 vendor coils.
- Version bump and tag pending the contract-change PR.

## 1.0.0 — 2026-10-29

Initial freeze imported from the Phase 2 design record.

- `system_contract.md` — SC-01…SC-10; D1-B (150 mm cube at 85.6–235.6 mm),
  D2-B (ICNIRP any accessible point + non-metal guard), D3-A (ADC channel map),
  D4 (150 mm volume + 100 mm high-precision core).
- `decisions_log.md` — decisions #1–#26, including M16 (DAC80508 + 8× LTC1563-2)
  and the one-board BRD-01 / PS-less Artix-7 decisions.
- `icd/pico_link.md` — Rev A, 2026-10-28.
- `requirements/manipulator.md` — RQ-M1…M17.

Consumers: `Capstone` monorepo (fpga, hardware, software) and the robot-arm repo
(pin `contract-v1.0.0`).
