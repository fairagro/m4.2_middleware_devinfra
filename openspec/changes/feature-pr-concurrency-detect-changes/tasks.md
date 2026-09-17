## 1. Documentation

- [ ] 1.1 Replace the partial Feature-PR jobs-only snippet in `docs/ci.md` with a complete recommended workflow
      (top-level `concurrency` cancel-in-progress by PR, full `detect-changes` with suggested `code` path filter +
      extend note, existing quality/build/check `skip` / check `if:` wiring) and verify the snippet is copy-pasteable
      YAML
- [ ] 1.2 Add release / pre-release / Helm concurrency guidance (`cancel-in-progress: false`, serialize by workflow+ref)
      and state that `detect-changes` / `skip` is Feature-PR-oriented; verify the section is present next to those
      caller examples
- [ ] 1.3 Document that reusable-level concurrency does not replace caller-level full-PR cancel and that `skip` /
      `detect-changes` stay caller-owned; verify `npm run lint:md` is clean for touched docs

## 2. Outer reusable concurrency

- [ ] 2.1 Add `concurrency` (`cancel-in-progress: true`) to `reusable-code-quality.yml`, `reusable-build.yml`, and
      `reusable-check.yml` with group
      `${{ github.repository }}-<stem>-${{ github.event.pull_request.number || github.ref }}`; verify each file declares
      `concurrency` near the workflow top
- [ ] 2.2 Add `concurrency` (`cancel-in-progress: false`) to `reusable-release.yml`, `reusable-helm-release.yml`,
      `reusable-helm-pre-release.yml`, and `reusable-registry-retry.yml` with the same group shape; verify nested
      bake/push/OCI helpers remain unchanged

## 3. Validate

- [ ] 3.1 Run `openspec validate feature-pr-concurrency-detect-changes --strict` and fix until it passes
