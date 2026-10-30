# Pico link — shared conformance vectors

The ICD (`../../pico_link.md`) deliberately leaves encoding, field widths, byte
order, CRC and cadence to the implementers (§5). Once the Pico side chooses a
frame, put the agreed vectors here so both sides test the same bytes.

Suggested layout:

```
vectors/
├─ README.md          # this file
├─ frame.md           # the chosen encoding, with a worked example
├─ pose_valid.json    # a valid pose frame + expected decode
├─ pose_stale.json    # a stale pose (age > 50 ms) -> stop
├─ stop.json          # STOP asserted -> stop
└─ fault.json         # Pico fault state -> PL fault
```

Rules:

- A vector is a byte string plus the expected decoded fields, not a screenshot.
- Both sides add a test that reads these files; do not fork the vectors.
- Changing a vector is a contract change (bump `contract/VERSION`).
