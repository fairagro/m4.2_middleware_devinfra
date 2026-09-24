## 1. Shared import script and postCreate

- [x] 1.1 Add `scripts/import-public-gpg-keys.sh` (product-style: import `public_gpg_keys/*.asc` or soft-skip) and
      verify `bash -n` plus exit 0 with empty keys dir
- [x] 1.2 Change `scripts/devcontainer-post-create.sh` to call the shared import script instead of an inline GPG loop
      and verify the script path is invoked
- [x] 1.3 Allowlist `scripts/import-public-gpg-keys.sh` in `docs/synced-paths.yaml` and verify it appears under `allow`
      while `.sops.yaml` / `public_gpg_keys/` do not

## 2. Devinfra recipients (Carsten + Jorge-new only)

- [x] 2.1 Add Jorge’s new public key under `public_gpg_keys/` and verify the fingerprint matches `A9069D1B…`
      (`gpg --show-keys` / import check)
- [x] 2.2 Ensure Carsten’s public key remains under `public_gpg_keys/` and verify fingerprint `CC7B10CE…`
- [x] 2.3 Update root `.sops.yaml` so every `creation_rules` path uses only Carsten + Jorge-new fingerprints (no
      Jorge-old) and verify `sops --version` / YAML parse; do **not** run `sops updatekeys` or decrypt in this change

## 3. Docs and product handoff

- [x] 3.1 Document `public_gpg_keys/` + `.sops.yaml` layout and the `sops updatekeys` handoff in `docs/devcontainer.md`
      (and sync.md if needed) and verify the docs describe product follow-up for Jorge-new + updatekeys
- [x] 3.2 Confirm GitHub issues exist (or are linked from the PR) in the three product repos (API, sql_to_arc,
      harvester) for adding Jorge-new and running `sops updatekeys` on existing enc files
