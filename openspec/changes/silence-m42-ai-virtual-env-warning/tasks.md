## 1. Wrapper and sync

- [ ] 1.1 Add executable `scripts/bin/m42-ai` that unsets `VIRTUAL_ENV` and runs
      `uv run --project <repo-root>/scripts/ai m42-ai "$@"` (repo root from wrapper path); verify
      `VIRTUAL_ENV=/workspace/.venv m42-ai --help` has no `VIRTUAL_ENV` mismatch warning on stderr
- [ ] 1.2 Add `scripts/bin/m42-ai` to `docs/synced-paths.yaml` allowlist beside other `scripts/bin` helpers; verify the
      path appears in the YAML list

## 2. Docs and skills

- [ ] 2.1 Update `scripts/ai/README.md` product invoke to silent primary (`m42-ai` /
      `env -u     VIRTUAL_ENV uv run --project scripts/ai m42-ai`); verify README does not recommend `--active` or
      removing DC `VIRTUAL_ENV`
- [ ] 2.2 Update Auth / command examples in synced skills (`issue-fixer`, `create-issue`, `review-fixer`, `code-review`)
      and matching thin docs to the silent primary form; verify no skill still presents raw
      `uv run --project scripts/ai m42-ai` as the only/primary product form without `env -u` or wrapper

## 3. Verification

- [ ] 3.1 Run `openspec validate silence-m42-ai-virtual-env-warning --strict` and confirm it passes; smoke
      `m42-ai auth-status` (or `--help`) with `VIRTUAL_ENV` set and confirm stderr is clean of the mismatch warning
