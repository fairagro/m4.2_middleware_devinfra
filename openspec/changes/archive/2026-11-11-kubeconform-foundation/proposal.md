## Why

`helm lint` / `helm template` only prove charts render. **kubeconform** validates rendered manifests against Kubernetes
OpenAPI schemas. Infra wants that after its template matrix
([infra#75](https://github.com/fairagro/m4.2_infrastructure/issues/75)); #347 locked kubeconform as **foundation**
tooling (pin + runner) that consumers can adopt without forcing product `run-helm-lint` hooks to hard-fail on CRD-heavy
charts.

## What Changes

- Pin `KUBECONFORM_VERSION` in `versions.env` (Renovate-managed) — one SoT for Dev Container and consumer CI
- Add `scripts/install-kubeconform.sh` (gitleaks/actionlint-style) and install the pin in the product Dev Container
  image
- Add thin shared helper `scripts/run-kubeconform.sh` (file args and/or stdin; pass-through flags; no chart discovery /
  `helm template`)
- Allowlist install + runner under `foundation` in `docs/synced-paths.yaml`
- Short note in `docs/quality.md`: when to use vs `run-helm-lint.sh`; CRD schemas / `-ignore-missing-schemas` stay
  consumer policy
- Do **not** wire kubeconform into product pre-commit or `run-helm-lint.sh` by default

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: kubeconform pin + install helper + generic runner contract; docs vs helm-lint
- `shared-devcontainer-base`: image installs pinned kubeconform from `versions.env`
- `synced-consumer-paths`: allowlist `scripts/install-kubeconform.sh` and `scripts/run-kubeconform.sh` on `foundation`

## Impact

- `versions.env`; `renovate.json` customManager; Dev Container Dockerfile/compose args
- `scripts/install-kubeconform.sh`; `scripts/run-kubeconform.sh`; `docs/synced-paths.yaml`; `docs/quality.md` (+ brief
  Dev Container mention if needed)
- Out of scope: Infra fizz/draven template matrix (infra#75); fleet-default Argo CRD schema packs; live cluster /
  server-side dry-run; product helm-lint hard-fail on kubeconform
