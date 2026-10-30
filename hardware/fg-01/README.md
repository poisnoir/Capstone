# hardware/fg-01 — 8-coil planar PCB field generator (reference)

Upstream (pristine, do not edit): `vendor/anser-osf/Design Files/`
- `Field Generator Board/CAD/` — `Top/Bottom_plate4.SLDPRT`, `Wire_path_drawing.SLDPRT/.DWG` (mechanics), `Drawing_pdf/fgasm.PDF` (assembly)
- `Field Generator Board/Photos/` — `Field_Generator_Assembled.png`, `..._withDuplo.PNG`, `Assembly_Render.png`, `Exploded_Render.png`
- `Emitter Coil/CAD/Gerbers/Transmitter Coil PCB Gerber.zip` — `spiral_coil_stackable_Rev_C` Gerbers + `.pcb` + plot report (the 8-coil PCB to replicate)

Working rule: new FG work (pen-volume coil placement sim, ICNIRP ≤27µT check) lives here;
reference Gerbers stay in vendor. Filament geometry for the solver comes from the trace
layout via `software/anser-matlab-ref/model/spiralCoilDimensionCalc.m`.
