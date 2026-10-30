# robot-arm/tests — FPGA-side integration tests

Placeholder until the Pico frame encoding is chosen (ICD §5). The tests here run
against a **mock Pico**, so the FPGA/PL side can be developed before the arm repo
is ready.

## Planned

- `mock_pico.py` — serial emulator: sends state/encoder frames, toggles
  HEARTBEAT at 100 Hz, asserts STOP, and records the PL's response.
- `test_stop.py` — STOP asserted → PL stops within 100 ms.
- `test_heartbeat.py` — HEARTBEAT absent for 100 ms → Pico-side stop (tested on
  the arm side; the mock asserts the PL side).
- `test_stale_pose.py` — pose age > 50 ms → stop.
- `test_vectors.py` — reads the shared vectors from
  `../../contract/icd/pico_link/vectors/` and checks both sides decode them the
  same way.

## Rules

- Use the shared vectors; do not fork them.
- A test that needs a real Pico is an INT-7 test, not a unit test.
- Record the contract version in the test output.
