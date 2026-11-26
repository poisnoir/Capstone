# software/anser-matlab-ref — Anser MATLAB golden model (reference only)

Unpacked from `vendor/anser-osf/P&O Code/Matlab/MatlabCode.zip` (30 files; `vendor/`
is local-only, gitignored). **Do not develop here** — this is the functionally-correct
baseline to port into `fpga/`. It is a **reference/golden model, not a live PC-side
pose solver**: decision "Full-FPGA pose" in `AGENTS.md` puts DDS, demodulation and
the LM/TRF solver in HDL/HLS with no MATLAB-in-loop. All module paths below exist
in this folder; the equations are Jaeger 2018 (see `docs/extracts/README.md`).
Upstream pointer: `https://github.com/BioDesignUCC/AnserEMT` (from `Latest Code.txt`
in the vendor snapshot) — **UNVERIFIED; not fetched** per `AGENTS.md`.

## Port map (MATLAB → full-FPGA per AGENTS.md)
- `model/spiralCoilFieldCalcMatrix.m` → filament Biot-Savart kernel (thesis Eq.3.17–3.18, Sonntag 2007). Golden B-field.
- `user/objective/objectiveCoilSquareCalc3D.m` (+ `objectiveScalingOffsetZ.m`) → solver cost `F=Vd−κ·Vm` (Eq.3.26–3.27).
- `user/system/fSysDecodeField.m` → bounded `lsqnonlin` LM solver with retry (`+[0,0,0,π,π]`, `residualThresh` fallback). Port to HDL/HLS LM/TRF.
- `user/tracking/fGetSensorPosition.m` → pipeline order: `fSysSensor → fSysGetField → fSysDecodeField → fSphericalToMatrix`.
- `user/system/fSysGetField.m` + `fSysDAQUpdate.m` + `daq/fDAQ*.m` → demod/ADC-sync path (FPGA real-time target).
- `user/calibration/fCalibrate.m`, `fGetCalField.m`, `fCheck.m` → per-coil κ calibration (7×7 grid); keep procedure for FPGA cal flow.
- `user/system/fSysSensor.m`, `fSysSave.m`, `fSysSetup.m`, `Run*.m` → harness/setup only, not synthesizable.
- `igtlink/igtlinkAPI/` → host-viz link; stays in host tools, not FPGA.
- `model/spiralCoilDimensionCalc.m` → coil-geometry helper for `hardware/`.

Regen (from the repository root, requires the local-only vendor snapshot):
`unzip -o -q "vendor/anser-osf/P&O Code/Matlab/MatlabCode.zip" -d software/anser-matlab-ref`
