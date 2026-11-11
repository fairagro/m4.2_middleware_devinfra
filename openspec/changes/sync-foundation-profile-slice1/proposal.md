## Why

#347 locked a gitops/infra profile and an optional fourth sync consumer. Today sync uses one Wave-A allowlist and three
python-product targets; applying that blob to `m4.2_infrastructure` would clobber its GitOps Dev Container and CI. Slice
1 needs a **foundation** path set (skills + AI plumbing) and an Infra target that receives only that set.

## What Changes

- Restructure `docs/synced-paths.yaml` to **profile-based** allowlists in one file (layout B): at least `foundation` and
  `python-product`, shared `exclude` / `overlays`
- Define Slice-1 **foundation** allow: agent skills (incl. `uv`), matching commands/prompts, skill docs, AI stack docs
  pointers as needed, `scripts/ai/**`, `scripts/bin/m42-ai`, personal-token helpers (`dev-tokens` / `set-dev-tokens` /
  related bin wrappers required by those helpers)
- Keep product targets on **foundation ∪ python-product** (today’s Wave-A coverage)
- Add optional sync target `infrastructure` → `fairagro/m4.2_infrastructure` using **foundation only**
- Update `scripts/sync-products.py`, sync workflow (`skip_infrastructure`, dry-run), and `docs/sync.md` for profiles +
  fourth target + non-goals
- **Out of scope:** Renovate/`versions.env` on Infra (#354), pre-commit split (#351), Dev Container targets (#352), live
  Infra bot-token grant (Slice 2)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `synced-consumer-paths`: sole SoT file gains `profiles` (foundation / python-product); document how consumers resolve
  which profile set applies; Slice-1 foundation membership for skills + AI plumbing
- `product-repo-sync`: resolve copy set from selected profiles; add `infrastructure` target; workflow skip/dry-run docs
  for the fourth consumer

## Impact

- Sync automation and allowlist YAML shape (products keep full union; Infra gets foundation-only when enabled)
- Docs / OpenSpec; Infra#80 can point at dry-run once landed
- No change to product runtime until next sync PR; Infra sync stays opt-in until bot access (#354) and operators unskip
