# Phase 2 — DRV-2 driver + power requirements

**Status:** **DRV-2 requirements gate ACCEPTED 2026-10-27.** Driver topology A
(LMH6321-class, single +15 V AC-coupled) is LOCKED. Power C1 + medical-grade
(one external 15 V/60 W adapter + on-board DC-DC/LDO tree) is LOCKED.
Current-sense A+ (summed Ch0 + individual peak/fault taps) is LOCKED.
DAC/filter is LOCKED: **M16 — 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8×
LTC1563-2 (4th-order, 60 kHz)**; DAC update 199.805 kSPS, SPI 49.152 MHz. Enclosure is LOCKED:
one box with an internal shield partition. Hardware E-stop is LOCKED: NC
mushroom button in the driver enable chain, independent of the FPGA.
**Current: 150 mA prototype first; 250 mA fallback; 500 mA max; programmable
150–500 mA.** BOM/schematic/test details remain open at the BOM pass.

**Sources:** `HAJ_Thesis_2018.pdf` §4.2–4.3 (original vs optimised driver),
§4.7 (power delivery), §4.8 (field generator); `docs/phase2/design_order.md` DRV-2;
`docs/phase2/tone_plan.md`; `docs/phase2/anser-baseline-findings.md`;
`software/anser-matlab-ref/fSysSetup.m` (`R_store`, `I_summer_scale`).

**Decision summary:**

- **LOCKED: A — LMH6321-class optimised driver architecture.** Single +15 V
  rail, AC-coupled, 100 µF coupling, 250 mA nominal / 500 mA max, ~180 cm²
  board. **New board based on thesis §4.3, not a clone.** The LMH6321 is the
  baseline current buffer; if lifecycle/availability/thermal requires a
  comparable buffer or different passives, that is allowed with a recorded
  deviation and a re-check of current, loop, and thermal. The vendor Rev A
  discrete class-AB board is reference/fallback only.
- **LOCKED: C1 — one external medical-grade 15 V/60 W-class adapter + on-board
  DC-DC/LDO tree.** +15 V, −15 V, +5 V, +3.3 V; +1.8 V only if the FPGA board
  needs it. Exact parts are BOM decisions. The FPGA board regulates its own
  core from +5 V/+3.3 V unless the final board requires an added rail.
- **LOCKED: A+ — current-sense.** Per-coil \(R_{store}\) + analog summer to
  AD7768 Ch0 for \(Y_I\); individual per-coil peak/overcurrent comparators for
  fault detection. No mux, no second ADC. Keep the thesis \(R_{store}\) values
  and summer scale 2.0103 as the baseline; allow modern current-sense amps/
  passives with calibration.
- **LOCKED: DAC/filter = M16** — 1× DAC80508 (16-bit, 8 ch, 200 kSPS, SPI)
  + 8× LTC1563-2 (4th-order, 60 kHz); the Artix-7 has no ADC and none is used
  for the drive. DAC update 199.805 kSPS (32.768 MHz ÷164); SPI 49.152 MHz,
  8×24-bit = 192 bits + 24-bit TRIGGER = 216 bits (4.394 µs); the LDAC is a
  software trigger (TRIGGER 0x05 bit 4) — the part has no LDAC pin.
- **LOCKED: enclosure** — one box with an internal shield partition between the
  driver/DC-DC section and the FE/ADC. Star ground, LDO analog rails, 15 V input
  CMC/CLC; thermal/EMI test. Two-box split is a fallback only if the EMI test
  fails and a deviation is approved.
- **LOCKED: hardware E-stop** — normally-closed mushroom button in the driver
  enable chain, independent of the FPGA. It cuts the +15 V driver/load-switch
  enable; the FPGA gets an opto-isolated status and runs a separate software
  watchdog. The follower stop remains ≤100 ms.

---

