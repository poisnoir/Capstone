# Contract — single source of truth

This folder is the **only shared write surface** in the repo. It freezes the
interfaces every team builds against. Team folders are owned by their team; this
folder is owned by the integration team and reviewed by the interface owners.

## Read order

1. `system_contract.md` — SC-01…SC-10, decisions D1–D4.
2. `decisions_log.md` — every locked decision, with date, justification, status
   and source.
3. The ICD for your interface (`icd/pico_link.md` for the robot arm).
4. `requirements/manipulator.md` — RQ-M1…M17, the follower requirements.

Status tags used everywhere:

- `LOCKED` — source-backed; do not reopen without a written deviation.
- `PROPOSED` — needs approval or a test.
- `OPEN` — team decision required.
- `TBD` — blocked by a missing input.

## Versioning

- `VERSION` is semver: **MAJOR** = breaking interface change, **MINOR** =
  additive change, **PATCH** = clarification/typo.
- `CHANGELOG.md` records every release and which consumers must act.
- A release is tagged `contract-vX.Y.Z`. CI publishes
  `contract-vX.Y.Z.zip` + `contract-vX.Y.Z.json` (version, commit, tree hash,
  per-file hashes) and updates the rolling `contract-latest` release.
- The robot-arm repo pins a version and pulls the release; see
  `../robot-arm/README.md`.

## Change process

1. Open a `contract-change` issue (affected SC/decision ID, old text, new text,
   reason, impact, gates to re-run).
2. Open a PR that changes this folder **and**:
   - bumps `VERSION`,
   - adds a `CHANGELOG.md` entry,
   - adds a `decisions_log.md` row (or updates the existing row's status),
   - puts `Contract-Change: yes` in the PR body.
3. Two approvals: the interface owner on each side + the contract owner.
4. Merge. CI tags and publishes the release.
5. Sync the arm repo (run `contract-sync` or open the sync PR), update the
   pinned issue, and tell the affected teams which gates to re-run.

The `contract-guard` Action fails a PR that changes `contract/` without the
version/changelog/decision updates.

## Current consumers

| Consumer | What it pins | How it syncs |
|---|---|---|
| `Capstone` monorepo (fpga, hardware, software) | `main` | same repo; no copy |
| Robot-arm repo | `contract-vX.Y.Z` | `contract-sync` workflow, release zip + json |

## Ownership

- Contract owner: integration lead (SC-10 in `system_contract.md`).
- Interface owners: the named owner on each side of an ICD (see the ICD header).
- Do not edit this folder in a team PR without the contract-change process.
