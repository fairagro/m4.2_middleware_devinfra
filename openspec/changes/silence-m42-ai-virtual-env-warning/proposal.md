## Why

Product Dev Containers set `VIRTUAL_ENV=/workspace/.venv` while agent skills invoke
`uv run --project scripts/ai m42-ai …`, which uses `scripts/ai/.venv`. uv correctly ignores the mismatched `VIRTUAL_ENV`
but prints a warning on every call, noise that clutters agent logs. We need one documented silent primary invoke without
`--active` or removing DC `VIRTUAL_ENV`.

## What Changes

- Add a thin synced `scripts/bin/m42-ai` wrapper that unsets `VIRTUAL_ENV` then runs
  `uv run --project scripts/ai m42-ai "$@"`.
- Allowlist the wrapper in `docs/synced-paths.yaml` with other `scripts/bin` helpers.
- Update synced skill Auth / command templates and `scripts/ai/README.md` so the primary silent form is `m42-ai …` when
  `scripts/bin` is on `PATH`, with portable fallback `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`.
- Keep Dev Container `VIRTUAL_ENV` and forbid documenting `uv run --active` for this CLI.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `agent-ai-gh`: Primary portable silent invoke for skills/README; wrapper as preferred PATH form.
- `issue-fixer`: Auth/command templates use silent primary invoke.
- `create-issue`: Preferred create path uses silent primary invoke.
- `review-fixer`: `review-open` start path uses silent primary invoke.
- `code-review`: Mechanical helper command form uses silent primary invoke.
- `personal-token-helpers`: Document `scripts/bin/m42-ai` alongside other PATH wrappers (unset `VIRTUAL_ENV` before
  product `--project` uv run).

## Impact

- New file: `scripts/bin/m42-ai` (synced).
- Docs/skills: Auth sections and example commands in four fixer skills + thin docs + README.
- Specs: deltas above; Dev Container `remoteEnv.VIRTUAL_ENV` unchanged (`shared-devcontainer-base`).
- No CLI Python package API change; wrapper is shell-only.