## 1. Requirements

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| DRV-01 | Excitation: **FPGA DDS on Artix-7 XC7A35T PL (PS-less, BRD-01) + M16 DAC/filter: 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8× LTC1563-2 (4th-order, 60 kHz); XADC not used; DAC update 199.805 kSPS; SPI 49.152 MHz, 8×24-bit + TRIGGER frame = 216 bits, software LDAC**; amplitude/phase control | `tone_plan.md`; AGENTS; `simulations/m16/FINAL_REPORT.md` | LOCKED (M16 selected 2026-10-27) | 8-tone FFT + phase; filter/image/EVM |
| DRV-02 | Output: 250 mA nominal / 500 mA max; **150 mA prototype first**; programmable 150–500 mA; load 70 µH + 2 Ω; 34 kHz \(\lvert Z\rvert\approx15.1\ \Omega\); 250 mA → 3.8 V RMS / 5.3 V peak; 500 mA peak → 7.55 V peak (rail limit); 20–34 kHz | Thesis §4.2–4.3; `tone_plan.md`; thermal note | PROPOSED; 150 mA first | Load-step test |
| DRV-03 | Constant-current: loop phase margin ≥45° at 34 kHz; output impedance high; current error ≤0.1%; drift ≤0.1% over 18–28 °C; no DC current in the coil | Thesis §4.3.3; O'Donoghue §II | PROPOSED | Step/load response; current log |
| DRV-04 | Distortion: THD ≤−60 dBc at 250 mA; all-tone IMD below the spur budget; channel crosstalk ≤−60 dB; noise | Docs spur budget; `tone_plan.md` IMD note | PROPOSED | Sense-resistor FFT + 8-tone IMD |
| DRV-05 | Power: **C1 + medical-grade locked** — one external 15 V/60 W-class medical-grade adapter + on-board DC-DC/LDO tree; +15 V, −15 V, +5 V, +3.3 V; no on-board mains stage | §3 | LOCKED | Rail noise/load test |
| DRV-06 | Thermal: 8 channels at 250 mA; coil \(I^2R\) ≈0.125 W/coil, sense ≈0.06 W each, LMH6321 dissipation; no 3 kg heatsink; ~180 cm² board | Thesis §4.3; measured R/L | PROPOSED | Thermal soak |
| DRV-07 | Protection: overcurrent, overtemp, disable, fault, stop ≤100 ms; AC coupling prevents DC coil current | Phase 1 #17; thesis §4.3.1 | PROPOSED | Fault injection |
| DRV-08 | Current-sense: \(R_{store}\) per coil, summer scale 2.0103, V/I transfer, bandwidth ≥34 kHz, phase, common-mode, ADC Ch0 | `fSysSetup.m` | PROPOSED | Known-current injection |
| DRV-09 | Test: constant-current step/load, THD/IMD, thermal, fault/disable | Phase 1 test plan | PROPOSED | Test report |

---

## 2. Driver decision

**LOCKED: A — LMH6321-class thesis §4.3 architecture; new board, parts open.**

| Item | Vendor Rev A (old) | New board (LOCKED A) |
|---|---|---|
| Output stage | Discrete class-AB (D44/D45) | LMH6321-class integrated buffer; alternate allowed with deviation |
| Rails | ±15 V | +15 V single rail, AC-coupled |
| Current | 250 mA nominal / 500 mA max | 250 mA nominal / 500 mA max |
| Quiescent/heat | ~30 W, 3 kg heatsink | ~180 cm² board, lower quiescent |
| Coupling | DC | 100 µF AC coupling |
| Status | Reference/fallback | **LOCKED architecture; parts open** |

- The vendor Rev A board is the original 2013 discrete design; it is not the
  optimised thesis design. Cloning it would inherit the 30 W/3 kg thermal
  problem.
- The LMH6321 is limited to 300 mA (500 mA with the current limit disabled);
  treat 500 mA as max/short-term. The 250 mA nominal is the design point.
- At 34 kHz the load is 15.1 Ω; 250 mA gives 5.3 V peak, within the 7.5 V
  single-rail swing. 500 mA peak is at the rail limit; do not run continuous
  500 mA at 34 kHz.
- The thesis phase-lead compensation was tuned for 20–30 kHz; re-check the loop
  at 34 kHz with the real coil and mutual coupling.

---

## 3. Power delivery

**LOCKED: C1 — one external medical-grade 15 V/60 W adapter + on-board
DC-DC/LDO tree.** Use a modern medical-grade 15 V/60 W-class adapter plus an
on-board DC-DC/LDO tree; outputs +15 V, −15 V, +5 V, +3.3 V (and +1.8 V only if
the FPGA board needs it). Exact adapter/DC-DC/LDO parts are BOM decisions; the
thesis ME60/PTN78000AAH/TPS7A33/47 chain is the reference.

