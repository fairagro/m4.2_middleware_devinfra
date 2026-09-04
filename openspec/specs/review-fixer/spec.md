# review-fixer Specification

## Purpose

Defines the canonical `/review-fixer` Fixer skill and thin Cursor/Copilot entrypoints that triage Copilot and Bugbot PR
review comments using the shared AI review policy.

## Requirements

### Requirement: review-fixer skill is canonical here

The repository MUST provide `.agents/skills/review-fixer/SKILL.md` as the Fixer procedure for shared consumers. The
skill MUST treat `docs/ai_review_policy.md` as the decision source of truth, process open Copilot/Bugbot work only
unless a specific review URL is given, and MUST NOT commit or push. When any finding is `fix`, the skill MUST use two
phases: local fixes plus dismiss/follow-up replies first; `Fixed in <sha>` only after the user has committed.

#### Scenario: Agent runs /review-fixer with a PR number

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs fetching open AI review work once and triaging only unresolved AI threads plus
  summary-only / suppressed findings from the latest AI review body
- **AND** resolved threads are not re-triaged

#### Scenario: Agent pauses for user commit before Fixed replies

- **WHEN** triage yields at least one `fix` action
- **THEN** the skill applies local code changes without committing
- **AND** posts dismiss/follow-up replies in that first phase
- **AND** waits for a user-created commit SHA before posting `Fixed in <sha>.` and resolving those threads

### Requirement: Auth uses shared gh wrapper and conventions

The skill's Auth section MUST direct agents to `scripts/bin/gh` (on `PATH` in the Dev Container) and personal-token
paths from path conventions (`/commandhistory/tokens.env` or `~/.config/<git-repo-name>/tokens.env`). It MUST NOT
hard-code a product slug such as `middleware-api` or a product-specific bashhistory volume name.

#### Scenario: Missing token without TTY

- **WHEN** `gh` cannot obtain `GH_TOKEN` and there is no TTY for prompting
- **THEN** the skill tells the agent to ask the user (in chat) to run `source ./scripts/set-dev-tokens.sh` in a real
  terminal and wait for confirmation before continuing GitHub writes
- **AND** it MUST NOT ask the user to paste a PAT into chat
- **AND** if the user declines or auth still fails, the agent skips GitHub writes, prints intended replies, and may
  still apply local `fix` changes

### Requirement: Supported environment cites principles.global.md

When dismissing unsupported-host findings (macOS, Windows, Homebrew, unofficial bare Linux), the skill MUST quote
`openspec/principles.global.md` Supported development environment (not only a product-local `principles.md`).

#### Scenario: Fixer dismisses Homebrew PATH noise

- **WHEN** a finder comments on Homebrew or macOS host PATH breakage
- **THEN** the skill's decision path dismisses with practicality None citing `openspec/principles.global.md`

### Requirement: Follow-up issues use create-issue

When opening at most one follow-up issue for Medium+ deferred items, the skill MUST instruct agents to read and follow
`.agents/skills/create-issue/SKILL.md` (org issue type, allowlisted triage labels, body template, Auth). Title MUST be
`Follow-up from PR #<pr_number> AI review`. Low nits MUST NOT become issues. The skill MUST NOT use a separate
inline-only `gh issue create` template that bypasses create-issue.

#### Scenario: Medium+ deferral opens one create-issue follow-up

- **WHEN** the fixer defers at least one Medium+ item
- **THEN** the skill directs opening one issue via the create-issue procedure
- **AND** Low-only nits still do not become issues

#### Scenario: create-issue missing in consumer checkout

- **WHEN** create-issue artifacts are absent
- **THEN** the skill tells the agent to report that and print intended create-issue inputs
- **AND** it still MUST NOT invent off-allowlist labels or a parallel create path

### Requirement: Cursor command and Copilot prompt entrypoints

The repository MUST provide `.cursor/commands/review-fixer.md` and `.github/prompts/review-fixer.prompt.md` that point
agents at the review-fixer skill and `docs/ai_review_policy.md`, summarizing open-work-only triage and that the agent
does not commit or push (user commits; Fixed replies use that SHA).

#### Scenario: Slash command loads the skill

- **WHEN** a user runs `/review-fixer` in Cursor
- **THEN** the command instructs reading `.agents/skills/review-fixer/SKILL.md`
- **AND** using `docs/ai_review_policy.md` as the decision source of truth

### Requirement: README indexes review-fixer

The root `README.md` MUST mention the shared `/review-fixer` artifacts among synced agent paths (skill and/or command)
so consumers know not to diverge locally.

#### Scenario: Consumer finds review-fixer ownership

- **WHEN** a contributor reads the root README layout or Docs section
- **THEN** they learn that review-fixer skill/command/prompt are canonical shared content
