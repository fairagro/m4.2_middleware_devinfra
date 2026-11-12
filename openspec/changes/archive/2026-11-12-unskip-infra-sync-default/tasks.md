## 1. Workflow

- [x] 1.1 Update `.github/workflows/sync-products.yml`: `skip_infrastructure` default **false**; remove unconditional
      push `--skip-infrastructure`; refresh input description — verify push path no longer always skips Infra

## 2. Docs

- [x] 2.1 Update `docs/sync.md` push/dispatch wording for Infra included by default + how to skip — verify no “skipped
      until checklist” default
- [x] 2.2 Update `docs/renovate.md` Slice-2 checklist and `docs/synced-paths.yaml` comment for post-checklist default —
      verify dry-run/live steps no longer say push stays skipped

## 3. Validate

- [x] 3.1 Run `openspec validate unskip-infra-sync-default --strict` and Prettier on touched Markdown — verify clean