**No on-board mains stage.** The 108/120/132 V 60 Hz wall is handled by the
external 15 V adapter; the board does not implement a mains rectifier,
transformer, or isolation. The adapter is the mains safety/EMC boundary. The
board's power stage is only the low-voltage DC-DC/LDO tree: 15 V DC input →
inverting −15 V, +5 V, +3.3 V, and the +15 V pass-through for the LMH6321. This
is the thesis ME60 approach and avoids a from-scratch 110 V design (creepage,
isolation, EMC, safety testing, board size). The board input still needs a fuse,
common-mode choke, reverse-polarity/transient protection, and a hardware disable.

**What is actually switched on-board:**

- **+15 V is not converted.** It comes from the adapter and feeds the LMH6321
  current buffer directly.
- **−15 V is generated from +15 V** for the bipolar INA163/ADA4940/ADA4896
  analog stages. A linear regulator cannot invert, so an inverting switching
  converter (PTN78000AAH or modern equivalent) makes −15 V, followed by a
  low-noise LDO (TPS7A33).
- **+5 V/+3.3 V are generated from +15 V** for the AD7768/FPGA. A buck is used
  if the current is high; an LDO after it cleans the rail. If only the ADC is
  powered (tens of mA), linear LDOs from +15 V are also possible.
- The external adapter switches 120 V AC → 15 V DC; the board switches 15 V DC
  → −15 V/+5 V/+3.3 V. The two stages are different.

**Why switching instead of linear:** 15 V → 5 V at 1 A dissipates 10 W in a
linear pass element; 15 V → 3.3 V at 1 A dissipates 11.7 W. A buck is much more
efficient; the LDO after it removes the switching ripple. A negative rail cannot
be made with a positive linear regulator at all.

**If on-board switcher EMI is a concern:** a **±15 V/5 V medical-grade
multi-output adapter** (C2) or a second −15 V adapter would move the −15 V/+5 V
conversion outside the box; the board would only LDO/filter. That is a power-tree
change from C1; trade size/cost/availability.

| Rail | Load | Note |
|---|---|---|
| +15 V | LMH6321 current buffer (8 ch), analog | 250 mA nominal; 5.3 V peak at 34 kHz; 60 W adapter |
| −15 V | INA163/ADA4940/ADA4896 analog | Low current; inverting DC-DC + LDO |
| +5 V | AD7768 AVDD1/AVDD2, FPGA input | AD7768 AVDD1 5 V; AVDD2 2.25–5 V |
| +3.3 V | AD7768 IOVDD, FPGA/digital | AD7768 IOVDD 2.5–3.3 V |
| +1.8 V | FPGA core if needed | Use the FPGA board regulator or add a rail |

- One wall adapter, one enclosure; no bench supply in the final build.
- **Isolation grade LOCKED: medical-grade isolated adapter** (thesis ME60 class).
  The pen is handheld; medical-grade is required for the operator safety/leakage
  case. Exact part is a BOM decision; verify IEC 60601-class isolation.
- **FPGA rail scope DEFAULT:** the PSU provides +5 V/+3.3 V and the FPGA board
  derives its core rails; add +1.8 V (or another rail) only if the final FPGA
  board requires it.
- Add input common-mode choke, CLC filtering, fusing, reverse-polarity
  protection, and a hardware disable for the driver; the stop path must remove
  coil current within 100 ms.
- The 60 W adapter covers eight channels at 250 mA plus analog/digital
  housekeeping; verify inrush and thermal.

---

## 4. Current-sense / back-channel

**LOCKED: A+ — per-coil \(R_{store}\) + analog summer → AD7768 Ch0, plus
individual per-coil peak/overcurrent comparators for fault detection.** No mux,
no second ADC. The per-coil current-sense resistors also close the LMH6321
constant-current loop; the summer is the separate \(Y_I\) path to Ch0.

**How the thesis calibrates without an extra ADC:** the eight coils are
frequency-multiplexed. The single summed current-sense channel contains eight
tones; the DFT/Goertzel extracts each coil's current amplitude and phase at its
own tone. The per-coil \(R_{store}\) values and `I_summer_scale = 2.0103` correct
the different current-to-voltage gains. Calibration is a one-time fit:

