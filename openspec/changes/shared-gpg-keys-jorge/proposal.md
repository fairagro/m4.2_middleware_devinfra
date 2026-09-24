## Why

Devinfra needs the same shared public-GPG + SOPS recipient pattern as product repos so developers can encrypt/decrypt
repo secrets and so Jorge’s new key can be added as a recipient. postCreate already imports `public_gpg_keys/*.asc` when
present, but the folder, `.sops.yaml`, and a shared import script are missing (#230).

## What Changes

- Add repo-root `public_gpg_keys/` with Carsten’s and Jorge’s **new** (2026-09-23, `A9069D1B…`) armored public keys
  (not Jorge’s older `37D38A6C…` key used in some products).
- Add repo-root `.sops.yaml` with two `creation_rules` (generic enc + dotenv), both listing Carsten + Jorge-new
  fingerprints.
- Extract `scripts/import-public-gpg-keys.sh` (product-style); wire postCreate to call it instead of an inline loop.
- Document the layout and that `sops updatekeys` on existing ciphertext is a follow-up where decrypt rights exist
  (product issues; Devinfra enc files remain maintainer-local).
- **Not** in this change: running `sops updatekeys` in CI/agent; rotating Jorge’s old key in product repos (tracked as
  product issues).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-devcontainer-base`: postCreate MUST import keys via a shared `scripts/import-public-gpg-keys.sh` when
  `public_gpg_keys/*.asc` exist; Devinfra docs MUST describe root `.sops.yaml` + `public_gpg_keys` as the recipient
  layout (content stays repo-local, not product-synced).

## Impact

- `public_gpg_keys/*.asc`, `.sops.yaml`, `scripts/import-public-gpg-keys.sh`, `scripts/devcontainer-post-create.sh`,
  `docs/devcontainer.md` (and related sync notes if the import script is allowlisted for products).
- Existing Devinfra ciphertext (`.env.integration.enc`, `dev_environment/secrets.enc.yaml`) needs a later
  `sops updatekeys` by someone who can decrypt — out of agent scope per lock-in.
- Product follow-up issues: add Jorge-new key + `updatekeys` where secrets exist.
