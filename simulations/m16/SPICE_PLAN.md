# M16 + LTC1563-2 — pure-SPICE verification plan (datasheet-realistic)

**Status:** simulation-only plan for today, 2026-10-27. No bench in this pass.
**Goal:** estimate whether the M16 path can meet the 8-tone IMD, image, loop, and noise targets using vendor SPICE models where they represent real operation, and datasheet-based behavioral non-idealities where they do not.
**Honesty:** this produces a **bounded estimate**, not a validation. The final 8-tone IMD number is a bench measurement.

---

## 1. What simulation can and cannot prove

| Can estimate | Cannot prove |
|---|---|
| Filter fc, Q, image at 165.8 kHz, phase | DAC80508 actual INL/DNL/IMD |
| Current-loop phase/gain margin, step | LMH6321 class-AB crossover distortion |
| Per-driver single-tone THD (out-of-band) | LTC1563-2 actual distortion/noise |
| 8-tone IMD from datasheet nonlinearities | EMI/layout coupling |
| Noise from datasheet spectral densities | Thermal drift/aging |
| Monte Carlo tolerance spread | Board parasitics |

A pure-SPICE pass is an **architecture screen**. It can show “10–20 dB margin” or “marginal,” not “the board passes.”

---

## 2. Correct 8-tone topology

The design is **8 drivers, one tone each**:

```text
DDS f1 → DAC/filter/loop 1 → coil 1 ─┐
DDS f2 → DAC/filter/loop 2 → coil 2 ─┼─► field sum at pen → INA163 → ADA4940 → AD7768
...                                  │
DDS f8 → DAC/filter/loop 8 → coil 8 ─┘
          │
          └─► 8× 1 Ω sense → summer → AD7768 Ch0
```

The 8-tone IMD that matters is at:
- the **current-sense summer / Ch0** (8 currents, one op-amp/ADC),
- the **pen receiver** (8 fields, INA163/ADA4940/AD7768),
- **mutual coupling** between coils (each driver sees the other tones),
- **DAC channel crosstalk** and shared supply/ground.

The **one-driver 8-tone test** (T8) is a stress screen, not the system IMD.

---

## 3. Models: vendor first, datasheet behavioral second

### 3.1 Vendor models to use if they represent real operation

| Block | Model | Check |
|---|---|---|
| LTC1563-2 | ADI/LTspice model | Does it include noise/distortion? |
| OPA192 | TI SPICE model | Includes noise/THD? |
| LMH6321 | TI SPICE model | Does it include class-AB crossover? |
| INA163 | TI SPICE model | Includes noise/THD? |
| ADA4940-2 | ADI SPICE model | Includes noise/THD? |
| DAC80508 | TI SPICE/IBIS | SPICE only if it includes INL/DNL/settling; IBIS is not enough for IMD |
| AD7768-4 | ADI model if any | Otherwise behavioral ADC with datasheet noise/THD |

If a vendor model is **ideal/behavioral** (no nonlinearity/noise), do not treat its IMD as real; use the datasheet behavioral model instead.

### 3.2 Datasheet behavioral models for the gaps

**DAC80508 (16-bit, 8 ch, 0.2 MSPS):**
- Ideal 16-bit quantizer + sample-and-hold at 199.805 kSPS.
- **Code-error table** consistent with datasheet INL ±1 LSB / DNL ±1 LSB (monotonic). Use a worst-case pattern (e.g., alternating ±1 LSB or a polynomial fit) plus a random table; run several patterns.
- 5 µs settling model (one-pole or datasheet settling shape).
- Output buffer 0–5 V, 20 mA.
- If TI provides a transistor-level model with INL/DNL/settling, use it instead.

**LTC1563-2 (4th-order Butterworth, 60 kHz):**
- Vendor model if it includes noise/distortion; otherwise behavioral 4th-order (two Sallen-Key/MFB sections) + datasheet noise:
  - 36 µV RMS at 25.6 kHz, 60 µV RMS at 256 kHz; interpolate ~55 µV at 60 kHz.
  - fc ±2%; DC offset <1 mV.
- Distortion: datasheet THD if given; otherwise treat the filter as low-distortion and state the limitation.

**LMH6321 (300 mA buffer):**
- Vendor model if it includes the class-AB output stage; otherwise a behavioral buffer with:
  - 300 mA limit, 110 MHz BW, 1800 V/µs,
  - a crossover/soft-saturation nonlinearity fit to the datasheet THD at 20–34 kHz, 150/250 mA.
