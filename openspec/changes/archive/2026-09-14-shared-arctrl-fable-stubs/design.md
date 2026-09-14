## Context

See proposal.md — Why. Comments on #67: include `fable_library`; keep owslib/rdflib product-local; one-offs stay
per-import ignore; update arctrl skill only in Devinfra. `#64` landed `pyrightconfig.json` with `stubPath: stubs` on
main.

## Goals / Non-Goals

**Goals:** Synced incomplete stubs + README + allowlist + quality docs + skill guidance update.

**Non-Goals:** Full typed stubs; owslib/rdflib/lxml stub packages; product middleware PRs; mypy.ini module overrides.

## Decisions

1. **Copy harvester seed verbatim** for `stubs/arctrl/**` and `stubs/fable_library/**` (including sparse leaves).
2. **Fleet README** adapted from harvester `stubs/README.md` (Devinfra-owned wording; link #67/#64).
3. **Skill:** replace preferred pyproject override block with stubs/`MYPYPATH`/`stubPath`; strip ignores from
   illustrative imports for arctrl/fable; keep a short note for unrelated one-off libs.
4. **OpenSpec:** deltas on `shared-python-quality-config` and `shared-arctrl-skill`.

## Risks / Trade-offs

- **[Risk] Incomplete stubs hide real type errors inside arctrl** → Accepted; better than ignore_missing_imports /
  per-import spam; refine stubs later if needed.
- **[Risk] Products forget MYPYPATH** → Docs + README; CI inputs already support path overlays.

## Migration Plan

1. Land stubs + allowlist + docs + skill in Devinfra.
2. Sync; products drop arctrl/fable ignores; keep product-local owslib/rdflib stubs.
3. Rollback: revert allowlist/stubs; products can temporarily restore ignores.
