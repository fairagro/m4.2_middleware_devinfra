## ADDED Requirements

### Requirement: Code Quality thread resolve is not finding dismiss

The review-fixer skill and `docs/review-fixer.md` MUST document that resolving a `github-code-quality` (or equivalent)
review thread — including posting `Dismissed.` / `Fixed in …` and `resolveReviewThread` — does **not** dismiss the
linked GitHub Code Quality finding or necessarily unblock Code Quality merge gates. Until a documented dismiss API
exists, agents MUST instruct **manual Dismiss finding** in the PR UI (or rely on a real code fix + re-scan) when a
linked finding remains `state: open` or when a CQ bot thread has no enrichment but findings may still be open. Phase 1
output MUST NOT claim Remaining risk / open work is clear solely because such threads were resolved while findings stay
`open`. Preferring a future `code-quality-dismiss` CLI is out of scope for this change and MAY be noted as follow-up
only.

#### Scenario: Agent dismisses a CQ false positive

- **WHEN** triage chooses `dismiss` on an unresolved Code Quality bot thread (optionally with linked finding
  `state: open`)
- **THEN** the skill still posts the usual dismiss reply and may resolve the thread
- **AND** Phase 1 output explicitly states that manual **Dismiss finding** (or re-scan after a real fix) is still
  required while the finding remains open
- **AND** the skill does not treat thread resolve alone as clearing Code Quality gate risk

#### Scenario: Docs spell out the gap

- **WHEN** a contributor reads `docs/review-fixer.md` (or the skill Auth/fetch sections)
- **THEN** they learn thread resolve ≠ Code Quality dismiss
- **AND** they learn findings REST is read-only for agents today
