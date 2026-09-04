# create-issue Delta

## MODIFIED Requirements

### Requirement: Prefer issue-create CLI

When creating issues, `/create-issue` MUST prefer `uv run --project scripts/ai m42-ai issue-create` (org type, triage
labels, optional `--parent`) when the CLI is present in the checkout. Raw `gh issue create` remains a documented
fallback only when the CLI is unavailable. Duplicate-create rules (no second create after a produced issue URL) still
apply.

#### Scenario: create-issue documents CLI first

- **WHEN** an agent follows `/create-issue` to open a deferred issue
- **THEN** the skill shows `m42-ai issue-create` as the preferred create path
- **AND** relation `sub-of` maps to `--parent`
