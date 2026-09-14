## ADDED Requirements

### Requirement: Code Quality wording is consumer-portable

`openspec/principles.global.md` Code Quality MUST describe shared quality gates in wording that remains accurate for
product consumers: use shared config fragments when present (`ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`) or the
project's equivalent config, and cite `docs/quality.md` when that file is synced. It MUST NOT imply that every consumer
checkout already has Devinfra-only paths, and MUST NOT push agents to invent a second quality policy channel.

#### Scenario: Product agent reads Code Quality

- **WHEN** an agent in a product checkout reads `openspec/principles.global.md` Code Quality
- **THEN** the commands remain valid when shared fragments are synced
- **AND** the text does not require inventing product-local quality policy outside shared fragments / project config
