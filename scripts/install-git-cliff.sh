#!/usr/bin/env bash
# Install pinned git-cliff onto PATH (CI / host). Pin from versions.env GIT_CLIFF_VERSION.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# shellcheck source=scripts/load-versions-env.sh
source "${REPO_ROOT}/scripts/load-versions-env.sh"

PIN="${GIT_CLIFF_VERSION:-}"
if [[ -z "${PIN}" ]]; then
  echo "install-git-cliff: GIT_CLIFF_VERSION missing from versions.env" >&2
  exit 1
fi

VER="${PIN#v}"
DEST="${GIT_CLIFF_INSTALL_DIR:-/usr/local/bin}"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

curl -fsSL "https://github.com/orhun/git-cliff/releases/download/${PIN}/git-cliff-${VER}-x86_64-unknown-linux-gnu.tar.gz" \
  | tar -xz -C "${TMP}"
install -m 0755 "${TMP}/git-cliff-${VER}/git-cliff" "${DEST}/git-cliff"
git-cliff --version
