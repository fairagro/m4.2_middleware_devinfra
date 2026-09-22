## ADDED Requirements

### Requirement: uv-audit ignore overlay is product-owned

`docs/synced-paths.yaml` MUST list the uv-audit accepted-risk ignore file (path chosen at apply; default
`.uv-audit-ignore`) under `overlays` so sync never overwrites product-local advisory ID ignores. Documentation
(`docs/sync.md` and/or `docs/quality.md`) MUST name the path and how the shared runner applies it.

#### Scenario: Ignore file listed as overlay

- **WHEN** a contributor inspects sync overlays documentation for uv audit
- **THEN** the ignore file path appears under `overlays`
- **AND** sync does not wipe product-local ignore entries
