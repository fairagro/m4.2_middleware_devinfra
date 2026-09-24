## Context

See proposal.md — Why. postCreate already imports `public_gpg_keys/*.asc` inline; products use a small
`scripts/import-public-gpg-keys.sh`. Devinfra lacks the folder, `.sops.yaml`, and key files. Ciphertext exists but
`sops updatekeys` stays maintainer/product-side (lock-in C).

## Goals / Non-Goals

**Goals:**

- Match the product root layout: `public_gpg_keys/*.asc` + `.sops.yaml` (two creation_rules) + shared import script.
- Recipients: Carsten (`CC7B10CE…`) + Jorge-new (`A9069D1B…`) only.
- postCreate calls the shared script (same behavior, clearer SoT for sync into products if allowlisted).

**Non-Goals:**

- Running `sops updatekeys` / decrypt in the agent or CI.
- Shipping Jorge’s older key (`37D38A6C…`).
- Syncing `.sops.yaml` / key **content** into products (still per-repo; only the import script may be shared tooling).

## Decisions

1. **Root layout like API/sql_to_arc** — not infrastructure’s per-`environments/*/public_gpg_keys` layout (Devinfra is
   one repo, not multi-env infra).
2. **Two creation_rules** — generic enc paths + dotenv `.env*.enc`, both with the same two PGP fingerprints (matches
   product `.sops.yaml` shape and issue AC).
3. **Import script** — copy product semantics (`public_gpg_keys/*.asc`, soft-empty exit 0, require `gpg`); postCreate
   replaces the inline loop with `bash scripts/import-public-gpg-keys.sh`.
4. **Allowlist** — add `scripts/import-public-gpg-keys.sh` to `docs/synced-paths.yaml` `allow` so products can sync the
   runner; do **not** allowlist `.sops.yaml` or `public_gpg_keys/**` (content stays local).
5. **updatekeys** — Devinfra ciphertext: maintainer with decrypt rights runs `sops updatekeys` after merge. Products:
   GitHub issues to add Jorge-new + updatekeys (and drop/ignore old Jorge key as they choose).

## Risks / Trade-offs

- [Risk] New recipients cannot decrypt existing ciphertext until `updatekeys` → Mitigation: document; product issues;
  Devinfra maintainer step after PR.
- [Risk] Filename vs fingerprint mismatch → Mitigation: name `.asc` files `{FINGERPRINT}_{Name}.asc` like products.
- [Risk] Syncing only the import script while products keep their own keys → Acceptable; script is behavior SoT only.
