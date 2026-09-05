# Shared quality scripts — Tasks

## 1. Config files

- [x] 1.1 Add root `.bandit` suitable for `bandit -c` (align with API product pattern)
- [x] 1.2 Confirm `.markdownlint.json` / `.markdownlintignore` / `.markdownlint-cli2.jsonc` still match vendor excludes;
      adjust only if needed for pre-commit markdownlint

## 2. Scripts

- [x] 2.1 Add `scripts/quality-check.sh` (commit-stage `pre-commit` check only; no pre-push stage)
- [x] 2.2 Add `scripts/quality-fix.sh` (commit-stage fix mode only; no pre-push stage)
- [x] 2.3 Add templated `scripts/run-container-structure-test.sh` (build image → container-structure-test; overridable
      Dockerfile / tag / test paths)
- [x] 2.4 Make scripts executable and safe under `set -euo pipefail` (or equivalent)

## 3. Pre-commit skeleton

- [x] 3.1 Add `.pre-commit-config.yaml` commit-stage hooks: trailing-whitespace / YAML-TOML hygiene, ggshield, ruff,
      mypy, bandit, pylint, markdownlint (API-aligned)
- [x] 3.2 Add pre-push stage: pytest + CST entry calling `scripts/run-container-structure-test.sh`
- [x] 3.3 Target Python tools at `middleware/`; exclude pinned vendor skills (`gh`, `docker`, `hadolint`, `uv`,
      `scan-secrets` when present)

## 4. Docs

- [x] 4.1 Document sync + `pre-commit install --hook-type pre-commit` in README and/or `docs/` (postCreate / #10)
- [x] 4.2 Explicitly defer pre-push git-hook install to #9; document CST runner parameters for consumers

## 5. Verify

- [x] 5.1 Smoke: scripts are invokable; commit-stage config parses (`pre-commit validate-config` or equivalent)
- [x] 5.2 Mark OpenSpec tasks complete only after files match `shared-quality-tooling` requirements
