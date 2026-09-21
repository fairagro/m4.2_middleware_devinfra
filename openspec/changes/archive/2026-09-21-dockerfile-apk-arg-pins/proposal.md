## Why

Product Dockerfiles pin Alpine apk packages either inline (`pkg=X.Y.Z-rN`) or via `ARG …_VERSION=` defaults. Shared
`update-dockerfile-pins.sh` only rewrites inline literals, so ARG-based pins stay stale while the script prints success
— Bake then fails (seen in sql_to_arc). The fleet needs one supported pin style and a script that updates it end-to-end
with fail-loud behaviour.

## What Changes

- Standardize on **style B**: `ARG <PKG>_VERSION=X.Y.Z-rN` plus `"pkg=${<PKG>_VERSION}"` in `RUN apk add` (no duplicate
  inline version literals for apk).
- Teach `scripts/update-dockerfile-pins.sh` to refresh those ARG defaults from Alpine APKINDEX; keep inline `name==` pip
  pin updates.
- Fail loud when apk pins cannot be refreshed or when forbidden inline `pkg=…-rN` apk pins remain.
- Document the convention in `docs/renovate.md` (and script header); #167 UX already landed separately.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-product-app-dockerfile`: product last-stage / product Dockerfile apk pin style and updater contract

## Impact

- `scripts/update-dockerfile-pins.sh` (synced)
- `docs/renovate.md` / brief `docs/ci.md` pointer if needed
- Product Dockerfiles migrate to ARG style on sync / follow-up (out of this PR’s product trees)
