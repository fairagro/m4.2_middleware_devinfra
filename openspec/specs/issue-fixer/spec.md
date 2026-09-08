# issue-fixer Specification

## Purpose

Canonical `/issue-fixer` triage → in-skill explore when required → create issue branch → implement → pause → draft PR
(real commits only), with no auto-committing of fix commits, no empty bootstrap commits, and **no** OpenSpec cadence.

## Requirements

### Requirement: issue-fixer skill is canonical here

The repository MUST provide `.agents/skills/issue-fixer/SKILL.md` as the shared issue-fixer procedure. The skill MUST
accept an issue number or URL, fetch the issue with `gh`, determine org issue type and triage labels when present, and
MUST NOT auto-commit or auto-push fix commits. Auth MUST match `/review-fixer` / `/create-issue`.

#### Scenario: Agent runs /issue-fixer with an issue number

- **WHEN** the user invokes `/issue-fixer` with an issue number or URL
- **THEN** the skill instructs fetching the issue and triaging type, labels, problem, paths, and acceptance criteria
- **AND** it does not commit or push product fix commits

### Requirement: issue-fixer does not run OpenSpec

`/issue-fixer` MUST NOT invoke OpenSpec slash skills (`/opsx-explore`, `/opsx-propose`, `/opsx-apply`, `/opsx-archive`,
`/opsx-update`) or create an OpenSpec change as part of its procedure. `/review-fixer` and `/create-issue` MUST likewise
NOT invoke those commands. Standalone `/opsx-*` commands remain available only when the user invokes them explicitly
outside these skills.

#### Scenario: issue-fixer stays off OpenSpec

- **WHEN** an agent runs `/issue-fixer`
- **THEN** it does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore` as part of that skill

#### Scenario: Sibling skills stay off OpenSpec

- **WHEN** an agent runs `/review-fixer` or `/create-issue`
- **THEN** it does not run `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, or `/opsx-explore` as part of that skill

### Requirement: Explore in-skill when required

After successful triage and before branch/implement/PR, the skill MUST run explore for org issue types `Feature` and
`Refactoring`. For `Bug`, `Security`, and `Task`, explore is required only when criteria are missing, multiple plausible
fixes exist, or the user asks. `Discussion` MUST NOT implement by default. When explore runs, the skill MUST explore
in-skill (clarify scope, compare options, wait for lock-in / `go` / `skip explore`) and MUST NOT invoke `/opsx-explore`.
When explore is not required, the skill MUST skip explore and continue to implement.

#### Scenario: Feature issue uses in-skill explore

- **WHEN** the issue type is `Feature` and triage finds actionable scope
- **THEN** the skill explores in-skill and waits for user lock-in or skip-explore
- **AND** it does not create a branch or PR until that pause ends
- **AND** it does not run `/opsx-explore`

#### Scenario: Clear Bug skips explore

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to explore first
- **THEN** the skill skips explore and proceeds to create the issue branch and implement

### Requirement: Branch then implement then pause then draft PR

On every run that will implement, the skill MUST:

1. Create local branch `issue-<issue_number>-<slug>` from `main`
2. Implement in the working tree (MUST NOT auto-commit; MUST NOT open a draft PR in this step)
3. **Pause** until the user confirms after reviewing (they commit/push)
4. On continue: ensure a **draft** PR when the branch tip has real commits ahead of `main` (MUST NOT use empty bootstrap
   commits)

Early exits that never implement MAY skip this cadence.

#### Scenario: Branch before implement

- **WHEN** the run will implement after explore (or after skipping explore)
- **THEN** the skill creates `issue-<issue_number>-<slug>` from `main` before writing product code
- **AND** it does not open a draft PR yet
- **AND** it does not auto-commit

#### Scenario: Implement pause before draft PR

- **WHEN** implementation for the current slice is done
- **THEN** the skill stops for the user to review/commit/push
- **AND** it does not open a draft PR until the user confirms

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
in-skill explore when required → create issue branch → implement → pause → draft PR, and that `/issue-fixer` does not
run OpenSpec.

#### Scenario: Contributor reads issue-fixer docs

- **WHEN** a contributor opens `docs/issue-fixer.md`
- **THEN** they learn explore is in-skill when required
- **AND** they learn the branch → implement → pause → draft PR cadence
- **AND** they learn `/issue-fixer` does not run OpenSpec
