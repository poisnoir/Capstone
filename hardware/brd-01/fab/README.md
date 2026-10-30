# BRD-01 fabrication outputs

Put only **released** fabrication packages here, one folder per revision:

```
fab/
└─ rev-a/
   ├─ brd-01-rev-a-gerbers.zip
   ├─ brd-01-rev-a-drill.zip
   ├─ brd-01-rev-a-bom.csv
   └─ brd-01-rev-a-README.md   # fab house, stackup, date, DRC result
```

Do not commit every intermediate plot. Gerbers and drill files are binary; keep
the zip small. The KiCad source is the source of truth; a fab package is a
release artifact.
