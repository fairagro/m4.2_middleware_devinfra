# shared-git-hooks-lfs Specification

## Purpose

Version-controlled Git LFS hooks and installer so product repos install the same pre-push (LFS + pre-commit pre-push
stage) and LFS lifecycle hooks after clone or Dev Container create.

## Requirements

### Requirement: Setup script installs local LFS and project hooks

The repository MUST provide `scripts/setup-git-lfs.sh` that, from a git worktree: verifies `git-lfs` is on `PATH` (MUST
fail clearly if missing — MUST NOT auto-install via Homebrew or similar unsupported host package managers), runs
`git lfs install --local` (with skip-smudge / force as appropriate for local-only config), and copies
`scripts/git-hooks/{pre-push,post-checkout,post-commit,post-merge}` into `.git/hooks/` as executable files when those
sources exist.

#### Scenario: Contributor runs setup with git-lfs present

- **WHEN** a contributor runs `./scripts/setup-git-lfs.sh` in a clone with `git-lfs` available
- **THEN** local LFS is initialized and the four project hooks are installed under `.git/hooks/`
- **AND** the script does not write LFS filter config only to the user’s global gitconfig as its primary path

#### Scenario: git-lfs missing

- **WHEN** `git-lfs` is not on `PATH`
- **THEN** the script exits non-zero with guidance to install Git LFS
- **AND** it does not invoke Homebrew or other unsupported host package managers

### Requirement: pre-push runs LFS then pre-commit pre-push stage

`scripts/git-hooks/pre-push` MUST invoke `git lfs pre-push` with the hook arguments, then run the shared pre-commit
configuration’s **pre-push** stage (via `uv run pre-commit`, project `.venv` `python -m pre_commit`, or `pre-commit` on
`PATH`) using `.pre-commit-config.yaml` and `--hook-type=pre-push` (or equivalent `hook-impl`). Because both consumers
read the git pre-push ref list from stdin, the hook MUST buffer that stdin once and replay it to LFS and to pre-commit
(so the quality stage is not skipped after LFS drains stdin).

#### Scenario: git push triggers LFS and quality pre-push

- **WHEN** the installed `pre-push` hook runs on `git push`
- **THEN** Git LFS pre-push runs first with the ref list from stdin
- **AND** the pre-commit pre-push stage runs afterward with the same ref list (pytest / container-structure-test when
  configured)

### Requirement: LFS lifecycle hooks are version-controlled

The repository MUST provide `scripts/git-hooks/post-checkout`, `post-commit`, and `post-merge` that delegate to the
corresponding `git lfs` hook commands when `git-lfs` is available.

#### Scenario: post-checkout delegates to LFS

- **WHEN** the installed `post-checkout` hook runs
- **THEN** it calls `git lfs post-checkout` with the hook arguments (when git-lfs is present)

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

### Requirement: Dev Container postCreate invokes setup-git-lfs

On the documented Linux Dev Container create path, `scripts/devcontainer-post-create.sh` MUST invoke
`scripts/setup-git-lfs.sh` after the commit-stage pre-commit hook is installed (or after `uv sync` when that provides
`pre-commit`), so LFS and project pre-push hooks are present without a separate manual step.

#### Scenario: postCreate installs LFS hooks

- **WHEN** a contributor creates/recreates the Dev Container and postCreate completes successfully
- **THEN** `./scripts/setup-git-lfs.sh` has been run as part of that flow
- **AND** `.git/hooks/pre-push` (and the other project LFS hooks) are present from `scripts/git-hooks/`
