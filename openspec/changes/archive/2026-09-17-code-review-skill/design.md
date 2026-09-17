## Context

See `proposal.md` for motivation ([#171](https://github.com/fairagro/m4.2_middleware_devinfra/issues/171) /
[#140](https://github.com/fairagro/m4.2_middleware_devinfra/issues/140)). Today `/review-fixer` consumes external AI
review threads; there is no synced skill that _produces_ a first-party critical review. `m42-ai` already wraps `gh` for
fixer/issue flows. `gh pr review --comment -F <file>` creates a formal Pull Request Review (COMMENT) without custom
GraphQL — suitable for the locked “formal review if cheap” preference.

## Goals / Non-Goals

**Goals:**

- One skill + thin entrypoints mirroring create-issue / review-fixer layout
- Mechanical recurrence in `scripts/ai` (context, report path, publish)
- Formal COMMENT review on PRs; `/tmp` for local; auth failure → `/tmp` only
- Explicit anti-overlap with the quality toolchain; judgment-only import cycles

**Non-Goals:**

- Landing vulture / import-linter / pip-audit / griffe (separate Features)
- Auto-fixing findings, auto-approve, or REQUEST_CHANGES by default
- Encoding severity triage policy as Python
- Replacing `/review-fixer`

## Decisions

### D1: Skill name `code-review`

Matches command `/code-review` and issue lock-in. Distinct from `review-fixer`.

### D2: Formal PR Review via `gh pr review --comment`

**Choice:** wrap `gh pr review --comment -F <file>` in `m42-ai code-review-publish`.

**Alternatives:** conversation-only `gh pr comment` (cheaper conceptually but not a Review); raw GraphQL
`addPullRequestReview` (more code, no benefit while `gh` covers COMMENT).

**Fallback:** if review submit fails with auth present, one `gh pr comment` (or existing `review-reply --conversation`)
and report channel in JSON.

### D3: Three small CLI commands (not one mega-command)

1. `code-review-context` — git/gh metadata JSON
2. `code-review-report-write` — persist Markdown under `/tmp`
3. `code-review-publish` — GitHub COMMENT review when `--pr` set

Keeps tests fixture-friendly and matches existing `m42-ai` style (JSON in/out, no policy).

### D4: Diff acquisition

Prefer `git merge-base` + `git diff --name-only` / stats for local; for `--pr`, use `gh pr view` /
`gh pr diff --name-only` (or equivalent) without dumping entire patches into JSON. Agent opens files as needed.

### D5: Sync surfaces

Allowlist: `.agents/skills/code-review/**`, `.cursor/commands/code-review.md`, `.github/prompts/code-review.prompt.md`,
`docs/code-review.md`. `scripts/ai/**` already allowed.

## Risks / Trade-offs

- [Agent still duplicates Ruff nits] → Mitigation: hard anti-dup list in skill + docs; call out vulture/import-linter as
  toolchain-owned when present
- [PR review spam] → Mitigation: one publish per run; skill must not loop publish
- [Huge diffs overwhelm context] → Mitigation: context command returns paths/stats only; agent samples

## Migration Plan

Land on Devinfra; sync delivers skill to products. No consumer code changes required beyond next sync PR.

## Open Questions

None — explore lock-ins applied (name, formal Review when cheap, `scripts/ai` for recurrence).
