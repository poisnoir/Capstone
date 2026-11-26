# Pico 2 link — interface control document

**Canonical location:** `contract/icd/pico_link.md` · **Contract version:** 1.1.5; tag `contract-v1.1.5` published when CI runs; two-approval review pending
**Status:** Rev B, 2026-11-26; STOP scope clarified 2026-11-25 (#30); pin 1
changed to no-connect by #32. Applies to BRD-01 (PL) ↔ Pico 2 (follower).
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
| Connector on BRD-01 | 6-pin `J123`: pin 1 **NC**, pin 2 GND, pin 3 `PICO_TX`, pin 4 `PICO_RX`, pin 5 `PICO_STOP_N`, pin 6 `PICO_HEARTBEAT` (Rev B, #32) |
| Cable | 1 m, shielded, **signal ground only** — no motor current in it |
| Level | 3.3 V LVCMOS UART, no translation (both ends 3.3 V) |
| Rate | 1 Mbaud default; 0.5–3 Mbaud acceptable |
| Grounding | motor return bonded at the Pico, not at BRD-01; single-point bond to chassis |
| Fallback | RS-485 on the same TX/RX pins if the ground test shows >200 mV |

RP2350 I/O is **not** 5 V tolerant. Keep everything 3.3 V.

**Pico power (Rev B, #32).** BRD-01 supplies **no 3V3 on J123** — pin 1 is a
no-connect in the committed netlist. The Pico is powered from its own USB;
do not assume a 3V3 source on this connector. RP2350 I/O is not 5 V tolerant.

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
| Arm-motion stop response | ≤100 ms from host request, power-up/brownout, overcurrent or unconfigured FPGA; tracker field and pose continue (#30) |

## 5. Free choices (implementers)

Encoding (binary, ASCII, JSON), field widths, byte order, CRC or checksum, baud rate within the
range above, cadence above 100 Hz, acks/retries, the Pico state machine, homing sequence,
acceleration profile, steps/mm, limit handling, and how the Pico clamps out-of-range targets.

## 6. Failsafe

- **STOP** is an active-low level at `J123.5` (`PICO_STOP_N`), driven by the
  power-sheet latch: `U755` (74LVC1G08) ANDs `PICO_STOP_REQ_N` (`U4.P4`, with the
  `R754` pull-down for an unconfigured FPGA) with the arm latch `U753.5 (Q)` on
  `/power/ARM_Q`. `U753.3 (~Q)` is a no-connect. Cable unplugged → 0 V → stop.
  It is a level, not a message.
- Power-up / +3.3 V brownout (U751) and `/DRIVER_FAULT_N` (U752) clear the latch,
  which asserts STOP; SW750 arms it. STOP is **arm motion only**, ≤100 ms; the
  field rail `+15V_FUSED` is unswitched and pose keeps flowing (#30).
- **HEARTBEAT** absent for 100 ms → the Pico stops locally.
- There is **no panel E-stop on BRD-01**. The last hardware-independent stop path
  was removed by explicit decision (#30): STOP depends on the host link, the
  FPGA, the cable and the Pico firmware. The UART carries control data, and a
  host STOP request travels over it; it is no longer correct to call the UART
  "never the safety path".
- A genuine FPGA/ADC/driver fault is a separate tracker-side safe state: the DDS
  stops and all eight DAC channels go zero-scale (`icd/dac_fpga.md` §3).

## 7. Open items

1. Confirm a free UART plus two GPIO on the existing follower board (header or test pads). If not
   available, a 4-wire pigtail is the fallback — no board respin.
2. The Pico side supplies the frame definition once chosen; the PL side freezes its encoder to it.

## 8. Related

- `docs/handoff/m16-fpga-handoff.md` §1.1 — role split.
- `docs/phase2/system_schematic.md` §6 — BRD-01 pin assignment.
- `docs/phase2/fpga_integration_options.md` — why there is no PS.
