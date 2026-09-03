# Review Fixer — Delta

## Purpose

Defines the canonical `/review-fixer` Fixer skill and thin Cursor/Copilot entrypoints that triage Copilot and Bugbot PR
review comments using the shared AI review policy.

## ADDED Requirements

### Requirement: review-fixer skill is canonical here

The repository MUST provide `.agents/skills/review-fixer/SKILL.md` as the Fixer procedure for shared consumers. The
skill MUST treat `docs/ai_review_policy.md` as the decision source of truth, process open Copilot/Bugbot work only
unless a specific review URL is given, and MUST NOT commit or push unless the user asks.

#### Scenario: Agent runs /review-fixer with a PR number

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs fetching open AI review work once and triaging only unresolved AI threads plus
  summary-only / suppressed findings from the latest AI review body
- **AND** resolved threads are not re-triaged

### Requirement: Auth uses shared gh wrapper and conventions

The skill's Auth section MUST direct agents to `scripts/bin/gh` (on `PATH` in the Dev Container) and personal-token
paths from path conventions (`/commandhistory/tokens.env` or `~/.config/<git-repo-name>/tokens.env`). It MUST NOT
hard-code a product slug such as `middleware-api` or a product-specific bashhistory volume name.

#### Scenario: Missing token without TTY

- **WHEN** `gh` cannot obtain `GH_TOKEN` and there is no TTY for prompting
- **THEN** the skill tells the agent to skip GitHub writes, print intended replies, and point at
  `./scripts/set-dev-tokens.sh`

### Requirement: Supported environment cites principles.global.md

When dismissing unsupported-host findings (macOS, Windows, Homebrew, unofficial bare Linux), the skill MUST quote
`openspec/principles.global.md` Supported development environment (not only a product-local `principles.md`).

#### Scenario: Fixer dismisses Homebrew PATH noise

- **WHEN** a finder comments on Homebrew or macOS host PATH breakage
- **THEN** the skill's decision path dismisses with practicality None citing `openspec/principles.global.md`

### Requirement: Follow-up issue Markdown is inline

When opening at most one follow-up issue for Medium+ deferred items, the skill MUST include an inline GitHub Markdown
body template (title pattern, bullets with path / severity / practicality / why not this PR). It MUST NOT require
`.agents/skills/create-issue/` to be present.

#### Scenario: Follow-up without create-issue skill

- **WHEN** the fixer defers at least one Medium+ item and create-issue is not installed
- **THEN** the skill still specifies how to create one follow-up issue with a Markdown body
- **AND** Low nits still do not become issues

### Requirement: Cursor command and Copilot prompt entrypoints

The repository MUST provide `.cursor/commands/review-fixer.md` and `.github/prompts/review-fixer.prompt.md` that point
agents at the review-fixer skill and `docs/ai_review_policy.md`, summarizing open-work-only triage and no commit/push
unless asked.

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
