# Personal GH_TOKEN / GITGUARDIAN_API_KEY. Source this file.
# Empty prompt = skip (remembered). To set later: source ./scripts/set-dev-tokens.sh
# Store: /commandhistory/tokens.env (Dev Container) or
# ~/.config/<git-repo-name>/tokens.env (host; name from origin remote)

if [ "${BASH_SOURCE[0]-}" = "${0-}" ]; then
  echo "dev-tokens: source this file (do not execute it directly)" >&2
  echo "dev-tokens: example: source ./scripts/dev-tokens.sh" >&2
  exit 1
fi

_dev_tokens_real_git() {
  local self candidate
  self="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/bin/git"
  if [ -n "${CURSOR_REAL_GIT:-}" ] && [ -x "${CURSOR_REAL_GIT}" ] && [ ! "${CURSOR_REAL_GIT}" -ef "${self}" ]; then
    printf '%s' "${CURSOR_REAL_GIT}"
    return 0
  fi
  candidate="$(command -v -p git 2>/dev/null || true)"
  if [ -n "${candidate}" ] && [ ! "${candidate}" -ef "${self}" ]; then
    printf '%s' "${candidate}"
    return 0
  fi
  for candidate in /usr/bin/git /usr/local/bin/git; do
    if [ -x "${candidate}" ] && [ ! "${candidate}" -ef "${self}" ]; then
      printf '%s' "${candidate}"
      return 0
    fi
  done
  echo "dev-tokens: could not find real git binary" >&2
  return 1
}

_dev_tokens_repo_name() {
  local real_git url name toplevel scripts_dir repo_root
  real_git="$(_dev_tokens_real_git)" || return 1
  # Always query the repo that owns this script, not the caller's CWD
  # (wrappers may run from outside a worktree, e.g. `git --version` in $HOME).
  scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  repo_root="$(cd "${scripts_dir}/.." && pwd)"
  url="$("${real_git}" -C "${repo_root}" remote get-url origin 2>/dev/null)" || true
  if [ -n "${url}" ]; then
    name="${url%.git}"
    name="${name%/}"
    name="${name##*/}"
    name="${name##*:}"
  fi
  if [ -z "${name}" ]; then
    toplevel="$("${real_git}" -C "${repo_root}" rev-parse --show-toplevel 2>/dev/null)" || true
    if [ -n "${toplevel}" ]; then
      name="$(basename "${toplevel}")"
    fi
  fi
  if [ -z "${name}" ]; then
    echo "dev-tokens: cannot determine git repository name for host token path ~/.config/<repo>/tokens.env" >&2
    echo "dev-tokens: expected a git clone at ${repo_root} with an origin remote" >&2
    return 1
  fi
  printf '%s' "${name}"
}

_dev_tokens_file() {
  if [ -d /commandhistory ]; then
    echo /commandhistory/tokens.env
    return 0
  fi
  local repo
  repo="$(_dev_tokens_repo_name)" || return 1
  mkdir -p "${HOME}/.config/${repo}"
  echo "${HOME}/.config/${repo}/tokens.env"
}

# Decode one stored value. Writes use b64:<base64> only — no legacy parsers.
_dev_tokens_decode_raw() {
  local raw=$1
  local decoded
  if [ "${raw#b64:}" != "${raw}" ]; then
    if decoded="$(printf '%s' "${raw#b64:}" | base64 -d 2>/dev/null)"; then
      printf '%s' "${decoded}"
      return 0
    fi
    echo "dev-tokens: ignoring corrupt b64 token entry" >&2
    return 1
  fi
  if [ -n "${raw}" ]; then
    echo "dev-tokens: ignoring non-b64 token entry (re-run: source ./scripts/set-dev-tokens.sh)" >&2
  fi
  return 1
}

_dev_tokens_get_stored() {
  local var=$1 line raw
  [ -f "${_DEV_TOKENS_FILE}" ] || return 0
  line="$(grep -E "^${var}=" "${_DEV_TOKENS_FILE}" 2>/dev/null | tail -n1)" || true
  [ -n "${line}" ] || return 0
  raw="${line#*=}"
  _dev_tokens_decode_raw "${raw}" || true
}

_DEV_TOKENS_FILE="$(_dev_tokens_file)" || return 1

# Apply stored tokens without clobbering a caller-set value, and without
# exporting empty "skip" markers (GH_TOKEN='') over a live environment.
if [ -f "${_DEV_TOKENS_FILE}" ]; then
  for _dev_tokens_var in GH_TOKEN GITGUARDIAN_API_KEY; do
    if [ -n "${!_dev_tokens_var-}" ]; then
      continue
    fi
    _dev_tokens_val="$(_dev_tokens_get_stored "${_dev_tokens_var}")"
    if [ -n "${_dev_tokens_val}" ]; then
      export "${_dev_tokens_var}=${_dev_tokens_val}"
    fi
  done
  unset _dev_tokens_var _dev_tokens_val
fi

_dev_tokens_write() {
  local var=$1 val=$2 b64
  (
    umask 077
    touch "${_DEV_TOKENS_FILE}"
    chmod 600 "${_DEV_TOKENS_FILE}"
    grep -v "^${var}=" "${_DEV_TOKENS_FILE}" >"${_DEV_TOKENS_FILE}.tmp" 2>/dev/null || true
    # -w0 is GNU; BSD/other base64 may wrap at 76 cols — collapse to one line for KEY=value storage.
    b64="$(printf '%s' "${val}" | base64 -w0 2>/dev/null || printf '%s' "${val}" | base64)"
    b64="$(printf '%s' "${b64}" | tr -d '\n\r')"
    printf '%s=b64:%s\n' "${var}" "${b64}" >>"${_DEV_TOKENS_FILE}.tmp"
    # Rewrite in place to preserve mode/owner of the token file.
    cat "${_DEV_TOKENS_FILE}.tmp" >"${_DEV_TOKENS_FILE}"
    rm -f "${_DEV_TOKENS_FILE}.tmp"
  )
}

_dev_tokens_ask() {
  local var=$1 hint=$2 val cur
  cur="${!var-}"
  if [ -z "${DEV_TOKENS_FORCE:-}" ]; then
    [ -n "${cur}" ] && return 0
    grep -q "^${var}=" "${_DEV_TOKENS_FILE}" 2>/dev/null && return 0
  fi
  { printf '' >/dev/tty; } 2>/dev/null || return 0
  printf '%s — %s (empty skips until set-dev-tokens.sh)\n> ' "${var}" "${hint}" >/dev/tty
  IFS= read -r -s val </dev/tty || true
  printf '\n' >/dev/tty
  _dev_tokens_write "${var}" "${val}"
  [ -n "${val}" ] && export "${var}=${val}"
}

_dev_tokens_ask GH_TOKEN "GitHub PAT (issues + PRs)"
_dev_tokens_ask GITGUARDIAN_API_KEY "GitGuardian API key"
unset -f _dev_tokens_file _dev_tokens_write _dev_tokens_ask _dev_tokens_real_git _dev_tokens_repo_name
unset -f _dev_tokens_decode_raw _dev_tokens_get_stored
unset _DEV_TOKENS_FILE
