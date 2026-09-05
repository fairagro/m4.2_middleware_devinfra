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

# ── Personal tokens: interactive shells source helper (Kombi with PATH wrappers)
echo "==> Ensure ~/.bashrc sources scripts/dev-tokens.sh"
bashrc="${HOME}/.bashrc"
marker_begin="# >>> m4.2-dev-tokens (managed by postCreate) >>>"
marker_end="# <<< m4.2-dev-tokens <<<"
token_src="${repo_root}/scripts/dev-tokens.sh"
touch "${bashrc}"
# Refresh managed block only when markers are well-formed (exactly one begin before one end).
# Otherwise awk skip-mode would truncate everything after a lone begin marker.
begin_count="$(awk -v b="${marker_begin}" '$0 == b { c++ } END { print c+0 }' "${bashrc}")"
end_count="$(awk -v e="${marker_end}" '$0 == e { c++ } END { print c+0 }' "${bashrc}")"
begin_line="$(awk -v b="${marker_begin}" '$0 == b { print NR; exit }' "${bashrc}")"
end_line="$(awk -v e="${marker_end}" '$0 == e { print NR; exit }' "${bashrc}")"
if [ "${begin_count}" -eq 0 ] && [ "${end_count}" -eq 0 ]; then
  : # first install — append below
elif [ "${begin_count}" -eq 1 ] && [ "${end_count}" -eq 1 ] &&
  [ -n "${begin_line}" ] && [ -n "${end_line}" ] && [ "${begin_line}" -lt "${end_line}" ]; then
  tmp="$(mktemp)"
  awk -v b="${marker_begin}" -v e="${marker_end}" '
    $0 == b {skip=1; next}
    $0 == e {skip=0; next}
    !skip {print}
  ' "${bashrc}" >"${tmp}"
  cat "${tmp}" >"${bashrc}"
  rm -f "${tmp}"
else
  echo "WARNING: unexpected m4.2-dev-tokens markers in ${bashrc} (begin=${begin_count} end=${end_count}); skipping refresh" >&2
fi
if ! grep -qF "${marker_begin}" "${bashrc}" 2>/dev/null; then
  {
    echo "${marker_begin}"
    echo "# Load stored GH_TOKEN / GITGUARDIAN_API_KEY; prompt only on TTY."
    echo "if [ -f \"${token_src}\" ]; then"
    echo "  # shellcheck disable=SC1091"
    echo "  source \"${token_src}\""
    echo "fi"
    echo "${marker_end}"
  } >>"${bashrc}"
elif ! grep -qF "${marker_end}" "${bashrc}" 2>/dev/null; then
  echo "WARNING: corrupted m4.2-dev-tokens markers in ${bashrc}; skipping token block update" >&2
fi

echo "==> Load stored personal tokens into this postCreate environment (no TTY prompt)"
if [ -f "${token_src}" ]; then
  # shellcheck disable=SC1091
  source "${token_src}" || true
fi

echo "==> Dev Container post-create done"
echo "    gh=$(command -v gh || echo missing)  openspec=$(command -v openspec || echo missing)  uv=$(command -v uv || echo missing)  node=$(command -v node || echo missing)"
echo "    prettier=$(command -v prettier || echo missing)  markdownlint-cli2=$(command -v markdownlint-cli2 || echo missing)"
echo "    scripts/bin on PATH via remoteEnv after rebuild"
