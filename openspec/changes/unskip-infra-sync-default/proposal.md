# Proposal

## Why

Slice-2 Infra Renovate/sync prerequisites are done (first live sync, Renovate green, Dependabot version updates wound
down). Operators still must pass `skip_infrastructure=false` on every live dispatch, and **push-to-main** hard-skips
Infra. [#388](https://github.com/fairagro/m4.2_middleware_devinfra/issues/388) flips the default so Infra is included
like the python-product targets, while keeping an explicit skip for ops emergencies.

## What Changes

- `.github/workflows/sync-products.yml`: stop unconditional `--skip-infrastructure` on push; set dispatch
  `skip_infrastructure` default to **false** (keep the input so ops can skip)
- Docs (`docs/sync.md`, `docs/renovate.md`, allowlist comment in `docs/synced-paths.yaml`): Infra is no longer “skipped
  until checklist”; document how to skip when needed
- OpenSpec `product-repo-sync`: Infra included by default on push and dispatch; skip remains available

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `product-repo-sync`: default-include `infrastructure` on push and dispatch; `skip_infrastructure` remains for
  emergencies; docs no longer require checklist-gated default skip

## Impact

Next allowlist-touching `main` push (and live dispatch without skip) opens/updates Infra sync PRs when foundation/gitops
paths differ. Ops can still set `skip_infrastructure=true` on dispatch.
