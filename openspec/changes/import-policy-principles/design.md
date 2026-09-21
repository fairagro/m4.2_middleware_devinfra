## Context

See `proposal.md` / [#156](https://github.com/fairagro/m4.2_middleware_devinfra/issues/156). Explore locked A–D and
retyped Feature. Comments already locked module-level imports and absolute `middleware.…` imports.

Today `openspec/principles.global.md` has no Import policy. `/code-review` goal 5 is judgment-only with no shared text
to apply.

## Goals / Non-Goals

**Goals:**

- Normative Import policy (rules 1–7 + A–D) in `principles.global.md`
- Agent pointer from code-review skill + `docs/code-review.md`
- Spec deltas for `global-principles` and `code-review`

**Non-Goals:**

- Cleaning product repos (harvester #155 / #140)
- Landing import-linter / vulture
- Changing Ruff isort settings or enforcing via CI in this change

## Decisions

### D1: Home = principles.global.md

Shared, synced to products. Keep product-specific graphs in local `principles.md` / specs.

### D2: Section placement

Add **Import policy** after **Code Quality** (or before Testing) so quality + import rules sit together.

### D3: Agent pointer

Update `.agents/skills/code-review/SKILL.md` goal 5 and `docs/code-review.md` Anti-duplication / import note to cite
`openspec/principles.global.md` Import policy. Do not fork a product-only skill.

### D4: A–D text

Encode explore lock-ins verbatim in the principles section (eager absolute `__init__` OK when acyclic; registration
side-effect module; no runtime shims; tests that import app code follow the same rules).

## Risks / Trade-offs

- **[Risk]** Existing product code violates the policy on sync → Mitigation: policy is normative for new work/reviews;
  cleanup stays product issues
- **[Risk]** Over-long principles file → Mitigation: keep rules numbered and tight; no product examples

## Migration Plan

1. Land principles + skill/doc + OpenSpec sync via draft PR `Fixes #156`.
2. After product sync, agents see the rules; optional product cleanup issues separately.

## Open Questions

None — A–D locked in explore.
