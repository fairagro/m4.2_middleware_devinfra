## MODIFIED Requirements

### Requirement: Recurring steps use m42-ai

Recurring mechanical steps MUST go through a silent primary form: `m42-ai …` when `scripts/bin` is on `PATH`, or
`env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …` otherwise: at least (1) shape diff/PR context as JSON, (2)
write the report file under `/tmp`, (3) publish the PR Review (or documented fallback). The skill MUST keep judgment and
checklist application in the agent, not encode AI review policy as Python. Bare `uv run m42-ai …` MAY be noted as valid
only when `scripts/ai` is a root workspace member. MUST NOT recommend `uv run --active` to silence the `VIRTUAL_ENV`
mismatch warning.

#### Scenario: Skill documents portable invoke

- **WHEN** an agent in a product checkout follows `/code-review`
- **THEN** the skill shows `m42-ai …` or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …` as the primary
  command form for helpers
- **AND** it does not require root-workspace membership of `scripts/ai`
