# Phase 2 — System contract (SC-0)

**Canonical location:** `contract/` · **Version:** 1.0.0 · **Tag:** `contract-v1.0.0`
**Change process:** `contract/README.md` — do not edit without a contract-change PR.

**Status:** draft for team sign-off, 2026-10-27. Technical items SC-01…SC-05 are
locked. **D1-B, D3-A, and D4 were approved by the team on 2026-10-27. FE-4 is
locked to INA163 + ADA4940-2.** FG-1 may proceed.

**Sources:** `docs/phase2/design_order.md`; `docs/phase2/tone_plan.md`;
`docs/phase2/adc_justification.md`; `hardware/bom/BOM_ADC-01.xlsx`; AD7768/AD7768-4 Rev.D
datasheet (`docs/ad7768-ad7768-4.pdf`); `HAJ_Thesis_2018.pdf` §4.7–4.8; Phase 1
specs #1–25; `simulations/field_jacobian.py`.

**Status tags:** `LOCKED` = source-backed, do not reopen without a written
deviation; `PROPOSED` = needs approval/test; `OPEN` = team decision required.

---

## 1. Locked technical contract

| ID | Contract | Source | Status |
|---|---|---|---|
| SC-01a | Coordinate frame: origin at the geometric centre of the FG PCB, \(z=0\) on the board top surface, \(+z\) normal toward the pen, right-handed, SI units. Hand approaches from \(+z\). | Thesis §4.8 (origin at PCB centre); Phase 1 #3 | LOCKED datum; \(z_{min}=85.6\ \mathrm{mm}\) (D1-B, LOCKED) |
| SC-01b | Certified hand volume: **minimum 100 mm cube; Phase 2 design target 150 mm cube at \(z=85.6\ldots235.6\) mm (D1-B); 200 mm stretch** only if the SC-01d jitter gate passes. The final acceptable volume is the largest cube meeting SC-01d; 100 mm is the Phase 1 minimum. The Anser 250 mm volume is heritage; the 30×30 cm FG board supports the target range. | Phase 1 Table 1 (100 mm min); Anser paper pp.3,8 (250 mm heritage); first-pass FG scan; D1 decision 2026-10-27 | LOCKED minimum; 150 mm target LOCKED (D1-B); final by SC-01d; verify drawing/spec review |
| SC-01c | The working volume is the locus of the **sensor coil/tip**, not the pen housing. Jaeger sensor coils are ~12 mm long, 9–12 mm diameter; the pen body (~150 mm) and the operator's hand sit outside the volume. Only the tracked point must remain inside. The ±45° tilt is the coil orientation; the body/hand sweep outside. The ICNIRP assessment surface (D2) covers the accessible hand/body envelope, which is larger than the volume. | Jaeger Ch.7 Table 7.1; Phase 1 #3 | LOCKED interpretation; verify spec/drawing review |
| SC-01d | Volume acceptance gate: final volume = largest candidate (100/150/200 mm) with (a) ICNIRP pass at the chosen current/guard, (b) full 8×5 rank 5 and no simultaneous null over the cube and ±45°, (c) 95th-percentile CRLB position jitter ≤0.15 mm and orientation ≤0.1° at the design SNR, (d) 85.6/152 mm calibration planes inside. 100 mm minimum; **150 mm/B is the locked baseline (D1-B); 200 mm only if the gate passes**. A failure demotes to 100 mm; it does not move the bottom face without a written deviation. | Phase 1 #5–6/#11; `docs/phase2/anser-baseline-findings.md` jitter target; first-pass conditioning; D1/D4 decisions 2026-10-27 | PROPOSED test gate; baseline 150/B; verify CRLB/jitter at FG-1/INT-7 |
| SC-01e | CRLB noise requirement (first pass, common \(\sigma_B\)): at 250 mA, **150 mm/B requires \(\sigma_B\le26\) pT** (weakest-tone SNR ≥72 dB) for 0.15 mm/0.1° at the 95th percentile; 100 mm/B ≤58 pT; 200 mm/B ≤11 pT. At the 150 mA prototype, the requirements scale to **150/B ≤15.6 pT, 200/B ≤6.6 pT, 100/B ≤34.8 pT**; B air + INA163 ~5.3 pT passes 150/B ~3× and 200/B ~1.25×. PEN-3 must measure the actual per-tone \(\sigma_B\) and re-run the weighted CRLB. | CRLB scan 2026-10-27; `simulations/field_jacobian.py`; `pen_link_budget.md` | PROPOSED; verify in PEN-3 |
| SC-02 | Calibration/test planes at 85.6 mm and 152 mm above the board top; 7×7 grid = 98 points; non-metal fixture; RMS metric Eq.(7.10). | Jaeger Ch.7 §7.2.2; `docs/phase2/anser-baseline-findings.md` | LOCKED method |
| SC-03 | Tone plan: 8 tones at 20, 22, 24, 26, 28, 30, 32, 34 kHz; ODR 256 kSPS; N=512; \(J=40\ldots68\); rectangular + integer-J primary, Hamming fallback; N=1024 Hamming fallback. | `docs/phase2/tone_plan.md` (2026-10-26) | LOCKED |
| SC-04a | ICNIRP: 27 µT RMS, general public, 3 kHz–10 MHz; multi-tone linear sum \(\sum_j B_j/27\,\mu T \le 1\); 27 µT = 38.2 µT peak. Assessment surface: **any accessible point** (D2 = B). | ICNIRP 2010 Table 4, Eq.5; Phase 1 #20; D2 decision 2026-10-27 | LOCKED number/rule + surface B |
| SC-04b | ICNIRP guard: **non-metal access barrier**, not an EMF shield. Open-top ring/fence/spacer at the 27 µT contour (~57 mm above the board at 250 mA), no metal within 150 mm, plastic fasteners, removable for calibration/field mapping. It does not reduce the 150 mm working volume: with the B cube bottom at 85.6 mm, the guard is 28.6 mm below the cube. A metal box is prohibited (eddy-current distortion). Guard is a mechanical/safety BOM item, not a field-generator part. | D2 decision 2026-10-27; Phase 1 #20; 150 mm metal-free rule | LOCKED; verify field probe at accessible boundary + guard check |
| SC-05 | ADC: AD7768-4BSTZ-RL7 (2 pcs: build + spare); differential ±VREF = ±4.096 V; VCM output; precharge buffer + external RC/charge reservoirs; ADR434BRZ 4.096 V reference; MCLK ≤32.768 MHz; fast mode, decimation ×32, ODR 256 kSPS; wideband filter, group delay 34/ODR = 133 µs; DCLK/DOUT data lanes, DRDY, SYNC/START (no CONVST); SPI configuration only. | AD7768-4 datasheet; `BOM_ADC-01` | LOCKED part/contract |
| SC-05a | ADC clock jitter: design target ≤30 ps rms for the ADC's 104 dB target; minimum acceptable 1 ns rms = 73.4 dB at 34 kHz, with a written deviation if used. | \(SNR_j=-20\log(2\pi f t_j)\); RQ-A4 correction | LOCKED target |
| SC-05b | ADC digital lane rate: **4 active channels** × 32-bit frames × 256 kSPS = 32.768 Mbit/s; 4 DOUT lanes → DCLK 8.192 MHz; 2 lanes → 16.384 MHz. A 2×6 Pmod (8 I/O) is insufficient; use 2×8/custom header. | AD7768-4 datasheet; `adc_justification.md` §6; D3-A | LOCKED |
| SC-05c | Coil capacitance budget: 73 pF total at 34 kHz (cable + connector + preamp input); 56 pF cable budget. The AD7768 switched-cap network is behind the preamp and is not part of this budget. | `tone_plan.md` §6; connector Rev D | LOCKED |
| SC-06 | Channel map = **D3-A (LOCKED)**: Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference sensor; Ch2 wired but enabled when pen 2 is built | `adc_justification.md`; `fSysSetup.m`; D3 decision 2026-10-27 | LOCKED |
| SC-07 | Clock tree: one TCXO → FPGA PLL → clk_dds + MCLK_adc; single sync reset; DDS 32-bit; integer-J frames; one-time ADC START/SYNC, then count DRDY; discard the first 68 samples (266 µs) after sync. | AGENTS full-FPGA decision; `tone_plan.md` | LOCKED architecture; part TBD |
| SC-08 | Budget: \(T_{acq}=512/256\text{ k}=2.000\) ms; ADC group delay 0.133 ms; 2.133 ms total; 7.867 ms left for demod + solver + overhead at 10 ms/100 Hz; filter-off latency <20 ms, filter-on <100 ms, stop <100 ms. | `tone_plan.md` §3; Phase 1 #14–17 | LOCKED |
| SC-09 | Units/naming: RMS unless stated; dBc; T/A; mm; frame = N samples; tone frequencies in Hz; phase in degrees/radians; ICNIRP field values RMS. | Team convention | LOCKED |
| SC-10 | Change control: one owner per interface; SC-0 sign-off freezes the contract; any change requires a written deviation and re-run of affected gates. Owners follow `design_order.md` (FG/driver/front-end/ADC: Tung; DDS: Kevin; sampling/demod: William; solver: Kevin+William+Tristan; filter/scaling: Amirmohammad; PMS: Tristan/Joyal; view/log/failsafe: shared). | Phase 1 Table 8; `design_order.md` | PROPOSED |

