# Split surface quality bar path map (issue #32)

## Why

The surface quality bar’s path→surface table lives inside the synced `docs/ai_review_policy.md`. Product repos must not
hand-edit that file, so adding a local package-layout row means forking the whole policy or waiting on Devinfra. Split
the **map** from the **rules** so products can extend paths without merge conflicts on the shared policy body.

## What Changes

- Move the default path→surface table out of `docs/ai_review_policy.md` into synced `docs/surface-quality-bar.global.md`
- Keep triage **rules** (how the bar affects step 5 / nits / dismiss) in `docs/ai_review_policy.md`, with links to the
  global map and to an optional product-local overlay
- Document product overlay as `docs/surface-quality-bar.md` (not overwritten by sync of the `.global.md` file)
- Update `ai-review-policy` spec, skill/README pointers, and sync-facing docs as needed
- No runtime/CLI behaviour change

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `ai-review-policy`: Require the path map to live in `docs/surface-quality-bar.global.md` (synced default) with
  optional product extensions in `docs/surface-quality-bar.md`; policy doc keeps rules and points at those files

## Impact

- Docs: `docs/ai_review_policy.md`, new `docs/surface-quality-bar.global.md`
- Spec: `openspec/specs/ai-review-policy`
- Pointers: `.agents/skills/review-fixer`, `.agents/skills/issue-fixer`, README / `docs/issue-fixer.md` as needed
- Sync (#13): global map is syncable; product `surface-quality-bar.md` stays local
- Issue: [#32](https://github.com/fairagro/m4.2_middleware_devinfra/issues/32)
