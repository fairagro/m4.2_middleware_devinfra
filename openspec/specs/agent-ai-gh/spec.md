# agent-ai-gh Specification

## Purpose

Deterministic GitHub and git plumbing for agent skills: JSON in/out via a small CLI, no AI review policy encoded as
code.

## Requirements

### Requirement: CLI package under scripts/ai

The repository MUST provide a Python CLI under `scripts/ai/` as a **uv workspace member** of the repo-root
`pyproject.toml` (editable install into the root `.venv` via `uv sync`). Agents MUST be able to run it with `uv` from
the repo root as `uv run m42-ai …` (equivalent: `uv run --project scripts/ai m42-ai …`). Runtime MUST use `gh` (and
`git` where needed) from `PATH` for auth and GitHub/git operations — MUST NOT introduce a second credential model.
Host-environment policy (Linux Dev Container / GHA Linux) MUST remain outside the CLI (fixer policy only).

#### Scenario: Agent invokes review-open

- **WHEN** an agent runs `uv run m42-ai review-open --pr <n>` (or
  `uv run --project scripts/ai m42-ai review-open --pr <n>`)
- **THEN** the CLI performs one GraphQL fetch via `gh` and prints shaped JSON to stdout
- **AND** it does not prompt for a separate token store

### Requirement: review-open shapes open AI work

`review-open` MUST emit JSON including: PR number/url, AI review round count, unresolved AI review threads (first
comment author matching Copilot/Bugbot/Cursor heuristics), **every** AI review body with heuristically extracted
suppressed / summary-only findings (`ai_reviews`, `summary_only_findings`), and a convenience `latest_ai_review`, plus
the PR head branch name after successful checkout. Resolved threads and non-AI threads MUST be omitted from the
unresolved list. Round count and AI-review lists MUST include only **submitted** reviews (non-null `submittedAt`, state
not `PENDING`). Summary-only findings MUST NOT be limited to the single latest AI review (a later Bugbot/Cursor
submission MUST NOT hide earlier Copilot suppressed comments). Only the latest **unanswered** suppressed AI review
contributes to `summary_only_findings` (at most one open summary review); a triage reply (`Fixed in` / `Dismissed.` /
`Follow-up:`, optionally with `#pullrequestreview-<id>`) after a suppressed review MUST mark it answered. Only
**submitted** non-AI review bodies count as such triage replies (PENDING / unsubmitted drafts MUST be ignored). An
optional `--review-id` MAY force that review’s suppressed items into the open set for permalink triage. When GraphQL
returns a null `pullRequest`, the CLI MUST fail with a clear error naming owner/repo/PR. Summary-only findings MUST be
marked non-resolvable.

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** only the open AI thread appears under unresolved AI threads
- **AND** round_count counts AI review submissions only

#### Scenario: Pending AI reviews are excluded

- **WHEN** GraphQL includes an AI review with null `submittedAt` or state `PENDING`
- **THEN** that review is omitted from `round_count` and `ai_reviews`
- **AND** it does not affect suppressed-review selection

#### Scenario: Pending non-AI draft reviews do not answer suppressed findings

- **WHEN** GraphQL includes a non-AI review with state `PENDING` (or null `submittedAt`) whose body looks like a triage
  reply (`Fixed in` / `Dismissed.` / `Follow-up:`)
- **THEN** that draft MUST NOT mark any suppressed AI review as answered
- **AND** submitted non-AI triage review bodies and issue comments continue to mark suppressed reviews answered as
  before

### Requirement: review-open ensures PR head checkout

Before emitting open-work JSON, `review-open` MUST resolve the PR head ref name, ensure the local checkout is that
branch (fetch + checkout when needed), and include the checked-out branch name in the JSON (e.g. `head_ref` /
`current_branch`). When the working tree/index is dirty and the current branch is **not** the PR head, the CLI MUST
refuse with a clear error JSON and non-zero exit (matching `issue-branch` cleanliness intent for wrong-branch work).
Dirty state **on** the PR head MUST be allowed. When the head cannot be checked out, the CLI MUST fail closed with a
clear error JSON (no partial silent continue on another branch).

#### Scenario: Wrong-branch dirty refuses

