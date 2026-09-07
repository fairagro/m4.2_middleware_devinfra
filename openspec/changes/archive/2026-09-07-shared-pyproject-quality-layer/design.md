# Design: shared Python quality config fragments

## Context

See proposal.md — Why. Explore lock-ins for issue #28: **A2** (quality only), **B2** (fragments), **D1** (no product
smoke PR), Dockerfile deferred with **base Dockerfile + local last stage**. `#10` Dev Container base exists; `#13` will
sync paths later.

## Goals / Non-Goals

**Goals:**

- One editable source of truth in Devinfra for shared ruff / mypy / pylint (and closely related) settings aimed at
  `middleware/` products.
- Clear docs: sync set vs product-local `pyproject.toml` vs Devinfra `scripts/ai/pyproject.toml`.

**Non-Goals:**

- Dockerfile artifacts in this change.
- Full product `pyproject.toml` replace; pytest/coverage unification unless trivially shared.
- Live adoption PR in a product repo (D1).

## Decisions

1. **Fragment files (B2), not section-merge into product pyproject**
   - **Choice:** Ship e.g. `ruff.toml`, `mypy.ini` (or `mypy.toml`), `.pylintrc` (exact names locked in tasks from tool
     defaults and current pre-commit invocation).
   - **Why:** Sync = overwrite file; no TOML region merge; product keeps `[project]` / uv workspace.
   - **Alternative (B1):** rejected for MVP.

2. **Layout path**
   - **Choice:** Place fragments at **repo root** of Devinfra (same paths products will use after sync), e.g. root
     `ruff.toml`, so sync mapping is 1:1 and tools’ default discovery works in consumers.
   - **Why:** Ruff/mypy discover config from CWD; matches product checkout layout after #13.
   - **Alternative:** `config/quality/` prefix — needs hook `--config` everywhere; deferred unless conflicts with
     Devinfra’s own minimal `[tool.ruff]` in root `pyproject.toml`.

3. **Coexistence with Devinfra root `pyproject.toml`**
   - **Choice:** Keep Devinfra root `pyproject.toml` minimal (workspace + thin tool stubs). Prefer **fragment files
     win** for ruff when both exist — verify ruff precedence (explicit `ruff.toml` typically overrides); adjust Devinfra
     stubs or document “Devinfra uses fragments too” so local `uv run ruff` is consistent.
   - **Why:** One mental model; avoid divergent Devinfra vs product rules.

4. **`scripts/ai/pyproject.toml`**
   - **Choice:** Keep unchanged; **exclude** from product quality sync allowlist.
   - **Why:** Package manifest for `m42-ai-gh`, not product tooling.

5. **Content seed**
   - **Choice:** Extract shared middleware-oriented settings from `m4.2_advanced_middleware_api` root `pyproject.toml`
     `[tool.ruff|mypy|pylint…]` as the starting point; strip product-only paths if any; keep `middleware/`
     excludes/targets.
   - **Why:** API is the richest current source; other products align toward it.

6. **Dockerfile follow-up (not implemented here)**
   - **Choice:** Sub-issue: unify three product Dockerfiles to the same stages, then one **shared base Dockerfile** with
     ARGs for package/binary differences, plus a **thin product-local last stage** (CMD/labels/ports).
   - **Why:** User lock-in; keeps #28 PR focused.

## Risks / Trade-offs

- **[Risk] Devinfra root pyproject `[tool.ruff]` vs `ruff.toml` confusion** → Mitigation: decision 3; smoke `ruff check`
  locally in Devinfra after landing fragments.
- **[Risk] Product mypy_path / pyright paths differ** → Mitigation: document local overrides; keep path lists minimal or
  documented as “extend locally”.
- **[Trade-off] Pytest/coverage stay duplicated** → Accepted for MVP.

## Migration Plan

1. Land fragments + docs on this branch / draft PR (`Fixes #28` for the narrowed MVP; link Dockerfile sub-issue).
2. #13 syncs fragment paths into products; products delete redundant `[tool.*]` blocks from root pyproject in adoption
   PRs.
3. Dockerfile sub-issue implements base + last-stage separately.

## Open Questions

None for MVP (lock-ins closed).
