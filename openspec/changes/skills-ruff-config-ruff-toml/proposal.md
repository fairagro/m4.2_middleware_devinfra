## Why

Synced `issue-fixer` / `review-fixer` skills tell agents to run Ruff with `--config pyproject.toml`, but product repos
(and Devinfra) use workspace-root `ruff.toml` without `[tool.ruff]` in `pyproject.toml`. That breaks or misconfigures
Ruff in product checkouts ([#91](https://github.com/fairagro/m4.2_middleware_devinfra/issues/91); surfaced on API PR
#391).

## What Changes

- Point skill Ruff guidance at `--config ruff.toml` (format + check) in `issue-fixer` and `review-fixer`
- Spot-check: no remaining `--config pyproject.toml` for Ruff under `.agents/skills/`

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- (none — skill wording only; OpenSpec required because skill files are in scope; `skip_specs: true`)

## Impact

- `.agents/skills/issue-fixer/SKILL.md`, `.agents/skills/review-fixer/SKILL.md`
- Products pick up on next skill sync
