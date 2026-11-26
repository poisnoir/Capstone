# Phase 2 — External ADC justification (signal path)

Authoritative math appendix for the decision: **dedicated simultaneous-sampling ADC, not XC7Z010 XADC, for the sensor + current-sense signal path.** The XADC comparison in §2 is historical (that Zynq/PS option was rejected); the locked design is PS-less Artix-7 (#26) with no XADC in the signal path (#9).

Traces to: `docs/phase2/README.md` §§2–6 (specs #1–25), AGENTS.md full-FPGA override, Jaeger 2018 Eq.(3.17)–(3.27), (7.1)–(7.9), `software/anser-matlab-ref/fSysSetup.m`, `user/system/fSysGetField.m`, `user/system/fSysDecodeField.m`.

Default conditions apply throughout: 18–28 °C, no metal within 150 mm, 100:1 scaling, filter on unless stated.

---

## 1. What the ADC must do

Per frame, the solver needs 8 tone amplitudes **and signs** per sensor (`fSysGetField.m:14-48`):

$$
B_i = \mathrm{sign}(\Delta\phi_i)\cdot |Y_i| / A_{sens,i},\quad i = 1..8
$$

$$
\Delta\phi_i = \angle Y_{I,i} - \angle Y_{V,i} - \mathrm{DAQ\_phase}_i
$$

- \(Y_{I}\) = driver-summer current spectrum (ADC **Ch0**, volts, stationary; D3-A/SC-06).
- \(Y_{V}\) = pen-sensor spectrum (ADC **Ch1**, µV–mV, moving; D3-A/SC-06). Ch2 is pen 2 (wired, enabled when built); Ch3 is the reference sensor.
- Cost minimized in `fSysDecodeField.m:14`: \(F(p) = V_d - \kappa\cdot V_m(p)\), \(p = (x,y,z,\theta,\phi)\), bounded LM/TRF with retry \(+[0,0,0,\pi,\pi]\), residual gate 1e-15.

So the ADC carries **phase**, not just magnitude. Any inter-channel skew, drift, or crosstalk lands directly in the orientation sign. Specs at stake:

| Spec (Phase 1 #) | Threshold | ADC link |
|---|---|---|
| #5–6 hand | ≤2 mm / ≤1° on 7×7 grid, RMS Eq.(7.10), 98 pts @85.6/152 mm | tone SNR + phase-sign integrity |
| #9–10 tool | ≤25 µm @100:1 (≤100 µm @20:1) | hand error / S; orientation error leaks into position via solver Jacobian |
| #11 repeatability | ≤10 µm, 10 approaches | frame-to-frame noise floor |
| #12–13 tremor | ≥20 dB @6–12 Hz, ≤3 dB below 1 Hz | 6–12 Hz sidebands must clear spur floor |
| #14–16 latency/rate | ≤20 ms off / ≤100 ms on, ≥100 Hz pose | deterministic integer-J frames, no dropped frame |
| §4 spur budget | spurs ~60–70 dB below tone (recompute with final N/Ac/Iout) | quantization + leakage + crosstalk sum |

---

## 2. Why XC7Z010 XADC fails the signal path

XADC facts (DS190/UG480 class): dual 12-bit SAR, **1 MSPS aggregate shared** across a muxed sequencer (VP/VN + up to 16 aux), 0–1 V unipolar inputs, DRP/AXI readout from PS, no external CONVST edge, sampling-cap kickback into the source.

### 2a. Resolution — kills spur budget, orientation at nulls and edges

Ideal converter SNR:

$$
SNR_{ideal} = 6.02N + 1.76\ \mathrm{dBFS}
$$

12-bit → 74 dBFS ideal; real XADC ENOB ≈ 10–11 → SINAD ≈ 62–68 dB. Budget needs 60–70 dB below tone **before** thermal noise, leakage, and crosstalk are added — XADC arrives with ~0 dB margin.

Tone-to-tone spread inside one frame forces the issue. Position falloff (~\(1/r^3\)) from 85.6 to 152 mm plus calibration-plane offsets:

$$
\left(\frac{152}{85.6}\right)^3 \approx 5.6\times \approx 15\ \mathrm{dB}
$$

plus orientation nulls (\(\hat{n}\cdot B \to 0\) as pitch/yaw approach ±45°) drive individual tones toward zero. Net spread routinely 30–40 dB: the weakest tone lives on ~40–400 LSBs of a 12-bit converter, and a nulled tone on a handful of LSBs.

Phase (hence sign) estimation variance for tone amplitude \(A\) over \(N\)-sample Goertzel/DFT with noise \(\sigma_n\):

$$
\sigma_\phi \approx \frac{\sigma_n}{A\sqrt{N}},\qquad \sigma_n^2 = \sigma_{thermal}^2 + \sigma_{q}^2 + \sigma_{xtalk}^2 + \sigma_{leak}^2
$$

with quantization noise \(\sigma_q = q/\sqrt{12}\), \(q = FSR/2^N\). Shrinking \(A\) (null/edge) while holding \(\sigma_q\) fixed inflates \(\sigma_\phi\) past the sign-decision boundary in `fSysGetField.m:48`. A flipped sign mirrors the solved hemisphere — pitch/yaw error of order tens of degrees on that frame, then LM retry/lock loss. This is exactly where Ch.7 Figs.7.8–7.10 already show the largest errors (volume edges). 16-bit dedicated (98 dBFS ideal, ~88–92 dB real) buys ~25 dB of margin:

$$
\Delta SNR = 6.02\cdot(16-12) \approx 24\ \mathrm{dB}
$$

Processing gain \(PG = 10\log_{10}(N/2)\) (N = 500–2000 → 24–30 dB) helps both converters equally and does not close the 24 dB gap.

**Killed:** #5–6 (orientation ≤1°, edge position), #9–10 (tool error via mis-oriented \(\hat{n}\) in \(V_m(p)\)), #11 (repeatability floor), #12–13 (6–12 Hz sidebands under the spur floor).

### 2b. Mux skew — kills the ≤1° orientation budget directly

XADC samples Ch1 then Ch2 sequentially, \(\Delta t \ge 1\ \mu s\) at 1 MSPS shared (worse with sequencer overhead, averaging, aux channels). Phase skew per tone:

$$
\Delta\phi(f) = 2\pi f\,\Delta t
$$

$$
\Delta\phi(20\ \mathrm{kHz}) \approx 0.126\ \mathrm{rad} \approx 7.2^\circ,\quad \Delta\phi(34\ \mathrm{kHz}) \approx 0.214\ \mathrm{rad} \approx 12.2^\circ
$$

Anser's NI-6216 (also muxed, 400 kS/s) survived only via the per-tone `DAQ_phase_offset = 2πF/400000` calibration (`fSysSetup.m:174`). That correction is valid while \(\Delta t\) is constant. XADC \(\Delta t\) moves with sequencer programming, AXI arbitration, temperature, and supply — drift of just 100 ns is:

$$
2\pi\cdot 34\ \mathrm{kHz}\cdot 100\ \mathrm{ns} \approx 0.0214\ \mathrm{rad} \approx 1.22^\circ
$$

i.e. the **entire** orientation budget consumed by clock-domain slop. The residual gate in `fSysDecodeField.m:27` (1e-15) then rejects frames or converges mirrored, stalling the ≥100 Hz pipeline with retries. A simultaneous-sampling ADC has \(\Delta t \equiv 0\) by construction — no per-tone fudge, no drift term.

**Killed:** #5–6 orientation, #16 rate (retry storms), #14–15 latency (retries blow the ≤20 ms filter-off budget).

### 2c. Shared-cap crosstalk + non-deterministic readout — kills position and rate

Mux kickback: the shared sampling cap retains charge from the previous channel. With Ch1 carrying driver-summer volts (~1 V) and Ch2 carrying sensor µV–mV, first-order crosstalk of −60 dB (typical muxed SAR) injects:

$$
V_{xtalk} \approx 1\ \mathrm{V}\cdot 10^{-60/20} = 1\ \mathrm{mV}
$$

signal-sized on the sensor channel, at the **same** 8 tone frequencies (it is the same waveform, delayed) — indistinguishable from field, unfilterable, and it corrupts \(\kappa\) (which assumes \(V_d\) and current reference are independent measurements of one linear system, Eq.3.26).

Readout path compounds it: XADC data exits via DRP/AXI under PS arbitration. Frame boundaries jitter by microseconds — breaking the integer-J lock between DDS tones and the demod window (frame = J DDS cycles). Non-integer truncation spreads each tone (Dirichlet leakage) into neighbors spaced 2 kHz apart, raising the spur floor 10–20 dB in the worst case and burying the 6–12 Hz tremor sidebands (#12–13). PL-generated START/SYNC with DRDY interrupt and ping-pong BRAM/DMA (see §4) holds determinism; PS-polled XADC cannot.

Throughput is not the blocker (256 kS/s/ch × 512-sample frame = 2 ms acq — fast enough); **determinism** is.

**Killed:** #5–6 position (far-tone corruption), #12–13 tremor, #14–16 (jittered pipeline).

### 2d. Input range and drive

0–1 V unipolar XADC needs the preamp to attenuate/level-shift the sensor path (which natively swings bipolar µV–mV around ground after the E301-class stage) while presenting <100 Ω settling impedance to absorb kickback within 1 µs. That forces a fast, low-noise, high-drive output stage whose own settling crosstalk must still be calibrated — effort better spent on a differential simultaneous ADC with a defined input range (the AD7768-4's ±4.096 V differential) and a purpose-built output stage.

---

## 3. External ADC requirements (any vendor must pass)

| Req ID | Threshold | Math / rationale | Verify |
|---|---|---|---|
| RQ-A1 simultaneous | Ch0 (current), Ch1 (pen 1), Ch2 (pen 2, wired), Ch3 (reference) sampled at the same instant on shared START/SYNC/MCLK; skew ≡ 0 (D3-A/SC-06) | §2b: removes Δφ(f) term entirely; no DAQ_phase_offset drift | two-tone phase test: Δφ flat vs f and temp; channel-skew test |
| RQ-A2 resolution | ≥16 bit, SINAD ≥ 84 dB, THD ≤ −90 dB | §2a: 24 dB over XADC; holds 60–70 dB spur budget with thermal + leakage stacked; AD7768-4 is 24-bit, 107.5 dB SINAD, −120 dB THD | single-tone FFT @25 kHz, −1 dBFS and −40 dBFS; far-tone SNR |
| RQ-A3 rate | ≥250 kS/s/ch sustained (256 kS/s used), no missing codes | N=512 at 256 k = 2.0 ms; N=1024 = 4.0 ms; leaves demod + LM inside 10 ms pose budget (§5) | sustained DRDY capture, code-density histogram |
| RQ-A4 sync | external MCLK ≤32.768 MHz (XO direct); ODR 256 kSPS ceiling; SYNC/START/DRDY; aperture jitter set by the SNR target | \(SNR_j = -20\log(2\pi f t_j)\): 1 ns @34 kHz = 73.4 dB, not 104 dB. For 104 dB at 34 kHz, \(t_j \le 30\) ps. Specify the XO jitter from this (one XO drives MCLK directly, no PLL-generated MCLK — SC-07/#28), not from a 1 ns assumption | clock-phase sweep; integer-J leakage test (§5); jitter measurement |
| RQ-A5 input | differential ±VREF = ±4.096 V (not ±5/±10 V), VCM common mode, Zin ≥1 MΩ, CMRR ≥60 dB | AD7768-4 actual input; the earlier ±5/±10 V wording is stale and superseded; the front end maps the pen signal to ±4.096 V differential around VCM | CMRR sweep 20–34 kHz; Zin vs frequency; full-scale sweep |
| RQ-A6 digital | DCLK/DOUT lanes to PL; DCLK ≤32.768 MHz; on-board 3.3 V board nets on BRD-01, no external header (SC-05b/`icd/adc_fpga.md`); SPI configuration only | \(R_{data}=4\cdot32\cdot256\ \mathrm{k}=32.768\ \mathrm{Mbit/s}\) (D3-A/SC-05b); 4 lanes → 8.192 MHz, 2 lanes → 16.384 MHz; a 2×6 Pmod is too small — rationale for on-board nets (§6) | eye/continuity; sustained lane-rate soak |
| RQ-A7 determinism | DRDY → PL interrupt; ping-pong BRAM/DMA; zero dropped frames at ≥100 Hz | §2c; TL + Tsolv < 10 ms mapped in §5 | 1-hour ≥100 Hz moving-sensor run, drop counter = 0 |

**Locked part: AD7768-4** (simultaneous sigma-delta 24-bit, §9). The §9e shortlist (2× ADS127L11 synced or ADS1278-class) is a vetting fallback if the locked part fails. Fallback: AD7606C-16 (8-ch simultaneous 16-bit 1 MSPS, serial, ±10/±5 V) or TI ADS8688S/ADS85xx equivalents, with the §9a.1 analog-AA verification burden. Single-channel or muxed parts (e.g. AD4004 alone, ADS131M0x-class ≤32 kSPS) do **not** pass RQ-A1/§9c — rejected.

---

## 4. Capacitance / resonance budget the front end must respect

Total shunt across each coil (cable distributed + connector + ADC/preamp input + any intentional tuning cap):

$$
C_{total} = C_{cable} + C_{conn} + C_{amp+ADC} + C_{tune}
$$

Self-resonance must stay a decade above band. With the Phase 2 top tone 34 kHz (`docs/phase2/tone_plan.md`):

$$
f_{res} = \frac{1}{2\pi\sqrt{L\,C_{total}}} > 10\cdot 34\ \mathrm{kHz} = 340\ \mathrm{kHz}
$$

Worst case E + ferrite \(L \approx 3\ \mathrm{mH}\):

$$
C_{max} = \frac{1}{(2\pi\cdot340\ \mathrm{kHz})^2\cdot 3\ \mathrm{mH}} \approx 73\ \mathrm{pF}
$$

**Recalculated 2026-11-26** (number-for-number agreement with `tone_plan.md` §6).
With \(f_{res}\ge10\times34=340\) kHz and worst-case coil E + ferrite
\(L\approx3\) mH (Jaeger Table 7.1 as quoted in AGENTS.md; thesis local-only,
coil value not re-derived here):
\[
C_{max}=\frac{1}{(2\pi\cdot340\times10^3)^2\cdot3\times10^{-3}}
=73.04\ \mathrm{pF}\approx73\ \mathrm{pF}\ (3\ \mathrm{s.f.})
\]
Air coils at the same threshold: B 804 µH → \(1/((2\pi\cdot340\times10^3)^2\cdot804\times10^{-6})=272.5\) pF ≈ 272 pF; C 91 µH → 2.41 nF. Both pass trivially; the 350 pF figure in the point-in-time flowchart handoff is stale.

**Preamp-input stack (derivation replaces the unsourced "10 pF"):**

- INA163: TI datasheet SBOS177D (Rev. D, May 2005), p.3 Electrical Characteristics, INPUT IMPEDANCE — Differential 60 MΩ ‖ **2 pF**, Common-Mode 60 MΩ ‖ **2 pF** (typ). Fetched from `https://www.ti.com/lit/ds/symlink/ina163.pdf` on 2026-11-26; the REF-08 local datasheet cache is absent on this machine. → 2 pF directly across the two inputs, 2 pF from each input to ground.
- BAS70H dual Schottky clamps: two diodes per leg, each ≤2 pF at 0 V / 1 MHz → **4 pF per leg** to the ±12 V rails (AC ground) (`hardware/brd-01/kicad/bom-to-cad.md`:530; Nexperia BAS70H data sheet). Mapping to the differential shunt the coil sees: two equal 4 pF legs to ground are in series across the coil → 2 pF when the legs are symmetric; if one leg is held at AC ground by its 10 kΩ bias return, that leg's full 4 pF appears across the coil (worst case).
- 100 Ω series per leg (`system_schematic.md` §5.1) adds no shunt capacitance; \(X_C(4\ \mathrm{pF}@34\ \mathrm{kHz})\approx1.17\ \mathrm{M\Omega}\gg100\ \Omega\), so the clamp capacitance is essentially fully across the link. The 10 µF coupling caps are ~0.47 Ω at 34 kHz and do not reduce it.
- Sum: symmetric = 2 (INA diff) + 1 (INA common-mode pair in series) + 2 (clamp pair in series) = 5 pF; worst leg = 2 + 2 + 4 = 8 pF; plus 2 pF board-pad/layout allowance → **\(C_{preamp}=10\) pF allocation**, inside FE-01's ≤20 pF gate with 10 pF headroom. Verify on the assembled BRD-01 pen channel.

\[
C_{cable}=73.04-10\ (\mathrm{conn,\ RQ\!-\!C3})-10\ (\mathrm{preamp})=53.04\ \mathrm{pF}\approx53\ \mathrm{pF}.
\]

SC-05c's "56 pF cable budget" was corrected to 53 pF and locked by decision #34 (contract 1.1.3); no contract change is pending. The filed W2697 0.6 m whip is \(0.6\times65=39\) pF cable, 59 pF with the 20 pF terminations: it passes the 53 pF cable line by 14 pF (total \(f_{res}\approx378\) kHz). Maximum compliant length at 65 pF/m is \(53.04/65=0.816\) m; the 0.8 m alternate is 52 pF cable / 72 pF total (\(f_{res}\approx342\) kHz), with only 1 pF of cable margin — it passes only if \(C_{tune}\approx0\) and is not worst-case robust. Topology: the capacitance seen by the coil is cable + connector + **preamp input** (+ tuning cap); the ADC's switched-cap input sits after the preamp and is a separate drive requirement in FE-4/ADC-5. The earlier "ADC \(C_{in}\)" wording conflated the two; the ADC's external RC/charge reservoirs are not directly across the coil. Any preamp above the 20 pF gate must be re-budgeted; `connector_requirements.xlsx` Rev D and `BOM_PEN-ANA-01.xlsx` Rev 0.03 still quote the stale cable allocation — file-owner follow-ups, not contract changes.

---

## 5. Latency / rate budget the ADC must fit

Anser baseline (`fSysSetup.m:146-149`: Fs = 100 kS/s, N = 5000) spends 50 ms in acquisition alone → ~20 Hz max (Ch.3 Table 3.4) — incompatible with ≥100 Hz pose and ≤20 ms filter-off latency.

Filed budget (filter off, worst case):

$$
T_{pose} = T_{acq} + T_{demod} + T_{solv} < 10\ \mathrm{ms}
$$

$$
T_{acq} = N/F_s:\quad 512/256\ \mathrm{k} = 2.0\ \mathrm{ms}\quad (1024/256\ \mathrm{k} = 4.0\ \mathrm{ms})
$$

The AD7768-4 tops out at 256 kSPS, so the earlier 500 kSPS examples are stale. The Phase 2 tone plan (`docs/phase2/tone_plan.md`) uses 2 kHz spacing and N=512, which restores the 2.0 ms acquisition budget; the 1 kHz plan would need N=1024 for the Hamming fallback (4.0 ms), or N=512 rectangular with only 2-bin spacing. This leaves ~8 ms for streaming Goertzel demod (parallel per-tone, PL) + bounded LM/TRF (relaxed TolFun, warm-started from MA filter `fSysSetup.m:204-205`, ping-ponged with acquisition). Integer-J framing (frame = J DDS cycles, Fs = Fclk/N from the one 32.768 MHz XO; ADC ODR = XO ÷128, SC-07/#28) keeps Goertzel bins leakage-free; the AD7768-4 `SYNC`/`START` and `DRDY` frame boundaries are the actuators of that lock — it has no `CONVST` pin.

---

## 6. Digital lane math (physical + PL)

A 2×6 Pmod is a physical 100 mil, 3.3 V connector with 8 I/O. The AD7768-4 data path is **not SPI**: it outputs 24-bit data on DOUTx lanes synchronous to DCLK, framed by DRDY; SPI is configuration only. PL implements: one-time `START`/`SYNC` at startup, DCLK capture of the DOUT lanes, DRDY-gated frame ping-pong → BRAM. There is no PS on BRD-01 (#26); nothing is bit-banged at rate.

Data rate (4 active channels per D3-A/SC-05b, 32-bit frames, 256 kSPS):

$$
R_{data} = 4\cdot32\cdot256\ \mathrm{k} = 32.768\ \mathrm{Mbit/s}
$$

4 DOUT lanes → DCLK 8.192 MHz; 2 lanes → 16.384 MHz. A 2×6 Pmod has 8 I/O; 4 DOUT + DCLK + DRDY + SYNC/START + MCLK + RESET already needs 10 signals before SPI configuration — that is why these are board nets on BRD-01, not an external header (SC-05b/`icd/adc_fpga.md`). FMC/LVDS is not needed at this rate.

---

## 7. XADC housekeeping — historical Zynq comparison only

In the rejected XC7Z010/Zynq option, the XADC would have handled slow DC
housekeeping (die temperature, rail monitors, static field-probe level,
interlock comparators), never the 20–30 kHz signal path or the pose loop. The
locked design has no PS and does not use the 12-bit XADC (#9/#26).

---

## 8. Verification hooks (Phase 2 §6 rows)

- Single/dual-tone FFT per RQ-A2 at −1 and −40 dBFS; far-tone (attenuated 40 dB) SNR and sign stability over temperature (RQ-A1).
- Skew sweep: Δφ vs f flat within ±0.1° (RQ-A1); the AD7768-4 is simultaneous, so mux skew is zero. Aperture jitter: measure rms; 1 ns at 34 kHz = 73.4 dB, 30 ps for 104 dB (RQ-A4).
- Integer-J on/off: rectangular vs Hamming leakage/spur delta ≥10 dB (§5, `docs/phase2/tone_plan.md`).
- 1-hour ≥100 Hz moving-sensor run: zero dropped frames, arm-motion STOP / tracking-lost arm halt ≤100 ms with field, DDS/DAC and pose continuing (#30) (RQ-A7, specs #16–17).
- \(C_{total}\) LCR + \(f_{res}\) sweep 20–500 kHz per coil ( §4).
- 7×7 κ grid + 98-pt RMS Eq.(7.10) as the acceptance gate for the whole chain (#5–6).

---

## 9. Architecture decision: sigma-delta (locked) vs SAR vs XADC

**Decision (2026-10-16): external simultaneous sigma-delta (24-bit class) for the signal path.** SAR simultaneous (e.g. AD7606C-16 class) is retained as the documented fallback. XADC is rejected (#9); its §2/§7 housekeeping discussion is historical, not a live path.

### 9a. The load-bearing difference: where the anti-alias filter lives

A SAR samples at \(F_s\) and keeps everything below \(F_s/2\) — including wideband preamp noise folded back onto the 8 tones. The analog anti-alias (AA) filter in front of a SAR must therefore be flat to 34 kHz and fully down before \(F_s/2\) (e.g. −80 dB at 128 kHz for \(F_s = 256\) kS/s): a 5th–6th-order matched pair, one per channel.

A sigma-delta oversamples at MHz modulator rate and applies its **digital** decimation filter on-chip. The analog AA collapses to a single RC pole (out-of-band shaped noise is removed digitally). Two consequences decide this for the pen link:

1. **Phase-match for free.** The demod needs \(\Delta\phi_i\) per tone to ±0.1° (§8). Two analog AA filters built from 1%-tolerance parts mismatch in corner frequency by ~1%, and near-corner phase slope converts that directly into inter-channel skew. For a 2nd-order section with \(f_c = 100\) kHz, phase at 34 kHz is:

$$
\phi(f) = -\tan^{-1}\!\left(\frac{f/f_c}{Q(1-(f/f_c)^2)}\right) \;\approx\; -29^\circ\ \mathrm{at}\ 34\ \mathrm{kHz}
$$

and \(d\phi/df_c\cdot 1\%\) mismatch lands at \(\sim 0.3\)–\(0.5^\circ\) per section — two cascaded sections plus temperature drift consume the whole ≤1° orientation budget (#5–6) before the ADC contributes anything. Sigma-delta digital decimation filters on Ch1/Ch2 are bit-identical arithmetic: mismatch ≡ 0 by construction, over temperature, forever. The only analog phase left is one RC pole per channel (set a decade out, ~2.8° absolute, matched to resistor tolerance and stable since both channels share the same reel/batch).

2. **Quantization disappears as a design variable.** 24-bit FS: \(SNR_{ideal} = 6.02\cdot24+1.76 \approx 146\) dBFS; real ENOB 17–20 at speed → 104–122 dB. Against the §2a requirement (~80 dBFS + margin): quantization noise sits 25–40 dB below the analog chain floor (preamp \(e_n\)-dominated ≈ 60 dB over 5 kHz BW), so frame-shortening for latency (small \(N\), less processing gain \(PG = 10\log_{10}(N/2)\)) never exposes a quantization wall. With 16-bit SAR the same move costs real margin: halving \(N\) from 1000→500 loses 3 dB of PG against a 90 dB-real converter already 20 dB closer to the spur floor.

### 9b. What happens if SAR (the fallback)

A simultaneous SAR (AD7606C-16 class: 8-ch simultaneous, 16-bit, 1 MSPS, serial) **passes** RQ-A1–A7 as written and would track: zero group delay (~µs conversion), exact sample-instant locking, simpler timing, and a lower interface rate than the locked 32-bit path (§6/§9c: 4 channels, 32.768 Mbit/s, 8.192 MHz on 4 lanes / 16.384 MHz on 2). Cost of choosing it:

- Design, match, and temperature-qualify the 5th–6th-order analog AA pair whose phase mismatch analysis above becomes a Phase 2 deliverable with measured drift data (extra fab + test weeks on the fast-buildable schedule).
- ~20 dB less headroom on null/edge tones and short frames (§9a.2); the ≤1° orientation spec then depends on per-tone analog-phase calibration holding over 18–28 °C — the same drift class that already threatens \(\kappa\).
- Muxed SAR variants reintroduce §2b–2c verbatim and do **not** qualify as fallback; only simultaneous-SAR counts.

Fallback trigger: sigma-delta vetting fails any of RQ-A1 (no simultaneous multi-channel part in stock), §9c delay (>0.5 ms), or lane/power limits — then AD7606C-16 class with the AA pair becomes the locked part and §9a.1 becomes its verification burden.

### 9c. Sigma-delta costs, bounded

- **Group delay is constant, not jitter.** Decimation delay \(D = N_{taps}/ODR\) (AD7768-4 wideband: 34/256 kSPS ≈ 133 µs) shifts every frame equally; it is subtracted once as a fixed timestamp offset in the pose log. Requirement: \(D < 0.5\) ms so \(T_{acq} + D\) stays inside the §5 <10 ms budget. Verify per datasheet filter tables at the chosen ODR — wideband/sharp modes trade taps for droop; FDM absorbs stable droop into per-tone \(\kappa\) (§1: one \(\kappa\) per coil-frequency), so prefer the lowest-delay mode whose droop is stable over temperature.
- **ODR floor is hard:** passband must cover 34 kHz with margin → ODR ≥ ~4×34 ≈ 136 kSPS. The AD7768-4 fast mode (256 kSPS) meets this; parts capped at 32 kSPS (e.g. ADS131M0x class) are rejected without further review.
- **Lane floor rises with word length:** 4 active ch × 32-bit frames (24 data + status) × 256 kSPS over 2 lanes:

$$
R_{data} = 4\cdot32\cdot256\ \mathrm{k} = 32.768\ \mathrm{Mbit/s}\quad(16.384\ \mathrm{MHz\ on\ 2\ lanes})
$$

Use 4 DOUT lanes at 8.192 MHz where possible; 2 lanes at 16.384 MHz is still within the AD7768-4 DCLK limit. The data path is DCLK/DOUT, not SPI; a 2×6 Pmod is too small (see §6).

- **Power/price:** SD modulators + MCLK tree draw more than SAR equivalents and 24-bit simultaneous parts cost more per channel; both fit the ≤1000 CAD/pair envelope at prototype qty (verify at BOM time) and neither touches the pen mass budget (preamp-box parts).

### 9d. What happens if XADC (recap — not an option)

§2a–2d stand: ~65 dB real SINAD against a 60–70 dB spur budget (kills #5–6/#11/#12–13), 7–10° mux skew with 100 ns = 1° drift (kills ≤1°), −60 dB shared-cap crosstalk injecting 1 mV of driver waveform into the sensor channel (kills #5–6), AXI-jittered frames breaking integer-J lock (kills #14–16). XADC: rails/temp/static-probe DC only (§7).

### 9e. Vetting gate before any sigma-delta BOM row

Candidate must show, from datasheet + bench: simultaneous modulators with shared START/CLK; ODR ≥ 250 kSPS preferred (136 k hard floor for 34 kHz); \(D < 0.5\) ms in the selected filter mode; droop at 34 kHz stable ±0.05 dB over 18–28 °C (else it escapes \(\kappa\)); preamp input capacitance ≤20 pF into the §4 coil budget (ADC input network drive verified separately); DCLK/DOUT lanes sustaining §9c rate; in-stock at an approved supplier. Shortlist: 2× ADS127L11 synced (24-bit, to 400 kSPS) or 1× ADS1278 (8-ch simultaneous, to 144 kSPS, marginal headroom).
