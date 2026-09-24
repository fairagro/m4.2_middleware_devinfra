## ADDED Requirements

### Requirement: review-open enriches Code Quality findings

When shaping open work, `review-open` MUST attempt to load repository Code Quality findings via the documented read-only
REST API (`GET …/code-quality/findings`, including required preview Accept headers when GitHub documents them). For each
unresolved review thread whose first comment author is the GitHub Code Quality bot (`github-code-quality` or documented
equivalent), the CLI MUST attach correlatable finding metadata when a single best match exists (at least path agreement
with the finding location; prefer matching rule id/title or message text). Attached fields MUST include finding `number`
and `state` (`open` | `dismissed`) and SHOULD include rule id when present. When the API is unavailable, returns an
error, or no unique match exists, enrichment MUST be omitted without failing `review-open`. The CLI MUST NOT call any
dismiss/write Code Quality endpoint (none is supported in this change).

#### Scenario: Fixture attaches open finding to CQ thread

- **WHEN** `review-open` shapes a fixture with an unresolved `github-code-quality` thread and a matching open finding
  for the same path/rule
- **THEN** that thread’s JSON includes finding `number` and `state: open`
- **AND** non-CQ threads are unchanged

#### Scenario: Findings API failure is soft

- **WHEN** the Code Quality findings request fails or the endpoint is missing
- **THEN** `review-open` still exits successfully with open-work JSON
- **AND** CQ threads omit finding enrichment rather than failing the command
