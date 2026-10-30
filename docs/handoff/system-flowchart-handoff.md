# EM AccuBot — Standalone Flowchart Handoff (Systems & Subsystems, Detailed)

**STANDALONE NOTICE:** This document is self-contained. The flowchart author has NO access to the project folder, repo, PDFs, or spreadsheets. Everything needed to draw the charts is embedded below. Original file paths are noted in parentheses for traceability only — do not require them to complete the work.

- **Project:** EM AccuBot, Team 25 (ELEC/COEN 490 Capstone). FPGA-based electromagnetic motion controller for precision teleoperation.
- **Audience:** Person drawing the system/subsystem flowcharts for the Phase 2 report and presentation.
- **Goal:** Charts detailed enough that a new member can trace any sample from coil current to tool motion, and any spec to its test.
- **Architecture (locked, overrides Phase 1):** Full-FPGA pose. DDS excitation + ADC sync + demodulation + LM/TRF pose solver all in HDL/HLS on FPGA. No PC-side pose solver, no MATLAB-in-loop. Host is logging / calibration UI / visualization only.
- **Phase 2 update (2026-10-26):** `docs/phase2/design_order.md` and `docs/phase2/tone_plan.md` are the current decision records. Where this handoff says 20.5–27.5 kHz @1 kHz, CONVST, or SPI data, the newer documents win: tones are 20–34 kHz @2 kHz, AD7768-4 uses SYNC/START/DRDY, and the data path is DCLK/DOUT.
- **Drawing standard (mandatory):** IEEE 315 / IEC 60617 for all schematics, block diagrams, flow charts, and graphics. Software-only diagrams may use ANSI/IEEE Software Requirements Specification instead. Follow Concordia Form and Style Guide Ch.2–7 for layout. Signal flow left-to-right, power top-to-bottom, faults in red dashed lines, calibration in blue dashed lines. Cite equation numbers on model/solver/sensor blocks.

---

## 0. What Phase 2 requires (so the charts fit the report)

Phase 2 is "Design: carrying out the design work as scheduled in Phase 1, documenting the design, preparing the design review, and updating the schedule and plan." Group report is 15–20 pages and must contain:

