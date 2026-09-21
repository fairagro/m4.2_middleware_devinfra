## MODIFIED Requirements

### Requirement: Ensure PR head before local fix edits

When a PR number or URL is known, `/review-fixer` MUST treat `m42-ai review-open` as the **first hard gate** before any
triage checklist, GitHub reply, or local `fix` edit. The skill MUST instruct agents to invoke
`uv run --project scripts/ai m42-ai review-open --pr <n>` (or equivalent) as the first action and MUST NOT proceed until
the command succeeds with `current_branch` matching `head_ref`.

When `review-open` fails closed (dirty tree on a different branch, checkout failure, or clear error JSON), the skill
MUST instruct agents to **stop immediately**, surface the CLI error to the user, and MUST NOT stash, force-checkout, or
otherwise improvise around the failure. The skill MUST NOT silently switch back to a previous branch after a failed or
empty open-work run.

Dirty working tree **on** the PR head MUST remain allowed (matching CLI). Paste-only triage without a PR MUST NOT
require checkout.

#### Scenario: PR-scoped run checks out via review-open first

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs starting with `uv run --project scripts/ai m42-ai review-open --pr <n>` as the first
  action
- **AND** triage and local `fix` file edits are deferred until that command has succeeded with the PR head checked out

#### Scenario: Checkout failure stops without improvisation

- **WHEN** `review-open` exits non-zero because the tree is dirty on a branch other than the PR head (or checkout fails)
- **THEN** the skill instructs stopping and showing the CLI error to the user
- **AND** it forbids stash/checkout workarounds and silent return to the previous branch
