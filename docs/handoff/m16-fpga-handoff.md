# M16 FPGA handoff — DDS / SPI / clock for DAC80508 + LTC1563-2

**Project:** EM AccuBot, Team 25 (ELEC/COEN 490), Phase 2
**Audience:** FPGA engineer owning the PL/HLS pose pipeline and the PL↔host/Pico interfaces
**Status:** M16 **selected 2026-10-27**. This supersedes the 8× AD5541A/1 MSPS interface.
**Diagram:** `m16-section-diagram.png` / `.svg` (same folder). The chart and this handoff are cross-referenced.
**Standalone:** this handoff and the diagram are the only files needed for the M16 interface; repo paths below are traceability links.

![M16 block diagram](m16-section-diagram.png)
**Repo references (traceability):** `../../simulations/m16/FINAL_REPORT.md`; `../phase2/dig6_requirements.md`; `../phase2/system_schematic.md`; `../../hardware/bom/BOM_SYSTEM-01.xlsx`.

---

## 1. What changed, in one paragraph

The excitation is now **one DAC80508** (16-bit, 8 channels, SPI, internal 2.5 V reference) followed by **eight LTC1563-2** 4th-order Butterworth filters (fc = 60 kHz, one resistor per channel). The DAC updates at **199.805 kSPS** = 32.768 MHz ÷ 164, not 1.024 MSPS. The SPI runs at **49.152 MHz**, sending eight 24-bit data frames plus a 24-bit TRIGGER frame (216 bits) per update; the burst is 4.394 µs of the 5.005 µs update period. The ADC remains the AD7768-4 at 256 kSPS, 4 DOUT lanes, DCLK 8.192 MHz, N = 512, integer J = 40…68. The DDS stays 32-bit at 32.768 MHz; the DAC words are decimated by 164; the tones remain exact 20–34 kHz. The FPGA no longer drives 8 SPI lanes; one SPI replaces 16 pins, freeing 13 pins in the FPGA pin budget.

## 1.1 Role split — PL, host PC, Pico 2

There is **no PS**. The FPGA is a PS-less Artix-7 on BRD-01; the Pico 2 is a separate MCU at the
follower stage; the host PC is a laptop, not a board.

| Block | Owns | Why |
|---|---|---|
| **PL** (Artix-7 XC7A35T) | DDS, SPI to DAC80508, ADC capture, Goertzel, LM/TRF solver, Kalman/scaling, host link, Pico link, status | Deterministic, parallel, common clock |
| **Host PC** (USB-UART) | Pose log, calibration UI, camera/viz, offline κ fit, protocol config | Not hard real-time; already required for the magnified view |
| **Pico 2** (follower MCU) | Step/dir, encoder loop, homing/limits, local stop/watchdog | Dedicated, deterministic, next to the motor drivers |

The host PC is **not** in the control loop: losing the link costs logging, not control. The Pico 2
is not the pose solver, and the pose never goes through the PC. The PL→Pico link is a 1 m UART
with a hardware STOP and a heartbeat.

---

## 2. Clock tree

| Clock | Source | Value | Use |
|---|---|---|---|
| XO | 32.768 MHz TCXO | 32.768 MHz | ADC MCLK; DDS clock; counter reference |
| PLL | XO ×3 | 98.304 MHz | SPI source |
| SPI SCLK | 98.304 ÷2 | **49.152 MHz** | DAC80508 SCLK (max 50 MHz) |
| DAC update | XO ÷164 | **199.805 kSPS** | DAC word latch; period 5.00488 µs |
| ADC ODR | XO ÷128 | 256 kSPS | AD7768-4 |
| Frame | N = 512 | 2.000 ms | integer-J demod |

