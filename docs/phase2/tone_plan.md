# Phase 2 — Tone plan decision

**Decision (2026-10-26).** Lock eight tones at **20, 22, 24, 26, 28, 30, 32, 34 kHz**
(2 kHz spacing). Use the AD7768-4 in fast mode at **ODR = 256 kSPS**, **N = 512
samples/frame** by default. Use a **rectangular (integer-J) demod as the primary**;
**Hamming is the fallback** for transient/interference-heavy frames. The integer-J bins
are \(J_i = 40, 44, \ldots, 68\), four bins between adjacent tones. **N = 1024 is the
documented fallback if Hamming is required and its bench margin is insufficient**; it
costs 2 ms of acquisition and requires re-checking the 100 Hz budget.

This supersedes the 20.5–27.5 kHz @ 1 kHz heritage note for Phase 2. The 1 kHz plan is
retained only as a comparison and as a fallback if the ferrite resonance or narrow-band
requirements later force it.

**Key numbers:** \(T_{acq}=2.0\) ms; \(J=40\ldots68\); 4 bins; rectangular margin
1.11 bins, Hamming margin 25–95 Hz; 34 kHz top tone; 73 pF cable/coil budget; 30 ps
clock jitter for 104 dB.

Sources: AD7768/AD7768-4 Rev.D datasheet (`docs/ad7768-ad7768-4.pdf`); thesis §3
(window/DFT) and §4.2–4.8 (driver/coil); `docs/phase2/anser-baseline-findings.md`;
`docs/phase2/adc_justification.md`; `docs/phase2/design_order.md`; `simulations/field_jacobian.py`.

---

## 1. Inputs that decide the plan

| Input | Value | Source |
|---|---|---|
| ADC max ODR | 256 kSPS/ch, fast mode | AD7768-4 datasheet |
| MCLK / decimation | 32.768 MHz, ×32 → ODR 256 kSPS | AD7768-4 datasheet |
| Wideband filter group delay | 34/ODR = 132.8 µs | AD7768-4 datasheet |
| Wideband passband / stopband | 0.4 × ODR = 102.4 kHz / 0.499 × ODR = 127.7 kHz | AD7768-4 datasheet |
| Pose budget | \(T_{pose}<10\) ms; ≥100 Hz; latency ≤20/100 ms | Phase 1 #14–16 |
| Window criterion | main lobe width < half the tone spacing (Hamming fallback); integer-J orthogonality for rectangular | Thesis §3 Eq.3.14; common-clock architecture |
| Rectangular main lobe | 0.89 bins (−3 dB); zero tone-to-tone leakage at exact integer bins | Thesis Table 3.3; DFT orthogonality |
| Hamming main lobe | 1.81 bins (−6 dB, table) to 1.95 bins (thesis measured) | Thesis Table 3.3/text |
| FG current | 250 mA nominal, 500 mA max | Thesis §4.2–4.3 |
| Coil load | 70 µH + 2 Ω | Thesis §4.8 |
| Pen resonance | ~485 kHz air, ~290 kHz ferrite | Jaeger Ch.7 |
| Cable capacitance | 0.6 m W2697 ≈ 39 pF + 20 pF terminations = 59 pF | `BOM_PEN-ANA-01` |

The critical change from the earlier budget: the AD7768-4 tops out at **256 kSPS**, not
the 500 kSPS used in `adc_justification.md` §5. The tone plan must fit the real ODR.

---

## 2. Comparison

\(N\) = samples/frame, \(\Delta f=F_s/N\) = bin width, spacing in bins = \(\Delta F/\Delta f\).
The rectangular main lobe is 0.89 bins; the Hamming main lobe is 1.81–1.95 bins. The
table evaluates the **Hamming fallback** because it is the stricter case. With
rectangular + integer-J, the tones are orthogonal at the exact bins, so the main-lobe
criterion is not the binding constraint.

