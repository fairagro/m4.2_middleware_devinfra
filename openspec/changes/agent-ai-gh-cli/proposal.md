## Why

Agent slash commands spend context on deterministic GitHub/git plumbing. Skills need a small CLI so models keep judgment
while fetch/filter/post/create/start become JSON in/out. Separately, `/issue-fixer` must always plan via `/opsx-propose`
before branch/PR/implement — optional “spec-worthy” skips were wrong.

## What Changes

- Add `scripts/ai/` Python package (`m42-ai`) run with `uv`: `review-open`, `review-reply`, `review-resolve`,
  `issue-create`, `issue-start`
- Auth only via PATH `gh` / `GH_TOKEN` (no second credential model)
- Unit-test JSON shaping with fixtures (no live GitHub in CI)
- Wire `/review-fixer`, `/create-issue`, `/issue-fixer` to invoke the CLI first
- **Require** `/opsx-propose` on every implementable `/issue-fixer` run (before branch/PR/implement)
- Land canonical `issue-fixer` main capability (missing from `openspec/specs/` after extraction)

## Capabilities

### New Capabilities

- `agent-ai-gh`: Deterministic GitHub/git plumbing CLI under `scripts/ai/` for agent skills
- `issue-fixer`: Canonical `/issue-fixer` skill contract including mandatory OpenSpec propose and CLI bootstrap

### Modified Capabilities

- `review-fixer`: Fetch open work via `m42-ai review-open`; replies/resolves via CLI
- `create-issue`: Prefer `m42-ai issue-create` for typed/labeled creates

## Impact

- New path: `scripts/ai/` (+ `uv` project); skills/docs/README
- Consumers sync skills + `scripts/ai/` in a later wave
- Does not encode AI review policy as a Python decision tree
