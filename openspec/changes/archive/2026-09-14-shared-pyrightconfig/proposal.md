## Why

Product checkouts (e.g. harvester Wave B) keep a local `pyrightconfig.json` for basedpyright/Pylance (`venv`,
`stubPath`, `scripts/ai` `extraPaths`). That drifts from Devinfra and invites post-sync hand-edits of what should be a
verbatim quality/IDE fragment ([#57](https://github.com/fairagro/m4.2_middleware_devinfra/issues/57)). Promote a shared
baseline so sync delivers one analysis config without product package path patches.

## What Changes

- Add root `pyrightconfig.json` with the issue baseline (`venvPath`/`venv`, `stubPath: stubs`,
  `extraPaths: [scripts/ai/src]`, common excludes) — no middleware / product-only paths.
- List it on `docs/synced-paths.yaml` (and human inventory in `docs/sync.md` if present).
- Document in `docs/quality.md`: basedpyright uses this file; product stubs under `stubs/`; do not put package paths in
  the synced blob; replace the “product-local until #64” wording.
- Light comment polish on `.vscode/settings.json` pointing at the shared fragment.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-python-quality-config`: shared Pyright/basedpyright fragment + adoption docs (stubs / no product path overlays
  in the synced file).

## Impact

- New allowlisted root config; quality/sync docs; OpenSpec main sync on archive.
- Products pick up the file on next sync; replace interim local copies (no product PR in this change).
