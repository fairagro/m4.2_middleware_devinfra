## Why

Verbatim shared Dev Container postCreate installs only the quality `pre-push` and never runs product LFS setup, so LFS
products (e.g. sql_to_arc) lose compose/`git lfs` configuration after create/rebuild. Shared and product installers also
cannot safely share `.git/hooks/pre-push` under a file-overwrite model. Discussion #114 locked a durable compose +
drop-in design; this change implements it in Devinfra (#155).

## What Changes

- Replace monolith `.git/hooks/pre-push` install with a **Devinfra-owned dispatcher** plus **`pre-push.d/` fragments**
  (quality fragment from shared SoT; products drop their own numbered scripts). Installers are idempotent and must not
  alter foreign fragments.
- **MVP:** compose only for `pre-push`. Product LFS `post-*` hooks stay flat and untouched by shared setup.
- At **T-late**, shared postCreate runs **`scripts/devcontainer-post-create.d/*.sh`** (sorted). **Hard-fail** when a
  present drop-in is not executable or exits non-zero. Still MUST NOT hard-code product LFS script names.
- Update docs and OpenSpec for `shared-git-hooks` and `shared-devcontainer-base`.
- **BREAKING** for products that relied on replacing the entire `.git/hooks/pre-push` after shared setup: they must
  register a `pre-push.d/` fragment and (for Dev Container restore) add a `devcontainer-post-create.d/` drop-in.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-git-hooks`: dispatcher + `pre-push.d/` install contract; quality fragment only; foreign fragments preserved;
  docs for product fragment ownership
- `shared-devcontainer-base`: T-late `devcontainer-post-create.d/` drop-ins with hard-fail; stop forbidding all product
  extension while still forbidding hard-coded LFS script names

## Impact

- `scripts/setup-git-hooks.sh`, `scripts/git-hooks/**`, `scripts/devcontainer-post-create.sh`
- `docs/quality.md`, `docs/devcontainer.md` (and related README pointers if any)
- Synced allowlist already covers these scripts; product sync will pick up the new contract
- sql_to_arc (and other LFS products): follow-up to emit `pre-push.d/10-git-lfs` + a postCreate drop-in (out of this
  repo’s merge, documented as required adopt work)
