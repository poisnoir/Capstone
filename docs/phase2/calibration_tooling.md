# Phase 2 — Calibration tooling

**Purpose.** List the tools needed for the one-time calibration chain:
Helmholtz \(A_{sens}(f)\), 7×7 grid κ/zOffset, \(I_{out}\), and the ICNIRP/field
map. This is a tooling list, not a new design decision.

**Sources:** `HAJ_Thesis_2018.pdf` §4.4/§7.2.2; `docs/phase2/anser-baseline-findings.md`;
`docs/handoff/system-flowchart-handoff.md` §11; `software/anser-matlab-ref/user/calibration/`;
`docs/phase2/pen_link_budget.md`; `contract/system_contract.md` SC-02/SC-04b.

---

## 1. Helmholtz \(A_{sens}(f)\)

| Tool | Purpose | Likely source |
|---|---|---|
| Helmholtz coil pair with known constant (thesis: 321 µT/A) | Known B field at the pen | Lab/borrow; else build + calibrate |
| Low-distortion AC current source / driver + DDS | Drive the Helmholtz coil at 20–34 kHz | Lab bench / FG driver |
| Precision 4-wire current shunt (0.01–0.1 Ω, 0.1%) + 6.5-digit DMM | Measure the Helmholtz current | Lab; cheap to buy |
| Non-metal pen holder/alignment fixture | Put the pen coil at the Helmholtz centre, axis aligned | 3D print / Delrin |
| Gain-phase analyser (thesis GP102) **or** the AD7768/FE/FPGA chain + trusted current reference | Measure \(V\) at each tone; compute \(A_{sens}=V/B\) | Lab GP102 if available; otherwise use the FPGA chain and verify against the DMM/shunt |
| Oscilloscope/FFT (verification) | Check tone purity/phase | Lab |
| LCR meter / impedance analyser | Coil R/L, cable capacitance, resonance | Lab |

**Output:** \(A_{sens}(f)\) per tone (V/T), stored for the solver.

---

## 2. 7×7 grid κ/zOffset

| Tool | Purpose | Likely source |
|---|---|---|
| Non-metal 2-axis XY stage with micrometer/stepper (0.01 mm) | Position the pen at 49 known x/y points | Lab/manual stage; build fixture |
| 7×7 non-metal grid fixture / Delrin former with equispaced holes | Hold the pen at the grid points | 3D print / machine |
| Z-height gauge/caliper + non-metal blocks | Set 85.6 mm and 152 mm planes | Lab; 3D print |
| Rotation/tilt stage (±45°) | Orientation tests and field map; not required for the basic BStore grid | Build/borrow |
| USB microscope / camera + non-metal alignment | Align the pen to the grid | Lab |
| Non-metal table/frame; no metal within 150 mm | Valid field/accuracy | Lab procedure |
| FG board + driver + 15 V adapter + guard | Generate the field | Project hardware |
| AD7768/FE/FPGA + host logger | Acquire/demodulate the 8 tones; store `BStore` | Project hardware |
| MATLAB/Python + `fGetCalField`/`fCalibrate` | Fit per-coil `BScale` κ and `zOffset`; RMS Eq.(7.10) | Software |

**Output:** `BStore` 49×8 per plane; κ (8×1), zOffset; 98-point RMS.

---

## 3. \(I_{out}\) (per-coil current vector)

| Tool | Purpose | Likely source |
|---|---|---|
| Per-coil \(R_{store}\) measurement (4-wire DMM) | Calibrate the current-sense scale | Lab |
| Precision current shunt/current probe + DMM/scope | Verify the per-coil current once | Lab; cheap |
| Summed current-sense channel + per-tone demod | Extract each coil current at its tone (FDM); no extra ADC | Project hardware |
| `data/I_store.mat` generation script | Store the per-coil \(I_{out}\) vector for the golden model | Software |
| LMH6321 driver + current-sense summer | Generate/measure the current | Project hardware |

**Output:** \(I_{out}\) (8×1) for `fSysSetup.m`; the closed-loop driver keeps it
stable. The new FPGA can use the live per-tone amplitude instead of the stored
file.

---

## 4. ICNIRP / field map