**Rules:**
- One XO, one reset. The DDS phase accumulator runs continuously; do **not** reset it at the ADC frame boundary.
- The DAC update and ADC frame are both divided from the 32.768 MHz XO, but they are not 1:1 (164 vs 128). The DDS phase at each DAC sample is deterministic: phase advances by \(164 \times \text{FTW}\) per update.
- The 49.152 MHz SPI is a 3/2 ratio to the XO; use the PLL output (98.304 MHz) divided by 2. Crossing from the 32.768 MHz DDS domain to the 49.152 MHz SPI domain needs a stable latch/handshake; the DAC words are static for the whole frame.

---

## 3. DDS

| Item | Value |
|---|---|
| Accumulator | 32-bit at 32.768 MHz |
| Tones | 20, 22, 24, 26, 28, 30, 32, 34 kHz |
| FTW | \(k \times 262144\), k = 10…17 (exact) |
| LUT | 4096 × 16 sine, 12-bit phase truncation |
| Per-tone | 16-bit amplitude, 16-bit phase offset |
| DAC word | 16-bit unsigned, 0–5 V full scale, midscale 2.5 V |
| Update | every 164 XO clocks; latch 8 words; SPI out |

FTW table:

| Tone | k | FTW (dec) | FTW (hex) |
|---|---|---|---|
| 20 kHz | 10 | 2,621,440 | 0x00280000 |
| 22 kHz | 11 | 2,883,584 | 0x002C0000 |
| 24 kHz | 12 | 3,145,728 | 0x00300000 |
| 26 kHz | 13 | 3,407,872 | 0x00340000 |
| 28 kHz | 14 | 3,670,016 | 0x00380000 |
| 30 kHz | 15 | 3,932,160 | 0x003C0000 |
| 32 kHz | 16 | 4,194,304 | 0x00400000 |
| 34 kHz | 17 | 4,456,448 | 0x00440000 |

Per update:
1. At the ÷164 tick, latch the eight 16-bit words (one per channel) and the per-channel phase/amplitude.
2. Start the SPI sequencer: eight 24-bit frames, CS low per frame, MSB first.
3. After the last frame, send a **9th 24-bit frame writing TRIGGER (0x05) bit 4 = 1**. That is the
   LDAC: the DAC80508 has **no LDAC pin**, so the simultaneous update is a software trigger.
   Total 216 bits = 4.394 µs, still inside the 5.005 µs period.
4. Repeat at 199.805 kSPS.

The DDS phase is **not** reset per frame. The current-sense Ch0 is the phase reference; the per-tone κ calibration absorbs the fixed filter/loop group delay.

---

## 4. DAC80508 interface

**Part:** DAC80508MRTET (WQFN-16), 16-bit, 8 channels, SPI, internal 2.5 V reference, gain 2 → 0–5 V, 5 µs settling.

### 4.1 Pins (FPGA side)

| Signal | Direction | Notes |
|---|---|---|
| DAC_SCLK | out | 49.152 MHz, idle low |
| DAC_CS | out | active low, one per 24-bit frame |
| DAC_SDI | out | MSB first |
| DAC_SDO | in | optional readback |

**There is no `DAC_LDAC` pin.** The DAC80508MRTET has no dedicated LDAC input; pin 23 is a spare.
The simultaneous update is the **TRIGGER register (address 0x05), bit 4 (LDAC, write 1)**.
The same SPI bus carries it as a 9th 24-bit frame.

**Init sequence (once):**
1. SYNC register (0x02) = `0x00FF` → set SYNC-EN = 1 for DAC0…DAC7 (frame `0x0200FF`). The reset
   value `0xFF00` is asynchronous mode, where each channel updates on its own CS rising edge.
2. Gain 2 (0–5 V) is the **M-variant default** (CONFIG 0x03 BUFF-GAIN = 1); no write needed
   unless you change the range or power down a channel.
3. Per update: write the 8 data frames, then write TRIGGER = `0x0010` (frame `0x050010`).

