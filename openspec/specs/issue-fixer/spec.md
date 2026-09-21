# issue-fixer Specification

## Purpose

Canonical `/issue-fixer` triage → in-skill explore when required → create issue branch → type-routed implement (OpenSpec
for Feature/Refactoring; Task/Bug fast path) → pause → draft PR (real commits only), with no auto-committing of fix
commits and no empty bootstrap commits.

## Requirements

### Requirement: issue-fixer skill is canonical here

The repository MUST provide `.agents/skills/issue-fixer/SKILL.md` as the shared issue-fixer procedure. The skill MUST
accept an issue number or URL, fetch the issue with `gh` (prefer `m42-ai issue-view`), determine org issue type and triage
labels when present, and MUST NOT auto-commit or auto-push fix commits. Auth MUST match `/review-fixer` /
`/create-issue`.

Triage MUST include issue conversation comments from `issue-view` JSON `comments` (or `gh issue view` including
comments). When comments contradict each other or the issue body, the **newer** comment wins (`created_at` later).

#### Scenario: Agent runs /issue-fixer with an issue number

- **WHEN** the user invokes `/issue-fixer` with an issue number or URL
- **THEN** the skill instructs fetching the issue and triaging type, labels, problem, paths, acceptance criteria, and
  issue comments
- **AND** it does not commit or push product fix commits

#### Scenario: Newer comment wins on conflict

- **WHEN** triage finds an issue body (or older comment) that conflicts with a later comment
- **THEN** the skill treats the newer comment as authoritative for problem statement / done-when / lock-ins

### Requirement: issue-fixer does not run OpenSpec

`/issue-fixer` MUST route OpenSpec by org issue type:

- **Feature** and **Refactoring**: after explore (when required), follow `.cursor/skills/openspec-propose/SKILL.md`,
  then `.cursor/skills/openspec-apply-change/SKILL.md`, then after the draft-PR step
  `.cursor/skills/openspec-archive-change/SKILL.md` as the last `go` — **except** when it is clear the slice is
  **docs-only** (Markdown/MDC and/or code comments only) **and** no skill file is in scope.
- **Task**, **Bug**, and cheap **Security**: MUST NOT invoke OpenSpec slash skills or create an OpenSpec change unless
  the user explicitly asks (`use opsx`), **except** when a skill file is in scope (`SKILL.md` under `.agents/skills/` or
  `.cursor/skills/`), in which case OpenSpec is required even for Task.
- If a **Task** clearly changes a capability under `openspec/specs/`, the skill MUST pause once and ask to retype as
  Feature or confirm `use opsx` — it MUST NOT silently create an OpenSpec change.
- Docs-only Markdown under `openspec/specs/` or `openspec/changes/` is **not** docs-only. If docs-only is unclear for
  Feature/Refactoring, keep OpenSpec.
- **Discussion** MUST NOT implement by default.
- `/review-fixer` and `/create-issue` MUST NOT invoke OpenSpec commands as part of their procedures. Standalone
  `/opsx-*` remain available when the user invokes them explicitly outside these skills. A user override MAY force
  OpenSpec on a Bug/Task or skip OpenSpec on a Feature.

#### Scenario: Clear Task stays off OpenSpec

- **WHEN** the issue type is `Task` with actionable known-how scope
- **AND** no skill file is in scope
- **AND** the user did not ask to use OpenSpec
- **THEN** the skill does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore`
- **AND** it proceeds to the issue branch and implement like the Bug fast path

#### Scenario: Feature uses OpenSpec propose then apply then archive

- **WHEN** an agent runs `/issue-fixer` on a `Feature` with actionable scope that is not docs-only
- **THEN** after the issue branch exists it creates an OpenSpec change via the propose skill
- **AND** it does not implement product code until the user confirms after reviewing proposal artifacts
- **AND** after apply and the draft PR, a later `go` runs the archive skill

#### Scenario: Clear Bug stays off OpenSpec

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to use OpenSpec
- **THEN** the skill does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore`
- **AND** it proceeds to the issue branch and implement as today

#### Scenario: Docs-only Feature skips OpenSpec

- **WHEN** the issue type is `Feature` or `Refactoring`
- **AND** it is clear the slice only changes Markdown/MDC and/or code comments
- **AND** no skill file (`SKILL.md` under `.agents/skills/` or `.cursor/skills/`) is in scope
- **THEN** the skill does not create an OpenSpec change
- **AND** it implements on the issue branch like the Bug fast path

#### Scenario: Skill-file change keeps OpenSpec

- **WHEN** the issue type is `Task`, `Feature`, or `Refactoring`
- **AND** a skill file is in scope
- **THEN** the skill follows propose → apply → draft PR → archive even if typed Task or the rest of the slice is
  Markdown

#### Scenario: Misfiled Task pauses for retype or opsx

- **WHEN** the issue type is `Task`
- **AND** acceptance criteria clearly change a capability under `openspec/specs/`
- **AND** the user has not already said `use opsx`
- **THEN** the skill pauses and asks to retype as Feature or confirm `use opsx`
- **AND** it does not silently create an OpenSpec change folder

#### Scenario: Sibling skills stay off OpenSpec

