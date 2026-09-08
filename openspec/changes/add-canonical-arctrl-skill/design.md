# Design: add-canonical-arctrl-skill

## Context

See proposal.md — Why. Harvester already publishes the fullest `.agents/skills/arctrl/SKILL.md` (~17 KB; arctrl ≥
3.2.1). API and sql-to-arc ship thinner v3.x copies. Devinfra first-party skills today are workflow skills
(`review-fixer`, `create-issue`, `issue-fixer`); vendor trees are `gh` / `docker` / `hadolint` / `uv` only.

## Goals / Non-Goals

**Goals:**

- Land a single canonical skill path under `.agents/skills/arctrl/` sourced from harvester
- Document discovery in README without confusing it with vendor pins
- Keep markdown format/lint on the skill (first-party)

**Non-Goals:**

- Product-repo sync PRs or deleting product-local copies (#13)
- Cursor command / Copilot prompt wrappers for arctrl
- Expanding or rewriting the skill beyond harvester fidelity unless needed for repo markdown style
- Changing vendor exclude lists except by **not** adding arctrl

## Decisions

1. **Source of truth for content = harvester tip at import**  
   Copy `fairagro/m4.2_middleware_harvester` `.agents/skills/arctrl/SKILL.md` via `gh api` (raw). Prefer byte-faithful
   import then run `npm run format:md` / `lint:md` so Prettier/markdownlint may normalize wrapping without dropping
   sections.  
   _Alternative:_ Merge API + harvester manually — rejected; issue asks harvester full set.

2. **New OpenSpec capability `shared-arctrl-skill`**  
   Mirrors how workflow skills have their own specs; keeps `vendor-agent-skills` focused on `gh skill` pins.  
   _Alternative:_ Extend `vendor-agent-skills` with a “first-party reference skills” clause — rejected; wrong capability
   name and would blur vendor vs first-party.

3. **No vendor ignore path for arctrl**  
   Do not add to `.prettierignore` / `.markdownlintignore` / pre-commit excludes. Fix any lint nits in the imported
   file.  
   _Alternative:_ Treat as vendor-like exclude — rejected by issue AC.

4. **README: layout row + short first-party note**  
   Add a layout table row next to other `.agents/skills/*` first-party entries. Optionally one sentence under Vendor
   section clarifying shared first-party skills (including arctrl) are hand-maintained here — keep the Vendor section’s
   install commands unchanged.  
   _Alternative:_ Separate “First-party skills” H2 — fine if README stays readable; prefer minimal diff (layout + brief
   note).

## Risks / Trade-offs

- **[Risk] Harvester skill drifts after import** → Mitigation: products sync from Devinfra (#13); future updates land
  here first.
- **[Risk] Prettier/markdownlint changes wrap/structure of long skill** → Mitigation: format once; preserve headings and
  code fences; do not delete feature sections to silence lint.
- **[Trade-off] Skill size (~500 lines) in Devinfra** → Acceptable; matches harvester and is the point of the issue.

## Migration Plan

1. Add skill + README on this branch; merge via draft PR (`Fixes #35`).
2. Sync consumers later (#13) replace product copies — out of this change.
3. Rollback: delete `.agents/skills/arctrl/` and README rows; no other deps.

## Open Questions

- None for this change (product sync timing stays on #13).
