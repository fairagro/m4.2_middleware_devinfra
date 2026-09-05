# Shared quality tooling

Commit-stage and pre-push quality via [`pre-commit`](https://pre-commit.com). Canonical files live in this Devinfra repo
for sync into product consumers (`middleware/` package root — see [path conventions](conventions.md)).

## Script environments

Not every file under `scripts/` is Dev Container-only. Personal-token helpers are; quality runners are not.

| Script / tree                         | Environment            | Notes                                                                                                                                                    |
| ------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `quality-check.sh` / `quality-fix.sh` | Host or Dev Container  | Needs `uv`. Commit-stage also runs `npm run lint:md` (Node/`npm`; host: `npm install`). On the host, set `GITGUARDIAN_API_KEY` for ggshield if required. |
| `run-container-structure-test.sh`     | Host or Dev Container  | Needs Docker + `container-structure-test`                                                                                                                |
| `setup-git-lfs.sh` / `git-hooks/`     | Host or Dev Container  | Needs `git-lfs` on PATH; copies hooks into `.git/hooks/`                                                                                                 |
| `load-versions-env.sh`                | Host or Dev Container  | Reads `versions.env`, writes `.python-version`                                                                                                           |
| `scripts/ai/` (`m42-ai`)              | Host or Dev Container  | Needs `gh` on `PATH` and auth (`GH_TOKEN` / `gh auth`)                                                                                                   |
| `dev-tokens.sh` / `set-dev-tokens.sh` | **Dev Container only** | Store: `/commandhistory/tokens.env`                                                                                                                      |
| `scripts/bin/gh`, `scripts/bin/git`   | **Dev Container only** | On `PATH` via `remoteEnv`; load the token store                                                                                                          |
| `devcontainer-post-create.sh`         | **Dev Container only** | Invoked from `devcontainer.json`                                                                                                                         |

Supported day-to-day development remains the Linux Dev Container ([principles](../openspec/principles.global.md)). Host
checkouts may run the **host-or-DC** scripts above; they do not get the personal-token store or PATH wrappers — use
tokens already in your environment (e.g. exported from `~/.bashrc`) or `gh auth` as you prefer.

## Files

| Path                                      | Role                                                |
| ----------------------------------------- | --------------------------------------------------- |
| `.pre-commit-config.yaml`                 | Commit-stage + pre-push hook skeleton               |
| `scripts/quality-check.sh`                | Run **commit-stage** hooks only (check)             |
| `scripts/quality-fix.sh`                  | Run commit-stage **autofix** hooks only             |
| `scripts/run-container-structure-test.sh` | Templated Docker build + `container-structure-test` |
| `scripts/setup-git-lfs.sh`                | Install Git LFS (local) + copy `scripts/git-hooks/` |
| `scripts/git-hooks/`                      | `pre-push` (LFS + pre-commit) + LFS lifecycle hooks |
| `.bandit`                                 | Bandit config (`bandit -c .bandit`)                 |
| `.markdownlint.json` (+ ignore / cli2)    | Markdownlint (also used by the markdownlint hook)   |

## Install

### Commit stage

```bash
uv sync
npm install   # host clones needing local markdownlint/prettier; skip if tools are global
uv run pre-commit install --hook-type pre-commit
```

Typical place: Dev Container **postCreate** (issue
[#10](https://github.com/fairagro/m4.2_middleware_devinfra/issues/10)). These hooks are **not** files under
`scripts/git-hooks/`.

### Pre-push (Git LFS + quality stage)

```bash
./scripts/setup-git-lfs.sh
```

Copies `scripts/git-hooks/{pre-push,post-checkout,post-commit,post-merge}` into `.git/hooks/` and runs
`git lfs install --local`. Requires `git-lfs` on `PATH` (no Homebrew/apt auto-install). Call from postCreate when #10
wires it, or once after clone.

On `git push`, `pre-push` runs Git LFS first, then the shared pre-commit **pre-push** stage (pytest +
`scripts/run-container-structure-test.sh` from the #7 skeleton). Product Dockerfiles / CST YAML stay in consumers. Needs
Docker/tests when those hooks are active.

Manual without the git hook:

```bash
uv run pre-commit run --all-files --hook-stage pre-push
```

## Manual runs (commit stage)

```bash
./scripts/quality-check.sh   # commit-stage, non-mutating only
./scripts/quality-fix.sh     # autofix hooks, then re-run quality-check
uv run pre-commit run --all-files   # full commit stage (includes autofixers)
```

On a **host** checkout, export `GITGUARDIAN_API_KEY` (and any other secrets hooks need) yourself — there is no
`~/.config/…` token helper outside the Dev Container.

## Container structure test parameters

`scripts/run-container-structure-test.sh` defaults:

| Input       | Default                                              | Override                 |
| ----------- | ---------------------------------------------------- | ------------------------ |
| Dockerfile  | `docker/Dockerfile`                                  | `CST_DOCKERFILE` or `$1` |
| Image tag   | `app:structure-test`                                 | `CST_IMAGE_TAG` or `$2`  |
| Test config | `docker/container-structure-tests` (dir of `*.yaml`) | `CST_CONFIG` or `$3`     |

Optional Docker `--build-arg` values are taken from `versions.env` when set (`PYTHON_VERSION`, `UV_VERSION`,
`ALPINE_VERSION`, `ALPINE_MINOR`, `PIP_VERSION`).

Example (API-shaped product):

```bash
CST_DOCKERFILE=docker/Dockerfile.api \
CST_IMAGE_TAG=fairagro-advanced-middleware-api:test \
CST_CONFIG=docker/container-structure-tests/api.yaml \
  ./scripts/run-container-structure-test.sh
```

## Notes

- Vendor skill trees under `.agents/skills/{gh,docker,hadolint,uv}/` (and `scan-secrets` if present) are excluded from
  tree-walking hooks — do not hand-edit those trees.
- This Devinfra repo has **no** `middleware/` packages; Python hooks scoped to `middleware/` apply after sync to a
  product repo.