**SPI mode:** CPOL = 0, CPHA = 1 (idle low, SDI changes on the rising edge, latched on the
falling edge) — verify against Figure 65. **Also verify** the 24-bit frame order and the channel
address map (A–H). The BOM part is `DAC80508MRTET`.

### 4.2 Frame

- 24 bits per channel: `{RW, 000, A[3:0], DI[15:0]}` (RW = 0 for write, bits 22:20 reserved 0).
- 8 channels × 24 bits = **192 bits**; plus the 24-bit TRIGGER frame = **216 bits**.
- At 49.152 MHz: 216 / 49.152 M = **4.394 µs** of clocks; the update period is 5.005 µs. With the
  mandatory CS gaps the real burst is **4.720 µs** (285 ns idle) — see §4.5.
- The datasheet requires **≥1 µs between DAC output updates**; one LDAC per 5.005 µs period
  satisfies it. Do not send two TRIGGER frames inside one period.
- If the TRIGGER frame is omitted (asynchronous mode), each channel updates on its own CS rising
  and the first-to-last skew is up to **3.906 µs ≈ 48° at 34 kHz**, not 0.05°. That is a real
  phase error; it can be pre-compensated in the per-tone phase word, but use the TRIGGER.

### 4.3 Channel map

| DAC channel | Coil | Tone |
|---|---|---|
| A | 1 | 20 kHz |
| B | 2 | 22 kHz |
| C | 3 | 24 kHz |
| D | 4 | 26 kHz |
| E | 5 | 28 kHz |
| F | 6 | 30 kHz |
| G | 7 | 32 kHz |
| H | 8 | 34 kHz |

The FG-1 field map may reorder coil→tone; keep the DAC channel map versioned.

### 4.4 Prototype path: Pmod DA4 (AD5628) — different protocol, same architecture

Short answer: **not the same wire protocol.** Same clock, same SPI mode, same CS-per-frame and the
same "software update-all" idea — but a different frame width, field layout, command set and update
divisor. Plan on a small protocol adapter, not a drop-in.

| | Pmod DA4 (AD5628-1) | M16 (DAC80508MRTET) |
|---|---|---|
| Resolution | 12 bit | 16 bit |
| Full scale | 0–2.5 V (1.25 V ref ×2) | 0–5 V |
| Frame | **32 bit**: 4 don't-care + C[3:0] + A[3:0] + 12-bit data + 8 don't-care | **24 bit**: RW + 000 + A[3:0] + 16-bit data |
| Frames per update | **8** (7 data + 1 update-all) | **9** (8 data + TRIGGER) |
| Update-all | command `0010` (write input n, update all) on the 8th frame | TRIGGER 0x05 bit 4, 9th frame |
| Init | internal ref off at reset; command `1000` | SYNC 0x02 = 0x00FF |
| Bits per update | **256** | **216** |
| Divisor | ÷180 = **182.04 kSPS** | ÷164 = 199.805 kSPS |
| SPI mode | CPOL 0, CPHA 1 (latched on falling edge) | same |
| tSU / tH | **4 / 4 ns** | **5 / 10 ns** |
| tCYCLE | 20 ns min (50 MHz) | 20 ns (50 MHz) |
| SDO / LDAC / CLR on header | **none** (CS, MOSI, SCLK, GND, VCC only) | SDO on pin; LDAC is a register bit |
| Settling | 2.5 µs typ | 5 µs |

**Rate.** 256 bits at 49.152 MHz = **5.208 µs**; the M16 5.005 µs period does not fit. Run at
**XO ÷180 = 182.04 kSPS** (5.493 µs). That leaves 285 ns for the eight SYNC-high gaps (35.6 ns
each, against 15 ns min). The image moves to **148.0 kHz**, where the LTC1563-2 is still ≈ −31 dB.

**Command set** (Table 9, Rev. J): `0000` write input n, `0001` update n, **`0010` write input n +
update all (software LDAC)**, `0011` write and update n, `1000` internal ref. Use **`0010`** on the
8th frame. Some older app notes quote `0011` for update-all; that is the "write and update n"
command in Rev. J.

