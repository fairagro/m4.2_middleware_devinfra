# Tasks: shared Python quality config fragments

## 1. Fragments from API seed

- [ ] 1.1 Add root `ruff.toml` extracted from product API `[tool.ruff*]` (middleware-oriented; no product-only secrets)
- [ ] 1.2 Add shared Mypy config file (document exact filename) from API `[tool.mypy]`, with notes for local path
      overlays
- [ ] 1.3 Add shared Pylint config file from API `[tool.pylint*]`, aligned with Ruff disables

## 2. Devinfra coexistence

- [ ] 2.1 Align Devinfra root `pyproject.toml` thin `[tool.ruff]` / `[tool.mypy]` stubs with fragments (or remove
      redundant stubs) so local `uv run ruff` / mypy behavior is unambiguous
- [ ] 2.2 Confirm `scripts/ai/pyproject.toml` unchanged and listed as **not** in the product quality sync set

## 3. Hooks and docs

- [ ] 3.1 Update `.pre-commit-config.yaml` if hooks need explicit `--config` paths for the new fragments
- [ ] 3.2 Extend `docs/quality.md` (+ README pointer if needed): sync file list, local vs shared, D1/smoke via #13,
      Dockerfile deferred to sub-issue (base + local last stage)
- [x] 3.3 Open GitHub sub-issue under #28 for Dockerfile unify → shared base with ARGs + product-local last stage
      (`relation: sub-of #28`) — [#36](https://github.com/fairagro/m4.2_middleware_devinfra/issues/36)

## 4. Verify

- [ ] 4.1 `openspec validate shared-pyproject-quality-layer --strict`
- [ ] 4.2 `npm run format:md` and `npm run lint:md` on touched Markdown
