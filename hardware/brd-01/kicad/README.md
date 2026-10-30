# BRD-01 KiCad project

The KiCad project lives here:

```
kicad/
├─ brd-01.kicad_pro
├─ brd-01.kicad_sch
├─ brd-01.kicad_pcb
├─ sym-lib-table
└─ fp-lib-table
```

Rules:

- KiCad files are text (S-expression); commit them.
- Do not commit `*-backups/`, `fp-info-cache`, `*.kicad_prl`, `*.bak`
  (gitignored).
- Run ERC/DRC before a fab release; put the released package in `../fab/`.
- The schematic is not frozen until the part checks in
  `contract/decisions_log.md` are closed (35T→50T pin compatibility, HR banks,
  shield can, connectors).
