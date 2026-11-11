## ADDED Requirements

### Requirement: Reusable code-quality runs actionlint

When `skip` is false, `reusable-code-quality.yml` MUST install the caller’s pinned actionlint (from the caller’s
`versions.env` via the shared install helper) and MUST run actionlint against the checkout’s GitHub workflow files. The
step MUST fail the job on findings (**blocking**). Missing actionlint pin or install failure MUST fail closed. The same
`ACTIONLINT_VERSION` pin MUST be used as for Dev Container and commit-stage hooks (no alternate CI-only pin).

#### Scenario: CI actionlint fails on a workflow finding

- **WHEN** reusable code-quality runs with `skip` false and a workflow under `.github/workflows/` has an actionlint
  finding
- **THEN** the job fails
- **AND** the installed binary matches the caller `ACTIONLINT_VERSION`

#### Scenario: CI actionlint uses versions.env pin

- **WHEN** an operator changes only `ACTIONLINT_VERSION` in the caller `versions.env` and syncs/rebuilds as documented
- **THEN** both local hooks and reusable code-quality use that new pin after install/rebuild
