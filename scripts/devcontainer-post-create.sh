#!/usr/bin/env bash
# Sequential Dev Container postCreate setup.
# Environment: Linux Dev Container only (invoked from .devcontainer/devcontainer.json).
#
# Generic for this shared-infra repo — no product-repo assumptions (issue #10).

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
cd "${repo_root}"

# ── commandhistory (Dev Container volume only) ───────────────────────────────
if [ -d /commandhistory ]; then
    echo "==> Fix commandhistory permissions"
    sudo chown -R "$(id -u):$(id -g)" /commandhistory
fi

# ── gh config volume ─────────────────────────────────────────────────────────
if [ -d /home/vscode/.config/gh ] || [ -e /home/vscode/.config ]; then
    echo "==> Fix gh config permissions"
    sudo mkdir -p /home/vscode/.config/gh
    sudo chown -R "$(id -u):$(id -g)" /home/vscode/.config
fi

# ── versions.env → .python-version ───────────────────────────────────────────
echo "==> Sync versions from versions.env"
# shellcheck disable=SC1091
source "${script_dir}/load-versions-env.sh"

# Tokens for interactive use come from scripts/bin/{gh,git} (PATH via remoteEnv),
# which source scripts/dev-tokens.sh. Do not patch ~/.bashrc.
echo "==> Load stored personal tokens into this postCreate environment (no TTY prompt)"
token_src="${repo_root}/scripts/dev-tokens.sh"
if [ -f "${token_src}" ]; then
  # shellcheck disable=SC1091
  source "${token_src}" || true
fi

echo "==> Dev Container post-create done"
echo "    gh=$(command -v gh || echo missing)  openspec=$(command -v openspec || echo missing)  uv=$(command -v uv || echo missing)  node=$(command -v node || echo missing)"
echo "    prettier=$(command -v prettier || echo missing)  markdownlint-cli2=$(command -v markdownlint-cli2 || echo missing)"
echo "    scripts/bin on PATH via remoteEnv after rebuild"
