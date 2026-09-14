## 1. Fragment + allowlist

- [ ] 1.1 Add root `pyrightconfig.json` with the issue baseline JSON
- [ ] 1.2 Add `pyrightconfig.json` to `docs/synced-paths.yaml` and update `docs/sync.md` inventory if needed

## 2. Docs + settings comment

- [ ] 2.1 Update `docs/quality.md` (files table + IDE section: basedpyright, stubs, no product paths; remove “until
      #64”)
- [ ] 2.2 Align `.vscode/settings.json` comment to point at synced `pyrightconfig.json`
- [ ] 2.3 Format/lint only touched Markdown

## 3. Validate

- [ ] 3.1 `openspec validate shared-pyrightconfig --strict`
