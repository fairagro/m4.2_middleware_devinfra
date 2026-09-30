## MODIFIED Requirements

### Requirement: issue-start

`issue-start` MUST, on a clean working tree/index: ensure branch `{channel}/issue-<n>-<slug>` exists (create from `main`
if needed after fetch + fast-forward pull of the base), refuse when `HEAD` is not ahead of the base, push the tip, and
open a draft PR whose body includes `Fixes #<n>`. `{channel}` MUST be one of `build`, `ci`, or `docs` (default `build`
when the caller does not pass a channel). It MUST NOT create empty bootstrap commits. It MUST NOT mark the PR ready. The
draft PR body MUST NOT include tool marketing footers such as “Made with Cursor”. Fetch + fast-forward pull of the base
branch MUST succeed before creating a missing issue branch (MUST NOT ignore pull failures).

When the caller does **not** pass a body override, the draft PR body MUST be a Markdown Summary whose bullets are
derived from the issue title and the short subject list of commits ahead of the base (`git log` subjects, capped), and
MUST end with `Fixes #<n>`. It MUST NOT use a placeholder such as `MVP scope: (fill in)` as the Summary content.

`issue-start` MUST accept an optional body override (`--body` and/or `--body-file`). When provided, that text is the PR
body; if it does not already contain `Fixes #<n>`, the CLI MUST append `Fixes #<n>`.

#### Scenario: Dirty tree refuses issue-start

- **WHEN** `issue-start` is invoked with a dirty working tree or index
- **THEN** it exits non-zero without creating a branch or PR

#### Scenario: Tip equals base refuses issue-start

- **WHEN** `issue-start` is invoked and `HEAD` has no commits ahead of the base
- **THEN** it exits non-zero without creating an empty commit or opening a PR

#### Scenario: issue-start PR body has no Cursor footer

- **WHEN** `issue-start` opens a draft PR
- **THEN** the body contains `Fixes #<n>`
- **AND** it does not contain “Made with Cursor”

#### Scenario: issue-start uses channel prefix

- **WHEN** `issue-start` creates a missing branch with `--channel ci`
- **THEN** the branch name is `ci/issue-<n>-<slug>`

#### Scenario: Default body is not the fill-in stub

- **WHEN** `issue-start` opens a draft PR without a body override and `HEAD` is ahead of the base
- **THEN** the body Summary does not consist of `MVP scope: (fill in)`
- **AND** the body includes at least one descriptive Summary bullet (issue title and/or commit subject)
- **AND** the body includes `Fixes #<n>`

#### Scenario: Body-file override wins and keeps Fixes

- **WHEN** `issue-start` is invoked with `--body-file` containing a crafted Summary without `Fixes #<n>`
- **THEN** the opened PR body uses that Summary content
- **AND** `Fixes #<n>` is present (appended if it was missing)
