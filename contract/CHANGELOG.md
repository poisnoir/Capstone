# Contract changelog

All notable contract changes. Versioning: MAJOR = breaking interface change,
MINOR = additive, PATCH = clarification.

## 1.1.0 — 2026-11-25 — tag `contract-v1.1.0` pending review

MINOR: additive decisions and interface clarifications; no pose/accuracy spec moved. This
section is prepared on branch `docs/spine-consistency`. **The tag, release zip/json and
arm-repo sync have not happened**; they follow PR approval and the two required approvals.

- `system_contract.md` — SC-07 corrected to the locked XO-direct clock tree (decision #21/#28):
  one 32.768 MHz XO drives ADC MCLK and the FPGA; the PLL only makes the 49.152 MHz DAC SPI;
  the selected part is an XO, not a TCXO, and there is no PLL-generated MCLK or discrete buffer.
  SC-05b and SC-08 updated for the one-board transport and the arm-only STOP scope.
- `icd/dac_fpga.md` — frozen Rev A (2026-11-02): 216-bit burst, TRIGGER cadence, CS gaps,
  CPOL/CPHA, SDI +2.5 ns delay, readback/CRC limits. §3 safe state clarified: genuine faults
  stop the DDS; an arm STOP does not (decision #30).
- `decisions_log.md` — #18, #20, #22, #23 promoted to LOCKED; #21 updated for the PS-less
  Artix-7 on BRD-01 (no 2×20 IDC); #27 FG-01 vendor coils (contract PR in review); #30
  arm-only STOP scope.
- **Decision #30 (STOP):** no panel E-stop / K1 / K2 on BRD-01. `PICO_STOP_N` is the AND of the
  FPGA request (`PICO_STOP_REQ_N`, `U4.P4` + `R754` pull-down) and the arm latch `U753.5 (Q)`
  via `/power/ARM_Q`; `U753.3 (~Q)` is NC. STOP is arm motion only, ≤100 ms; field and pose
  continue. The last hardware-independent stop path is removed; genuine faults still stop the
  DDS. #10/#21/#22/#25 are superseded in part.
- `icd/power.md`, `icd/pico_link.md`, `icd/adc_fpga.md`, `icd/README.md` — STOP split and
  on-board ADC nets instead of an external 2×8 header. Locked power parts (#20) are not
  changed by this release. Consumers: `Capstone` monorepo (fpga, hardware, software) and
  the robot-arm repo (pin `contract-v1.0.0` until this tag is published, then move to
  `contract-v1.1.0`).

## 1.0.0 — 2026-10-29

Initial freeze imported from the Phase 2 design record.

- `system_contract.md` — SC-01…SC-10; D1-B (150 mm cube at 85.6–235.6 mm),
  D2-B (ICNIRP any accessible point + non-metal guard), D3-A (ADC channel map),
  D4 (150 mm volume + 100 mm high-precision core).
- `decisions_log.md` — decisions #1–#26, including M16 (DAC80508 + 8× LTC1563-2)
  and the one-board BRD-01 / PS-less Artix-7 decisions.
- `icd/pico_link.md` — Rev A, 2026-10-28.
- `requirements/manipulator.md` — RQ-M1…M17.

Consumers at v1.0.0: `Capstone` monorepo (fpga, hardware, software) and the
robot-arm repo (pinned `contract-v1.0.0`; see the 1.1.0 section above).
