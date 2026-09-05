# agent-ai-gh Specification

## Purpose

Deterministic GitHub and git plumbing for agent skills: JSON in/out via a small CLI, no AI review policy encoded as
code.

## Requirements

### Requirement: CLI package under scripts/ai

The repository MUST provide a Python CLI under `scripts/ai/` runnable with `uv` (e.g.
`uv run --project scripts/ai m42-ai …`). Runtime MUST use `gh` (and `git` where needed) from `PATH` for auth and
GitHub/git operations — MUST NOT introduce a second credential model. Host-environment policy (Linux Dev Container / GHA
Linux) MUST remain outside the CLI (fixer policy only).

#### Scenario: Agent invokes review-open

- **WHEN** an agent runs `uv run --project scripts/ai m42-ai review-open --pr <n>`
- **THEN** the CLI performs one GraphQL fetch via `gh` and prints shaped JSON to stdout
- **AND** it does not prompt for a separate token store

### Requirement: review-open shapes open AI work

`review-open` MUST emit JSON including: PR number/url, AI review round count, unresolved AI review threads (first
comment author matching Copilot/Bugbot/Cursor heuristics), **every** AI review body with heuristically extracted
suppressed / summary-only findings (`ai_reviews`, `summary_only_findings`), and a convenience `latest_ai_review`.
Resolved threads and non-AI threads MUST be omitted from the unresolved list. Round count and AI-review lists MUST
include only **submitted** reviews (non-null `submittedAt`, state not `PENDING`). Summary-only findings MUST NOT be
limited to the single latest AI review (a later Bugbot/Cursor submission MUST NOT hide earlier Copilot suppressed
comments). Only the latest **unanswered** suppressed AI review contributes to `summary_only_findings` (at most one open
summary review); a triage reply (`Fixed in` / `Dismissed.` / `Follow-up:`, optionally with `#pullrequestreview-<id>`)
after a suppressed review MUST mark it answered. An optional `--review-id` MAY force that review’s suppressed items into
the open set for permalink triage. When GraphQL returns a null `pullRequest`, the CLI MUST fail with a clear error
naming owner/repo/PR. Summary-only findings MUST be marked non-resolvable.

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** only the open AI thread appears under unresolved AI threads
- **AND** round_count counts AI review submissions only

#### Scenario: Pending AI reviews are excluded

- **WHEN** GraphQL includes an AI review with null `submittedAt` or state `PENDING`
- **THEN** that review is omitted from `round_count` and `ai_reviews`
- **AND** it does not affect suppressed-review selection

### Requirement: review-reply and review-resolve

The CLI MUST support posting an `in_reply_to` pull-review comment, posting a PR conversation comment for summary-only
items, and resolving a review thread by GraphQL thread id. Multiline bodies MUST be sent safely (not broken by shell
`-f` escaping).

#### Scenario: Reply uses JSON input body

- **WHEN** `review-reply` is invoked with a multiline body
- **THEN** the CLI posts via `gh api` using structured JSON input
- **AND** the full body is preserved

### Requirement: issue-create

`issue-create` MUST create a GitHub issue with exactly one org issue type and allowlisted triage labels (`severity:*`,
`practicality:*`, `cost:*`), ensuring missing allowlisted labels are created. Optional `--parent` MUST attach a native
sub-issue. Fallback to a linked create MUST occur only when no issue URL was produced; MUST NOT create a second issue
after a partial success. Success JSON MUST always include `partial_failure` (false on full success; true on degraded /
partial outcomes such as parent fallback or post-create errors with an existing URL). When `gh issue create --parent`
exits non-zero, the CLI MUST inspect **both** stdout and stderr for an issue URL before any linked fallback create.
`ensure_labels` MUST list existing labels with a high enough limit (or equivalent) so allowlisted labels past the
default page size are not treated as missing.

#### Scenario: Parent failure without URL falls back once

- **WHEN** create with `--parent` fails and no issue URL was returned
- **THEN** the CLI performs one linked create and reports the parent error
- **AND** it does not invent a third create path

### Requirement: issue-start

`issue-start` MUST, on a clean working tree/index: ensure branch `issue-<n>-<slug>` exists (create from `main` if
needed after fetch + fast-forward pull of the base), refuse when `HEAD` is not ahead of the base, push the tip, and open
a draft PR whose body includes `Fixes #<n>`. It MUST NOT create empty bootstrap commits. It MUST NOT mark the PR ready.
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

`issue-view` MUST fetch an issue and print JSON including `number`, `title`, `url`, `body`, `state`, `issue_type` (nullable),
`labels`, `triage` (`severity` / `practicality` / `cost` extracted from allowlisted label names when present), and
`author`.

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

### Requirement: Fixture tests without live GitHub

Unit tests MUST cover JSON shaping/filtering with recorded fixtures and MUST NOT call live GitHub in CI.

#### Scenario: pytest uses fixtures only

- **WHEN** `uv run --project scripts/ai --extra dev pytest` runs in CI
- **THEN** shaping tests pass using checked-in fixtures
- **AND** no network GitHub API is required for those tests
