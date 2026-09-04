# issue-fixer Specification

## Purpose

Defines the canonical `/issue-fixer` skill and thin Cursor/Copilot entrypoints that triage a GitHub issue, explore
Feature/Refactoring decisions with the user before GitHub writes, open a draft PR from one empty bootstrap commit, and
implement locally without auto-committing fix commits.

## ADDED Requirements

### Requirement: issue-fixer skill is canonical here

The repository MUST provide `.agents/skills/issue-fixer/SKILL.md` as the shared issue-fixer procedure. The skill MUST
accept an issue number or URL, fetch the issue with `gh`, determine org issue type and triage labels when present, and
MUST NOT auto-commit or auto-push fix commits. The skill MUST use Auth guidance matching `/review-fixer` and
`/create-issue` (`scripts/bin/gh`, chat ask for `source ./scripts/set-dev-tokens.sh`, no PAT in chat).

#### Scenario: Agent runs /issue-fixer with an issue number

- **WHEN** the user invokes `/issue-fixer` with an issue number or URL
- **THEN** the skill instructs fetching the issue and triaging type, labels, problem, paths, and acceptance criteria
- **AND** it does not commit or push product fix commits

### Requirement: Explore pause before GitHub writes for Feature and Refactoring

After successful triage and before any branch, empty commit, or PR creation, the skill MUST run an explore pause for org
issue types `Feature` and `Refactoring`: surface open decision threads, recommend defaults as proposals, and wait for
user lock-in, “go”, or “skip explore”. The skill MUST NOT create branches, commits, or PRs during that pause. For `Bug`,
`Security`, and `Task`, explore is required only when actionable criteria are missing, multiple plausible fixes exist,
or the user asks to explore first. `Discussion` MUST NOT proceed to implement by default (see type gates). The skill MAY
offer an OpenSpec proposal when `openspec/` exists and the work is spec-worthy; it MUST NOT require OpenSpec for every
run.

#### Scenario: Feature issue pauses for lock-in

- **WHEN** the issue type is `Feature` and triage finds actionable scope
- **THEN** the skill surfaces open threads and waits for user lock-in or skip-explore
- **AND** it does not create a branch or PR until that pause ends

#### Scenario: Clear Bug skips explore

- **WHEN** the issue type is `Bug` with clear acceptance criteria and a realistic path
- **AND** the user did not ask to explore first
- **THEN** the skill may proceed to the branch/PR workflow without an explore pause

### Requirement: Discussion and Security type gates

For org issue type `Discussion`, the skill MUST NOT create a branch, empty commit, or PR by default; it MUST ask for a
decision or retype and proceed only if the user explicitly requests a concrete implementation. For org issue type
`Security`, the skill MAY implement after triage (and explore when required by the explore rules), but MUST require
clear acceptance criteria and a realistic path, prefer the smallest correct fix, and MUST NOT apply speculative
hardening with no path.

#### Scenario: Discussion does not open a PR

- **WHEN** the issue type is `Discussion` and the user has not explicitly asked to implement a concrete change
- **THEN** the skill does not create a branch or PR
- **AND** it asks for clarification or retype

#### Scenario: Security with clear criteria may implement

- **WHEN** the issue type is `Security` with clear acceptance criteria and a realistic path
- **THEN** the skill may proceed through the normal branch/PR and local-implement path
- **AND** it prefers a narrow MVP over speculative hardening

### Requirement: Empty bootstrap commit and draft PR

After explore (when required) and user go-ahead, the skill MUST create branch `issue-<n>-<slug>` from `main`, create
exactly one empty commit on a clean working tree/index with a standardized message that includes the issue number (e.g.
`Start issue #<n>`), push that commit, and open a **draft** PR with base `main` whose body includes `Fixes #<n>`. The
skill MUST NOT mark the PR ready for review. The skill MUST NOT create fix commits or push fix commits; implementation
stays in the working tree until the user commits and pushes. If GitHub writes fail (auth), the skill MUST skip PR
creation, print a draft, and may still work locally when appropriate.

#### Scenario: Draft PR from empty bootstrap commit

- **WHEN** the agent is ready to open the PR after lock-in
- **THEN** it creates one empty commit on a clean tree, pushes it, and opens a draft PR with `Fixes #<n>` in the body
- **AND** it does not mark the PR ready
- **AND** it does not commit subsequent fix changes

### Requirement: Split rule and create-issue for sub-issues

The skill MUST split only when ≥2 logically independent, independently mergeable blocks exist. Within a block, ~50 new
production lines is a guideline, not a hard cap. When splitting, the skill MUST create at most 3–6 sub-issues by reading
and following `.agents/skills/create-issue/SKILL.md` (one invocation per sub-issue), MUST NOT use a parallel inline-only
`gh issue create` template, and MUST implement only the MVP slice in the current PR while linking sub-issues from the PR
body (and parent issue when practical). Sub-issue types MUST use real org types: `Refactoring` when the slice is
structural; `Task` when the parent is only subdivided; other types when the slice retains that nature. If create-issue
artifacts are missing, the skill MUST report that and print intended create-issue inputs without inventing an
off-allowlist create path.

#### Scenario: Split uses create-issue

- **WHEN** the agent identifies ≥2 independently mergeable blocks and must defer some
- **THEN** it opens each deferred sub-issue via the create-issue procedure
- **AND** the current PR implements only the MVP slice
- **AND** it does not bypass create-issue with an inline-only create template

#### Scenario: No logical split keeps one PR

- **WHEN** the work cannot be divided into independently mergeable blocks
- **THEN** the skill does not force a split solely because the change is large

### Requirement: Cursor command and Copilot prompt entrypoints

The repository MUST provide `.cursor/commands/issue-fixer.md` and `.github/prompts/issue-fixer.prompt.md` that point at
the issue-fixer skill, summarize explore-before-PR for Feature/Refactoring, allow the empty bootstrap commit push for
the draft PR, and state that fix commits are not auto-committed or auto-pushed.

#### Scenario: Slash command loads the skill

- **WHEN** a user runs `/issue-fixer` in Cursor
- **THEN** the command instructs reading `.agents/skills/issue-fixer/SKILL.md`
- **AND** summarizes that Feature/Refactoring explore before branch/PR, and that only the empty bootstrap commit may be
  pushed by the agent

### Requirement: Docs and README index issue-fixer

The repository MUST provide `docs/issue-fixer.md` as a thin human index (workflow, split rule, create-issue handoff,
Auth pointer) linking the skill, and the root `README.md` MUST index `/issue-fixer` in Docs, layout, and synced agent
paths using the same pattern as `/review-fixer` and `/create-issue`.

#### Scenario: Contributor finds issue-fixer docs

- **WHEN** a contributor reads the root README Docs or layout section
- **THEN** they find `/issue-fixer` among shared skills and a link to `docs/issue-fixer.md`
