# Design: review-fixer synced-path guard

## Context

See `proposal.md` for motivation (#45 / API#374). Today `docs/ai_review_policy.md` and the surface bar already push
“cheap + High practicality → fix,” and `/review-fixer` has no hard stop for synced trees in consumers. Sync (#13) and
README already say “do not hand-edit,” but that prose is not in the fixer decision order. Explore lock-ins: **A1**
allowlist file, **B2** follow-up vs dismiss gate, **C1** skill+policy+content in one PR, **D1** reuse
`follow-up`/`dismiss` (no `upstream` action).

## Goals / Non-Goals

**Goals:**

- One allowlist SoT (`docs/synced-paths.global.md`) that skill + policy + README point at.
- Decision-order hard stop before step 5 for synced paths in consumers.
- Close the two attached upstream findings in Devinfra (README dual-layout, atomic token write).

**Non-Goals:**

- Implementing sync automation / #13 manifest generator (allowlist may mirror Wave A by hand until sync owns it).
- Changing create-issue or issue-fixer OpenSpec rules.
- New triage action enum (`upstream`).
- Patching product repos from this PR.

## Decisions

### D1 — Allowlist file vs policy section vs skill-only

**Choice:** `docs/synced-paths.global.md` (A1). Skill and policy link; README Docs index links. Initial list curated
from issue AC + README “do not hand-edit” inventory; keep globs where useful (`scripts/ai/**`).

**Alternatives:** A2 (policy-only section) — harder to sync as a discrete artifact and bloats policy. A3 (skill-only) —
drifts from sync docs.

### D2 — Detecting “consumer vs Devinfra”

**Choice:** Heuristic in skill prose: if the checkout is this Devinfra repo (remote/name or path conventions documented
in skill), shared paths MAY be fixed; otherwise apply the hard rule. Prefer checking known remote
`fairagro/m4.2_middleware_devinfra` or equivalent when `gh`/`git` available; if unsure and paths match allowlist, treat
as consumer (safer: no local sync drift).

**Alternatives:** Env var `DEVINFRA_CHECKOUT=1` — extra product config. Always forbid edits to allowlisted paths even in
Devinfra — blocks fixing #45 content here via review-fixer (unacceptable).

### D3 — B2 follow-up gate

**Choice:** `follow-up` → Devinfra when Medium+ / Risk / seen-in-the-wild shared bug; else `dismiss` with
synced-upstream reason. Bundling still at most one follow-up issue per review-fixer run via create-issue when Medium+
items exist (existing rule); Low synced nits do not open issues.

**Alternatives:** B1 always follow-up — issue noise. B3 always dismiss — too weak for atomic-token class bugs.

### D4 — Atomic token write

**Choice:** Keep mktemp in same dir as store; append new line to temp; `mv -f tmp store` (POSIX rename). Preserve umask
077 / chmod 600 on the final file (chmod after mv if needed).

**Alternatives:** `install -m 600 tmp store` — fine if available in DC; prefer portable `mv`.

### D5 — README dual-layout

**Choice:** Lead consumer section with `--project scripts/ai`; keep Devinfra workspace section clearly labeled. Tests:
document both root pytest (Devinfra) and `--project scripts/ai pytest` (consumer).

## Risks / Trade-offs

- **[Allowlist drift vs sync manifest]** → Mitigation: comment in allowlist that #13 should eventually generate or
  validate against the same list; keep list short and glob-heavy.
- **[False consumer classification in forks of Devinfra]** → Mitigation: prefer remote match; document override in
  skill.
- **[Follow-up issues without GH write in product]** → Mitigation: existing auth / print-intended-create-issue path.
- **[Dismiss hides real shared bugs]** → Mitigation: B2 Medium+/Risk/seen-in-the-wild still follow-up.

## Migration Plan

1. Land allowlist + skill + policy + content on Devinfra; sync to products via #13.
2. No consumer migration step beyond next sync PR.
3. Rollback: revert commit; products remain as before until sync.

## Open Questions

None — explore lock-ins A1/B2/C1/D1 bind this design.
