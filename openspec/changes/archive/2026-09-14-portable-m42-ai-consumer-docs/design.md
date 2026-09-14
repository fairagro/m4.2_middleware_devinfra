## Context

See proposal.md — Why. `scripts/ai/README.md` already documents Devinfra workspace vs consumer `--project` layouts.
Fixer skills and thin docs still lead with bare `uv run m42-ai`, which breaks in products. `scripts/ai` already ships
pytest via `dependency-groups.dev` + `default-groups`. `docs/conventions.md` and `docs/quality.md` are on the sync
allowlist. Explore lock-in: prefer `--project` everywhere in skills; keep conventions links; soften principles Code
Quality; treat pytest as verify-only unless broken.

## Goals / Non-Goals

**Goals:**

- One portable primary invoke in synced fixer skills + thin docs
- Specs match that contract for `agent-ai-gh` and the three fixer skills
- Principles Code Quality readable without assuming missing files
- pytest `--project` path remains green

**Non-Goals:**

- Changing CLI behavior or auth model
- Forcing products to add `scripts/ai` to the root workspace
- Syncing extra auth docs beyond `docs/conventions.md`
- Rewriting all of `principles.global.md` beyond Code Quality portability

## Decisions

1. **Primary invoke = `uv run --project scripts/ai m42-ai …`**
   - **Why:** Works in both layouts; agents copy skill examples verbatim.
   - **Alt considered:** Dual examples everywhere — rejected; skills stay short; README already has the dual layout.
2. **pytest: verify, don't re-architect**
   - **Why:** Already `default-groups = ["dev"]` with pytest; AC is satisfied if clean `--project` collect works.
   - **Alt:** Move pytest to main `dependencies` — unnecessary with default-groups.
3. **`docs/conventions.md` stays**
   - **Why:** Now synced; no second path.
4. **Principles: soft fragment wording, keep gate list**
   - **Why:** Fragments + `docs/quality.md` are synced for Wave A; still word so older/partial checkouts aren't pushed
     toward illegal `Any` / second configs.
5. **Delta specs on five capabilities**
   - Real contract change for how skills document CLI; not `skip_specs`.

## Risks / Trade-offs

- **[Risk] Devinfra agents type longer commands** → Mitigation: one-line note that bare `uv run m42-ai` still works when
  workspace member; `--project` is correct in Devinfra too.
- **[Risk] Thin Cursor commands/prompts omit examples** → Mitigation: update only files that embed bare `uv run m42-ai`;
  leave pure “follow skill” stubs alone.
- **[Risk] Drive-by Prettier on whole tree** → Mitigation: format only touched Markdown paths.

## Migration Plan

1. Merge this change; products pick up on next skill/`scripts/ai`/`principles.global.md` sync.
2. No product-local patches; no rollback beyond revert of the sync blob.
