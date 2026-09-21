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

`review-open` MUST emit JSON including: PR number/url, finder review round count, **all unresolved review threads** (any
first-comment author; JSON key MAY remain `unresolved_ai_threads` for compatibility), **every** finder review body —
author matching Copilot/Bugbot/Cursor heuristics **or** body containing the stable `/code-review` marker
`<!-- m42-ai:code-review -->` — with heuristically extracted suppressed / summary-only findings (`ai_reviews`,
`summary_only_findings`), and a convenience `latest_ai_review`, plus the PR head branch name after successful checkout.
Resolved threads MUST be omitted from the unresolved list. Round count and finder-review lists MUST include only
**submitted** finder reviews (non-null `submittedAt`, state not `PENDING`). Summary-only findings MUST NOT be limited to
the single latest finder review (a later Bugbot/Cursor/`code-review` submission MUST NOT hide earlier Copilot suppressed
comments except via the answered-summary selection rule). Only the latest **unanswered** summary finder review
contributes to `summary_only_findings` (at most one open summary review); a triage reply (`Fixed in` / `Dismissed.` /
`Follow-up:`, optionally with `#pullrequestreview-<id>`) after a summary review MUST mark it answered. Only
**submitted** non-finder review bodies count as such triage replies (PENDING / unsubmitted drafts MUST be ignored;
`/code-review` marked bodies MUST NOT count as triage replies). An optional `--review-id` MAY force that review’s
summary items into the open set for permalink triage. When GraphQL returns a null `pullRequest`, the CLI MUST fail with
a clear error naming owner/repo/PR. Summary-only findings MUST be marked non-resolvable. For `/code-review` bodies,
findings MUST be extracted from the Markdown findings table (header row with a `path` column).

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** both the open AI thread and the open human thread appear under unresolved threads
- **AND** the resolved AI thread is omitted
- **AND** round_count counts finder review submissions only
- **AND** Copilot suppressed / summary-only findings remain available when unanswered

#### Scenario: Pending AI reviews are excluded

- **WHEN** GraphQL includes an AI review with null `submittedAt` or state `PENDING`
- **THEN** that review is omitted from `round_count` and `ai_reviews`
- **AND** it does not affect suppressed-review selection

#### Scenario: Pending non-AI draft reviews do not answer suppressed findings

- **WHEN** GraphQL includes a non-AI review with state `PENDING` (or null `submittedAt`) whose body looks like a triage
  reply (`Fixed in` / `Dismissed.` / `Follow-up:`)
- **THEN** that draft MUST NOT mark any suppressed AI review as answered
- **AND** submitted non-finder triage review bodies and issue comments continue to mark suppressed reviews answered as
  before

#### Scenario: Human-login code-review COMMENT is summary-packed

- **WHEN** GraphQL includes a submitted review under a human login whose body starts with `<!-- m42-ai:code-review -->`
  and a findings table with a `path` column
- **THEN** that review is included in `ai_reviews` / `round_count`
- **AND** its table rows appear under `summary_only_findings` when it is the open unanswered summary review
- **AND** those findings are marked non-resolvable

### Requirement: review-open ensures PR head checkout

Before emitting open-work JSON, `review-open` MUST resolve the PR head ref name, ensure the local checkout is that
branch (fetch + checkout when needed), and include `head_ref`, `current_branch`, `ok: true`, and `pr_head_ok: true` in
success JSON. When the working tree/index is dirty and the current branch is **not** the PR head, the CLI MUST refuse
with non-zero exit and structured error JSON including at least `ok: false`, `pr_head_ok: false`,
`error_code: "dirty_wrong_branch"`, `error`, `agent_action: "stop"`, plus `head_ref` / `current_branch` when known.
Dirty state **on** the PR head MUST be allowed. When the head cannot be checked out, the CLI MUST fail closed with
structured error JSON (`error_code` one of `empty_head_ref`, `checkout_failed`, `checkout_branch_mismatch`) — no partial
silent continue on another branch. `agent_action: "stop"` means agents MUST NOT stash, force-checkout, or otherwise
improvise around the failure.

#### Scenario: Wrong-branch dirty refuses

- **WHEN** `review-open` runs and the working tree is dirty on a branch other than the PR head
- **THEN** the process exits non-zero with structured error JSON (`error_code` `dirty_wrong_branch`, `agent_action`
  `stop`)
- **AND** it does not change the current branch

#### Scenario: Checkout succeeds and JSON includes head

- **WHEN** `review-open` runs on a clean tree (or dirty tree already on the PR head) and the PR head is checkoutable
- **THEN** the local checkout is the PR head branch
- **AND** the emitted JSON includes that branch name with `ok` and `pr_head_ok` true
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

