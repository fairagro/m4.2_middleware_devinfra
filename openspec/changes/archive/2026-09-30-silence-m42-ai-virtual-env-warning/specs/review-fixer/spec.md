## MODIFIED Requirements

### Requirement: Fetch open work via review-open CLI

When a PR is known, `/review-fixer` MUST start from a silent primary invoke: `m42-ai review-open --pr <n>` when
`scripts/bin` is on `PATH`, or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai review-open --pr <n>` otherwise
(or equivalent), which establishes the PR head checkout and returns shaped open-work JSON. The agent MUST triage that
JSON and MUST NOT dump the raw GraphQL payload into the model as the primary fetch path. Replies and resolves SHOULD use
`m42-ai review-reply` / `review-resolve` when the CLI is present (documented with the same silent form family). Bare
`uv run m42-ai …` MAY be noted as valid only when `scripts/ai` is a root workspace member. MUST NOT recommend
`uv run --active` to silence the `VIRTUAL_ENV` mismatch warning.

#### Scenario: review-fixer starts from review-open JSON

- **WHEN** the user runs `/review-fixer` with a PR number
- **THEN** the skill instructs invoking `m42-ai review-open` (or
  `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai review-open`) first
- **AND** triage uses `unresolved_ai_threads` (all unresolved authors) and summary-only / suppressed / code-review
  fields from that JSON
- **AND** the skill treats successful `review-open` as having checked out the PR head before any local `fix` edits

### Requirement: Ensure PR head before local fix edits

When a PR number or URL is known, `/review-fixer` MUST treat `m42-ai review-open` as the **first hard gate** before any
triage checklist, GitHub reply, or local `fix` edit. The skill MUST instruct agents to invoke
`m42-ai review-open --pr <n>` (or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai review-open --pr <n>`) as the
first action and MUST NOT proceed unless the CLI exits 0 with `ok` / `pr_head_ok` true (checkout established by
plumbing).

When `review-open` fails closed, the skill MUST instruct agents to **stop immediately**, surface the structured CLI JSON
(`error_code`, `error`, `agent_action: stop`) to the user, and MUST NOT stash, force-checkout, or otherwise improvise
around the failure. The skill MUST NOT silently switch back to a previous branch after a failed or empty open-work run.
Gate semantics (dirty wrong branch vs dirty on head, checkout failure codes) MUST live in the CLI, not as agent-side
heuristics.

Dirty working tree **on** the PR head MUST remain allowed (matching CLI). Paste-only triage without a PR MUST NOT
require checkout.

#### Scenario: PR-scoped run checks out via review-open first

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs starting with `m42-ai review-open --pr <n>` (or the
  `env -u VIRTUAL_ENV uv run --project scripts/ai` equivalent) as the first action
- **AND** triage and local `fix` file edits are deferred until that command exits 0 with `pr_head_ok` true

#### Scenario: Checkout failure stops without improvisation

- **WHEN** `review-open` exits non-zero with `agent_action: stop` (e.g. `error_code` `dirty_wrong_branch`)
- **THEN** the skill instructs stopping and showing the CLI JSON to the user
- **AND** it forbids stash/checkout workarounds and silent return to the previous branch
