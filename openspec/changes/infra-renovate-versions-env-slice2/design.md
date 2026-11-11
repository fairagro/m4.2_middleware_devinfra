# Design

## Context

See proposal.md — Why. Slice 1 already profiles sync; Renovate + `versions.env` still sit on `python-product` only.
Compose already uses `.devcontainer/.env` → `../versions.env`. Pins are declarations only — syncing unused keys to Infra
does not install product toolchain binaries.

## Goals / Non-Goals

**Goals:**

- Deliver Renovate + one `versions.env` to Infra via **Sync** (`foundation` profile)
- Keep product Dev Container rebuild happy path unchanged (single pin file + existing symlink)
- Document operator checklist (PAT → Infra secret → unskip → Infra#80) and Infra Dependabot wind-down **plan**

**Non-Goals:**

- Splitting `versions.env` into multiple files
- Materializing Compose env from multiple SoT files
- Granting the PAT or writing the Infra Actions secret from CI/agent
- Deleting Infra’s `.github/dependabot.yml` in this repo
- Migrating Infra Dockerfiles from `ARG` pins onto `versions.env`
- Syncing product `.devcontainer/**` or `.python-version` to Infra
- Flipping `skip_infrastructure` default to false before the checklist is done

## Decisions

### D1 — One pin file (C1)

- Keep a single repo-root `versions.env` as the pin SoT for Devinfra, products, and Infra.
- Pin-ownership buckets (shared / python-product / Infra-owned) stay **documentation**; they do not require a file
  split.
- **Why not C2?** Compose interpolates one project `.env`; a split forced a materialize helper the fleet does not want.
  Unused pins on Infra are harmless.

### D2 — Sync allowlist

- Move to **`foundation`**: `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`, `versions.env`.
- Keep on **`python-product`**: `.python-version`, Dev Container blob, CodeQL, product quality surfaces.
- Infra effective allow therefore gains Renovate + `versions.env` without `python-product`.

### D3 — Renovate synced-SoT skip

- Products continue to skip Devinfra-owned paths including `versions.env` and Renovate artifacts.
- Infra also skips `versions.env` + Renovate artifacts (+ synced `package.json` / lock) so pin bumps stay in Devinfra;
  Sync propagates.
- Infra-local managers (Dockerfile ARGs, local workflows) remain enabled.

### D4 — Ops checklist vs default skip

- Document checklist in `docs/renovate.md` + `docs/sync.md`.
- Keep push `skip_infrastructure` **default true** in this change.

### D5 — Dependabot wind-down = docs plan only

- Document Infra wind-down after first green Renovate run; do not edit the Infra repo from this PR.

## Risks / Trade-offs

- [Infra checkout shows unused product pins] → Document no-op semantics; defer file split if noise becomes a real
  problem.
- [Operators unskip before PAT] → Keep default skip true; checklist ordering is PAT/secret before unskip.

## Migration Plan

1. Land allowlist + Renovate Infra skip + docs/checklist on Devinfra.
2. Sync to products (automatic) — `versions.env` / Renovate arrive via foundation.
3. Operators run checklist; dry-run then live Infra sync; enable Renovate secret on Infra.
4. After Renovate green on Infra, Infra-local Dependabot wind-down (outside this PR).

## Open Questions

- None for this pivot.
