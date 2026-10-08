## ADDED Requirements

### Requirement: git-cliff pinned for Conventional Commits version detection

The shared Dev Container toolchain MUST pin **git-cliff** in `versions.env` (exact version SoT, same pattern as other
CLI pins) and install it on `PATH` in the shared image so contributors can dry-run bump detection locally. Release
GitHub Actions jobs that resolve `version_bump: auto` MUST use the same pin. Documentation (`docs/devcontainer.md`
and/or `docs/ci.md`) MUST mention `git-cliff` for local bump dry-runs tied to release auto-detect.

#### Scenario: git-cliff available in Dev Container

- **WHEN** a contributor uses the shared Dev Container after this change
- **THEN** `git-cliff` is on `PATH` at the version pinned in `versions.env`

#### Scenario: Pin is single SoT

- **WHEN** an operator updates the git-cliff version
- **THEN** they change only `versions.env` (plus any lockstep install recipe)
- **AND** Dev Container and Release jobs document consuming that pin
