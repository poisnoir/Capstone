# Pico 2 link — interface control document

**Canonical location:** `contract/icd/pico_link.md` · **Contract version:** 1.0.0
**Status:** Rev A, 2026-10-28. Applies to BRD-01 (PL) ↔ Pico 2 (follower).
**Owners:** PL side = FPGA engineer; Pico side = follower firmware.
**Scope:** the minimum contract. Encoding, framing and timing details are the implementers' choice
as long as this document holds.

---

## 1. Division of work (fixed)

- The **PL solves the pose** (architecture lock, `AGENTS.md`).
- The **Pico drives the follower**: motion, limits, homing, local stop.
- The Pico is **not** the pose solver.

Why: the LM solve needs 0.6–0.7 GFLOP/s nominal (`fpga_vs_mcu_compute_budget.md` §3) and the
RP2350 delivers ~0.15 GFLOP/s. A Pico-side solve runs at ~20–25 Hz against a 100 Hz requirement.
The PL also keeps the ADC capture and Goertzel regardless — raw ADC would be ~3 MB/s.

## 2. Physical layer

| Item | Value |
|---|---|
| Connector on BRD-01 | 6-pin: 3V3, GND, TX, RX, STOP, HEARTBEAT |
| Cable | 1 m, shielded, **signal ground only** — no motor current in it |
| Level | 3.3 V LVCMOS UART, no translation (both ends 3.3 V) |
| Rate | 1 Mbaud default; 0.5–3 Mbaud acceptable |
| Grounding | motor return bonded at the Pico, not at BRD-01; single-point bond to chassis |
| Fallback | RS-485 on the same TX/RX pins if the ground test shows >200 mV |

RP2350 I/O is **not** 5 V tolerant. Keep everything 3.3 V.

## 3. Information that must cross

| Direction | Content |
|---|---|
| PL → Pico | tool pose (x, y, z, θ, φ), validity/status flags, pose age or timestamp, commands (engage / home / stop) |
| Pico → PL | state (idle / homing / tracking / stopped / fault), limit status, encoder position, fault code |
| Discrete | STOP (PL → Pico, level) |
| Discrete | HEARTBEAT (PL → Pico, 100 Hz toggle) |

## 4. Rates and limits

| Requirement | Value |
|---|---|
| Pose update | ≥100 Hz |
| Maximum pose age acted on | **50 ms** — older → stop |
| State / encoder report | ≥50 Hz |
| Stop response | ≤100 ms |

## 5. Free choices (implementers)

Encoding (binary, ASCII, JSON), field widths, byte order, CRC or checksum, baud rate within the
range above, cadence above 100 Hz, acks/retries, the Pico state machine, homing sequence,
acceleration profile, steps/mm, limit handling, and how the Pico clamps out-of-range targets.

## 6. Failsafe

- **STOP** is a hardware active-low level with a pull-down at the Pico. Cable unplugged → 0 V →
  stop. It is a level, not a message.
- **HEARTBEAT** absent for 100 ms → the Pico stops locally.
- The **hardware E-stop** drops the driver enable independently of both processors.
- The UART carries control data only. It is never the safety path.

## 7. Open items

1. Confirm a free UART plus two GPIO on the existing follower board (header or test pads). If not
   available, a 4-wire pigtail is the fallback — no board respin.
2. The Pico side supplies the frame definition once chosen; the PL side freezes its encoder to it.

## 8. Related

- `docs/handoff/m16-fpga-handoff.md` §1.1 — role split.
- `docs/phase2/system_schematic.md` §6 — BRD-01 pin assignment.
- `docs/phase2/fpga_integration_options.md` — why there is no PS.
