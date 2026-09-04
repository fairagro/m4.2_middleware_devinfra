# Extract issue-fixer — Design

## Context

See proposal.md. Source behavior lives in `fairagro/m4.2_advanced_middleware_api` `.agents/skills/issue-fixer/` plus
Cursor command and Copilot prompt. Devinfra already has shared Auth, `/review-fixer`, and `/create-issue` on `main`.
Explore lock-ins A–G from `/opsx-explore` on [#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15) drive
the deltas from a 1:1 API copy.

## Goals / Non-Goals

**Goals:**

- Land canonical issue-fixer skill, command, prompt, and thin docs
- Match Auth to review-fixer/create-issue; deferred issues only via create-issue
- Same docs/README pattern for review-fixer, create-issue, and issue-fixer (add missing `docs/review-fixer.md`)
- Encode empty bootstrap commit + draft PR + explore pause + type gates + sub-vs-linked relation in the skills

**Non-Goals:**

- #16 `issue-start` CLI (skill text should stay compatible with a later CLI wrap)
- Deep nested epic hierarchies beyond one parent level for a split
- Product-repo sync PRs or smoke tests
- Hard dependency on `/opsx-explore` or OpenSpec for every run

## Decisions

### 1. Variante: API procedure + Devinfra Auth + lock-ins A–G

- **Choice:** Copy API skill shape; rewrite Auth like create-issue; replace vague “empty head” with one
  `git commit --allow-empty` on a clean tree; draft PR; explore before writes for Feature/Refactoring;
  Discussion/Security gates; create-issue for deferred work with relation G
- **Alternatives:** 1:1 API copy; defer explore to a separate slash command
- **Why:** GitHub cannot open a PR with identical SHAs; #16 already says draft; user workflow is explore-then-implement

### 2. Empty commit message and clean-tree check

- **Choice:** Message `Start issue #<issue_number>`; require clean working tree and index before `--allow-empty` so
  staged files cannot sneak into the bootstrap commit; do not use `--no-verify`
- **Alternatives:** Truly empty branch (impossible for PR); placeholder file commit
- **Why:** Platform constraint; keeps “no fix commits” honest

### 3. Draft PR; agent never marks ready

- **Choice:** `gh pr create --draft`; remind user to mark ready after they push real commits
- **Alternatives:** Ready PR; auto-`gh pr ready` after first user push
- **Why:** Avoids Finder noise on empty bootstrap; aligns with #16

### 4. Explore stance inlined (not `/opsx-explore` dependency)

- **Choice:** Skill embeds explore stance (open threads, wait for lock-in); optionally offer OpenSpec propose when
  `openspec/` exists; user may `skip explore` / `go`
- **Alternatives:** Always invoke `/opsx-explore`; always require OpenSpec change
- **Why:** Portable across product repos; matches how #15 was run without hard-wiring Cursor OpenSpec commands

### 5. Deferred issues via create-issue; docs parity trio

- **Choice:** Same amendment pattern as review-fixer→create-issue; add `docs/issue-fixer.md` and `docs/review-fixer.md`;
  update `docs/create-issue.md` + README; document relation G in create-issue docs
- **Alternatives:** Inline `gh issue create` in issue-fixer; README-only for issue-fixer
- **Why:** One creator skill; user required identical documentation pattern for all three

### 6. Quality checks when product `middleware/` exists

- **Choice:** Match review-fixer wording: focused pytest/ruff when the consumer has product packages; Devinfra itself
  has none
- **Why:** Skill is shared; API “skip quality unless debugging” was too weak for a code-writing fixer

### 7. Sub-issue vs linked relation (lock-in G)

- **Choice:** Callers pass `relation: sub-of #<issue_number> | linked` into create-issue.
  - **Sub-issue** (`gh issue create --parent` / equivalent): new work is still part of the parent’s acceptance criteria
    / done-when (issue-fixer splits of the issue being fixed).
  - **Linked** (body Links + optional related mention only): distinct follow-up problem not covered by that parent
    (typical review-fixer deferral; “discovered while working on #N”).
  - Unclear → ask once; default **linked** (do not pollute hierarchy).
  - review-fixer: **linked** by default; **sub-of #<issue_number>** only when the PR body has `Fixes #<issue_number>`
    and the deferred item is clearly remaining acceptance criteria of that issue.
- **Alternatives:** Markdown links only (previous Non-Goal); always sub-issue under PR or epic
- **Why:** User lock-in; GitHub CLI supports `--parent` / `--add-sub-issue`; hierarchy should mean “same work split,”
  not “related topic”

## Risks / Trade-offs

- **[Risk] Empty commit triggers CI minutes on drafts** → Mitigation: document that draft is a review gate, not a CI
  gate; product workflows may later filter drafts (#11+)
- **[Risk] Hooks fail on empty commit (commit-msg)** → Mitigation: do not `--no-verify`; fix message; fail clearly
- **[Risk] Explore pause ignored by hurried agents** → Mitigation: command/prompt restate wait; specs require no
  branch/PR during pause
- **[Risk] Wrong relation (sub vs linked)** → Mitigation: default linked when unclear; explicit heuristics in skills
- **[Risk] `gh issue create --parent` unsupported on older gh / org** → Mitigation: skill documents flag; fall back to
  one linked create only when no issue URL exists yet; never create again after a partial post-create failure
- **[Trade-off] create-issue + review-fixer docs/behavior touch in this change** → Acceptable for parity and G

## Migration Plan

1. Implement artifacts on a branch from `main`
2. Content review; close #15 when merged
3. Consumers sync later; #16 wraps `issue-start` against this contract
4. Rollback = revert

## Open Questions

None — A–G locked in explore.
