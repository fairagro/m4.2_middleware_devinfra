## 1. Workflow + docs

- [x] 1.1 Add `.github/workflows/reusable-registry-retry.yml` with `workflow_call` inputs (`git_tag`, `release_kind`,
      `retry_dockerhub`, `retry_ghcr`, Docker/Helm naming inputs as needed) and verify YAML validates (`actionlint` if
      available, or `gh workflow view` / dry structural review)
- [x] 1.2 Implement Docker path: checkout `git_tag` → Bake rebuild → selective registry pushes; verify no tag/Release
      create steps exist in that path
- [x] 1.3 Implement Helm final path: download Release `.tgz` for `git_tag` → selective `helm push`; verify no version
      bump/tag create
- [x] 1.4 Implement GitHub Release body update replacing `## Registry status` only; verify other sections preserved in a
      fixture/snippet test or documented dry example
- [x] 1.5 Fail closed when `retry_dockerhub: true` without secrets and when neither registry flag is true; verify error
      messages are clear in workflow `if:` / step logic

## 2. Documentation

- [x] 2.1 Update `docs/ci.md` with registry-retry section (inputs table, secrets, tag listing one-liner, scope limits);
      verify `npm run format:md` and `npm run lint:md` pass

## 3. OpenSpec validate

- [x] 3.1 Run `openspec validate registry-retry-publish --strict` and fix any reported issues
