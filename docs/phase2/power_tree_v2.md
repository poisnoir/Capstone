# BRD-01 power tree v2: requirements and component values

**Status: LOCKED (2026-11-25, decision #31). Adopted as the BRD-01 power tree;
supersedes the part list of decision #20.** The captured schematic (§9, ERC 0/0)
and the committed netlist in
[brd01_wiring_manifest.md](brd01_wiring_manifest.md) implement these rails
(`+6V`, `+3.3V`, `+5V_EXC`, `+5VA`, MGJ2D151515SC). This file is the power
authority for the as-built board; the older v1 tree in
[power-tree.md](../../hardware/brd-01/kicad/power-tree.md) is historical.
The §7 D2 tone band is locked by decision #33 (2026-11-26): 0.3–4.6 V, centre
2.45 V, on a 5.0 V rail. The §7 bench checks C1/C5/C6/C7 and the §9
`TRIP_REF` reconciliation remain open. No rail or value is changed here.

Each number is tagged:

- **[DS]**: read from the manufacturer datasheet (revision given in §8).
- **[doc]**: from an existing design doc.
- **[calc]**: calculated here from [DS] values.
- **[est]**: estimate. Verify before ordering.

---

## 1. Why v2

| Problem in v1 | v2 fix |
|---|---|
| U146 drops 15 V → 5 V: 0.8–1.5 W in the LDO | U146 fed from a 6 V buck: about 0.06 W |
| An LDO cannot make 5.0 V from the OKI (4.8–5.2 V out [DS]) | 6 V pre-rail leaves about 1 V of LDO headroom |
| 4.6 V +5VA fails: AD7768-4 AVDD1 min is 4.5 V [DS] and the TPS7A47 is ±2.5% [DS] | +5VA stays at 5.0 V |
| DAC80508 and LTC1563-2 sit on the OKI's 50–75 mV switching ripple [DS] | Own low-noise LDO: `+5V_EXC` |
| U1 TPS7A2033 burns about 0.5 W making 3.3 V from 5 V | 3.3 V from a buck |
| Excitation current at 20–34 kHz would modulate a shared analog rail | Separate excitation and receiver LDOs |

## 2. Topology

```text
+15V_FUSED ─┬─ U5 MGJ2D151515SC ─ U6 LT3045-1 / U2 LT3093 ─► ±12VA            (unchanged)
            │
            └─ U147 TPSM63604, 6.0 V, 1.024 MHz synced ─► +6V ── PG_6V
                  ├─ U144 TPS62130A ─► +1V0_FPGA   EN ← PG_6V    ┐
                  ├─ U145 TPS62130A ─► +1V8_FPGA   EN ← PG_1V0   ├ FPGA rails
                  ├─ U7 TPS62130A ─► +3.3V       EN ← PG_1V8   ┘
                  ├─ FL1 damped LC ─ U149 TPS7A4701 ─► +5V_EXC  (DAC80508, 8× LTC1563-2)
                  └─ FL2 damped LC ─ U146 TPS7A4701 ─► +5VA     (AD7768-4, 2× ADA4940-2)

FPGA pin BUCK_SYNC (1.024 MHz = 32.768 MHz ÷ 32) ─ 1 nF ─► U147 EN/SYNC
```

The passives, the FL1/FL2 filter labels and the `PG_6V`/`BUCK_SYNC` names were
proposals. Regulator designators follow the captured schematic (§9): U147
(6 V), U7 (3.3 V), U149 (`+5V_EXC`), U146 (`+5VA`) and U5 (±12VA).

Removed: U3 OKI-78SR-5, U1 TPS7A2033, net `+5V`.

### Why the TPSM63604 and not the TPSM53604

Both are TI 36 V, 4 A buck modules with the inductor built in. The
**TPSM53604 runs in pulse-frequency mode (PFM) below about 0.5–0.55 A** at
15 V in and 5–7 V out (datasheet Figure 7-14), and it cannot be forced into
fixed-frequency PWM [DS]. Our 6 V load is about 0.4–0.9 A, so it would often
sit in PFM. PFM bursts at a load-dependent rate that can fall in the 20–34 kHz
tone band. Its 1.4 MHz frequency is also fixed internally [DS].

The **TPSM63604** keeps a constant switching frequency across the full load
range (forced PWM after soft start). Its frequency is set by a resistor
(200 kHz–2.2 MHz) and it can be synchronized to an external clock [DS]. It is
a different package and pinout. Check its price and availability before
committing.

---

## 3. Load tally

### +5VA (receiver)

| Load | Typ | Max | Source |
|---|---|---|---|
| AD7768-4 AVDD1, fast mode, input precharge on | 18.2 mA | 20.3 mA | [DS] |
| … with both reference precharge buffers on | 28.8 mA | 32.5 mA | [DS] |
| AD7768-4 AVDD2, fast mode | 18.8 mA | 20.3 mA | [DS] |
| 2× ADA4940-2, 4 amplifiers × 1.25 / 1.38 mA | 5.0 mA | 5.5 mA | [DS] |
| ADA4940-2 output drive into the ADC inputs (precharge buffers on) | ~1 mA | ~2 mA | [est] |
| **Total** | **~43 mA** | **~48 mA (60 mA with reference buffers on)** | |

ADA4940-2 at 5 V [DS]: supply range 3–7 V, output swing to within 0.1 V of
each rail (0.1–4.9 V; the ADC needs 0.45–4.55 V per leg), PSRR 90 dB typ /
80 dB min at DC.

### +5V_EXC (excitation)

| Load | Typ | Max | Source |
|---|---|---|---|
| DAC80508 IDD, internal reference on | 5 mA | 6 mA | [DS] |
| DAC80508 output drive into 8 filter inputs | ~2 mA | ~4 mA | [est] |
| 8× LTC1563-2, high-speed mode, 10.5 / 17 mA each at 4.75 V | 84 mA | 136 mA | [DS] |
| LTC1563-2 output drive (8 outputs, ~5 kΩ nominal load each) | ~4 mA | ~8 mA | [est] |
| **Total** | **~95 mA** | **~155 mA** | |

LTC1563-2 notes [DS]:

- LP (pin 1) tied to V+ selects **high-speed mode**. That is correct: low-power
  mode only reaches a 25.6 kHz cutoff, and the design uses 60 kHz.
- ~EN (pin 9) is tied to GND on the schematic, which enables the part ✓.
- Output swing at VS = 4.75 V, 10 kΩ load: high ≥ 4.55 V, low ≤ 0.05 V.
- AGND sits at VS/2 = 2.5 V, matching the DAC midscale.
- The datasheet recommends low-noise linear supplies and says switching
  supplies reduce the filter's dynamic range. That supports a dedicated LDO
  for this rail.

The FT231X (U142) moves off this rail to `+3.3V` (see D3 in §7).

### +3.3V (digital)

| Load | Max | Source |
|---|---|---|
| AD7768-4 IOVDD, fast mode, wideband filter | 46.8 mA | [DS] |
| Artix-7 35T VCCO, 4 banks (see FPGA estimate below) | 30 mA running; 164 mA power-on surge | [DS] DS181 Tables 5–6; [est] |
| FT231X VCC + VCCIO (moved from +5V) | 8.4 mA | [DS] |
| W25Q64 flash, Y1 oscillator | ~40 mA | [est] |
| Comparators, open-drain buffers, latch logic, pull-ups | ~5 mA | [est] |
| J123 Pico header pin 1 | 0: **BRD-01 does not power the Pico** (D4) | |
| **Total** | **~0.13 A running; ~0.26 A during FPGA power-on** | |

### +1V0_FPGA and +1V8_FPGA

#### FPGA running-current estimate

Basis: XC7A35T-1 at 85 °C junction temperature. Logic from
[solver-algorithm-handoff.md](../handoff/solver-algorithm-handoff.md) §6:
the solver is ~25–40 DSP48 and ~7k LUT at 131.07 MHz. DDS, Goertzel demodulator,
ADC capture and DAC SPI add a few kLUT and < 20 BRAM36 at 32.768–98.304 MHz.
One MMCM (VCO 786.432 MHz). Total: ~12k LUT, ~15k FF, 40 DSP, 20 BRAM36.
The per-block figures are engineering estimates using typical 7-series power
per resource at 12.5% toggle [est]. They replace a Xilinx Power Estimator run
until synthesis exists.

| Contributor | VCCINT (1.0 V) | VCCAUX (1.8 V) | VCCO (3.3 V) |
|---|---|---|---|
| Quiescent, 85 °C typ [DS] | 95 mA (+1 mA VCCBRAM) | 22 mA | 4 mA (4 banks) |
| MMCM ×1 | ~30 mA | ~60 mA | |
| Clock trees, 3 domains | ~40 mA | | |
| Logic + routing, ~12k LUT at ~100 MHz avg | ~100 mA | | |
| DSP48 ×40 at 131 MHz | ~60 mA | | |
| BRAM36 ×20 | ~40 mA | ~5 mA | |
| I/O: DAC SPI at 49.152 MHz, ADC SPI/DCLK, UART, Pico, sync | | ~10 mA | ~10 mA |
| **Typical running** | **≈ 0.37 A** | **≈ 0.10 A** | **≈ 15 mA** |
| **Design max** (2× dynamic, 2× static for process/temperature, 50T upgrade) | **≈ 0.8 A** | **≈ 0.2 A** | **≈ 30 mA** |
| Power-on surge the supply must deliver [DS] Table 6 | 215 + 61 = 276 mA | 62 mA | 4 + 160 = 164 mA |

All three are well inside the 3 A TPS62130A rating. The VCCO surge during
power-on, not the running current, sets the +3.3V peak. Confirm with the
Power Estimator once the design synthesizes (FPGA team).

### +6V (sum)

| Branch | Typical | Design max |
|---|---|---|
| +1V0 buck output | 1.0 V × 0.37 A = 0.37 W | 1.0 V × 0.8 A = 0.80 W |
| +1V8 buck output | 1.8 V × 0.10 A = 0.18 W | 1.8 V × 0.2 A = 0.36 W |
| +3.3V buck output | 3.3 V × 0.13 A = 0.43 W | 3.3 V × 0.4 A = 1.32 W |
| Buck subtotal ÷ 85% [est], at 6 V | 1.15 W → 0.19 A | 2.92 W → 0.49 A |
| +5V_EXC + +5VA LDOs (pass-through) | 0.095 + 0.045 = 0.14 A | 0.155 + 0.06 = 0.22 A |
| **+6V total** | **≈ 0.33 A** | **≈ 0.71 A** |

That is about 0.15 A typical / 0.35 A max from the 15 V input. The typical
0.33 A is well below the TPSM53604's ~0.5 A PFM threshold, which confirms
the switch to the TPSM63604 (constant frequency at all loads). The 4 A part
is oversized for current but keeps the module cool and leaves room for the
50T. The 2 A and 3 A family members (TPSM63602/TPSM63603) come in a
different package, so changing to them is a footprint change.

---

## 4. Component values

### U147: +6V pre-regulator, TPSM63604RDLR

| Function | Pin | Part / value | How it was chosen |
|---|---|---|---|
| Input | VIN1 (1), VIN2 (16) ← `+15V_FUSED` | 2× 10 µF 50 V X7R 1210 (GRM32ER71H106KA12L), one per VIN pin, symmetric | ≥ 2× 10 µF required [DS] |
| Input HF | VIN1, VIN2 | 100 nF 50 V X7R 0603 each | layout practice |
| Input bulk | +15V_FUSED near U147 | 68–100 µF 35 V aluminium electrolytic, or C30 if within a few cm | damps cable resonance [DS] §8.3.4 |
| Output voltage | FB (10) | RFBT 49.9 kΩ 0.1% (VOUT → FB), RFBB 10.0 kΩ 0.1% (FB → AGND) | VOUT = 1 V × (1 + 49.9/10) = **5.99 V** [calc]; VFB ±1% [DS] → 5.92–6.06 V |
| Feed-forward | across RFBT | CFF 18 pF C0G | between Table 8-1 values for 5 V (22 pF) and 7.5 V (15 pF) [DS] |
| Output | VOUT1 (8), VOUT2 (9) | 3× 22 µF 25 V X7R 1210 (GRM32ER71E226ME15L) | COUT(min) ≈ 28 µF effective at 6 V [DS] Table 8-1; 3× 22 µF ≈ 40–50 µF after DC bias [est] |
| Frequency | RT (12) | RRT 13.0 kΩ 1% → **1.000 MHz** free-running | RRT = 13.46/fSW − 0.44 kΩ [DS] Eq. 5; Eq. 6 suggests ≈ 0.9 MHz at 15 V in |
| Enable / UVLO | EN/SYNC (14) | RENT 1.00 MΩ (VIN → EN), RENB 118 kΩ (EN → AGND) | on 11.97 V, off 8.62 V [calc] from VEN_RISE 1.263 V and VEN_FALL 0.91 V [DS]; parallel 105 kΩ, inside the ~100 kΩ the datasheet asks for when syncing [DS] |
| Sync | EN/SYNC (14) | CSYNC 1 nF from FPGA `BUCK_SYNC` | 3.3 V edge > 2.4 V threshold, 1 nF [DS] §8.3.7 |
| Bias | VLDOIN (5) → +6V | 1 µF X7R to GND | VOUT ≤ 12 V, so connect to VOUT for efficiency [DS] |
| Power good | PG (13) | 100 kΩ pull-up to +6V → `PG_6V` → U144 EN | 10–100 kΩ, ≤ 16 V [DS]; TPS62130 EN max is VIN + 0.3 V [DS] |
| Switch-node slew | RBOOT (4), CBOOT (3) | leave unconnected (internal 100 Ω) | slower edges, lower EMI [DS] §8.3.9 |
| Switch node | SW (2) | no connection, minimum copper | [DS] |
| Ground | AGND (6, 11), PGND (17–20) | AGND to PGND at one point | [DS] |
| Not connected | NC (15) | GND | [DS] |

**Frequency plan.** The ADC modulator samples at 8.192 MHz (MCLK/4 [DS])
and its filter rejects everything outside the band by 105 dB [DS]. Synced to
1.024 MHz = 8.192 MHz ÷ 8, every harmonic of the buck folds to exactly DC.
Free-running, the frequency can drift ±10% [DS fSW_RT spec]. If it free-runs
within about ±13 kHz of 1.024 MHz, the 8th harmonic aliases into the tone
band (1.02 MHz → 32 kHz) [calc]. That is why RT is set to 1.000 MHz, not
1.024 MHz. Through the LC filter, the LDO and the ADC's 90 dB supply
rejection, a free-running harmonic is attenuated to a negligible level, so the
sync is for determinism rather than survival.

The FPGA needs one spare 3.3 V I/O for `BUCK_SYNC` (32.768 MHz ÷ 32). The
clock must be absent at start-up [DS]. That is automatic: the FPGA is powered
by this module and only drives the clock after configuration. The module
switches to the sync clock after 2048 cycles [DS]. The datasheet gives a sync
range of 200 kHz–2.2 MHz and no limit relative to the RT setting; confirm the
lock on the bench.

### U144, U145, U7: FPGA rail bucks, TPS62130ARGTR

The existing U144/U145 parts already follow TI's typical application
(Table 9-1). Only their input rail, EN source and pull-up rail change.

| Function                          | U144 +1V0_FPGA                          | U145 +1V8_FPGA                      | U7 +3.3V (new)                    | Source                                             |
| --------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------------- | -------------------------------------------------- |
| PVIN, AVIN                        | +6V                                     | +6V                                 | +6V                               |                                                    |
| PVIN cap                          | C180 10 µF → **specify 25 V X7R 1206**  | C184 → same                         | 10 µF 25 V X7R 1206               | [DS] §9.2.2.2.2.2; value field today is only "10u" |
| AVIN cap                          | C183 100 nF                             | C187 100 nF                         | 100 nF                            | required [DS]                                      |
| Inductor                          | L140 XFL4020-222                        | L141 XFL4020-222                    | XFL4020-222                       | [DS] Table 9-1                                     |
| Output cap                        | C182 22 µF                              | C186 22 µF                          | 22 µF X7R                         | recommended 22 µF [DS]                             |
| FB divider (VFB 0.8 V)            | R190 49.9k / R191 200k → **1.000 V**    | R193 249k / R194 200k → **1.796 V** | **619k / 200k → 3.276 V**         | R1 = R2 (VOUT/0.8 − 1), R2 ≤ 400 kΩ [DS] Eq. 6     |
| Output range (VFB 785.6–814.4 mV) | 0.982–1.018 V                           | 1.764–1.829 V                       | 3.217–3.335 V                     | [calc]                                             |
| Artix-7 limit                     | 0.95–1.05 V ✓                           | 1.71–1.89 V ✓                       | VCCO 3.3 V ±5%: 3.135–3.465 V ✓   | [DS] DS181 Table 2                                 |
| Soft start                        | C181 3.3 nF → 1.65 ms                   | C185 3.3 nF → 1.65 ms               | 3.3 nF → 1.65 ms                  | tSS = C × 1.25 V / 2.5 µA [DS] Eq. 10              |
| EN                                | `PG_6V`                                 | `PG_1V0`                            | `PG_1V8`                          |                                                    |
| PG pull-up                        | R192 100k to **+6V**                    | R195 100k to **+6V**                | none: tie PG to GND or leave open | PG < 7 V [DS]                                      |
| FSW                               | **to its own PG (`PG_1V0`) → 1.25 MHz** | GND → 2.5 MHz                       | GND → 2.5 MHz                     | see below                                          |
| DEF                               | GND                                     | GND                                 | GND                               |                                                    |

**U144 FSW change.** At 2.5 MHz the on-time is VOUT/VIN × 400 ns
[DS] Eq. 1: 1.0/6 × 400 = 67 ns, under the 80 ns minimum on-time [DS]. The
part would then lower its own frequency to about 2.1 MHz, which is not
controlled. At 1.25 MHz the on-time is 133 ns. The datasheet requires
starting with FSW low to limit inrush and suggests tying FSW to VOUT or PG
[DS]. Tying it to `PG_1V0` (already pulled to +6V, under the 7 V pin limit)
starts at 2.5 MHz and switches to 1.25 MHz once the rail is good. The 2.2 µH
inductor is the minimum for 1.25 MHz [DS]. U145 (120 ns) and U7 (220 ns)
are fine at 2.5 MHz. Neither 1.25 MHz nor 2.5 MHz puts a harmonic up to the
30th into the ADC band [calc].

U7 uses the captured TPS62130A. The fixed 3.3 V TPS62132 with no divider is an
alternative. The TPS62132's PG floats high when off [DS], which only matters if
something is chained after it. Nothing is, so either works. Keeping the
TPS62130A keeps one part number.

### U149 +5V_EXC and U146 +5VA: TPS7A4701RGWR

| Function | U149 +5V_EXC (new) | U146 +5VA (existing) | Source |
|---|---|---|---|
| IN (15, 16) | +6V via FL1 | +6V via FL2 (was +15V_FUSED) | |
| Input cap | part of FL1: 2.2 µF X7R ≥ 16 V | part of FL2; C188 changes to 2.2 µF ≥ 16 V | ≥ 1 µF [DS] |
| EN (13) | +6V | +6V (was +15V_FUSED) | |
| Output set (ANY-OUT) | 3P2V (6) + 0P4V (10) to GND → **5.0 V** | unchanged → 5.0 V | 1.4 V + sum of grounded pins [DS] Table 6-1 |
| SENSE/FB (3) | to OUT | unchanged | |
| NR (14) | 1 µF X7R | C189 1 µF | CNR 1 µF in the PSRR/noise specs [DS] |
| Output cap (1, 20) | 47 µF X7R ≥ 10 V | C190 47 µF | ≥ 10 µF required, 47 µF ceramic highly recommended [DS] |
| Output range | 4.875–5.125 V | 4.875–5.125 V | ±2.5% [DS] |
| Load max | ~155 mA | ~60 mA | §3 |
| Dissipation | 1.0 V × 0.155 A = 0.16 W | 1.0 V × 0.06 A = 0.06 W | [calc] |
| Unused ANY-OUT pins (4, 5, 8, 9, 11, 12), NC (2, 17–19) | open | open | |

**Excitation headroom.** Two parts limit the swing on a 4.875 V worst-case
rail:

- DAC80508: at gain 2 the span is 0–5.0 V, and the output needs 0.15 V of
  headroom to VDD at 5 mA [DS]. Codes above about 4.7 V clip.
- LTC1563-2: output high is ≥ 4.55 V at VS = 4.75 V [DS], about 0.2 V below
  the rail. At 4.875 V that is about 4.67 V.

**Locked FPGA requirement (#33): keep the DDS tone within 0.3–4.6 V (≤ 92% of
full scale, centre 2.45 V).** The alternative is 5.3 V (add 0P2V +
0P1V), which leaves only 70 mV under the DAC's 5.5 V maximum — rejected.

### D_REF: ADC reference clamp (new)

```text
 U103 OPA192 (on +12VA) ── R186 10 Ω ──┬── ADC_REF (AD7768-4 REF1+, REF2+)
                                       │
                                     D_REF  BAT54 (or the BAS70 already on the receiver BOM)
                                       │ anode at ADC_REF, cathode at +5VA
                                     +5VA
```

The AD7768-4 limits REF+ and the analog inputs to AVDD1 + 0.3 V [DS].
The reference (ADR434 → OPA192 buffer) runs from +12VA.

- **v1:** +5VA came from 15 V and outlived ±12VA at power-down.
- **v2:** +6V stops when the input falls to 8.62 V (U147 UVLO-off). The MGJ2
  is unregulated (line regulation 1%/% [DS]), so at that point ±12VA is
  still about 8 V and the reference still drives 4.096 V into an unpowered
  ADC.

The clamp keeps REF within a Schottky drop of +5VA. Fault current is limited
by the OPA192 output. The AD7768-4 tolerates transient currents up to 100 mA
without latch-up [DS]. Diode leakage at 0.9 V reverse is negligible next to
the buffer's drive.

The ADA4940-2 inputs are also driven from ±12VA stages (Ch0 summer, INA163
outputs), but through 1 kΩ input resistors that limit fault current to about
12 mA. The ADA4940-2 rates only differential input (1.2 V) [DS]. No change
proposed there; check on the bench by cycling power with a tone applied.

### FL1, FL2: damped LC input filters

```text
 +6V ── L 1.0 µH ──┬───────────┬──► LDO IN
                   │           │
                 C 2.2 µF    Rd 0.68 Ω
                   │           │
                  GND        Cd 10 µF
                               │
                              GND
```

| Part | Value | Note |
|---|---|---|
| L | 1.0 µH shielded, ≥ 0.5 A, DCR ≤ 0.1 Ω (for example XFL4020-102) | same family as the buck inductors |
| C | 2.2 µF X7R ≥ 16 V 0805 | also serves as the LDO input capacitor |
| Rd + Cd | 0.68 Ω 0603 in series with 10 µF X7R ≥ 16 V | damping leg: Rd ≈ √(L/C) = 0.67 Ω |

Simulated response [calc]:

| Frequency | Gain |
|---|---|
| Peak (64 kHz) | +2.7 dB |
| Worst point in the 20–34 kHz tone band | +1.8 dB |
| 1.024 MHz (TPSM63604) | −39 dB |
| 1.25 MHz / 2.5 MHz (FPGA bucks' frequencies) | −42 / −55 dB |

The +1.8 dB in the tone band is harmless: the LDO behind it rejects input
ripple by ≥ 55 dB from 10 Hz to 10 MHz [DS]. Without the damping leg the
filter would ring near the tones.

---

## 5. Power-up sequence and timing

| Step | Time (typ) | Event | Source |
|---|---|---|---|
| 0 | 0 | +15V_FUSED rises past 11.97 V | RENT/RENB |
| 1 | +0.7 ms | U147 starts switching | tEN 0.7 ms [DS] |
| 2 | +5 ms (3.5–7) | +6V at 90% | tSS [DS] |
| 3 | ≈ 6 ms | +6V above 94% → `PG_6V` high | PG threshold [DS]; +5V_EXC and +5VA start as +6V rises |
| 4 | ≈ 7.6 ms | +1V0_FPGA good → `PG_1V0` | 50 µs + 0.95 × 1.65 ms [DS] |
| 5 | ≈ 9.2 ms | +1V8_FPGA good → `PG_1V8` | same |
| 6 | ≈ 10.9 ms | +3.3V good | same |
| 7 | + U751 delay | arm latch released; board starts **disarmed** | unchanged |
| 8 | after configuration | FPGA drives `BUCK_SYNC`; U147 locks after 2048 cycles (2 ms) | [DS] |

Checks against the Artix-7 data sheet (DS181):

- Order VCCINT/VCCBRAM → VCCAUX → VCCO is the recommended power-on sequence ✓.
- Each FPGA rail ramps in 1.65 ms, inside the 0.2–50 ms ramp-time window ✓.
- VCCO − VCCAUX may exceed 2.625 V for at most 500 ms per power cycle. On
  power-up VCCAUX comes first. On power-down, U145's PG drops when +1V8 falls
  below 90%, and that disables U7, so +3.3V follows within milliseconds ✓.
- The TPS62130A holds PG low while off [DS], so a downstream rail never
  enables early.

---

## 6. Expected ripple at the analog rails

| Point | Ripple | Source |
|---|---|---|
| +6V at U147 | ~10 mV p-p at 1.024 MHz | [est] |
| After FL1/FL2 (−39 dB) | ~0.1 mV | [calc] |
| After TPS7A4701 (≥ 55 dB) | ~0.2 µV | [DS] + [calc] |
| Seen by the AD7768-4 core (AVDD1 rejection 90 dB) | negligible | [DS] |

**MGJ2 (unchanged ±15 V converter) switches at about 45 kHz typ, unsynced
[DS].** That is inside the ADC passband (0–102 kHz), just above the
20–34 kHz tones. On the ±12VA rails the LT3045/LT3093 reject it, and the
demodulator only looks at the tone bins. Its transformer field is a
placement concern: keep U5 away from the pen connector and the INA163
inputs, and check for a 45 kHz spur (and its drift) on the bench.

Other MGJ2 numbers [DS]: 67 mA per rail rated, minimum load 10% (6.7 mA;
below 5% the output can rise to 1.25× nominal), start-up 10.5 ms typ into
10 µF, line regulation 1.0%/%.

The larger remaining risk is magnetic and ground coupling, not supply
ripple. Place U147 and the FPGA bucks at the power/driver end of the board,
away from the INA163 inputs and the pen connector. Keep their switching
return currents out of the receiver ground.

---

## 7. Decisions and checks

Every paper item is resolved. D2's tone band is locked by decision #33;
what remains is bench verification (§7 checks).

### Decisions (locked with #31; D2 band locked with #33)

| # | Item | Resolution |
|---|---|---|
| D1 | 6 V pre-regulator | **TPSM63604RDLR at 5.99 V, RT 1.000 MHz, synced to 1.024 MHz**, replacing the OKI-78SR-5 (supersedes the decision #20 part list) |
| D2 | `+5V_EXC` voltage | **LOCKED #33: 5.0 V rail.** The DAC80508 keeps its gain-2 0–5 V part span; the FPGA keeps the DDS tone within the locked **0.3–4.6 V band (centre 2.45 V, ≤ 92% FS)**. The 5.3 V ANY-OUT alternative is rejected (70 mV under the DAC 5.5 V maximum). Cross-referenced in `icd/dac_fpga.md` §3, `docs/handoff/m16-fpga-handoff.md` and `dig6_requirements.md` |
| D3 | FT231X supply | **U142 VCC (12) and ~RESET (11) move to `+3.3V`; 3V3OUT (10, net `FT_3V3`) ties to `+3.3V`.** VCC range 2.97–5.5 V; with VCC at 3.3 V, 3V3OUT must be driven with 3.3 V [DS] |
| D4 | Pico power | **BRD-01 does not power the Pico.** J123 pin 1 is a no-connect on BRD-01, so the two 3.3 V supplies are never tied together. The ICD (`contract/icd/pico_link.md`) Rev B now lists pin 1 as NC, aligned by decision #32 (2026-11-26); the Pico uses its own USB |
| D5 | `BUCK_SYNC` pin | **FPGA ball R3** (IO_L8P_T1_34, Bank 34 at 3.3 V, a plain I/O next to R1/R2), 32.768 MHz ÷ 32, through 1 nF to U147 EN/SYNC |

### Checks

| # | Item | Result |
|---|---|---|
| C1 | TPSM63604 sync from RT 1.000 MHz to 1.024 MHz | datasheet gives only the 200 kHz–2.2 MHz sync range, no limit relative to RT. **Bench:** confirm lock on SW with a scope |
| C2 | LTC1563-2 current, swing, LP pin | **closed**: 17 mA max each in high-speed mode; LP = V+ is correct (§3) |
| C3 | ADA4940-2 PSRR at 20–34 kHz | **closed**: about 90 dB (+PSRR) flat from DC to ~200 kHz, ~73 dB at 1 MHz (datasheet Figure 41) |
| C4 | FT231X VCC range | **closed**: see D3 |
| C5 | MGJ2 load margin and 45 kHz | **closed on paper**: ~7–8 mA margin per rail (bom-to-cad.md). **Bench:** look for a 45 kHz spur and its drift; place U5 away from the pen input (§6) |
| C6 | FPGA running currents | **estimated** (§3): 0.37 / 0.10 / 0.015 A typical, 0.8 / 0.2 / 0.03 A design max. FPGA team confirms with the Power Estimator after synthesis |
| C7 | AD7768-4 supply limits at power-up/down | **closed with a fix, one margin open**: no limit between its own supplies [DS], but REF+ ≤ AVDD1 + 0.3 V is violated at v2 power-down. `D_REF` = `D534` (BAS70H,115) is placed (§4). Abs-max is AVDD1 + 0.3 V (`AD7768-4` Rev D, Table 7, p. 23, "Reference Input Voltage to AVSS"); a Schottky clamp holds ADC_REF at AVDD1 + Vf, so the clamp is compliant only while Vf ≤ 0.3 V at the actual fault current. **Bench:** measure V(ADC_REF) − V(+5VA) while cycling +15 V with a 4.096 V reference applied; if it exceeds 0.3 V, fit a lower-Vf part or add a series resistor ahead of D534 |
| C8 | C180/C184 voltage rating | **closed**: specify 10 µF 25 V X7R 1206 (§4); the schematic value field only says "10u" today |

### Schematic changes this implies

| Sheet | Change |
|---|---|
| power | remove U3, U1; add U147 + passives, U7 + passives, U149 + passives, FL1/FL2; move U144/U145/U146 inputs to +6V; U144 EN ← `PG_6V`, U144 FSW ← `PG_1V0`; R192/R195 pull-ups to +6V; U146 EN to +6V; C188 → 2.2 µF; C180/C184 → 25 V |
| power | delete net `+5V`; new nets `+6V`, `+5V_EXC`, `PG_6V`, `BUCK_SYNC` |
| driver | U10 VDD and U80–U87 V+/LP from `+5V` → `+5V_EXC` |
| fpga | U142 VCC, ~RESET, 3V3OUT → `+3.3V`; ball R3 → `BUCK_SYNC` |
| receiver | add D_REF from `ADC_REF` to `+5VA` |
| connectors | J123 pin 1 → no-connect |

## 8. Datasheets used

| Part | Document |
|---|---|
| TPSM63604 | TI SLVSGJ5, April 2022 |
| TPSM53604 (rejected) | TI SNVSBC9C, September 2021 |
| TPS62130A | TI SLVSAG7F, November 2021 |
| TPS7A4701 | TI SBVS204G, May 2026 |
| AD7768-4 | ADI Rev D |
| DAC80508 | TI, 2017–2018 revision |
| LTC1563-2 | ADI/LTC 156323fa |
| ADA4940-2 | ADI ADA4940-1/ADA4940-2 |
| FT231X | FTDI DS_FT231X v1.4 |
| MGJ2D151515SC | Murata KDC_MGJ2 |
| OKI-78SR | Murata |
| Artix-7 | AMD DS181 v1.27.1, July 2024 |

## 9. Schematic implementation (power sheet, 2026-11-24)

The power sheet is captured and wired. The §7 cross-sheet changes are done:

- driver: 27 `+5V` labels became `+5V_EXC` (U10 VDD and the eight LTC1563
  V+/LP pins). The `+5V` net no longer exists anywhere.
- fpga: `U142` VCC and `~RESET` and its two decoupling capacitors moved to
  `+3.3V`; `3V3OUT` is tied to `+3.3V` as D3 requires, with that pin typed
  passive so ERC does not read two sources on one rail; ball `R3` is wired
  to `BUCK_SYNC`.
- connectors: `J123.1` is a no-connect (D4).
- receiver: `D_REF` (§4, C7) is placed as `D534` (`BAS70H,115`,
  `Diode_SMD:D_SOD-123F`, the part already on the receiver BOM). Anode on
  `/receiver/ADC_REF` after `R186`, cathode on `+5VA`; ADC_REF is 6 pins and
  +5VA 30 pins in the netlist. The reference-filter resistor was renamed
  R184 → R186 in commit `8d39a99`.

ERC on the full hierarchy is **0 errors / 0 warnings**.

Reference designators as captured; these are the refs used throughout §2–§7:

| Function | Captured refs |
|---|---|
| 6 V module | U147; C800–C804 input; R803/R804 UVLO; C809 sync; R802 RT; R800/R801/C805 feedback; C806–C808, C810 output; R805 PG pull-up |
| 3.3 V buck | **U7**; C811/C812 input; C814 soft start; L800; R806/R807 feedback; C813 output |
| +5V_EXC LDO | U149; FL1 = L801, C817, R808 + C818; C815 NR; C816 output |
| +5VA input filter | FL2 = L802, C188 (moved, now 2.2 µF), R809 + C820 → U146 |
| ±12VA module | U5 MGJ2D151515SC → U6 LT3045-1 (+12VA) / U2 LT3093 (−12VA) |
| Removed | U3 (OKI-78SR), U8, U9, U1 (removed earlier) |

Joins into the older label-based FPGA buck area use labels: `PG_6V` (U144
EN), `PG_1V0` (U144 FSW, now 1.25 MHz after start-up), `PG_1V8` (U7 EN), and
the former `+5V` global labels there renamed to `+6V`. Generated CAD that
still needs validation is listed in
[bom-to-cad.md](../../hardware/brd-01/kicad/bom-to-cad.md#power-tree-v2-generated-cad-to-validate-2026-11-24).

The `U144.7` FSW strap was briefly regressed to GND in `193f280` (taken from
`b72cffd`) and restored to `PG_1V0` here: 1.0 V from 6 V gives a 67 ns on-time
at 2.5 MHz, under the 80 ns minimum [DS], so the part would fold down to an
uncontrolled ~2.1 MHz, whereas `PG_1V0` starts at 2.5 MHz and switches to
1.25 MHz (133 ns) once the rail is good.

### Open bench item — `TRIP_REF`

The comparator trip numbers are **unreconciled**; do not pick new resistors
before measuring. Three figures are on the table and do not agree:

- `R710` 52.3 kΩ / `R711` 10 kΩ divider: \(V_{REF}\approx0.53\) V at `TRIP_REF`.
- Driver sheet note: **~253 mA at 3.3 V** positive-peak trip with the 1 Ω shunts.
- Driver sheet note: **~280 mA nominal LMH6321 clamp**.

Bench item: measure `TRIP_REF`, the per-channel trip current and the actual
LMH6321 clamp, then reconcile the divider against both notes. No resistor
value changes are authorized by this decision.
