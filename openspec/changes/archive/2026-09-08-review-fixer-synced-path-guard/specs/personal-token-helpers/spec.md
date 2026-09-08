# personal-token-helpers Delta

## ADDED Requirements

### Requirement: Token store writes are atomic

`_dev_tokens_write` (or equivalent in `scripts/dev-tokens.sh`) MUST replace `/commandhistory/tokens.env` (or the
resolved store path) with an **atomic** update: write the complete new contents to a temporary file in the same
directory, then replace the destination via `mv` (or equivalent rename). It MUST NOT truncate the destination via shell
redirect (`cat … >store`) after the temp file is complete. Interrupt or ENOSPC during the write MUST NOT leave a
truncated existing store when a prior complete store existed (best-effort: failed rename leaves the previous file
intact).

#### Scenario: Write replaces store via rename

- **WHEN** `_dev_tokens_write` persists a new or updated token value
- **THEN** it finishes the temp file before replacing the store path
- **AND** the replacement uses rename/`mv` rather than redirecting onto the live store file

#### Scenario: Failed mid-write does not wipe prior store via redirect

- **WHEN** writing the temp file fails before rename
- **THEN** the previous tokens store file remains unchanged when it already existed
