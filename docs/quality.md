# Shared quality tooling

Commit-stage and pre-push quality via [`pre-commit`](https://pre-commit.com). Canonical files live in this Devinfra repo
for sync into product consumers (`middleware/` package root — see [path conventions](conventions.md)).

## Files

| Path                                      | Role                                                |
| ----------------------------------------- | --------------------------------------------------- |
| `.pre-commit-config.yaml`                 | Commit-stage + pre-push hook skeleton               |
| `scripts/quality-check.sh`                | Run **commit-stage** hooks only (check)             |
| `scripts/quality-fix.sh`                  | Run commit-stage **autofix** hooks only             |
| `scripts/run-container-structure-test.sh` | Templated Docker build + `container-structure-test` |
| `.bandit`                                 | Bandit config (`bandit -c .bandit`)                 |
| `.markdownlint.json` (+ ignore / cli2)    | Markdownlint (also used by the markdownlint hook)   |

## Install (commit stage)

```bash
uv sync
pre-commit install --hook-type pre-commit
# or: uv run pre-commit install --hook-type pre-commit
```

Typical place: Dev Container **postCreate** (issue
[#10](https://github.com/fairagro/m4.2_middleware_devinfra/issues/10)).

**Pre-push git hook** install (so the pre-push stage runs on `git push`) is issue
[#9](https://github.com/fairagro/m4.2_middleware_devinfra/issues/9) — not done by these scripts.

## Manual runs

```bash
./scripts/quality-check.sh   # commit-stage only
./scripts/quality-fix.sh     # autofix hooks, then re-run quality-check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push   # pytest + CST (needs Docker / tests)
```

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
