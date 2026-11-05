## Why

Fleet secret scanning today uses **ggshield**, which needs a GitGuardian API key and network access and is only wired as
a pre-commit hook (not in reusable CI). Middleware Discussion #340 locked **replace with gitleaks**: fully local MIT
scanner, no SaaS token, fits `versions.env` CLI pins, and can gate PRs in CI so skipped hooks cannot merge secrets.

## What Changes

- **BREAKING (products after sync):** Remove ggshield from the shared pre-commit skeleton and fleet Python quality pins;
  contributors no longer need `GITGUARDIAN_API_KEY` for the secret-scan hook.
- Add **gitleaks** as the fleet secret scanner: pin via `versions.env`, install for Dev Container / CI, commit-stage
  pre-commit hook, and a failing gate in `reusable-code-quality.yml`.
- Document allowlist (`.gitleaksignore` or equivalent), migration for product repos, and drop GitGuardian-only token
  docs where unused.
- Update quality / code-review specs and docs that name ggshield so anti-duplication and sync guidance point at
  gitleaks.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: Commit-stage secret scan MUST be gitleaks (not ggshield); pin/install via versions.env / CLI
  path rather than `quality-tools-pins.txt`; document allowlist and removal of GitGuardian API key requirement for that
  gate.
- `reusable-ci-workflows`: Reusable code-quality MUST run gitleaks (fail closed on findings) when `skip` is false.
- `code-review`: Anti-duplication list MUST name gitleaks instead of ggshield as the owned secret-scan surface.

## Impact

- `.pre-commit-config.yaml`, `scripts/quality-tools-pins.txt`, `pyproject.toml` / lock, `versions.env`, Dev Container
  install scripts, `scripts/dev-tokens.sh` / docs (`GITGUARDIAN_API_KEY`), `docs/quality.md`, `docs/ci.md`.
- `.github/workflows/reusable-code-quality.yml` (+ OpenSpec / sync notes for products).
- Product sync (#13): after merge, products drop ggshield pins and adopt gitleaks hook/CI; infra follow-up
  `m4.2_infrastructure#74` adopts the same pattern.
- Renovate: new `GITLEAKS_VERSION` regex pin; remove ggshield from pip_requirements surface.
