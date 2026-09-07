# ai-review-policy Delta

## ADDED Requirements

### Requirement: Surface quality bar path map files

The repository MUST provide `docs/surface-quality-bar.global.md` as the synced default **path→surface** map for the
surface quality bar (typical paths, bar, exotic-edge default per surface). `docs/ai_review_policy.md` MUST keep the
triage **rules** that describe how the bar affects fixer step 5, nit-budget, and dismiss behaviour, and MUST point
readers to `docs/surface-quality-bar.global.md` plus an optional product-local overlay at `docs/surface-quality-bar.md`.
Sync of the shared policy and of `surface-quality-bar.global.md` MUST NOT overwrite a product’s
`docs/surface-quality-bar.md`. Consumers MUST NOT need to edit `docs/ai_review_policy.md` solely to add or adjust a
path→surface row.

#### Scenario: Contributor opens the default path map

- **WHEN** a contributor opens `docs/surface-quality-bar.global.md` in Devinfra or after sync into a product repo
- **THEN** they find the default path→surface table (or equivalent map) for shared surfaces
- **AND** they learn that product-specific path rows belong in `docs/surface-quality-bar.md`, not in the synced policy
  body

#### Scenario: Product extends the map without editing the policy

- **WHEN** a product repo needs an additional path→surface row (e.g. a local package layout)
- **THEN** it MAY add that row in local `docs/surface-quality-bar.md`
- **AND** it MUST NOT need to hand-edit synced `docs/ai_review_policy.md` or synced `docs/surface-quality-bar.global.md`
  for that extension
