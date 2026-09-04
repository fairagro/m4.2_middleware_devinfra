# issue-fixer Specification

## Purpose

Canonical `/issue-fixer` triage → `/opsx-explore` when required → `/opsx-propose` → pause → `/opsx-apply` → pause →
`/opsx-archive`, with a draft PR from an empty bootstrap commit and no auto-committing of fix commits. OpenSpec commands
are exclusive to this skill.

## ADDED Requirements

### Requirement: issue-fixer skill is canonical here

The repository MUST provide `.agents/skills/issue-fixer/SKILL.md` as the shared issue-fixer procedure. The skill MUST
accept an issue number or URL, fetch the issue with `gh`, determine org issue type and triage labels when present, and
MUST NOT auto-commit or auto-push fix commits. Auth MUST match `/review-fixer` / `/create-issue`.

#### Scenario: Agent runs /issue-fixer with an issue number

- **WHEN** the user invokes `/issue-fixer` with an issue number or URL
- **THEN** the skill instructs fetching the issue and triaging type, labels, problem, paths, and acceptance criteria
- **AND** it does not commit or push product fix commits

### Requirement: OpenSpec is exclusive to issue-fixer

`/issue-fixer` MAY and MUST (per cadence below) use OpenSpec slash skills (`/opsx-explore`, `/opsx-propose`,
`/opsx-apply`, `/opsx-archive`, `/opsx-update`). `/review-fixer` and `/create-issue` MUST NOT invoke those OpenSpec
commands as part of their procedures.

#### Scenario: Sibling skills stay off OpenSpec

- **WHEN** an agent runs `/review-fixer` or `/create-issue`
- **THEN** it does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore` as part of that skill

### Requirement: Explore via opsx-explore when required

After successful triage and before `/opsx-propose` or any branch/PR, the skill MUST run explore for org issue types
`Feature` and `Refactoring`. For `Bug`, `Security`, and `Task`, explore is required only when criteria are missing,
multiple plausible fixes exist, or the user asks. `Discussion` MUST NOT implement by default. When explore runs, the
skill MUST follow `.cursor/skills/openspec-explore/SKILL.md` (`/opsx-explore`) and MUST NOT use a parallel in-skill
explore procedure. When explore is not required, the skill MUST skip `/opsx-explore` and continue to the propose
cadence.

#### Scenario: Feature issue uses opsx-explore

- **WHEN** the issue type is `Feature` and triage finds actionable scope
- **THEN** the skill runs `/opsx-explore` and waits for user lock-in or skip-explore
- **AND** it does not create a branch or PR until that pause ends

#### Scenario: Clear Bug skips explore

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to explore first
- **THEN** the skill skips `/opsx-explore` and proceeds to `/opsx-propose`

### Requirement: OpenSpec cadence propose then apply then archive with pauses

On every run that will implement, the skill MUST follow this cadence:

1. **`/opsx-propose`** (`.cursor/skills/openspec-propose/SKILL.md`) → **pause** until the user confirms after reviewing
   proposal / specs / design / tasks.
2. On continue: create the draft bootstrap PR (when needed), then **`/opsx-apply`**
   (`.cursor/skills/openspec-apply-change/SKILL.md`) → **pause** until the user confirms after reviewing the working
   tree (they commit/push; the agent MUST NOT auto-commit fix commits).
3. On continue: **`/opsx-archive`** (`.cursor/skills/openspec-archive-change/SKILL.md`).

If `openspec/` is missing, the skill MUST stop and MUST NOT implement. Early exits that never implement MAY skip the
cadence. The skill MUST NOT skip propose because the work seemed small or not “spec-worthy”. The skill MUST NOT run
apply before the propose pause confirmation, and MUST NOT run archive before the apply pause confirmation.

#### Scenario: Propose pause before apply

- **WHEN** `/opsx-propose` has finished writing artifacts
- **THEN** the skill stops and asks the user to review the change
- **AND** it does not open a draft PR or run `/opsx-apply` until the user confirms

#### Scenario: Apply pause before archive

- **WHEN** `/opsx-apply` has finished the current implementation slice
- **THEN** the skill stops for the user to review/commit/push
- **AND** it does not run `/opsx-archive` until the user confirms

#### Scenario: Archive only after apply pause

- **WHEN** the user confirms after the apply pause
- **THEN** the skill runs `/opsx-archive` for the change

### Requirement: Empty bootstrap commit and draft PR via CLI preferred

After the propose-pause confirmation and before or as part of starting `/opsx-apply`, the skill MUST create branch
`issue-<issue_number>-<slug>` from `main`, one empty commit on a clean tree with `Start issue #<issue_number>`, push,
and open a draft PR with `Fixes #<issue_number>`. Prefer `m42-ai issue-start` when available. MUST NOT mark the PR
ready; MUST NOT create fix commits. PR bodies MUST NOT include tool marketing footers such as “Made with Cursor”; if
injected, the skill MUST strip them before continuing.

#### Scenario: Draft PR from empty bootstrap commit

- **WHEN** the agent is ready to open the PR after propose and user spec-review approval
- **THEN** it creates one empty commit on a clean tree, pushes it, and opens a draft PR with `Fixes #<issue_number>`
- **AND** it does not mark the PR ready
- **AND** the PR body does not contain a “Made with Cursor” footer

### Requirement: Thin docs and entrypoints

The repository MUST provide thin Cursor command and Copilot prompt entrypoints and `docs/issue-fixer.md` that state
`/opsx-explore` when required → `/opsx-propose` → pause → `/opsx-apply` → pause → `/opsx-archive`, and that OpenSpec is
issue-fixer-only.

#### Scenario: Contributor reads issue-fixer docs

- **WHEN** a contributor opens `docs/issue-fixer.md`
- **THEN** they learn explore uses `/opsx-explore` when required
- **AND** they learn the propose → pause → apply → pause → archive cadence
- **AND** they learn OpenSpec is not used by `/review-fixer` or `/create-issue`
