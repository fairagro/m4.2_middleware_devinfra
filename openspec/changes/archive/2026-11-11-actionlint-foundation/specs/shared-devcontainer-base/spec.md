## ADDED Requirements

### Requirement: Actionlint pinned in the shared Dev Container image

The shared product Dev Container image MUST install **actionlint** at the version pinned by `ACTIONLINT_VERSION` in
`versions.env` (Compose build-arg / Dockerfile `ARG`, same pattern as gitleaks). The binary MUST be on `PATH` after
rebuild so commit-stage actionlint hooks work without a separate host install. Documentation (`docs/devcontainer.md`
and/or `docs/quality.md`) MUST name actionlint among shared CLI tools.

#### Scenario: actionlint available after rebuild

- **WHEN** a contributor rebuilds the Dev Container from this repo’s compose/Dockerfile
- **THEN** `actionlint` is on `PATH` at `ACTIONLINT_VERSION`
- **AND** Dev Container docs list actionlint with the other shared lint CLIs
