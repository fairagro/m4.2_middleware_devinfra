# Proposal

## Why

#347 Decision 4 schedules Renovate + a pin SoT on `m4.2_infrastructure` only when Slice 2 lands — not as a Slice-1
prerequisite. Slice 1 (#350) already ships the `infrastructure` sync target and foundation allowlist, but
`renovate.json`, the Renovate workflow, and `versions.env` remain **python-product-only**, and push sync still skips
Infra by default until bot access exists. Infra still uses Dependabot (devcontainers) plus Dockerfile `ARG` pins, so
fleet CLI pins and Renovate cannot converge without a **pin-file split** and an Infra-reachable Renovate sync path.

## What Changes

- Split toolchain pins into a **foundation-eligible** file and a **python-product** file (C2), with product loaders
  composing both; Infra syncs only the foundation pin file
- Move shared Renovate config + workflow (and Renovate docs) onto a profile the `infrastructure` target already uses
  (`foundation`), so Sync can deliver them without dragging `.devcontainer/**` or python-product hooks
- Document the ops **checklist** to extend `DEVINFRA_BOT_TOKEN` PAT access to Infra, set the secret on Infra, unskip
  live Infra sync when ready, and comment Infra#80 — no automated PAT/secret mutation in-repo
- Document a **Dependabot wind-down plan** for Infra (keep alerts; remove/avoid Dependabot version-update PRs once
  Renovate is green) — implementation of deleting Infra’s `dependabot.yml` stays Infra-local / follow-up
- Update sync / Renovate / pin-ownership docs and profile tests so “Renovate/`versions.env` deferred to #354” is no
  longer the contract
- Keep `skip_infrastructure` default **true** until operators complete the checklist (dispatch dry-run/unskip remains)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `synced-consumer-paths`: Foundation allowlist gains Renovate artifacts, Renovate docs, and the foundation pin file;
  stop forbidding Renovate / foundation pins on Infra; keep full `versions.env` / `.python-version` / Dev Container on
  python-product only
- `product-repo-sync`: Infra effective allow may include Renovate + foundation pins; docs replace “until #354” with
  Slice-2 adoption + bot checklist; orphan/delete rules unchanged
- `shared-renovate`: Config/docs cover Infra as a fourth consumer; regex managers handle the split pin files; bot-token
  docs list Infra; Dependabot wind-down plan for Infra; unused managers stay harmless when product-only files are absent
- `shared-devcontainer-base`: Product Dev Container / `load-versions-env` contract sources foundation + product pin
  files (Compose/`versions.env` happy path stays one logical pin SoT for products)

## Impact

- `docs/synced-paths.yaml`, `docs/sync.md`, `docs/renovate.md`, `docs/devcontainer.md` (pin buckets)
- New `versions.foundation.env` (name finalized in design) + trimmed/`composed` `versions.env`;
  `scripts/load-versions-env.sh` and pin-reading install helpers (`install-gitleaks.sh`, helm lint pin lookup, …)
- `renovate.json` customManagers / packageRules for both pin files; product skip-list paths updated
- Sync profile tests (`scripts/tests/test_sync_products_profiles.py`)
- Operator checklist (PAT, Infra secret, Infra#80) — out-of-band; not CI-enforced
- Infra repo adoption via Sync after token; Dependabot file removal not in this Devinfra PR
