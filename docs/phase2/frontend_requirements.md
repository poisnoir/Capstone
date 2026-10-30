# Phase 2 — FE-4 receiver front-end requirements

**Status:** **FE-4 requirements gate ACCEPTED 2026-10-27.** The INA163 +
ADA4940-2 chain is **LOCKED** (ADA4896-2 alternate); the AD7768-4 is the locked
ADC. The differential output is designed to its ±4.096 V input, VCM, and
external RC/charge reservoirs. Bench verification remains at FE-4/ADC-5.

**Sources:** `HAJ_Thesis_2018.pdf` §4.4 (INA163 vs INA128) and Table 4.2;
`docs/phase2/pen_link_budget.md`; `contract/system_contract.md` SC-05/SC-05a–c;
`docs/phase2/adc_justification.md` §9a; AD7768-4 datasheet (input range, VCM,
recommended RC/amplifiers); E301 schematic/parts list (reference only);
`docs/phase2/anser-baseline-findings.md`.

**Decision summary (LOCKED):**

- **INA163** instrumentation amp; **not** INA128/AD620/AD627 for the
  150/200 mm target. INA128/AD620 are only acceptable for the 100 mm fallback.
- **Coil B air-core is LOCKED** from PEN-3 (A/E alternates); no ferrite for B.
- Gain distribution: **INA163 ~35× + differential stage ~2× = ~70×**; the
  strongest tone is ≤−6 dBFS at the AD7768 ±4.096 V differential input.
- Differential output stage: **ADA4940-2** (LOCKED) (fully differential, AD7768
  fast-mode recommended); ADA4896-2 is the alternate. VCM from the ADC;
  inter-channel phase match ≤0.1°.
- Supplies: INA163 on **±12 V** (from the isolated RV-1515D + TPS7A47/TPS7A33
  LDOs); ADA4940-2 and AD7768 on **+5 V**; IOVDD **+3.3 V**; ADR434 4.096 V
  reference shared with a buffer.
- The E301 AD620/AD627 + AD711 heritage is **not sufficient for 200/B and only
  marginal for 150/B** (B/E at 34 kHz); it is a 100 mm fallback / reference only.
- The **AD7768-4 is the locked ADC** for FE-4; this front end is designed to its
  ±4.096 V differential input, VCM, and external RC/charge reservoirs.

---

## 1. Architecture

```
pen coil B (air) → protection/ESD → INA163 (G≈35) → single-ended
   → ADA4940-2/ADA4896-2 differential stage (G≈2, VCM=ADC VCM)
   → AD7768 external RC/charge reservoirs → AD7768-4 Ch1
```

- The pen coil is a floating differential source. The INA163 inputs need a
  bias/return path; the 12 µA input bias current must be handled.
- The ADC reference is ADR434 4.096 V; the ADC VCM sets the output common mode.
- The current-sense Ch0 and reference Ch2 are separate channels; the preamp
  design is for the pen channel and is duplicated for the reference if used.

---

## 2. Requirements

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| FE-01 | Input: **INA163 (LOCKED)**, differential, \(Z_{in}\ge1\) MΩ, CMRR ≥60 dB (target 100 dB), input protection/ESD, bias/return for the floating coil; preamp input capacitance ≤20 pF in the 73 pF coil budget | Phase 2 §4; INA163 12 µA bias; cable/coil resonance | CMRR sweep 20–34 kHz; Zin; bias/offset check |
| FE-02 | Gain: INA163 ~35× + differential stage ~2× (total ~70×); strongest tone at 150/200 mm ≤−6 dBFS; weakest tone above the noise floor; headroom for the 30–40 dB tone spread | `pen_link_budget.md`; AD7768 ±4.096 V | Gain/phase sweep; full-scale/headroom test |
| FE-03 | Noise: INA163 1.1 nV/√Hz; total input-referred ≤26 nV over the 500 Hz demod bin; \(\sigma_B\le26\) pT at 150 mm/B (≤11 pT at 200, ≤58 pT at 100) | SC-01e; PEN-3 link budget | Input-referred noise; weighted CRLB |
| FE-04 | Output: single-ended-to-differential, \(V_{CM}\) = ADC VCM, ±4.096 V differential max; **ADA4940-2 (LOCKED)**; ADA4896-2 alternate; AD7768 external RC/charge reservoirs; inter-channel phase match ≤0.1° | AD7768 datasheet; `adc_justification.md` §9a; AN-1384 | Output swing/settling; phase match |
| FE-05 | Reference/clock: ADR434 4.096 V for the ADC; ADC VCM; MCLK from the common clock tree; no front-end clock generation | `BOM_ADC-01`; SC-07 | Rail/reference noise; clock check |
| FE-06 | Test: gain, CMRR, input-referred noise, THD, phase match, output settling into the AD7768 RC/input model | Phase 1 test plan | Test report |