| Tool | Purpose | Likely source |
|---|---|---|
| 3-axis AC magnetic field probe/magnetometer (20–34 kHz) | Map the 27 µT contour; verify the guard | Lab/borrow; expensive |
| Non-metal tripod/scan stage | Position the probe at the accessible boundary | Build |
| Temperature/RH logger | Record default conditions | Lab |
| Scale, calipers | Pen mass ≤50 g; dimensions | Lab |

---

## 5. What we likely have vs need

**Likely lab-owned:** DMM, oscilloscope, bench PSU, function generator, LCR
meter, micrometer/calipers, scale, temperature/RH logger, PC.

**Project-specific / confirm availability:**
- Helmholtz coil + current shunt/DMM + non-metal pen holder.
- GP102/gain-phase analyser (or use the AD7768/FE/FPGA chain; a trusted current
  reference is still required).
- 3-axis AC field probe/magnetometer (ICNIRP/field map).
- Non-metal XY stage + 7×7 grid fixture + Z-height blocks.
- Rotation/tilt stage for ±45°.
- Precision current shunt/current probe.
- Non-metal guard/enclosure; non-metal fixtures.

**Open questions:** which of the above are already in the lab? The Helmholtz
coil, GP102, and 3-axis field probe are the expensive items; if they are not
available, decide whether to borrow, build, or use a calibrated reference
alternative. The 7×7 fixture/XY stage and non-metal guard are cheap to
3D-print/machine.

---

## 6. Alternatives and likely university-lab access

You do **not** need every specialised instrument. The calibration can be done
with simpler references:

| Need | Expensive/convenient option | Simpler alternative |
|---|---|---|
| Known B field | Commercial Helmholtz coil | Build a long solenoid or known-geometry coil; calculate \(B=\mu_0 N I/L\) (long solenoid) or Biot-Savart; verify with a search coil/gauss meter. A Helmholtz pair is better uniformity; a long solenoid is easier to build. |
| Amplitude/phase measurement | GP102 gain-phase analyser | The AD7768/FE/FPGA chain itself, cross-checked with a scope/FFT or lock-in; a precise current shunt/DMM gives the current reference. |
| 3-axis field map/ICNIRP | 3-axis AC magnetometer | A single-axis **search coil** with known \(N A\), rotated to three orthogonal orientations; compute the vector/magnitude. A spectrum analyser/loop antenna is an alternative if calibrated. |
| 7×7 positioning | Motorised XY stage | Manual micrometer XY stage, 3D-printed/Duplo grid, caliper; the thesis used a Duplo board + micrometer + USB microscope. |
| Pen holder/tilt | Commercial rotation stage | 3D-printed Delrin/PLA holder + manual tilt blocks; non-metal. |

**Likely in a general EE lab:** DMM (6.5-digit maybe), oscilloscope, function/
arbitrary waveform generator, bench PSU, LCR meter, spectrum analyser (maybe),
lock-in amplifier (maybe), soldering/ESD, 3D printer/makerspace, micrometers/
calipers.

**Specialised, likely in another lab:** Helmholtz coil (physics/EM lab), GP102
(power/energy lab), 3-axis AC field probe (EMC/magnetics lab), precision XY
stage (metrology). Ask the lab technician/supervisor to borrow; do not assume a
general EE room has them.

**Recommendation:** use the AD7768/FE/FPGA as the tone measurement chain; build
or borrow a solenoid/Helmholtz and a search coil; use a single-axis search coil
for the field/ICNIRP map; 3D-print the 7×7 fixture, pen holder, and guard. Buy
only the cheap items (current shunt, connectors, non-metal fixtures). Borrow the
GP102/3-axis probe if available; otherwise use the search-coil/solenoid method.

---

## 7. Calibration sequence

1. LCR/4-wire: coil R/L, cable capacitance, \(R_{store}\).
2. Helmholtz: \(A_{sens}(f)\) per tone; non-metal alignment.
3. 7×7 grid: 49 points × 2 heights; `BStore`; κ/zOffset fit.
4. \(I_{out}\): measure/store the per-coil current vector (or use live Ch0).
5. Validation: 98-point RMS Eq.(7.10); ICNIRP/guard scan; thermal.
