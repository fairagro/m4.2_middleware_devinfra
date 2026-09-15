## ADDED Requirements

### Requirement: Ensure PR head before local fix edits

When a PR number or URL is known, `/review-fixer` MUST rely on `m42-ai review-open` to establish the PR head branch
before applying any local `fix` edits. The skill MUST instruct agents not to write `fix` changes until checkout matches
the PR head (or until the CLI has failed closed with a clear error). Paste-only triage without a PR MUST NOT require
checkout.

#### Scenario: PR-scoped run checks out via review-open first

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs starting with `uv run --project scripts/ai m42-ai review-open --pr <n>`
- **AND** local `fix` file edits are deferred until that command has succeeded with the PR head checked out

## MODIFIED Requirements

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
- **AND** triage uses `unresolved_ai_threads` and summary-only / suppressed fields from that JSON
- **AND** the skill treats successful `review-open` as having checked out the PR head before any local `fix` edits
