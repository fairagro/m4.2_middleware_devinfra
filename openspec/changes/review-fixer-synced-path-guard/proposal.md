# review-fixer: never patch synced consumer paths (issue #45)

## Why

`/review-fixer` in product repos can (and did) apply local patches to **synced** Devinfra paths, creating drift that the
next sync overwrites or conflicts with. The real fix belongs upstream in Devinfra (or on an explicit product overlay),
not in the consumer tree. Wave A adopts are landing now; the skill and policy must hard-stop that before more PRs repeat
[API#374](https://github.com/fairagro/m4.2_advanced_middleware_api/pull/374).

## What Changes

- Add a single synced allowlist doc (`docs/synced-paths.global.md`) listing Devinfra-canonical paths consumers must not
  hand-edit; skill and policy link to it (explore **A1**).
- Harden `/review-fixer` + AI review policy: never `fix` synced trees in a consumer checkout; for synced findings use
  existing `follow-up` / `dismiss` (explore **D1**) with B2 gating — follow-up to Devinfra when Medium+ / Risk or
  seen-in-the-wild shared bug; otherwise dismiss “synced — edit upstream” (explore **B2**). Fix only documented local
  overlays.
- Policy one-liner: sync source-of-truth overrides “cheap + High practicality → fix in this PR” for synced paths.
- Content fixes in the same change (explore **C1**): `scripts/ai/README.md` documents workspace **and**
  `--project scripts/ai` consumer layouts; `_dev_tokens_write` atomically replaces the tokens file (`mv`).

## Capabilities

### New Capabilities

- `synced-consumer-paths`: Canonical allowlist of paths synced from Devinfra that consumers and `/review-fixer` must
  treat as read-only in product checkouts (plus documented overlay exceptions).

### Modified Capabilities

- `review-fixer`: Hard rule never modify synced/canonical paths; phase-1 actions use `follow-up`/`dismiss` (no new
  action label) with clear Devinfra targeting; working tree must not dirty synced files.
- `ai-review-policy`: Sync SoT overrides step-5 cheap fix for synced paths; cross-link allowlist and surface bar.
- `personal-token-helpers`: Token store writes MUST be atomic replace (no truncate-via-redirect).
- `agent-ai-gh`: Agent CLI docs MUST describe both Devinfra workspace membership and consumer `--project scripts/ai`
  invocation (and matching test commands).

## Impact

- `.agents/skills/review-fixer/SKILL.md`, thin command/prompt if needed
- `docs/ai_review_policy.md`, new `docs/synced-paths.global.md`, README Docs index, optional surface-bar cross-link
- `scripts/ai/README.md`, `scripts/dev-tokens.sh`
- OpenSpec main specs for the capabilities above (after archive)
- Consumers pick up behavior on next sync (#13); no consumer code in this PR
