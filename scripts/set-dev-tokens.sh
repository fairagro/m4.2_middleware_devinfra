#!/usr/bin/env bash
# Prompt for GH_TOKEN and GITGUARDIAN_API_KEY and save (overrides a previous skip).
# Source this to export into the current shell: source scripts/set-dev-tokens.sh
# Do not `set -euo pipefail` here — this file is sourced into the caller shell.
_prev_dev_tokens_force="${DEV_TOKENS_FORCE-}"
_had_dev_tokens_force=0
[ "${DEV_TOKENS_FORCE+x}" = x ] && _had_dev_tokens_force=1
export DEV_TOKENS_FORCE=1
# shellcheck source=scripts/dev-tokens.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dev-tokens.sh"
if [ "${_had_dev_tokens_force}" -eq 1 ]; then
  export DEV_TOKENS_FORCE="${_prev_dev_tokens_force}"
else
  unset DEV_TOKENS_FORCE
fi
unset _prev_dev_tokens_force _had_dev_tokens_force
