# Proposal

## Why

#349 kept deprecated `helm/` and `helmchart/` chart-root discovery beside canonical `charts/`. Consumer renames are done
([#361](https://github.com/fairagro/m4.2_middleware_devinfra/issues/361) blockers closed); the dual window must end so
the fleet only discovers `charts/<chart>/`.

## What Changes

- `scripts/run-helm-lint.sh`: discover only `charts/*/Chart.yaml`
- Pre-commit (product + infra): helm-lint `files` and `check-yaml` excludes → `charts/` only
- `.vscode/settings.json`: drop legacy Helm template associations
- Docs (`quality.md`, `ci.md`, related): drop deprecation / dual-discovery language
- OpenSpec: `shared-quality-tooling`, `shared-devcontainer-base`, `reusable-ci-workflows` — charts-only contracts

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: charts-only Helm lint discovery, check-yaml excludes, docs
- `shared-devcontainer-base`: IDE associations charts-only
- `reusable-ci-workflows`: Feature-PR Helm lint docs charts-only (no legacy path filters)

## Impact

Synced pre-commit configs, `run-helm-lint.sh`, `.vscode/settings.json`, quality/ci docs; consumers already on `charts/`.
