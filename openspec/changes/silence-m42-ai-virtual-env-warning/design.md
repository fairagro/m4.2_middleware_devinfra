## Context

See proposal.md — Why. Product DCs keep `VIRTUAL_ENV=/workspace/.venv` while `m42-ai` runs under `scripts/ai/.venv` via
`--project scripts/ai`. Skills currently document the noisy `uv run --project scripts/ai m42-ai …` form. `scripts/bin`
is already on `PATH` via `remoteEnv` and synced to products for `gh` / `git` / shortcuts.

## Goals / Non-Goals

**Goals:**

- One silent primary invoke for agents when `scripts/bin` is on `PATH`.
- Portable silent fallback without the wrapper (`env -u VIRTUAL_ENV …`).
- Preserve DC `VIRTUAL_ENV` and product `--project scripts/ai` layout.

**Non-Goals:**

- Changing uv, installing `m42-ai` into the root `.venv`, or using `--active`.
- Removing or renaming Dev Container `VIRTUAL_ENV`.
- Changing Python CLI entry points or package layout under `scripts/ai/`.

## Decisions

1. **Wrapper as primary silence path** — Add `scripts/bin/m42-ai` that `unset VIRTUAL_ENV` then
   `exec uv run --project "$repo_root/scripts/ai" m42-ai "$@"`. Prefer this over documenting only `env -u` because
   agents already resolve other tools via `scripts/bin`, and a short `m42-ai …` form is less error-prone than a long
   prefix on every skill example.
   - Alternative considered: skill-only `env -u VIRTUAL_ENV uv run …` with no wrapper — works, but longer templates and
     easy to omit the prefix in new docs.
   - Alternative considered: `--active` — rejected by issue AC (would target root `.venv`).

2. **Skills document wrapper first, `env -u` as portable equivalent** — Primary examples become `m42-ai …`. Auth
   sections note that the wrapper unsets conflicting `VIRTUAL_ENV`, and that without `scripts/bin` on `PATH` agents MUST
   use `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`. Bare `uv run m42-ai` remains Devinfra-only (workspace
   member), not primary for products.

3. **Allowlist + PATH only** — Sync the wrapper via `docs/synced-paths.yaml` like other `scripts/bin/*` files. No bashrc
   changes; discovery stays `scripts/bin` on `PATH`.

4. **Resolve project root from wrapper location** — `$(cd "$(dirname …)/../.." && pwd)` is wrong (`scripts/bin` → repo
   root is `../..` from bin? `scripts/bin` → `dirname` = scripts/bin, `../..` = repo root). Correct: `_dir/../..` from
   `scripts/bin` = workspace root. Use `$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)` — wait: `scripts/bin` →
   `..` = `scripts`, `../..` = repo root. Yes.

## Risks / Trade-offs

- [Name collision] → If someone has another `m42-ai` earlier on `PATH`, wrapper never runs. Mitigation: DC `remoteEnv`
  already prepends `scripts/bin`; document that fact in README.
- [Stale skill examples still using raw uv] → Agents keep seeing warnings until skills update. Mitigation: this change
  updates all four synced fixer skills + thin docs + agent-ai-gh contract.
- [Wrapper unused when agent copies old `uv run --project` without env -u] → Still noisy. Mitigation: specs require
  primary form to be silent; leftover raw form is non-primary.

## Migration Plan

1. Land wrapper + allowlist + docs/skills/spec deltas together.
2. Product sync picks up `scripts/bin/m42-ai` on next sync PR.
3. No rollback beyond reverting the commit; DC env unchanged.

## Open Questions

None.
