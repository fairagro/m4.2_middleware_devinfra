# Extract review-fixer and personal-token helpers — Proposal

## Why

Wave A needs `/review-fixer` as a shared Fixer skill, which depends on conventions-aligned `gh` token helpers. Issue #8
is pulled forward (ahead of epic #7) and landed in the same change as issue #5 so Auth paths and the skill stay
coherent. Policy and Finder entries already live here from #4.

## What Changes

- **Issue #8 (complete):** Add `scripts/dev-tokens.sh`, `scripts/set-dev-tokens.sh`, `scripts/bin/gh`,
  `scripts/bin/git`; wire Dev Container `PATH`; load stored tokens from postCreate/shell **and** keep wrappers (Kombi);
  document empty-skip + re-prompt; host token path `~/.config/<git-repo-name>/` from `origin` (no `PRODUCT_SLUG`);
  persist `GH_TOKEN` and `GITGUARDIAN_API_KEY`
- **Issue #5:** Add `.agents/skills/review-fixer/`, `.cursor/commands/review-fixer.md`,
  `.github/prompts/review-fixer.prompt.md` from the API (Variante A: keep GraphQL plumbing; generalize Auth to shared
  wrappers + conventions; cite `openspec/principles.global.md`; inline follow-up issue Markdown — no create-issue skill
  dependency)
- Done criteria for #5 in this repo: artifacts present and content-reviewed (no product-PR smoke test required here)
- Out of scope: #16 CLI, #14 create-issue, #6 vendor skills, #7 quality scripts

## Capabilities

### New Capabilities

- `personal-token-helpers`: Shared personal-token store/load/prompt scripts, `gh`/`git` PATH wrappers, and documented
  empty-skip / re-prompt behavior following path conventions
- `review-fixer`: Canonical `/review-fixer` skill plus Cursor command and Copilot prompt that triage Copilot/Bugbot PR
  reviews using the shared AI review policy

### Modified Capabilities

- `path-conventions`: Host personal-token path uses git repository name instead of product-slug / `PRODUCT_SLUG`
- `ai-review-policy`: Nit-budget is per fixer run (~15 lines), not gated on Copilot/Bugbot review round

## Impact

- Closes the Auth gap for agent `gh` use and lands the Fixer stack for Wave A sync
- Epic note: #8 listed after #7; this change intentionally does not wait on #7
- #16 may later replace embedded GraphQL with a CLI; skill stays judgment-focused
