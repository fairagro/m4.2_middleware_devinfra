# Shared quality scripts — Proposal

## Why

Product repos already run commit-stage and pre-push quality via `pre-commit`, but the shared Devinfra tree does not yet
ship the scripts and skeleton consumers can sync. Issue #6 (vendor skills + lint excludes) is merged; #7 is the next
slice so consumers can adopt one commit-stage / pre-push pattern with only package-root and Docker CST param tweaks.

## What Changes

- Add `scripts/quality-check.sh` and `scripts/quality-fix.sh` that run **commit-stage** hooks only (not pre-push).
- Add shared `.pre-commit-config.yaml` skeleton: commit-stage checks (trailing-whitespace / YAML-TOML, ggshield, ruff,
  mypy, bandit, pylint, markdownlint) and **pre-push** stages for `pytest` plus container-structure-test via a shared
  runner script.
- Add templated `scripts/run-container-structure-test.sh` (build image → `container-structure-test`); product-local
  Dockerfile path, image tag, and test YAML stay as parameters / local overlays.
- Add `.bandit` (and keep / align existing `.markdownlint.json`, `.markdownlintignore`, `.markdownlint-cli2.jsonc`).
- Document install expectations: commit-stage hook via `pre-commit install --hook-type pre-commit` (usually postCreate /
  #10); pre-push git hook install remains #9.
- Vendor excludes for `.agents/skills/gh` and `scan-secrets`; package-root convention `middleware/` per
  `docs/conventions.md`.

## Capabilities

### New Capabilities

- `shared-quality-tooling`: Shared commit-stage / pre-push quality scripts, pre-commit skeleton, bandit config, and
  templated container-structure-test runner for sync into product repos.

### Modified Capabilities

- (none — path-conventions and vendor-agent-skills already allow quality tooling to target `middleware/` and vendor
  excludes; this change implements the tooling those docs anticipated)

## Impact

- New files under `scripts/`, root pre-commit / bandit configs; README / docs for install and sync.
- Consumers (`m4.2_advanced_middleware_api` as primary source of truth to align with) sync these files later; this
  Devinfra repo has no `middleware/` packages — Python hooks are for consumer layout.
- Does not install pre-push git hooks (#9) or Dev Container postCreate (#10).
