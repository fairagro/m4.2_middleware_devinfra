## 1. Checker script

- [x] 1.1 Add `scripts/commit-path-check.sh` (parse commit message type; classify staged paths; implement reject matrix
      from design) — verify executable and `--help` / usage when message file missing
- [x] 1.2 Add focused fixtures/tests (propose-only `feat`, archive+specs `feat`, test-only `fix`, `chore` archive OK,
      mixed shipped+test `feat` OK, `docs` archive reject) — verify they pass under `uv run` / bash harness

## 2. Hook + sync

- [x] 2.1 Wire commit-msg hook in `.pre-commit-config.yaml` beside commitlint — verify
      `pre-commit run commit-path-check     --hook-stage commit-msg` (or documented invoke) rejects a fixture
      message+paths case
- [x] 2.2 Add script to sync allowlist (`docs/synced-paths.yaml` / `docs/sync.md` as needed) — verify path listed

## 3. Docs

- [x] 3.1 Update `docs/quality.md` Conventional Commits section: path-check is live (not “future”), reject matrix,
      `--no-verify` escape, coexistence with agent handoff — verify Prettier/markdownlint on touched docs

## 4. Validate

- [x] 4.1 Run `openspec validate commit-path-check --strict` — verify exit 0
