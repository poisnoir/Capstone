# ICD — Mechanical interfaces

**Status:** stub, not frozen. **Owners:** Tung (FG/enclosure), Tristan (arm
mechanics). **Canonical sources:** `contract/system_contract.md` SC-01a–c,
SC-04b, D1-B, D2; `docs/phase2/system_schematic.md`;
`../requirements/manipulator.md` (now `contract/requirements/`).

This stub does not add requirements. Until frozen, the SC rows and the
manipulator requirements are authoritative.

## What is already fixed

- FG PCB coordinate frame: origin at the geometric centre of the FG PCB, z = 0
  on the board top surface, +z toward the pen, right-handed, SI units.
- Tracking volume: 100 mm minimum, 150 mm target at z = 85.6–235.6 mm, 200 mm
  stretch only if SC-01d passes.
- ICNIRP guard: non-metal access barrier at the ~57 mm / 27 µT contour; no metal
  within 150 mm of the volume; plastic fasteners; removable for calibration.
- Pen is passive; the sensor coil/tip is the tracked point, not the pen housing.
- Follower is bench gear; its cable must not drag the pen.

## Open

- FG board mounting holes and enclosure footprint.
- Pen shell, cable strain relief and connector.
- Arm base/mount interface and the 150 mm keep-out envelope.
- Tilt pivot: hardware tip-pivot vs base wrist + software compensation.
- Camera/display mount and the ≥50× view.

## Change control

Any change to the fixed list is a contract change.
