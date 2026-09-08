# shared-renovate Delta

## ADDED Requirements

### Requirement: Bot token may be shared with product sync

Renovate documentation MUST state that the Actions secret used for self-hosted Renovate MAY be the same bot token
(fine-grained PAT or GitHub App installation token material) used by product-repo sync, provided scopes cover Contents
and Pull requests on Devinfra and the three product targets (plus Workflows/Issues as required by Renovate). Docs MUST
name the secret(s) operators should create and MUST NOT require SOPS-in-repo storage for that token.

#### Scenario: Operator configures one bot for Renovate and sync

- **WHEN** an operator reads Renovate (and sync) token docs
- **THEN** they learn one bot token MAY serve both workflows
- **AND** they learn required GitHub Actions secret setup (not SOPS)
