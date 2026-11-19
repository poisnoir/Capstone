# BRD-01 KiCad project

Open [brd-01.kicad_pro](brd-01.kicad_pro) in KiCad **10.0.8** with the
official 10.0.8 symbol and footprint libraries installed. The root schematic
retains the power, driver, FPGA, receiver and connector sheets from `ca3ad55`.
The sheets have no components or wires; the PCB has no outline, layout, or
approved stackup settings. This is a capture scaffold, not a design release.

Use the [BOM-to-CAD ledger](bom-to-cad.md) to add verified parts to the
appropriate sheet. Where the ledger specifies a footprint different from the
symbol default (including empty defaults), assign the listed footprint
explicitly. Use the BOM's actual MPN as the part value, not the name of a
generic symbol. Do not place procurement spares or promote alternates.

The project tables resolve `accubot` relative to `${KIPRJMOD}` at
[the shared hardware library](../../kicad/lib/). No global `accubot` table,
plugin, 3D model, or external CAD download is needed. To add more selected
parts in one batch, first check the official libraries against manufacturer
pin tables and package drawings, then curate only missing or incorrect
definitions directly in the shared library and update the ledger. Do not
commit downloaded libraries, datasheets, or per-part import projects.

From the repository root:

```bash
kicad-cli --version
kicad-cli sch erc --exit-code-violations -o /tmp/opencode/brd01-setup-erc.rpt hardware/brd-01/kicad/brd-01.kicad_sch
kicad-cli pcb drc --exit-code-violations -o /tmp/opencode/brd01-setup-drc.rpt hardware/brd-01/kicad/brd-01.kicad_pcb
mkdir -p /tmp/opencode/brd01-symbol-svg
kicad-cli sym export svg --output /tmp/opencode/brd01-symbol-svg hardware/kicad/lib/accubot.kicad_sym
```

Empty-sheet ERC checks hierarchy loading, not component connectivity. The
blank PCB reports `invalid_outline` until layout adds a real outline. Do not
silence that check or treat empty-sheet ERC as a release gate. Put only the
released fabrication package in [fab](../fab/).

Setup verification also used a disposable project at the same relative paths
with only the standard global KiCad tables. All 19 units of the 15 curated
symbols loaded; removing the project symbol table produced 19 library errors.
Numbered symbol pins matched numbered footprint pads for the 8 official and
15 curated table pairings, including the JST pen header, and for the separate
ST TVS mapping. The follow-up ST and JST checks also verified pad geometry.

Two disposable boards with outlines reported zero DRC violations: one with
`accubot:RECOM_RV-1515D_DIP24`, and one with `accubot:ST_SMBJ_DO-214AA_DS1283`
and the official JST pen header. These smoke checks verify library use, not
BRD-01 circuit capture, layout readiness, or pen harness qualification.
