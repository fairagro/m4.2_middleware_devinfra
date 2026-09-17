## Why

Agents lack a reusable first-party **code-review** skill, so ad-hoc branch/PR reviews drift. Discussion
[#140](https://github.com/fairagro/m4.2_middleware_devinfra/issues/140) locked the contract; Feature
[#171](https://github.com/fairagro/m4.2_middleware_devinfra/issues/171) implements it as synced fleet plumbing.

## What Changes

- Add synced skill `.agents/skills/code-review/` plus thin Cursor command and Copilot prompt
- Add short `docs/code-review.md` and allowlist entries so products receive the skill via sync
- Prefer a formal GitHub Pull Request Review via `gh pr review --comment` when a PR is known (cheap CLI path); otherwise
  write the report under `/tmp`. Fall back to a PR conversation comment only if posting a review fails
- Put recurring skill plumbing in `scripts/ai` (`m42-ai`): shape local/PR diff context, write the report file, publish
  the review/comment — judgment stays in the skill, not in the CLI
- Hard anti-duplication vs quality toolchain (Ruff/mypy/pylint/Bandit/markdownlint/Prettier/ggshield/CodeQL/Trivy, and
  vulture/import-linter once landed — [#172](https://github.com/fairagro/m4.2_middleware_devinfra/issues/172) /
  [#173](https://github.com/fairagro/m4.2_middleware_devinfra/issues/173)); skill is complementary to `/review-fixer`

## Capabilities

### New Capabilities

- `code-review`: Canonical `/code-review` skill (local `base...HEAD` and PR review), thin entrypoints, docs, and publish
  behavior (formal PR Review when cheap; `/tmp` report otherwise)

### Modified Capabilities

- `agent-ai-gh`: Add `m42-ai` commands for code-review recurring steps (diff context, report write, publish); document
  portable invoke from the new skill

## Impact

- Closes [#171](https://github.com/fairagro/m4.2_middleware_devinfra/issues/171); implements
  [#140](https://github.com/fairagro/m4.2_middleware_devinfra/issues/140) decision
- Touches `.agents/skills/`, `.cursor/commands/`, `.github/prompts/`, `docs/`, `docs/synced-paths.yaml`, `scripts/ai/`,
  README skill index as needed
- Does **not** land vulture/import-linter (separate Features); skill only names them as toolchain-owned when present