---

## 2. First-pass FG conditioning (information for D1/D4)

`simulations/field_jacobian.py` scans 100/150/200 mm cubes at 3×3×3 positions ×
3 pitch (0°, 22.5°, 45°) × 4 azimuth (0°, 90°, 180°, 270°), equal 250 mA per
coil, full 8×5 Jacobian scaled as 0.1 m position / 1 rad angle.

| Cube | \(z\) | ICNIRP sum @250 mA | Max current for 27 µT | Condition median / 95th / max | Min singular (T/A per 0.1 m/rad) | Weakest tone |
|---|---|---|---|---|---|---|
| 100 mm | 50–150 | **31.7 µT (fail)** | 213 mA | 23.8 / 108.4 / 147.6 | 2.31e-7 | 0.21 µT |
| 100 mm | 66–166 | 21.6 µT | 312 mA | 20.1 / 75.2 / 92.5 | 1.67e-7 | 0.19 µT |
| 100 mm | 85.6–185.6 | 14.8 µT | 456 mA | 20.7 / 46.1 / 63.2 | 1.15e-7 | 0.17 µT |
| 150 mm | 66–216 | 20.7 µT | 326 mA | 29.5 / 101.1 / 122.7 | 4.84e-8 | 0.11 µT |
| **150 mm** | **85.6–235.6** | **14.8 µT** | **456 mA** | **26.5 / 69.5 / 73.1** | **3.37e-8** | **0.10 µT** |
| 200 mm | 66–266 | 20.7 µT | 326 mA | 32.4 / 288.2 / 643.9 | 1.51e-8 | 0.07 µT |
| 200 mm | 85.6–285.6 | 14.8 µT | 456 mA | 35.2 / 150.5 / 368.3 | 1.12e-8 | 0.06 µT |