- If no datasheet THD curve covers the operating point, run the loop with an ideal buffer and add the datasheet THD as a post-simulation spur bound; label it an estimate.

**Receiver:**
- INA163 + ADA4940 vendor models; if unavailable, datasheet noise (1.1 nV/√Hz, 3.9 nV/√Hz) and THD.
- AD7768-4: behavioral 24-bit ADC + datasheet dynamic range (108 dB) and THD; or vendor model if available.
- The coil/field sum is linear; mutual coupling is a matrix, not a nonlinearity.

### 3.3 Datasheet-derived model library (own models)

We can build our own models from datasheet curves. They are **datasheet-consistent behavioral models**, not the real silicon: they reproduce the specified behavior near the datasheet operating point.

Method:

1. Digitize the datasheet curves at the operating point: INL/DNL vs code, THD vs frequency/amplitude, noise density, settling, output impedance, gain/phase.
2. Build the model from controlled sources/lookup tables: `TABLE`, `POLY`, `B` sources, sample-and-hold, quantizer, noise sources.
3. Calibrate at 150/250 mA, 20–34 kHz, 25 °C, with the specified supply/load.
4. Validate the model against the same datasheet curves; report the fit error.
5. Use min/max datasheet values for the pass/fail bound; typical for the expected value.

| Block | Datasheet data | Model mechanism | Confidence |
|---|---|---|---|
| DAC80508 | INL/DNL ±1 LSB, 5 µs, 0.2 MSPS, ref noise | 16-bit quantizer + code-error table + settling + ref noise | Medium: exact INL pattern unknown; worst-case table bounds it |
| LTC1563-2 | fc ±2%, 55 µV, THD if given | 4th-order + noise + polynomial | Medium-high |
| LMH6321 | 300 mA, 110 MHz, THD curve | buffer + tanh/crossover + output Z | Low-medium: crossover not fully specified |
| OPA192 | 5.5 nV/√Hz, THD | vendor/behavioral | High |
| INA163/ADA4940 | noise/THD | vendor/behavioral | High |
| AD7768 | 108 dB, THD | 24-bit + noise/THD | Medium-high |
| Summer | OPA2192 THD | behavioral | Medium |

Limits:

- Datasheet THD is often at 1 kHz or one frequency; extrapolating to 20–34 kHz is uncertain.
- The DAC INL/DNL pattern is not specified; a worst-case table gives a pessimistic bound.
- The LMH6321 class-AB crossover is not fully characterized; the model is a fit, not the real stage.
- The model is valid near the datasheet operating point; temperature/layout/EMI are not included.
- Result: a bounded estimate; the bench is the final IMD validation.

---

## 4. Test matrix (simulation-only)

### T1 — DC operating point
`.op`: DAC midscale, 7.5 V midrail, no DC coil current, node voltages, power.

### T2 — Filter AC
`.ac dec 200 1k 1meg`: fc, Q, gain at 34 kHz, image at 165.8 kHz, phase at 20/34 kHz, group delay. Monte Carlo R 0.1%, fc ±2%.

### T3 — Current-loop AC
Break the loop, inject AC, `analyze_stability`: PM ≥45°, GM ≥10 dB at 150/250 mA.

### T4 — Per-driver single-tone THD
One driver, one tone (20/34 kHz), 150 mA: current-sense FFT; harmonics at 40–102 kHz (out of band); check they do not alias/mix in the receiver.

### T5 — Current-sense summer 8-tone IMD
8 drivers, one tone each, summed at the sense/summer; summer op-amp + ADC model with datasheet THD; FFT at Ch0; check the eight tone bins and the 3rd-order products `2f_i−f_j`.

### T6 — Pen receiver 8-tone IMD
8 fields summed at the pen; INA163 + ADA4940 + AD7768 model; FFT at the ADC; check the tone bins and 3rd-order products. This is the primary in-band IMD test.

### T7 — Crosstalk / mutual coupling
Add the 8-coil mutual-coupling matrix and DAC channel crosstalk; repeat T4–T6. Coupled tones can intermodulate in each driver and the summer.

### T8 — One-driver 8-tone stress (screen)
8 tones into one driver/filter/loop; FFT at the current-sense. This is a stress screen for the filter/loop linearity, **not** the system IMD.

### T9 — Noise
`.noise`: DAC quantization, LTC1563-2 55 µV, OPA192/LMH6321, 1 Ω thermal, receiver; integrate a 500 Hz bin; compare 26 pT (0.15 mm) / 52 pT (0.3 mm).

