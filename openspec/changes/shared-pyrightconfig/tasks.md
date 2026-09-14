## 1. Fragment + allowlist

- [x] 1.1 Add root `pyrightconfig.json` with the issue baseline JSON
- [x] 1.2 Add `pyrightconfig.json` to `docs/synced-paths.yaml` and update `docs/sync.md` inventory if needed

## 2. Docs + settings comment

- [x] 2.1 Update `docs/quality.md` (files table + IDE section: basedpyright, stubs, no product paths; remove “until
      #64”)
- [x] 2.2 Align `.vscode/settings.json` comment to point at synced `pyrightconfig.json`
- [x] 2.3 Format/lint only touched Markdown

## 3. Validate

- [x] 3.1 `openspec validate shared-pyrightconfig --strict`
