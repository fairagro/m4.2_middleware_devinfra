#!/usr/bin/env bash
# Commit-stage quality gate via pre-commit (same hooks as `git commit`).
# Does not run pre-push hooks (pytest, container-structure-test).
#
# Environment: host or Dev Container (needs `uv`; ggshield needs GITGUARDIAN_API_KEY in env).
# In the Dev Container, personal tokens are loaded when /commandhistory exists.
#
# Usage: ./scripts/quality-check.sh
# Equivalent to: uv run pre-commit run --all-files

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if [ -d "${repo_root}/.venv/bin" ]; then
  export PATH="${repo_root}/.venv/bin:${PATH}"
fi

# Optional: Dev Container token store (ggshield). Do not require it on host checkouts.
if [ -d /commandhistory ]; then
  # shellcheck source=scripts/dev-tokens.sh
  source "${repo_root}/scripts/dev-tokens.sh"
fi

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Starting Code Quality Checks (pre-commit, commit stage)..."
echo "=================================="
echo -e "${YELLOW}pre-commit run --all-files...${NC}"

set +e
uv run pre-commit run --all-files
code=$?
set -e

if [ "${code}" -eq 0 ]; then
  echo -e "${GREEN}All pre-commit (commit-stage) hooks passed!${NC}"
  echo "================================="
  exit 0
fi

echo -e "${RED}pre-commit failed (exit ${code}).${NC}"
echo "Tip: apply autofixes with ./scripts/quality-fix.sh then re-run."
exit "${code}"
