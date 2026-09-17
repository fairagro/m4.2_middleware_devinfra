## ADDED Requirements

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

## MODIFIED Requirements

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
