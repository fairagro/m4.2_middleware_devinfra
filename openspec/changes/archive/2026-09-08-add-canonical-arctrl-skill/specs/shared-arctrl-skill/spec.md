# shared-arctrl-skill Specification

## Purpose

Canonical first-party arctrl agent skill so Devinfra owns the shared reference products sync from, at harvester fidelity
for arctrl ≥ 3.2.1, without treating it as a vendor skill pin.

## ADDED Requirements

### Requirement: Canonical arctrl skill is present

The repository MUST provide `.agents/skills/arctrl/SKILL.md` as the shared arctrl usage reference for agents. The skill
content MUST equal or supersede the harvester product skill feature set for arctrl ≥ 3.2.1 (including casing rules,
`fable_library`, WriteContracts / `GetAdditionalPayload`, `Comment`, and Columns API coverage where present in that
source). The skill MUST be first-party and hand-maintainable in this repo (not installed via `gh skill`).

#### Scenario: Fresh clone has arctrl skill

- **WHEN** a contributor clones the repository
- **THEN** `.agents/skills/arctrl/SKILL.md` is present without a separate install step
- **AND** the skill front matter identifies arctrl ≥ 3.2.1 (or equivalent compatibility)

#### Scenario: Content matches harvester fidelity

- **WHEN** a reviewer compares the canonical skill to the harvester `.agents/skills/arctrl/SKILL.md` at import time
- **THEN** the canonical skill covers the same feature set (or a deliberate superset)
- **AND** it does not regress to the thinner API / sql-to-arc skill shape

### Requirement: README documents the skill as first-party shared

The root README MUST list `.agents/skills/arctrl/` as a shared first-party skill (layout table and/or skills section)
and MUST NOT present it as a vendor `gh skill` pin or instruct `gh skill install` for arctrl.

#### Scenario: Contributor looks up arctrl skill ownership

- **WHEN** a contributor reads the root README for agent skills / layout
- **THEN** they find `.agents/skills/arctrl/` described as a shared first-party skill
- **AND** they are not directed to install or update it via `gh skill`

### Requirement: arctrl skill is not vendor-excluded

Shared markdownlint, Prettier, and pre-commit vendor excludes MUST NOT add `.agents/skills/arctrl/` to the vendor skill
ignore set. The skill MUST be formatted and linted like other first-party shared skills (`review-fixer`, `create-issue`,
`issue-fixer`).

#### Scenario: format:md covers arctrl skill

- **WHEN** `npm run format:md` / markdownlint runs on the repo
- **THEN** `.agents/skills/arctrl/` is not ignored solely because it is under `.agents/skills/`
- **AND** vendor excludes remain limited to `gh`, `docker`, `hadolint`, and `uv`