- Helmholtz: \(A_{sens}(f)=V/B\) for the pen+amp, using the known Helmholtz
  constant and current.
- 7×7 grid at 85.6/152 mm: known positions → `BStore` (49×8 per plane); the
  model uses \(I_{out}/R_{store}\); fit per-coil `BScale` (κ) and `zOffset`.
  The κ absorbs the current/sensor scaling.
- The per-coil \(I_{out}\) vector is stored/measured once (`fSysSetup.m` loads
  `data/I_store.mat`); the closed-loop driver keeps it stable, so the runtime
  does not need eight current ADCs.

At runtime `fSysGetField.m` uses the current-sense **phase** per tone to set the
field sign and the sensor amplitude/`Asens` for the field; the golden model uses
the stored \(I_{out}/R_{store}\) and κ. The current-sense amplitude per tone is
available from the same channel but is not used in the golden `BField` path. The
new FPGA can use the live per-tone amplitude from Ch0 instead of the stored
\(I_{out}\), which improves drift without an extra ADC. A+ adds individual
per-coil peak/overcurrent comparators for fault detection; it does not add
individual phase/current logging.

- Per-coil \(R_{store}\) from `fSysSetup.m`: 1.239, 1.02, 0.957, 0.995, 1.183,
  0.983, 0.991, 0.989 Ω.
- Summer scale `I_summer_scale = 2.0103`; the current-sense output goes to ADC
  Ch0 (pseudo-differential).
- At 250 mA the sense voltage is 0.24–0.31 V; the summer/ADC scaling must keep
  it within the AD7768 pseudo-differential range and preserve phase to 34 kHz.
- Verify the V/I transfer, bandwidth, phase, and common-mode with a known
  current; the current-sense is the phase reference \(Y_I\), so its phase error
  directly biases orientation.
- The current-sense channel is stationary; it does not see the pen motion.

---

## 5. DAC / excitation — M16 selected

**LOCKED: M16 — 1× DAC80508 (16-bit, 8 channels, 200 kSPS, SPI) + 8×
LTC1563-2 (4th-order Butterworth, 60 kHz, one resistor per channel).** DAC update
**199.805 kSPS** = 32.768 MHz ÷164; SPI **49.152 MHz**, 8×24-bit + 24-bit TRIGGER
= **216 bits = 4.394 µs**. LDAC is a software trigger (TRIGGER 0x05 bit 4); the part
has no LDAC pin.
The Artix-7 has no hard ADC; none is used for the drive.

**Artix-7 resource note:** the XC7A35T is the baseline (33k LC, 90 DSP, 50 BRAM36). The full
8-channel DDS + AD7768 capture + Goertzel + filament/LM solver is estimated at <20k LUT and
<20 BRAM36, so the 35T has margin; the XC7A50T in the same FTG256 footprint is the escape.
This is a DIG-6 synthesis gate, not an open part choice.

| Option | What it is | Verdict |
|---|---|---|
| **A — M16 (selected)** | 1× 8-channel 16-bit DAC80508 + 8× LTC1563-2 4th-order 60 kHz | **SELECTED 2026-10-27** |
| B — 8 single DACs | One 16-bit DAC per coil, separate SPI/parallel lanes | Alternate; ~$150 more, simpler filter |
| C — FPGA PWM + RC | 8 PWM channels + analog reconstruction | Rejected: carrier/EMI, linearity |
| D — one high-speed DAC + 8 bandpass filters | Sum all tones, split per coil | Rejected: lossy/phase-critical filters |

**Requirements (M16):** 8 independent outputs; 16-bit; DAC update 199.805 kSPS;
SPI 49.152 MHz; 4th-order 60 kHz filter; image −35.3 dB at 165.8 kHz; 8-tone
EVM ≤−60 dBc; output 0–5 V into the LMH6321 loop. SPICE screen:
`simulations/m16/FINAL_REPORT.md`.

## 6. Open items

- **Thermal reality:** 8×250 mA linear from +15 V is roughly 12–16 W in the
  LMH6321 output stages (the old discrete design was ~30 W/3 kg). The series cap
  **alone at +15 V does not reduce this** — lowering the load voltage increases
  the pass-device drop. The thermal fix is a lower driver rail (+5 V) plus the
  series cap (~4 W for 8×250 mA), and/or 150 mA nominal (the B air + INA163
  link budget still passes 200/B at 150 mA: ~5.3 pT vs ~6.6 pT required), plus a
  heatsink/fan and the one-box thermal soak. The 500 mA max at 34 kHz still
  needs the higher rail (~7.5 V cap/coil), so a +5 V nominal / +15 V max
  arrangement must be checked.
