# vendor-agent-skills Specification

## Purpose

Reproducible vendor agent skills (`gh`, Docker, hadolint, `uv`) committed under `.agents/skills/`, with lint excludes
and README install/update instructions.

## ADDED Requirements

### Requirement: Vendor skills installed and committed

The repository MUST contain project-scoped vendor skills at `.agents/skills/gh/`, `.agents/skills/docker/`,
`.agents/skills/hadolint/`, and `.agents/skills/uv/`, installed via `gh skill install` (not hand-authored). Those trees
MUST be committed so clones and sync consumers share the same pinned content. Contributors MUST NOT hand-edit files
under those paths; upgrades MUST go through `gh skill update` (or re-install) followed by a reviewable commit. The
repository MUST NOT pin GitGuardian `scan-secrets` as a committed vendor skill.

#### Scenario: Fresh clone has vendor skills

- **WHEN** a contributor clones the repository
- **THEN** `.agents/skills/{gh,docker,hadolint,uv}` are present without a separate install step
- **AND** `.agents/skills/scan-secrets` is absent
- **AND** README still documents how they were installed and how to update them

### Requirement: Documented install and update commands

The root README MUST document the `gh skill install` commands that place skills into `.agents/skills/` (project scope;
agents that share that directory, e.g. Cursor / GitHub Copilot), the rule not to hand-edit vendor trees, and
`gh skill update` for intentional upgrades.

#### Scenario: Contributor looks up vendor skill maintenance

- **WHEN** a contributor reads the root README for agent skills
- **THEN** they find install and update commands for `gh`, `docker`, `hadolint`, and `uv`
- **AND** they are told not to hand-edit those directories

### Requirement: Lint tooling excludes vendor skill trees

Shared markdownlint and Prettier configuration MUST exclude `.agents/skills/gh/`, `.agents/skills/docker/`,
`.agents/skills/hadolint/`, and `.agents/skills/uv/` so vendor Markdown is not reformatted or lint-failed. When a
pre-commit skeleton is added later, it MUST apply the same excludes; this change MUST NOT require introducing pre-commit
solely for those excludes.

#### Scenario: format:md skips vendor skills

- **WHEN** `npm run format:md` / markdownlint runs on the repo
- **THEN** paths under `.agents/skills/{gh,docker,hadolint,uv}/` are ignored
