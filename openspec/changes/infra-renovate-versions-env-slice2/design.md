# Design

## Context

See proposal.md — Why. Slice 1 already profiles sync; Renovate + `versions.env` still sit on `python-product` only.
`load-versions-env.sh` and most install helpers assume a single repo-root `versions.env`. Compose uses
`.devcontainer/.env` → `versions.env`. Shared `renovate.json` already states unused managers must be harmless when files
are absent — that property is what lets one config serve Infra after the pin split.

## Goals / Non-Goals

**Goals:**

- Land a durable **two-file pin SoT** aligned with pin-ownership buckets (foundation-eligible vs python-product)
- Deliver Renovate config/workflow + foundation pins to Infra via **Sync** (foundation profile)
- Keep product Dev Container rebuild happy path: one composed pin load, no hand-edits after sync
- Document operator checklist (PAT → Infra secret → unskip → Infra#80) and Infra Dependabot wind-down **plan**

**Non-Goals:**

- Granting the PAT or writing the Infra Actions secret from CI/agent
- Deleting Infra’s `.github/dependabot.yml` in this repo
- Migrating Infra Dockerfiles from `ARG` pins onto the foundation pin file
- Syncing product `.devcontainer/**`, python-product pre-commit, or full `versions.env` to Infra
- Flipping `skip_infrastructure` default to false before the checklist is done
- Adding Infra-owned pins (argocd / kind / ct) into the foundation file

## Decisions

### D1 — File names and pin membership

- **`versions.foundation.env`**: foundation-eligible pins synced on `foundation` — at least kubectl, Helm, minikube,
  sops, age, yq, xq, yamlfmt, hadolint, starship, gitleaks, Node/npm, OpenSpec, Prettier, markdownlint-cli2 (keys that
  already exist today under those buckets).
- **`versions.env`**: python-product-only pins — Dev Container base image, Python/uv, product-app
  Alpine/pip/pyinstaller, CST, Trivy, Renovate CLI, git-cliff (and `.python-version` remains product-only).
- **Why not keep one file and sync a filtered copy?** Dual SoT / generated subset drifts. Two authored files match the
  #347 / #352 “file split” intent.
- **Why not put Renovate CLI / Trivy on foundation?** They are product-DC / product-CI tools per current pin-ownership
  docs; Infra adoption does not need the npm Renovate CLI pin to run the GitHub Action.

### D2 — Product composition

- `scripts/load-versions-env.sh` sources **foundation first, then `versions.env`** (later file wins on duplicate keys —
  there MUST be no intentional duplicates across files).
- Product Compose / build-arg injection lists **both** files (replace single-symlink-only assumption). Keep or adjust
  `.devcontainer/.env` only if still required for a documented single-file consumer; prefer explicit dual `env_file`.
- Install helpers that need a foundation pin (e.g. gitleaks, helm pin lookup) MUST read `versions.foundation.env` (with
  a clear error if missing). Product-only helpers keep reading `versions.env`.

### D3 — Sync allowlist

- Move to **`foundation`**: `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`,
  `versions.foundation.env`.
- Keep on **`python-product`**: `versions.env`, `.python-version`, Dev Container blob, CodeQL workflow, etc.
- Infra effective allow therefore gains Renovate + foundation pins without `python-product`.
- Profile tests assert the new membership and that full `versions.env` is still absent from Infra.

### D4 — Renovate behavior with two pin files

- Extend regex `customManagers` / `packageRules` so foundation pins are managed from `versions.foundation.env` and
  product pins from `versions.env` (no duplicate key managed in both).
- **Synced SoT skip** applies in products **and** Infra for Devinfra-owned synced paths: at least
  `versions.foundation.env`, `renovate.json`, `.github/workflows/renovate.yml` (products also keep skipping
  `versions.env`, `.python-version`, Dev Container Dockerfile, CodeQL, product-app base). Pin bumps stay in Devinfra;
  Sync propagates.
- Infra-local managers (Dockerfile ARGs, github-actions in Infra workflows, etc.) remain enabled.

### D5 — Ops checklist vs default skip

- Document checklist in `docs/renovate.md` + `docs/sync.md`: (1) extend PAT repo access to
  `fairagro/m4.2_infrastructure`, (2) set `DEVINFRA_BOT_TOKEN` on Infra, (3) dispatch dry-run then unskip live Infra
  sync / optionally flip default later, (4) comment Infra#80.
- Keep push `skip_infrastructure` **default true** in this change so merge does not fail live sync before ops.

### D6 — Dependabot wind-down = docs plan only

- Document: after first green Renovate run on Infra, remove Dependabot **version updates** (`dependabot.yml` ecosystems
  that duplicate Renovate); keep Dependabot **alerts**; prefer Renovate for security remediation PRs.
- Do not edit the Infra repo from this PR.

## Risks / Trade-offs

- [Product rebuild breaks if only one pin file is present] → Fail closed in `load-versions-env.sh` with explicit missing
  file errors; sync both files to python-product targets (foundation ∪ python-product).
- [Renovate double-manages a pin after a mis-split] → Task: assert no key appears in both files; packageRules by
  filename.
- [Infra Renovate opens noisy PRs for missing product files] → Rely on unused-manager harmlessness; validate with a
  dry-run note in tasks.
- [Operators unskip before PAT] → Keep default skip true; checklist ordering is PAT/secret before unskip.
- [Larger apply surface than C1] → Accepted by lock-in; keep Infra Dockerfile migration out.

## Migration Plan

1. Land split + loader/Compose/helper updates on Devinfra; Renovate config updated; allowlist moved; docs/checklist.
2. Sync to products (automatic on merge) — products receive `versions.foundation.env` + Renovate stays present via
   foundation.
3. Operators run checklist; dry-run Infra sync; live sync PR into Infra; enable Renovate workflow secret on Infra.
4. After Renovate green on Infra, Infra-local Dependabot wind-down (outside this PR).
5. Rollback: revert allowlist moves and restore single-file loaders if needed; leave Infra secret/PAT in place
   (harmless).

## Open Questions

- Exact Compose wiring for dual env files vs retaining `.devcontainer/.env` symlink for one of the two files — resolve
  at apply without changing the “both files must load” contract.
