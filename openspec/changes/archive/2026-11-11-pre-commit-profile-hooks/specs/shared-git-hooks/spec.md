## MODIFIED Requirements

### Requirement: pre-push runs pre-commit pre-push stage only

The shared quality fragment (installed as `.git/hooks/pre-push.d/50-quality`, sourced from `scripts/git-hooks/`) MUST
run the consumer’s root pre-commit configuration **pre-push** stage (via `uv run pre-commit`, project `.venv`
`python -m pre_commit`, or `pre-commit` on `PATH`) using root `.pre-commit-config.yaml` and `--hook-type=pre-push` (or
equivalent `hook-impl`). Infra checkouts that sync `.pre-commit-config.infrastructure.yaml` MUST install or point that
file as the active root config before relying on this fragment. It MUST NOT invoke `git lfs pre-push`. The dispatcher
MUST preserve the git pre-push ref list for every fragment (including the quality fragment). Product-owned fragments
(e.g. Git LFS) are outside this requirement. When the active root has no pre-push hooks (e.g. Infra foundation+gitops
config), the quality fragment MUST still invoke pre-commit’s pre-push stage without requiring python-product pytest/CST
hooks to exist.

#### Scenario: git push triggers quality pre-push

- **WHEN** the installed dispatcher runs on `git push` and `.git/hooks/pre-push.d/50-quality` is present
- **THEN** the pre-commit pre-push stage runs (pytest / container-structure-test when configured)
- **AND** the quality fragment does not fail solely because `git-lfs` is missing

#### Scenario: Product fragment runs before quality when numbered earlier

- **WHEN** `.git/hooks/pre-push.d/` contains both an earlier-sorted product fragment (e.g. `10-git-lfs`) and
  `50-quality`
- **THEN** the dispatcher runs the product fragment before `50-quality` on `git push`
