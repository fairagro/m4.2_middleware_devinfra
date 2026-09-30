## MODIFIED Requirements

### Requirement: Prefer issue-create CLI

When creating issues, `/create-issue` MUST prefer a silent primary invoke: `m42-ai issue-create` when `scripts/bin` is
on `PATH`, or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai issue-create` otherwise (org type, triage labels,
optional `--parent`) when the CLI is present in the checkout. Bare `uv run m42-ai issue-create` MAY be noted as valid
only when `scripts/ai` is a root workspace member. Raw `gh issue create` remains a documented fallback only when the CLI
is unavailable. Duplicate-create rules (no second create after a produced issue URL) still apply. MUST NOT recommend
`uv run --active` to silence the `VIRTUAL_ENV` mismatch warning.

#### Scenario: create-issue documents CLI first

- **WHEN** an agent follows `/create-issue` to open a deferred issue
- **THEN** the skill shows `m42-ai issue-create` or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai issue-create`
  as the preferred create path
- **AND** relation `sub-of` maps to `--parent`
