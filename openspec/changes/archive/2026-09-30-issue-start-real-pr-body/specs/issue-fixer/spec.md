## MODIFIED Requirements

### Requirement: Draft PR after real commits via CLI preferred

After the implement-pause confirmation, the skill MUST ensure a **draft** PR exists with `Fixes #<issue_number>` when
the issue branch tip already has commits ahead of `main`. The skill MUST NOT create empty bootstrap commits
(`git commit --allow-empty` or equivalent). Prefer `m42-ai issue-start` when available. Prefer `m42-ai issue-view` for
triage fetch, `m42-ai issue-branch` for the early branch step, `m42-ai branch-ahead` / `m42-ai auth-status` for probes,
and `m42-ai pr-strip-footer` after PR create when a marketing footer may be present. MUST NOT mark the PR ready; MUST
NOT create fix commits. If the tip still equals `main`, the skill MUST stop and ask the user to commit first. PR bodies
MUST NOT include tool marketing footers such as “Made with Cursor”; if injected, the skill MUST strip them before
continuing.

When calling `issue-start`, the skill SHOULD pass a crafted Summary via `--body-file` (or `--body`) with 1–3 bullets
describing the change; if omitted, the CLI default (issue title / commit subjects) is acceptable. The skill MUST NOT
document or rely on a `MVP scope: (fill in)` stub as the intended PR body.

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

#### Scenario: Skill prefers real Summary over fill-in stub

- **WHEN** a contributor or agent follows `/issue-fixer` draft-PR guidance for `issue-start`
- **THEN** the skill documents passing a crafted Summary (`--body-file` / `--body`) or accepting the CLI default
- **AND** it does not present `MVP scope: (fill in)` as the intended body template
