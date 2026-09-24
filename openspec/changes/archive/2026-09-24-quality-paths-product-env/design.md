## Context

See proposal.md. Lock-in **A**: `.devcontainer/product.env` as single source; CI + `run-quality-cli.sh` re-read;
explicit workflow inputs override.

## Goals / Non-Goals

**Goals:**

- Empty `mypy_path` / `pylint_source_roots` → load `MYPYPATH` / `PYLINT_SOURCE_ROOTS` from product env file.
- Local hooks pick up file edits without container rebuild when those env vars are unset in the process.
- Docs + pointer to Harvester #299.

**Non-Goals:**

- Migrating product workflows in this PR.
- A separate `.quality-paths.env` (option B).
- Patching synced `mypy.ini` / `.pre-commit-config.yaml` with product paths.

## Decisions

1. **Default file** — `.devcontainer/product.env` (already overlay / Compose `env_file`). Optional workflow input
   `quality_env_file` defaults to that path for products that rename later.
2. **Parse style** — safe KEY=VALUE grep/source of only `MYPYPATH` and `PYLINT_SOURCE_ROOTS` (ignore comments/blank; do
   not `source` the whole file blindly if it may contain shell). Prefer a small shared bash helper used by CI step and
   `run-quality-cli.sh`.
3. **Override order** — process env / explicit workflow input wins if non-empty; else file; else unset.
4. **Pylint** — same file key `PYLINT_SOURCE_ROOTS` maps to reusable input / `--source-roots` (comma-separated as
   today).
5. **Missing file** — soft-skip (no fail); behavior matches today’s empty inputs.

## Risks / Trade-offs

- [Risk] Blind `source` of product.env executes arbitrary shell → Mitigation: parse only allowed keys.
- [Risk] Pre-commit already has MYPYPATH from stale Compose → Mitigation: document that non-empty process env wins; for
  live edits, unset or rebuild once, or rely on file when unset; helper only fills when unset.
- [Risk] Products keep duplicating inputs → Mitigation: docs + Harvester #299; inputs remain for gradual migrate.
