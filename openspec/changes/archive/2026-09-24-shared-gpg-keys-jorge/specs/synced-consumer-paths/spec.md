## ADDED Requirements

### Requirement: Import-public-gpg-keys script is allowlisted

`docs/synced-paths.yaml` MUST list `scripts/import-public-gpg-keys.sh` under `allow` so products can sync the shared
import runner. `.sops.yaml` and `public_gpg_keys/**` MUST NOT be on `allow` (repo-local recipient content).

#### Scenario: Import script on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `scripts/import-public-gpg-keys.sh` appears under `allow`
- **AND** `.sops.yaml` and `public_gpg_keys/` do not appear under `allow`
