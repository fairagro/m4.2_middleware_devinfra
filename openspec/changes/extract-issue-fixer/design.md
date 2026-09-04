# Extract issue-fixer — Design

## Context

See proposal.md. Source behavior lives in `fairagro/m4.2_advanced_middleware_api` `.agents/skills/issue-fixer/` plus
Cursor command and Copilot prompt. Devinfra already has shared Auth, `/review-fixer`, and `/create-issue` on `main`.
Explore lock-ins A–F from `/opsx-explore` on [#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15) drive
the deltas from a 1:1 API copy.

## Goals / Non-Goals

**Goals:**

- Land canonical issue-fixer skill, command, prompt, and thin docs
- Match Auth to review-fixer/create-issue; sub-issues via create-issue only
- Same docs/README pattern for review-fixer, create-issue, and issue-fixer (add missing `docs/review-fixer.md`)
- Encode empty bootstrap commit + draft PR + explore pause + type gates in the skill

**Non-Goals:**

- #16 `issue-start` CLI (skill text should stay compatible with a later CLI wrap)
- Native GitHub parent/child sub-issue GraphQL (body + PR links are enough)
- Product-repo sync PRs or smoke tests
- Hard dependency on `/opsx-explore` or OpenSpec for every run

## Decisions

### 1. Variante: API procedure + Devinfra Auth + lock-ins A–F

- **Choice:** Copy API skill shape; rewrite Auth like create-issue; replace vague “empty head” with one
  `git commit --allow-empty` on a clean tree; draft PR; explore before writes for Feature/Refactoring;
  Discussion/Security gates; create-issue for splits
- **Alternatives:** 1:1 API copy; defer explore to a separate slash command
- **Why:** GitHub cannot open a PR with identical SHAs; #16 already says draft; user workflow is explore-then-implement

### 2. Empty commit message and clean-tree check

- **Choice:** Message `Start issue #<n>`; require clean working tree and index before `--allow-empty` so staged files
  cannot sneak into the bootstrap commit; do not use `--no-verify`
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

### 5. Sub-issues via create-issue; docs parity trio

- **Choice:** Same amendment pattern as review-fixer→create-issue; add `docs/issue-fixer.md` and `docs/review-fixer.md`;
  update `docs/create-issue.md` + README
- **Alternatives:** Inline `gh issue create` in issue-fixer; README-only for issue-fixer
- **Why:** One creator skill; user required identical documentation pattern for all three

### 6. Quality checks when product `middleware/` exists

- **Choice:** Match review-fixer wording: focused pytest/ruff when the consumer has product packages; Devinfra itself
  has none
- **Why:** Skill is shared; API “skip quality unless debugging” was too weak for a code-writing fixer

## Risks / Trade-offs

- **[Risk] Empty commit triggers CI minutes on drafts** → Mitigation: document that draft is a review gate, not a CI
  gate; product workflows may later filter drafts (#11+)
- **[Risk] Hooks fail on empty commit (commit-msg)** → Mitigation: do not `--no-verify`; fix message; fail clearly
- **[Risk] Explore pause ignored by hurried agents** → Mitigation: command/prompt restate wait; specs require no
  branch/PR during pause
- **[Trade-off] create-issue + review-fixer docs touch in this change** → Acceptable for parity; keeps #15 coherent

## Migration Plan

1. Implement artifacts on a branch from `main`
2. Content review; close #15 when merged
3. Consumers sync later; #16 wraps `issue-start` against this contract
4. Rollback = revert

## Open Questions

None — A–F locked in explore.
