# review-fixer Specification

## Purpose

Defines the canonical `/review-fixer` Fixer skill and thin Cursor/Copilot entrypoints that triage unresolved PR review
threads (any author) and finder summary-only findings using the shared AI review policy.

## Requirements

### Requirement: review-fixer skill is canonical here

The repository MUST provide `.agents/skills/review-fixer/SKILL.md` as the Fixer procedure for shared consumers. The
skill MUST treat `docs/ai_review_policy.md` as the decision source of truth, process **all unresolved review threads**
(any author) from `review-open` plus finder summary-only / suppressed findings (Copilot/Bugbot/Cursor heuristics **and**
`/code-review` marked COMMENT bodies), unless a specific review URL scopes the run, and MUST NOT commit or push. When
any finding is `fix`, the skill MUST use two phases: local fixes plus dismiss/follow-up replies first; `Fixed in <sha>`
only after the user has committed.

#### Scenario: Agent runs /review-fixer with a PR number

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs fetching open review work once via `m42-ai review-open` and triaging unresolved threads
  (any author) plus summary-only / suppressed / code-review findings from that JSON
- **AND** resolved threads are not re-triaged

#### Scenario: Agent pauses for user commit before Fixed replies

- **WHEN** triage yields at least one `fix` action
- **THEN** the skill applies local code changes without committing
- **AND** posts dismiss/follow-up replies in that first phase
- **AND** waits for a user-created commit SHA before posting `Fixed in <sha>.` and resolving those threads

### Requirement: Auth uses shared gh wrapper and conventions

The skill's Auth section MUST direct agents to `scripts/bin/gh` (on `PATH` in the Dev Container) and personal-token
paths from path conventions (`/commandhistory/tokens.env`). It MUST NOT hard-code a product slug such as
`middleware-api` or a product-specific bashhistory volume name.

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

### Requirement: Fetch open work via review-open CLI

When a PR is known, `/review-fixer` MUST start from `uv run --project scripts/ai m42-ai review-open --pr <n>` (or
equivalent), which establishes the PR head checkout and returns shaped open-work JSON. The agent MUST triage that JSON
and MUST NOT dump the raw GraphQL payload into the model as the primary fetch path. Replies and resolves SHOULD use
`m42-ai review-reply` / `review-resolve` when the CLI is present (documented with the same portable
`--project scripts/ai` form). Bare `uv run m42-ai …` MAY be noted as valid only when `scripts/ai` is a root workspace
member.

#### Scenario: review-fixer starts from review-open JSON

- **WHEN** the user runs `/review-fixer` with a PR number
- **THEN** the skill instructs invoking `uv run --project scripts/ai m42-ai review-open` first
- **AND** triage uses `unresolved_ai_threads` (all unresolved authors) and summary-only / suppressed / code-review
  fields from that JSON
- **AND** the skill treats successful `review-open` as having checked out the PR head before any local `fix` edits

### Requirement: Ensure PR head before local fix edits

When a PR number or URL is known, `/review-fixer` MUST treat `m42-ai review-open` as the **first hard gate** before any
triage checklist, GitHub reply, or local `fix` edit. The skill MUST instruct agents to invoke
`uv run --project scripts/ai m42-ai review-open --pr <n>` (or equivalent) as the first action and MUST NOT proceed
unless the CLI exits 0 with `ok` / `pr_head_ok` true (checkout established by plumbing).

When `review-open` fails closed, the skill MUST instruct agents to **stop immediately**, surface the structured CLI JSON
(`error_code`, `error`, `agent_action: stop`) to the user, and MUST NOT stash, force-checkout, or otherwise improvise
around the failure. The skill MUST NOT silently switch back to a previous branch after a failed or empty open-work run.
Gate semantics (dirty wrong branch vs dirty on head, checkout failure codes) MUST live in the CLI, not as agent-side
heuristics.

Dirty working tree **on** the PR head MUST remain allowed (matching CLI). Paste-only triage without a PR MUST NOT
require checkout.

#### Scenario: PR-scoped run checks out via review-open first

- **WHEN** the user invokes `/review-fixer` with a PR number or URL
- **THEN** the skill instructs starting with `uv run --project scripts/ai m42-ai review-open --pr <n>` as the first
  action
- **AND** triage and local `fix` file edits are deferred until that command exits 0 with `pr_head_ok` true

#### Scenario: Checkout failure stops without improvisation

- **WHEN** `review-open` exits non-zero with `agent_action: stop` (e.g. `error_code` `dirty_wrong_branch`)
- **THEN** the skill instructs stopping and showing the CLI JSON to the user
- **AND** it forbids stash/checkout workarounds and silent return to the previous branch

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

### Requirement: Never modify synced paths in consumer checkouts

The `/review-fixer` skill MUST instruct agents never to modify paths listed in `docs/synced-paths.yaml` (or matching
globs) when running in a **product consumer** checkout. On a finding whose primary path is synced, the skill MUST NOT
choose action `fix` against that synced tree. Instead it MUST:

- use action `follow-up` (via create-issue against **Devinfra**, or a clear Devinfra-targeted follow-up) when the
  finding is correct for shared content and severity is Medium or higher, or the finding is Risk, or it is a known
  seen-in-the-wild shared bug; **or**
- use action `dismiss` with reason that the path is synced and must be edited upstream in Devinfra / wait for sync, when
  the item is a Low nit or otherwise not follow-up-worthy; **or**
- use action `fix` only on an **explicit product-local overlay** path documented in the allowlist (never by editing
  `.global` / synced trees).

Phase-1 triage output MUST label such items with existing actions (`follow-up` / `dismiss` / overlay `fix`) and a clear
reason that names the synced-path rule (no new action enum). After the run, the working tree MUST NOT contain dirty
edits under synced paths from fixer work. When `/review-fixer` runs **inside this Devinfra repository**, synced-path
files are the local source of truth and MAY be fixed here like any other in-repo path.

#### Scenario: Synced-path finding in a product PR is not fixed locally

- **WHEN** `/review-fixer` triages a correct cheap finding on `scripts/ai/README.md` (or another allowlisted synced
  path) in a product consumer PR
- **THEN** the skill does not apply a local patch to that synced file
- **AND** the phase-1 action is `follow-up` (Devinfra) or `dismiss` per the Medium+/Risk/seen-in-the-wild gate
- **AND** the working tree has no fixer-introduced dirty edits under that synced path

#### Scenario: Documented overlay may still be fixed in the consumer

- **WHEN** a finding targets a documented product-local overlay (e.g. `docs/surface-quality-bar.md`)
- **THEN** the skill MAY choose `fix` on that overlay path
- **AND** it MUST NOT edit the synced `.global` counterpart to satisfy the finding

#### Scenario: Devinfra checkout may fix shared content

- **WHEN** `/review-fixer` runs on a PR in the Devinfra repository itself
- **THEN** findings on allowlisted shared paths MAY be fixed in that checkout
- **AND** the consumer synced-path hard rule does not apply