- **WHEN** `review-open` runs and the working tree is dirty on a branch other than the PR head
- **THEN** the process exits non-zero with clear error JSON
- **AND** it does not change the current branch

#### Scenario: Checkout succeeds and JSON includes head

- **WHEN** `review-open` runs on a clean tree (or dirty tree already on the PR head) and the PR head is checkoutable
- **THEN** the local checkout is the PR head branch
- **AND** the emitted JSON includes that branch name
- **AND** open-work shaping still runs as before

### Requirement: review-reply and review-resolve

The CLI MUST support posting an `in_reply_to` pull-review comment, posting a PR conversation comment for summary-only
items, and resolving a review thread by GraphQL thread id. Multiline bodies MUST be sent safely (not broken by shell
`-f` escaping).

#### Scenario: Reply uses JSON input body

- **WHEN** `review-reply` is invoked with a multiline body
- **THEN** the CLI posts via `gh api` using structured JSON input
- **AND** the full body is preserved

### Requirement: issue-create

`issue-create` MUST create a GitHub issue with exactly one org issue type and allowlisted triage labels: required
`severity:*` and `cost:*`, and optional `practicality:*` (omit when there is no defect path). It MUST ensure missing
allowlisted labels it will attach are created. Optional `--parent` MUST attach a native sub-issue. Fallback to a linked
create MUST occur only when no issue URL was produced; MUST NOT create a second issue after a partial success. Success
JSON MUST always include `partial_failure` (false on full success; true on degraded / partial outcomes such as parent
fallback or post-create errors with an existing URL). When `gh issue create --parent` exits non-zero, the CLI MUST
inspect **both** stdout and stderr for an issue URL before any linked fallback create. When that create returns an issue
URL but non-zero status (parent attach failed after create), JSON MUST set `relation` to `linked` (not
`sub-of #<parent>`), keep `partial_failure` true, record `parent_error`, and set `parent_fallback` false when no second
create ran. `relation` MUST be `sub-of #<parent>` only when parent attach succeeded. `ensure_labels` MUST list existing
labels with a high enough limit (or equivalent) so allowlisted labels past the default page size are not treated as
missing.

#### Scenario: Parent failure without URL falls back once

- **WHEN** create with `--parent` fails and no issue URL was returned
- **THEN** the CLI performs one linked create and reports the parent error
- **AND** it does not invent a third create path
- **AND** JSON `relation` is `linked` and `parent_fallback` is true

#### Scenario: Parent failure with URL on stdout reports linked

- **WHEN** create with `--parent` exits non-zero but an issue URL appears on stdout or stderr
- **THEN** the CLI does not perform a second create
- **AND** JSON `relation` is `linked`, `partial_failure` is true, `parent_fallback` is false, and `parent_error` is set

### Requirement: issue-start

`issue-start` MUST, on a clean working tree/index: ensure branch `issue-<n>-<slug>` exists (create from `main` if needed
after fetch + fast-forward pull of the base), refuse when `HEAD` is not ahead of the base, push the tip, and open a
draft PR whose body includes `Fixes #<n>`. It MUST NOT create empty bootstrap commits. It MUST NOT mark the PR ready.
The draft PR body MUST NOT include tool marketing footers such as “Made with Cursor”. Fetch + fast-forward pull of the
base branch MUST succeed before creating a missing issue branch (MUST NOT ignore pull failures).

#### Scenario: Dirty tree refuses issue-start

- **WHEN** `issue-start` is invoked with a dirty working tree or index
- **THEN** it exits non-zero without creating a branch or PR

#### Scenario: Tip equals base refuses issue-start

- **WHEN** `issue-start` is invoked and `HEAD` has no commits ahead of the base
- **THEN** it exits non-zero without creating an empty commit or opening a PR

#### Scenario: issue-start PR body has no Cursor footer

- **WHEN** `issue-start` opens a draft PR
- **THEN** the body contains `Fixes #<n>`
- **AND** it does not contain “Made with Cursor”

### Requirement: auth-status

`auth-status` MUST call `gh auth status --json hosts` (or equivalent) and print shaped JSON including `ok`, `hostname`,
`logged_in`, `login`, `token_source`, and `error`. Exit code MUST be `0` when `ok` is true and non-zero otherwise. MUST
NOT introduce a second credential model.

