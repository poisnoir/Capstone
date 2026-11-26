# Phase 2 — DRV-2 driver + power requirements

**Status:** **DRV-2 requirements gate ACCEPTED 2026-10-27.** Driver topology A
(LMH6321-class, single +15 V AC-coupled) is LOCKED. Power C1 + medical-grade
(one external 15 V/60 W adapter + on-board DC-DC/LDO tree) is LOCKED; the
on-board tree is the v2 tree locked by decision #31 (2026-11-25).
Current-sense A+ (summed Ch0 + individual peak/fault taps) is LOCKED.
DAC/filter is LOCKED: **M16 — 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8×
LTC1563-2 (4th-order, 60 kHz)**; DAC update 199.805 kSPS, SPI 49.152 MHz. Enclosure is LOCKED:
one box with an internal shield partition. STOP is **arm-motion only** (#30):
NC mushroom button, no K1/K2, field rail `+15V_FUSED` unswitched; field, DDS/DAC
and pose continue. A genuine FPGA/ADC/driver fault is the separate tracker-side
safe state.
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
  DC-DC/LDO tree (v2, decision #31).** +15 V driver rail; on-board +6 V,
  +5V_EXC, +5VA, +3.3 V/+1V0_FPGA/+1V8_FPGA and ±12VA. Exact parts are locked
  per #31 (see §3); the +15 V driver swing is unchanged (#8).
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
- **LOCKED: STOP is arm-motion only (decision #30)** — normally-closed mushroom
  button; **no K1/K2** and the `+15V_FUSED` field rail is **unswitched**. Field,
  DDS/DAC and pose continue; only arm motion stops (≤100 ms). The FPGA gets an
  opto-isolated STOP status. A genuine FPGA/ADC/driver fault triggers the
  separate tracker-side safe state, not the arm STOP.

---

## 1. Requirements

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| DRV-01 | Excitation: **FPGA DDS on Artix-7 XC7A35T PL (PS-less, BRD-01) + M16 DAC/filter: 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8× LTC1563-2 (4th-order, 60 kHz); XADC not used; DAC update 199.805 kSPS; SPI 49.152 MHz, 8×24-bit + TRIGGER frame = 216 bits, software LDAC**; amplitude/phase control | `tone_plan.md`; AGENTS; `simulations/m16/FINAL_REPORT.md` | LOCKED (M16 selected 2026-10-27) | 8-tone FFT + phase; filter/image/EVM |
| DRV-02 | Output: 250 mA nominal / 500 mA max; **150 mA prototype first**; programmable 150–500 mA; load 70 µH + 2 Ω; 34 kHz \(\lvert Z\rvert\approx15.1\ \Omega\); 250 mA → 3.8 V RMS / 5.3 V peak; 500 mA peak → 7.55 V peak (rail limit); 20–34 kHz | Thesis §4.2–4.3; `tone_plan.md`; thermal note | PROPOSED; 150 mA first | Load-step test |
| DRV-03 | Constant-current: loop phase margin ≥45° at 34 kHz; output impedance high; current error ≤0.1%; drift ≤0.1% over 18–28 °C; no DC current in the coil | Thesis §4.3.3; O'Donoghue §II | PROPOSED | Step/load response; current log |
| DRV-04 | Distortion: THD ≤−60 dBc at 250 mA; all-tone IMD below the spur budget; channel crosstalk ≤−60 dB; noise | Docs spur budget; `tone_plan.md` IMD note | PROPOSED | Sense-resistor FFT + 8-tone IMD |
| DRV-05 | Power: **C1 + medical-grade locked; on-board tree v2 locked (#31)** — one external 15 V/60 W-class medical-grade adapter; +15 V driver rail, +6 V, +5V_EXC, +5VA, +3.3 V/+1V0_FPGA/+1V8_FPGA, ±12VA; no on-board mains stage | §3; #31 | LOCKED | Rail noise/load test |
| DRV-06 | Thermal: 8 channels at 250 mA; coil \(I^2R\) ≈0.125 W/coil, sense ≈0.06 W each, LMH6321 dissipation; no 3 kg heatsink; ~180 cm² board | Thesis §4.3; measured R/L | PROPOSED | Thermal soak |
| DRV-07 | Protection: overcurrent, overtemp; **arm-motion STOP ≤100 ms** (field/DDS/DAC/pose continue, #30); AC coupling prevents DC coil current; genuine FPGA/ADC/driver fault → separate tracker-side safe state | Phase 1 #17; thesis §4.3.1; #30 | PROPOSED | Fault injection |
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
DC-DC/LDO tree (v2, decision #31, 2026-11-25).** Use a modern medical-grade
15 V/60 W-class adapter; the on-board tree is the v2 tree in
`docs/phase2/power_tree_v2.md`, which decision #31 adopts, superseding the #20
part list.

> **Rail tree (#31, LOCKED 2026-11-25):** **+6 V** from TPSM63604;
> **+5V_EXC** for DAC80508 + 8× LTC1563-2; **+5VA** for AD7768-4 + 2× ADA4940-2;
> **+3.3 V / +1V0_FPGA / +1V8_FPGA**; **±12VA** from MGJ2D151515SC → LT3045-1 /
> LT3093. **OKI-78SR-5 and TPS7A2033 are removed** (the `+5 V` net no longer
> exists). The thesis ME60/PTN78000AAH/TPS7A33/47 chain is historical reference
> only. The +15 V driver swing (decision #8, single +15 V AC-coupled) is unchanged.

**No on-board mains stage.** The 108/120/132 V 60 Hz wall is handled by the
external 15 V adapter; the board does not implement a mains rectifier,
transformer, or isolation. The adapter is the mains safety/EMC boundary. The
board's power stage is only the low-voltage DC-DC/LDO tree: 15 V DC input →
+6 V buck pre-rail and ±12VA, with the +15 V pass-through for the LMH6321. This
is the thesis ME60 approach and avoids a from-scratch 110 V design (creepage,
isolation, EMC, safety testing, board size). The board input still needs a fuse,
common-mode choke, reverse-polarity/transient protection, and a hardware disable.

**What is actually switched on-board:**

- **+15 V is not converted.** It comes from the adapter and feeds the LMH6321
  current buffer directly (driver swing unchanged, #8).
- **+6 V is generated from +15 V** by U147 TPSM63604 (synced to `BUCK_SYNC`);
  it feeds the +1V0_FPGA/+1V8_FPGA/+3.3 V bucks and the two 5 V LDOs.
- **±12VA is generated by U5 MGJ2D151515SC** → U6 LT3045-1 / U2 LT3093 for the
  analog stages (replaces RV-1515D + TPS7A47/TPS7A33).
- **+5V_EXC (U149 TPS7A4701) and +5VA (U146 TPS7A4701)** feed the DAC80508 +
  8× LTC1563-2 and the AD7768-4 + 2× ADA4940-2 respectively; the `+5 V` net is
  removed. OKI-78SR-5 and TPS7A2033 are gone.
- The external adapter switches 120 V AC → 15 V DC; the board switches 15 V DC
  → +6 V and ±12VA. The two stages are different.

**Why switching instead of linear:** 15 V → 5 V at 1 A dissipates 10 W in a
linear pass element; 15 V → 3.3 V at 1 A dissipates 11.7 W. A buck is much more
efficient; the LDO after it removes the switching ripple. A negative rail cannot
be made with a positive linear regulator at all.

**If on-board switcher EMI is a concern:** *(v1-era option, not adopted)* a
**±15 V/5 V medical-grade multi-output adapter** (C2) or a second −15 V adapter would move the −15 V/+5 V
conversion outside the box; the board would only LDO/filter. That is a power-tree
change from C1; trade size/cost/availability.

| Rail | Load | Note |
|---|---|---|
| +15 V | LMH6321 current buffer (8 ch) | 250 mA nominal; 5.3 V peak at 34 kHz; 60 W adapter; driver swing unchanged (#8) |
| +6 V | Pre-rail for all on-board rails | TPSM63604 from +15 V, synced to `BUCK_SYNC` |
| ±12VA | INA163/ADA4940/ADA4896 analog | MGJ2D151515SC → LT3045-1 / LT3093 |
| +5V_EXC | DAC80508 + 8× LTC1563-2 | TPS7A4701 from +6 V |
| +5VA | AD7768 AVDD1/AVDD2, ADA4940-2 | TPS7A4701 from +6 V; AD7768 AVDD1 5 V; AVDD2 2.25–5 V |
| +3.3 V | AD7768 IOVDD, FPGA/digital | TPS62130A from +6 V; AD7768 IOVDD 2.5–3.3 V |
| +1V0_FPGA / +1V8_FPGA | FPGA core / aux | TPS62130A from +6 V |

- One wall adapter, one enclosure; no bench supply in the final build.
- **Isolation grade LOCKED: medical-grade isolated adapter** — ME60A1503F01
  (decision #20, retained by #31); the thesis ME60 class is the reference.
  The pen is handheld; medical-grade is required for the operator safety/leakage
  case. Verify IEC 60601-class isolation.
- **FPGA rail scope (v2, #31):** the PSU provides +3.3 V, +1V0_FPGA and
  +1V8_FPGA from +6 V; no added rail is needed.
- Add input common-mode choke, CLC filtering, fusing, reverse-polarity
  protection, and a hardware disable reserved for genuine driver faults; STOP
  is arm-motion only (#30) — it must not remove coil current or interrupt
  `+15V_FUSED`; the arm halt is ≤100 ms.
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
  switching, but the on-board +6 V/+3.3 V/+1V0/+1V8 bucks and ±12VA converter
  still switch inside (v2, #31).
  The LMH6321 is linear; the 8×250 mA 20–34 kHz current loops and FG cables are
  the intentional field, not EMI. Use a shielded partition/star ground/LDO analog
  rails/15 V input CMC; test the thermal/EMI. A two-box split is a fallback only
  if the EMI test fails and a deviation is approved.
  **Switcher placement:** keep U5 MGJ2D151515SC away from the pen connector and
  the INA163 inputs, and check its switching spur on the bench; place the +6 V
  module and FPGA bucks at the power/driver end of the board. The digital clocks
  are the other inside source. See `docs/phase2/power_tree_v2.md` §6.
- **STOP is arm-motion only (decision #30):** normally-closed mushroom button,
  no K1/K2, `+15V_FUSED` unswitched; field, DDS/DAC and pose continue, only the
  arm halts (≤100 ms). FPGA gets opto-isolated STOP status. A genuine
  FPGA/ADC/driver fault is the separate tracker-side safe state.
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
- +15 V driver swing and the v2 on-board rails (#31), protection/disable, DAC interface.
