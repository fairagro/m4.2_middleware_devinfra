## 1. Shared loader helper

- [ ] 1.1 Add a small bash helper that parses only `MYPYPATH` / `PYLINT_SOURCE_ROOTS` from a given env file (soft-skip
      missing) and verify with a unit-style shell fixture or scripted assertions
- [ ] 1.2 Wire `scripts/run-quality-cli.sh` to apply the helper when vars are unset/empty and verify unset→file and
      set→unchanged behavior

## 2. Reusable code-quality workflow

- [ ] 2.1 Extend `reusable-code-quality.yml` to load from `.devcontainer/product.env` (optional `quality_env_file`
      input) when `mypy_path` / `pylint_source_roots` are empty, with input override, and verify the step script logic
      (dry review / local bash extract if feasible)
- [ ] 2.2 Keep existing non-empty input behavior unchanged and verify docs table lists the new input

## 3. Docs and product handoff

- [ ] 3.1 Document the single-source contract + example `product.env` keys in `docs/ci.md` and `docs/quality.md` (and
      `docs/devcontainer.md` if needed) and verify SKIP/override order is clear
- [ ] 3.2 Link Harvester adopter follow-up https://github.com/fairagro/m4.2_middleware_harvester/issues/299 from docs or
      the PR body
