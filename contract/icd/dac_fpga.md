# ICD — DAC80508 ↔ FPGA DDS/SPI

**Status:** **FROZEN Rev A, 2026-11-02**; §3 safe-state clause clarified 2026-11-25
(decision #30) — the wire interface is unchanged. **Owners:** Tung (hardware/DAC), Kevin (FPGA DDS).
**Canonical sources:** `contract/decisions_log.md` #19 and #21;
`contract/system_contract.md` SC-03 and SC-07; `docs/phase2/system_schematic.md`;
`simulations/m16/FINAL_REPORT.md`; `docs/handoff/m16-fpga-handoff.md` §4.

This ICD freezes the wire interface. It does not restate the analog design or the
M16 SPICE evidence.

## 1. Physical layer

| Item | Value |
|---|---|
| Part | TI DAC80508MRTET, WQFN-16, 16-bit, 8 channels |
| Logic level | 3.3 V LVCMOS (HR bank), no translation |
| SCLK | 49.152 MHz = 98.304 ÷ 2 (XO ×3 → ÷2) |
| SPI mode | **CPOL = 0, CPHA = 1**: SDI changes on the rising edge, latched on the falling edge |
| Bit order | MSB first |
| Chip select | one CS low per 24-bit frame; 33 Ω series at the FPGA pin |
| Routing | SCLK/SDI matched pair over continuous ground, ≤50 mm on BRD-01, probe pads at the DAC |
| SDO | optional readback, see §5 |

## 2. Frame and update

- 24 bits per frame: `{RW, 000, A[3:0], DI[15:0]}`, RW = 0 for write.
- **8 data frames + 1 TRIGGER frame = 216 bits.**
- TRIGGER = register `0x05`, bit 4 = 1, data word `0x0010` → frame `0x050010`.
- One TRIGGER per update, **after** the eight data frames. Never two in one period.
- 216 bits at 49.152 MHz = 4.394 µs of clocks; with the mandatory CS gaps the burst is
  **4.720 µs** inside the 5.005 µs period (285 ns idle).
- CS gaps: `tCSH` ≥ 10 ns and `tCSHIGH` ≥ 15 ns → one idle SCLK period on each side of a
  frame (40.7 ns per boundary).
- Datasheet `tDACWAIT` ≥ 1 µs between output updates: satisfied by the 5.005 µs period.

## 3. Init and safe state

1. Write SYNC `0x02` = `0x00FF` once (frame `0x0200FF`) to put all 8 channels in
   synchronous mode. Reset value `0xFF00` is asynchronous.
2. Gain 2 (0–5 V) is the M-variant default; no CONFIG write needed.
   **OPEN follow-up:** `power_tree_v2.md` §7 D2 gives a 0.3–4.6 V DDS limit on
   `+5V_EXC`; decision #31 adopted the rails, not this frozen ICD's amplitude
   clause, so this ICD keeps the 0–5 V default pending a follow-up ICD change.
3. Power-on reset is **midscale** (2.5 V), matching the AC-coupled current loop.
4. **Genuine FPGA/ADC/driver fault:** stop the DDS, write zero-scale to all 8
   channels, then one TRIGGER. **Arm-only STOP (#30):** no DDS/DAC/coil effect —
   field and pose continue. A missed TRIGGER holds the previous sample for one
   period — a one-sample stall, not a glitch.

## 4. Timing margin (mandatory FPGA constraint)

| Spec | Min | Actual at 49.152 MHz | Margin |
|---|---|---|---|
| tSCLKHIGH / tSCLKLOW | 9 ns | 10.17 ns | 1.17 ns |
| tSDIS (setup) | 5 ns | 10.17 ns | 5.17 ns |
| **tSDIH (hold)** | **10 ns** | **10.17 ns** | **0.17 ns** |
| tCSS | 13 ns | 20.3 ns | 7.3 ns |

**Required: delay the SDI output by 2.5 ns** (ODELAY ≈ 32 taps at 78 ps, or a +44° MMCM
phase on the SDI output register). Result: setup 7.67 ns, hold 12.67 ns → 2.67 ns each.
Delaying SCLK is the wrong direction (it improves setup and worsens hold).

## 5. Not available at this rate

| Feature | Reason |
|---|---|
| CRC / frame-error checking | 32-bit frames → 9 × 32 = 288 bits = 5.858 µs > 5.005 µs |
| SDO readback every update | reads are rated 18 MHz (FSDO = 0) or 25 MHz (FSDO = 1); a read is 48 bits = 1.9–2.7 µs. Diagnostic only, in a stretched period |
| SYNC rewrite every update | 10 × 24 bits + gaps = 5.11 µs > 5.005 µs; rewrite periodically |

## 6. Left to the implementers

- FTG256 pin assignment (board netlist, not an interface constraint).
- RTL structure, FIFO depth, CDC implementation between the 32.768 MHz DDS and the
  49.152 MHz SPI domain.
- Optional SDO diagnostic reads and their cadence.
- Bench evidence: one-channel constant current, 8-tone EVM, THD/IMD, SPI eye at the DAC pins.

## 7. Change control

Any change to §1–§5 is a contract change: `contract-change` issue → PR → 2 approvals →
VERSION + CHANGELOG → tag. Do not change it in a team branch.
