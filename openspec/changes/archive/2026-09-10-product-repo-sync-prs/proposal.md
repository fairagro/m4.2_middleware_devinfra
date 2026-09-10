# Product-repo sync PRs (issue #13)

## Why

Shared Devinfra content still reaches products via manual Wave adopt. Issue #13 needs automation: a change on Devinfra
`main` must be able to open reviewable sync PRs in the three product repos, copying only allowlisted paths — never
product `middleware/`, never OpenSpec specs (product or Devinfra), never reusable CI workflow YAML (products keep
`uses:`).

## What Changes

- Add sync automation (**A1**): workflow + script that pushes allowlisted paths into `m4.2_advanced_middleware_api`,
  `m4.2_sql_to_arc`, and `m4.2_middleware_harvester` as PRs.
- **Single path list (**B1′**)**: `docs/synced-paths.yaml` remains the only human/machine SoT for what is synced and
  what `/review-fixer` treats as read-only in consumers. Expand vague rows into concrete paths; sync tooling reads this
  file (no second hand-maintained manifest).
- **Triggers (**C3**)**: on push to `main` (when relevant), open live sync PRs; `workflow_dispatch` with optional
  dry-run/skip flags for override.
- **Auth (**D**)**: document one bot token (Actions secret) with rights for Renovate and sync (Contents + PRs on
  targets); wire sync workflow to that secret (align Renovate docs/secret naming as needed).
- Hard excludes (**F**): never sync `middleware/`, `openspec/specs/**`, `openspec/changes/**`, product overlays, or
  `reusable-*.yml` workflow files.
- Docs: how sync works, dry-run/skip, token setup, relation to Wave issues / #13.

## Capabilities

### New Capabilities

- `product-repo-sync`: Automation and docs to open sync PRs from Devinfra into the three product repos using the
  synced-paths allowlist.

### Modified Capabilities

- `synced-consumer-paths`: Allowlist is the **sole** sync path SoT (machine-readable for automation); must list concrete
  shared paths (including quality/DC/hooks fragments); must state hard excludes for OpenSpec specs trees and product
  overlays.
- `shared-renovate`: Token docs MUST allow a shared bot secret used by Renovate and sync (same PAT/App, documented
  scopes).

## Impact

- New workflow (e.g. `.github/workflows/sync-products.yml`) + sync script under `scripts/`
- `docs/synced-paths.yaml` expanded; `docs/sync.md` (or similar); README / ci links
- Renovate docs/secret naming alignment
- OpenSpec specs above; product repos only receive PRs (no product commits in this change)
- Ops: create/configure bot token secret on Devinfra
