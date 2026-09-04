# Extract create-issue — Design

## Context

See proposal.md. Source of truth for behavior is the API skill at `fairagro/m4.2_advanced_middleware_api`
`.agents/skills/create-issue/`. Devinfra already has shared `gh` wrappers, token helpers, and `/review-fixer` Auth
patterns on `main`. Explore lock-ins: Variante B (artifacts + docs), Auth like review-fixer, create-if-missing
allowlisted labels in the skill (no bootstrap script).

## Goals / Non-Goals

**Goals:**

- Land canonical create-issue skill, command, and prompt
- Document issue types + triage labels; create-if-missing for allowlisted labels only
- Reuse shared Auth (`scripts/bin/gh` + chat `set-dev-tokens.sh` flow)

**Non-Goals:**

- #15 issue-fixer
- Org-level Issue Type provisioning
- Dedicated `ensure-triage-labels.sh` / postCreate label bootstrap
- Product-repo sync PRs or smoke tests in this change
- Replacing review-fixer’s inline Medium+ follow-up template (stays independent)

## Decisions

### 1. Variante B from API + Devinfra Auth

- **Choice:** Copy API skill/command/prompt; rewrite Auth to match review-fixer; include `Refactoring` everywhere types
  are listed; short README/docs for types + labels
- **Alternatives:** 1:1 copy only; add label bootstrap script
- **Why:** Explore lock-in; Done-when is artifacts + docs here

### 2. Create-if-missing labels inside the skill

- **Choice:** Before attach, `gh label list` / create allowlisted names only (fixed colors/descriptions in the skill).
  One-shot per repo emerges naturally on first successful create
- **Alternatives:** Docs-only; separate script
- **Why:** User preference; avoid free-text label sprawl via allowlist

### 3. Issue vocabulary extensions documented, not forked policy tables

- **Choice:** Cite `docs/ai_review_policy.md` for severity/practicality/cost core meanings; document
  `practicality:seen-in-the-wild` and `cost:medium` as create-issue extensions in skill + docs
- **Alternatives:** Expand ai_review_policy tables for issues
- **Why:** Keep Finder/Fixer policy focused; issue creator owns issue-oriented extras

### 4. Task vs Refactoring wording

- **Choice:** Skill text: `Task` = bounded follow-up/tech-debt/docs; `Refactoring` = multi-module or structural
  restructure. Drop “Task: refactor…” overlap from API wording where it conflicts
- **Why:** Issue #14 lists both types; API prompt was inconsistent

## Risks / Trade-offs

- **[Risk] PAT lacks label-write permission** → Mitigation: skill fails clearly; docs note needed scopes; user creates
  labels once in UI
- **[Risk] Org Issue Types missing** → Mitigation: document expected type names; creation fails with clear error (out of
  scope to provision)
- **[Trade-off] First create slower (label creates)** → Acceptable one-shot per repo

## Migration Plan

1. Add artifacts + docs on a branch from current `main`
2. Content review; close #14 when merged
3. Consumers sync later; no sync in this change
4. Rollback = revert
