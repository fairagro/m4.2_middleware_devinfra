# Extract issue-fixer — Proposal

## Why

Wave A needs a shared `/issue-fixer` so product repos triage a GitHub issue, pause for user decisions on
Feature/Refactoring, open a draft PR from an empty bootstrap commit, and implement locally without auto-committing
fixes. Issue [#14](https://github.com/fairagro/m4.2_middleware_devinfra/issues/14) is done;
[#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15) is unblocked.

## What Changes

- Add `.agents/skills/issue-fixer/SKILL.md` from the API, rewritten for Devinfra Auth and explore lock-ins (A–G)
- Add `.cursor/commands/issue-fixer.md` and `.github/prompts/issue-fixer.prompt.md` (empty-head bootstrap push allowed;
  fix commits not)
- Document workflow in skill + thin `docs/issue-fixer.md`; add `docs/review-fixer.md` so all three skills share the same
  docs pattern
- Deferred issues only via `/create-issue` (no parallel inline template), with a clear **relation**: GitHub native
  **sub-issue** when splitting a parent’s acceptance criteria; **linked** issue when the work is a distinct follow-up
  problem
- Amend create-issue for `relation` / `--parent`; amend review-fixer follow-ups for the same rule
- Out of scope: #16 CLI (`issue-start`), product-repo sync PRs, vendor skills (#6)

## Capabilities

### New Capabilities

- `issue-fixer`: Canonical `/issue-fixer` skill plus Cursor command, Copilot prompt, and docs that triage issues,
  explore Feature/Refactoring before GitHub writes, open a draft PR from one empty bootstrap commit, implement locally
  without fix commits/pushes, and split via create-issue as native sub-issues of the parent

### Modified Capabilities

- `create-issue`: Accept invocation from `/issue-fixer` and apply caller `relation` (`sub-of #<n>` →
  `gh issue create --parent`; `linked` → body Links only); document handoff and relation rule in skill/docs
- `review-fixer`: Require thin `docs/review-fixer.md` and README parity; follow-ups use create-issue with **linked** by
  default, **sub-of** only when the deferred item is remaining acceptance criteria of a PR `Fixes #<n>` issue

## Impact

- Closes the Fixer gap after `/review-fixer` and `/create-issue`; consumers sync later
- Aligns #15 with #16’s planned `issue-start` (empty commit + draft PR)
- Relies on existing personal-token helpers, create-issue, and `gh` parent/sub-issue flags
- Done in this repo when artifacts + docs are present and content-reviewed (no product smoke required here)
