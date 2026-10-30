# Pen — passive 5-DOF sensor

The pen is passive: one hand-wound coil, no electronics in the shell. The
tracked point is the sensor coil/tip, not the pen housing (SC-01c).

## Locked choices

- 5-DOF: x, y, z, pitch, yaw. **No roll** — a single coil cannot sense it.
- Air-core coil, no ferrite (decisions log #4). Ferrite gives ~+10 dB but adds
  nonlinearity and Barkhausen noise (thesis Eqs.7.5–7.7).
- Coil geometry from thesis Table 7.1 (Ch.7 extract): A–E; e.g. C = 120 turns,
  0.32 mm wire, 12 mm long, 9/12.2 mm ID/OD.
- Link budget and the σ_B target: `docs/phase2/pen_link_budget.md`
  (150 mm/B needs ≤26 pT; 100 mm/B ≤58 pT; 200 mm/B ≤11 pT).
- Pen mass ≤50 g; cable must not drag the pen.

## Open

- Final coil choice (B baseline; A/E alternates; C air out).
- Shell, strain relief, connector, and the cable capacitance budget
  (73 pF total at 34 kHz, SC-05c).
- Winding fixture and repeatability.

## Do not

- Add a ferrite core without a contract change.
- Put metal in the pen shell or within 150 mm of the volume.
