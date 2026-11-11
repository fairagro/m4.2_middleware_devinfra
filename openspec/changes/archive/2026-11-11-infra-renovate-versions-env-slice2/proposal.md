# Proposal

## Why

#347 Decision 4 schedules Renovate + a pin SoT on `m4.2_infrastructure` only when Slice 2 lands — not as a Slice-1
prerequisite. Slice 1 (#350) already ships the `infrastructure` sync target and foundation allowlist, but
`renovate.json`, the Renovate workflow, and `versions.env` remain **python-product-only**, and push sync still skips
Infra by default until bot access exists. Infra still uses Dependabot (devcontainers) plus Dockerfile `ARG` pins. Pins
alone do not install tools, so a **single** `versions.env` on foundation is enough for Infra (unused keys are no-ops
until a Dockerfile or hook reads them).

## What Changes

- Move shared Renovate config + workflow, Renovate docs, and **`versions.env`** onto `foundation` so Sync delivers them
  to Infra without dragging `.devcontainer/**`, `.python-version`, or python-product hooks (C1 — one pin file)
- Keep pin-ownership **buckets as documentation** (shared vs python-product vs Infra-owned); do **not** split the pin
  file
- Document the ops **checklist** to extend `DEVINFRA_BOT_TOKEN` PAT access to Infra, set the secret on Infra, unskip
  live Infra sync when ready, and comment Infra#80 — no automated PAT/secret mutation in-repo
- Document a **Dependabot wind-down plan** for Infra (keep alerts; remove/avoid Dependabot version-update PRs once
  Renovate is green) — deleting Infra’s `dependabot.yml` stays Infra-local / follow-up
- Update sync / Renovate / pin-ownership docs and profile tests so “Renovate/`versions.env` deferred to #354” is no
  longer the contract
- Keep `skip_infrastructure` default **true** until operators complete the checklist (dispatch dry-run/unskip remains)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `synced-consumer-paths`: Foundation allowlist gains Renovate artifacts, Renovate docs, and `versions.env`; keep
  `.python-version` / Dev Container on python-product only
- `product-repo-sync`: Infra effective allow may include Renovate + `versions.env`; docs replace “until #354” with
  Slice-2 adoption + bot checklist; orphan/delete rules unchanged
- `shared-renovate`: Config/docs cover Infra as a fourth consumer; bot-token docs list Infra; Dependabot wind-down plan
  for Infra; synced-SoT skip includes Infra for `versions.env` + Renovate artifacts
- `shared-devcontainer-base`: Docs state Infra may sync `versions.env` via foundation without adopting the product Dev
  Container; pin buckets remain documentary (one pin file)

## Impact

- `docs/synced-paths.yaml`, `docs/sync.md`, `docs/renovate.md`, `docs/devcontainer.md` (pin buckets + checklist)
- `renovate.json` packageRules (Infra skip); profile tests
- Operator checklist (PAT, Infra secret, Infra#80) — out-of-band; not CI-enforced
- Infra repo adoption via Sync after token; Dependabot file removal not in this Devinfra PR