Notes:

- **100 mm is the minimum** and the easy fallback. The 100 mm/85.6 cube has
  45% ICNIRP margin and the best 100 mm conditioning (95th 46 / max 63).
- **150 mm at 85.6 is the current design target.** It keeps the 45% ICNIRP
  margin, the 95th/max conditioning is 69.5/73.1 (only modestly worse than the
  100 mm cube), and the weakest tone is 0.10 µT — still above the amp floor.
  The absolute minimum singular value is 3.4× lower than the 100 mm cube, so
  the CRLB/jitter gate must confirm it.
- **150 mm at 66** is the lower-hand alternative: 20.7 µT (23% margin),
  95th/max 101.1/122.7, weakest 0.11 µT. The final gate decides if the corners
  are acceptable.
- **200 mm is a stretch, but not ruled out.** At 85.6 mm the 95th/max condition
  is 150.5/368.3; at 66 mm it is 288.2/643.9. The CRLB requires 11 pT; the
  PEN-3 link budget says B air + INA163 can deliver 5.3 pT at 20 kHz, so 200/B
  is plausible. The measured noise and conditioning decide; treat it as a
  stretch.
- `rank<5` poses are the \(\theta=0\) spherical-coordinate singularity
  (\(\phi\) undefined), not field nulls. The solver must handle it (retry or
  quaternion/rotation-vector parameterization).
- The 50–150 mm 100 mm cube fails ICNIRP at 250 mA; it needs ~213 mA, excludes
  the 152 mm calibration plane (top 150), and has the worst corners. Not a
  candidate.
- This is a first-pass 3×3×3/3×4 scan. FG-1 will refine the grid and report the
  CRLB at the target jitter; SC-01d sets the final volume.

