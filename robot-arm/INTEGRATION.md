# Integration — FPGA side ↔ arm side

## Layout

Keep the two repos side by side for integration:

```
~/work/
├─ Capstone/          # this monorepo (FPGA, hardware, contract)
└─ Capstone-arm/      # arm repo (Pico firmware, config, mechanics)
```

`./bootstrap.sh` clones the arm repo into `robot-arm/vendor/arm` (gitignored) if
you prefer a single workspace. It does not copy firmware into this repo.

## Wiring (from `contract/icd/pico_link.md`)

| Signal | Direction | Notes |
|---|---|---|
| 3V3 | PL → Pico | 3.3 V LVCMOS; RP2350 is not 5 V tolerant |
| GND | common | signal ground only; motor return bonded at the Pico |
| TX / RX | PL ↔ Pico | 1 Mbaud default (0.5–3 Mbaud acceptable) |
| STOP | PL → Pico | active-low level, pull-down at the Pico; unplugged = stop |
| HEARTBEAT | PL → Pico | 100 Hz toggle; absent for 100 ms → Pico stops locally |

Cable: 1 m shielded, signal ground only, no motor current. Fallback: RS-485 on
the same TX/RX pins if the ground test shows >200 mV.

## Test procedure

1. **Contract sync** — `capstone/tools/sync-contract.sh latest`; `--check` must
   pass.
2. **FPGA-side mock Pico** — run `tests/mock_pico.py` (placeholder until the
   frame encoding is chosen). It sends state/encoder frames and asserts
   STOP/HEARTBEAT; the PL must stop within 100 ms on STOP or a missing
   heartbeat.
3. **Pico-side ICD test** — the arm repo runs the same vectors from
   `contract/icd/pico_link/vectors/`; a stale pose (age > 50 ms) must stop.
4. **INT-7** — latency, stop, tremor, 98-point accuracy, ICNIRP scan, BOM.

## Safety

- STOP is a hardware level, not a message. The UART is never the safety path.
- The hardware E-stop drops the driver enable independently of both processors.
- A pose older than 50 ms is not acted on; the Pico stops.
- Motor current must not share the signal ground.

## Open items

- Frame encoding, field widths, CRC and cadence (ICD §5) — arm team chooses,
  then add vectors.
- Free UART + two GPIO on the follower board, or a 4-wire pigtail.
- Tilt pivot and the 150 mm keep-out envelope.
