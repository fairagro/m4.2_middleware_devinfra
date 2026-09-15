## ADDED Requirements

### Requirement: Node markdown toolchain manifests are allowlisted

`docs/synced-paths.yaml` MUST list root `package.json` and `package-lock.json` under `allow` so product consumers
receive the same npm scripts and pins used by commit-stage markdown hooks and reusable code-quality CI. Products MUST
NOT treat those manifests as standing sync excludes.

#### Scenario: package.json on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `package.json` and `package-lock.json` appear under `allow`
- **AND** they learn markdown CI/hooks adopt those files via sync from Devinfra
