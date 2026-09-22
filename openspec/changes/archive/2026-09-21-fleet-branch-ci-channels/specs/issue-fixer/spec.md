## MODIFIED Requirements

### Requirement: Branch then implement then pause then draft PR

On every run that will implement, the skill MUST create a local branch `{channel}/issue-<issue_number>-<slug>` from
`main` before writing OpenSpec artifacts or product code. `{channel}` is one of `build`, `ci`, or `docs` (CI channel
prefix — not the GitHub issue type). The skill MUST pick:

- `docs` when the slice is clearly docs-only (Markdown/MDC and/or code comments, no skill file, not under
  `openspec/specs/` or `openspec/changes/`)
- `ci` when the slice is clearly limited to shared CI/tooling (for example `scripts/`, `.devcontainer/`, workflows,
  quality configs, tests for those) without product image/app code
- `build` otherwise (including unclear scope — fail-safe toward image/RC-eligible work)

The skill MUST NOT use `feature/` as the channel prefix. The skill MUST NOT auto-commit; MUST NOT use empty bootstrap
commits. Prefer `m42-ai issue-branch` with the chosen channel when available.

For **Feature** and **Refactoring** that are **not** docs-only (or any type that touches a skill file, including Task)
the skill MUST then:

1. Follow the propose skill → **pause** until the user confirms after reviewing proposal / specs / design / tasks
2. On `go`: follow the apply skill → **pause** until the user confirms after reviewing the working tree (they
   commit/push)
3. On `go`: ensure a **draft** PR when the branch tip has real commits ahead of `main`
4. On `go` (last): follow the archive skill → **pause** so the user can commit archive results

For **Task**, **Bug**, and cheap **Security** (no OpenSpec), and for **docs-only** Feature/Refactoring that do not touch
a skill file, the skill MUST implement in the working tree, pause, then on continue ensure the draft PR as today.

Early exits that never implement MAY skip this cadence.

#### Scenario: Branch before propose or implement

- **WHEN** the run will implement after explore (or after skipping explore)
- **THEN** the skill creates `{channel}/issue-<issue_number>-<slug>` from `main` before writing product code or OpenSpec
  artifacts
- **AND** it does not open a draft PR yet
- **AND** it does not auto-commit

#### Scenario: Docs-only uses docs channel

- **WHEN** the slice is clearly docs-only per the docs-only rule
- **THEN** the skill creates a branch under `docs/issue-<issue_number>-…`

#### Scenario: Tooling-only uses ci channel

- **WHEN** the slice is clearly limited to shared CI/tooling without product image/app code
- **THEN** the skill creates a branch under `ci/issue-<issue_number>-…`

#### Scenario: Unclear or image-related uses build channel

- **WHEN** scope is unclear or includes product image/app code
- **THEN** the skill creates a branch under `build/issue-<issue_number>-…`

#### Scenario: Propose pause before apply

- **WHEN** the issue type is `Feature` or `Refactoring` (or Task with skill file / `use opsx`) and propose has finished
  writing artifacts
- **THEN** the skill stops and asks the user to review the change
- **AND** it does not run apply or open a draft PR until the user confirms

#### Scenario: Implement pause before draft PR

- **WHEN** implementation for the current slice is done (apply for OpenSpec types; direct implement for
  Task/Bug/Security)
- **THEN** the skill stops for the user to review/commit/push
- **AND** it does not open a draft PR until the user confirms

#### Scenario: Archive is the last go after draft PR

- **WHEN** the issue type is `Feature` or `Refactoring` (or Task with skill file / `use opsx`) and a draft PR exists (or
  was skipped only because the tip still equals `main`)
- **AND** the user confirms with `go` after that step
- **THEN** the skill follows the archive skill for the change
- **AND** it does not auto-commit the archive result
