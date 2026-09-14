## ADDED Requirements

### Requirement: Synced skills prefer portable m42-ai invoke

Synced first-party fixer skills (`issue-fixer`, `create-issue`, `review-fixer`) and their thin docs MUST document
`uv run --project scripts/ai m42-ai …` as the primary invoke. They MAY note that bare `uv run m42-ai …` works only when
`scripts/ai` is a root uv workspace member (Devinfra). They MUST NOT present bare `uv run m42-ai` as the only or primary
form for product consumers.

#### Scenario: Product agent follows issue-fixer skill

- **WHEN** an agent in a product checkout follows a synced fixer skill to run `m42-ai`
- **THEN** the skill shows `uv run --project scripts/ai m42-ai …` as the primary command
- **AND** it does not require root-workspace membership of `scripts/ai`

### Requirement: scripts/ai pytest works with --project

`scripts/ai` MUST declare a test dependency (or default dependency group) such that `uv run --project scripts/ai pytest`
succeeds in a clean checkout that uses `--project scripts/ai` (product layout).

#### Scenario: Consumer runs scripts/ai pytest

- **WHEN** a contributor runs `uv run --project scripts/ai pytest` after syncing `scripts/ai`
- **THEN** pytest is available without adding product-local deps to the root workspace
- **AND** fixture tests under `scripts/ai/tests` can be collected
