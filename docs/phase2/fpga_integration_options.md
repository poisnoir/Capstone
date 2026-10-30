# FPGA integration options — evaluation note

**Status:** **DECIDED 2026-10-28 — option D (PS-less FPGA on BRD-01).** A, B and C are kept as the
evaluation trail. Decision row #26 in `decisions_log.md`.

**Scope:** how the programmable logic physically gets into BRD-01. It does not reopen the
architecture lock (full-FPGA pose, `AGENTS.md`) or the M16 excitation.

---

## 1. What the pose pipeline actually needs

From `fpga_vs_mcu_compute_budget.md` and `dig6_requirements.md`:

| Resource | Need | Where it fits |
|---|---|---|
| Sine LUT | 4096 × 16 = 64 kb | 2 × BRAM36 |
| Capture ping-pong | 4 ch × 512 × 32 bit × 2 = 128 kb | 4 × BRAM36 |
| Coil geometry | 8 × 101 × 3 × 4 B ≈ 9.7 kB | BRAM |
| Calibration/κ | ≈ 25 kB | BRAM |
| Solver throughput | 0.6–0.7 GFLOP/s at 100 poses/s nominal; 5 GFLOP/s worst-case retry | a few hundred DSPs at 10–20 % efficiency |
| Host link | pose + config at 100–116 Hz | UART/USB, < 1 Mbit/s |

**No frame buffers, no OS, no large dataset.** Everything lives in BRAM and a few kB of
coefficients. The pose rate is 100–116 Hz, not 500 Hz.

## 2. So why DDR3?

DDR3 is not a pose-pipeline requirement. It is a **Zynq PS requirement**: the PS runs Linux for
the host link, logging, calibration UI and camera/viz. Every architecture that keeps the PS needs
DDR3, a 6-layer impedance-controlled board and PMIC sequencing. Every architecture that drops the
PS needs none of it.

The PS's jobs are already listed as host-side work in `AGENTS.md` (`software/` = host tools only:
logging, calibration, viz). The camera/magnified view belongs to the follower/demo subsystem
(PMS-01), not to the pose board.

## 3. Options

| | A. Zynq on BRD-01 | B. Zynq module on BRD-01 | C. Owned dev board | **D. PS-less FPGA on BRD-01** |
|---|---|---|---|---|
| Part | XC7Z020 CLG400 + DDR3L + PMIC | Trenz/MYIR-class SoM | existing board | XC7A50T / XC7S50 CSG324 (or 35T) |
| DDR3 | yes, 2 × 16-bit, length-matched | on the module | on the dev board | **none** |
| Layers | 6 | 4 (carrier) | n/a | **4** |
| Assembly | 0.8 mm BGA + DDR3 | module connector + 0.8 mm BGA-free carrier | none | 0.8 mm BGA only |
| Linux on board | yes | yes | yes | **no — host PC** |
| True single PCB | yes | no (carrier + module) | no | **yes** |
| Design effort | +6–10 weeks, respin risk | +1–2 weeks | 0 | **+2–4 weeks** (no DDR, no PS boot) |
| Rough cost (5 boards) | $500–800 | $350–600 | $0 (owned) | **$250–450** |
| 49 MHz SPI | on-board | on-board | header/ribbon, marginal | on-board |

Cost figures are estimates, not quotes; the part prices move and the fab line is a placeholder.

## 4. Criteria

| Criterion | Weight | A | B | C | D |
|---|---|---|---|---|---|
| Schedule to a working demo | high | poor | good | best | good |
| First-spin risk | high | high | low | none | medium (BGA only) |
| One board / product form | medium | best | medium | poor | best |
| Signal integrity at 49 MHz SPI | medium | best | best | marginal | best |
| On-board Linux/UI | low | yes | yes | yes | no (host PC) |
| Cost | medium | high | high | lowest | lowest |
| Team effort to design/layout | high | high | low | none | medium |

## 5. Open questions to close before deciding

1. **Which FPGA board do we actually own?** The Phase 1 baseline says "owned" but the model is TBD.
   If none is owned, option C is not free and its advantage shrinks.
2. **Is the host PC guaranteed at every demo?** D puts the UI, log and camera on the host. If the
   demo must be self-contained, D loses.
3. **Can we assemble a 0.8 mm BGA?** JLCPCB/PCBWay assembly can; the lab may not. This decides
   whether A/D are buildable at all.
4. **Does the FPGA part need to be a Zynq for the course?** Some capstones expect an SoC. If the
   rubric requires a PS, D is out.
5. **What does the solver need in practice?** Synthesise the HLS kernel for a 35T/50T early; if it
   does not fit, D moves to 100T or back to A/B.
6. **Host link choice for D:** USB-UART (FT2232H/CP2102N) vs Ethernet PHY (RGMII, more pins and
   another clock domain). USB-UART is enough for pose + config.

## 6. Gate

Decide after (a) the owned-board question, (b) an HLS resource estimate for the filament/LM kernel
on a 50T, and (c) the assembly route. Until then BRD-01 keeps the FPGA as a **zone with an open
part** (`system_schematic.md` §6.0) and the 2×20 pin list stays valid as board nets.

**Current leaning:** D if the host PC is always present and a 50T fits; B if on-board Linux is
required; A only if someone owns a 6-layer DDR3 design and can absorb a respin.
