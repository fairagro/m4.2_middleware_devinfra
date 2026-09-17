## Purpose

Defines the canonical `/code-review` skill and thin Cursor/Copilot entrypoints that produce a first-party critical
review of a local branch diff or GitHub pull request, without duplicating quality-toolchain findings or replacing
`/review-fixer`.

## ADDED Requirements

### Requirement: code-review skill is canonical here

The repository MUST provide `.agents/skills/code-review/SKILL.md` as the shared first-party review procedure. The skill
MUST review a branch diff (default base `main`) **or** a GitHub PR number/URL using the same checklist. It MUST produce
a structured findings report; it MUST NOT commit, push, or auto-approve. It MUST NOT triage Copilot/Bugbot review
threads (that remains `/review-fixer`).

#### Scenario: Agent runs /code-review on local branch

- **WHEN** the user invokes `/code-review` without a PR reference
- **THEN** the skill reviews `git diff` of merge-base(base, HEAD)...HEAD (default base `main`)
- **AND** it writes the report under `/tmp` via the documented `m42-ai` helper
- **AND** it does not post to GitHub

#### Scenario: Agent runs /code-review with a PR

- **WHEN** the user invokes `/code-review` with a PR number or URL
- **THEN** the skill reviews that PR’s diff using the same checklist as the local path
- **AND** it publishes findings as a formal Pull Request Review comment event when auth succeeds

### Requirement: Review goals and anti-duplication

The skill MUST cover these goals (skip when not applicable to the diff): security (judgment beyond automated scanners),
correctness / missing edge cases, concurrency and races, architecture and simplicity, import graph / cycles
(**judgment-only**), defensive bloat vs missing edges, resource use, dead / unused code, OpenSpec↔code drift **only
where specs exist and the diff touches that surface**, docs↔code drift (weaker severity than spec drift), and test
adequacy for new risks.

The skill MUST NOT restate findings that the quality toolchain already owns: Ruff, mypy, pylint, Bandit, markdownlint,
Prettier, ggshield, CodeQL, Trivy, and (once landed) vulture and import-linter. Format, import sort, line-length, and
type noise that CI already fails MUST be out of scope.

Severity language MUST align with `docs/ai_review_policy.md`. For Medium+ findings the skill MAY offer `/create-issue`
(it MUST NOT auto-create issues unless the user asks).

#### Scenario: Style-only nit is omitted

- **WHEN** a diff only has import-sort or line-length issues already covered by Ruff/Prettier
- **THEN** the skill does not report those as findings
- **AND** it still reviews applicable judgment goals on the same diff

#### Scenario: Spec drift only when specs touch the surface

- **WHEN** the diff changes code with no related OpenSpec requirement in the checkout
- **THEN** the skill does not invent a spec-drift finding solely for missing specs

### Requirement: Publish via formal PR Review or /tmp

When a PR is known and GitHub auth works, the skill MUST publish the report as a GitHub **Pull Request Review** with
event **COMMENT** (not REQUEST_CHANGES / APPROVE) using `m42-ai` (wrapping `gh pr review --comment` or equivalent). The
CLI path MUST remain low-effort — no custom GraphQL review mutation is required when `gh pr review` suffices.

When no PR is known, the skill MUST write the report to a file under `/tmp` (stable naming via `m42-ai`) and MUST NOT
require GitHub writes.

If posting a formal review fails after auth is available, the skill MAY fall back to a single PR conversation comment;
it MUST still retain the `/tmp` report.

The skill MUST NOT auto-LGTM. One publish per run (no silent spam loops).

#### Scenario: Local review writes /tmp only

- **WHEN** `/code-review` runs without a PR reference
- **THEN** `m42-ai` writes `/tmp/code-review-*.md` (or the documented pattern)
- **AND** no `gh pr review` or PR comment is attempted

#### Scenario: PR review posts COMMENT review

- **WHEN** `/code-review` runs with a valid PR and `GH_TOKEN` / `gh` auth is available
- **THEN** the report is submitted as a Pull Request Review with COMMENT event
- **AND** the review body contains the structured findings

### Requirement: Recurring steps use m42-ai

Recurring mechanical steps MUST go through `uv run --project scripts/ai m42-ai …` (portable primary form): at least (1)
shape diff/PR context as JSON, (2) write the report file under `/tmp`, (3) publish the PR Review (or documented
fallback). The skill MUST keep judgment and checklist application in the agent, not encode AI review policy as Python.
Bare `uv run m42-ai …` MAY be noted as valid only when `scripts/ai` is a root workspace member.

#### Scenario: Skill documents portable invoke

- **WHEN** an agent in a product checkout follows `/code-review`
- **THEN** the skill shows `uv run --project scripts/ai m42-ai …` as the primary command form for helpers
- **AND** it does not require root-workspace membership of `scripts/ai`

### Requirement: Auth matches shared gh helpers

The skill's Auth guidance MUST match the shared personal-token helpers: use `scripts/bin/gh` on `PATH` in the Dev
Container; never invent or paste PATs into chat. When there is no TTY and `GH_TOKEN` is missing, for PR publish the
skill MUST ask the user to run `source ./scripts/set-dev-tokens.sh` in a real terminal and wait; if they decline or auth
still fails, it MUST skip GitHub writes and leave the `/tmp` report as the deliverable.

#### Scenario: Missing token without TTY on PR path

- **WHEN** `/code-review` targets a PR and `gh` cannot obtain `GH_TOKEN` and there is no TTY
- **THEN** the skill asks the user (in chat) to source `./scripts/set-dev-tokens.sh` and wait
- **AND** if auth still fails, it keeps the `/tmp` report and does not paste a PAT into chat

### Requirement: Thin command and prompt entrypoints

The repository MUST provide `.cursor/commands/code-review.md` and `.github/prompts/code-review.prompt.md` that point
agents at the code-review skill and summarize local-vs-PR inputs and publish behavior (formal Review vs `/tmp`).

#### Scenario: Cursor command points at skill

- **WHEN** a user invokes the Cursor `/code-review` command
- **THEN** the command file directs the agent to `.agents/skills/code-review/SKILL.md`
- **AND** it does not re-implement the full checklist inline

### Requirement: Sync allowlist and short docs

`docs/synced-paths.yaml` MUST allow `.agents/skills/code-review/**`, the thin command/prompt paths, and
`docs/code-review.md`. The repository MUST provide a short `docs/code-review.md` describing purpose, inputs/outputs,
anti-duplication, and relationship to `/review-fixer`. The root `README.md` Docs/skills index MUST mention
`/code-review` among synced agent paths when other first-party skills are listed there.

#### Scenario: Allowlist covers code-review surfaces

- **WHEN** product-repo sync runs with the updated allowlist
- **THEN** the code-review skill, command, prompt, and docs path are eligible to sync
- **AND** consumers are instructed not to hand-edit those synced trees
