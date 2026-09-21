## MODIFIED Requirements

### Requirement: review-fixer skill is canonical here

The repository MUST provide `.agents/skills/review-fixer/SKILL.md` as the Fixer procedure for shared consumers. The
skill MUST treat `docs/ai_review_policy.md` as the decision source of truth, process **all unresolved review threads**
(any author) from `review-open` plus finder summary-only / suppressed findings (Copilot/Bugbot/Cursor heuristics **and**
`/code-review` marked COMMENT bodies), unless a specific review URL scopes the run, and MUST NOT commit or push. When
any finding is `fix`, the skill MUST use two phases: local fixes plus dismiss/follow-up replies first; `Fixed in <sha>`
only after the user has committed.

#### Scenario: Agent runs /review-fixer with a PR number

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs fetching open review work once via `m42-ai review-open` and triaging unresolved threads
  (any author) plus summary-only / suppressed / code-review findings from that JSON
- **AND** resolved threads are not re-triaged

#### Scenario: Agent pauses for user commit before Fixed replies

- **WHEN** triage yields at least one `fix` action
- **THEN** the skill applies local code changes without committing
- **AND** posts dismiss/follow-up replies in that first phase
- **AND** waits for a user-created commit SHA before posting `Fixed in <sha>.` and resolving those threads

### Requirement: Fetch open work via review-open CLI

When a PR is known, `/review-fixer` MUST start from `uv run --project scripts/ai m42-ai review-open --pr <n>` (or
equivalent), which establishes the PR head checkout and returns shaped open-work JSON. The agent MUST triage that JSON
and MUST NOT dump the raw GraphQL payload into the model as the primary fetch path. Replies and resolves SHOULD use
`m42-ai review-reply` / `review-resolve` when the CLI is present (documented with the same portable
`--project scripts/ai` form). Bare `uv run m42-ai …` MAY be noted as valid only when `scripts/ai` is a root workspace
member.

#### Scenario: review-fixer starts from review-open JSON

- **WHEN** the user runs `/review-fixer` with a PR number
- **THEN** the skill instructs invoking `uv run --project scripts/ai m42-ai review-open` first
- **AND** triage uses `unresolved_ai_threads` (all unresolved authors) and summary-only / suppressed / code-review
  fields from that JSON
- **AND** the skill treats successful `review-open` as having checked out the PR head before any local `fix` edits
