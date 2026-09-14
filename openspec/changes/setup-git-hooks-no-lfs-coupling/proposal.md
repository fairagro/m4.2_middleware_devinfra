## Why

Shared `scripts/setup-git-hooks.sh` currently **detects and deletes** Git LFS `post-*` hooks and documents LFS as a
shared concern, while Devinfra’s contract is that Git LFS is entirely product-owned. With verbatim Dev Container JSON
([#65](https://github.com/fairagro/m4.2_middleware_devinfra/issues/65)), products cannot keep multi-step `postCreate` in
JSON; we must not invent shared “call product `install-dev-hooks.sh` if present” callbacks. Docs still drift toward
“product postCreate snippet” / `remoteEnv` for `MYPYPATH` instead of `product.env`.

## What Changes

- Remove LFS-aware deletion and LFS-specific messaging from `scripts/setup-git-hooks.sh` (install quality `pre-push`
  only; leave other hooks untouched).
- Do **not** add optional product-script invocation from `devcontainer-post-create.sh`.
- Update `docs/devcontainer.md` and `docs/quality.md`: LFS = product-owned and independent; no JSON postCreate snippet
  for LFS; path overlays via `product.env` / CI inputs (not `remoteEnv` for `MYPYPATH`).
- Align `shared-devcontainer-base` so docs/requirements forbid shared LFS hook management and product-script callbacks
  from shared postCreate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-git-hooks`: `setup-git-hooks.sh` MUST NOT detect/remove/manage Git LFS hooks; docs MUST NOT imply shared LFS
  hook cleanup.
- `shared-devcontainer-base`: shared postCreate MUST NOT invoke optional product scripts such as
  `install-dev-hooks.sh`; consumer docs MUST describe LFS as product-owned (not via synced JSON postCreate) and
  `MYPYPATH` via `product.env` / CI.

## Impact

- Synced `scripts/setup-git-hooks.sh` (and docs) in product consumers after next sync.
- sql-to-arc (and any LFS product) keeps owning LFS install/overlay scripts; after verbatim adopt they re-apply LFS
  product-side when needed (no Devinfra callback). Tracked via product adopt issues (e.g. sql-to-arc #129), not this
  change’s MVP.
- Issue: [#112](https://github.com/fairagro/m4.2_middleware_devinfra/issues/112).
