## MODIFIED Requirements

### Requirement: review-open shapes open AI work

`review-open` MUST emit JSON including: PR number/url, finder review round count, **all unresolved review threads**
(any first-comment author; JSON key MAY remain `unresolved_ai_threads` for compatibility), **every** finder review body
— author matching Copilot/Bugbot/Cursor heuristics **or** body containing the stable `/code-review` marker
`<!-- m42-ai:code-review -->` — with heuristically extracted suppressed / summary-only findings (`ai_reviews`,
`summary_only_findings`), and a convenience `latest_ai_review`, plus the PR head branch name after successful checkout.
Resolved threads MUST be omitted from the unresolved list. Round count and finder-review lists MUST include only
**submitted** finder reviews (non-null `submittedAt`, state not `PENDING`). Summary-only findings MUST NOT be limited
to the single latest finder review (a later Bugbot/Cursor/`code-review` submission MUST NOT hide earlier Copilot
suppressed comments except via the answered-summary selection rule). Only the latest **unanswered** summary finder
review contributes to `summary_only_findings` (at most one open summary review); a triage reply (`Fixed in` /
`Dismissed.` / `Follow-up:`, optionally with `#pullrequestreview-<id>`) after a summary review MUST mark it answered.
Only **submitted** non-finder review bodies count as such triage replies (PENDING / unsubmitted drafts MUST be ignored;
`/code-review` marked bodies MUST NOT count as triage replies). An optional `--review-id` MAY force that review’s
summary items into the open set for permalink triage. When GraphQL returns a null `pullRequest`, the CLI MUST fail with
a clear error naming owner/repo/PR. Summary-only findings MUST be marked non-resolvable. For `/code-review` bodies,
findings MUST be extracted from the Markdown findings table (header row with a `path` column).

#### Scenario: Fixture filters resolved and human threads

- **WHEN** `review-open` shaping runs on a recorded GraphQL fixture with resolved AI, open AI, and open human threads
- **THEN** both the open AI thread and the open human thread appear under unresolved threads
- **AND** the resolved AI thread is omitted
- **AND** round_count counts finder review submissions only
- **AND** Copilot suppressed / summary-only findings remain available when unanswered

#### Scenario: Pending AI reviews are excluded

- **WHEN** GraphQL includes an AI review with null `submittedAt` or state `PENDING`
- **THEN** that review is omitted from `round_count` and `ai_reviews`
- **AND** it does not affect suppressed-review selection

#### Scenario: Pending non-AI draft reviews do not answer suppressed findings

- **WHEN** GraphQL includes a non-AI review with state `PENDING` (or null `submittedAt`) whose body looks like a triage
  reply (`Fixed in` / `Dismissed.` / `Follow-up:`)
- **THEN** that draft MUST NOT mark any suppressed AI review as answered
- **AND** submitted non-finder triage review bodies and issue comments continue to mark suppressed reviews answered as
  before

#### Scenario: Human-login code-review COMMENT is summary-packed

- **WHEN** GraphQL includes a submitted review under a human login whose body starts with `<!-- m42-ai:code-review -->`
  and a findings table with a `path` column
- **THEN** that review is included in `ai_reviews` / `round_count`
- **AND** its table rows appear under `summary_only_findings` when it is the open unanswered summary review
- **AND** those findings are marked non-resolvable
