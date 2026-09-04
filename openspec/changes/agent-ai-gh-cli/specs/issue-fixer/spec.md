# issue-fixer Specification

## Purpose

Canonical `/issue-fixer` triage → explore → OpenSpec propose → spec-review pause → draft PR from empty bootstrap → local
implement without auto-committing fix commits.

## ADDED Requirements

### Requirement: issue-fixer skill is canonical here

The repository MUST provide `.agents/skills/issue-fixer/SKILL.md` as the shared issue-fixer procedure. The skill MUST
accept an issue number or URL, fetch the issue with `gh`, determine org issue type and triage labels when present, and
MUST NOT auto-commit or auto-push fix commits. Auth MUST match `/review-fixer` / `/create-issue`.

#### Scenario: Agent runs /issue-fixer with an issue number

- **WHEN** the user invokes `/issue-fixer` with an issue number or URL
- **THEN** the skill instructs fetching the issue and triaging type, labels, problem, paths, and acceptance criteria
- **AND** it does not commit or push product fix commits

### Requirement: Explore pause before GitHub writes for Feature and Refactoring

After successful triage and before any branch, empty commit, or PR creation, the skill MUST run an explore pause for org
issue types `Feature` and `Refactoring`. For `Bug`, `Security`, and `Task`, explore is required only when criteria are
missing, multiple plausible fixes exist, or the user asks. `Discussion` MUST NOT implement by default. The skill MUST
NOT hard-depend on `/opsx-explore` (`/opsx-explore` is **optional**; in-skill explore is enough).

#### Scenario: Feature issue pauses for lock-in

- **WHEN** the issue type is `Feature` and triage finds actionable scope
- **THEN** the skill surfaces open threads and waits for user lock-in or skip-explore
- **AND** it does not create a branch or PR until that pause ends
- **AND** it does not require `/opsx-explore`

### Requirement: OpenSpec propose before implement

**`/opsx-propose` is mandatory.** Before any branch, empty bootstrap commit, draft PR, or implementation on a run that
will implement, the skill MUST run `/opsx-propose` by following `.cursor/skills/openspec-propose/SKILL.md`. If
`openspec/` is missing, the skill MUST stop and MUST NOT implement. Early exits that never implement MAY skip propose.
The skill MUST NOT skip propose because the work seemed small or not “spec-worthy”.

#### Scenario: Implement run always proposes

- **WHEN** triage completes and the run will open a draft PR and implement
- **THEN** the skill creates an OpenSpec change via `/opsx-propose` before the empty bootstrap commit

### Requirement: Spec-review pause after propose

After `/opsx-propose` artifacts exist, the skill MUST pause and MUST NOT create a branch, empty commit, draft PR, or
start implementation until the user confirms after reviewing proposal / specs / design / tasks (e.g. `go`, `approved`,
or an `/opsx-update` pass then `go`). Prefer `/opsx-apply` only after that confirmation and after the draft PR exists.

#### Scenario: Agent stops for spec review

- **WHEN** `/opsx-propose` has finished writing artifacts
- **THEN** the skill stops and asks the user to review the change
- **AND** it does not open a draft PR until the user confirms

### Requirement: Empty bootstrap commit and draft PR via CLI preferred

After propose **and** the spec-review confirmation, the skill MUST create branch `issue-<issue_number>-<slug>` from
`main`, one empty commit on a clean tree with `Start issue #<issue_number>`, push, and open a draft PR with
`Fixes #<issue_number>`. Prefer `m42-ai issue-start` when available. MUST NOT mark the PR ready; MUST NOT create fix
commits. PR bodies MUST NOT include tool marketing footers such as “Made with Cursor”; if injected, the skill MUST strip
them before continuing.

#### Scenario: Draft PR from empty bootstrap commit

- **WHEN** the agent is ready to open the PR after propose and user spec-review approval
- **THEN** it creates one empty commit on a clean tree, pushes it, and opens a draft PR with `Fixes #<issue_number>`
- **AND** it does not mark the PR ready
- **AND** the PR body does not contain a “Made with Cursor” footer

### Requirement: Thin docs and entrypoints

The repository MUST provide thin Cursor command and Copilot prompt entrypoints and `docs/issue-fixer.md` that state
explore → `/opsx-propose` → spec-review pause → draft PR → local implement.

#### Scenario: Contributor reads issue-fixer docs

- **WHEN** a contributor opens `docs/issue-fixer.md`
- **THEN** they learn that `/opsx-propose` is required before implement
- **AND** they learn there is a pause for spec review before the draft PR