#### Scenario: Missing host is not ok

- **WHEN** `auth-status` runs and the requested hostname has no auth entry
- **THEN** JSON has `ok: false` and a non-empty `error`
- **AND** the process exits non-zero

### Requirement: issue-view

`issue-view` MUST fetch an issue and print JSON including `number`, `title`, `url`, `body`, `state`, `issue_type`
(nullable), `labels`, `triage` (`severity` / `practicality` / `cost` extracted from allowlisted label names when
present), and `author`.

#### Scenario: Triage labels extracted

- **WHEN** `issue-view` runs on an issue with `severity:medium`, `practicality:high`, and `cost:cheap` labels
- **THEN** `triage.severity` is `severity:medium`
- **AND** `triage.practicality` is `practicality:high`
- **AND** `triage.cost` is `cost:cheap`

### Requirement: issue-branch and branch-ahead

`issue-branch` MUST, on a clean working tree/index: ensure `issue-<n>-<slug>` exists (create from base after fetch +
fast-forward pull when missing), check it out, and MUST NOT commit, push, or open a PR. `branch-ahead` MUST fetch
`origin/<base>` before counting, print JSON with `base`, `upstream` (`origin/<base>`), `current_branch`, `ahead`, and
`ok` (`true` iff `ahead > 0`), and MUST exit non-zero when not ahead.

#### Scenario: issue-branch creates without PR

- **WHEN** `issue-branch` runs and the local issue branch is missing
- **THEN** it creates and checks out `issue-<n>-<slug>` from the base
- **AND** it does not push or open a PR

#### Scenario: branch-ahead exit code

- **WHEN** `branch-ahead` runs and `HEAD` equals the base tip
- **THEN** JSON has `ok: false` and `ahead: 0`
- **AND** the process exits non-zero

### Requirement: pr-strip-footer

`pr-strip-footer` MUST fetch a PR body, remove trailing tool marketing footers such as “Made with Cursor” / “Made with
[Cursor](…)”, and edit the PR only when the body changed. JSON MUST include `changed` and the resulting `body`.

#### Scenario: Footer stripped when present

- **WHEN** `pr-strip-footer` runs on a PR whose body ends with a Cursor marketing footer
- **THEN** the edited body no longer contains that footer
- **AND** JSON reports `changed: true`

#### Scenario: Clean body is a no-op

- **WHEN** `pr-strip-footer` runs on a PR body without a marketing footer
- **THEN** it does not call `gh pr edit`
- **AND** JSON reports `changed: false`

### Requirement: code-review-context shapes local or PR diff metadata

`m42-ai` MUST provide a command (e.g. `code-review-context`) that prints JSON for `/code-review` mechanical setup:
resolved base ref (default `main`), HEAD / PR head identity, changed file paths, and optional short diff stats. When
`--pr <n>` (or equivalent) is given, it MUST resolve the PR head and include `pr` number/url in the JSON. It MUST NOT
embed AI review policy or finding judgments. Large unified diffs MAY be omitted or truncated with a clear flag — the
agent reads files as needed.

#### Scenario: Local context without PR

- **WHEN** an agent runs `uv run --project scripts/ai m42-ai code-review-context --base main`
- **THEN** stdout JSON includes base, head, and changed paths for merge-base(base, HEAD)...HEAD
- **AND** it does not call GitHub unless a PR flag is supplied

#### Scenario: PR context includes pr fields

- **WHEN** an agent runs `m42-ai code-review-context --pr <n>`
- **THEN** JSON includes `pr` number/url and the PR head identity
- **AND** changed paths reflect that PR’s diff vs its base

### Requirement: code-review-report-write and code-review-publish

`m42-ai` MUST provide a command that writes a Markdown report body to a deterministic `/tmp` path (e.g.
`/tmp/code-review-<slug>-<utc>.md`) and prints JSON including that path.

