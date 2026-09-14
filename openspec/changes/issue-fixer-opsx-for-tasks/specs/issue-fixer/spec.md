# issue-fixer Delta

## MODIFIED Requirements

### Requirement: issue-fixer does not run OpenSpec

`/issue-fixer` MUST route OpenSpec by org issue type. For **Task**, **Feature**, and **Refactoring**, after explore
(when required) the skill MUST follow `.cursor/skills/openspec-propose/SKILL.md`, then
`.cursor/skills/openspec-apply-change/SKILL.md`, then after the draft-PR step
`.cursor/skills/openspec-archive-change/SKILL.md` as the last `go` — **except** when it is clear the slice is
**docs-only** (Markdown/MDC and/or code comments only). Docs-only work MUST use the Bug-style implement path (no
OpenSpec) **unless** a skill file is in scope (`SKILL.md` under `.agents/skills/` or `.cursor/skills/`), in which case
OpenSpec remains required. Markdown under `openspec/specs/` or `openspec/changes/` is **not** docs-only. If docs-only is
unclear, the skill MUST keep OpenSpec for Task/Feature/Refactoring. For **Bug** and cheap **Security**, the skill MUST
NOT invoke OpenSpec slash skills or create an OpenSpec change unless the user explicitly asks. **Discussion** MUST NOT
implement by default. `/review-fixer` and `/create-issue` MUST NOT invoke OpenSpec commands as part of their procedures.
Standalone `/opsx-*` remain available when the user invokes them explicitly outside these skills. A user override MAY
force OpenSpec on a Bug or skip OpenSpec on a Task.

#### Scenario: Task uses OpenSpec propose then apply then archive

- **WHEN** an agent runs `/issue-fixer` on a `Task` with actionable scope
- **THEN** after the issue branch exists it creates an OpenSpec change via the propose skill
- **AND** it does not implement product code until the user confirms after reviewing proposal artifacts
- **AND** after apply and the draft PR, a later `go` runs the archive skill

#### Scenario: Clear Bug stays off OpenSpec

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to use OpenSpec
- **THEN** the skill does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore`
- **AND** it proceeds to the issue branch and implement as today

#### Scenario: Docs-only Task skips OpenSpec

- **WHEN** the issue type is `Task`, `Feature`, or `Refactoring`
- **AND** it is clear the slice only changes Markdown/MDC and/or code comments
- **AND** no skill file (`SKILL.md` under `.agents/skills/` or `.cursor/skills/`) is in scope
- **THEN** the skill does not create an OpenSpec change
- **AND** it implements on the issue branch like the Bug fast path

#### Scenario: Skill-file change keeps OpenSpec

- **WHEN** the issue type is `Task`, `Feature`, or `Refactoring`
- **AND** a skill file is in scope
- **THEN** the skill follows propose → apply → draft PR → archive even if the rest of the slice is Markdown

#### Scenario: Sibling skills stay off OpenSpec

- **WHEN** an agent runs `/review-fixer` or `/create-issue`
- **THEN** it does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore` as part of that skill

### Requirement: Explore in-skill when required

After successful triage and before branch/propose/implement/PR, the skill MUST run explore for org issue types `Feature`
and `Refactoring`. For `Bug`, `Security`, and `Task`, explore is required only when criteria are missing, multiple
plausible fixes exist, or the user asks. `Discussion` MUST NOT implement by default. When explore runs, the skill MUST
explore in-skill (clarify scope, compare options, wait for lock-in / `go` / `skip explore`) and MUST NOT invoke
`/opsx-explore`. When explore is not required, the skill MUST skip explore and continue to the type-routed next step
(OpenSpec propose for Task/Feature/Refactoring; implement for Bug/Security).

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

For **Task**, **Feature**, and **Refactoring** that are **not** docs-only (or that touch a skill file) the skill MUST
then:

1. Follow the propose skill → **pause** until the user confirms after reviewing proposal / specs / design / tasks
2. On `go`: follow the apply skill → **pause** until the user confirms after reviewing the working tree (they
   commit/push)
3. On `go`: ensure a **draft** PR when the branch tip has real commits ahead of `main`
4. On `go` (last): follow the archive skill → **pause** so the user can commit archive results

For **Bug** and cheap **Security** (no OpenSpec), and for **docs-only** Task/Feature/Refactoring that do not touch a
skill file, the skill MUST implement in the working tree, pause, then on continue ensure the draft PR as today.

Early exits that never implement MAY skip this cadence.

#### Scenario: Branch before propose or implement

- **WHEN** the run will implement after explore (or after skipping explore)
- **THEN** the skill creates `issue-<issue_number>-<slug>` from `main` before writing product code or OpenSpec artifacts
- **AND** it does not open a draft PR yet
- **AND** it does not auto-commit

#### Scenario: Propose pause before apply

- **WHEN** the issue type is `Task`, `Feature`, or `Refactoring` and propose has finished writing artifacts
- **THEN** the skill stops and asks the user to review the change
- **AND** it does not run apply or open a draft PR until the user confirms

#### Scenario: Implement pause before draft PR

- **WHEN** implementation for the current slice is done (apply for OpenSpec types; direct implement for Bug/Security)
- **THEN** the skill stops for the user to review/commit/push
- **AND** it does not open a draft PR until the user confirms

#### Scenario: Archive is the last go after draft PR

- **WHEN** the issue type is `Task`, `Feature`, or `Refactoring` and a draft PR exists (or was skipped only because the
  tip still equals `main`)
- **AND** the user confirms with `go` after that step
- **THEN** the skill follows the archive skill for the change
- **AND** it does not auto-commit the archive result

### Requirement: Thin docs and entrypoints

The repository MUST provide thin Cursor command and Copilot prompt entrypoints and `docs/issue-fixer.md` that state
in-skill explore when required, type-routed OpenSpec (propose → pause → apply → pause → draft PR → archive as last `go`
for Task/Feature/Refactoring except clear docs-only slices; Bug/Security fast path without OpenSpec), the skill-file
exception, `skip_specs` vs real delta specs, and that `/review-fixer` and `/create-issue` do not run OpenSpec.

#### Scenario: Contributor reads issue-fixer docs

- **WHEN** a contributor opens `docs/issue-fixer.md`
- **THEN** they learn explore is in-skill when required
- **AND** they learn Task/Feature/Refactoring use propose → apply → draft PR → archive except clear docs-only slices
  (Markdown/comments, no skill files)
- **AND** they learn Bug/Security stay off OpenSpec unless asked
- **AND** they learn `/review-fixer` and `/create-issue` do not run OpenSpec

## ADDED Requirements

### Requirement: skip_specs versus delta specs

When `/issue-fixer` creates an OpenSpec change, it MUST write real delta specs when a capability contract changes. It
MUST set `skip_specs: true` only when the Task (or Feature/Refactoring) is docs/tooling with **no** spec-level behavior
change. The skill MUST NOT invent a requirement solely to satisfy validation.

#### Scenario: Contract change uses a delta spec

- **WHEN** `/issue-fixer` proposes a Task that changes an existing capability (for example `issue-fixer` itself)
- **THEN** the change includes a delta spec for that capability
- **AND** it does not set `skip_specs: true`

#### Scenario: Docs-only Task may skip specs

- **WHEN** `/issue-fixer` proposes a Task that does not change spec-level behavior
- **THEN** the change MAY set `skip_specs: true`
- **AND** it does not invent a capability requirement only to pass validation
