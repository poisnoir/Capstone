# M16 + LTC1563-2 — SPICE results (first pass)

> **Phase 2 report:** see `FINAL_REPORT.md` for the consolidated report with figures. This file is the working log.

Date: 2026-10-27. LTspice 26.1.1 batch mode via Wine. The `ltspice` ADI bridge could not start headless; the `ltspice-sim` batch server crashed on a stepped run, so the netlists were run directly with `LTspice.exe -b -ascii` and parsed with `parse_raw.py`.

## 1. Filter AC — `filter_ac.cir`

4th-order Butterworth, fc = 60 kHz, Q = 0.541/1.307.

| Frequency | Gain | Phase |
|---|---|---|
| 20 kHz | 0.00 dB | −50.7° |
| 26 kHz | −0.01 dB | −66.8° |
| 34 kHz | −0.05 dB | −89.6° |
| 60 kHz | −3.0 dB | −152.8° |
| 165.8 kHz | **−35.3 dB** | — |
| 990 kHz | −97.4 dB | — |

**Verdict: pass.** The filter gives the expected 4th-order image rejection at 165.8 kHz.

## 2. DAC 8-tone stress — `dac_inl_sweep.cir`

16-bit quantizer + synthetic INL pattern, 1 LSB amplitude, 7 tones (24 kHz off), per-tone 0.1 V.

| INL pattern cycles | 24 kHz product |
|---|---|
| 1 | −43.4 dBc |
| 3 | −43.7 dBc |
| 7 | −50.0 dBc |
| 17 | −58.0 dBc |
| 31 | −66.5 dBc |
| 127 | −76.2 dBc |
| 511 | −86.3 dBc |
| 1023 | −39.7 dBc |

**Verdict: pattern-dependent; worst case fails −60 dBc.** This is a one-DAC 8-tone stress, not the real system: each driver carries one tone, so its INL produces out-of-band harmonics, not in-band 8-tone products. The result shows that if multiple tones share a DAC (crosstalk), the INL can create in-band products; the real DAC INL/DNL curve or the bench is needed.

## 3. Summer 8-tone IMD — `summer_a3_100/110/120.cir`

7 tones (24 kHz off), per-tone 0.424 V peak (0.3 V RMS, the real summer level after ×2.0103), 3rd-order nonlinearity set for a single-tone THD at that amplitude.

| Single-tone THD at 0.424 V | 24 kHz product | Verdict |
|---|---|---|
| −100 dBc | **−61.9 dBc** | pass, ~2 dB margin |
| −110 dBc | **−71.9 dBc** | pass, ~12 dB margin |
| −120 dBc | **−82.1 dBc** | pass, ~22 dB margin |

The 8-tone product is about **single-tone THD + 38 dB** for this 7-tone case. To meet −60 dBc, the summer/ADC single-tone THD at the operating level must be **≤ −98 dBc**.

The OPA2192/OPA192/AD7768 datasheet THD at 20–34 kHz and 0.4–3.4 V decides whether the design passes. If it is −110 dBc, the summer has ~12 dB margin; if it is only −100 dBc, the margin is ~2 dB.

### Summer gain sweep

The thesis baseline summer gain is 2.0103 (0.3 V RMS per tone). Backing it off reduces the 8-tone peak and the distortion:

| Summer gain | Per-tone peak | 24 kHz product | SNR cost vs 2.0103 |
|---|---|---|---|
| 2.0103 | 0.424 V | −61.86 dBc | 0 dB |
| 1.5 | 0.316 V | −66.96 dBc | −3.1 dB |
| 1.0 | 0.211 V | −73.98 dBc | −6.1 dB |

A 3 dB backoff buys ~5 dB of IMD; a 6 dB backoff buys ~12 dB. The 24-bit ADC has the SNR margin; the summer gain is a design lever, not a fixed 2.0103.

### Datasheet THD check

Read from OPA2192 datasheet Rev. E, Figure 26 (THD+N ratio vs frequency, VOUT = 3.5 V RMS, BW = 80 kHz) and Figure 27 (THD+N vs output amplitude, f = 1 kHz):

- **Figure 26, G = +1, RL = 10 kΩ (blue):** ~−104 dB at 10 kHz, ~−102 dB at 20 kHz, ~−98 dB at 34 kHz at 3.5 V RMS.
- **Figure 27:** at 1 kHz, ~−120 dB at 0.85 V RMS vs ~−108 dB at 3.5 V RMS. The summer’s 8-tone sum is ~0.85 V RMS (0.3 V RMS per tone), so the 20–34 kHz estimate is ~**−114 to −110 dB**, not −105.
- **AD7768-4:** THD = **−120 dB** typical. The ADC is not the limiter.
- At −110 dB summer THD, the 8-tone product is ~**−72 dBc**; at −114 dB, ~**−76 dBc**. That is **12–16 dB margin** at gain 2.0103; gain 1.5 adds ~5 dB more.

The OPA2192 is **not** the 8-tone limiter at the summer’s operating level. The remaining unknown is the DAC INL/crosstalk, not the summer op-amp.




## 4. What this means

- The **M16 DAC/filter/loop per channel is a single-tone path**; it is not the 8-tone bottleneck. The filter AC passes.
- The **8-tone IMD is at the current-sense summer and the pen receiver**, where eight tones meet. The crest factor makes the 8-tone product ~38 dB worse than the single-tone THD.
- **Lever:** reduce the summer gain from 2.0103 to ~1.0–1.5. That backs off the 8-tone peak (currently ~3.4 V of the 4.096 V ADC full scale), buys ~3–6 dB of IMD, and costs 3–6 dB of SNR; the 24-bit ADC has margin.
- **DAC INL** is the remaining unknown; the one-DAC stress is a screen, not the system test. The DAC channel crosstalk and the actual INL/DNL curve matter; the bench is the final gate.

## 5. Next SPICE runs

1. Summer with the **datasheet THD** of OPA2192/AD7768 at 20–34 kHz, not a generic polynomial.
2. Summer at **gain 1.0/1.5** to quantify the backoff trade.
3. Per-channel DAC/filter/loop **single-tone THD at 150 mA**.
4. 8-driver sum at the summer with the real per-tone amplitudes.
5. Bench one-channel 8-tone FFT for the final number.
