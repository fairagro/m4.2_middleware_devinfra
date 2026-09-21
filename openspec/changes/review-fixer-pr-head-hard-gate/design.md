# Design: review-fixer PR-head hard gate

## Context

See `proposal.md` (Why). `ensure_pr_head` already fail-closed with a plain `RuntimeError` string; agents still
improvised. Put the stop contract in JSON the CLI owns.

## Goals / Non-Goals

**Goals:**

- Stable `error_code` + `agent_action: stop` on gate failure; `pr_head_ok` on success
- Skill reduced to “call CLI → honor JSON”
- Keep dirty-on-head allowed

**Non-Goals:**

- Auto-stash or agent-driven dirty-tree repair
- New subcommand (gate stays inside `review-open`)

## Decisions

1. **`PrHeadGateError.as_json()`** — codes: `dirty_wrong_branch`, `empty_head_ref`, `checkout_failed`,
   `checkout_branch_mismatch`. Alternative: string-match `error` in the skill — rejected.
2. **Success sets `ok` / `pr_head_ok` only when checkout ran** (`ensure_checkout=True`). Library callers with
   `ensure_checkout=False` keep shaping-only JSON without those flags.
3. **Skill cites CLI fields**, not a second prose checklist of dirty-tree cases.

## Risks / Trade-offs

- [Agents ignore `agent_action`] → Keep skill imperative and short; plumbing still refuse checkout.
- [Other RuntimeErrors lack `error_code`] → Generic fail JSON still sets `agent_action: stop`.

## Migration Plan

Ship CLI + skill together via sync. Products pick up both on next Devinfra sync.
