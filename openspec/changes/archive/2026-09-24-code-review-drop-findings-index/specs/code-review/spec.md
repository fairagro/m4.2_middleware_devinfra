## MODIFIED Requirements

### Requirement: Publish via formal PR Review or /tmp

When a PR is known and GitHub auth works, the skill MUST publish the report as a GitHub **Pull Request Review** with
event **COMMENT** (not REQUEST_CHANGES / APPROVE) using `m42-ai` (wrapping `gh pr review --comment` or equivalent). The
CLI path MUST remain low-effort — no custom GraphQL review mutation is required when `gh pr review` suffices.

When no PR is known, the skill MUST write the report to a file under `/tmp` (stable naming via `m42-ai`) and MUST NOT
require GitHub writes.

If posting a formal review fails after auth is available, the skill MAY fall back to a single PR conversation comment;
it MUST still retain the `/tmp` report.

The skill MUST NOT auto-LGTM. One publish per run (no silent spam loops).

Published report bodies (PR Review **and** `/tmp`) MUST start with the stable HTML comment marker
`<!-- m42-ai:code-review -->` so `/review-fixer` / `review-open` can treat the submission as a finder summary source
even under a human GitHub login.

Findings MUST use **numbered blocks** only (not a multi-column Markdown table, and not `###` headings per finding): each
finding is `N. **Title**` followed by bullets that carry at least **severity**, **cost**, **goal**, **path**, and
**note**. Empty findings MAY omit the list. The skill MUST NOT emit a separate “Findings index” (or equivalent) Markdown
table for machine consumption — `/review-fixer` extracts paths from the numbered **Path** bullets. The skill MUST NOT
rely on HTML `<table>` or images for the published review body.

#### Scenario: Local review writes /tmp only

- **WHEN** `/code-review` runs without a PR reference
- **THEN** `m42-ai` writes `/tmp/code-review-*.md` (or the documented pattern)
- **AND** no `gh pr review` or PR comment is attempted

#### Scenario: PR review posts COMMENT review

- **WHEN** `/code-review` runs with a valid PR and `GH_TOKEN` / `gh` auth is available
- **THEN** the report is submitted as a Pull Request Review with COMMENT event
- **AND** the review body contains the structured findings

#### Scenario: Report body carries review-fixer marker

- **WHEN** the skill writes a `/tmp` report or publishes a COMMENT review
- **THEN** the body begins with `<!-- m42-ai:code-review -->`
- **AND** findings use numbered blocks with a **Path** bullet so `review-open` can extract summary-only work
- **AND** the body does not include a Findings index Markdown table