| Plan | N | Bin | Tones / bins | Spacing | Hamming width | Margin vs half-spacing | \(T_{acq}\) | Left for demod+solve | Verdict (Hamming fallback) |
|---|---|---|---|---|---|---|---|---|---|
| 1 kHz | 512 | 500 Hz | 41–55 | 2 bins | 905–975 Hz | **fail** (half = 500 Hz) | 2.0 ms | 7.87 ms | fail Hamming; passes rectangular (0.89-bin lobe) |
| 1 kHz | 1024 | 250 Hz | 82–110 | 4 bins | 453–488 Hz | 12–47 Hz | 4.0 ms | 5.87 ms | timing risk |
| 1 kHz | 2048 | 125 Hz | 164–220 | 8 bins | 226–244 Hz | 256–274 Hz | 8.0 ms | 1.87 ms | fail rate |
| 2 kHz | 256 | 1000 Hz | 20–34 | 2 bins | 1.81–1.95 kHz | **fail** (half = 1 kHz) | 1.0 ms | 8.87 ms | fail Hamming; passes rectangular (0.89-bin lobe) |
| **2 kHz** | **512** | **500 Hz** | **40–68** | **4 bins** | **905–975 Hz** | **25–95 Hz** | **2.0 ms** | **7.87 ms** | **selected: passes both windows** |
| 2 kHz | 1024 | 250 Hz | 80–136 | 8 bins | 453–488 Hz | 513–548 Hz | 4.0 ms | 5.87 ms | Hamming fallback |
| 4 kHz | 256 | 1000 Hz | 20–48 | 4 bins | 1.81–1.95 kHz | 50–190 Hz | 1.0 ms | 8.87 ms | not selected (top 48 kHz) |

The key comparison is **1 kHz/N=512 vs 2 kHz/N=512 with rectangular + integer-J**: both
use 2 ms of acquisition, but the 2 kHz plan has 4-bin spacing instead of 2 bins, so its
rectangular main-lobe margin is 1.11 bins (555 Hz) vs 0.11 bin (55 Hz), and it also
passes the Hamming fallback. The 1 kHz plan's only advantage is its narrower band
(20.5–27.5 kHz vs 20–34 kHz), which matters for ferrite resonance and cable capacitance;
that is not enough to give up the 2 kHz plan's margin. If Hamming is required, 1 kHz
needs N=1024 (4 ms) while 2 kHz/N=512 still passes at 2 ms.

**2 kHz/N=256** is the 1 ms rectangular-only option (2-bin spacing, 0.11-bin margin,
~111 Hz), but it loses the Hamming fallback and halves the main-lobe margin. It is not
selected; N=512 is the robust default.

---

## 3. Timing budget at N = 512

| Term | Value | Note |
|---|---|---|
| \(T_{acq}=N/F_s\) | 512/256 k = **2.000 ms** | 8 tones, integer-J |
| ADC group delay | 34/256 k = **0.133 ms** | wideband filter, fixed |
| Acquisition + ADC delay | **2.133 ms** | |
| Remaining at 10 ms | **7.867 ms** | demod + solver + overhead |
| Pose period at 100 Hz | 10 ms | spec #16 |
| Filter-off latency | <20 ms | spec #14 |
| Filter-on latency | <100 ms | spec #15 |

This is the same 2 ms acquisition the earlier 500 kSPS/N=1000 budget assumed. The
2 kHz/N=512 choice therefore preserves the ~8 ms demod/solve window. N=1024 would leave
only 5.87 ms; use it only if the Hamming fallback margin at N=512 is too small.

The ADC wideband filter settling time is 68/ODR = 266 µs. Use a one-time `START`/`SYNC`
at startup and count `DRDY` pulses; do **not** pulse `SYNC_IN` every frame. The filter
must be allowed to settle after the initial sync.

---

## 4. Spectral / window check

For N=512, \(F_s=256\) kSPS, \(\Delta f=500\) Hz. The tones are at integer bins:

\[
J_i = \frac{f_i N}{F_s} = \frac{f_i}{500} = 40, 44, 48, 52, 56, 60, 64, 68
\]

for 20, 22, 24, 26, 28, 30, 32, 34 kHz. Adjacent tones are 4 bins apart. With
**rectangular + integer-J**, the DFT at each tone bin is orthogonal to the other tones
(zero tone-to-tone leakage); the rectangular main lobe is 0.89 bins, so the margin to the
2-bin half-spacing is 1.11 bins (555 Hz). With the **Hamming fallback**, the main lobe is
1.81–1.95 bins, margin 0.05–0.19 bins (25–95 Hz); tight but valid, and bench-confirmed.