### CRLB at the 0.15 mm / 0.1° gate

Reference per-tone field noise \(\sigma_B=1\) nT, 250 mA, same grid. The
required \(\sigma_B\) is the binding value that puts the 95th-percentile
position/orientation jitter at the target.

| Volume | 95th position @1 nT | 95th orientation @1 nT | Required \(\sigma_B\) (binding) |
|---|---|---|---|
| 100 mm/B | 1.06 mm | 1.73° | 58 pT |
| **150 mm/B** | **4.40 mm** | **3.83°** | **26 pT** |
| 150 mm/A | 3.00 mm | 2.69° | 37 pT |
| 200 mm/B | 13.90 mm | 8.68° | 11 pT |

- **150 mm/B** needs \(\sigma_B\le26\) pT at the weakest tone (SNR ≥72 dB) to
  meet 0.15 mm/0.1° at the 95th percentile. **100 mm/B** needs 58 pT; **200 mm/B**
  needs 11 pT.
- The pen/amp stage must demonstrate the actual per-tone \(\sigma_B\). A
  \(10^6\) V/T chain with 1.1 nV/√Hz over a 500 Hz bin (24.6 nV) gives ~25 pT,
  right at the 150 mm/B 26 pT requirement; the 100 mm/B 58 pT has ~2.3× margin;
  the 200 mm/B 11 pT needs ~2.4× lower noise. This is the PEN-3 trade.
- This is a common-\(\sigma_B\) first pass. PEN-3 must replace it with the
  measured per-tone \(A_{sens}(f)\) and noise, then re-run the weighted CRLB.
- 200 mm/B is not impossible, but it requires the low end of the pen/amp noise
  budget (11 pT) and the first-pass conditioning 95th 150/368. Treat it as a
  stretch, not the target.

---

## 3. Team decisions

### D1 — Tracking-volume \(z\) placement and target side

The 100 mm cube is the minimum; the design target is 150 mm, with 200 mm as a
stretch only if SC-01d passes. The bottom-face height still matters:

| Option | Target cube | ICNIRP margin | Hand height | Conditioning | Notes |
|---|---|---|---|---|---|
| A | 150 mm, 66–216 | 23% | lower | 95th 101 / max 123 | 9 mm guard to the 27 µT contour at 250 mA |
| **B** | **150 mm, 85.6–235.6** | **45%** | 20 mm higher | **95th 69.5 / max 73.1** | bottom aligns with the first calibration plane |
| C | 150 mm, 50–200 | fail @250 mA (213 mA) | lowest | worst | not recommended; ICNIRP fail at 250 mA |

**Decision: B at 150 mm — LOCKED (2026-10-27).** It keeps the
45% ICNIRP margin, the corner conditioning is only modestly worse than the
100 mm cube, and the cube bottom aligns with the 85.6 mm calibration plane. The
150 mm cube is \(z=85.6\ldots235.6\) mm. Option A (66–216) and C (50–200) are
rejected: A has only 23% ICNIRP margin and worse conditioning; C fails ICNIRP at
250 mA. The 100 mm cube at 85.6–185.6 remains the minimum fallback; 200 mm at
85.6–285.6 is a stretch only if SC-01d passes. SC-01d may demote the volume; it
does not move the bottom face without a written deviation.

**CRLB consequence:** 150/B needs \(\sigma_B\le26\) pT; 100/B needs 58 pT;
200/B needs 11 pT. A heritage-class \(10^6\) V/T chain with 1.1 nV/√Hz over
500 Hz is ~25 pT, so 150/B is feasible but tight at 250 mA. If PEN-3 cannot
meet 26 pT, the options are: 100/B fallback (58 pT), a lower-noise/higher-gain
amp, or a higher continuous current — ICNIRP allows up to 456 mA at 150/B, but
the driver/thermal must be checked.

**200 mm stretch:** only if SC-01d passes at 200 mm. First pass at 85.6 mm gives
95th/max 150.5/368.3 and weakest tone 0.06 µT; at 66 mm it is worse
(288.2/643.9). PEN-3 B air + INA163 can meet the 11 pT CRLB, so 200 mm is
plausible; the measured noise/jitter decides. Do not lock 200 mm without
measured evidence.

### D2 — ICNIRP assessment surface

