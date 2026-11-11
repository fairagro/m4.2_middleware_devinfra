## Why

Infra deferred local actionlint ([infra#73](https://github.com/fairagro/m4.2_infrastructure/issues/73)) until the
gitops/infra profile landed. Actionlint belongs in the **foundation** quality set for every repo with GitHub Actions
workflows. #351 split the pre-commit roots; this change adds a single pin shared by Dev Container, commit-stage hooks,
and blocking reusable CI.

## What Changes

- Pin `ACTIONLINT_VERSION` in `versions.env` (Renovate-managed) — one SoT for local and GitHub Actions
- Add `scripts/install-actionlint.sh` (gitleaks-style) and install the pin in the product Dev Container image
- Add foundation `actionlint` hooks to **both** `.pre-commit-config.yaml` and `.pre-commit-config.infrastructure.yaml`
  (`language: system`, fail closed when the binary/pin is missing)
- Run actionlint in reusable code-quality CI after installing the same pin (**blocking**)
- Allowlist the install script on `foundation`; document in `docs/quality.md` / `docs/ci.md` / Dev Container docs
- Note Infra adoption path (infra#80): hook arrives via Infra pre-commit root; `versions.env` pin follows #354

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: foundation actionlint hook on both pre-commit roots; pin + install helper contract
- `shared-devcontainer-base`: image installs pinned actionlint from `versions.env`
- `synced-consumer-paths`: allowlist `scripts/install-actionlint.sh` on `foundation`
- `reusable-ci-workflows`: reusable code-quality installs the pin and runs actionlint (blocking)

## Impact

- Product + Infra pre-commit configs; Dev Container Dockerfile/compose args; `versions.env`; `renovate.json`
- `scripts/install-actionlint.sh`; `.github/workflows/reusable-code-quality.yml`
- Docs: quality/ci/devcontainer; short comment on infra#80 at apply time
- Out of scope: separate required-only-actionlint status check; moving `versions.env` onto Infra (#354)
