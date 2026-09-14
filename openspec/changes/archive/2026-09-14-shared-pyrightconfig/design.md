## Context

See proposal.md — Why. Issue #64 lock-in: exact JSON baseline from the issue; allowlist + `quality.md`; OpenSpec on
`shared-python-quality-config`. Related: #57 never-patch synced blobs; settings.json already points analysis overlays at
pyrightconfig.

## Goals / Non-Goals

**Goals:**

- One verbatim `pyrightconfig.json` for Devinfra + products after sync.
- Docs that close the “until #64” interim and forbid product path patches in the synced file.

**Non-Goals:**

- Mypy config-merge; product `middleware/` `extraPaths`; `dev_environment` exclude in the shared file.
- Migrating product repos in this PR (sync + follow-up adopt only).

## Decisions

1. **Baseline matches the issue JSON** — already validated in harvester interim; keep identical keys/values.
2. **`stubPath: stubs` even when Devinfra has no stubs tree** — harmless when absent; products that need third-party
   silence keep stubs product-local (not in `mypy.ini`).
3. **Capability: `shared-python-quality-config`** — same family as ruff/mypy/pylint fragments, not a new capability.
4. **Settings.json** — keep `python.analysis.extraPaths` for scripts/ai if already present (parity / pre-interpreter);
   comments MUST point at synced `pyrightconfig.json` as the Pyright SoT, not “product-local until #64”.

## Risks / Trade-offs

- **[Risk] Empty `stubs/` in Devinfra** → Mitigation: Pyright tolerates missing stubPath dir; optional empty
  `stubs/.gitkeep` only if tools complain (default: omit).
- **[Risk] Products still patch extraPaths after sync** → Mitigation: docs + #57; review-fixer synced-path rule.

## Migration Plan

1. Land Devinfra file + allowlist + docs.
2. Sync to products; products delete divergent local keys that duplicate the baseline.
3. Rollback: drop allowlist entry / revert file; products can temporarily keep local copy.