`m42-ai` MUST provide a publish command that, given `--pr` and `--body-file` (or equivalent), submits a Pull Request
Review with event **COMMENT** via `gh pr review --comment` (or equivalent). It MUST NOT approve or request changes by
default. When `--pr` is omitted, publish MUST be a no-op for GitHub and succeed after the report file exists (local-only
path). On review-submit failure with auth present, the command MAY fall back to a single PR conversation comment and
MUST report which channel was used in JSON.

#### Scenario: Write report under /tmp

- **WHEN** an agent runs `m42-ai code-review-report-write --body-file -` (or `--body`) with review Markdown
- **THEN** the file is created under `/tmp` with the documented naming pattern
- **AND** JSON includes the absolute path

#### Scenario: Publish COMMENT review for a PR

- **WHEN** an agent runs `m42-ai code-review-publish --pr <n> --body-file <path>` with working `gh` auth
- **THEN** GitHub receives a Pull Request Review with COMMENT event whose body matches the file
- **AND** JSON reports the publish channel as a formal review

#### Scenario: Local publish skips GitHub

- **WHEN** `code-review-publish` runs without `--pr`
- **THEN** it does not call `gh pr review` or create a PR comment
- **AND** exit status is success when the report path is valid

### Requirement: Fixture tests without live GitHub

Unit tests MUST cover JSON shaping/filtering with recorded fixtures and MUST NOT call live GitHub in CI.

#### Scenario: pytest uses fixtures only

- **WHEN** `uv run pytest` runs in CI (tests under `scripts/ai/tests`)
- **THEN** shaping tests pass using checked-in fixtures
- **AND** no network GitHub API is required for those tests

### Requirement: Agent CLI README documents workspace and consumer layouts

`scripts/ai/README.md` MUST document both layouts:

1. **Devinfra (workspace member):** `scripts/ai` is a `tool.uv.workspace` member of the repo-root `pyproject.toml`;
   preferred invoke `uv run m42-ai …` after root `uv sync`; tests via root `uv run pytest` when so configured.
2. **Product consumers:** by design `scripts/ai` is **not** in the product root workspace; invoke with
   `uv run --project scripts/ai m42-ai …` (and document the matching test command, e.g.
   `uv run --project scripts/ai pytest`).

The README MUST NOT imply that product repos use root-workspace membership solely because Devinfra does. Both layouts
MUST remain valid for their respective repos.

#### Scenario: Product adopter reads Run / Tests sections

- **WHEN** a contributor in a product repo opens synced `scripts/ai/README.md`
- **THEN** they find `--project scripts/ai` as the primary consumer invoke (or clearly labeled consumer path)
- **AND** they find Devinfra workspace / root `uv run` documented as the Devinfra layout
- **AND** test instructions match each layout

### Requirement: Synced skills prefer portable m42-ai invoke

Synced first-party agent skills (`issue-fixer`, `create-issue`, `review-fixer`, `code-review`) and their thin docs MUST
document `uv run --project scripts/ai m42-ai …` as the primary invoke. They MAY note that bare `uv run m42-ai …` works
only when `scripts/ai` is a root uv workspace member (Devinfra). They MUST NOT present bare `uv run m42-ai` as the only
or primary form for product consumers.

#### Scenario: Product agent follows issue-fixer skill

- **WHEN** an agent in a product checkout follows a synced fixer skill to run `m42-ai`
- **THEN** the skill shows `uv run --project scripts/ai m42-ai …` as the primary command
- **AND** it does not require root-workspace membership of `scripts/ai`

#### Scenario: Product agent follows code-review skill

- **WHEN** an agent in a product checkout follows `/code-review` to run helpers
- **THEN** the skill shows `uv run --project scripts/ai m42-ai …` as the primary command
- **AND** it does not require root-workspace membership of `scripts/ai`

### Requirement: scripts/ai pytest works with --project

`scripts/ai` MUST declare a test dependency (or default dependency group) such that `uv run --project scripts/ai pytest`
succeeds in a clean checkout that uses `--project scripts/ai` (product layout).

#### Scenario: Consumer runs scripts/ai pytest

- **WHEN** a contributor runs `uv run --project scripts/ai pytest` after syncing `scripts/ai`
- **THEN** pytest is available without adding product-local deps to the root workspace
- **AND** fixture tests under `scripts/ai/tests` can be collected