`issue-start` MUST, on a clean working tree/index: ensure branch `{channel}/issue-<n>-<slug>` exists (create from `main`
if needed after fetch + fast-forward pull of the base), refuse when `HEAD` is not ahead of the base, push the tip, and
open a draft PR whose body includes `Fixes #<n>`. `{channel}` MUST be one of `build`, `ci`, or `docs` (default `build`
when the caller does not pass a channel). It MUST NOT create empty bootstrap commits. It MUST NOT mark the PR ready. The
draft PR body MUST NOT include tool marketing footers such as “Made with Cursor”. Fetch + fast-forward pull of the base
branch MUST succeed before creating a missing issue branch (MUST NOT ignore pull failures).

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

#### Scenario: issue-start uses channel prefix

- **WHEN** `issue-start` creates a missing branch with `--channel ci`
- **THEN** the branch name is `ci/issue-<n>-<slug>`

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
present), `author`, and `comments` (array of `{author, body, created_at}`, oldest first; empty when none). Comments MUST
come from the issue conversation (same source as `gh issue view --json comments`).

#### Scenario: Triage labels extracted

- **WHEN** `issue-view` runs on an issue with `severity:medium`, `practicality:high`, and `cost:cheap` labels
- **THEN** `triage.severity` is `severity:medium`
- **AND** `triage.practicality` is `practicality:high`
- **AND** `triage.cost` is `cost:cheap`

#### Scenario: Comments included oldest first

- **WHEN** `issue-view` runs on an issue that has two comments with distinct `createdAt` timestamps
- **THEN** JSON `comments` lists both entries with `author`, `body`, and `created_at`
- **AND** the list is ordered oldest → newest

### Requirement: issue-branch and branch-ahead

`issue-branch` MUST, on a clean working tree/index: ensure `{channel}/issue-<n>-<slug>` exists (create from base after
fetch + fast-forward pull when missing), check it out, and MUST NOT commit, push, or open a PR. `{channel}` MUST be one
of `build`, `ci`, or `docs` (default `build`). `branch-ahead` MUST fetch `origin/<base>` before counting, print JSON
with `base`, `upstream` (`origin/<base>`), `current_branch`, `ahead`, and `ok` (`true` iff `ahead > 0`), and MUST exit
non-zero when not ahead.

#### Scenario: issue-branch creates without PR

- **WHEN** `issue-branch` runs and the local issue branch is missing
- **THEN** it creates and checks out `{channel}/issue-<n>-<slug>` from the base
- **AND** it does not push or open a PR

#### Scenario: issue-branch default channel is build

- **WHEN** `issue-branch` runs without an explicit channel
- **THEN** the branch name starts with `build/issue-`

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

### Requirement: CLI supports sync follow-up plumbing

The `m42-ai` CLI (under `scripts/ai/`) MUST provide commands (or a documented equivalent invoke surface) that sync
orchestration can call to:

1. Resolve a Devinfra pull request for a given commit SHA (when one exists).
2. Parse `SYNC-FOLLOWUP: <stable-id>` trailers from a PR body and from that PR’s issue/review comments (stable-id MUST
   be a non-empty token suitable for dedupe keys).
3. Ensure a follow-up GitHub issue exists in a target product repository for a given stable-id: create with org type
   `Task`, triage labels `severity:low` and a documented `cost:*` default, body from a Devinfra-owned template that
   links the Devinfra commit/PR, or reuse an existing **open** issue already keyed to that id (dedupe). MUST NOT create
   a second open issue for the same repo + id.

These commands MUST use `gh` on `PATH` (same auth model as the rest of the CLI). They MUST emit machine-readable JSON
suitable for Actions logging. Dry-run / no-op modes MAY exist for testing but live ensure MUST create or reuse issues
only when explicitly requested.

#### Scenario: Parse trailers from body and comments

- **WHEN** an agent or sync job asks the CLI to collect follow-up ids for a PR that has `SYNC-FOLLOWUP: remove-stubs` in
  the body and another id only in a comment
- **THEN** the CLI reports both distinct ids
- **AND** malformed lines without a stable id are ignored

#### Scenario: Ensure reuses open issue

- **WHEN** ensure runs for product repo R and id `remove-stubs` and an open issue already carries that dedupe key
- **THEN** the CLI returns that issue’s URL/number without creating another open issue

#### Scenario: Ensure creates Task when missing

- **WHEN** ensure runs for product repo R and id `remove-stubs` and no open dedupe match exists
- **THEN** the CLI creates a `Task` issue with `severity:low` and the documented cost label
- **AND** the body links the Devinfra source PR or commit