**Frame word:** `(cmd << 24) | (addr << 20) | (code12 << 8)`.

**Init.** The internal reference is **off at reset**. Write command `1000` with the data LSB = 1 →
**`0x08000100`** (Digilent's note quotes `0x8001` as a 16-bit view). Check VREFOUT ≈ 1.25 V, or the
full-scale output ≈ 2.5 V, before trusting anything downstream.

**Data scaling — the trap.** The Pmod full scale is 2.5 V, not 5 V, so **`code12 = code16 / 8`**,
not `code16 >> 4`. A plain truncation halves every command and every coil current.

**Timing is looser on the Pmod.** The AD5628 needs 4 ns setup and 4 ns hold, so at 49.152 MHz it has
~6.2 ns of margin where the DAC80508 has **0.17 ns**. A clean Pmod prototype therefore **does not
de-risk the M16 hold problem** — treat them as two separate risks. The Pmod's own binding spec is
`tCYCLE` ≥ 20 ns (0.345 ns at 49.152 MHz), i.e. it also sits at ~98 % of its rating.

| The Pmod **can** prove | The Pmod **cannot** prove |
|---|---|
| DDS → SPI sequencing, CS/frame timing, software update-all | 16-bit EVM, CRLB/jitter, κ, 98-point RMS, 25 µm tool error |
| LTC1563-2 response, image rejection, filter phase | The DAC80508 0.17 ns hold — the AD5628 spec is 4 ns, not 10 ns |
| Current-loop closure, PM/step, LMH6321 crossover, 150 mA thermal | The final 49.152 MHz / 5.005 µs timing and settling margin |
| Current-sense phase, grounding/crosstalk, demod/solver end-to-end | SDO readback, midscale power-up, 16-bit INL/crosstalk |
| 12-bit resolution (0.61 mV = 0.61 mA step) for a first light | Anything that depends on 0–5 V full scale or 16-bit amplitude |

**RTL:** keep one sequencer (frame width, CS gap, optional post-frame register write) and put the
packer behind a variant parameter — `pack_m16(ch, code16)` and `pack_da4(ch, code12)`. The DDS,
sample tick, capture, demod and solver do not change.

Keep `DAC80508MRTET` on BRD-01 for the accuracy build; the Pmod is a bench vehicle, not a BOM
substitute.

### 4.5 SPI timing margin at 49.152 MHz — and the PCB rule

The DAC latches SDI on the **SCLK falling edge** (`tCSS`/`tCSH` are both referenced to the falling
edge), so the standard Xilinx ODDR arrangement — SDI and SCLK both launched on the same 49.152 MHz
rising edge — gives **half a period** of setup and half a period of hold.

| Spec | Min | At 49.152 MHz | Margin |
|---|---|---|---|
| fSCLK (write) | 50 MHz max | 49.152 MHz | 1.7 % |
| tSCLKHIGH | 9 ns | 10.17 ns | 1.17 ns |
| tSCLKLOW | 9 ns | 10.17 ns | 1.17 ns |
| tSDIS (setup) | 5 ns | 10.17 ns | 5.17 ns |
| **tSDIH (hold)** | **10 ns** | **10.17 ns** | **0.17 ns** |
| tCSS (CS before 1st falling edge) | 13 ns | give 20.3 ns | 7.3 ns |
| tCSH (last falling edge to CS high) | 10 ns | give 20.3 ns | 10.3 ns |
| tCSHIGH (CS high between frames) | 15 ns | give 20.3 ns | 5.3 ns |
| tDACWAIT (between output updates) | 1 µs | 5.005 µs | 4.0 µs |

**Hold is the binding constraint.** TI specifies 50 MHz operation with a 10 ns hold, i.e. the part
is characterised at exactly 50 % duty with **zero** hold margin. 10.17 ns is not margin — it is
0.17 ns, which is ~3 cm of PCB trace or one connector pin of skew. A 0.5 m ribbon cable cannot
guarantee it.

**Fix on the FPGA side: delay SDI, not SCLK.** Delaying SCLK makes setup better and hold *worse*.
Delay the SDI output by **~2.5 ns** (ODELAY ≈ 32 taps at 78 ps, or a +44° MMCM phase on the SDI
output register). That trades the 5.17 ns of surplus setup for hold and lands at:

| | After +2.5 ns SDI delay | Margin |
|---|---|---|
| setup | 7.67 ns | 2.67 ns |
| hold | 12.67 ns | 2.67 ns |

Do **not** try to fix it with duty cycle: `tSCLKHIGH`/`tSCLKLOW` ≥ 9 ns caps that trick at about
1.3 ns of hold margin.

**Do not stream 216 bits back-to-back.** Each 24-bit frame is its own access cycle, so CS must rise
between frames: `tCSH` ≥ 10 ns and `tCSHIGH` ≥ 15 ns. Use one idle SCLK period each side
(40.7 ns per boundary, 8 boundaries = 325 ns). Burst = 4.395 + 0.325 = **4.720 µs**, leaving
**285 ns** idle in the 5.005 µs period. If the RTL just toggles CS every 24 bits with no gap, it
violates both.

**Placement rule.** Since 2026-10-28 the electronics is **one board (BRD-01)**, with the DAC80508
and the FPGA on it (§6.0 of `system_schematic.md`). For on-board or module FPGA integration the SPI
is a ~30–50 mm trace and the cable problem disappears:

1. **FPGA and DAC on BRD-01** (~30–50 mm): SCLK/SDI as a matched pair over continuous ground,
   33 Ω series at the FPGA pin, SDI +2.5 ns, probe pads at the DAC. **This is the plan.**
2. If the owned **dev board** is used (option C), the SPI crosses a header/cable: matched pair,
   no ribbon, per-board delay calibration, ≤150 mm.
3. Fallback if the margin cannot be held: SCLK 32.768 MHz → 216 bits = 6.59 µs; with the CS gaps
   the update is **÷224 = 146.3 kSPS** (÷228 = 143.7 kSPS with full gaps). The image moves to
   112 kHz where the LTC1563-2 is only ≈ −22 dB, so retune the filter (one resistor/channel) or
   accept a degraded prototype.

**No VIO trap:** the 50 MHz write rating applies to both VIO ranges (1.7–2.7 V and 2.7–5.5 V).
The 12/18/25 MHz rows in Table 7 are **read/daisy-chain** (SDO) only.

### 4.5.1 Verdict — is 49.152 MHz implementable?

**The protocol: yes. The electrical margin: only with the SDI delay and an on-board SPI.**

The protocol is simple and deterministic: 24-bit CS-delimited frames, a short frame is *ignored*
(not misapplied), power-on reset is midscale on the M variant, and the only stateful setup is one
SYNC write. Nothing in the logic is fragile.

What is tight is the clock. Any SCLK that fits 216 bits **and** the CS gaps into 5.005 µs is
≥ ~45 MHz (216T + 8 × 25 ns ≤ 5005 ns → f ≥ 44.95 MHz; with comfortable 40.7 ns gaps, ≥ 46.1 MHz).
So the half period can never exceed ~11.1 ns against a **10 ns hold spec** — the hold margin is at
most ~1.1 ns anywhere in the feasible window, and 0.17 ns at 49.152 MHz. **The SDI delay is
mandatory at any clock that supports 199.805 kSPS, not a tuning option.** After the +2.5 ns delay
the pin-level margin is 2.67 ns each way; allow ~0.3 ns for connector/trace skew and you still have
~2.3 ns, which is a normal manufacturable margin.

**Three things the protocol cannot give you at this rate:**

| Feature | Why it does not fit |
|---|---|
| **CRC / frame-error checking** | 32-bit frames → 9 × 32 = 288 bits = **5.858 µs** > 5.005 µs. CRC is only usable if the update rate drops. |
| **SDO readback every update** | Reads are rated **18 MHz** (FSDO = 0) or **25 MHz** (FSDO = 1); a read is 48 bits = 1.9–2.7 µs. Bring-up diagnostic only, done by stretching one update period. |
| **Re-writing SYNC (0x02) every update** | 10 × 24 = 240 bits + gaps = **5.11 µs** > 5.005 µs. Re-write it periodically (or after any suspected reset) instead. |

**Failure modes are graceful:** a truncated frame is ignored, a missed TRIGGER holds the previous
sample for one period, and a lost SYNC write only re-enables asynchronous mode (per-channel skew),
it does not corrupt data. There is no CRC, so a bit flip in the *address* field would write one
sample to the wrong channel — keep the SPI short and shielded, and watch the current-sense fault
taps for it.

**Decision point:** on-board (≤50 mm, matched SCLK/SDI pair, +2.5 ns SDI delay) → stable at
49.152 MHz. Across a header plus a long ribbon (owned dev board, option C) → not stable at any
clock that supports 200 kSPS.


### 4.6 Output scaling

- 0–5 V maps to 0–500 mA in the current loop; 150 mA = 1.5 V.
- The sine is around 2.5 V; the 100 µF coupling blocks DC.
- Per-tone amplitude is a 16-bit word; the 8 tones are **not** summed in one DAC — each channel carries one tone. The current-sense summer sums the eight coil currents; the ADC Ch0 sees eight tones.

---

## 5. LTC1563-2 filter (analog, no FPGA control)

- 4th-order Butterworth, fc = 60 kHz; \(R = 10\,\text{k}\Omega \times 256/60 = 42.67\,\text{k}\Omega\) (0.1%).
- One IC per channel; no clock, no digital control.
- Image at 165.8 kHz: **−35.3 dB**; phase at 34 kHz ~−90°; the per-tone κ calibration absorbs it.
- The filter is before the OPA192/LMH6321 current loop; the loop stability is a bench item.

---

## 6. ADC capture

| Item | Value |
|---|---|
| Part | AD7768-4, 4 channels, 24-bit |
| ODR | 256 kSPS; DCLK 8.192 MHz |
| Lanes | 4 DOUT; 32-bit frames |
| Control | SYNC/START, RESET, DRDY; SPI config only |
| Frame | 512 samples = 2.000 ms |
| Channels | Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference |

- One-time START/SYNC after power-up; discard the first 68 samples (266 µs); then count DRDY.
- Ping-pong BRAM: 4 × 512 × 32 bit = 64 kb per frame; 2 frames = 128 kb.
- Do **not** pulse SYNC per frame; it breaks the integer-J phase.

---

## 7. Demod / solver / output

- Goertzel per tone per channel: 8 × 4 = 32 complex outputs per frame.
- \(J_k = f_k/500 = 40, 44, \ldots, 68\); rectangular + integer-J primary; Hamming fallback.
- \(Y_I\) from Ch0 per tone; \(Y_V\) from the pen per tone; κ per coil/tone.
- Solver: 8×5 LM/TRF, bounds, warm start, retry; 800 filament segments.
- Timing budget: 2.000 ms acquisition + 0.133 ms ADC delay + 0.5 ms demod + 3–5 ms solve + overhead = 6.6–8.6 ms; 115–151 Hz.
- PL → host PC over USB-UART (log/UI); PL → Pico 2 over UART with STOP and HEARTBEAT; the Pico 2 is the follower motor controller, not the pose solver.

---

## 8. FPGA pin assignment (M16)

| Pin | Signal | Direction | Notes |
|---|---|---|---|
| 1–2 | +3.3 V | power |  |
| 3–4 | GND | power |  |
| 5 | MCLK_ADC | in | 32.768 MHz from XO |
| 6 | DCLK | in | 8.192 MHz from ADC |
| 7–10 | DOUT0–3 | in | ADC Ch0–Ch3 |
| 11 | DRDY | in | 256 kHz |
| 12 | SYNC_START | out | one-time |
| 13 | ADC_RESET | out | active low |
| 14 | ADC_SPI_SCLK | out | config |
| 15 | ADC_SPI_MOSI | out | config |
| 16 | ADC_SPI_MISO | in | config |
| 17 | ADC_SPI_CS | out | config |
| 18 | GND | power |  |
| 19 | DAC_SCLK | out | 49.152 MHz |
| 20 | DAC_CS | out | active low |
| 21 | DAC_SDI | out | MSB first |
| 22 | DAC_SDO | in | optional |
| 23–35 | spare | — | **13** pins freed (no LDAC pin; 8-lane DAC removed) |
| 36 | GND | power |  |
| 37 | ESTOP_STATUS | in | opto-isolated |
| 38 | WATCHDOG_KICK | out | to Pico/relay |
| 39 | FAULT_IRQ | in | wired-OR fault |
| 40 | GND | power |  |

These are on-board nets on BRD-01 (option D), not a header. The 13 spare pins are available for the host UART, Pico UART, config flash and debug. Do not repurpose the ADC/DAC pins without a schematic revision.

---

## 9. Calibration / register map (proposal)

| Address | Register | Notes |
|---|---|---|
| 0x00 | CONTROL | enable, reset, filter on/off, test mode |
| 0x04 | TONE0_FTW | 32-bit; k×262144 |
| 0x08 | TONE0_AMP_PHASE | 16-bit amp + 16-bit phase |
| … | … | 8 tones |
| 0x40 | KAPPA[8] | per-coil/tone calibration |
| 0x60 | DAC_CH_MAP | coil→DAC channel |
| 0x64 | SUMMER_GAIN | 2.0103 or 1.5 |
| 0x80 | STATUS | tracking/clamped/stopped/fault, drop count |
| 0x84 | POSE | x,y,z,θ,φ + timestamp |

Calibration flow: Helmholtz \(A_{sens}(f)\) → 7×7 κ/zOffset → per-tone amplitude/phase → current-sense \(I_{out}\) → verify 98-point RMS. The FPGA uses live per-tone \(I_{out}\) from Ch0; no stored \(I_{store}\) file is required.

---

## 10. Fault / stop

- **E-stop:** NC mushroom cuts the +15 V driver enable; the FPGA gets an opto-isolated `ESTOP_STATUS`; it cannot re-enable the driver.
- **Watchdog:** `WATCHDOG_KICK` to the Pico/relay; a missing kick stops the follower.
- **Overcurrent:** per-coil peak comparators wire-OR to `FAULT_IRQ`; the FPGA disables the DAC channels and flags.
- **Status:** tracking / clamped / stopped / fault; the Pico stops ≤100 ms.

---

## 11. Bring-up order

1. **Clock:** 32.768 MHz at the ADC/FPGA; 49.152 MHz at the DAC; 199.805 kSPS update; scope.
2. **SPI:** 216-bit burst (8×24 data + 24-bit TRIGGER); CS per frame; DAC midscale on all 8 channels; readback if SDO.
3. **One tone:** 20 kHz, 150 mA command; DAC output; filter output; current-sense; FFT.
4. **Eight tones:** current-sense FFT; image at 165.8 kHz; 8-tone EVM; target ≤−60 dBc.
5. **ADC:** 4 lanes, 256 kSPS, 32.768 Mbit/s; zero dropped frames over 1 hour.
6. **Demod:** Goertzel vs MATLAB/Python golden; integer-J.
7. **Solver:** 98-point grid; worst-case retry; 100 Hz.
8. **Fault/E-stop:** timing; overcurrent; watchdog.
9. **1-hour moving run:** zero drops, no retry storm.

**Pass criteria (from the M16 report):** filter image ≤−35 dB; summer 8-tone EVM ≤−60 dBc (7 dB margin at −110 dB THD); DAC crosstalk ≤−85 dBc; ADC zero drops; pose 115–151 Hz.

---

## 12. What the FPGA does **not** own

- LTC1563-2 fc/phase (analog, fixed resistor).
- Current-loop stability/compensation (analog/bench).
- LMH6321 crossover distortion (bench).
- EMI/layout/thermal (board/bench).
- The final 8-tone FFT and jitter measurement (bench).
- Pico 2 motor control (step/dir, encoder loop, homing/limits/local stop) is a separate MCU; the PS is the host/coordinator, not the motor controller.

---

## 13. Open items / risks

| Item | Risk | Action |
|---|---|---|
| DAC80508 SPI mode/TRIGGER/address map | Wrong frame → no output or no simultaneous update | Read the datasheet; logic-analyser the first 216-bit burst |
| 49.152 MHz PLL/CDC | Setup/hold, jitter | Constrain the PLL; verify with the scope; keep the SPI away from the analog |
| **SPI hold 0.17 ns** | Data hold at the DAC pin; header/cable skew | Delay SDI ~2.5 ns; keep the DAC on the FPGA board; probe SCLK/SDI at the DAC |
| 199.805 kSPS ÷164 | Non-200k update; DDS phase | Verify the ÷164 counter and the DAC word latch |
| 13 spare pins | Board mapping | Freeze the FTG256 pin assignment before layout |
| Filter phase/κ | Phase error | Calibrate per tone; 0.1% R; 1% C0G |
| Loop PM/step | Oscillation | Bench; lead network; 150 mA first |
| DAC INL/IMD | 8-tone products | Bench one channel; crosstalk screen |
| EMI | In-band spurs | One-box shield; star ground; bench FFT |

---

## 14. Files

- `m16-section-diagram.png` / `.svg` — M16 block diagram (same folder); the handoff and diagram are cross-referenced.
- `../../simulations/m16/FINAL_REPORT.md` — filter/summer/INL/crosstalk/CRLB results.
- `../../simulations/m16/*.cir`, `*.raw`, `figs/*.png` — netlists and figures.
- `../phase2/dig6_requirements.md` — clock/DDS/capture/demod/timing.
- `../phase2/system_schematic.md` — BRD-01 zones and pin assignment.
- `../../contract/icd/pico_link.md` — PL ↔ Pico 2 interface contract.
- `../../hardware/bom/BOM_SYSTEM-01.xlsx` — DAC80508 + LTC1563-2 BOM.

---

## 15. Handoff checklist

- [ ] Read the M16 report and the updated DIG-6.
- [ ] Confirm the PL/host/Pico 2 split: PL = pose; host PC = log/cal; Pico 2 = motor control.
- [ ] Verify the DAC80508 SPI mode, 24-bit frame, channel addresses, and TRIGGER 0x05 bit 4.
- [ ] Implement the 32.768/98.304/49.152/199.805 clock tree and reset.
- [ ] Implement the 8-tone DDS with the FTW table, LUT, amplitude/phase.
- [ ] Implement the 216-bit SPI burst (8 data frames + TRIGGER 0x05 bit 4); no LDAC pin.
- [ ] Add the ~2.5 ns SDI output delay; measure setup/hold at the DAC pins, not the FPGA pins.
- [ ] Implement the AD7768-4 capture (4 lanes, 256 kSPS, ping-pong).
- [ ] Implement the Goertzel demod (8 × 4), integer-J.
- [ ] Implement the 8×5 solver, filter, scaling, Pico output.
- [ ] Implement the calibration registers and κ.
- [ ] Implement the E-stop/watchdog/fault status.
- [ ] Run the bring-up and log the results.
