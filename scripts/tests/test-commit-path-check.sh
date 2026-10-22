#!/usr/bin/env bash
# Fixtures for scripts/commit-path-check.sh (#320)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CHECK="${ROOT}/scripts/commit-path-check.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

pass=0
fail=0

run_case() {
  local name="$1" expect="$2" subject="$3" paths="$4"
  local msg="${TMP}/msg-${name}"
  local staged="${TMP}/staged-${name}"
  printf '%s\n' "${subject}" >"${msg}"
  printf '%s\n' ${paths} >"${staged}"
  set +e
  out="$("${CHECK}" --staged-from "${staged}" "${msg}" 2>&1)"
  code=$?
  set -e
  if [[ "${expect}" == "ok" && "${code}" -eq 0 ]]; then
    pass=$((pass + 1))
  elif [[ "${expect}" == "fail" && "${code}" -ne 0 ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL ${name}: expected ${expect}, got exit ${code}" >&2
    echo "${out}" >&2
    fail=$((fail + 1))
  fi
}

run_case propose-feat fail \
  "feat(opsx): implement something" \
  "openspec/changes/foo/proposal.md openspec/changes/foo/tasks.md"

run_case archive-feat fail \
  "feat(openspec): archive foo and sync specs" \
  "openspec/changes/archive/2026-10-01-foo/proposal.md openspec/specs/shared-renovate/spec.md"

run_case test-only-fix fail \
  "fix(generic): update tests" \
  "middleware/harvester/tests/unit/test_main.py"

run_case chore-archive ok \
  "chore(openspec): archive foo and sync specs" \
  "openspec/changes/archive/2026-10-01-foo/proposal.md openspec/specs/x/spec.md"

run_case shipped-feat ok \
  "feat(api): add version endpoint" \
  "middleware/api/src/middleware/api/api/fastapi_app.py"

run_case mixed-test-product ok \
  "fix(generic): adapt mapper and tests" \
  "middleware/generic/src/middleware/generic/plugin.py middleware/generic/tests/unit/test_plugin.py"

run_case docs-archive fail \
  "docs(openspec): archive foo" \
  "openspec/changes/archive/2026-10-01-foo/tasks.md"

run_case docs-archive-typo ok \
  "docs: fix typo in archived proposal" \
  "openspec/changes/archive/2026-10-01-foo/proposal.md"

run_case deps-ok ok \
  "deps: Update npm toolchain" \
  "package-lock.json"

# Missing --staged-from path must be a usage error (not soft-pass as empty index)
{
  msg="${TMP}/msg-missing-staged"
  printf '%s\n' "feat: anything" >"${msg}"
  set +e
  out="$("${CHECK}" --staged-from "${TMP}/does-not-exist" "${msg}" 2>&1)"
  code=$?
  set -e
  if [[ "${code}" -ne 0 ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL missing-staged-from: expected fail, got exit 0" >&2
    echo "${out}" >&2
    fail=$((fail + 1))
  fi
}

# --staged-from without a value must be a clear usage error (not shift failure)
{
  msg="${TMP}/msg-staged-no-value"
  printf '%s\n' "feat: anything" >"${msg}"
  set +e
  out="$("${CHECK}" --staged-from 2>&1)"
  code=$?
  set -e
  if [[ "${code}" -ne 0 && "${out}" == *"--staged-from requires a file path"* ]]; then
    pass=$((pass + 1))
  else
    echo "FAIL staged-from-no-value: expected usage exit, got ${code}" >&2
    echo "${out}" >&2
    fail=$((fail + 1))
  fi
}

echo "commit-path-check fixtures: ${pass} passed, ${fail} failed"
[[ "${fail}" -eq 0 ]]
