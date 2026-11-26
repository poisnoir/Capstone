# hardware/fg-01 — 8-coil planar PCB field generator (reference)

FG-01 uses the vendor DesignSpark PCB coil source and separate mounting
plates. There is no FG-01 KiCad project in the repository. The
[BRD-01 KiCad project](../brd-01/kicad/brd-01.kicad_pro) contains the driver
electronics and field-generator connectors.

Upstream (pristine, do not edit): `vendor/anser-osf/Design Files/`
- `Field Generator Board/CAD/` — `Top/Bottom_plate4.SLDPRT`, `Wire_path_drawing.SLDPRT/.DWG` (mechanics), `Drawing_pdf/fgasm.PDF` (assembly)
- `Field Generator Board/Photos/` — `Field_Generator_Assembled.png`, `..._withDuplo.PNG`, `Assembly_Render.png`, `Exploded_Render.png`
- `Emitter Coil/CAD/Gerbers/Transmitter Coil PCB Gerber.zip` — **one** emitter coil PCB (`spiral_coil_stackable_Rev_C`): Gerbers + DesignSpark `.pcb` + plot report. The field generator is **eight** of these on two machined plates, not one large PCB

**Assembly (decision #27, 2026-11-02):** 8 vendor coils, one per position, **no stacking**;
2 machined plates at the `fSysSetup.m` centres: x = [−93.543, 0, 93.543,
−68.55, 68.55, −93.543, 0, 93.543], y = [93.543, 68.55, 93.543, 0, 0,
−93.543, −68.55, −93.543] mm; coils 2, 4, 5, 7 at 45°, the rest at 90°. Coil:
**25 turns split across two layers** (not 20), 70 mm outer, 0.5 mm track /
0.25 mm gap, 1.6 mm FR4, L ≈ 79 µH, R ≈ 2.9 Ω (AnserEMT 2017, Table 2;
decision #27).

**Gerbers must be re-exported** from `spiral_coil_stackable_Rev_C.pcb` in DesignSpark PCB.
The 2013 export has no outline layer and 10× drill coordinates (the plot report says mm, the
file header says inch, and the geometry matches 0.1 in units) — do not send that zip to a fab.

Working rule: new FG work (pen-volume coil placement sim, ICNIRP ≤27µT check) lives here;
reference Gerbers stay in vendor. **Filament geometry comes from the actual Gerber traces**
(dual-layer, 25 turns), not from `spiralCoilDimensionCalc.m` — the generic 25-turn spiral has an
inner opening of ~32 mm, the physical coil ~12 mm, so the trace layout is the accurate source.
