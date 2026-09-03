# Agree path conventions — Proposal

## Why

Product repos use API-specific or inconsistent names for personal-token stores and Docker volumes (`middleware-api`,
`sql-to-arc`, …). Before extracting shared scripts and Dev Container pieces, we need written conventions so sync does
not fight those names. Issue #3 is next in the epic after bootstrap layout (#2).

## What Changes

- Add `docs/conventions.md` documenting: personal-token paths (per-product, not shared), Docker volume naming pattern
  with a product-slug table, and `middleware/` as the product package root
- Link that doc from the root `README.md` Docs index
- No script, volume, or consumer-repo renames in this change

## Capabilities

### New Capabilities

- `path-conventions`: Written shared path and naming conventions for tokens, Dev Container volumes, and product package
  roots

### Modified Capabilities

- (none — main specs empty; prior `repo-layout` delta was archived without sync)

## Impact

- Later extraction issues (#4–#10, #8 especially) have a single conventions doc to follow
- Root README Docs section gains one link
- Existing Docker volumes and host token files unchanged (documentation only; migrations out of scope)
