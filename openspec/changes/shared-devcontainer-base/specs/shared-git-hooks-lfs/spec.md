# shared-git-hooks-lfs Delta

## MODIFIED Requirements

### Requirement: Documentation of commit vs pre-push install

Documentation (README and/or `docs/quality.md` / Dev Container docs) MUST state that:

- Commit-stage hooks are installed with `pre-commit install --hook-type pre-commit` (not files under
  `scripts/git-hooks/`), including via shared Dev Container postCreate.
- Pre-push LFS + quality hooks are installed with `./scripts/setup-git-lfs.sh` (postCreate / after clone).
- Pre-push pre-commit stages run pytest and container-structure-test via `scripts/run-container-structure-test.sh` / #7
  config (product application Dockerfiles stay in consumers).

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality or README docs for git hooks
- **THEN** they learn the commit-stage vs `setup-git-lfs.sh` split
- **AND** they learn postCreate runs both installs on the Dev Container path
- **AND** they learn pre-push runs the #7 CST/pytest stages

## ADDED Requirements

### Requirement: Dev Container postCreate invokes setup-git-lfs

On the documented Linux Dev Container create path, `scripts/devcontainer-post-create.sh` MUST invoke
`scripts/setup-git-lfs.sh` after the commit-stage pre-commit hook is installed (or after `uv sync` when that provides
`pre-commit`), so LFS and project pre-push hooks are present without a separate manual step.

#### Scenario: postCreate installs LFS hooks

- **WHEN** a contributor creates/recreates the Dev Container and postCreate completes successfully
- **THEN** `./scripts/setup-git-lfs.sh` has been run as part of that flow
- **AND** `.git/hooks/pre-push` (and the other project LFS hooks) are present from `scripts/git-hooks/`
