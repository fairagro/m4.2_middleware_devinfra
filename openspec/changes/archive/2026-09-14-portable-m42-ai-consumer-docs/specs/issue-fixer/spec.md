## ADDED Requirements

### Requirement: Portable m42-ai examples in skill and docs

`/issue-fixer` skill and thin docs MUST document `uv run --project scripts/ai m42-ai …` for `issue-view`,
`issue-branch`, `issue-start`, `auth-status`, `pr-strip-footer`, and related probes. Bare `uv run m42-ai …` MAY be noted
as valid only when `scripts/ai` is a root workspace member (Devinfra). Product consumers MUST NOT be told that bare
`uv run m42-ai` is the primary path.

#### Scenario: Agent runs issue-view from skill text

- **WHEN** an agent follows `/issue-fixer` triage fetch instructions
- **THEN** the skill shows `uv run --project scripts/ai m42-ai issue-view`
- **AND** the same portable form is used for branch and draft-PR CLI examples
