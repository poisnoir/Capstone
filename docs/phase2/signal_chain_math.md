# Phase 2 — Signal-chain math: excitation to (x, y, z)

**Purpose.** One reference for the equations between the DAC word and the 5-DOF pose.
Every number is sourced (`path:line` or `path §N`) or derived here from sourced
inputs; derived values are marked *derived*. No design decision is reopened.
Where two frozen documents disagree, §10 records the disagreement and this file
follows the higher-authority source (`contract/` > `AGENTS.md` > `docs/phase2/` > handoffs).

Sources of authority for this file: `AGENTS.md` (Jaeger 2018 reference model and
Eq. numbers), `contract/system_contract.md` (SC-01…SC-10),
`contract/decisions_log.md` (#19, #23, #27, #28, #33, #34),
`contract/icd/dac_fpga.md`, `docs/handoff/solver-algorithm-handoff.md` §3–4
(frozen golden formulation and FPGA numerics), and the frozen Phase 2 design
record listed per row below.

---

## 0. Purpose, conventions, symbol table

**Frames and units.** The **FG/coil frame** is the measurement frame: origin at
the geometric centre of the FG PCB, \(z=0\) on its top surface, \(+z\) normal
toward the pen, right-handed, SI (`contract/system_contract.md` SC-01a). The
**pen body frame** carries the sensor coil; only its coil-axis direction
\(\hat n\) is observed, expressed in the FG frame. Fields, currents and tone
amplitudes are RMS unless stated; frames are \(N=512\) ADC samples
(`contract/system_contract.md` SC-09, SC-03). Angles in equations are radians;
degree values are labelled.

**Symbols.**

| Symbol | Meaning | Source |
|---|---|---|
| \(f_i, J_i\) | tone \(i\) frequency (Hz) and integer DFT bin | `docs/phase2/tone_plan.md` §4 |
| \(f_{DDS}=32.768\) MHz, \(f_{DAC}=199.805\) kSPS, \(F_s=256\) kSPS | common-clock rates | `contract/system_contract.md` SC-07 |
| \(W=32\), \(\Delta\Phi_i\) | DDS accumulator width, phase increment | `docs/phase2/dig6_requirements.md` §1 |
| \(\tilde I_i=|I_i|e^{j\phi_i}\) | coil-current phasor at tone \(i\) | §1 below |
| \(\mathbf{a},\mathbf{b},\mathbf{c}\) | filament segment vectors, §2 | `software/anser-matlab-ref/model/spiralCoilFieldCalcMatrix.m:19-29` |
| \(\mathbf b_i(\mathbf p)\) | unit-current filament field of coil \(i\) at pose \(\mathbf p\) | §1, §2 |
| \(\theta,\phi\) | polar angle from \(+z\) and azimuth from \(+x\) toward \(+y\); \(\hat n=[\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta]\) | `AGENTS.md`; `docs/phase2/calibration_tooling.md` §1; Eq.(3.19)–(3.25) in §3 |
| \(A_{sens,i}\) | pen+amp sensitivity, V/T, per tone | `docs/phase2/calibration_tooling.md` §1 |
| \(\kappa_i\) | per-coil/tone scale from the 7×7 fit | `docs/handoff/solver-algorithm-handoff.md` §3 |
| \(Y_{I,i},Y_{V,i}\) | Goertzel phasors: summed current (Ch0), pen (Ch1) | `docs/phase2/dig6_requirements.md` §4 |
| \(\mathbf p=(x,y,z,\theta,\phi)\) | 5-DOF pose | `docs/handoff/solver-algorithm-handoff.md` §3 |

**Angle/sign conventions.** Positive \(I_i\) follows the filament direction
\(\mathbf a=\text{end}-\text{start}\) in the golden coil geometry
(`software/anser-matlab-ref/model/spiralCoilFieldCalcMatrix.m:19-21`).
Tone phase is measured against the common XO; the phase reference is Ch0, the
summed current sense (`docs/phase2/tone_plan.md` §4). The golden phase
difference is \(\Delta\phi_i=\angle Y_{I,i}-\angle Y_{V,i}-\mathrm{DAQ\_phase}_i\)
(`software/anser-matlab-ref/user/system/fSysGetField.m:29`), wrapped to
\([-\pi,\pi]\) before its sign is taken (lines 34–43). ADC group delay is a fixed
per-tone rotation, absorbed into the calibration rotation, not re-estimated per
frame (`docs/phase2/tone_plan.md` §5; `docs/phase2/dig6_requirements.md` §4).

**End-to-end map.** A 32-bit DDS at 32.768 MHz generates eight exact integer-J
tones; one DAC80508 channel per tone is clamped to 0.3–4.6 V, filtered by an
LTC1563-2 and driven as a regulated coil current. That current produces a
quasi-static field computed by a sum of straight filaments; the pen coil converts
the component along its axis to an EMF proportional to \(\omega\), which the
INA163/ADA4940-2 front end maps into the AD7768-4's ±4.096 V differential input.
The FPGA captures \(N=512\) simultaneous samples, runs one Goertzel per
tone/channel, reduces each tone to a signed amplitude using the Ch0 phase sign
and \(A_{sens}\), and minimises an 8-residual least-squares cost against the
filament model to obtain \((x,y,z,\theta,\phi)\). No PC solver is in the loop
(`AGENTS.md`; `docs/handoff/m16-fpga-handoff.md` §1.1).

| Block | Governing equation | Source |
|---|---|---|
| DDS / DAC | \(\Delta\Phi_i=2^W f_i/f_{DDS}\); \(c_{16}=\mathrm{round}(V\cdot2^{16}/5)\) | §1 |
| Reconstruction / driver | \(\lvert H(f)\rvert=[1+(f/f_c)^8]^{-1/2}\); \(\tilde I_i=I_i e^{j\phi_i}\) | §1 |
| Field | \(\mathbf B(\mathbf p)=\sum_i\tilde I_i\,\mathbf b_i(\mathbf p)\), filament sum | §2 |
| Sensor | \(\tilde V_i=-j\omega_i\mu_a N A\,\mathbf B_i\!\cdot\!\hat n\) | §3 |
| Front end / ADC | \(V_{ADC}=G_{FE}\tilde V_i\); \(k_{ADC}=\mathrm{round}(V_{ADC}2^{24}/8.192)\) | §4 |
| Demod | Goertzel recurrence; \(B_i=\operatorname{sign}(\Delta\phi_i)\lvert Y_{V,i}\rvert/A_{sens,i}\) | §5 |
| Solve | \(\min_{\mathbf p}\lVert \mathbf V_d-\kappa\odot\mathbf V_m(\mathbf p)\rVert^2\), \(lb\le\mathbf p\le ub\) | §6 |

---

## 1. Excitation / field generation

**Tone plan.** Eight tones \(f_i=2\,\mathrm{kHz}\cdot k\), \(k=10\ldots17\);
\(F_s=256\) kSPS, \(N=512\), bin width \(F_s/N=500\) Hz, so \(J_i=f_i/500\) is
integer (`docs/phase2/tone_plan.md` §1, §4; `contract/system_contract.md` SC-03).
The DDS clock and ADC ODR are integer divides of one 32.768 MHz XO
(`contract/system_contract.md` SC-07, decision #28).

| \(i\) | \(f_i\) (kHz) | \(J_i\) (derived: \(f_i N/F_s\)) | FTW \(\Delta\Phi_i=k\cdot262144\) | DAC channel / coil |
|---|---|---|---|---|
| 1 | 20 | 40 | 2,621,440 (0x00280000) | A / 1 |
| 2 | 22 | 44 | 2,883,584 (0x002C0000) | B / 2 |
| 3 | 24 | 48 | 3,145,728 (0x00300000) | C / 3 |
| 4 | 26 | 52 | 3,407,872 (0x00340000) | D / 4 |
| 5 | 28 | 56 | 3,670,016 (0x00380000) | E / 5 |
| 6 | 30 | 60 | 3,932,160 (0x003C0000) | F / 6 |
| 7 | 32 | 64 | 4,194,304 (0x00400000) | G / 7 |
| 8 | 34 | 68 | 4,456,448 (0x00440000) | H / 8 |

Source: `docs/handoff/m16-fpga-handoff.md` §3 and §4.3;
`docs/phase2/dig6_requirements.md` §1. FG-1 may reassign coil→tone; the tone set
and spacing are fixed (`docs/phase2/tone_plan.md` §4).

**Integer-J / leakage-free condition.** For a rectangular observation of length
\(N\), \(X[J]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi Jn/N}\). A tone at bin \(J_i\) gives
\(\sum_{n=0}^{N-1}e^{j2\pi(J_i-J)n/N}=N\delta_{J,J_i}\); hence zero tone-to-tone
leakage when \(J_i=f_iN/F_s\) is integer. Rectangular main lobe 0.89 bins
(−3 dB), 1.11-bin (555 Hz) margin to the 2-bin half-spacing
(`docs/phase2/tone_plan.md` §1, §4; thesis §3 Eq.3.14 cited there).

**DDS and DAC mapping.** The accumulator is \(W=32\) bits at 32.768 MHz:

$$
\Delta\Phi_i=\operatorname{round}\!\left(\frac{2^{W}f_i}{f_{DDS}}\right)
=\operatorname{round}\!\left(\frac{2^{32}\,k\cdot2\,\mathrm{kHz}}{32.768\,\mathrm{MHz}}\right)
=k\cdot262144,\quad k=10\ldots17 .
$$

Source: `docs/phase2/dig6_requirements.md` §1. Exact integers ⇒ no fractional
word, no DDS/ADC beat, no per-frame phase reset (`docs/phase2/dig6_requirements.md` §1;
`contract/system_contract.md` SC-07). One shared 4096×16 sine LUT with 12-bit
phase truncation, 16-bit per-tone amplitude and phase words; truncation spurs
≈72 dBc, below the −60 dBc spur budget (`docs/phase2/dig6_requirements.md` §2 DIG-01a/b).
The 16-bit amplitude quantisation step at the DAC part span is

$$
q_{DAC}=\frac{5\ \mathrm V}{2^{16}}=76.3\ \mu\mathrm V,\qquad
SNR_{ideal}=6.02\cdot16+1.76=98.1\ \mathrm{dBFS},
$$

derived from the span (`contract/icd/dac_fpga.md` §3) and the ideal-converter
relation (`docs/phase2/adc_justification.md` §2a). Code mapping is
\(c_{16}=\operatorname{round}(V\,2^{16}/5)\); the part span is 0–5 V but the
locked firmware tone band is **0.3–4.6 V, centre 2.45 V**, ≤92 % FS
(decision #33; `contract/icd/dac_fpga.md` §3):

| DAC voltage | Code (derived, \(V\cdot2^{16}/5\)) | Note | Source |
|---|---|---|---|
| 2.5 V | 32,768 | part power-on midscale, not the operating centre | `contract/icd/dac_fpga.md` §3 |
| 2.45 V | 32,113 | locked tone centre | decision #33 |
| 0.3 / 4.6 V | 3,932 / 60,293 | locked clamp | decision #33 |

DAC update \(f_{DAC}=32.768\,\mathrm{MHz}/164=199.805\) kSPS (5.005 µs);
8×24-bit data + a 24-bit TRIGGER frame = 216 bits = 4.394 µs at
49.152 MHz (`contract/system_contract.md` SC-07; `contract/icd/dac_fpga.md` §2).

**Reconstruction filter.** One LTC1563-2 per channel, 4th-order Butterworth,
60 kHz nominal. With the application resistor relation
\(f_c(\mathrm{kHz})=2560/R(\mathrm{k}\Omega)\), the 60 kHz target gives
\(R=10\,\mathrm{k}\Omega\cdot256/60=42.67\,\mathrm{k}\Omega\); the filed
42.7 kΩ gives \(f_c=2560/42.7=59.95\) kHz (−0.08 %)
(`docs/handoff/m16-fpga-handoff.md` §5;
`docs/phase2/brd01_value_justification.md:135`;
`hardware/brd-01/kicad/bom-to-cad.md:442`). For an ideal 4th-order Butterworth,

$$
|H(f)|=\frac{1}{\sqrt{1+(f/f_c)^8}},\qquad
A_{img}(f_i)=-10\log_{10}\!\left[1+\left(\frac{f_{DAC}-f_i}{f_c}\right)^8\right].
$$

*Derived from the locked order and \(f_c\), checked against the SPICE result.
With \(f_c=60\) kHz the top-tone image at \(199.805-34=165.805\) kHz gives
\(-35.3\) dB, matching `simulations/m16/FINAL_REPORT.md` §3.1 (−35.3 dB);
the lowest-tone image at 179.805 kHz gives −38.1 dB. Filter phase at 34 kHz is
−89.6° (report §3.1) and is absorbed by per-tone κ.*

**Current driver.** Closed-loop transconductance (LMH6321-class, single +15 V,
AC-coupled) with 150 mA prototype / 250 mA nominal / 500 mA max and current
error ≤0.1 % (`docs/phase2/driver_power_requirements.md` §1 DRV-02/03, §2;
decision #11). The locked FG coil is 79 µH / 2.9 Ω (decision #27), while the
SPICE/thesis model load is 70 µH + 2 Ω; at 34 kHz the latter gives
\(\lvert Z\rvert=15.1\ \Omega\) (`docs/phase2/tone_plan.md` §6) and the former
gives \(\lvert Z\rvert=\sqrt{2.9^2+(2\pi\cdot34\,\mathrm{kHz}\cdot79\,\mu H)^2}
=17.1\ \Omega\) (*derived*), i.e. 4.28 V RMS / 6.05 V peak at 250 mA, inside the
7.5 V single-rail swing. Loop phase margin ≥45° at 34 kHz is a bench gate;
the thesis reports 15° at 30 kHz uncompensated
(`docs/phase2/driver_power_requirements.md` §1 DRV-03;
`simulations/m16/FINAL_REPORT.md` §3.6, §7). Per tone define the current phasor
\(\tilde I_i=|I_i|e^{j\phi_i}\), where \(\phi_i\) includes filter and loop phase.

**Linearity and unit-current field.** The filament model is linear in current,
so for a fixed pose \(\mathbf p\),

$$
\mathbf B(\mathbf p)=\sum_{i=1}^{8}\tilde I_i\,\mathbf b_i(\mathbf p),
\qquad
\mathbf b_i(\mathbf p)=\sum_{\text{segments}}\frac{\mu_0}{4\pi}
\frac{\mathbf c\times\mathbf a}{|\mathbf c\times\mathbf a|^2}
\left(\frac{\mathbf a\!\cdot\!\mathbf c}{|\mathbf c|}
-\frac{\mathbf a\!\cdot\!\mathbf b}{|\mathbf b|}\right).
$$

Source: §2 and `software/anser-matlab-ref/model/spiralCoilFieldCalcMatrix.m:47-54`.

---

## 2. Forward field model (what the hardware must compute)

**One straight filament.** With segment endpoints \(\mathbf p_0,\mathbf p_1\)
and observation point \(\mathbf P\), the golden definitions are
\(\mathbf a=\mathbf p_1-\mathbf p_0\), \(\mathbf b=\mathbf p_1-\mathbf P\),
\(\mathbf c=\mathbf p_0-\mathbf P\)
(`software/anser-matlab-ref/model/spiralCoilFieldCalcMatrix.m:19-29`).
Thesis Eq.(3.17)–(3.18) (Jaeger 2018, citing Sonntag 2007) gives, with
\(\mu_0=4\pi\times10^{-7}\) (`fSysSetup.m:25`),

$$
\mathbf H_{\text{seg}}=\frac{I}{4\pi}\,
\frac{\mathbf c\times\mathbf a}{|\mathbf c\times\mathbf a|^2}
\left(\frac{\mathbf a\!\cdot\!\mathbf c}{|\mathbf c|}
-\frac{\mathbf a\!\cdot\!\mathbf b}{|\mathbf b|}\right),
\qquad \mathbf B=\mu_0\mathbf H .
$$

**rsqrt-friendly form** (frozen for HDL; no divides):

$$
\mathbf B_{\text{seg}}=\frac{\mu_0 I}{4\pi}\,(\mathbf c\times\mathbf a)\,r_s^2
\left((\mathbf a\!\cdot\!\mathbf c)\,r_c-(\mathbf a\!\cdot\!\mathbf b)\,r_b\right),
$$

with \(r_b=\operatorname{rsqrt}(|\mathbf b|^2)\),
\(r_c=\operatorname{rsqrt}(|\mathbf c|^2)\),
\(r_s=\operatorname{rsqrt}(|\mathbf c\times\mathbf a|^2)\): three rsqrt and
one square per segment, versus two `sqrt` plus three divides in the golden form
(`docs/handoff/solver-algorithm-handoff.md` §4). Cost ≈30 MAC/segment;
800 segments/evaluation (8 coils × 25 turns × 4 traces = 8×100), 24 kMAC/eval
(`docs/phase2/dig6_requirements.md` §5 DIG-04b;
`docs/handoff/solver-algorithm-handoff.md` §5;
`simulations/field_jacobian.py` geometry helper).

**Dipole warning.** The dipole expression Eq.(3.15) is invalid close to these
large planar coils; use the filament model Eq.(3.17)–(3.18) everywhere in the
100–200 mm volume (`AGENTS.md` gotchas;
`docs/phase2/dig6_requirements.md` §5 DIG-04b).

**Sensor-side material.** Ferrite core (3C90, \(\mu_r\approx2300\), 12×6 mm)
adds ≈+10 dB flux gain but introduces nonlinearity and Barkhausen noise,
Eqs.(7.5)–(7.7) (`AGENTS.md`; `docs/phase2/README.md` §4). PEN-3 locks coil B
**air-core**, \(\mu_a=1\), so Eqs.(7.5)–(7.7) are not used in the current model;
they apply only if a ferrite variant is reinstated
(decision #4; `docs/phase2/pen_link_budget.md` Assumptions, §4).

**Sensitivity / Jacobian.** Only \(\mathbf P\) varies in the segment kernel;
\(\mathbf a\) is fixed. Since \(\mathbf c-\mathbf b=-\mathbf a\),
\(\mathbf q=\mathbf c\times\mathbf a=\mathbf b\times\mathbf a\) is independent
of \(\mathbf P\). For coordinate \(P_j\in\{x,y,z\}\) (*derived from the above
kernel*):

$$
\frac{\partial}{\partial P_j}\!\left(\frac{\mathbf a\!\cdot\!\mathbf c}{|\mathbf c|}
-\frac{\mathbf a\!\cdot\!\mathbf b}{|\mathbf b|}\right)
= -a_j(r_c-r_b)+(\mathbf a\!\cdot\!\mathbf c)c_j r_c^3
-(\mathbf a\!\cdot\!\mathbf b)b_j r_b^3 ,
$$

so \(\partial\mathbf B/\partial P_j\) reuses the same per-segment intermediates.
The analytic-Jacobian design and its cost (≈3 model evaluations/iteration
versus 6 for forward differences) are specified in
`docs/handoff/solver-algorithm-handoff.md` §4; the golden checks the model
against `simulations/field_jacobian.py` (§9).

---

## 3. Sensing / receiving

**Point-sensor flux.** Thesis Eq.(3.19)–(3.25) gives the point-coil
approximation

$$
\Phi=\mu_a\,\mathbf B\!\cdot\!A\hat n,\qquad
\hat n(\theta,\phi)=[\sin\theta\cos\phi,\ \sin\theta\sin\phi,\ \cos\theta],
$$

valid only for a coil whose cross-section is small relative to the field
variation scale (`AGENTS.md`; `docs/phase2/calibration_tooling.md` §1). For a
large coil, the integrated form Eq.(7.2) must be used instead; PEN-3 does not
re-derive it here (`AGENTS.md`; `docs/phase2/README.md` §4).

**EMF and the signed amplitude.** With
\(\Phi(t)=\Re\{\tilde\Phi e^{j\omega t}\}\),

$$
\tilde V=-\frac{d\Phi}{dt}=-j\omega\tilde\Phi
\;\Rightarrow\;
|\tilde V|=\omega\,\mu_a A\,|\mathbf B\!\cdot\!\hat n|,
\qquad \frac{V}{T}=N A\omega\mu_a .
$$

The factor \(-j\) rotates every pen tone by the same −90°; the current sense
Ch0 has a different fixed transfer phase. Therefore
\(\Delta\phi_i=\angle Y_{I,i}-\angle Y_{V,i}-\mathrm{DAQ\_phase}_i\) equals the
angle of \(\mathbf B\!\cdot\!\hat n\) plus a fixed offset (the −90°
differentiation, filter/loop phase and DAQ calibration rotation). Reversing
\(\mathbf B\!\cdot\!\hat n\) reverses \(Y_V\)
by \(\pi\) and therefore flips \(\operatorname{sign}(\Delta\phi_i)\) while
leaving \(|Y_V|\) unchanged. That is the physical origin of the eight **signed**
real amplitudes and the reason no complex residual is needed
(`software/anser-matlab-ref/user/system/fSysGetField.m:22-48`;
`docs/handoff/solver-algorithm-handoff.md` §3; §5 below).

**Constants that enter the transfer function.** Cited values, no re-derivation:

| Constant | Value | Where it enters | Source |
|---|---|---|---|
| Coil B turns, geometry | \(N=319\); ID/OD 11/14.1 mm; \(NA=3.95\times10^{-2}\) m² | \(V/T=NA\omega\mu_a\); mean area | `docs/phase2/pen_link_budget.md` §1 |
| Coil B sensitivity | 4,959 V/T @20 kHz; 8,430 V/T @34 kHz | \(\tilde V/T\), \(A_{sens}\), CRLB | `docs/phase2/pen_link_budget.md` §1; `docs/phase2/frontend_requirements.md` §3 |
| Coil B \(R,L\) | 8.6 Ω, 804 µH | thermal noise \(4kTRB\); \(\lvert Z\rvert\) | `docs/phase2/pen_link_budget.md` §1 |
| Self-resonance | ~485 kHz air / ~290 kHz ferrite | upper validity limit; 34 kHz is 14.3×/8.5× below | `docs/phase2/tone_plan.md` §1, §6 |
| Cable capacitance | 59 pF (0.6 m W2697 39 pF + 20 pF terminations); 73 pF total budget = 10 + 10 + 53 pF | shunt across coil, \(f_{res}=1/(2\pi\sqrt{LC})\) | `docs/phase2/tone_plan.md` §1, §6; `contract/system_contract.md` SC-05c |
| Ferrite (if used) | 3C90, \(\mu_r\approx2300\), +10 dB | Eqs.(7.5)–(7.7); excluded by air-core lock | `AGENTS.md`; decision #4 |
| Table 7.1 alternates | A 321 T / 9–12.5 mm; C 120 T / 9–12.2 mm; D/E ferrite-cored | same \(NA\omega\mu_a\) form | `AGENTS.md`; `docs/phase2/pen_link_budget.md` §1 |

**Receive transfer matrix.** Combining the filament field and point-sensor flux
for one pen coil (\(j=1\)) and eight emitter coils,

$$
\tilde V_j=\sum_{i=1}^{8} j\omega_i M_{ji}\tilde I_i,\qquad
M_{ji}=\mu_a N A\,\hat n_j\!\cdot\!\mathbf b_i(\mathbf p),
$$

i.e. the mutual inductance \(M_{ji}\) is the filament flux per unit current
through the sensor; this is the matrix form of Eq.(3.17)–(3.25) and is the
quantity \(A_{sens}\) and κ absorb (`docs/phase2/frontend_requirements.md` §1;
`software/anser-matlab-ref/user/objective/objectiveCoilSquareCalc3D.m:22-36`).

---

## 4. Receive chain to digital

**Front end.** INA163 (G≈35) → ADA4940-2 differential stage (G≈2), total ≈70;
the strongest 34 kHz tone is kept at 3.40 V differential, below ±4.096 V
(`docs/phase2/frontend_requirements.md` decision summary, §4). Coil-B fields at
150/200 mm (`docs/phase2/frontend_requirements.md` §4):

| Tone | Field | \(V_s\) (derived: V/T × B) | ×70, differential | differential ADC codes (derived) | Source |
|---|---|---|---|---|---|
| weakest @20 kHz | 0.10 µT | 0.496 mV | 34.7 mV | 71,066 | `docs/phase2/frontend_requirements.md` §4 |
| weakest @34 kHz | 0.10 µT | 0.843 mV | 59.0 mV | 120,832 | same |
| strongest @20 kHz | 5.76 µT | 28.6 mV | 2.00 V | 4,096,000 | same |
| strongest @34 kHz | 5.76 µT | 48.6 mV | 3.40 V | 6,963,200 | same |

Codes use a signed 24-bit converter with ±4.096 V differential full scale:
\(k=\operatorname{round}(V_{diff}\,2^{23}/4.096)\). One LSB is
\(8.192/2^{24}=488.3\) nV differential (*derived* from `contract/system_contract.md` SC-05).

**ADC.** AD7768-4, 24-bit, 4 channels sampled simultaneously, ODR 256 kSPS
(`contract/system_contract.md` SC-05/SC-06). Wideband filter group delay
\(34/F_s=132.8\ \mu s\); passband \(0.4F_s=102.4\) kHz; stopband
\(0.499F_s=127.7\) kHz at 105 dB (34 kHz is 0.33× the passband); settling
\(68/F_s=266\ \mu s\) after the one-time START/SYNC, with the first 68 samples
discarded (`docs/phase2/tone_plan.md` §1, §3, §5). Aperture jitter bound
\(SNR_j=-20\log_{10}(2\pi f t_j)\): at 34 kHz, 1 ns → 73.4 dB, 30 ps → 103.9 dB
(`docs/phase2/tone_plan.md` §5; `docs/phase2/adc_justification.md` §2a, RQ-A4).

**Noise and CRLB.** Input-referred noise over one 500 Hz bin
(`docs/phase2/frontend_requirements.md` §3; `simulations/m16/FINAL_REPORT.md` §3.5):

| Term | Value | Source |
|---|---|---|
| INA163 voltage noise | 24.6 nV = 1.1 nV/√Hz × √500 | `docs/phase2/frontend_requirements.md` §3 |
| Coil thermal | 8.4 nV = √(4kTRB), R=8.6 Ω | same |
| INA163 current noise × source | 1.8 nV | same |
| Total input-referred | ≈26.1 nV (RSS) | `simulations/m16/FINAL_REPORT.md` §3.5 |
| \(\sigma_B\) @20 kHz / @34 kHz | 5.3 / 3.1 pT | `docs/phase2/frontend_requirements.md` §3 |
| Required \(\sigma_B\), 150/B @250 mA | ≤26 pT | `contract/system_contract.md` SC-01e |
| Processing gain | \(PG=10\log_{10}(N/2)=24.1\) dB for N=512 | `docs/phase2/adc_justification.md` §2a |

The phase-variance bound for an \(N\)-sample coherent DFT is

$$
\sigma_\phi\approx\frac{\sigma_n}{A\sqrt N},\qquad
\sigma_n^2=\sigma_{thermal}^2+\sigma_q^2+\sigma_{xtalk}^2+\sigma_{leak}^2,
\qquad \sigma_q=\frac{q}{\sqrt{12}},\ q=\frac{FSR}{2^{N_{ADC}}},
$$

(`docs/phase2/adc_justification.md` §2a). With the tabulated weakest tone
\(A=0.496\) mV, \(\sigma_n=26.1\) nV and \(N=512\), *derived*
\(\sigma_\phi=2.33\times10^{-6}\) rad = 0.000133°. The sign decision boundary is
\(\Delta\phi_i=0\) or \(\pm\pi\), where the determinant of §5 vanishes, so this
variance must be compared with the calibrated distance to that boundary; the
per-tone calibrated offsets are not yet fixed numerically (§10). The relative
amplitude CRLB follows from the same linear mapping
*A_sens cancels*: \(\sigma_A/A=\sigma_B/B\). For the 0.10 µT weakest tone,
\(\sigma_A/A=5.3\ \mathrm{pT}/0.10\ \mu\mathrm T=5.3\times10^{-5}\) (85.5 dB)
achieved, versus \(26/100=2.6\times10^{-4}\) (71.7 dB) required
(*derived* from `docs/phase2/pen_link_budget.md` §§1–3 and SC-01e; the table
there quotes 85.4 dB SNR). An explicit \(\sigma_A/A\) column is not tabulated
in the cited docs; the values above are derived, not a new spec.

**Code→field scaling chain** (all gains algebraic):

$$
\underbrace{k_{ADC}}_{\text{counts}}
\;\xrightarrow{\;8.192/2^{24}\;}\;V_{diff}
\;\xrightarrow{\;/G_{FE}\;}\;V_{coil}
\;\xrightarrow{\;/\mu_aNA\;}\;\omega B_{\parallel}
\;\xrightarrow{\;/\omega_i\;}\;B_{\parallel}
\;\xrightarrow{\;/A_{sens,i}\;}\;B_i\ \text{(signed per §5)} .
$$

\(G_{FE}\approx70\) (`docs/phase2/frontend_requirements.md` §4),
\(\mu_aNA=3.95\times10^{-2}\) m² and the V/T values are in §3,
\(A_{sens,i}\) comes from the Helmholtz fit
(`docs/phase2/calibration_tooling.md` §1).

---

## 5. Demodulation

**Goertzel.** With \(w[n]\) the window and \(\theta_k=2\pi J_k/N\), the HDL form
is (`docs/handoff/system-flowchart-handoff.md:186`;
`docs/phase2/anser-baseline-findings.md` §9):

$$
s_k[n]=w[n]x[n]+2\cos\theta_k\,s_k[n-1]-s_k[n-2],\qquad s_k[-1]=s_k[-2]=0,
$$

$$
Y_k=s_k[N-1]-e^{-j\theta_k}s_k[N-2],
$$

$$
\Re Y_k=s_k[N-1]-\cos\theta_k\,s_k[N-2],\qquad
\Im Y_k=\sin\theta_k\,s_k[N-2],
$$

the last line derived by expanding \(e^{-j\theta_k}\). Coefficient
\(2\cos\theta_k\), bin \(J_k=f_kN/F_s=40,44,\ldots,68\). Run for Ch0 (\(Y_I\))
and the pen channel (\(Y_V\)) at all eight tones: 32 tone/channel pairs × 512
samples = 16,384 real multiplies per frame, 1.90 M multiply/s at 115.8 Hz
(`docs/phase2/dig6_requirements.md` §4 DIG-03a). Output per frame: 8 complex
\(Y_V\), 8 complex \(Y_I\), timestamp and status (DIG-03d).

**Windows.** Rectangular with integer \(J\) gives zero tone-to-tone leakage and
the narrowest ENBW; its −13 dB sidelobes affect only non-bin components, which
the ADC digital filter plus analog AA must reject
(`docs/phase2/tone_plan.md` §4). Hamming is the fallback: main lobe
1.81–1.95 bins, −42 dB sidelobes, margin 25–95 Hz at 4-bin spacing; if its
bench margin is <50 Hz, use N=1024 (8-bin spacing, 4 ms acquisition)
(`docs/phase2/tone_plan.md` §2, §4, §8). Blackman (2.35 bins) does not fit at
N=512 (`docs/phase2/tone_plan.md` §4). If the integer-J condition is broken by
fractional-bin truncation, the rectangular response follows the Dirichlet
kernel \(\sin(\pi N\delta)/(N\sin\pi\delta)\); the cited consequence is a
10–20 dB spur-floor rise in the worst case
(`docs/phase2/adc_justification.md` §2c).

**Amplitude, phase, rotation.** \(|Y|=\sqrt{I^2+Q^2}\); \(\varphi=\operatorname{atan2}(Q,I)\)
is for characterisation only — the solver does not use it
(`docs/handoff/solver-algorithm-handoff.md` §3). The ADC wideband group delay
adds \(\omega_i\cdot34/F_s\) per tone (*derived*, from
`docs/phase2/tone_plan.md` §5): 236.25° at 20 kHz through 185.63° at 34 kHz
(mod 360°). It is a fixed per-tone rotation absorbed by the calibration
rotation/DAQ_phase term; no per-frame phase search
(`docs/phase2/dig6_requirements.md` §4 DIG-03c).

**Signed amplitude — golden reduction.** Exactly as the golden model
(`software/anser-matlab-ref/user/system/fSysGetField.m:22-48`):

$$
\Delta\phi_i=\angle Y_{I,i}-\angle Y_{V,i}-\mathrm{DAQ\_phase}_i
\quad\text{(wrapped to }[-\pi,\pi]\text{)},
$$

$$
B_i=\operatorname{sign}(\Delta\phi_i)\,\frac{|Y_{V,i}|}{A_{sens,i}},
\qquad
\texttt{BField = sign(Phase1)'. * MagY(2,:)'. / sys.Asens';}
$$

With rotated pen pair \((\tilde I_V,\tilde Q_V)=(I_V,Q_V)e^{j\phi_{\text{cal}}}\),
the sign test avoids `atan2` entirely:

$$
\operatorname{sign}(\Delta\phi_i)
=\operatorname{sign}\!\left[\Im\!\left(Y_{I,i}\,\overline{Y_{V,i}}\,e^{-j\phi_{\text{cal}}}\right)\right]
=\operatorname{sign}\!\left[\begin{vmatrix} \tilde I_{V,i} & \tilde Q_{V,i}\\ I_{I,i} & Q_{I,i}\end{vmatrix}\right]
$$

(derived: \(\Im\{A\overline B\}=Q_A I_B-I_A Q_B=\tilde I_V Q_I-\tilde Q_V I_I\);
sign of the sine of a
wrapped angle equals sign of the angle on \((-\pi,\pi)\)). At \(|\Delta\phi_i|=\pi\)
the determinant is zero and the sign is ambiguous; the golden wrap leaves ±π
unchanged (`software/anser-matlab-ref/user/system/fSysGetField.m:34-43`). This
2×2 determinant is the frozen 8-real-residual measurement model
(`docs/handoff/solver-algorithm-handoff.md` §3).

**κ / \(A_{sens}\) normalisation.** Helmholtz gives \(A_{sens}(f)=V/B\) per tone
(`docs/phase2/calibration_tooling.md` §1). The 7×7 grid (49 points × 85.6/152 mm
planes, 98 points) gives `BStore` (49×8 per plane); for each coil \(c\) the golden
fit minimises, over \((\delta z,\kappa_c)\),

$$
r_{c,q}(\delta z,\kappa_c)
=B^{meas}_{c,q}
-\kappa_c\,\frac{I_{out,c}}{R_{store,c}}\,
\mu_0 H_{z,c}(x_q,y_q,z_q-\delta z),
$$

starting from \((0,1)\), with the per-coil \(\delta z\) averaged after the fit.
The objective is \(\min_{\delta z,\kappa_c}\sum_{q=1}^{49}r_{c,q}^2\), solved with
`lsqnonlin` settings `TolFun=1e-22`, `TolX=1e-7`, `MaxFunEvals=2000`,
`MaxIter=2000`
(`software/anser-matlab-ref/user/calibration/fCalibrate.m:20-50`;
`software/anser-matlab-ref/user/objective/objectiveScalingOffsetZ.m:30-48`;
`docs/phase2/calibration_tooling.md` §2, §7). Acceptance is the 98-point RMS of
Eq.(7.10) (`contract/system_contract.md` SC-02). At runtime the model uses
\(\kappa_c I_{out,c}/R_{store,c}\)
(`software/anser-matlab-ref/user/objective/objectiveCoilSquareCalc3D.m:32`).

**Spur / leakage budget.** Target is spurs ~60–70 dB below the tone, before
thermal noise, leakage and crosstalk are stacked
(`docs/phase2/adc_justification.md` §1, §2a). What sets it: DDS phase truncation
≈72 dBc (`docs/phase2/dig6_requirements.md` §2 DIG-01b); DAC crosstalk/INL
≤−85 dBc and summer 8-tone EVM −67.1 dBc worst with 7.1 dB margin
(`simulations/m16/FINAL_REPORT.md` §3.2–3.3); receiver ≤−80 dBc estimate
(report §3.4); window sidelobes and integer-J leakage above
(`docs/phase2/tone_plan.md` §4); jitter 73.4 dB at 1 ns / 103.9 dB at 30 ps
(§4 above). The demod contributes zero tone-to-tone leakage only while the
integer-J condition holds; the bench compares windows and records the spur
floor (`docs/phase2/tone_plan.md` §7; `docs/phase2/dig6_requirements.md` §7).

---

## 6. Pose solve to (x, y, z, θ, φ)

**Cost.** Thesis Eq.(3.26)–(3.27), frozen in the handoff:

$$
F(\mathbf p)=\mathbf V_d-\kappa\odot\mathbf V_m(\mathbf p),\qquad
\min_{\mathbf p}\ \|F(\mathbf p)\|^2\ \text{s.t.}\ lb\le\mathbf p\le ub .
$$

Source: `docs/handoff/solver-algorithm-handoff.md` §3;
`contract/requirements/manipulator.md` for the follower-side use. The golden
objective returns the *opposite* overall sign,
\(F_{\text{golden}}=\text{fluxModel}-\text{fluxReal}\)
(`software/anser-matlab-ref/user/objective/objectiveCoilSquareCalc3D.m:36`);
a global sign flip leaves \(\|F\|^2\) and the minimiser unchanged (recorded in §10).

**Measurement vector.** Eight entries \(B_i\), one per coil/tone, from the
signed-amplitude reduction of §5:
\(\mathbf V_d=[B_1,\ldots,B_8]^T\)
(`software/anser-matlab-ref/user/system/fSysGetField.m:48`;
`docs/handoff/solver-algorithm-handoff.md` §3). No complex residual, no
`atan2` in the solve path.

**Bounds.** Golden `portable` bounds: \(x,y\in[-0.25,0.25]\) m,
\(z\in[0,0.5]\) m, \(\theta,\phi\in[-2\pi,2\pi]\)
(`software/anser-matlab-ref/user/system/fSysDecodeField.m:17-22`; handoff §3).
The FPGA proposal uses canonical \(\theta\in[0,\pi]\), \(\phi\in[-\pi,\pi]\)
with vertex clamp on output (handoff §4); that is a proposal, not a golden change.

**Golden settings (frozen).** `lsqnonlin` bounded →
**trust-region-reflective (TRF)**, not LM; finite-difference Jacobian;
`TolFun=1e-16`, `TolX=1e-6`, `MaxIter=40`, `MaxFunEvals=500`; if
`resnorm>1e-15`, retry from \(\mathbf p_0+[0,0,0,\pi,\pi]\), else hold the prior
estimate; warm start is a 5-tap moving average of past solutions
(`software/anser-matlab-ref/fSysSetup.m:184,204-205,246-248`;
`fSysDecodeField.m:25-34`; handoff §3).

**FPGA numerics (proposal under validation).** Damped Gauss–Newton with a fixed
λ ladder:

$$
(J^T\!J+\lambda\,\operatorname{diag}J^T\!J)\,\delta=-J^T\!F ,
$$

accept → \(\lambda/10\), reject → \(\lambda\times10\) (≤2 rejects), 4–10
iteration cap, 5×5 Cholesky solve with a λ floor to keep the system positive
definite at \(\theta\to0\), one retry and a watchdog that expires to the last
estimate with a `degraded` flag (`docs/handoff/solver-algorithm-handoff.md` §4,
§8–§9). This is a bounded-budget approximation of the golden TRF subproblem,
not a claim about MATLAB internals (handoff §3 note).

**Analytic Jacobian.** From \(\Phi=k\,\mathbf B(\mathbf p)\cdot\hat n\) with
\(k=\kappa\,\mu_aNA\,I_{out}/R_{store}\),
\(\partial\hat n/\partial\theta=[\cos\theta\cos\phi,\cos\theta\sin\phi,-\sin\theta]\)
and \(\partial\hat n/\partial\phi=[-\sin\theta\sin\phi,\sin\theta\cos\phi,0]\):

$$
\frac{\partial\Phi}{\partial\theta}=k\,\mathbf B\!\cdot\!\frac{\partial\hat n}{\partial\theta},
\qquad
\frac{\partial\Phi}{\partial\phi}=k\,\mathbf B\!\cdot\!\frac{\partial\hat n}{\partial\phi},
$$

effectively free once \(\mathbf B\) is computed. The three position derivatives
use the differentiated segment kernel of §2 and share its intermediates; cost
≈3 model evaluations/iteration versus 6 for forward differences
(`docs/handoff/solver-algorithm-handoff.md` §4).

**Precision / conditioning.** float32 with normalised coordinates and field;
golden is float64. Normal equations square the condition number, so float32
conditioning near \(\theta\to0\) and at the volume boundary is a sign-off gate;
escalate to Givens QR of the 8×5 only if needed, not to float64
(handoff §4, §8 V3, §10). First-pass 8×5 conditioning for the 150 mm/B cube is
median/95th/max 26.5/69.5/73.1, with the \(\theta=0\) singularity causing
rank<5 poses (`contract/system_contract.md` §2 and SC-01d).

**Why 5 DOF.** A single coil senses only \(\mathbf B\cdot\hat n\); rotating the
pen about its own axis leaves \(\hat n\) unchanged, so
\(\partial\Phi/\partial\psi=k\,\mathbf B\cdot(\hat n\times\hat n)=0\) for the
roll angle \(\psi\). The null space of the measurement map contains every
rotation about \(\hat n\); roll is unobservable by construction, and 6-DOF
would need two orthogonal coils (`AGENTS.md` gotchas; `docs/phase2/README.md` §2
spec #1–2).

**Degenerate / out-of-volume handling.** Bounds clamp plus a `clamped` status;
the retry is attempted at most once; if the residual still exceeds the gate the
FPGA keeps the last estimate with `degraded`, and the follower watchdog halts
on stale pose (`docs/handoff/solver-algorithm-handoff.md` §4, §9;
`docs/handoff/m16-fpga-handoff.md` §7, §10). The golden fallback is
`solution = sys.estimateInit`
(`software/anser-matlab-ref/user/system/fSysDecodeField.m:31-33`). Pose status
values are tracking / clamped / stopped / fault (M16 handoff §10).

---

## 7. Numeric budget

| Term | Value | Source |
|---|---|---|
| Acquisition \(T_{acq}=N/F_s\) | 2.000 ms | `docs/phase2/dig6_requirements.md` §6 |
| ADC group delay | 0.133 ms | `docs/phase2/tone_plan.md` §3 |
| Demod | 0.500 ms | `docs/phase2/dig6_requirements.md` §6 |
| Solver | 5.000 ms (proposed FPGA nominal ≈0.5–1.1 ms) | `docs/phase2/dig6_requirements.md` §6; `docs/handoff/solver-algorithm-handoff.md` §5 |
| Overhead | 1.000 ms | `docs/phase2/dig6_requirements.md` §6 |
| **Total / pose rate** | **8.633 ms / 115.8 Hz**; 10 ms / 100 Hz requirement leaves 1.367 ms | `docs/phase2/dig6_requirements.md` §6 |
| Filter-off / filter-on latency | ≈9.1 ms / ≤100 ms | `docs/phase2/dig6_requirements.md` §6 |
| Demod ops | 32 × 512 = 16,384 real multiplies/frame; 1.90 M/s | `docs/phase2/dig6_requirements.md` §4 |
| Model ops | 800 segments/eval, ~30 MAC/segment = 24 kMAC/eval; 288–864 kMAC/pose; 28,800–86,400 rsqrt/pose | `docs/handoff/solver-algorithm-handoff.md` §5 |
| Capture memory | 4 × 512 × 32 bit = 64 kb/frame; ping-pong 128 kb (4 BRAM36) | `docs/phase2/dig6_requirements.md` §3 DIG-02c |
| LUT memory | 4096×16 = 64 kb = 2 BRAM36 | `docs/phase2/dig6_requirements.md` §2 DIG-01b |
| Solver resources (estimated) | ~25–40 DSP48, ~7k LUT @131.07 MHz | `docs/handoff/solver-algorithm-handoff.md` §5–§6 |
| Precision | float32 normalised (proposal) vs float64 golden | `docs/handoff/solver-algorithm-handoff.md` §4 |

---

## 8. Worked end-to-end example (no fabricated intermediates)

Representative pose: a 7×7 calibration point on the locked 150 mm/B cube bottom
plane, \(z=85.6\) mm, with x/y from the 31.75 mm grid and \(\theta=\phi=0\)
(`contract/system_contract.md` SC-02, D1-B;
`software/anser-matlab-ref/fSysSetup.m:68-73`). The weakest-tone field input
0.10 µT at 150 mm/B and the strongest 5.76 µT are first-pass 8×5 scan values at
250 mA (`docs/phase2/pen_link_budget.md` Assumptions;
`docs/phase2/frontend_requirements.md` §4).

| Step | Calculation | Status |
|---|---|---|
| 1. Coil current | \(\tilde I_i=250\) mA at each tone, closed loop; phase reference Ch0 | sourced: `docs/phase2/driver_power_requirements.md` §1 DRV-02, §4 |
| 2. DAC word | centre 2.45 V → code 32,113; clamp 0.3–4.6 V | computed: §1 |
| 3. Filter image | 34 kHz tone → image 165.805 kHz at −35.3 dB | computed: §1, matches `simulations/m16/FINAL_REPORT.md` §3.1 |
| 4. Field at sensor | \(\mathbf B(\mathbf p)=\sum_i\tilde I_i\mathbf b_i(\mathbf p)\); weakest tone 0.10 µT, strongest 5.76 µT | input sourced; per-pose fields **requires sim/bench** (`simulations/field_jacobian.py`) |
| 5. Sensor EMF | \(V/T=4,959\) @20 kHz / 8,430 @34 kHz; weakest 0.496 mV, strongest 48.6 mV | computed: §4 table |
| 6. Front end / ADC | ×70 → 34.7 mV / 3.40 V; 71,066 / 6,963,200 counts | computed: §4 table |
| 7. Noise / CRLB | 26.1 nV in 500 Hz → 5.3 pT @20 kHz; \(\sigma_\phi\approx2.33\times10^{-6}\) rad, \(\sigma_A/A\approx5.3\times10^{-5}\) | computed: §4 |
| 8. Demod | Goertzel at bins 40…68; \(|Y|\) and sign via determinant; \(B_i=\operatorname{sign}(\Delta\phi_i)|Y_i|/A_{sens,i}\) | equations in §5; numeric \(|Y|\) **requires bench** (`A_sens` not yet fixed numerically for Phase 2 tones) |
| 9. Calibration | κ, \(\delta z\) from the 7×7 fit; 98-point RMS Eq.(7.10) | procedure sourced; numeric κ **not yet fixed** in the repo (§10) |
| 10. Solve | 8 residuals, TRF golden / damped-GN FPGA, warm start, bounds, one retry | equations in §6; output pose for this point **requires sim/bench** |

The repo has no numeric per-tone κ, Phase-2 \(A_{sens}\), or measured 8-tone
frame vectors, so steps 4, 8–10 cannot be carried to a numeric pose without
running the golden model or the bench. The checklist above states the inputs and
their sources instead of inventing values.

---

## 9. Verification / golden checks

| Check | Artefact | Pass criterion | Source |
|---|---|---|---|
| Goertzel vs MATLAB matrix demod | FPGA I/Q for a prerecorded frame vs `fSysGetField.m:19-48` (`Y=(X.*G)*E`) | amplitude/phase within tolerance; integer-J on/off leakage measured | `docs/phase2/dig6_requirements.md` §7; `docs/handoff/m16-fpga-handoff.md` §11 |
| Filament kernel (incl. rsqrt/NR form) | `simulations/field_jacobian.py` vs `spiralCoilFieldCalcMatrix.m:17-54` | rsqrt form ≤1e-6 relative to golden; field ≤20 % vs probe/golden | `docs/handoff/solver-algorithm-handoff.md` §8 V3; `docs/phase2/dig6_requirements.md` §5 DIG-04b |
| Solver | pose vs `fSysDecodeField.m` / `objectiveCoilSquareCalc3D.m` on the 98-point grid, trajectory and cold start | ≤2 mm / ≤1°; median ≤4 iterations; cap-hit and retry rates reported | `docs/handoff/solver-algorithm-handoff.md` §8 V1, §9 |
| Calibration | 7×7 κ/\(\delta z\) fit; 98-point RMS Eq.(7.10) | RMS gate from Eq.(7.10); κ stability over 18–28 °C | `docs/phase2/calibration_tooling.md` §2, §7; `contract/system_contract.md` SC-02 |
| Front end | SPICE/receiver model and Helmholtz \(A_{sens}(f)\) sweep | ≤−60 dBc receiver EVM (estimate ≤−80 dBc); \(\sigma_B\le26\) pT at 150/B | `simulations/m16/FINAL_REPORT.md` §3.4–3.5; `docs/phase2/frontend_requirements.md` §7 |
| Filter/image and spur floor | 8-tone FFT at DAC/current-sense/ADC | image ≤−35 dB; EVM ≤−60 dBc; spur floor 60–70 dB below tone | `simulations/m16/FINAL_REPORT.md` §4; `docs/phase2/tone_plan.md` §7 |
| Timing/latency | timed pose loop, 1 h moving run | 8.633 ms worst case; filter-off ≤20 ms; zero dropped frames | `docs/phase2/dig6_requirements.md` §7 |

---

## 10. Conflicts / open items

| # | Item | Source disagreement / gap | Treatment / what resolves it |
|---|---|---|---|
| 1 | Solver name | Handoff §3 freezes bounded `lsqnonlin` = **TRF** and says "LM/TRF" prose is stale; `docs/phase2/README.md` §3–§4, `docs/phase2/dig6_requirements.md` DIG-04c, `docs/handoff/m16-fpga-handoff.md` §7 and decision #23 still say LM/TRF | Golden formulation is TRF per handoff §3 (higher-authority frozen formulation); decision #23 uses the ambiguous label. Resolve by updating the stale prose, not the algorithm |
| 2 | Residual sign | Handoff §3: \(V_d-\kappa V_m\); golden `objectiveCoilSquareCalc3D.m:36`: `fluxModel - fluxReal` | Both minimise the same \(\|F\|^2\); sign convention recorded, no decision needed |
| 3 | Angle bounds | Golden \(\theta,\phi\in[-2\pi,2\pi]\) (`software/anser-matlab-ref/user/system/fSysDecodeField.m:18-19`); FPGA proposal \(\theta\in[0,\pi]\), \(\phi\in[-\pi,\pi]\) (handoff §4) | Proposal is not adopted here; π-retry covers the second branch. Resolve at solver sign-off (handoff §12) |
| 4 | Jacobian | Golden uses finite differences (handoff §3 settings table); FPGA proposal uses analytic (handoff §4) | Two different implementations; handoff V1 decides whether analytic reaches the same minimum |
| 5 | Solver compute estimate | `docs/phase2/dig6_requirements.md` §5: 800×6 FD×10 iters = 48,000 evals/pose; handoff §5: 12 nominal (4×3) / 36 worst evals/pose | The dig6 figure is the heritage FD/heritage-iteration bound; use handoff §5 for the proposed design. Resolve by the V1 iteration histogram |
| 6 | FG coil load | 70 µH + 2 Ω (`docs/phase2/tone_plan.md` §1, §6; `simulations/m16/FINAL_REPORT.md` §0) vs locked 79 µH / 2.9 Ω (decision #27) | Contract #27 is the hardware model; 70 µH + 2 Ω is the SPICE/thesis load. Both shown in §1; resolve by measured R/L at FG-1 |
| 7 | DAC code→current mapping | 0–5 V → 0–500 mA was a pre-D2 assumption; exact offset/gain under the 0.3–4.6 V clamp is OPEN (`docs/handoff/m16-fpga-handoff.md` §4.6; `docs/phase2/dig6_requirements.md` §2 DIG-01f) | **Not yet fixed**. Bench current-loop mapping before setting amplitude |
| 8 | Numeric κ, zOffset | Golden setup initialises `BScaleActive` to zeros and `zOffsetActive` to 0 (`fSysSetup.m:254-266`); no fitted values in repo | **Not yet fixed**; produced by the 7×7 grid fit (§5) |
| 9 | Phase-2 \(A_{sens}(f)\) and DAQ_phase | Golden \(A_{sens}\) and `DAQ_phase_offset=2πF/400000` belong to the legacy 20.5–27.5 kHz / muxed 100 kSPS NI DAQ (`fSysSetup.m:33-35,146-174`); Phase 2 is 20–34 kHz simultaneous AD7768 with zero mux skew | **Not yet fixed**: measure \(A_{sens}\) per tone (Helmholtz) and absorb the fixed group delay into the calibration rotation |
| 10 | Explicit amplitude CRLB table | `docs/phase2/adc_justification.md` §2a gives \(\sigma_\phi\) and PG but no \(\sigma_A/A\) column; `simulations/m16/FINAL_REPORT.md` §3.5 gives \(\sigma_B\) | \(\sigma_A/A=\sigma_B/B\) derived in §4 from sourced inputs; no new numeric spec invented |
| 11 | Tone→coil assignment | DAC map A–H → coils 1–8 is fixed (`docs/handoff/m16-fpga-handoff.md` §4.3); FG-1 may reorder coil→tone (`docs/phase2/tone_plan.md` §4) | Current map used in §1 table; version the final map at FG-1 |
| 12 | Ferrite parameters | AGENTS.md gives µr≈2300 / +10 dB / Eqs.(7.5)–(7.7); local thesis extracts are absent (`docs/extracts/README.md`), so Eq. numbers are cited via AGENTS.md, not re-derived | Air-core lock (decision #4) makes Eqs.(7.5)–(7.7) inactive; re-open only with a ferrite variant |
| 13 | Spur floor target | "60–70 dB below tone" is a range (`docs/phase2/adc_justification.md` §1); simulated summer EVM is −67.1 dBc (`simulations/m16/FINAL_REPORT.md` §3.2) | Keep the range; bench 8-tone FFT closes it (`docs/phase2/tone_plan.md` §7) |
| 14 | JAEGER extract availability | `docs/extracts/README.md` says the three thesis extracts are local-only and absent from the repo; §2 and §3 cite equation numbers through `AGENTS.md` and tracked handoffs | No inline quotation of the thesis; regenerate locally via `tools/extract_jaeger.sh` if equation text must be re-checked |
