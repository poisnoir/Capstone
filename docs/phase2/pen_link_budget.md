# Phase 2 — PEN-3 pen coil + amp link budget

**Status:** draft for PEN-3 sign-off, 2026-10-27. **Coil B air-core is LOCKED
(no ferrite).** The INA163 amp is a proposed choice, not locked; the rest of the
link budget is first-pass from the Jaeger Ch.7 coil table and the thesis
INA163/INA128 comparison. It answers the CRLB question: can the pen coil + amp
deliver the field-equivalent noise \(\sigma_B\) required by the 100/150/200 mm
volume gates?

**Sources:** `HAJ_Thesis_2018.pdf` Ch.7 Table 7.1 and §4.4 (INA163 vs INA128);
`docs/extracts/Jaeger2018_bespoke-sensor_Ch7_extract.txt`;
`docs/phase2/anser-baseline-findings.md`; `contract/system_contract.md` SC-01e;
`simulations/field_jacobian.py`; `adc_justification.md`; `tone_plan.md`.

**Assumptions:**

- Worst-case weakest tone: **0.10 µT at 150 mm/B**, **0.06 µT at 200 mm/B**,
  **0.17 µT at 100 mm/B** (first-pass 8×5 scan at 250 mA).
- Demod bin **500 Hz** (rectangular primary, N=512 at 256 kSPS).
- Temperature 300 K; coil thermal noise \(e_{th}=\sqrt{4kTRB}\).
- Air core \(\mu_a=1\); ferrite measured \(\mu_a\approx3\) (+10 dB).
- Amp candidates: INA163 (1.1 nV/√Hz, 0.8 pA/√Hz), INA128 (8 nV/√Hz,
  0.3 pA/√Hz), AD620 (9 nV/√Hz, 0.1 pA/√Hz), AD627 (27 nV/√Hz, 0.1 pA/√Hz).
  The thesis Table 4.2 gives the INA163/INA128 values; AD620/AD627 are the
  E301-class alternatives.
- Coil mean area \(A=\pi((ID+OD)/4)^2\); \(V/T=N A \omega \mu_a\).
- The required \(\sigma_B\) from SC-01e: **150/B ≤26 pT**, **100/B ≤58 pT**,
  **200/B ≤11 pT**.

---

## 1. Coil parameters and induced voltage

Table 7.1 coils, air core, mean area:

| Coil | N | ID/OD (mm) | R (Ω) | L (µH) | \(N A\) (m²) | V/T @20 kHz | V/T @34 kHz | Air accuracy (mm) | Ferrite accuracy (mm) |
|---|---|---|---|---|---|---|---|---|---|
| A | 321 | 9 / 12.5 | 7.4 | 604 | 2.91e-2 | 3661 | 6224 | 1.89 | — |
| **B** | **319** | **11 / 14.1** | **8.6** | **804** | **3.95e-2** | **4959** | **8430** | **1.59** | — |
| C | 120 | 9 / 12.2 | 0.8 | 91 | 1.06e-2 | 1331 | 2262 | 2.48 | 1.90 |
| D | 216 | 9 / 11.4 | 9.4 | 425 | 1.77e-2 | 2218 | 3771 | 1.98 | 1.62 |
| E | 417 | 9 / 12.0 | 14.3 | 1018 | 3.61e-2 | 4537 | 7714 | 1.70 | 1.58 |

The coil source impedance at 20 kHz is \(Z=\sqrt{R^2+(\omega L)^2}\):
A 76 Ω, B 101 Ω, C 11.5 Ω, D 54 Ω, E 129 Ω. At 34 kHz it is 1.7× higher.
The INA163 current noise contribution is <2.3 nV over 500 Hz; the thermal noise
is 2.6–10.9 nV; the INA163 voltage noise is 24.6 nV. The amp dominates.

---

## 2. Field-equivalent noise \(\sigma_B\)

\(\sigma_B = \sqrt{(e_n^2 + e_{th}^2 + (i_n Z)^2)B} / (N A \omega)\).

| Coil | INA163 @20 k | INA163 @34 k | INA128 @20 k | INA128 @34 k | AD620 @20 k | AD620 @34 k |
|---|---|---|---|---|---|---|
| A | 7.1 pT | 4.2 pT | 48.9 pT | 28.8 pT | 55.0 pT | 32.4 pT |
| **B** | **5.3 pT** | **3.1 pT** | **36.1 pT** | **21.2 pT** | **40.6 pT** | **23.9 pT** |
| C | 18.6 pT | 10.9 pT | 134.4 pT | 79.1 pT | 151.2 pT | 89.0 pT |
| D | 11.8 pT | 6.9 pT | 80.8 pT | 47.5 pT | 90.8 pT | 53.4 pT |
| E | 5.9 pT | 3.5 pT | 39.5 pT | 23.2 pT | 44.4 pT | 26.1 pT |

Pass/fail against the gates:

| Gate | Required | INA163 | INA128 | AD620 |
|---|---|---|---|---|
| 100/B | ≤58 pT | all coils pass | A/B/D/E pass @34, A/B/E pass @20; C fails | same as INA128 |
| **150/B** | **≤26 pT** | **all coils pass @20 k** | only B/E @34 k pass; A marginal; C/D fail | B/E @34 k only; A marginal; C/D fail |
| 200/B | ≤11 pT | A/B/E pass @20 k; D marginal; C fails @20 but passes @34 | fail | fail |

