# review-fixer Delta

## ADDED Requirements

### Requirement: Never modify synced paths in consumer checkouts

The `/review-fixer` skill MUST instruct agents never to modify paths listed in `docs/synced-paths.global.md` (or
matching globs) when running in a **product consumer** checkout. On a finding whose primary path is synced, the skill
MUST NOT choose action `fix` against that synced tree. Instead it MUST:

- use action `follow-up` (via create-issue against **Devinfra**, or a clear Devinfra-targeted follow-up) when the
  finding is correct for shared content and severity is Medium or higher, or the finding is Risk, or it is a known
  seen-in-the-wild shared bug; **or**
- use action `dismiss` with reason that the path is synced and must be edited upstream in Devinfra / wait for sync, when
  the item is a Low nit or otherwise not follow-up-worthy; **or**
- use action `fix` only on an **explicit product-local overlay** path documented in the allowlist (never by editing
  `.global` / synced trees).

Phase-1 triage output MUST label such items with existing actions (`follow-up` / `dismiss` / overlay `fix`) and a clear
reason that names the synced-path rule (no new action enum). After the run, the working tree MUST NOT contain dirty
edits under synced paths from fixer work. When `/review-fixer` runs **inside this Devinfra repository**, synced-path
files are the local source of truth and MAY be fixed here like any other in-repo path.

#### Scenario: Synced-path finding in a product PR is not fixed locally

- **WHEN** `/review-fixer` triages a correct cheap finding on `scripts/ai/README.md` (or another allowlisted synced
  path) in a product consumer PR
- **THEN** the skill does not apply a local patch to that synced file
- **AND** the phase-1 action is `follow-up` (Devinfra) or `dismiss` per the Medium+/Risk/seen-in-the-wild gate
- **AND** the working tree has no fixer-introduced dirty edits under that synced path

#### Scenario: Documented overlay may still be fixed in the consumer

- **WHEN** a finding targets a documented product-local overlay (e.g. `docs/surface-quality-bar.md`)
- **THEN** the skill MAY choose `fix` on that overlay path
- **AND** it MUST NOT edit the synced `.global` counterpart to satisfy the finding

#### Scenario: Devinfra checkout may fix shared content

- **WHEN** `/review-fixer` runs on a PR in the Devinfra repository itself
- **THEN** findings on allowlisted shared paths MAY be fixed in that checkout
- **AND** the consumer synced-path hard rule does not apply