### T10 — Monte Carlo
R 0.1%, fc ±2%, coil L ±20%, R ±10%, coupling ±20%; 100 runs; image/IMD/phase spread.

### T11 — Fallback comparisons
Behavioral LTC1564 8th-order, AD5541A 1 MSPS + 2nd-order, AD9833 10-bit/6 MHz; same topology; compare image/IMD/noise.

---

## 5. 8-tone vector and FFT

Define explicitly:
- Tones: 20, 22, 24, 26, 28, 30, 32, 34 kHz.
- Per-tone amplitude: set the total coil current to 150 mA (prototype) and 250 mA (nominal); state whether RMS or peak.
- Phases: zero and a worst-case set that maximizes the crest factor.
- Test both the nominal vector and the worst-case crest.

FFT:
- DAC rate 199.805 kSPS; 10 ms is 1998.05 samples, not integer. Use a coherent sample count or a window; state the resolution and leakage.
- The 2 kHz spacing needs ≥100 Hz bins; a 10 ms window gives that, but the non-integer rate requires resampling or a flat-top/Hann window.
- Check the 3rd-order products at the tone bins; sum all products per bin, not just one.

---

## 6. Pass/fail (simulation estimate)

| Test | Metric | Pass |
|---|---|---|
| T1 | DC coil current | <1 mA |
| T2 | fc / image | 60 ±2% / ≥35 dB at 165.8 kHz |
| T3 | PM / GM | ≥45° / ≥10 dB |
| T4 | single-tone THD | ≤−60 dBc |
| T5 | summer 8-tone products | ≤−60 dBc per bin (sum) |
| T6 | receiver 8-tone products | ≤−60 dBc per bin (sum) |
| T7 | crosstalk/mutual coupling | ≤−60 dBc |
| T8 | one-driver stress | ≤−60 dBc (screen) |
| T9 | in-band noise | ≤−71.7 dB (0.15 mm) or ≤−65.7 dB (0.3 mm) |
| T10 | 95th percentile | within budget |
| T11 | fallback comparison | relative margin |

The −60 dBc is a placeholder; derive the final per-bin limit from the pose/tool budget. A −60 dBc product is ~0.1% amplitude error, roughly 0.15 mm at 150 mm; 0.3 mm allows ~0.2%.

---

## 7. Tool workflow (LTspice MCP)

1. `check_installation`.
2. `create_netlist` for one driver channel; `generate_schematic` if a graphical `.asc` is wanted.
3. `simulate_netlist` / `simulate` for `.op`, `.ac`, `.tran`, `.noise`.
4. `get_operating_point` (T1).
5. `analyze_stability` (T3).
6. `analyze_waveform` (FFT/THD/settling for T4–T8).
7. `analyze_noise` / `get_total_noise` (T9).
8. `monte_carlo` (T10).
9. `parameter_sweep` (filter fc, coupling, compensation).
10. `plot_waveform` / `export_csv` for the report.

For the 8-channel sum, simulate one driver channel and build a behavioral 8-channel sum at the summer/receiver; a full 8-channel transistor-level netlist is possible but slow.

---

## 8. Deliverables

- Netlists: one driver, filter AC, loop AC, 8-tone summer, receiver, noise, Monte Carlo.
- Raw/CSV/SVG plots.
- `m16-spice-report.md`: results, pass/fail, confidence, recommended filter R/compensation/coupling, and the list of items that only the bench can prove.

---

## 9. Risks / confidence

- **High confidence:** filter response/phase, loop stability, step, Monte Carlo, image.
- **Medium confidence:** per-driver THD, summer/receiver IMD if the models include the datasheet nonlinearity.
- **Low confidence:** DAC80508 INL/DNL/IMD, LMH6321 crossover, LTC1563-2 distortion, EMI. These need the bench.
- If the simulation shows <6 dB margin on T5/T6, treat it as “likely fail on the bench”; if >15 dB, “likely pass.”

---

## 10. Decision gates

1. **Gate A:** T2/T3 pass → proceed.
2. **Gate B:** T5/T6/T7 >10 dB margin → architecture likely passes; <6 dB → plan the LTC1564 8th-order or AD5541A 1 MSPS fallback.
3. **Gate C:** T9/T10 pass → layout/bench plan.
4. **Bench:** the one-channel 8-tone FFT is the final validation; simulation does not replace it.