AD627 is not viable: its 27 nV/√Hz gives 122–454 pT, above all gates.

**150 mA prototype (thermal-first):** the required CRLB noise scales with
current (0.6× at 150 mA): 150/B ≤15.6 pT, 200/B ≤6.6 pT, 100/B ≤34.8 pT.
B air + INA163 ~5.3 pT passes 150/B ~3× and 200/B ~1.25×; 200/B is thin and
needs the measured noise/CRLB. 250 mA gives 200/B ~2× margin but more heat.

---

## 3. Signal and SNR at the weakest tone

At 0.10 µT (150/B), the coil signal is \(V_s=N A \omega B\):

| Coil | \(V_s\) @20 k | \(V_s\) @34 k | SNR @20 k, INA163 | SNR @34 k, INA163 |
|---|---|---|---|---|
| A | 0.366 mV | 0.622 mV | 83.2 dB | 89.0 dB |
| B | 0.496 mV | 0.843 mV | 85.4 dB | 91.2 dB |
| C | 0.133 mV | 0.226 mV | 74.5 dB | 80.3 dB |
| D | 0.222 mV | 0.377 mV | 78.0 dB | 83.8 dB |
| E | 0.454 mV | 0.771 mV | 84.6 dB | 90.4 dB |

The required SNR at the 95th-percentile CRLB is ~72 dB for 150/B (26 pT) and
~75 dB for 200/B (11 pT). With INA163, all coils except C at 20 kHz clear the
150/B gate; B/A/E clear 200/B at 20 kHz, and C clears 200/B only at 34 kHz
(10.9 pT, marginal).

---

## 4. Decision

### Ferrite: **no** for A/B/E air-core

- B air is the best overall: 1.59 mm accuracy, \(\sigma_B=5.3\) pT at 20 kHz and
  3.1 pT at 34 kHz with INA163. It passes 150/B with ~5× margin and 200/B with
  ~2× margin.
- A air: 1.89 mm, 7.1 pT at 20 kHz; smaller OD (12.5 mm) if pen diameter
  matters. Passes 150/B with 3.7× and 200/B with 1.5×.
- E air: 1.70 mm, 5.9 pT at 20 kHz; 12.0 mm OD but 0.15 mm wire (fragile).
  Passes both with similar margin to B.
- C air is out: 2.48 mm accuracy and 18.6 pT at 20 kHz. C ferrite would give
  1.90 mm and ~6.2 pT, but adds nonlinearity/Barkhausen; only use it if a
  small-diameter ferrite coil is forced.
- D air: 1.98 mm, 11.8 pT at 20 kHz; marginal for 200/B, passes 150/B. It is
  not the best choice unless the 11.4 mm OD is required.

### Amp: **INA163** for 150/200; INA128/AD620 only for 100/B

- INA163 is the only candidate that meets 150/B for all coils at 20 kHz and
  200/B for A/B/E at 20 kHz.
- INA128/AD620 meet 100/B with A/B/E and are marginal for 150/B (B/E at 34 kHz
  only). The E301 AD620/AD627 heritage is **not sufficient** for 150/200; the
  thesis INA163 recommendation is validated by this link budget.
- AD627 is not viable.

### Gain / output stage

- B air at 0.10 µT/20 kHz gives 0.496 mV; the strongest tone (5.76 µT at
  34 kHz) gives 48.6 mV. A single gain of ~80–150 fits the AD7768 ±4.096 V
  differential input; gain 200 would clip the strong tone. Use a two-stage or
  a gain of ~80–100 with per-tone assignment/headroom.
- The INA163 input bias current is 12 µA; with the B coil 8.6 Ω the DC offset
  is ~103 µV, which becomes ~8 mV at gain 80. AC-couple or bias the coil and
  keep the output stage headroom. The FE-4 design must handle this.

### Tone assignment

Pair the **weakest field coil with 34 kHz** and the strongest with 20 kHz. The
field per tone is frequency-independent, so the assignment changes the induced
voltage (1.7× at 34 kHz) without changing the field/ICNIRP. This is how C can
reach 200/B at 34 kHz (10.9 pT), and how A/B/E gain margin.

---

## 5. PEN-3 gate

- **150 mm/B:** B air + INA163 passes (\(\sigma_B=5.3\) pT at 20 kHz vs 26 pT
  required). This is the current target; build B air + INA163 and measure.
- **200 mm/B:** B air + INA163 passes at 20 kHz (5.3 pT vs 11 pT) and 34 kHz
  (3.1 pT); A/E also pass. 200 mm is feasible with the best coil/amp, but the
  conditioning/CRLB 95th (150/368 at 1 nT) and the weakest-tone assignment
  leave less margin. Treat 200 as a stretch and verify on the bench.
- **100 mm/B:** B/A/E + INA163 passes easily; even INA128/AD620 can meet 100/B
  with A/B/E. This is the minimum/fallback.
- **Ferrite:** no for B/A/E; C ferrite only if a small-diameter coil is forced.

**Exit gate:** build/measure B air (and A/E as alternates), measure
\(A_{sens}(f)\) and input-referred noise over 20–34 kHz, and re-run the weighted
CRLB with the real per-tone noise. If the 150/B gate passes, 150 mm is the
target; if 200/B also passes, 200 mm is allowed. If neither, fall back to 100 mm
or increase current within the ICNIRP/driver/thermal limits.
