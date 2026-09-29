## Context

Nit-budget and Fixed non-nit / cycle-abort live in `docs/ai_review_policy.md` (canonical) and are mirrored in
`.agents/skills/review-fixer/SKILL.md`. Spec contract is `openspec/specs/ai-review-policy`. Motivating case: API PR #520
dismissed correct shrink/cleanup Low comments after budget exhaustion, then humans overrode.

## Goals / Non-Goals

**Goals:**

- Always fix correct, this-PR, size-neutral/size-reducing Low findings; exclude them from nit-line spend.
- Preserve ~15-line budget for additive Low nits and new-abstraction ban.
- Keep cycle abort on Fixed non-nit = 0 even when only size-neutral Low fixes landed (no infinite loops).

**Non-Goals:**

- Changing Risk / step-5 rules, surface quality bar dismissals, or synced-path gates.
- Automating LOC measurement in `m42-ai` (agent judgment remains).
- Raising or removing the additive nit-budget cap.

## Decisions

1. **Net production LOC** — Compare production lines after the cheapest correct patch vs before (deletes and pure
   moves/relocations without new helpers count as ≤0). New named abstraction → still additive / not exempt.
2. **Fixed non-nit** — Size-neutral Low fixes stay outside Fixed non-nit so abort still fires after a shrink-only run;
   optional one additive-nit-only pass unchanged.
3. **Accounting** — Exempt fixes still post `nit-lines this run: 0` so prior-spend sums stay honest.
4. **Docs + skill only** — No OpenSpec capability beyond `ai-review-policy`; review-fixer skill text tracks the policy
   checklist (step 6 / budget paragraph).

## Risks / Trade-offs

- [Risk] Agents game “size-neutral” while sneaking small additions → Mitigation: policy text requires cheapest correct
  fix and forbids new abstractions; reviewers can still push back.
- [Risk] Endless shrink-only cycles if agents treat them as Fixed non-nit → Mitigation: explicit abort scenario.
- [Trade-off] Manual LOC estimate is soft (same class as today’s nit-lines tracking).

## Migration Plan

1. Land policy + skill wording on Devinfra.
2. Sync to products; no product code change required.
3. No data migration.
