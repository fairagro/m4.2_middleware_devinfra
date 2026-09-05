#!/usr/bin/env bash
# Install Git LFS (local config) and copy version-controlled hooks into .git/hooks/.
#
# Environment: host or Dev Container (requires git-lfs on PATH — no apt/brew auto-install).
#
# Usage (from any cwd):
#   ./scripts/setup-git-lfs.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_SOURCE_DIR="${REPO_ROOT}/scripts/git-hooks"
HOOKS_TARGET_DIR="${REPO_ROOT}/.git/hooks"

echo "Setting up Git LFS hooks for repository..."

if ! command -v git-lfs >/dev/null 2>&1; then
  echo "ERROR: git-lfs is not on PATH." >&2
  echo "Install Git LFS (https://git-lfs.com), then re-run this script." >&2
  echo "The Linux Dev Container normally provides git-lfs; do not rely on Homebrew/apt auto-install here." >&2
  exit 1
fi

echo "git-lfs: $(git lfs version | head -n1)"

if [[ ! -d "${REPO_ROOT}/.git" ]]; then
  echo "ERROR: not a git worktree root: ${REPO_ROOT}" >&2
  exit 1
fi

if [[ ! -d "${HOOKS_SOURCE_DIR}" ]]; then
  echo "ERROR: missing hooks source dir: ${HOOKS_SOURCE_DIR}" >&2
  exit 1
fi

# Repo-local only: avoid writing Git LFS filters into the user's global ~/.gitconfig.
# --force refreshes LFS defaults; project hooks below replace them.
echo "Initializing Git LFS (local config)..."
(
  cd "${REPO_ROOT}"
  git lfs install --local --skip-smudge --force
)

mkdir -p "${HOOKS_TARGET_DIR}"

for hook in pre-push post-checkout post-commit post-merge; do
  source_hook="${HOOKS_SOURCE_DIR}/${hook}"
  target_hook="${HOOKS_TARGET_DIR}/${hook}"
  [[ -f "${source_hook}" ]] || continue
  echo "Installing ${hook} hook"
  cp "${source_hook}" "${target_hook}"
  chmod +x "${target_hook}"
done

echo ""
echo "Git LFS hooks setup complete."
echo "Installed:"
ls -la "${HOOKS_TARGET_DIR}/pre-push" \
  "${HOOKS_TARGET_DIR}/post-checkout" \
  "${HOOKS_TARGET_DIR}/post-commit" \
  "${HOOKS_TARGET_DIR}/post-merge" 2>/dev/null || true
echo ""
echo "Verify with: git lfs env"
echo "Commit-stage hooks remain: uv run pre-commit install --hook-type pre-commit"
