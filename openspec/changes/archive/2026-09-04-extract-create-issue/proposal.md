# Extract create-issue — Proposal

## Why

Wave A needs a shared `/create-issue` creator so product repos classify GitHub issues (org issue type + triage labels)
without re-running review-fixer. Issue #5 is done; [#14](https://github.com/fairagro/m4.2_middleware_devinfra/issues/14)
is unblocked and blocks issue-fixer (#15).

## What Changes

- Add `.agents/skills/create-issue/SKILL.md` from the API (Variante B), with Devinfra Auth matching `/review-fixer`
  (wrappers + chat ask for `set-dev-tokens.sh`; never paste PATs)
- Add `.cursor/commands/create-issue.md` and `.github/prompts/create-issue.prompt.md`
- Document org issue types and triage label families in README and/or a short docs note; keep types as GitHub Issue
  Types (not `kind:*` labels)
- Skill MUST create-if-missing only allowlisted triage labels when attaching them (one-shot per repo, no separate
  bootstrap script)
- Align type list (include `Refactoring`) and clarify Task vs Refactoring; document issue cost values
  (`cheap|medium|expensive`) vs review-policy cost
- Out of scope: #15 issue-fixer, org Issue Type admin setup, product-repo sync PRs, label bootstrap scripts

## Capabilities

### New Capabilities

- `create-issue`: Canonical `/create-issue` skill plus Cursor command and Copilot prompt that create GitHub issues with
  one org issue type and triage labels, using shared `gh` auth

### Modified Capabilities

- (none)

## Impact

- Closes the Creator gap after `/review-fixer`; consumers sync artifacts later
- Relies on existing personal-token helpers and AI review policy vocabulary for severity/practicality/cost definitions
- Done in this repo when artifacts + docs are present and content-reviewed (no product smoke required here)
