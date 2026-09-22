## MODIFIED Requirements

### Requirement: issue-start

`issue-start` MUST, on a clean working tree/index: ensure branch `{channel}/issue-<n>-<slug>` exists (create from `main`
if needed after fetch + fast-forward pull of the base), refuse when `HEAD` is not ahead of the base, push the tip, and
open a draft PR whose body includes `Fixes #<n>`. `{channel}` MUST be one of `build`, `ci`, or `docs` (default `build`
when the caller does not pass a channel). It MUST NOT create empty bootstrap commits. It MUST NOT mark the PR ready. The
draft PR body MUST NOT include tool marketing footers such as “Made with Cursor”. Fetch + fast-forward pull of the base
branch MUST succeed before creating a missing issue branch (MUST NOT ignore pull failures).

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

### Requirement: issue-branch and branch-ahead

`issue-branch` MUST, on a clean working tree/index: ensure `{channel}/issue-<n>-<slug>` exists (create from base after
fetch + fast-forward pull when missing), check it out, and MUST NOT commit, push, or open a PR. `{channel}` MUST be one
of `build`, `ci`, or `docs` (default `build`). `branch-ahead` MUST fetch `origin/<base>` before counting, print JSON
with `base`, `upstream` (`origin/<base>`), `current_branch`, `ahead`, and `ok` (`true` iff `ahead > 0`), and MUST exit
non-zero when not ahead.

#### Scenario: issue-branch creates without PR

- **WHEN** `issue-branch` runs and the local issue branch is missing
- **THEN** it creates and checks out `{channel}/issue-<n>-<slug>` from the base
- **AND** it does not push or open a PR

#### Scenario: issue-branch default channel is build

- **WHEN** `issue-branch` runs without an explicit channel
- **THEN** the branch name starts with `build/issue-`

#### Scenario: branch-ahead exit code

- **WHEN** `branch-ahead` runs and `HEAD` equals the base tip
- **THEN** JSON has `ok: false` and `ahead: 0`
- **AND** the process exits non-zero
