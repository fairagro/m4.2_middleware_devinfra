# agent-ai-gh Specification

## Purpose

Deterministic GitHub and git plumbing for agent skills: JSON in/out via a small CLI, no AI review policy encoded as
code.

## ADDED Requirements

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
comment author matching Copilot/Bugbot/Cursor heuristics), and the latest AI review body with heuristically extracted
suppressed-comment bullets. Resolved threads and non-AI threads MUST be omitted from the unresolved list.

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** only the open AI thread appears under unresolved AI threads
- **AND** round_count counts AI review submissions only

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
after a partial success.

#### Scenario: Parent failure without URL falls back once

- **WHEN** create with `--parent` fails and no issue URL was returned
- **THEN** the CLI performs one linked create and reports the parent error
- **AND** it does not invent a third create path

### Requirement: issue-start

`issue-start` MUST, on a clean working tree/index: create branch `issue-<n>-<slug>` from `main`, create exactly one
empty commit `Start issue #<n>`, push it, and open a draft PR whose body includes `Fixes #<n>`. It MUST NOT mark the PR
ready.

#### Scenario: Dirty tree refuses issue-start

- **WHEN** `issue-start` is invoked with a dirty working tree or index
- **THEN** it exits non-zero without creating a branch or PR

### Requirement: Fixture tests without live GitHub

Unit tests MUST cover JSON shaping/filtering with recorded fixtures and MUST NOT call live GitHub in CI.

#### Scenario: pytest uses fixtures only

- **WHEN** `uv run --project scripts/ai --extra dev pytest` runs in CI
- **THEN** shaping tests pass using checked-in fixtures
- **AND** no network GitHub API is required for those tests