- **Series tuning capacitor option (not locked):** a series cap per coil at its
  tone cancels the coil reactance, reducing the driver voltage/reactive power
  (e.g. 3.8 V → 0.5 V at 250 mA/34 kHz; C 0.31–0.9 µF), but **not** the coil
  current. Risks: LMH6321 loop stability, L/C/mutual-coupling tolerance,
  capacitor voltage/current/reliability, start-up/fault, and the existing 100 µF
  AC coupling. Prototype one channel and decide after the test; do not lock yet.
- **M16 bench** (DRV-01): the SPICE screen is done; bench the DAC80508 SPI/LDAC,
  the LTC1563-2 image/phase, the 8-tone EVM, and the loop PM/step. The 8× AD5541A
  is the alternate if the M16 bench fails.
- **Enclosure/EMI LOCKED: one box with an internal shield partition** between
  the driver/DC-DC section and the FE/ADC. The external adapter removes the mains
  switching, but the on-board −15 V/+5 V/+3.3 V converters still switch inside.
  The LMH6321 is linear; the 8×250 mA 20–34 kHz current loops and FG cables are
  the intentional field, not EMI. Use a shielded partition/star ground/LDO analog
  rails/15 V input CMC; test the thermal/EMI. A two-box split is a fallback only
  if the EMI test fails and a deviation is approved.
  **The −15 V rail is the least aggressive switcher:** it powers only the
  low-current analog (tens of mA), and its ~440 kHz switching is far above the
  20–34 kHz signal; a shielded inductor, small switching loop, LDO + pi filter
  make it manageable. The bigger inside sources are the +5 V/+3.3 V/FPGA
  regulators and the digital clocks, not the −15 V rail.
- **Hardware E-stop LOCKED:** normally-closed mushroom button in the driver
  enable chain, independent of the FPGA; it cuts the +15 V driver/load-switch
  enable. The FPGA gets an opto-isolated status and runs a separate software
  watchdog. The follower stop remains ≤100 ms.
- **LMH6321 availability**: if the part is obsolete/unavailable, use the
  vendor Rev A discrete stage as a fallback, or a comparable high-current
  buffer; re-check the thermal/loop.
- **Power adapter**: confirm the ME60 or an equivalent 60 W medical-grade 15 V
  supply is in stock and within the ≤1000 CAD/pair budget.
- **Thermal**: measure the LMH6321/board temperature at 8×250 mA; the 180 cm²
  board is the thesis estimate, not a tested enclosure.
- **All-tone IMD**: with 2 kHz spacing, 3rd-order products fall on tone bins;
  the driver linearity is load-bearing. Measure 8-tone IMD, not just THD.

---

## 7. Exit gate

**Accepted at requirements level 2026-10-27.** The tests below are the
BOM/prototype gate; exact adapter/passives are BOM items; the M16 DAC/filter is selected. See
`contract/decisions_log.md`.

- One channel constant-current verified before any accuracy claim.
- THD/IMD, thermal, fault/disable, current-sense V/I/phase measured.
- Schematic/BOM signed; DAC part selected; power adapter/rails verified.
- If the driver cannot deliver the FG-03 current/compliance, return to FG-1;
  do not silently reduce current and leave PEN-3 based on the old field.

---

## 8. Deferred to schematic/BOM

The DRV-2 requirements pass freezes the **block-level architecture and critical
values**; it does not require every small part. The following can be decided in
the schematic/BOM pass after the order is complete:

- Exact passives, footprints, connectors, test points, decoupling values.
- Heatsink/enclosure mechanical details (the thermal requirement stays).
- PCB layout/stackup/assembly.
- BOM pricing/sourcing for non-critical parts.

Still required before build/sign-off (not deferred):

- LMH6321, 250 mA nominal / 500 mA max, 100 µF AC coupling.
- \(R_{store}\) values and summer scale; current-sense V/I/phase.
- Compensation topology / phase margin at 34 kHz.
- +15 V/±15 V rails, protection/disable, DAC interface.