1. Abstract.
2. Review of design specifications (OIQ 3.2.11, 3.3.14) — revisit all specs, confirm or revise with justification.
3. Design review of work done to date, with block diagrams, flow charts, graphs, schematics.
4. Alternatives at COMPONENT level (OIQ 3.1.2): list, analyze, state trade-offs explicitly, justify choice WITH NUMBERS (weighted matrix). Phase 1 was system level (EM vs stereo vs QR vs IMU vs linkage); Phase 2 is component level (coil geometry, driver, ADC/DAC, demod, solver, filter, leadscrew, camera, etc.).
5. Developing the solution selected (OIQ 3.1.4) + design development (3.2.4).
6. Deviations from Phase 1 task allocation/schedule, discussed and justified + updated schedule/plan. Final deliverables are evaluated against the REVISED plan.
7. Per-student 1–2 page contribution summary (6 members = 6–12 pages inside the page count).
8. Appendix A: first ELSEE assignment. Appendix B: Life-Long Learning form per student.
9. References (OIQ GPP, IEEE 315/IEC 60617, Jaeger 2018 equations, O'Donoghue 2014, ICNIRP).

Presentation is 40 min per group: 20 min present + 15 min Q&A + 5 min setup/logoff, over Zoom. Those who did NOT present Phase 1 MUST present Phase 2. Every member must accumulate at least 5 min of talk across Phases 1–4. Presentation is based on the report: main design/implementation results, problems deferred to Phase 3, justification of scope/spec/schedule changes vs Phase 1. A working demo of part of the project is encouraged but not mandatory.

Design approval rule: finish the design, draw the COMPLETE system block diagrams and schematic(s), present them to the Technical Coordinator, justify the solution, get approval of the schematic, then fill in and submit the BOM. Approval email must have the approved BOM plus supporting documents (schematics, block diagrams, flow charts, etc.) attached. Approval is not valid without attachments. If the design/BOM is not approved by the deadline (January 22, 2027, 17:00), the team may not receive materials on time.

Every spec number must have a test-case idea. For each number written, have an idea how to prove the design met it.

Suggested partial demos (any subset proving the chain): single-coil field sense on scope/FFT with SFDR check; DDS+ADC common-clock sync; Goertzel tone decode vs golden; static 5-DOF solve on a prerecorded frame; tremor-filter sim (6–12 Hz in, attenuated out); single-axis follower move from scaled synthetic pose. All on non-metal fixtures with conditions logged.

---

## 1. What to deliver (drawing list)

1. **L0 context diagram.** One box = EM AccuBot. External actors: operator hand (pen input), tracking volume (100 mm minimum / 150 mm target airspace), follower workpiece (5 mm cube tool volume), camera/display viewer, wall power (120 V 60 Hz), lab environment (temp/RH/metal rule), host logger.
2. **L1 system flowchart.** 7 boxes from Section 3, with every inter-system flow labeled with signal name, approximate level, and rate where given.
3. **L2 subsystem flowcharts.** One per L1 box (Sections 4–10), down to named blocks that each carry either an equation number, a parameter value, or a locked part number.
4. **L3 detail flowcharts.** Required for: (a) FPGA acquire-to-demod-to-solve pipeline, (b) calibration flow, (c) fault/stop flow, (d) tremor-filter plus scaling flow.
5. **Traceability table.** Every spec #1–25 maps to at least one flowchart block and at least one test idea (table provided in Section 9).

---

## 2. Default conditions, specs, and success gate (put in a corner box on every chart)

**Default test conditions** (apply to every spec row unless the row says otherwise): indoor lab; 18–28 C; 30–60% RH non-condensing; NO conductive/ferromagnetic objects except the system within 150 mm of tracking volume; controller inside tracking volume; scaling 100:1; tremor filter ON; 120 V +/-10%, 60 Hz wall power.

**Input specs (#1–7):** 1–2 pen controllers; 5-DOF each (x, y, z position plus pitch and yaw orientation; NO roll — single-coil physics, roll about the coil axis is unobservable); 100 mm minimum / 150 mm target / 200 mm stretch tracking volume (final by jitter gate SC-01d); +/-45 degrees pitch/yaw from rest; hand error at most 2 mm position (typical 1 mm) and at most 1 degree orientation on a reference grid; scaling selectable 20:1 to 1000:1.

**Output specs (#8–18):** tool workspace at least 5 mm cube; tool error at most 100 um at 20:1 and at most 25 um at 100:1 versus scaled hand motion; repeatability at most 10 um over 10 approaches; tremor attenuation at least 20 dB at 6–12 Hz; deliberate-motion attenuation at most 3 dB below 1 Hz (tested with 0.5 Hz and 1 Hz sine); latency at most 20 ms with filter OFF and at most 100 ms with filter ON; pose rate at least 100 Hz; stop (commanded or on tracking loss) within 100 ms; on-screen magnification at least 50x.

**Operator / safety / environment (#19–25):** pen mass at most 50 g; AC field at operator at most 27 uT anywhere in tracking volume (ICNIRP cap); supply 108/120/132 V at 60 Hz; material cost at most 1000 CAD per controller-plus-follower pair; operating 18–28 C; storage -10 to 40 C; RH at most 80% non-condensing.

**Functional requirements (8):** (F1) track 1–2 pens; (F2) scaled follow; (F3) tremor reduction; (F4) engage/disengage where the hand relocates while the tool stays; (F5) emergency stop; (F6) live enlarged view; (F7) timestamped pose log; (F8) status reporting including tracking-lost.

**Non-functional requirements (7):** (N1) micrometre-level precise and repeatable tool; (N2) no disruptive delay; (N3) no mechanical linkage (thin sensor cable is allowed); (N4) fail-safe halt on tracking or field fault; (N5) ICNIRP field compliance; (N6) in budget; (N7) ordinary lab plus wall outlet.

**Measurement of success (all under default conditions):** operator hits 9 of 10 targets of 200 um size using magnified view only; pen within 2 mm and 1 degree; pose at least 100 Hz; tool within 25 um plus repeatability within 10 um at 100:1; 20 dB tremor cut with at most 3 dB loss to intended motion; latency within 100 ms with filter on.

**Committed deliverable** is ONE controller-and-follower pair. A second pair is built only after the first meets spec. The follower XYZ stage is a demo test-bed, not the product. Stretch only: second pair, VR view, on-device outlier rejection.

**Team owners (from Phase 1 Table 8):** Field-generator coil array and placement simulation — Tung Lam Ha. Closed-loop current drivers — Tung. Receiver front-end and ADC interface — Tung. FPGA DDS and excitation — Kevin Michel Mandiouba. FPGA sampling, demod, and pose-estimate interface — William White. 5-DOF solver port to HDL/HLS LM/TRF — Kevin + William with Tristan Ovesson. Tremor filter, motion scaling, schedule tracking — Amirmohammad Gharibipour (Kalman, Oct to Mar). Follower mechanics, fabrication, assembly, characterization — Tristan Ovesson (MicroManipulatorStepper XYZ). Follower firmware, motor, host-comm, tracker integration — Joyal Biju Kulangara (homing/limits Nov–Jan, host commands, engage/disengage plus stop watchdog, status states). Magnified view, logging, failsafes — shared.

**Schedule backbone:** Sep–Oct 2026 research/architecture; Oct–Nov component select and procure; Oct–Jan FPGA plus Kalman start; Nov–Jan firmware/host; Dec assembly; Jan–Feb integration; Feb 15 pre-demo teleop prototype; latency/EMC/full-system tests; in-lab demo week of Mar 22; Apr 2 report. Second controller and VR only after core validates.

**Budget backbone:** about C$962 materials per controller-plus-follower pair (about 4% of a C$25.5k commercial equivalent); plus camera/test C$75 plus 15% contingency = C$1,193 total; funded by C$500 department plus team remainder. FPGA board already owned. FX for conversions: 1 USD = 1.425 CAD, 1 EUR = 1.604 CAD (Oct 2026). To-date ordered slices: pen analog link about $67.96 CAD parts plus about $8 shipping; ADC sub-assembly about $122.31 CAD; system-to-date about $190.27 CAD versus the 1000 CAD/pair cap.

---

## 3. L1 systems (top-level boxes and main flows)

Draw these 7 boxes. Arrows show the primary signal direction:

```
[1 FIELD GENERATOR] -- B-field, 8 tones -- > [2 PEN SENSOR + FRONTEND] -- uV-mV analog -- > [3 ADC + SYNC]
[1] <-- I-drive closed-loop -- [1b COIL DRIVER + DDS] <-- tuning words -- [4 FPGA CORE]
[3] -- samples --> [4 FPGA CORE: demod -> solve -> filter -> scale] -- xyz + status --> [5 FOLLOWER (PMS XYZ + firmware)]
[4] -- pose log >=100 Hz + video >=50x --> [6 HOST: viz / log / cal tools]
[7 POWER / SAFETY / ENV] -+-> all boxes (rails, interlocks, watchdogs)
```

| Box | Name | What it owns | Key specs |
|-----|------|--------------|-----------|
| 1 | Field-generator coil array + placement | 8-coil planar PCB, filament-model placement sim, ICNIRP field check | #3–4 volume/angle, #20 field |
| 1b | Closed-loop current driver + excitation DDS | Constant-current AC driver, FPGA multichannel DDS, current sense-back | kappa stability gate for #5–6 |
| 2 | Pen coil + receiver frontend | Hand-wound 5-DOF coil, INA128-class preamp, connector + whip cable | #1–2 pens/5-DOF, #5–6, #19 mass |
| 3 | ADC + clock/sync | External simultaneous ADC, TCXO-to-PLL common clock, integer-J framing | #5–6/#9–13 spur+phase, #14–16 rate/latency |
| 4 | FPGA core | DDS, ADC-sync, Goertzel demod, filament kernel, LM/TRF solver, Kalman filter, scaling, robot command | #5–6/#9–13, #12–13 filter, #14–16 |
| 5 | Follower + firmware + magnified view | PMS XYZ stage, Pico motor boards, homing/limits, engage/stop, camera/display | #7–11, #14–15, #17–18 |
| 6 | Host tools only | Logging, calibration UI, visualization link (NO pose solve here) | >=100 Hz log, >=50x view |
| 7 | Power / safety / environment / failsafes | PSU, interlocks, watchdogs, env procedure, BOM | #17 stop, #20–25 |

---

## 4. System 1 / 1b — Field generation + driver + DDS (draw as 3 lanes)

### 4a. Field-generator array (baseline to replicate)

- **Reference design (upstream snapshot, 35 files, ~43 MB):** 8-coil planar PCB named `spiral_coil_stackable_Rev_C` (Gerbers + .pcb + plot report in the Transmitter Coil PCB Gerber archive); mechanics `Top_plate4.SLDPRT`, `Bottom_plate4.SLDPRT`, `Wire_path_drawing.SLDPRT/.DWG`, assembly `fgasm.PDF`; photos `Field_Generator_Assembled.png`, `..._withDuplo.PNG`, `Assembly_Render.png`, `Exploded_Render.png`. New field-generator work (pen-volume placement sim, ICNIRP check) is new design; the reference Gerbers stay untouched.
- **Golden geometry (exact values for the solver and the sim):** outer square side length l = 70 mm; track width w = 0.5 mm; spacing s = 0.25 mm; PCB thickness 1.6 mm; turns N = 25; two footprints (vertical coils at 90 deg, angled coils at 45 deg). Eight centre positions in mm, x = [-93.543, 0, 93.543, -68.55, 68.55, -93.543, 0, 93.543], y = [93.543, 68.55, 93.543, 0, 0, -93.543, -68.55, -93.543]. Coils 2, 4, 5, 7 use the angled footprint; the rest use the vertical footprint.
- **Frequency plan (heritage):** 8 tones at 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5 kHz (1 kHz spacing, 20–30 kHz band). Each coil transmits one tone. Verify field at most 27 uT anywhere in the tracking volume.
- **Filament B-field model (draw these equations on the kernel block):**
  - Per straight PCB trace (Biot-Savart, Sonntag 2007): B(r) = (mu0 * I / 4pi) * ((c x a) / |c x a|^2) * ((a.c/|c|) - (a.b/|b|)), where I is filament current, a is the filament vector, b and c point from the observation point to the filament tip and tail. Equation (3.17).
  - Per coil: B_coil = sum of B(ri) over all k-1 filaments. Equation (3.18). Parallelizable. Minimum 8 coils for a planar tracker.
  - Do NOT use the dipole model B(r) = (mu0/4pi)*[3r(m.r)/|r|^5 - m/|r|^3], Equation (3.15), nor the large-circular-coil elliptic-integral model. Those are invalid close to large/planar coils. Always draw the filament model.
- **Placement simulation block:** inputs = trace layout above; outputs = B field, Jacobian J = dB/dp, and spur budget. Rerun when the field generator changes. A runnable Python mirror exists that ports the two MATLAB geometry/field functions and prints per-axis |J|, allowed voltage Vall, and per-tone spur allowance at z = 66/100/150/200 mm, centre and 50,50 mm off-centre.

### 4b. Driver + DDS (load-bearing — draw prominently)

- **Why it matters:** constant-current drive is load-bearing. Temperature and inductance drift break the per-coil calibration scalar kappa. Reference design: `ac_driver_coil_circuit_Rev_A.sch` + `.pcb` (DesignSpark) + Coil Driver Board Gerber archive; datasheets for LM7171 (current-feedback amp), LM311, TL081, MCP23008, MCP4562, IDT74FCT807BT, 74HC/HCT4051, SN74LVC1G3157, plus crystal, diode, switch, heatsink, and wire sheets. **Constant-current verification is a must-pass gate before any accuracy claim is written.**
- **FPGA DDS + common clock:** one TCXO feeds an FPGA PLL that produces clk_dds and clk_adc (CONVST/SCLK) frequency-locked. DDS formula: fout = tuning_word * fclk / 2^N; example 32-bit accumulator at 100 MHz gives 0.023 Hz steps. Chain: 12–14-bit LUT + 12–16-bit DAC + 50–100 kHz RC + coil inductance + narrowband DFT meets the spur budget. Use one sync reset for DDS and ADC dividers, then calibrate once. Analog group delay in microseconds is constant, so absorb it into one DAQ_phase_offset plus per-coil kappa. Do NOT generate-then-read per cycle; stream both continuously (example: 1000 master ticks per ADC sample at 100 MHz / 100 kHz).
- **Flows to draw:** tuning words -> DAC -> driver -> coil current -> sense-resistor sense-back (ADC channel 1, about 1 V, stationary) -> closed loop. Sense-resistor FFT check: harmonics more than 60 dB below the tone. The driver-summer current spectrum is the phase reference Y_I for demodulation. Jitter need is nanosecond level, not picosecond. ADC and DAC must accept external clock; prefer simultaneous-sampling over multiplexed (removes inter-channel skew); one sync reset then calibrate; verify constant current FIRST, coherence second.
- **Golden sense values (embed so the chart has numbers):** sense resistors R_store = [1.239, 1.02, 0.957, 0.995, 1.183, 0.983, 0.991, 0.989] ohms; Helmholtz calibrator current estimates I_temp = [2.3115, 2.3106, 2.3043, 2.3039, 2.3035, 2.3028, 2.3025, 2.3021]/99.96 A; B_temp = 321e-6 * I_temp T; sensor-plus-amp scale Asens = [7.8227, 8.1754, 8.4482, 8.7949, 9.1415, 9.4907, 9.8349, 10.1804] ./ B_temp (V/T per tone, Helmholtz + gain-phase analyser); summer scale I_summer_scale = 2.0103.

---

## 5. System 2 — Pen sensor + frontend

- **Coil itself (hand-wound, Thesis Table 7.1):** 12 mm long Delrin formers, hand-wound with visual/layer inspection, one turn of magnet tape per layer, twisted-pair to miniXLR plug RT5FC-B. Table:
  - A: 321 turns, 12 mm, 9 mm ID, 12.5 mm OD, 0.19 mm wire, 7.4 ohm, 604 uH.
  - B: 319 turns, 12 mm, 11 mm ID, 14.1 mm OD, 0.19 mm wire, 8.6 ohm, 804 uH.
  - C: 120 turns, 12 mm, 9 mm ID, 12.2 mm OD, 0.32 mm wire, 0.8 ohm, 91 uH.
  - D: 216 turns, 12 mm, 9 mm ID, 11.4 mm OD, 0.19 mm wire, 9.4 ohm, 425 uH.
  - E: 417 turns, 12 mm, 9 mm ID, 12.0 mm OD, 0.15 mm wire, 14.3 ohm, 1018 uH.
  - Ferrite option in C/D/E only: 12 x 6 mm 3C90 rod, relative permeability 2300. Resonance about 485 kHz air, about 290 kHz with ferrite; linear at 20–30 kHz.
- **Physics blocks (write these on the chart):**
  - (7.1) vs(t) = -dPhi/dt. (7.2) vs(t) = -N * d/dt * integral over Ac of (B.dA) — required for large coils. (7.3) small-coil form vs(t) = -mu0 * N * Ac * dH/dt, with B = mu0*H and Ac = pi*((do/4)+(di/4))^2 approx per (7.4). (7.5) apparent permeability mua = mur / (1 + kd*(mur-1)). (7.6) vs(t) = -mua*mu0*N * d/dt * integral(H.dA). (7.7) demagnetisation kd approx (dc^2/lc^2)*[2*ln(2*lc/dc)-1] for core diameter dc and length lc. (7.8) H = H0(x,y,z)*sin(wt). (7.9) vs(t) = -mua*mu0*N*w*cos(wt) * integral(H0.dA). mua = 1 for air core.
  - Point-sensor approximation Phi = mua*B*A*nhat with nhat = sin(theta)cos(phi)*xhat + sin(theta)sin(phi)*yhat + cos(theta)*zhat, Equations (3.19)–(3.24), valid ONLY for small cross-section where B is uniform; large coils must use integrated (7.2). Multi-coil vector form (3.25): V = [v1 ... vN]' = [dPhi1/dt ... dPhiN/dt]'. Minimum 8 coils for planar tracking. Ferrite gives about +10 dB but adds nonlinearity and Barkhausen noise.
- **Measured accuracy (embed as the acceptance reference):** 7x7 grid on the field generator at 85.6 mm and 152 mm heights = 98 points; RMS metric Equations (7.10)–(7.11) over x/y/z. Air: A 1.89 mm, B 1.59 mm, C 2.48 mm, D 1.98 mm, E 1.70 mm. With ferrite: C 1.90 mm (-23%), D 1.62 mm (-18%), E 1.58 mm (-7%). NDI 0.5 mm reference probe 1.79 mm in the same rig. FFT shows about +10 dB from ferrite (measured mua about 3 vs about 10 predicted, about 5 with corrected kd about 0.2). Assume bespoke coils are worse than NDI on jitter until measured.
- **Capacitance / resonance budget (load-bearing, draw as a constraint box):** Ctotal = Ccable + Cconn + Camp+ADC + Ctune. Self-resonance fres = 1/(2*pi*sqrt(L*Ctotal)) must exceed 10 * 27.5 kHz (i.e. above about 300 kHz). Worst case E plus ferrite L about 3 mH gives Cmax about 94 pF. Filed pen whip (0.6 m miniature balanced about 39 pF + 10 pF connector + 10 pF amp/ADC = 59 pF) passes with 35 pF left for tuning or margin. Built air coils pass trivially (B 804 uH allows 350 pF; C 91 uH allows nanofarads). ADC input capacitance (typically 10–20 pF) is a first-class term; any candidate above 20 pF must be re-budgeted.
- **Amp heritage (no coil geometry inside):** Sensor Amplifier PCB archive (Eagle E301 versions 2.0/3.0 .brd/.sch) is INA128U plus 3296Y trimmers plus 1206 passives only, plus Gerbers archive. Sensor plus amp collapse into Asens(f) per tone plus per-emitter BScale kappa (8x1) plus zOffset, switched per sensor.
- **Flows:** B-field at pen -> flux -> uV–mV -> differential preamp (E301 class, input impedance at least 1 Mohm, CMRR at least 60 dB) -> ADC channel 2, moving (plus optional reference sensor channel 3). Helmholtz-calibrate pen plus amp as a unit: Asens(f) = V/B. Pen mass at most 50 g.
- **LOCKED connector + cable (embed part numbers so purchasing is unambiguous):**
  - Connectors (Rev B): L1 chassis receptacle IO IO-TXLR3-M-PS-1, male pins, solder cup, panel bulkhead on preamp box, 3-pos mini-XLR, brass/gold, about 10 mohm, 1000+ cycles, mates with L2 one-to-one. L2 cable plug IO IO-TXLR3-F, female sockets, solder, for 2–3.5 mm cable OD. Quantity 2 each (2 sensor channels: probe plus reference/spare). Approved second source: Amphenol AG3MCC plus AG3F. Female on cable, male on panel (microphone convention, no exposed pins on pen). Weighted decision (OIQ style, weights sum 1.0): cost 0.20, mating cycles 0.20, mass/OD 0.20, solder/build speed 0.15, shield/chuck fit 0.15, stock 0.10; IO pair scores 4.45/5, Amphenol 4.15, Switchcraft TB3 3.45, LEMO/JST pen-final 3.30.
  - Cable (Rev C): C1 pen whip Mogami W2697 2-conductor 28 AWG miniature balanced (one twisted pair plus served shield, 2.5 mm OD), 10 ft cut (two 0.6 m whips plus spare), about 65 pF/m so 0.6 m is 39 pF plus terminations = 59 pF within 94 pF, lavalier flex, lowest torque. C2 static-reference only Mogami W2893 4-conductor 26 AWG mini quad paralleled to a pair plus shield, about 4 mm OD, 5 ft cut, quad gives 10–20 dB extra rejection but about 130 pF/m so cap at 0.5 m on air coils only. C3 termination AES48: pen-plug Pin 1 = braid only with coil-to-shield open; panel Pin 1 plus shell to chassis star; pigtail under 10 mm; verify open with DMM. Weighted cable decision: C-budget on built coils 0.25, chuck fit 0.25, flex/tremor 0.20, mass 0.15, handling noise 0.10, stock/build 0.05; W2697 scores 4.90/5 (locked pen whip), others 2.85–2.95 or static-only.
  - Connector requirements (any vendor must pass): RQ-C1 at least 3 poles (SIG+, SIG-, shield drain); RQ-C2 contact resistance at most 30 mohm initial and delta at most 10 mohm over life, isolation at least 1 Gohm; RQ-C3 contact capacitance at most 10 pF and Ctotal within 94 pF; RQ-C4 over 1000 mates, latch, at most 20 N, chuck 2–4 mm, shell under 10 g off-pen; RQ-C5 360-degree shield, single-point star at ADC, shell over 30–50 mm from coil; RQ-C6 Pmod/SPI is the digital ADC-to-FPGA link, not the preamp link.
  - Cable requirements (any bulk wire must pass): RQ-B1 2 conductors plus braid/spiral shield, 24–28 AWG stranded OFC, conductor at most 0.2 ohm/m, shield at most 0.1 ohm/m; RQ-B2 cond-shield K0 at most 150 pF/m AND length-times-K0 within 76 pF budget, cond-cond K1 at most 15 pF/m, length at most 0.8 m; RQ-B3 shield coverage at least 90% braid/served on the whip (foil rejected — cracks with 6–12 Hz flex), 360-degree termination, pigtail under 10 mm; RQ-B4 OD 2.0–3.5 mm, mass at most 15 g/m, flex at least 10k cycles with bend at most 30 mm, handling under 0.2 mV; RQ-B5 twist pitch at most 25 mm, route pen whip away from field-generator drive and BNC by over 10 cm, single-point star at ADC.

---

## 6. System 3 — ADC + sync (draw the external ADC as locked, XADC as a rejected path)

- **Decision (locked):** external simultaneous sigma-delta, 24-bit class, for the signal path. Primary: AD7768-4 (4-channel simultaneous, 256 kSPS, group delay 133 us, in stock; confirm RL7 vs RL unit price in cart, take cheaper). Backup with quantity zero (do not order unless primary fails vetting): ADS1274-class quad 24-bit to 144 kSPS, frames at most 500 samples. Voltage reference ADR434BRZ 4.096 V. Fallback if sigma-delta vetting fails: simultaneous SAR AD7606C-16 class (8-channel simultaneous, 16-bit, 1 MSPS, serial, +/-10/+/-5 V) WITH a 5th–6th-order matched analog anti-alias pair as a new Phase 2 deliverable with measured drift data. XADC (dual 12-bit SAR, 1 MSPS aggregate shared across a muxed sequencer, 0–1 V unipolar, DRP/AXI readout, no external CONVST edge) is DC housekeeping ONLY (die temp, rails, static field-probe level, interlock comparators) — never in the 20–30 kHz signal path.
- **Why XADC fails (draw as 4 kill-arrows):**
  - (a) Resolution: ideal SNR = 6.02*N + 1.76 dBFS, so 12-bit is 74 dBFS ideal and about 62–68 dB real (ENOB 10–11) against a 60–70 dB spur budget — zero margin before thermal, leakage, and crosstalk. Position falloff (~1/r^3) from 85.6 to 152 mm is (152/85.6)^3 about 5.6x or 15 dB, plus orientation nulls (nhat.B to zero near +/-45 deg) drive individual tones toward zero; net spread routinely 30–40 dB, so the weakest tone lives on 40–400 LSBs and a nulled tone on a handful of LSBs. Phase variance sigma_phi approx sigma_n/(A*sqrt(N)) with sigma_q = q/sqrt(12) inflates past the sign-decision boundary, mirroring the solved hemisphere by tens of degrees, then LM retry and lock loss. 16-bit buys 6.02*(16-12) = 24 dB. Processing gain PG = 10*log10(N/2) with N = 500–2000 (24–30 dB) helps both converters equally and does not close the gap. Kills hand/orientation at nulls and edges, tool error via mis-oriented nhat, repeatability floor, and 6–12 Hz sidebands under the spur floor.
  - (b) Mux skew: XADC samples Ch1 then Ch2 sequentially with delta-t at least 1 us (worse with sequencer overhead). Phase skew delta-phi(f) = 2*pi*f*delta-t gives 0.129 rad (7.4 deg) at 20.5 kHz and 0.173 rad (9.9 deg) at 27.5 kHz. The heritage NI-6216 (also muxed, 400 kS/s) survived only via per-tone DAQ_phase_offset = 2*pi*F/400000, valid while delta-t is constant. XADC delta-t moves with sequencer programming, AXI arbitration, temp, and supply; drift of just 100 ns is 2*pi*27.5 kHz*100 ns = 0.017 rad = 1.0 deg, the ENTIRE orientation budget. The residual gate (1e-15) then rejects frames or converges mirrored, stalling the 100 Hz pipeline with retries. Simultaneous sampling has skew identically zero. Kills orientation, rate (retry storms), and filter-off latency.
  - (c) Shared-cap crosstalk plus non-deterministic readout: mux kickback with Ch1 at about 1 V and Ch2 at uV–mV gives first-order crosstalk of -60 dB injecting Vxtalk = 1 V * 10^(-60/20) = 1 mV — signal-sized, at the SAME 8 tone frequencies, unfilterable, corrupting kappa. PS-polled readout jitters frame boundaries by microseconds, breaking integer-J lock and spreading each tone into 1 kHz-spaced neighbours by 10–20 dB, burying tremor sidebands. PL-generated CONVST with DRDY interrupt and ping-pong BRAM/DMA holds determinism; PS polling cannot. Throughput is not the blocker (500 kS/s/ch times 1000-sample frame = 2 ms acquisition — fast enough); determinism is. Kills position on far tones, tremor, and pipeline jitter.
  - (d) Input range/drive: 0–1 V unipolar forces an attenuate/level-shift stage presenting under 100 ohm settling impedance within 1 us, whose own settling crosstalk must still be calibrated — effort better spent on a differential bipolar simultaneous ADC whose +/-5/+/-10 V range matches the preamp directly.
- **External ADC requirements (annotate on the chart as RQ-A1 to RQ-A7):**
  - RQ-A1 simultaneous: Ch1 current plus Ch2 sensor (plus Ch3 reference) on one CONVST edge, skew identically zero. Verify two-tone phase flat vs frequency and temp.
  - RQ-A2 resolution: at least 16 bit, SINAD at least 84 dB, THD at most -90 dB. Verify single-tone FFT at 25 kHz at -1 dBFS and -40 dBFS plus far-tone SNR.
  - RQ-A3 rate: at least 500 kS/s/ch sustained (1 MSPS preferred), no missing codes. Frame 500–2000 samples = 1–4 ms acquisition at 500 k, leaving demod plus LM inside the 10 ms pose budget. Verify sustained DRDY capture plus code-density histogram.
  - RQ-A4 sync: external CONVST plus SCLK inputs, aperture jitter at most 1 ns rms, since SNR_j = -20*log(2*pi*f*tj) gives 104 dB at 27.5 kHz and 1 ns — below the 16-bit floor so jitter never binds. Verify clock-phase sweep and integer-J leakage test.
  - RQ-A5 input: differential/bipolar (+/-5 V or +/-10 V), input impedance at least 1 Mohm, CMRR at least 60 dB. Verify CMRR sweep 20–30 kHz and impedance vs frequency.
  - RQ-A6 digital: SPI/serial lanes to programmable logic, SCLK to 50 MHz, 3.3 V Pmod-compatible. Floor SCLK at least Fs*(bits+overhead)*channels/lanes: 500 k*18*2/2 = 9 MHz minimum; run 25–50 MHz with framing headroom. Verify eye/continuity plus sustained lane-rate soak.
  - RQ-A7 determinism: DRDY/BUSY to logic interrupt, ping-pong BRAM/DMA, zero dropped frames at 100 Hz or more. Verify 1-hour moving-sensor run at 100 Hz or more with drop counter zero.
  - Locked class: simultaneous sigma-delta 24-bit (2x ADS127L11 synced or ADS1278-class). Fallback listed above. Single-channel or multiplexed parts (for example single AD4004 alone, or 32 kSPS-class parts) do NOT pass RQ-A1 and the ODR floor — rejected.
- **Why sigma-delta wins (draw as the deciding note):** (1) Phase-match for free. A SAR needs a flat-to-27.5 kHz analog anti-alias filter fully down before Fs/2 (for example -80 dB at 250 kHz for Fs = 500 kS/s): a 5th–6th-order matched pair, one per channel. Two 1%-tolerance analog filters mismatch corner by about 1%; near-corner phase slope converts that into about 0.3–0.5 deg per 2nd-order section at 27.5 kHz (absolute phase about -30 deg for fc = 100 kHz), and two cascaded sections plus temp drift consume the whole 1-degree budget before the ADC contributes anything. Sigma-delta digital decimation filters on Ch1/Ch2 are bit-identical arithmetic: mismatch identically zero over temperature forever; only one RC pole per channel remains (set a decade out, about 2.8 deg absolute, matched to resistor tolerance). (2) Quantization disappears as a variable. 24-bit full-scale ideal SNR = 6.02*24+1.76 = 146 dBFS; real ENOB 17–20 at speed is 104–122 dB, so quantization sits 25–40 dB below the analog chain floor (preamp noise-dominated about 60 dB over 5 kHz BW), and shortening frames for latency (halving N loses 3 dB of processing gain) never exposes a quantization wall. With 16-bit SAR the same move costs real margin against a 90 dB-real converter already 20 dB closer to the spur floor.
- **Sigma-delta costs, bounded (draw as notes):** group delay D = Ntaps/ODR (example 64 taps at 400 kSPS = 160 us) shifts every frame equally and is subtracted once as a fixed timestamp offset; require D under 0.5 ms so acquisition plus D stays inside the under-10 ms budget. ODR floor is hard: passband must cover 27.5 kHz with margin, so ODR at least about 4*27.5 = 110 kSPS; parts capped at 32 kSPS are rejected without review. Lane floor rises with word length: 2 ch x 32-bit frames (24 data + status) x ODR over 2 lanes gives SCLK_min = 400 k*32*2/2 = 12.8 MHz; run 25–50 MHz on Pmod over under 10 cm with series-R and a ground per signal. Power/price fit the 1000 CAD/pair envelope at prototype quantity and do not touch the pen mass budget (preamp-box parts). Prefer the lowest-delay filter mode whose droop is stable over temperature; stable droop is absorbed into per-tone kappa.
- **Vetting gate before any sigma-delta BOM row:** simultaneous modulators with shared START/CLK; ODR at least 250 kSPS preferred (110 k hard floor); D under 0.5 ms in the selected filter mode; droop at 27.5 kHz stable within 0.05 dB over 18–28 C (else it escapes kappa); Cin at most 20 pF into the 94 pF budget; SPI lanes sustaining the lane rate; in stock at an approved supplier. Shortlist: 2x ADS127L11 synced (24-bit, to 400 kSPS) or 1x ADS1278 (8-ch simultaneous, to 144 kSPS, marginal headroom). Locked file choice per BOM: AD7768-4 primary as above.
- **Pmod/SPI physical note:** Pmod = physical 2x6 100 mil, host-female / peripheral-male, 3.3 V (Digilent Type-2A SPI: SCLK/MOSI/MISO/CS plus CONVST plus DRDY plus RESET plus GND/VCC). Logic implements a CONVST generator phase-locked to DDS, SPI master at the ADC clock polarity/phase, DRDY-gated capture, ping-pong BRAM to AXI DMA. Processor configures and consumes frames; nothing bit-banged at rate. FMC/LVDS enters only for parallel over 10 MSPS x 16 bit x 2 ch — not needed at filed rates.
- **Timing core (draw prominently):** integer-J frames — frame = J DDS cycles, Fs = Fclk/N from one TCXO-to-PLL. PL-generated CONVST phase-locked to DDS. TL = L/Fs where TL is acquisition time, L is frame length in samples, Fs is sampling rate. (Note: one thesis print shows Fs*L — that is an OCR drop; 5000/100 kHz = 50 ms proves division.) Fs is hardware (DAQ/ADC max plus Nyquist 68 kHz for 34 kHz). L is the choice (bin width w = Fs/L under half the 1 kHz tone spacing, coherence with J integer, Hamming 780 Hz lobes non-overlapping). TL is the consequence. Maximum system rate = 1/TL; measured rate is lower. Filed budget with filter OFF, worst case: Tpose = Tacq + Tdemod + Tsolv under 10 ms, with Tacq = N/Fs (1000/500 k = 2.0 ms; 500/1 M = 0.5 ms), leaving about 8 ms for streaming Goertzel demod (parallel per tone, in logic) plus bounded LM/TRF (relaxed tolerance, warm-started from a moving-average filter, ping-ponged with acquisition). Choose L by sweeping L = 50–2000 and plotting SFDR, Brms, |J|, position sigma, and rate; smallest L with sigma at most 0.15 mm plus spur under tone plus Tacq+Tsolv under 10 ms moving wins. If no such L exists, fix current/noise/clock/ADC, not L.

---

## 7. System 4 — FPGA core (needs its own L3 pipeline chart)

**Pipeline order (golden, draw top to bottom):** select sensor -> demodulate stored samples to field strengths -> resolve 5-DOF vector -> convert to 4x4 matrix. In golden MATLAB these are `fSysSensor -> fSysGetField -> fSysDecodeField -> fSphericalToMatrix`, called per pose by `fGetSensorPosition`.

1. **Sensor select:** switch on sensor number 1 or 2; load that sensor's zOffsetActive, BScaleActive (8x1 kappa), BStoreActive (49x8 grid), and estimateInit (warm-start vector). If no sensor selected, raise an error. For two pens, call repeatedly because each pen has different calibration.
2. **Demodulation (draw full math):** inputs per frame are reference current samples X(:,1) = rawData(:,1) and selected-sensor samples X(:,2) = rawData(:,dataColumn), where DAQ channels are [0, trackingSensor, refSensor] (example [0,1,4]: ch0 = current sense). Demodulate with the matrix FIR method Y = (X .* G) * E, where E is Lx8 complex exponentials exp(j*2*pi*F*t) with F as above and G is the replicated lowpass/chebwin window (length L-1, 200 dB sidelobe design in golden). Magnitudes MagY = 2*abs(Y); phases PhaseY = angle(Y). Phase difference Phase1 = PhaseY(current,:) - PhaseY(sensor,:) - DAQPhase, where DAQPhase = 2*pi*F/400000 per tone in the heritage muxed system (constant only while mux skew is constant — removed by simultaneous ADC). Wrap each tone into [-pi, pi]: if abs(Phase1(j)) > pi then Phase1(j) = -sign(Phase1(j))*(2*pi - abs(Phase1(j))). Field per coil BField = sign(Phase1)' .* MagY(sensor,:)' ./ Asens'. So the ADC carries PHASE, not just magnitude; any skew/drift/crosstalk lands in the orientation sign.
   - **HDL form:** Goertzel per tone s[n] = w[n]*x[n] + 2*cos(2*pi*Fi/Fs)*s[n-1] - s[n-2], read Y = s[L-1] - exp(-j*2*pi*Fi/Fs)*s[L-2]. Same multiply-accumulate count as the matrix form, but streaming: 2 states plus 1 coefficient per tone, latency TL+2 cycles, ping-pong frame N/N+1, no block-RAM burst. Matrix form is kept as the Python golden check; Goertzel goes in HDL. Buffer frame, bulk dot versus 8 templates costs Lx8 complex MACs plus Lx8 coefficient store (about 80k floats at L=5000).
3. **Filament kernel (draw as the model block):** inputs are filament current I=1, coil trace matrices xcoil/ycoil/zcoil, and observation point Px,Py,Pz. Steps per filament: a = end-minus-start; b = end-minus-P; c = start-minus-P; mag_b, mag_c; a.b, a.c; q = c x a components; m2 = |q|^2; s = ((a.c/|c|)-(a.b/|b|))/m2; H-contribution = (I/4pi)*q*s; sum over filaments to Hx,Hy,Hz. Scale by mu0 to Bx,By,Bz. Called on every cost evaluation (about 800 filament segments). Geometry helper generates the spiral trace coordinates from N, length, width, spacing, thickness, angle as in Section 4a.
4. **Solver (draw full cost + bounds + retry):** state p = (x, y, z, theta, phi). Cost F(x,y,z,theta,phi) = Vd - kappa .* Vm, Equation (3.26), where Vd is the measured voltage/field vector from (3.25)/demod, Vm is the model vector, kappa is the per-coil calibration scalar (electrically: current-to-sensor-voltage per transmitter coil; linearity lumps all into one scalar per coil). Minimise ||F(p)||^2 subject to lb <= p <= ub, Equation (3.27); pmin is the sensor pose. Use Levenberg-Marquardt or trust-region. Golden bounds (portable rig): lower [-0.25, -0.25, 0, -2pi, -2pi], upper [0.25, 0.25, 0.5, 2pi, 2pi]. Golden solver options: TolFun 1e-16, TolX 1e-6 (1 um optimizer step — NOT system resolution, which is ~150x coarser than noise), MaxFunEvals 500, MaxIter 40, Display off; residual threshold 1e-15; initial estimate at transmitter centre 15 cm above it (x0 = [0, 0, 0.15 or -0.15, 0, 0] plus moving-average store MA_length = 5 prefilled with x0, which moves the start to the previous good solution to improve convergence). If residual above threshold, retry once from estimateInit + [0,0,0,pi,pi]; if still above, give up and return the initial estimate (tracking-lost path). Per-coil flux model in the cost: fluxModel = BScaleActive' .* (Iout' ./ Rstore') .* (Bx*sin(theta)*cos(phi) + By*sin(theta)*sin(phi) + Bz*cos(theta)); out = fluxModel - fluxReal. FPGA port: relaxed TolFun, warm-started, ping-ponged acquire/solve, Fs above 100 kHz. Failure mode to draw: moving sensor over 50 cm/s breaks the warm start and needs more iterations (heritage MATLAB drops 72 to 64 Hz) — draw this retry-storm arrow as a threat to the 100 Hz budget.
5. **Spherical-to-matrix:** inputs [x,y,z,theta,phi] with theta elevation and phi azimuth. Output 4x4 matrix R = Rz(phi)*Ry(theta) plus translation: row1 [cosphi*costheta, -sinphi, cosphi*sintheta, x]; row2 [sinphi*costheta, cosphi, sinphi*sintheta, y]; row3 [-sintheta, 0, costheta, z]; row4 [0,0,0,1]. For the Slicer/visualizer path, add pi to phi, convert metres to millimetres, premultiply by a fixed Slicer registration matrix, attach a timestamp, and send as a transform.
6. **Spur budget annotation (draw as a table on the demod/solver boundary):** position sigma sigmax = sigmaV / ||J|| where J[i] = dBz,i/dx (finite-difference with dx = 0.2 mm in the sim). Values for the z-coil, 1-D least-squares (reference for the chart):
   - z=66 mm centre: |Jx| 5.43e-04 T/A/m, Vall = 0.15 mm*|J| is -35.6 dB (x) / -48.2 dB (z) re Brms, per-tone (minus 18 dB) -53.6 dB.
   - z=100 mm centre: |Jx| 2.28e-04, Vall -41.4 dB (x) / -46.0 dB (z), per-tone -59.4 dB.
   - z=150 mm centre: |Jx| 0.69e-04, Vall -46.6 dB (x) / -45.6 dB (z), per-tone -64.6 dB.
   - z=200 mm centre: |Jx| 0.26e-04, Vall -50.2 dB (x) / -46.8 dB (z), per-tone -68.2 dB.
   - Off-centre 50,50 mm within 1–2 dB. Quoted 60–70 dB budget = Vall(-35 to -51 dB) minus 8.45 dB (7 aggressors) minus 9.5 dB (spur under one-third of jitter). Full 5-DOF 8x5 Jacobian tightens about 2–3 dB. Fractional dV/V per coil is unusable (nulls give 1e6 %/mm); joint least-squares must be used. Recompute with final pen turns/area and output current/sense-resistor when the field generator changes.
   - Bench check: (i) Helmholtz-calibrate pen+amp as a unit; (ii) single coil on with closed-loop current logged, on a non-metal stage (coarse blocks plus micrometer fine plus USB microscope), L=5000, Fs=100 kHz, demod as above, B = |Y|/Asens, calibrate kappa/zOffset on the 7x7 grid first; (iii) finite difference Jx,i = [Bz,i(x+dx)-Bz,i(x-dx)]/2dx with dx = 0.5 mm at 66/100/150 mm and compare to the table — over 20% mismatch means a current/metal/kappa issue; (iv) all coils on: SFDR = 20*log(Vi/Vspur) from raw-volts FFT must beat the per-tone column.
7. **Pose-rate context (draw as the rationale for full-FPGA):** heritage名的 performance with Fs = 100 kHz: frame 250 (2.5 ms acq) gives 72 Hz static / 64 Hz dynamic; 500 (5 ms) gives 70/61; 1000 (10 ms) gives 65/62; 2000 (20 ms) gives 50/50; 5000 (50 ms) gives 20/20. Static means under 5 cm/s; dynamic means over 50 cm/s. At frame 250 with 72 Hz, total 13.9 ms minus acq 2.5 ms leaves solve-plus-overhead about 11.4 ms; 100 Hz needs under 7.5 ms. Minimum frame 50 gives 2 kHz bin width and Fs/L spacing but separate DDS/ADC clocks leak, so practical minimum is 250 plus Hamming (780 Hz lobe). A Linux DAQ buffer issue forces acq longer than solve (empirically frame 2000). Creators swept frames 250–5000 across OS/language/static/dynamic and chose large frames for accuracy — they built a visualizer, not a tremor loop. Paper rate 15 Hz (Nyquist 7.5 Hz) misses the 6–12 Hz tremor band entirely; MATLAB 50–72 Hz and Python-static to about 138 Hz still miss margin. Hence full-FPGA with common-clock DDS+ADC, streaming demod, parallel filament kernel, relaxed tolerance, ping-pong, Fs above 100 kHz.
8. **Framework mapping (for the software swimlane, kept for traceability):** heritage Python framework had four modules — daq.py (acquire via NI-DAQmx/Base or MCC UL, PyDAQmx cross-platform), filter.py (conditioning, discrete Fourier, matrix multiplies), model.py (field model), solver.py (cost, LM/TRF, tolerances), plus pyIGTLink.py (stream 4x4 transforms to CustusX/3DSlicer). MATLAB golden files map as: filament kernel + geometry helper to the FPGA filament kernel; objective (cost) to the solver cost; decode-field to the bounded least-squares solver; tracking (sensor-position) to the pipeline order; DAQ-update plus get-field plus DAQ setup to the demod/ADC-sync path; calibration trio to the FPGA calibration flow; sensor-select/save/setup/run scripts to harness/setup only (not synthesizable); IGTLink API to host visualization only. Data acquisition setup in golden: NI-USB 6216 in session mode, single-ended channels [0,1,4] at Fs = 100 kS/s with continuous background acquisition and a DataAvailable listener calling the store callback; heritage demodulation used Fs = 100 kS/s, L = 5000, F as above, E as above, G as replicated FIR/chebwin row, and a moving-average store as above.
9. **Tremor filter + scaling (draw as post-solve blocks):** Kalman filter (Oct–Mar owner); requirements at least 20 dB cut at 6–12 Hz and at most 3 dB loss below 1 Hz (verify with sine sweep 6–12 Hz plus 0.5/1 Hz); scaling 20:1–1000:1, default 100:1; tool_error = hand_error / S (2 mm hand /100 = 20 um tool, passes 25 um; /20 = 100 um, borderline; visual-servoed 200 um targets tolerate smooth 2–3 mm bias the operator adapts to, but NOT non-linear distortion changing over 0.5–1 mm over a few mm travel, nor jitter/drift/latency). Resolution note: no smallest-step spec was published; jitter is the floor. Heritage jitter with the NDI probe (150 samples at 15 Hz): bottom 0.13 +/-0.11 mm, middle 0.15 +/-0.10 mm, top 0.29 +/-0.34 mm; accuracy 0.82/1.14/1.98 mm bottom/mid/top; rotation 0.04 deg perpendicular / 0.09 deg coplanar. Tool-side at 100:1, 0.15 mm maps to 1.5 um jitter, fine versus 10 um repeatability and 25 um budget. Tremor needs resolution, not absolute accuracy: a 2 mm DC offset plus 0.5 mm 10 Hz wobble is filterable, but 2 mm random 10 Hz jumps are not; need in-band (6–12 Hz) jitter about 0.1–0.2 mm RMS hand-side at 100 Hz or more. Heritage had tremor = none (only moving-average length 5).
10. **Outputs:** x/y/z plus pitch/yaw plus status go to the follower command, the timestamped pose log, and the visualization link.

**FPGA board note:** board and HDL partitioning are NOT frozen — leave a generic "FPGA (TBD)" box and do not pin drivers or constraints.

---

## 8. System 5 / 6 — Follower, firmware, view, log (draw as command + safety loop)

- **PMS XYZ stage (test-bed, not the product):** open-source MicroManipulatorStepper XYZ; resolution test with about 10 um per full step at 2 mm lead baseline; budget backlash and microstep error against 10 um repeatability; workspace at least 5 mm cube verified by micrometer travel.
- **Firmware / motor / host-comm / tracker integration:** homing and limits (Nov–Jan), host commands, engage/disengage (hand relocates, tool stays), emergency stop plus stop watchdog within 100 ms, status states: tracking / out-of-volume / stopped / fault.
- **Magnified view + logging + failsafes:** at least 50x camera/display (verify by stage-micrometer on-screen calibration); timestamped pose log at 100 Hz or more; volume-excursion halt plus alarm; excess-tremor halt; field-instability halt; comm-loss watchdog.

---

## 9. Calibration + verification flows (separate swimlane charts)

### 9a. Calibration flow (blue dashed)

1. Helmholtz-calibrate pen plus amp as a unit: Asens(f) = V/B per tone using a gain-phase analyser.
2. Collect the grid: 7x7 point-by-point on the field generator (49 positions; top-down grid with points shaded by Euclidean distance from the origin; Delrin former in equispaced holes; two former heights give 49 x 2 = 98 measurements per coil). Golden portable coordinates: x = (-3 to 3)*31.75 mm repeated over 7 rows; y = 95.25, 63.5, 31.75, 0, -31.75, -63.5, -95.25 mm; z = (boardDepth 15 mm + (5 + 0.5)*19.2 mm) for portable (fixed rig uses 32 mm pitch minus 8 mm offset and boardDepth 11.5 mm with negative z). Prompt per point, acquire via DAQ-update, demodulate via get-field, store into BStoreActive (49x8), save to per-sensor file. Single coil on, closed-loop current logged, non-metal stage (coarse blocks plus micrometer fine plus USB microscope), L = 5000, Fs = 100 kHz.
3. Fit per coil: for each coil 1–8, extract that coil's 49 field strengths, solve for [zOffset, Bscale] starting from [0, 1] with least-squares options TolFun 1e-22, TolX 1e-7, MaxFunEvals 2000, MaxIter 2000, using the single-coil z-offset/scale objective (model each test point with the filament kernel for that coil only, scale by mu0*Bscale, multiply by Iout/Rstore, difference versus sensed). Store zOffsetAllCoils per coil and BScaleActive per coil; mean zOffset over coils is the active offset; save per-sensor calibration file plus system file. Then apply zOffset to the test-point z, recalibrate once more, and re-check.
4. Check: for each test point, solve the full 5-DOF cost from that point's stored fields starting at the analytic point (theta/phi zero, sensor axial), with check options TolFun 1e-17, TolX 1e-8, MaxFunEvals/MaxIter 500, bounds x/y +/-0.25 m, z 0–0.5 m, angles per rig; error per axis is measured-minus-analytic; total per-point error is sqrt(dx^2+dy^2+dz^2); report RMS in mm. Ideal is zero; real error comes from positional uncertainty, tolerances, and calibration noise.
5. Keep this procedure for the FPGA calibration flow (same steps, same metric).

### 9b. Verification: spec-to-block-to-test table (draw each test as a tag on its block)

| Spec | Threshold | Design block(s) | Test idea |
|------|-----------|-----------------|-----------|
| #1–2 | 1–2 pens, 5-DOF no roll | Pen coil + sensor-select + solver DOF | Two-pen arbitration; show roll unobservable by construction |
| #3–4 | 100 mm min / 150 mm target, +/-45 deg | Field-generator placement sim | Reference-grid sweep with known steps |
| #5–6 | Hand at most 2 mm / 1 deg, RMS Eq.7.10 over 98 pts at 85.6/152 mm | Generator + driver + frontend + ADC + solver + kappa cal | 7x7 grid at 2 heights, RMS; NDI-style jitter run |
| #7 | Scaling 20:1–1000:1 | Scaling block | Command-vs-motion ratio at 20:1, 100:1, 1000:1 |
| #8 | Workspace at least 5 mm cube | Follower mechanics | Micrometer travel |
| #9–10 | Tool at most 100 um at 20:1, 25 um at 100:1 | Error budget hand/S plus stage | Scaled-hand follow error at 20:1 and 100:1 |
| #11 | Repeatability at most 10 um, 10 approaches | Stage plus filter steady-state | 10 approaches, spread |
| #12–13 | Tremor at least 20 dB at 6–12 Hz, deliberate at most 3 dB below 1 Hz | Kalman/tremor filter | Sine sweep 6–12 Hz plus 0.5/1 Hz, dB in/out |
| #14–15 | Latency at most 20 ms filter-off / 100 ms filter-on | Pipeline TL+Tsolv budget | Hand-onset to tool-onset timing, filter on/off |
| #16 | Pose at least 100 Hz | Full-FPGA pipeline | Timed pose loop, moving-sensor case |
| #17 | Stop within 100 ms | Watchdog + engage/stop | Stop command and tracking-loss to halt timing |
| #18 | View at least 50x | Camera/display | Stage-micrometer on-screen calibration |
| #19–20 | Pen at most 50 g, field at most 27 uT | Pen mechanics + generator drive | Scale; AC field probe in volume |
| #21–25 | Power / cost / environment | PSU + BOM + lab procedure | Outlet tolerance, BOM within 1000 CAD/pair, temp/RH log |

Anser-vs-Phase-1 verdicts for context: hand NDI 0.82/1.14/1.98 mm lower-two-thirds pass, bespoke C 2.48 mm fails max; orientation 0.04/0.09 deg passes by ~10x; jitter 0.13/0.15/0.29 mm maps to 1.5 um tool at 100:1, passes; tool NDI 11.4/57 um middle and 19.8/99 um top (bespoke worst 24.8/124 um) — NDI passes, bespoke fails at 20:1; pose rate 15 Hz paper / 50–72 Hz MATLAB fails (Nyquist misses tremor); tremor none (only moving average) — to implement on FPGA; latency acq 2.5–50 ms plus MaxIter-40 solver passes with filter on, tight with filter off; volume 250 mm cube heritage with aluminium cylinder causing 27 mm error validates the 150 mm metal-free rule.

Phase 1 test hooks that become Phase 2 verification: XYZ tracking test; pitch/yaw test (beat the paper's angle test); tremor sim/test; constant-current test; robot resolution test.

---

## 10. Fault / safety flow (red dashed, separate chart)

Triggers, all leading to halt within 100 ms with status reported: stop command; tracking-lost (residual gate exceeded or out-of-volume or solver gave up to initial estimate); volume excursion (halt plus alarm); excess tremor; field instability (kappa/current drift); comm-loss watchdog; metal intrusion (aluminium-cylinder 27 mm error precedent validates the rule); emergency stop. Show engage/disengage interlock (hand moves free, tool frozen). Power/environment box: 108/120/132 V at 60 Hz; operating 18–28 C; storage -10 to 40 C; RH at most 80%; BOM within 1000 CAD/pair. Bring to lab consulting: project description, block diagram, electronic schematic, and any other documentation.

---

## 11. Upstream reference inventory (so nothing is invented)

- Jaeger 2018 thesis (282 pp, UCC 2018): Ch.3 filament/sensor model and solver (Eq. 3.15–3.27, Fig.3.17–3.21, Tables 3.4–3.5); Ch.7 bespoke sensor (Eq. 7.1–7.14, Fig.7.1–7.12, Tables 7.1–7.5). Agent working crop is PDF pp.84–94 plus 199–214 with text extracts.
- Jaeger et al. 2017 paper: 1.14 mm / 0.04 deg, 8 freqs 20.5–27.5 kHz at 1 kHz spacing, closed-loop current driver.
- O'Donoghue et al. 2014: filament method plus driver detail; closed-loop driver §II load-bearing with thesis §4.3.3.
- Anser OSF snapshot node 47q8q (35 files, ~43 MB, downloaded 2026-10-13): Design Files (field-generator board, emitter coil, sensor amp, AC driver with the datasheets listed in Section 4b); P&O Code/Matlab (MatlabCode.zip, 30 files, plus next-rev pointer to a GitHub AnserEMT repo, unverified); System Manual (Manual.pdf, 23 pp, 2017 — start here for bring-up).
- MATLAB golden (30 files): setup/sensor/calibration/run scripts plus DAQ, model, user/system, user/tracking, user/calibration, user/objective, IGTLink API folders with the port map in Section 7.8. Host visualization via OpenIGTLink to CustusX/3DSlicer; transform name example `ProbeToTracker`.
- Python framework (NOT fetched — draw as an external box, do not invent): openemt.org modules daq.py / filter.py / model.py / solver.py plus pyIGTLink.py; sibling repos python-anser / qt-anser / Matlab-Anser.
- Simulations: field/Jacobian script porting the two geometry/field functions with the constants in Section 4a.
- Phase 2 component files: ADC justification (RQ-A1–A7 plus §9 sigma-delta lock); ADC BOM (AD7768-4 primary, ADS1274 backup, ADR434BRZ ref, ~$122.31); pen-analog BOM (connectors + cable, ~$67.96); connector/cable requirements and weighted alternatives (IO locked, Amphenol alt, W2697 locked, W2893 static-only); datasheets on file: ADS1274, AD7768 summary, IO-TXLR3-F and IO-TXLR3-M-PS-1 drawings, Mogami catalog/tech plus W2697 photo/spec.

---

## 12. Open decisions / traps (show as diamonds or notes, do not resolve silently)

- FPGA part and HDL partitioning not frozen — leave a generic "FPGA (TBD)" box.
- Final field-generator placement plus drive current (ICNIRP 27 uT check pending sim).
- Final ADC part pending the §9e vetting gate (simultaneous sigma-delta locked, SAR fallback documented, single/muxed/32 kSPS rejected).
- Final pen coil (A–E plus air/ferrite) pending kappa-grid plus jitter measurement; assume bespoke worse than NDI until measured.
- Dipole model invalid near large/planar coils — always draw filament (3.17), never (3.15).
- Never put the pose solver on PC/MATLAB in the chart (stale Phase 1); host is logging/calibration/visualization only.
- Never edit vendor snapshots or frozen reference PDFs; regenerate extracts with document tools, do not hand-edit outputs.
- Single-channel or multiplexed ADC variants reintroduce mux-skew and crosstalk verbatim and do NOT qualify as fallback; only simultaneous parts count.
- `TolX = 1e-6` is an optimizer step (1 um), not system resolution.
- Metal within 150 mm invalidates all accuracy claims; ferrite gain is not free accuracy (linearity/noise tradeoff).

---

## 13. Author checklist

- [ ] L0 plus L1 plus per-system L2 plus FPGA/calibration/fault L3 drawn, flows labeled with level/rate/format where given above.
- [ ] Equation citations on model/solver/sensor blocks: (3.17)–(3.18), (3.19)–(3.25), (3.26)–(3.27), (7.1)–(7.9), (7.10)–(7.11).
- [ ] Locked part numbers on connector/cable/ADC blocks; vendor archive names on reference blocks; solver options/bounds/retry on solver blocks.
- [ ] Specs #1–25 each trace to at least one block plus at least one test idea; default-conditions box on every chart.
- [ ] 5-DOF no-roll, 150 mm metal rule, kappa-before-accuracy order, integer-J lock, 60–70 dB spur budget, TL+Tsolv under 10 ms all visible.
- [ ] Rejected paths shown once with one-line kill reason: dipole model, XADC in signal path, PC solver, muxed/single-channel or 32 kSPS ADC, foil-shield whip, oversize cable on the pen.
- [ ] Owners plus Phase 3 hooks (integration to Feb 15 prototype to Mar 22 demo) noted for caption and schedule figure.
- [ ] No external file or folder access assumed; this document alone plus drawing tools suffices.
