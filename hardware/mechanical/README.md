# Mechanical — enclosure, guard, mounts

Owner: Tung with Tristan. The mechanical design carries two contract items:
the 150 mm metal-free rule and the non-metal ICNIRP guard.

## What lives here

- Enclosure for BRD-01, FG-01 and the power entry; internal shield partition
  (the one-box decision, #10/#25).
- Non-metal ICNIRP guard: open-top ring/fence at the ~57 mm / 27 µT contour at
  250 mA. It is an **access barrier, not an EMF shield** (SC-04b, D2). Plastic
  fasteners; removable for the 7×7 calibration grid and field mapping.
- FG board mount, pen holder/cable strain relief, camera/display bracket
  (≥50× view), follower base/mount.
- The 150 mm keep-out envelope around the tracking volume.

## Rules

- No metal, carbon fiber or metal mesh within 150 mm of the volume. A metal box
  is prohibited (eddy-current distortion).
- The guard must not reduce the 150 mm cube: with the cube bottom at 85.6 mm,
  the guard sits 28.6 mm below it.
- The follower cable must not drag the pen.
- Tilt pivot: hardware tip-pivot vs base wrist + software compensation is still
  open (`contract/requirements/manipulator.md` B5).

## Files

CAD/STEP/STL are binary; keep them small and commit only released versions. If
the mechanical team adopts a CAD tool with large assemblies, revisit Git LFS
before adding them.