- **WHEN** an agent runs `/review-fixer` or `/create-issue`
- **THEN** it does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore` as part of that skill

### Requirement: Explore in-skill when required

After successful triage and before branch/propose/implement/PR, the skill MUST run explore for org issue types `Feature`
and `Refactoring`. For `Bug`, `Security`, and `Task`, explore is required only when criteria are missing, multiple
plausible fixes exist, or the user asks. `Discussion` MUST NOT implement by default. When explore runs, the skill MUST
explore in-skill (clarify scope, compare options, wait for lock-in / `go` / `skip explore`) and MUST NOT invoke
`/opsx-explore`. When explore is not required, the skill MUST skip explore and continue to the type-routed next step
(OpenSpec propose for Feature/Refactoring when applicable; implement for Task/Bug/Security).

#### Scenario: Feature issue uses in-skill explore

- **WHEN** the issue type is `Feature` and triage finds actionable scope
- **THEN** the skill explores in-skill and waits for user lock-in or skip-explore
- **AND** it does not create a branch, OpenSpec change, or PR until that pause ends
- **AND** it does not run `/opsx-explore`

#### Scenario: Clear Bug skips explore

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to explore first
- **THEN** the skill skips explore and proceeds to create the issue branch and implement (no OpenSpec)

### Requirement: Branch then implement then pause then draft PR

On every run that will implement, the skill MUST create local branch `issue-<issue_number>-<slug>` from `main` before
writing OpenSpec artifacts or product code. The skill MUST NOT auto-commit; MUST NOT use empty bootstrap commits.

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
- **THEN** the skill creates `issue-<issue_number>-<slug>` from `main` before writing product code or OpenSpec artifacts
- **AND** it does not open a draft PR yet
- **AND** it does not auto-commit

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

### Requirement: Draft PR after real commits via CLI preferred

After the implement-pause confirmation, the skill MUST ensure a **draft** PR exists with `Fixes #<issue_number>` when
the issue branch tip already has commits ahead of `main`. The skill MUST NOT create empty bootstrap commits
(`git commit --allow-empty` or equivalent). Prefer `m42-ai issue-start` when available. Prefer `m42-ai issue-view` for
triage fetch, `m42-ai issue-branch` for the early branch step, `m42-ai branch-ahead` / `m42-ai auth-status` for probes,
and `m42-ai pr-strip-footer` after PR create when a marketing footer may be present. MUST NOT mark the PR ready; MUST
NOT create fix commits. If the tip still equals `main`, the skill MUST stop and ask the user to commit first. PR bodies
MUST NOT include tool marketing footers such as “Made with Cursor”; if injected, the skill MUST strip them before
continuing.

#### Scenario: Draft PR requires commits ahead of main

- **WHEN** the agent is ready to open the PR after implement and user confirmation
- **AND** the issue branch tip has at least one commit ahead of `main`
- **THEN** it ensures a draft PR with `Fixes #<issue_number>` exists
- **AND** it does not mark the PR ready
- **AND** the PR body does not contain a “Made with Cursor” footer
- **AND** it did not create an empty bootstrap commit

#### Scenario: No PR when tip equals main

- **WHEN** the agent would open a draft PR but the issue branch tip equals `main`
- **THEN** it does not create an empty commit
- **AND** it asks the user to commit real work first

### Requirement: Thin docs and entrypoints

The repository MUST provide thin Cursor command and Copilot prompt entrypoints and `docs/issue-fixer.md` that state
in-skill explore when required, type-routed OpenSpec (propose → pause → apply → pause → draft PR → archive as last `go`
for Feature/Refactoring except clear docs-only slices; Task/Bug/Security fast path without OpenSpec unless skill file or
user override), the skill-file exception, misfile pause for Task, `skip_specs` vs real delta specs, and that
`/review-fixer` and `/create-issue` do not run OpenSpec.

#### Scenario: Contributor reads issue-fixer docs

- **WHEN** a contributor opens `docs/issue-fixer.md`
- **THEN** they learn explore is in-skill when required
- **AND** they learn Feature/Refactoring use propose → apply → draft PR → archive except clear docs-only slices
- **AND** they learn Task/Bug/Security stay off OpenSpec unless asked or a skill file is in scope
- **AND** they learn triage includes issue comments with newer-wins on conflict
- **AND** they learn `/review-fixer` and `/create-issue` do not run OpenSpec

### Requirement: Portable m42-ai examples in skill and docs

`/issue-fixer` skill and thin docs MUST document `uv run --project scripts/ai m42-ai …` for `issue-view`,
`issue-branch`, `issue-start`, `auth-status`, `pr-strip-footer`, and related probes. Bare `uv run m42-ai …` MAY be noted
as valid only when `scripts/ai` is a root workspace member (Devinfra). Product consumers MUST NOT be told that bare
`uv run m42-ai` is the primary path.

#### Scenario: Agent runs issue-view from skill text

- **WHEN** an agent follows `/issue-fixer` triage fetch instructions
- **THEN** the skill shows `uv run --project scripts/ai m42-ai issue-view`
- **AND** the same portable form is used for branch and draft-PR CLI examples

### Requirement: skip_specs versus delta specs

When `/issue-fixer` creates an OpenSpec change, it MUST write real delta specs when a capability contract changes. It
MUST set `skip_specs: true` only when the Feature/Refactoring (or Task with `use opsx` / skill file) is docs/tooling
with **no** spec-level behavior change. The skill MUST NOT invent a requirement solely to satisfy validation.

#### Scenario: Contract change uses a delta spec

- **WHEN** `/issue-fixer` proposes a Feature that changes an existing capability (for example `issue-fixer` itself)
- **THEN** the change includes a delta spec for that capability
- **AND** it does not set `skip_specs: true`

#### Scenario: Docs tooling Feature may skip specs

- **WHEN** `/issue-fixer` proposes a Feature that does not change spec-level behavior
- **THEN** the change MAY set `skip_specs: true`
- **AND** it does not invent a capability requirement only to pass validation