**Assignment and accuracy.** Default assignment is coil \(i\) in `fSysSetup.m` order →
tone \(i\) in ascending order; FG-1 may reorder the assignment if the conditioning map
requires it, but the tone set and spacing are fixed. Each coil transmits one tone, and
the current-sense summer is the per-tone phase reference \(Y_I\). Frequency accuracy is
set by the common TCXO: relative spacing is exact, absolute error is the TCXO ppm, and
there is no per-tone drift because the DDS and ADC share the clock.

- **Rectangular primary:** zero tone-to-tone leakage and the narrowest ENBW (best SNR).
  Its −13 dB sidelobes affect only non-bin components (harmonics, transients, out-of-band
  interference); the ADC digital filter plus analog AA must handle those. The bench
  compares rectangular vs Hamming and confirms the spur floor.
- **Hamming fallback:** −42 dB sidelobes, better for transient-heavy frames; it passes at
  2 kHz/N=512 with 25–95 Hz margin.
- **Do not use Blackman at N=512**: 2.35 bins > 2-bin half-spacing.
- If Hamming is required and its margin is <50 Hz, move to N=1024: 8-bin spacing,
  2.05–2.19-bin margin (513–548 Hz), 4 ms. With rectangular, N=512 has 1.11-bin margin.

---

## 5. ADC / filter / interface implications

- **Mode:** fast mode, MCLK 32.768 MHz, decimation ×32, ODR 256 kSPS, wideband filter.
- **Group delay:** 34/ODR = 132.8 µs; subtract once as a fixed timestamp offset.
- **Passband:** 102.4 kHz at 0.4 × ODR; 34 kHz is 0.33 × passband, flat.
- **Stopband:** 127.7 kHz at 105 dB; a single RC pole ahead of the AD7768's external
  RC/charge-reservoir network is sufficient.
- **Data path:** 3 active channels × 32-bit frames × 256 kSPS = 24.576 Mbit/s.
  - 4 DOUT lanes → DCLK = 6.144 MHz.
  - 2 DOUT lanes → DCLK = 12.288 MHz.
  - 4 active channels would be 32.768 Mbit/s (8.192 MHz on 4 lanes).
- **Data interface is DCLK/DOUT, not SPI.** SPI is configuration only.
- **Control:** `SYNC_IN`, `START`, `SYNC_OUT`, `DRDY`; there is no `CONVST`. Wire
  `START` → `SYNC_OUT` → `SYNC_IN` for a one-time startup sync, or drive `SYNC_IN` from
  the FPGA with an MCLK-synchronous pulse. Discard the first 68 samples (68/ODR = 266 µs)
  after the initial sync; then count `DRDY` for frame boundaries. Do not pulse
  `SYNC_IN` every frame.
- **Clock jitter:** \(SNR_j=-20\log(2\pi f t_j)\). At 34 kHz, 1 ns rms gives only
  **73.4 dB**, not the 104 dB claimed in the old RQ-A4. For the ADC's 104 dB target,
  the clock jitter must be **≤30 ps rms**; if the system spur target is only 60–70 dB,
  1 ns may be sufficient. Specify the TCXO/PLL from the chosen target and measure it;
  do not claim 104 dB at 1 ns.
- **Pin budget:** 4 DOUT + DCLK + DRDY + SYNC/START + MCLK + RESET = 10 signals, plus SPI
  configuration. A 2×6 Pmod has 8 I/O; use a 2×8 or custom header.
- **Correct the stale requirements:** `adc_justification.md` RQ-A4/A5/A6 still says
  CONVST/SCLK, ±5/±10 V, and SPI data. The actual AD7768-4 is ±4.096 V differential,
  DCLK/DOUT data, SYNC/START/DRDY control.

---

## 6. Coil / driver / ICNIRP consequences

- **Field per tone is frequency-independent** in the quasi-static band. The ICNIRP linear
  sum and the 27 µT contour at 250 mA are unchanged by the tone plan.
