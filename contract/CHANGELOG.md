# Contract changelog

All notable contract changes. Versioning: MAJOR = breaking interface change,
MINOR = additive, PATCH = clarification.

## 1.1.4 — 2026-11-26 — tag `contract-v1.1.4` pending release

PATCH clarification; no interface change. The Ch3 reference sensor channel
stays in the SC-06 channel map, but its front-end parts stay DNP in the BOM and
assembly on the first build; firmware enables the channel when populated. The
user approved this directly on 2026-11-26 (decision #35) in place of the usual
`contract-change` PR and two approvals. The tag, release zip/json and arm-repo
sync remain pending, as for 1.1.1–1.1.3.

- **Decision #35 (Ch3 reference path):** wired but DNP on the first build. No
  board, BOM or firmware interface change: the first build keeps three
  populated channels plus the reference path, and Ch3 is enabled once fitted.
- `system_contract.md` SC-06 and D3 — the channel map now states the wired/DNP
  assembly state explicitly, matching `hardware/brd-01/kicad/README.md` and
  `hardware/brd-01/kicad/bom-to-cad.md`.
- `docs/phase2/frontend_requirements.md` §1 — the existing DNP statement now
  cites #35.

## 1.1.3 — 2026-11-26 — tag `contract-v1.1.3` pending release

PATCH defect correction in a locked SC row; no interface added or removed. The
cable requirement is tightened from a number that failed its own self-resonance
rule. The user approved this change directly on 2026-11-26; that approval is
recorded here (and in decision #34) in place of the usual `contract-change` PR
and two approvals. The tag, release zip/json and arm-repo sync remain pending,
as for 1.1.1 and 1.1.2.

- **Decision #34 (pen-cable capacitance):** SC-05c's cable allocation is
  corrected 56 → 53 pF. The locked total stays 73 pF at 34 kHz: 10 pF connector
  (RQ-C3) + 10 pF preamp-input stack + 53 pF cable. The old 56 pF gives
  76 pF total, \(f_{res}\approx333\) kHz < the 340 kHz floor;
  \(73.04-10-10=53.04\) pF. The filed 0.6 m W2697 whip passes by 14 pF; the
  longest cable at 65 pF/m is 0.816 m. Derivation: `docs/phase2/tone_plan.md` §6
  and `docs/phase2/adc_justification.md` §4 (both from the verified recalc
  \(e871e1f\)); preamp stack sources: INA163 SBOS177D and the BAS70H datasheet.
- `system_contract.md` SC-05c — decision text and status unchanged (LOCKED)
  except for the corrected allocation and the explicit 10 pF breakdown. The
  stale "connector Rev D" source citation is **dropped**: that file still
  quotes the superseded 56 pF cable allocation. The row now cites the two
  recalculated design documents instead, as does `decisions_log.md` #34.

## 1.1.2 — 2026-11-26 — tag `contract-v1.1.2` pending release

PATCH clarification; no rail, part or wire-interface behaviour changed. The
tag, release zip/json and arm-repo sync are pending PR approval and the two
required approvals.

- **Decision #33 (DAC tone band):** the DDS is clamped to **0.3–4.6 V, centre
  2.45 V** (≤92 % FS). `+5V_EXC` stays 5.0 V and the DAC80508 keeps its gain-2
  0–5 V part span; the 5.3 V ANY-OUT alternative is rejected (70 mV under the
  DAC 5.5 V maximum). This closes the amplitude wording left open by #31.
- `icd/dac_fpga.md` §3 — the OPEN amplitude follow-up is replaced by the locked
  firmware band; the gain-2 part span and no-CONFIG-write statement stand.
  `decisions_log.md` #33 added, the DAC OPEN bullet closed; cross-referencing
  docs (`power_tree_v2.md` §7 D2, `system_schematic.md`, the M16 FPGA handoff,
  `dig6_requirements.md` and `driver_power_requirements.md`) state the same band.

## 1.1.1 — 2026-11-26 — tag `contract-v1.1.1` pending review

PATCH clarification; no electrical or interface behaviour changed. Prepared on
branch `contract/pin1-nc`. **The tag, release zip/json and arm-repo sync have
not happened**; they follow PR approval and the two required approvals.

- **Decision #32 (Pico J123 pin 1 = no-connect):** the 6-pin Pico link is pin 1
  NC, pin 2 GND, pin 3 `PICO_TX`, pin 4 `PICO_RX`, pin 5 `PICO_STOP_N`, pin 6
  `PICO_HEARTBEAT`. BRD-01 does not supply 3V3 on J123; the Pico is powered from
  its own USB. The committed netlist (`8d39a99`) has
  `unconnected-(J123-Pin_1-Pad1)` with `J123.1` `passive+no_connect`, so the
  ICD Rev A 3V3 text was the stale side.
- `icd/pico_link.md` — Rev B (2026-11-26): pin-1 row is NC, the OPEN follow-up
  note is deleted, and the USB-powered/no-3V3 statement is recorded.
  `icd/README.md` status updated to Rev B; `decisions_log.md` #32 added and the
  pin-1 OPEN bullet closed. Cross-referencing docs (`brd01_io_handoff.md`,
  `brd01_wiring_manifest.md` note 2, `brd01_component_reference.md` item 5,
  `brd01_power_v2_deepseek_handoff.md`, `estop_scope_change.md`, `robot-arm/`
  README and INTEGRATION) now point at the closed decision.

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
- `decisions_log.md` — #21 updated for the PS-less Artix-7 on BRD-01 (no 2×20 IDC);
  #27 FG-01 vendor coils (contract PR in review); #28 clock clarification; #30 arm-only
  STOP scope. #18/#20/#22/#23 were already LOCKED on main; #20's part list is now
  superseded in part by #31.
- **Decision #30 (STOP):** no panel E-stop / K1 / K2 on BRD-01. `PICO_STOP_N` is the AND of the
  FPGA request (`PICO_STOP_REQ_N`, `U4.P4` + `R754` pull-down) and the arm latch `U753.5 (Q)`
  via `/power/ARM_Q`; `U753.3 (~Q)` is NC. STOP is arm motion only, ≤100 ms; field and pose
  continue. The last hardware-independent stop path is removed; genuine faults still stop the
  DDS. #10/#21/#22/#25 are superseded in part.
- **Decision #31 (power):** power tree v2 adopted — `+6V` from U147 TPSM63604 (1.024 MHz,
  synced to `BUCK_SYNC`), `+1V0_FPGA`/`+1V8_FPGA`/`+3.3V` from TPS62130A,
  `+5V_EXC`/`+5VA` from TPS7A4701, `±12VA` from MGJ2D151515SC + LT3045-1/LT3093.
  The OKI-78SR-5 / RV-1515D / TPS7A20 parts of #20 are removed; the adapter and
  one-board intent of #20 stand. The board/BOM already implemented v2.
- `icd/power.md`, `icd/pico_link.md`, `icd/adc_fpga.md`, `icd/README.md` — v2 rails
  (#31), STOP split and on-board ADC nets instead of an external 2×8 header. Consumers:
  `Capstone` monorepo (fpga, hardware, software) and the robot-arm repo (pin
  `contract-v1.0.0` until this tag is published, then move to `contract-v1.1.0`).

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
