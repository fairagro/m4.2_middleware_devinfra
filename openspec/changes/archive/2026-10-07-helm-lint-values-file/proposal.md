## Why

Feature-PR Helm template smoke uses bare chart defaults. Charts that need CI overlays (or leave deploy-time secrets
unset) fail `helm template` even when `helm lint` passes. The reusable has no `-f` input, and the synced local
`run-helm-lint.sh` hook has the same bare-chart gap — so Feature-PR CI and commit-stage quality can diverge once CI
gains an overlay.

## What Changes

- Add optional `values_file` to `reusable-helm-lint.yml` (path relative to caller checkout): when set, assert the file
  exists and pass `-f` to `helm lint` and `helm template`; when empty, keep bare-chart behaviour.
- Teach `scripts/run-helm-lint.sh` the same overlay via optional env `HELM_VALUES_FILE` (same semantics: empty → bare;
  set → require file + `-f` on lint and template).
- Document CI input and local env in `docs/ci.md` / `docs/quality.md`.
- Extend `reusable-ci-workflows` and `shared-quality-tooling` requirements for overlay parity.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: Optional `values_file` on Feature-PR Helm lint reusable.
- `shared-quality-tooling`: Optional `HELM_VALUES_FILE` for commit-stage Helm lint / template smoke.

## Impact

- Devinfra: workflow, `scripts/run-helm-lint.sh`, docs, OpenSpec deltas above.
- Products: may pass `values_file` on Feature-PR callers and/or export `HELM_VALUES_FILE` locally; no required product
  change if bare chart already works.
- Multi-file value lists remain out of scope.
