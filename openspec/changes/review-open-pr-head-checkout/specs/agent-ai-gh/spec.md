## ADDED Requirements

### Requirement: review-open ensures PR head checkout

Before emitting open-work JSON, `review-open` MUST resolve the PR head ref name, ensure the local checkout is that
branch (fetch + checkout when needed), and include the checked-out branch name in the JSON (e.g. `head_ref` /
`current_branch`). When the working tree/index is dirty and the current branch is **not** the PR head, the CLI MUST
refuse with a clear error JSON and non-zero exit (matching `issue-branch` cleanliness intent for wrong-branch work).
Dirty state **on** the PR head MUST be allowed. When the head cannot be checked out, the CLI MUST fail closed with a
clear error JSON (no partial silent continue on another branch).

#### Scenario: Wrong-branch dirty refuses

- **WHEN** `review-open` runs and the working tree is dirty on a branch other than the PR head
- **THEN** the process exits non-zero with clear error JSON
- **AND** it does not change the current branch

#### Scenario: Checkout succeeds and JSON includes head

- **WHEN** `review-open` runs on a clean tree (or dirty tree already on the PR head) and the PR head is checkoutable
- **THEN** the local checkout is the PR head branch
- **AND** the emitted JSON includes that branch name
- **AND** open-work shaping still runs as before

## MODIFIED Requirements

### Requirement: review-open shapes open AI work

`review-open` MUST emit JSON including: PR number/url, AI review round count, unresolved AI review threads (first
comment author matching Copilot/Bugbot/Cursor heuristics), **every** AI review body with heuristically extracted
suppressed / summary-only findings (`ai_reviews`, `summary_only_findings`), and a convenience `latest_ai_review`, plus
the PR head branch name after successful checkout. Resolved threads and non-AI threads MUST be omitted from the
unresolved list. Round count and AI-review lists MUST include only **submitted** reviews (non-null `submittedAt`, state
not `PENDING`). Summary-only findings MUST NOT be limited to the single latest AI review (a later Bugbot/Cursor
submission MUST NOT hide earlier Copilot suppressed comments). Only the latest **unanswered** suppressed AI review
contributes to `summary_only_findings` (at most one open summary review); a triage reply (`Fixed in` / `Dismissed.` /
`Follow-up:`, optionally with `#pullrequestreview-<id>`) after a suppressed review MUST mark it answered. Only
**submitted** non-AI review bodies count as such triage replies (PENDING / unsubmitted drafts MUST be ignored). An
optional `--review-id` MAY force that review’s suppressed items into the open set for permalink triage. When GraphQL
returns a null `pullRequest`, the CLI MUST fail with a clear error naming owner/repo/PR. Summary-only findings MUST be
marked non-resolvable.

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** only the open AI thread appears under unresolved AI threads
- **AND** round_count counts AI review submissions only

#### Scenario: Pending AI reviews are excluded

- **WHEN** GraphQL includes an AI review with null `submittedAt` or state `PENDING`
- **THEN** that review is omitted from `round_count` and `ai_reviews`
- **AND** it does not affect suppressed-review selection

#### Scenario: Pending non-AI draft reviews do not answer suppressed findings

- **WHEN** GraphQL includes a non-AI review with state `PENDING` (or null `submittedAt`) whose body looks like a triage
  reply (`Fixed in` / `Dismissed.` / `Follow-up:`)
- **THEN** that draft MUST NOT mark any suppressed AI review as answered
- **AND** submitted non-AI triage review bodies and issue comments continue to mark suppressed reviews answered as
  before
