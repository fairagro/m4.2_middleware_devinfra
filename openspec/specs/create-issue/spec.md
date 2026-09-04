# create-issue Specification

## Purpose

Defines the canonical `/create-issue` creator skill and thin Cursor/Copilot entrypoints that open GitHub issues with one
org issue type and triage labels, using shared `gh` authentication, without re-running review-fixer triage.

## Requirements

### Requirement: create-issue skill is canonical here

The repository MUST provide `.agents/skills/create-issue/SKILL.md` as the shared issue-creator procedure. The skill MUST
create issues only (no code changes, no commit/push unless the user asks). It MUST NOT re-run `/review-fixer` triage on
PR review threads. It MUST accept either a PR reference plus a finding summary (optional triage fields) or free-text
“create an issue for …”.

#### Scenario: Agent runs /create-issue with a finding summary

- **WHEN** the user invokes `/create-issue` with a PR number/URL and a finding summary
- **THEN** the skill instructs creating one GitHub issue from that input
- **AND** it does not fetch and re-triage all Copilot/Bugbot threads on the PR

### Requirement: One org issue type and triage labels

The skill MUST pick exactly one GitHub org issue type from: `Bug`, `Security`, `Feature`, `Task`, `Discussion`,
`Refactoring`. It MUST NOT encode kinds as `kind:*` labels. It MUST attach triage labels from these families only:
`severity:blocker|high|medium|low`, `practicality:high|medium|low|none|seen-in-the-wild`, and
`cost:cheap|medium|expensive`. Severity, practicality, and cost definitions MUST cite `docs/ai_review_policy.md`, with
`practicality:seen-in-the-wild` and `cost:medium` documented as issue-oriented extensions.

#### Scenario: Security finding becomes a Security issue

- **WHEN** the user asks to create an issue for credential leakage with severity High
- **THEN** the skill selects issue type `Security`
- **AND** attaches matching allowlisted severity/practicality/cost labels

### Requirement: Create-if-missing allowlisted labels only

Before attaching a triage label, if that label is missing in the target repository and is on the allowlist above, the
skill MUST create it (via `gh`) then attach it. The skill MUST NOT create arbitrary or free-text labels outside the
allowlist.

#### Scenario: First create-issue in a repo without triage labels

- **WHEN** `/create-issue` runs in a repo that lacks `severity:high`
- **AND** the chosen triage includes severity High
- **THEN** the skill creates `severity:high` (and any other missing allowlisted labels it will attach)
- **AND** creates the issue with those labels

### Requirement: Auth matches shared gh helpers

The skill's Auth guidance MUST match the shared personal-token helpers: use `scripts/bin/gh` on `PATH` in the Dev
Container; never invent or paste PATs into chat. When there is no TTY and `GH_TOKEN` is missing, the skill MUST ask the
user (in chat) to run `source ./scripts/set-dev-tokens.sh` in a real terminal and wait; if they decline or auth still
fails, it MUST skip GitHub writes and print the draft title/body/type/labels.

#### Scenario: Missing token without TTY

- **WHEN** `gh` cannot obtain `GH_TOKEN` and there is no TTY for prompting
- **THEN** the skill tells the agent to ask for `source ./scripts/set-dev-tokens.sh` and wait
- **AND** it MUST NOT ask the user to paste a PAT into chat

### Requirement: Prefer issue-create CLI

When creating issues, `/create-issue` MUST prefer `uv run --project scripts/ai m42-ai issue-create` (org type, triage
labels, optional `--parent`) when the CLI is present in the checkout. Raw `gh issue create` remains a documented
fallback only when the CLI is unavailable. Duplicate-create rules (no second create after a produced issue URL) still
apply.

#### Scenario: create-issue documents CLI first

- **WHEN** an agent follows `/create-issue` to open a deferred issue
- **THEN** the skill shows `m42-ai issue-create` as the preferred create path
- **AND** relation `sub-of` maps to `--parent`

### Requirement: Markdown body template and user output

Created issues MUST use a GitHub Markdown body that includes type, triage block, problem, why-not-now, suggested
acceptance criteria, and links when a PR is known. The agent MUST return the issue URL (or “skipped GitHub writes” plus
the draft), the selected issue type, and the attached labels.

#### Scenario: Successful create returns URL and metadata

- **WHEN** issue creation succeeds
- **THEN** the user receives the issue URL, the org issue type, and the label set

### Requirement: review-fixer may invoke create-issue for follow-ups

The skill MUST accept invocation from `/review-fixer` with pre-filled Medium+ deferred items (typical title
`Follow-up from PR #<pr_number> AI review`) without re-running full PR review triage.

#### Scenario: review-fixer hands off a bundled follow-up

- **WHEN** review-fixer requests one follow-up issue with deferred Medium+ findings and triage fields
- **THEN** create-issue creates that issue using its type/label/body rules
- **AND** it does not re-fetch and re-triage all Copilot/Bugbot threads

### Requirement: Cursor command and Copilot prompt entrypoints

The repository MUST provide `.cursor/commands/create-issue.md` and `.github/prompts/create-issue.prompt.md` that point
at the create-issue skill and `docs/ai_review_policy.md` for severity/practicality/cost vocabulary, and MUST list all
six org issue types including `Refactoring`.

#### Scenario: Slash command loads the skill

- **WHEN** a user runs `/create-issue` in Cursor
- **THEN** the command instructs reading `.agents/skills/create-issue/SKILL.md`

### Requirement: Docs index issue types and triage labels

The root README and/or linked docs MUST document the six org issue types and the triage label families (including
create-if-missing allowlist behavior) so consumers know what `/create-issue` expects.

#### Scenario: Contributor looks up create-issue conventions

- **WHEN** a contributor reads the root README Docs or layout section for issue creation
- **THEN** they find the org issue types and triage label families
- **AND** they learn that allowlisted missing labels are created on demand by the skill