- **Pen coil:** 34 kHz is 14.3× below the air-coil resonance (~485 kHz) and 8.5× below the
  ferrite resonance (~290 kHz). The 10× guideline is relaxed for ferrite. If ferrite is
  chosen in PEN-3, measure \(A_{sens}(f)\) and phase at 34 kHz and confirm linearity; the
  preliminary link budget says the amp floor is easily cleared, so ferrite is an
  accuracy/size choice, not an SNR necessity.
- **Cable capacitance:** the 10× resonance target at 34 kHz is 340 kHz. Worst case
  \(L=3\) mH gives
  \[
  C_{max}=\frac{1}{(2\pi\cdot340\,\mathrm{kHz})^2\cdot3\,\mathrm{mH}}\approx73\ \mathrm{pF}
  \]
  (was 94 pF at 27.5 kHz). The filed W2697 0.6 m whip is 59 pF, so it passes with 14 pF
  margin; 0.8 m is marginal. **Topology note:** the coil sees the preamp input, not the
  ADC input. The 73 pF budget covers cable + connector + preamp input; the AD7768's
  switched-cap RC sits after the preamp and is designed in FE-4/ADC-5. Updated in
  connector Rev D / BOM Rev 0.03.
- **Driver compliance:** at 34 kHz, \(Z_{coil}=\sqrt{2^2+(2\pi\cdot34\,\mathrm{kHz}\cdot70\,\mu H)^2}\approx15.1\ \Omega\).
  - 250 mA RMS → 3.8 V RMS = 5.3 V peak; within the 7.5 V single-rail swing.
  - 500 mA peak → 7.55 V peak; at the rail limit.
  - 500 mA RMS → 10.7 V peak; not achievable on the single 15 V rail.
  Keep 500 mA as a max/short-term rating, not continuous. The thesis phase-lead
  compensation was tuned for 20–30 kHz; re-check loop phase margin ≥45° at 34 kHz with
  the real coil and mutual coupling.
- **EMC/eddy:** 34 kHz is slightly worse than 27.5 kHz for eddy-current distortion and
  radiated emissions; the default no-metal condition and the driver filter cover it.

---

## 7. Verification plan

1. **Eight-tone FFT at the ADC:** measure integer-J on/off leakage, compare rectangular
   vs Hamming main-lobe leakage, and confirm the spur floor against the 60–70 dB budget.
2. **Tone coherence:** two-tone phase and amplitude stability over 1 h and 18–28 °C.
3. **IMD:** with 2 kHz spacing, 3rd-order products \(2f_i-f_j\) land on other tone bins
   (e.g., 2×22−20 = 24 kHz). The window cannot separate them; the driver/coil linearity
   and per-tone \(\kappa\) must hold IMD below the spur budget. Measure all-tones IMD,
   not just single-tone THD.
4. **Pen coil:** \(A_{sens}(f)\) and phase at 20–34 kHz; resonance sweep; ferrite A/B if
   applicable.
5. **Driver:** current/voltage at 34 kHz, 250 mA nominal and 500 mA peak; compliance,
   THD, thermal.
6. **Moving run:** 1 h at ≥100 Hz, zero dropped frames; latency and stop timing.
7. **ICNIRP:** field-probe scan at the final current; linear sum ≤27 µT at accessible
   points. The tone plan does not change the field sum, but verify at 34 kHz.

---

## 8. Fallbacks / open items

- **N=1024 fallback:** if Hamming is required and the N=512 margin is <50 Hz on the
  bench, use N=1024 (4 ms acquisition, 5.87 ms left) and re-check the solver budget.
  With rectangular, N=512 has 1.11-bin margin and needs no fallback. Do not reduce the
  tone spacing to 1 kHz without re-running this comparison.
- **Ferrite:** if PEN-3 chooses ferrite, re-check the 34 kHz resonance/phase margin and
  the 73 pF cable budget. Air-core is preferred unless ferrite is needed for accuracy.
- **Connector/cable:** RQ-C3/RQ-B2 and BOM_PEN-ANA-01 are updated to 73 pF total /
  56 pF cable at 34 kHz (connector Rev D, BOM Rev 0.03). The filed 0.6 m W2697 remains
  compliant; the 0.8 m alternate is not worst-case compliant.
- **AGENTS.md:** the 20.5–27.5 kHz @1 kHz line remains a heritage note; this file is the
  Phase 2 decision.
