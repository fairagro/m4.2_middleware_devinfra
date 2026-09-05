# Shared git-hooks + LFS — Tasks

## 1. Hooks and installer

- [x] 1.1 Add `scripts/git-hooks/post-checkout`, `post-commit`, `post-merge` (LFS delegates; install via setup script)
- [x] 1.2 Add `scripts/git-hooks/pre-push` (LFS pre-push, then pre-commit pre-push stage via `uv run` / venv / PATH)
- [x] 1.3 Add `scripts/setup-git-lfs.sh` (`git lfs install --local`, copy hooks, fail if git-lfs missing; no brew/apt
      auto-install)
- [x] 1.4 Make scripts executable; safe under `set -e` / `set -euo pipefail` as appropriate

## 2. Docs

- [x] 2.1 Document commit-stage (`pre-commit install`) vs `./scripts/setup-git-lfs.sh` in README and/or
      `docs/quality.md`
- [x] 2.2 Document that pre-push stages run pytest + CST (`run-container-structure-test.sh` / #7); note postCreate call
      (full wiring #10)

## 3. Verify

- [x] 3.1 Smoke: `bash -n` on scripts; setup fails clearly without git-lfs mock or succeeds in Dev Container
- [x] 3.2 Mark tasks complete when files match `shared-git-hooks-lfs` requirements
