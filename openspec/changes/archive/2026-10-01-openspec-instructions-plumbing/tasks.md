## 1. CLI plumbing

- [x] 1.1 Add `m42-ai openspec-instructions --artifact <id> --change <name>` that shells to
      `openspec instructions <id> --change <name> --json`, validates JSON, exits 0 with instructions fields on success,
      and exits non-zero with `{ok:false, error, agent_action:"stop"}` on empty/non-JSON/`change_error`/missing
      `openspec` — verify with unit tests using mocked subprocess output (no network)
- [x] 1.2 Wire the subcommand in `cli.py` / argparse and verify `m42-ai openspec-instructions --help` lists it
- [x] 1.3 Document the command in `scripts/ai/README.md` Commands table and verify the row names the fail-closed
      behavior

## 2. OpenSpec skills

- [x] 2.1 Update `openspec-propose`, `openspec-apply-change`, `openspec-archive-change`, `openspec-update-change`, and
      `openspec-sync-specs` to prefer `m42-ai openspec-instructions`, forbid inventing templates on failure, and
      discourage brittle `2>&1 | python json.load` pipes — verify each skill Markdown mentions the helper and
      stop-and-report guidance
- [x] 2.2 Add a one-line portable fallback (`env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`) where skills
      already document portable m42-ai forms — verify propose skill shows both wrapper and portable forms

## 3. Verification

- [x] 3.1 Run `uv run --project scripts/ai pytest` for the new tests and verify they pass
- [x] 3.2 Smoke: against this change, run
      `m42-ai openspec-instructions --artifact proposal --change openspec-instructions-plumbing` and verify exit 0 with
      `resolvedOutputPath`; run with `--change no-such-change` and verify non-zero + `agent_action: stop`
