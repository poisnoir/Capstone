# hardware/brd-01/driver — closed-loop AC current driver (reference)

Upstream (pristine, do not edit): `vendor/anser-osf/Design Files/AC Current Driver/`
- `CAD/ac_driver_coil_circuit_Rev_A.sch` + `.pcb` (DesignSpark) + `CAD/Gerbers/Coil Driver Board PCB Gerber.zip`
- `Datasheets/` — `lm7171.pdf` (current-feedback amp), `LM311.pdf`, `tl081.pdf`, `MCP23008.pdf`, `mcp4562.pdf`, `IDT74FCT807BT.pdf`, `74HC_HCT4051.pdf`, `sn74lvc1g3157.pdf`, crystal/diode/switch/heatsink/wire PDFs

Why it matters: constant-current drive is load-bearing (thesis §4.3.3, O'Donoghue 2014 §II) —
temperature/inductance drift breaks κ calibration. Verify constant-current before any tracking test.
New FPGA DDS + driver work lives here; reference schematics stay in vendor.
