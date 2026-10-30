# robot-arm/ — integration stub for the separate arm repo

The robot arm (Pico 2 firmware, motor config, mechanics) lives in a **separate
repo owned by the arm team** (Tristan + Joyal). This folder is the integration
layer: it pins the contract, holds the FPGA-side test harness, and documents the
handshake. It is **not** a second copy of the firmware.

**Arm repo URL:** `ARM_REPO_URL` — to be filled in when the arm team creates or
points the repo. Until then, the contract release and the ICD are the interface.

## What this repo provides

| Item | Where |
|---|---|
| Canonical contract + versioned releases | `../contract/`, GitHub Releases `contract-vX.Y.Z` |
| FPGA ↔ arm ICD | `../contract/icd/pico_link.md` |
| Follower requirements (RQ-M1…M17) | `../contract/requirements/manipulator.md` |
| Shared conformance vectors | `../contract/icd/pico_link/vectors/` |
| FPGA-side mock-Pico tests | `tests/` |
| Handshake templates | `templates/` |

## Handshake (5 steps, arm-team side)

1. **Create or point the arm repo.** Keep the Pico firmware, motor config and
   mechanics there. Do not fork this monorepo.
2. **Add a read-only token.** Create a fine-grained PAT scoped to
   `poisnoir/Capstone` with **Contents: Read** only. Store it in the arm repo as
   the secret `CONTRACT_READ_TOKEN`. (Fallback: a read-only deploy key on
   `Capstone` + `git sparse-checkout set contract`; no expiry.)
3. **Copy the templates** into the arm repo:
   - `templates/sync-contract.sh` → `capstone/tools/sync-contract.sh`
   - `templates/contract-sync.yml` → `arm-repo/.github/workflows/contract-sync.yml`
   - `templates/contract-check.yml` → `arm-repo/.github/workflows/contract-check.yml`
   - `templates/CONTRACT_VERSION.example` → `capstone/CONTRACT_VERSION`
4. **Run `contract-sync`** (Actions → Run workflow, version `latest`). It
   downloads the release zip + json, verifies every SHA-256, updates
   `capstone/contract/`, and opens a PR.
5. **Link the repo to the org Project** and fill in `ARM_REPO_URL` here with a
   PR. The first `contract-v1.0.0` release is the handshake.

## How updates arrive

- The monorepo publishes a release on every push to `main` that changes
  `contract/` (immutable `contract-vX.Y.Z`, rolling `contract-latest`).
- The arm repo pins a version in `capstone/CONTRACT_VERSION` and pulls it. A
  weekly schedule checks for a newer release and opens a PR.
- `contract-check` fails on every arm-repo push if `capstone/contract/` was
  edited locally or no longer matches `capstone/contract-release.json`.
- If the arm team prefers not to use a token, they can download the release zip
  manually from the `Capstone` Releases page (the repo is public) and extract it
  to `capstone/contract/`.

## Manual fallback

```bash
# in the arm repo; the Capstone repo is public
gh release download contract-v1.0.0 --repo poisnoir/Capstone \
  --pattern 'contract-v1.0.0.zip' --pattern 'contract-v1.0.0.json'
unzip -q contract-v1.0.0.zip -d capstone/contract
# verify with capstone/tools/sync-contract.sh --check after copying the json
```

## Ownership

- Arm repo: Tristan + Joyal.
- ICD + requirements: contract owner (integration) with the arm team.
- Contract release pipeline: integration.
