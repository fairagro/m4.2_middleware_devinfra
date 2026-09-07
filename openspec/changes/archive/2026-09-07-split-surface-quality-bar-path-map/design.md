# Design: split surface quality bar path map

## Context

See proposal.md — Why. Today the path→surface table sits inside synced `docs/ai_review_policy.md`. Explore lock-in for
issue #32: **A′** Devinfra/synced default map = `docs/surface-quality-bar.global.md`; **B′** product overlay =
`docs/surface-quality-bar.md`; **C1** only the table (+ short how-to-read) moves; rules prose stays in the policy.

## Goals / Non-Goals

**Goals:**

- Extract the default map into `docs/surface-quality-bar.global.md`
- Point the policy (and skill pointers) at global map + optional product overlay
- Spec the sync/non-overwrite contract for the product file

**Non-Goals:**

- Changing step-5 / dismiss semantics of the surface quality bar
- Implementing sync (#13) automation in this change
- Moving rules prose into the map file (C2 rejected)
- Using `openspec/principles.md` as the product overlay (B2 rejected in favour of B′)

## Decisions

### D1 — Filenames mirror principles.global / principles

| File                                 | Role                                   | Sync         |
| ------------------------------------ | -------------------------------------- | ------------ |
| `docs/surface-quality-bar.global.md` | Default path→surface map               | Yes          |
| `docs/surface-quality-bar.md`        | Product (or Devinfra-local) extra rows | No overwrite |
| `docs/ai_review_policy.md`           | Rules + links to the two map files     | Yes          |

**Alternatives:** single `surface-quality-bar.md` everywhere (rejected — no clear sync vs local split); overlay only in
`openspec/principles.md` (rejected by lock-in B′).

### D2 — Map file content

Global file holds the current table from the policy (surfaces, typical paths, bar, exotic default) plus 2–4 lines on how
to read it and that products extend via `docs/surface-quality-bar.md`. Long “still fix when happy path broken”
paragraphs stay under the policy’s Surface quality bar section (C1).

### D3 — Devinfra may omit a local overlay

Devinfra need not ship a non-empty `docs/surface-quality-bar.md`; products create it when they need rows. Docs MUST
still describe the overlay path so sync consumers know the contract.

### D4 — Pointers

Update review-fixer / issue-fixer skill mentions and README docs index to cite the global map where they currently only
cite the policy section — without duplicating the table.

## Risks / Trade-offs

- [Two files to open for triage] → Mitigation: policy keeps a short link block; skills point at both
- [Sync list forgets to exclude product overlay] → Mitigation: document in map + quality/sync docs; #13 owns automation
- [Stale table copy if someone edits only the policy] → Mitigation: remove table from policy in this PR; link only

## Migration Plan

1. Land docs + spec delta + pointer updates on the issue branch.
2. Product adoption: after sync of `.global.md`, add local `docs/surface-quality-bar.md` when needed (no forced
   rewrite).
3. No rollback beyond restoring the table into the policy (undesirable).
