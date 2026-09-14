## 1. Dockerfile binary-builder

- [ ] 1.1 Update `docker/Dockerfile.product-app.base` binary-builder: provide `uv.lock` + required project/workspace
      metadata (copy from package-builder or context); install locked deps with `uv sync --frozen` (no-dev /
      no-install-workspace as needed)
- [ ] 1.2 Install package-builder wheels with `--no-deps` (system Python or PATH such that PyInstaller entry resolution
      still works); keep `pyinstaller==${PYINSTALLER_VERSION}`
- [ ] 1.3 Update the file header comment that currently documents bare `uv pip install` of wheels

## 2. Docs and validate

- [ ] 2.1 Document the lockfile-deterministic install contract in `docs/ci.md` (product-app Bake section)
- [ ] 2.2 `openspec validate lockfile-deterministic-product-app-base --strict`
- [ ] 2.3 Format/lint touched Markdown; hadolint on the Dockerfile if the project path expects it