---

## 3. Noise budget (coil B, 500 Hz bin, 300 K)

| Term | Value | Note |
|---|---|---|
| INA163 voltage noise | 24.6 nV | 1.1 nV/√Hz × √500 |
| Coil thermal noise | 8.4 nV | \(√(4kTRB)\), R=8.6 Ω |
| INA163 current noise × source | 1.8 nV | 0.8 pA/√Hz × 101 Ω × √500 |
| Differential stage (referred to input) | ≪1 nV | 3.9 nV/√Hz / 35 |
| **Total input-referred** | **≈26 nV** | RSS |
| Coil B sensitivity @20 kHz | 4959 V/T | Table 7.1 |
| **\(\sigma_B\) @20 kHz** | **≈5.3 pT** | 26 nV / 4959 V/T |
| \(\sigma_B\) @34 kHz | ≈3.1 pT | 26 nV / 8430 V/T |
| Required at 150/B | ≤26 pT | 5× margin |
| Required at 200/B | ≤11 pT | 2.1× margin |
| Required at 100/B | ≤58 pT | 11× margin |

The INA163 dominates; the differential stage and current noise are negligible.
The 150/200 gates are met with coil B air. Coil C (120 T) is 3.5× noisier
(18.6 pT at 20 kHz) and fails 200/B at 20 kHz; it is out.

---

## 4. Gain / output swing (coil B, 150/200 mm/B)

| Tone | Field | \(V_s\) @20 kHz | \(V_s\) @34 kHz | ×70 output (diff) | Headroom vs ±4.096 V |
|---|---|---|---|---|---|
| Weakest | 0.10 µT | 0.496 mV | 0.843 mV | 34.7 / 59.0 mV | large |
| Strongest | 5.76 µT | 28.6 mV | 48.6 mV | 2.00 / 3.40 V | 17–51% |

- Gain 70 keeps the strongest 34 kHz tone at 3.40 V differential, below the
  ±4.096 V full scale; the weakest tone is 35–59 mV, still ~17–18 bits of the
  24-bit ADC.
- If the field map shows a stronger tone, reduce the gain to ~60 or add a
  per-tone assignment that puts the strongest field at 20 kHz.
- The INA163 gain 35 and differential gain 2 are first-pass values; the exact
  \(R_G\)/feedback values follow the datasheet and the measured field map.

---

## 5. Bias / offset / protection

- INA163 input bias current is **12 µA**. With coil B (8.6 Ω) the DC offset is
  ~103 µV; at gain 70 it is ~7.2 mV at the ADC, within headroom. AC-couple the
  coil or use a low-impedance bias/return network so the 12 µA does not create
  a large offset.
- Input protection: ESD/clamp at the connector, series resistance, and the
  INA163 input rating; keep the protection capacitance within the 73 pF coil
  budget.
- The E301 AD620/AD627 input stage has lower bias current but 7–8× higher
  voltage noise; it cannot meet the 200 mm/B \(\sigma_B\) gate and is only
  marginal for 150 mm/B (B/E at 34 kHz). Use it only as the 100 mm
  fallback/reference.
- CMRR: INA163 ~100 dB; match the input bias/return network and the cable
  shield termination. Target ≥60 dB, design for 100 dB.

---

## 6. Output stage / ADC interface

- The AD7768-4 input is differential ±VREF = ±4.096 V with VCM = 2.5 V (5 V
  AVDD1). The differential stage must set the output common mode to the ADC
  VCM and keep each output within 0.45–4.55 V.
- Use the AD7768 datasheet Figure 87 RC/charge-reservoir network (C1/C2/C3,
  RIN) and a recommended differential amplifier: ADA4940-2 (fully differential,
  low power) or ADA4896-2 (fast mode, lowest noise). The final choice is a
  bench decision; both are allowed.
- The AD7768 external RC is **not** part of the 73 pF coil/cable budget; it sits
  after the preamp. The coil sees the INA163 input capacitance + cable +
  connector.
- Inter-channel phase match (pen vs reference) ≤0.1° at 20–34 kHz; use the same
  amplifier/RC/layout for both channels.

---

## 7. Verification / exit gate

1. Measure \(A_{sens}(f)=V/B\) and input-referred noise over 20–34 kHz with the
   Helmholtz coil; compute \(\sigma_B\).
2. Verify \(\sigma_B\le26\) pT at 150 mm/B (≤11 pT at 200, ≤58 pT at 100) with
   the measured per-tone field map and noise.
3. Measure CMRR, gain, THD, output swing, and phase match; drive the AD7768 RC
   model and confirm settling.
4. If 150/B passes, 150 mm is the target; if 200/B also passes, 200 mm is
   allowed. If not, fall back to 100 mm, increase current within ICNIRP/driver/
   thermal limits, or lower the amp noise.
