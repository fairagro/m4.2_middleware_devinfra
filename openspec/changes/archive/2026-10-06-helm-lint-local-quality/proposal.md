## Why

Feature-PR CI already runs `helm lint` via `reusable-helm-lint.yml`, but local commit-stage quality does not. Chart
errors can be committed and only fail on the Feature-PR job. Local lint belongs in synced Devinfra quality so every
product gets the same gate after sync.

## What Changes

- Add a shared runner (`scripts/run-helm-lint.sh`) that discovers product chart roots (`helmchart/*/Chart.yaml` and
  `helm/*/Chart.yaml`), no-ops when none exist, and otherwise runs `helm lint` plus the same default-values
  `helm template` smoke as the Feature-PR reusable.
- Wire that runner as a commit-stage local pre-commit hook so `./scripts/quality-check.sh` and git commit both run it.
- Keep `check-yaml` template excludes; do not treat YAML syntax checks as Helm validation.
- Document local vs Feature-PR reusable in `docs/quality.md` (and a pointer in `docs/ci.md` if needed).

## Capabilities

### New Capabilities

<!-- none — extend shared quality tooling -->

### Modified Capabilities

- `shared-quality-tooling`: Require commit-stage Helm lint (with no-op when no charts) using Helm on PATH (Dev Container
  pin from `versions.env`).

## Impact

- Synced: `.pre-commit-config.yaml`, `scripts/run-helm-lint.sh` (add to `docs/synced-paths.yaml`), `docs/quality.md`
  (optional `docs/ci.md`).
- Products pick up the hook on the next sync; no product fork of pre-commit YAML.
- Devinfra itself has no chart → hook is a no-op.
- Host checkouts with charts still need Helm on PATH (same pin as `HELM_VERSION`); Dev Container remains the supported
  environment.
