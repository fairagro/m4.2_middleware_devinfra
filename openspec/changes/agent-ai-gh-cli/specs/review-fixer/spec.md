## MODIFIED Requirements

### Requirement: Fetch open work via review-open CLI

When a PR is known, `/review-fixer` MUST start from `uv run --project scripts/ai m42-ai review-open --pr <n>` (or
equivalent) and triage the shaped JSON. It MUST NOT dump the raw GraphQL payload into the model as the primary fetch
path. Replies and resolves SHOULD use `m42-ai review-reply` / `review-resolve` when the CLI is present.

#### Scenario: review-fixer starts from review-open JSON

- **WHEN** the user runs `/review-fixer` with a PR number
- **THEN** the skill instructs invoking `m42-ai review-open` first
- **AND** triage uses `unresolved_ai_threads` and latest AI review / suppressed fields from that JSON
