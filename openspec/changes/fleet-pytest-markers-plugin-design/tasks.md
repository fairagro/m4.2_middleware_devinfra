## 1. Docs lock-in

- [x] 1.1 Update `docs/quality.md` pre-push / deferred #123 wording to state the **locked** plan: fleet markers SoT =
      pytest plugin (product `testpaths`/`pythonpath` stay local); coverage fragment deferred as a follow-up; point at
      this change name — verify the old “hand-copy / do not invent SoT here” text is consistent and does not claim the
      plugin already ships
- [x] 1.2 Comment on GitHub issue #123 summarizing the design lock-in (plugin first, coverage later, design-only PR) and
      verify the comment is visible on the issue

## 2. Validate

- [x] 2.1 Run `openspec validate fleet-pytest-markers-plugin-design --strict` and confirm pass (`skip_specs: true`, no
      delta spec files)
- [x] 2.2 Confirm working tree has **no** new pytest plugin package, coverage fragment, or `synced-paths.yaml` allowlist
      entry for unimplemented paths
