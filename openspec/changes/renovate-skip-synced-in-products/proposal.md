# Proposal: renovate-skip-synced-in-products

## Why

Product Renovate runs (API / sql-to-arc / harvester) opened duplicate dependency PRs for Devinfra-owned pins that are
synced via `#13` (e.g. API [#384](https://github.com/fairagro/m4.2_advanced_middleware_api/pull/384) on `versions.env`
and [#385](https://github.com/fairagro/m4.2_advanced_middleware_api/pull/385) on `# syntax=docker/dockerfile`). Those
updates must land only in Devinfra, then propagate by sync — not as three parallel Renovate PRs.

## What Changes

- Shared `renovate.json`: in the three product repos, disable updates for synced SoT files (`versions.env`,
  `.python-version`, `docker/Dockerfile.product-app.base`, `.devcontainer/Dockerfile`, Renovate config/workflow) and for
  package `docker/dockerfile`.
- Document the split in `docs/renovate.md`.
- Extend `shared-renovate` main + delta specs accordingly.

## Capabilities

### Modified Capabilities

- `shared-renovate`: Product Renovate must skip Devinfra-synced dependency SoT; Devinfra keeps bumping those pins.

## Out of Scope

- Closing existing product Renovate PRs (operator action after sync).
- Changing sync allowlist or product-local pep621 / last-stage `FROM` update rules beyond the BuildKit frontend package.
- Restoring leading `v` on Renovate write-back (separate Devinfra PR if still open).
