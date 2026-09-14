# shared-git-hooks Specification

## Purpose

Version-controlled git hooks and installer so product repos install the same pre-push quality gate (pre-commit pre-push
stage) after clone or Dev Container create, without requiring Git LFS.

## Requirements

### Requirement: Setup script installs project git hooks

The repository MUST provide `scripts/setup-git-hooks.sh` that, from a git worktree, copies `scripts/git-hooks/pre-push`
into `.git/hooks/pre-push` as an executable file when the source exists. The script MUST NOT require `git-lfs` on `PATH`
and MUST NOT run `git lfs install`. The script MUST NOT detect, remove, rewrite, or otherwise manage Git LFS hooks
(including `post-checkout`, `post-commit`, `post-merge`, or LFS-related content in other hook files). The repository
MUST NOT ship `scripts/setup-git-lfs.sh`.

#### Scenario: Contributor runs setup-git-hooks

- **WHEN** a contributor runs `./scripts/setup-git-hooks.sh` in a clone
- **THEN** `.git/hooks/pre-push` is installed from `scripts/git-hooks/pre-push`
- **AND** the script succeeds without `git-lfs` on `PATH`

#### Scenario: Existing non-pre-push hooks are left alone

- **WHEN** a contributor runs `./scripts/setup-git-hooks.sh` in a worktree that already has other `.git/hooks` entries
  (including product Git LFS hooks)
- **THEN** those non-`pre-push` hooks are not deleted by LFS content detection in the shared script

### Requirement: pre-push runs pre-commit pre-push stage only

`scripts/git-hooks/pre-push` MUST run the shared pre-commit configuration’s **pre-push** stage (via `uv run pre-commit`,
project `.venv` `python -m pre_commit`, or `pre-commit` on `PATH`) using `.pre-commit-config.yaml` and
`--hook-type=pre-push` (or equivalent `hook-impl`). It MUST NOT invoke `git lfs pre-push`. If the hook buffers stdin for
the quality stage, that buffering MUST preserve the git pre-push ref list for pre-commit.

#### Scenario: git push triggers quality pre-push

- **WHEN** the installed `pre-push` hook runs on `git push`
- **THEN** the pre-commit pre-push stage runs (pytest / container-structure-test when configured)
- **AND** the hook does not fail solely because `git-lfs` is missing

### Requirement: Documentation of commit vs pre-push install

Documentation (README and/or `docs/quality.md` / Dev Container docs) MUST state that:

- Commit-stage hooks are installed with `pre-commit install --hook-type pre-commit` (not files under
  `scripts/git-hooks/`), including via shared Dev Container postCreate.
- Pre-push quality hooks are installed with `./scripts/setup-git-hooks.sh` (postCreate / after clone).
- Pre-push pre-commit stages run pytest and container-structure-test via `scripts/run-container-structure-test.sh` when
  configured (product application Dockerfiles stay in consumers).
- Git LFS is **not** part of the shared toolchain or shared hook installer; products that need LFS own install and hook
  overlays entirely in the product repo. Shared `setup-git-hooks.sh` does not remove LFS hooks. Shared postCreate does
  not call product LFS scripts. Docs MUST NOT recommend editing synced Dev Container JSON `postCreate` for LFS.

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality or README docs for git hooks
- **THEN** they learn the commit-stage vs `setup-git-hooks.sh` split
- **AND** they learn postCreate runs both installs on the Dev Container path
- **AND** they learn shared Devinfra does not require or manage Git LFS hooks

### Requirement: Dev Container postCreate invokes setup-git-hooks

On the documented Linux Dev Container create path, `scripts/devcontainer-post-create.sh` MUST invoke
`scripts/setup-git-hooks.sh` after the commit-stage pre-commit hook is installed (or after `uv sync` when that provides
`pre-commit`), so project pre-push hooks are present without a separate manual step. Shared postCreate MUST NOT invoke
optional product-local scripts when present (e.g. `scripts/install-dev-hooks.sh`, `scripts/setup-git-lfs.sh`).

#### Scenario: postCreate installs project hooks

- **WHEN** a contributor creates/recreates the Dev Container and postCreate completes successfully
- **THEN** `./scripts/setup-git-hooks.sh` has been run as part of that flow
- **AND** `.git/hooks/pre-push` is present from `scripts/git-hooks/`
- **AND** postCreate does not call product `install-dev-hooks.sh` / `setup-git-lfs.sh` even if those files exist
