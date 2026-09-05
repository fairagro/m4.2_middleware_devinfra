# shared-quality-tooling Delta

## MODIFIED Requirements

### Requirement: Documentation of hook install boundaries

Documentation (README and/or `docs/`) MUST state that commit-stage installation is
`pre-commit install --hook-type pre-commit` (performed by shared `scripts/devcontainer-post-create.sh` on Dev Container
create, and runnable manually after clone), and that the pre-push **git** hook (Git LFS + pre-commit pre-push stage) is
installed via `scripts/setup-git-lfs.sh` from the shared git-hooks extract (also invoked from that postCreate). Manual
`uv run pre-commit run --hook-stage pre-push` remains valid without that git hook.

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality / README docs for this tooling
- **THEN** they learn how to install the commit-stage hook
- **AND** they learn pre-push git-hook install is `./scripts/setup-git-lfs.sh` (wired from postCreate on the Dev
  Container path)
