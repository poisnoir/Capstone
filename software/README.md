# software/ — host tools (no pose solve)

Host-side tools only: logging, calibration helpers, visualization, and the
MATLAB golden reference. The pose is solved on the FPGA; do not add a PC-side
solver (AGENTS.md architecture lock).

| Path | What |
|---|---|
| `anser-matlab-ref/` | Unpacked Anser MATLAB golden model, read-only. Port map in its README. |

Planned (not yet committed):

- `log/` — timestamped pose logger (≥100 Hz) and replay.
- `calibration/` — 7×7 κ grid helper, Helmholtz A_sens(f), 98-point RMS report.
- `viz/` — live pose/volume/status view; camera/display control.
- `igtlink/` — optional host link for external viewers.

Rules:

- Do not edit `anser-matlab-ref/`; it is the golden baseline. Port changes into
  `../fpga/`.
- Do not put the pose solver here.
- Keep logs and captured data out of git; use `data/` (gitignored) or an
  external drive.
