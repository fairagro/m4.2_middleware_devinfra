## MODIFIED Requirements

### Requirement: Setup script installs project git hooks

The repository MUST provide `scripts/setup-git-hooks.sh` that, from a git worktree, installs a **Devinfra-owned pre-push
compose layout**:

- `.git/hooks/pre-push` — thin **dispatcher** that buffers the git pre-push stdin once and runs every executable file
  under `.git/hooks/pre-push.d/` in lexicographic order, replaying the same stdin and arguments to each fragment; the
  first non-zero fragment exit MUST abort the hook
- `.git/hooks/pre-push.d/50-quality` — shared **quality fragment** whose source of truth lives under
  `scripts/git-hooks/` (alongside the dispatcher source)

The setup script MUST install or refresh only the dispatcher and the shared `50-quality` fragment from that SoT. It MUST
NOT delete, rename, or rewrite other files under `.git/hooks/pre-push.d/`. It MUST NOT require `git-lfs` on `PATH`, MUST
NOT run `git lfs install`, and MUST NOT detect, remove, rewrite, or otherwise manage Git LFS hooks (including
`post-checkout`, `post-commit`, `post-merge`, or LFS-related content in other hook files). Re-running the script MUST be
idempotent for the shared-owned paths. The repository MUST NOT ship `scripts/setup-git-lfs.sh`.

#### Scenario: Contributor runs setup-git-hooks

- **WHEN** a contributor runs `./scripts/setup-git-hooks.sh` in a clone
- **THEN** `.git/hooks/pre-push` is installed as the shared dispatcher
- **AND** `.git/hooks/pre-push.d/50-quality` is installed from the shared SoT
- **AND** the script succeeds without `git-lfs` on `PATH`

#### Scenario: Existing non-pre-push hooks are left alone

- **WHEN** a contributor runs `./scripts/setup-git-hooks.sh` in a worktree that already has other `.git/hooks` entries
  (including product Git LFS hooks)
- **THEN** those non-`pre-push` hooks are not deleted by LFS content detection in the shared script

#### Scenario: Foreign pre-push.d fragments are left alone

- **WHEN** a contributor runs `./scripts/setup-git-hooks.sh` in a worktree that already has additional
  `.git/hooks/pre-push.d/*` fragments besides the shared quality fragment
- **THEN** those foreign fragments are left in place (not deleted or rewritten)

### Requirement: pre-push runs pre-commit pre-push stage only

The shared quality fragment (installed as `.git/hooks/pre-push.d/50-quality`, sourced from `scripts/git-hooks/`) MUST
run the shared pre-commit configuration’s **pre-push** stage (via `uv run pre-commit`, project `.venv`
`python -m pre_commit`, or `pre-commit` on `PATH`) using `.pre-commit-config.yaml` and `--hook-type=pre-push` (or
equivalent `hook-impl`). It MUST NOT invoke `git lfs pre-push`. The dispatcher MUST preserve the git pre-push ref list
for every fragment (including the quality fragment). Product-owned fragments (e.g. Git LFS) are outside this
requirement.

#### Scenario: git push triggers quality pre-push

- **WHEN** the installed dispatcher runs on `git push` and `.git/hooks/pre-push.d/50-quality` is present
- **THEN** the pre-commit pre-push stage runs (pytest / container-structure-test when configured)
- **AND** the quality fragment does not fail solely because `git-lfs` is missing

#### Scenario: Product fragment runs before quality when numbered earlier

- **WHEN** `.git/hooks/pre-push.d/` contains both an earlier-sorted product fragment (e.g. `10-git-lfs`) and
  `50-quality`
- **THEN** the dispatcher runs the product fragment before `50-quality` on `git push`

### Requirement: Documentation of commit vs pre-push install

Documentation (README and/or `docs/quality.md` / Dev Container docs) MUST state that:

- Commit-stage hooks are installed with `pre-commit install --hook-type pre-commit` (not files under
  `scripts/git-hooks/`), including via shared Dev Container postCreate.
- Pre-push quality hooks are installed with `./scripts/setup-git-hooks.sh` (postCreate / after clone), which installs
  the dispatcher plus `pre-push.d/50-quality`.
- Products that need additional pre-push steps MUST drop numbered executables into `.git/hooks/pre-push.d/` (via a
  product installer) and MUST NOT replace the shared dispatcher file wholesale.
- Pre-push pre-commit stages run pytest and container-structure-test via `scripts/run-container-structure-test.sh` when
  configured (product application Dockerfiles stay in consumers).
- Git LFS is **not** part of the shared toolchain or shared hook installer; products that need LFS own install and hook
  overlays (including optional `pre-push.d` fragments and flat `post-*` hooks) entirely in the product repo. Shared
  `setup-git-hooks.sh` does not remove LFS hooks or foreign `pre-push.d` fragments. Shared postCreate MUST NOT hard-code
  product LFS script names; optional product work runs only via the documented `scripts/devcontainer-post-create.d/`
  drop-ins. Docs MUST NOT recommend editing synced Dev Container JSON `postCreate` for LFS.

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality or README docs for git hooks
- **THEN** they learn the commit-stage vs `setup-git-hooks.sh` (dispatcher + `pre-push.d`) split
- **AND** they learn postCreate runs shared hook install and optional `devcontainer-post-create.d` drop-ins
- **AND** they learn shared Devinfra does not require or manage Git LFS hooks

### Requirement: Dev Container postCreate invokes setup-git-hooks

On the documented Linux Dev Container create path, `scripts/devcontainer-post-create.sh` MUST invoke
`scripts/setup-git-hooks.sh` after the commit-stage pre-commit hook is installed (or after `uv sync` when that provides
`pre-commit`), so the dispatcher and shared quality fragment are present without a separate manual step. Shared
postCreate MUST NOT hard-code optional product-local script names (e.g. `scripts/install-dev-hooks.sh`,
`scripts/setup-git-lfs.sh`).

#### Scenario: postCreate installs project hooks

- **WHEN** a contributor creates/recreates the Dev Container and postCreate completes successfully
- **THEN** `./scripts/setup-git-hooks.sh` has been run as part of that flow
- **AND** `.git/hooks/pre-push` (dispatcher) and `.git/hooks/pre-push.d/50-quality` are present from
  `scripts/git-hooks/`
- **AND** postCreate does not call `scripts/install-dev-hooks.sh` or `scripts/setup-git-lfs.sh` by those hard-coded
  names even if those files exist
