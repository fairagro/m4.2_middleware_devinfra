# Design: review-fixer PR-head hard gate

## Context

See `proposal.md` (Why). CLI `ensure_pr_head` already fail-closes; the gap is agent skill wording that was easy to
bypass after a failed checkout.

## Goals / Non-Goals

**Goals:**

- Skill text that agents cannot reasonably skip: first action = `review-open`, then gate on branch match
- Explicit forbidden recoveries: stash, force checkout, silent branch restore
- Align with existing CLI (dirty on head OK)

**Non-Goals:**

- Changing `ensure_pr_head` / GraphQL shaping
- Auto-stashing or agent-driven dirty-tree repair
- New CLI flags

## Decisions

1. **Skill-only hardening** — raise the existing “Ensure PR head” requirement rather than new plumbing. Alternative: CLI
   wrapper that refuses to print open-work JSON without checkout — already true; agents still need stop rules.
2. **Place a short “First hard gate” block near the top of the PR-known path** (before Fetch / triage detail), plus
   tighten the existing Fetch section. Alternative: only deepen Fetch — rejected; agents skim past mid-skill prose.
3. **Thin docs get at most one sentence** pointing at the skill gate; no duplicate procedure.

## Risks / Trade-offs

- [Agents still improvise despite text] → Keep language imperative and short; cite fail-closed CLI error as the stop
  signal.
- [User wants agent to stash for them] → Out of scope; user cleans the tree or switches branch, then re-runs.

## Migration Plan

Sync skill to products. No rollback beyond reverting skill text.
