# shared-renovate Delta

## ADDED Requirements

### Requirement: Bot token is shared with product sync under one secret name

Renovate documentation and workflow MUST use the repository Actions secret `DEVINFRA_BOT_TOKEN` as the bot credential
(fine-grained PAT or GitHub App installation token material). The same secret MUST be the bot credential for
product-repo sync. Scopes MUST cover Contents and Pull requests on Devinfra and the three product targets (plus
Workflows/Issues as required by Renovate). Docs MUST NOT require SOPS-in-repo storage for that token and MUST NOT
document a second bot secret name (`RENOVATE_TOKEN`) as an alternate.

#### Scenario: Operator configures one bot for Renovate and sync

- **WHEN** an operator reads Renovate (and sync) token docs
- **THEN** they learn one secret `DEVINFRA_BOT_TOKEN` serves both workflows
- **AND** they learn required GitHub Actions secret setup (not SOPS)
