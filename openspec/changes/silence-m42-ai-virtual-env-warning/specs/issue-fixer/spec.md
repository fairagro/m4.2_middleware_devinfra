## MODIFIED Requirements

### Requirement: Portable m42-ai examples in skill and docs

`/issue-fixer` skill and thin docs MUST document a silent primary invoke for `issue-view`, `issue-branch`,
`issue-start`, `auth-status`, `pr-strip-footer`, and related probes: `m42-ai …` when `scripts/bin` is on `PATH`, or
`env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …` otherwise. Bare `uv run m42-ai …` MAY be noted as valid only
when `scripts/ai` is a root workspace member (Devinfra). Product consumers MUST NOT be told that bare `uv run m42-ai` is
the primary path. MUST NOT recommend `uv run --active` to silence the `VIRTUAL_ENV` mismatch warning.

#### Scenario: Agent runs issue-view from skill text

- **WHEN** an agent follows `/issue-fixer` triage fetch instructions
- **THEN** the skill shows a silent primary form (`m42-ai issue-view` or
  `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai issue-view`)
- **AND** the same silent form family is used for branch and draft-PR CLI examples
