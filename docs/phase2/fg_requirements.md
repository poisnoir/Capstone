# FG-1 requirements — pointer index

**Status (2026-11-25):** this gate document is **not a separate requirements
source**. FG-01 is locked by decision #27 (2026-11-02); the FG-1 gate rows live in
`docs/phase2/design_order.md` §3 and the interface values in
`contract/system_contract.md` SC-01/SC-02/SC-03/SC-04/SC-05. Use those, not a
new list here. Do not invent requirements in this file; add them through the
design-order process and, if they change an interface, through a contract change.

**Owner:** Tung.

## Locked FG-01 truth (decision #27)

- **8 vendor AnserEMT Rev C emitter coils**, one per position, **no stacking**, on
  two in-house machined plates at the `fSysSetup.m` centres
  (±93.543/±68.55 mm; coils 2, 4, 5, 7 at 45°).
- Per coil: **25 turns split over two layers, 70 mm outer**, 0.5 mm track /
  0.25 mm gap, 1.6 mm FR4, **L ≈ 79 µH, R ≈ 2.9 Ω** (AnserEMT 2017, Table 2).
- Gerbers must be re-exported from the DesignSpark `.pcb` — the 2013 zip has no
  outline layer and 10× drill coordinates.
- Source of truth for geometry: `hardware/fg-01/README.md`; BOM FG-01.

## Where the gate checks actually live

| Check | Authoritative location |
|---|---|
| Field / ICNIRP / conditioning / volume gates (FG-02…FG-10) | `docs/phase2/design_order.md` §3 (FG-1 stage table) |
| ICNIRP rule and guard (27 µT, non-metal, no metal within 150 mm) | `contract/system_contract.md` SC-04a/SC-04b |
| Volume (100 mm min / 150 mm target / 200 mm stretch) and calibration planes | `contract/system_contract.md` SC-01, SC-02 |
| Tone set, N, integer-J (8 tones 20–34 kHz @2 kHz, N=512) | `docs/phase2/tone_plan.md`; `contract/system_contract.md` SC-03 |
| Drive/load and current envelope (150 mA first / 250 mA / 500 mA max) | `docs/phase2/driver_power_requirements.md`; `contract/decisions_log.md` #8, #11 |
| Pen coil + amp noise floor (σ_B gate) | `docs/phase2/pen_link_budget.md`; SC-01e |
| Coil geometry / trace model | `hardware/fg-01/README.md`; `simulations/field_jacobian.py` |

**Verification gates still open** (tests, not design choices): field-probe map at
the 98 points, ICNIRP surface scan, 8×5 Jacobian conditioning/CRLB at the
150 mm/B baseline, thermal soak, current-loop step, and κ 7×7 fit — see
`contract/decisions_log.md` "Verification gates" (FG-1 / INT-7).
