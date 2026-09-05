# Shared quality scripts — Tasks

## 1. Config files

- [ ] 1.1 Add root `.bandit` suitable for `bandit -c` (align with API product pattern)
- [ ] 1.2 Confirm `.markdownlint.json` / `.markdownlintignore` / `.markdownlint-cli2.jsonc` still match vendor excludes;
      adjust only if needed for pre-commit markdownlint

## 2. Scripts

- [ ] 2.1 Add `scripts/quality-check.sh` (commit-stage `pre-commit` check only; no pre-push stage)
- [ ] 2.2 Add `scripts/quality-fix.sh` (commit-stage fix mode only; no pre-push stage)
- [ ] 2.3 Add templated `scripts/run-container-structure-test.sh` (build image → container-structure-test; overridable
      Dockerfile / tag / test paths)
- [ ] 2.4 Make scripts executable and safe under `set -euo pipefail` (or equivalent)

## 3. Pre-commit skeleton

- [ ] 3.1 Add `.pre-commit-config.yaml` commit-stage hooks: trailing-whitespace / YAML-TOML hygiene, ggshield, ruff,
      mypy, bandit, pylint, markdownlint (API-aligned)
- [ ] 3.2 Add pre-push stage: pytest + CST entry calling `scripts/run-container-structure-test.sh`
- [ ] 3.3 Target Python tools at `middleware/`; exclude `.agents/skills/gh/**` and `.agents/skills/scan-secrets/**`

## 4. Docs

- [ ] 4.1 Document sync + `pre-commit install --hook-type pre-commit` in README and/or `docs/` (postCreate / #10)
- [ ] 4.2 Explicitly defer pre-push git-hook install to #9; document CST runner parameters for consumers

## 5. Verify

- [ ] 5.1 Smoke: scripts are invokable; commit-stage config parses (`pre-commit validate-config` or equivalent)
- [ ] 5.2 Mark OpenSpec tasks complete only after files match `shared-quality-tooling` requirements
