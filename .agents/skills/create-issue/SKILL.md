---
name: create-issue
description: >-
  Creates a GitHub issue with one org issue type and triage labels (severity,
  practicality, cost). Use when the user asks to /create-issue, open a follow-up
  issue from a finding, or file deferred work — not for implementing fixes.
---

# Create issue

Create (and only create) GitHub issues for deferred work or AI-driven discussion requests.

You are a **creator** (not fixer). Do not implement code changes. Do **not** re-run `/review-fixer` triage on PR review
threads.

## Input

Accept any of:

1. A PR number or URL plus a finding summary. The user may include triage fields in plain text:
   - `type: Bug|Security|Feature|Task|Discussion|Refactoring`
   - `severity: Blocker|High|Medium|Low`
   - `practicality: High|Medium|Low|None|seen-in-the-wild`
   - `cost: cheap|medium|expensive`
   - affected `path:` sentences
2. Free text: “please create an issue for …” (no structured triage).

If a PR is identifiable, you may fetch minimal context (e.g. changed files), but do not re-run full review-fixer triage.
Prefer what the user provided.

Do **not** commit or push unless the user asks.

## Auth (`gh`)

`gh` is wrapped (`scripts/bin/gh`, on `PATH` in the Dev Container via `remoteEnv`). Missing `GH_TOKEN` prompts on
`/dev/tty` and is saved to `/commandhistory/tokens.env` in a Dev Container, or `~/.config/<git-repo-name>/tokens.env` on
a local clone (repository name from `origin` — see `docs/conventions.md`). Interactive shells also source
`scripts/dev-tokens.sh` after postCreate (Kombi). Do not read tokens from the git worktree; do not invent them. Never
ask the user to paste a PAT into chat.

**Agent / no TTY:** `/dev/tty` is unavailable in chat, so the wrapper cannot prompt. Before skipping GitHub writes:

1. Tell the user `GH_TOKEN` is missing and that the agent cannot open an interactive prompt here.
2. Ask them to run in a **Dev Container / IDE terminal** (not chat):

   ```bash
   source ./scripts/set-dev-tokens.sh
   ```

   Then reply here when done (or decline).

3. After they confirm, retry `gh` (e.g. `gh auth status`). If auth works, continue with label ensure + issue create.
4. Only if they decline or auth still fails: skip GitHub writes, print the draft title/body/type/labels, and stop.

Label create and issue create need a token that can write issues and labels on the target repo. If label create fails
with a permissions error, say so and suggest creating the allowlisted labels once in the GitHub UI (or broadening the
PAT).

## Decision inputs

Use [`docs/ai_review_policy.md`](../../../docs/ai_review_policy.md) for the core definitions of **severity**,
**practicality**, and **cost**.

### Issue-oriented extensions

- `practicality:seen-in-the-wild` — user provides evidence it already happens in real usage (logs, incidents, reports)
- `cost:medium` — between cheap and expensive for issue planning (review-fixer cost table is only `cheap|expensive`)

### Org issue type (exactly one)

GitHub **Issue Types** (not `kind:*` labels):

| Type          | When                                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| `Security`    | Credential/secret/PII leakage, unsafe authn/authz, or exploitable security weakness                        |
| `Bug`         | Wrong domain result, data loss/silent overwrite, broken API/HTTP contract, ownership/idempotency bypass    |
| `Feature`     | Intended new behaviour / capability                                                                        |
| `Task`        | Bounded follow-up: tech-debt, cleanup, docs, or a small actionable slice that is not a structural redesign |
| `Refactoring` | Multi-module or structural restructure (new abstractions, contract-preserving architecture change)         |
| `Discussion`  | Question, proposal, or ambiguous trade-off without a clear actionable change                               |

Do **not** use `Task` for major structural work — that is `Refactoring`.

### Practicality → label

- `practicality:high` if a realistic path exists in this system (cite the path)
- `practicality:medium|low|none` otherwise
- `practicality:seen-in-the-wild` when evidence is provided

## Triage label allowlist (create-if-missing)

Attach **only** labels from this allowlist. Before `gh issue create`, ensure each label you will attach exists. If
missing, create it with the fixed color/description below (`gh label create`). Never create free-text or off-allowlist
labels.

| Label                           | Color     | Description                                |
| ------------------------------- | --------- | ------------------------------------------ |
| `severity:blocker`              | `#B60205` | Blocks merge / data loss / broken contract |
| `severity:high`                 | `#D93F0B` | Serious defect with a real path            |
| `severity:medium`               | `#FBCA04` | Important but not high-risk                |
| `severity:low`                  | `#0E8A16` | Nit / low urgency                          |
| `practicality:high`             | `#1D76DB` | Realistic path in this system              |
| `practicality:medium`           | `#5319E7` | Non-default / internal / admin path        |
| `practicality:low`              | `#C5DEF5` | Mostly excluded by types/invariants        |
| `practicality:none`             | `#EDEDED` | No real path / unsupported environment     |
| `practicality:seen-in-the-wild` | `#BFDADC` | Observed in real usage                     |
| `cost:cheap`                    | `#C2E0C6` | Small local fix                            |
| `cost:medium`                   | `#FEF2C0` | Moderate issue-planning cost               |
| `cost:expensive`                | `#F9D0C4` | Large or cross-cutting work                |

Example ensure + create pattern:

```bash
# For each allowlisted label NAME you will attach:
gh label list --json name --jq '.[].name' | grep -Fxq "$NAME" \
  || gh label create "$NAME" --color "${COLOR#\#}" --description "$DESC"

gh issue create --title "..." --body-file /tmp/issue.md --label "severity:high" --label "practicality:high" --label "cost:cheap" --type Bug
```

(`--type` requires org Issue Types configured; if it fails, report clearly — provisioning types is out of skill scope.)

Use the current repo from context, or ask if the target repo is unclear.

## Issue body template

Body **must** be GitHub Markdown:

```markdown
## Type

Bug | Security | Feature | Task | Discussion | Refactoring

## Triage

- **severity:** …
- **practicality:** … (path or “seen-in-the-wild” evidence)
- **cost:** … (cheap | medium | expensive)

## Problem

<what is wrong / what we observed>

## Why not now?

<what prevents this from being handled in the original PR/dialogue>

## Acceptance criteria (suggested)

- <what “done” looks like>

## Links

- PR: …
```

## Output to the user

Return:

- the created issue URL (or “skipped GitHub writes” plus the draft title/body)
- the selected org issue type
- the attached labels

## Guardrails

- Do not commit or push unless asked.
- Never rewrite/patch code; only create an issue (and allowlisted labels if missing).
- If correctness is unclear or the user provided no actionable content, ask a single follow-up question instead of
  creating a low-quality issue.
- If label create fails due to permissions, stop attaching that label path, explain, and still offer the draft.