**Decision: B — any accessible point, with a non-metal guard (2026-10-27).**

- **Function:** the guard is an **access barrier, not an EMF shield**. Plastic,
  acrylic, or wood does not attenuate the 20–34 kHz magnetic field; it simply
  prevents the hand/body from reaching the region where the field exceeds
  27 µT. A metal box would shield/eddy-current distort and is prohibited.
- The 27 µT contour is ~57 mm above the board at 250 mA. The guard top must be
  at or above that contour.
- With the 150 mm/B cube bottom at 85.6 mm, the guard sits 28.6 mm below the
  working volume; it does **not** reduce the 150 mm cube.
- The guard is a **non-metal open-top ring/fence/spacer** around the FG board
  perimeter, not a metal box. PLA/PETG/acrylic/wood is acceptable; carbon-fiber,
  metal screws, and metal mesh are not. Use plastic fasteners.
- It must be removable so the 7×7 calibration grid and field-probe mapping can
  access the volume.
- A metal box is prohibited: metal within 150 mm of the tracking volume distorts
  the field and invalidates the accuracy claim.
- A full non-metal box is allowed but unnecessary; an open-top ring/fence is
  lighter, cheaper, and does not obstruct the pen/cable.

### D3 — ADC channel map / two-pen support

| Option | Ch0 | Ch1 | Ch2 | Ch3 | Consequence |
|---|---|---|---|---|---|
| **A** | current | pen 1 | pen 2 | reference | supports Phase 1 #1–2 (1–2 pens); no spare |
| B | current | pen 1 | reference | spare | one pen + ref + spare; second pen needs a mux/another ADC |
| C | current | pen 1 | reference | pen 2 | one pen + ref now; second pen later without ref |

**Decision: A — LOCKED (2026-10-27).** Ch0 current, Ch1 pen 1, Ch2 pen 2, Ch3
reference sensor. Phase 1 #1–2 supports 1–2 pens, so the second pen channel is
committed; the reference is retained. Ch2 is wired and captured from the first
build but enabled/used only when pen 2 exists. The first build is one pen +
reference; the second pen is a build option, not a new ADC/mux. The ADC lane
budget is 4 channels × 32 bit × 256 kSPS = 32.768 Mbit/s; 4 DOUT lanes = 8.192
MHz DCLK. Option B (spare) and C (pen 2 later without reference) are rejected.

### D4 — Precision volume

The tracking volume target is 150 mm; the 100 mm cube is the minimum. The
0.15 mm jitter/tremor target need not apply to the whole 150 mm volume: define
a **high-precision core** (e.g. central 100 mm) for the tremor target and the
full 150 mm volume for ≤2 mm gross tracking. The final core and full volume are
set by the SC-01d jitter gate.

**Decision: 150 mm tracking volume with a 100 mm high-precision core — LOCKED
(2026-10-27).** The core is the central 100 mm cube: \(x,y\in[-50,50]\) mm,
\(z=110.6\ldots210.6\) mm. The precision/tremor/jitter target (0.15 mm/0.1° at
the 95th percentile) applies to the core; the full 150 mm cube carries the
≤2 mm gross-tracking target. 200 mm is a stretch only if the SC-01d gate passes;
100 mm is the minimum fallback. CRLB-wise the core needs \(\sigma_B\le58\) pT,
the full 150 mm volume 26 pT, and 200 mm 11 pT; the core is the easier precision
target, while the 150 mm shell is the gross-tracking volume.

---

## 4. Sign-off

- [x] D1 bottom-face \(z\) chosen for the 150 mm target: **B, 85.6–235.6 mm** (100 mm fallback / 200 mm stretch).
- [x] D2 ICNIRP surface chosen: B (any accessible point + non-metal guard).
- [x] D3 channel map chosen: **A (current, pen 1, pen 2, reference)**.
- [x] D4 precision volume chosen: **150 mm tracking + 100 mm core**.
- [ ] SC-01d volume acceptance gate accepted (100 min / 150 target / 200 stretch; final by jitter).
- [ ] SC-01e CRLB noise target accepted (26 pT at 150/B, 58 pT at 100/B, 11 pT at 200/B; PEN-3 verify).
- [ ] SC-01…SC-10 reviewed and signed.
- [ ] `docs/phase2/design_order.md` stage summary updated.
