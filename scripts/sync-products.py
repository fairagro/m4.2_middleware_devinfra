#!/usr/bin/env python3
"""Copy allowlisted Devinfra paths into product repos and open sync PRs.

Path set comes only from docs/synced-paths.yaml. See docs/sync.md.
Typical callers: .github/workflows/sync-products.yml, or a manual local run.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = REPO_ROOT / "docs" / "synced-paths.yaml"

TARGETS: dict[str, str] = {
    "api": "fairagro/m4.2_advanced_middleware_api",
    "sql_to_arc": "fairagro/m4.2_sql_to_arc",
    "harvester": "fairagro/m4.2_middleware_harvester",
}

# New branches: chore/devinfra-sync-<shortsha>. Legacy rolling name also matches.
SYNC_BRANCH_PREFIX = "chore/devinfra-sync"
SHORT_SHA_LEN = 7
DRY_RUN_PREVIEW_LIMIT = 20


def sync_branch_name(source_sha: str) -> str:
    """Return SHA-scoped sync branch for this Devinfra commit."""
    short = source_sha.strip()[:SHORT_SHA_LEN]
    if len(short) < SHORT_SHA_LEN:
        raise SystemExit(f"source_sha too short for sync branch: {source_sha!r}")
    return f"{SYNC_BRANCH_PREFIX}-{short}"


def is_sync_head(head_ref: str) -> bool:
    """Return whether head is a legacy or SHA-scoped sync branch."""
    return head_ref == SYNC_BRANCH_PREFIX or head_ref.startswith(f"{SYNC_BRANCH_PREFIX}-")


def load_allow_exclude_text(text: str, *, source: str) -> tuple[list[str], list[str]]:
    """Load allow/exclude from YAML text (same rules as ``load_allow_exclude``)."""
    loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise SystemExit(f"{source}: expected a YAML mapping at the root")
    allow = loaded.get("allow") or []
    exclude = loaded.get("exclude") or []
    overlays = loaded.get("overlays") or []
    if not isinstance(allow, list) or not isinstance(exclude, list):
        raise SystemExit(f"{source}: `allow` and `exclude` must be YAML lists")
    if not isinstance(overlays, list):
        raise SystemExit(f"{source}: `overlays` must be a YAML list when present")
    allow_s = [str(x).strip() for x in allow if str(x).strip()]
    exclude_s = [str(x).strip() for x in exclude if str(x).strip()]
    seen = set(exclude_s)
    for raw in overlays:
        item = str(raw).strip()
        if item and item not in seen:
            exclude_s.append(item)
            seen.add(item)
    if not allow_s:
        raise SystemExit(f"{source}: `allow` list is empty")
    return allow_s, exclude_s


def load_allow_exclude(path: Path) -> tuple[list[str], list[str]]:
    """Load `allow` and effective denylist from the YAML SoT.

    Product-local `overlays` are never overwritten: they are merged into the
    denylist even if a maintainer forgets to duplicate them under `exclude`.
    """
    return load_allow_exclude_text(path.read_text(encoding="utf-8"), source=str(path))


def normalize_rel(path: str) -> str:
    """Normalize to repo-relative POSIX paths."""
    rel = path.replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def is_ignored_artifact(rel: str) -> bool:
    """Skip bytecode under allowlisted trees."""
    return "__pycache__" in Path(rel).parts or Path(rel).suffix in {".pyc", ".pyo"}


def _match_double_star(path: str, pattern: str) -> bool:
    """Match patterns like `dir/**` against path."""
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(prefix + "/")
    if "/**/" in pattern:
        left, right = pattern.split("/**/", 1)
        if not path.startswith(left + "/") and path != left:
            return False
        rest = path[len(left) + 1 :] if path.startswith(left + "/") else ""
        return fnmatch.fnmatch(rest, right) or any(
            fnmatch.fnmatch("/".join(rest.split("/")[i:]), right) for i in range(len(rest.split("/")))
        )
    return fnmatch.fnmatch(path, pattern.replace("**/", "").replace("/**", "/*"))


def is_excluded(rel: str, excludes: tuple[str, ...]) -> bool:
    """Return whether rel matches any YAML `exclude` glob."""
    rel = normalize_rel(rel)
    for glob in excludes:
        if "**" in glob:
            if _match_double_star(rel, glob):
                return True
        elif "/" in glob:
            if fnmatch.fnmatch(rel, glob):
                return True
        elif fnmatch.fnmatch(rel, glob) or fnmatch.fnmatch(Path(rel).name, glob):
            return True
    return False


def _add_files(found: set[Path], root: Path, path: Path) -> None:
    if path.is_file():
        found.add(path.relative_to(root))
    elif path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                found.add(child.relative_to(root))


def resolve_files(patterns: list[str], root: Path, excludes: tuple[str, ...]) -> list[Path]:
    """Expand allowlist globs; drop excludes and bytecode."""
    found: set[Path] = set()
    for raw in patterns:
        pattern = normalize_rel(raw)
        if pattern.endswith("/**"):
            _add_files(found, root, root / pattern[:-3])
        elif any(c in pattern for c in "*?["):
            for match in root.glob(pattern):
                _add_files(found, root, match)
        else:
            _add_files(found, root, root / pattern)
    return sorted(
        rel for rel in found if not is_excluded(rel.as_posix(), excludes) and not is_ignored_artifact(rel.as_posix())
    )


def is_allowed_path(rel: str, patterns: list[str]) -> bool:
    """Return whether ``rel`` matches any allow pattern (path-string form)."""
    rel = normalize_rel(rel)
    for raw in patterns:
        pattern = normalize_rel(raw)
        if pattern.endswith("/**"):
            if _match_double_star(rel, pattern):
                return True
        elif any(c in pattern for c in "*?["):
            if fnmatch.fnmatch(rel, pattern) or _match_double_star(rel, pattern):
                return True
        elif rel == pattern or rel.startswith(pattern.rstrip("/") + "/"):
            # Exact file or directory prefix when allow lists a file/dir path
            if rel == pattern:
                return True
            # Directory-style without /** : treat as prefix only if path is a dir entry
            # Allow entries are usually files or /** globs; plain dir rarely used.
            if pattern.endswith("/") and rel.startswith(pattern):
                return True
        elif "**" in pattern and _match_double_star(rel, pattern):
            return True
    return False


def filter_tree_paths(tree_paths: list[str], patterns: list[str], excludes: tuple[str, ...]) -> list[Path]:
    """Filter git ls-tree paths by allow/exclude (no working-tree walk)."""
    found: set[Path] = set()
    for raw in tree_paths:
        rel = normalize_rel(raw)
        if is_ignored_artifact(rel) or is_excluded(rel, excludes):
            continue
        if is_allowed_path(rel, patterns):
            found.add(Path(rel))
    return sorted(found)


def git_show_text(ref: str, path: str, *, cwd: Path) -> str:
    """Return file contents at ``ref:path``."""
    return git_out(["git", "show", f"{ref}:{path}"], cwd=cwd)


def git_ls_tree_files(ref: str, *, cwd: Path) -> list[str]:
    """List blob paths at ``ref``."""
    raw = git_out(["git", "ls-tree", "-r", "--name-only", ref], cwd=cwd)
    return [line for line in raw.splitlines() if line.strip()]


def resolve_files_at_ref(ref: str, *, cwd: Path = REPO_ROOT) -> list[Path]:
    """Resolve allowlist file set as of git ``ref`` (YAML + tree at that ref)."""
    try:
        yaml_text = git_show_text(ref, "docs/synced-paths.yaml", cwd=cwd)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"cannot read docs/synced-paths.yaml at {ref}: {exc}") from exc
    patterns, excludes = load_allow_exclude_text(yaml_text, source=f"{ref}:docs/synced-paths.yaml")
    tree = git_ls_tree_files(ref, cwd=cwd)
    return filter_tree_paths(tree, patterns, tuple(excludes))


def orphan_paths(base_files: list[Path], head_files: list[Path]) -> list[Path]:
    """Paths in base allowlist set but not in head (delta orphans)."""
    head_set = {p.as_posix() for p in head_files}
    return sorted(
        (p for p in base_files if p.as_posix() not in head_set),
        key=lambda p: p.as_posix(),
    )


def remove_orphans(orphans: list[Path], dest_root: Path) -> list[Path]:
    """``git rm`` orphans that exist under ``dest_root``; return removed paths."""
    removed: list[Path] = []
    for rel in orphans:
        dest = dest_root / rel
        if not dest.is_file():
            continue
        run(["git", "rm", "-f", "--", rel.as_posix()], cwd=dest_root)
        removed.append(rel)
    return removed


def copy_files(files: list[Path], src_root: Path, dest_root: Path) -> None:
    """Copy allowlisted relative files from src_root into dest_root."""
    for rel in files:
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_root / rel, dest)


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    """Print and run a subprocess command; raise on non-zero exit."""
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def try_run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> bool:
    """Print and run a command; return whether it exited 0."""
    print("+", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=cwd, env=env, check=False)
    return completed.returncode == 0


def git_out(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    """Run a command and return stripped stdout; raise on non-zero exit."""
    return subprocess.check_output(cmd, cwd=cwd, env=env, text=True).strip()


def open_sync_pr_number(*, repo: str, head: str, cwd: Path, env: dict[str, str]) -> int | None:
    """Return the open PR number for ``head``, if any."""
    raw = git_out(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            head,
            "--state",
            "open",
            "--json",
            "number",
            "--jq",
            ".[0].number // empty",
        ],
        cwd=cwd,
        env=env,
    )
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise SystemExit(f"invalid open PR number for head {head!r}: {raw!r}") from exc


def resolve_token() -> str | None:
    """Return DEVINFRA_BOT_TOKEN or GH_TOKEN from the environment, if set."""
    for key in ("DEVINFRA_BOT_TOKEN", "GH_TOKEN"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None


@dataclass(frozen=True)
class SyncTarget:
    """One product-repo sync invocation."""

    key: str
    repo: str
    files: list[Path]
    orphans: list[Path]
    source_sha: str
    dry_run: bool
    token: str | None


def supersede_older_sync_prs(
    *,
    repo: str,
    new_pr: int,
    source_sha: str,
    cwd: Path,
    env: dict[str, str],
) -> None:
    """Comment + close other open sync PRs; never closes ``new_pr``."""
    raw = git_out(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "100",
            "--search",
            f"head:{SYNC_BRANCH_PREFIX}",
            "--json",
            "number,headRefName",
        ],
        cwd=cwd,
        env=env,
    )
    try:
        listed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"gh pr list returned invalid JSON: {exc}") from exc
    if not isinstance(listed, list):
        raise SystemExit("gh pr list JSON: expected a list")

    short = source_sha[:SHORT_SHA_LEN]
    body = f"Superseded by #{new_pr}. Newer full allowlist sync from Devinfra `{short}`."
    for item in listed:
        if not isinstance(item, dict):
            continue
        number = item.get("number")
        head = item.get("headRefName")
        if not isinstance(number, int) or not isinstance(head, str):
            continue
        if number == new_pr or not is_sync_head(head):
            continue
        run(
            [
                "gh",
                "pr",
                "comment",
                str(number),
                "--repo",
                repo,
                "--body",
                body,
            ],
            cwd=cwd,
            env=env,
        )
        run(
            ["gh", "pr", "close", str(number), "--repo", repo],
            cwd=cwd,
            env=env,
        )
        print(f"superseded open sync PR #{number} ({head})", flush=True)


def _preview_paths(label: str, paths: list[Path]) -> None:
    for rel in paths[:DRY_RUN_PREVIEW_LIMIT]:
        print(f"  {label} {rel.as_posix()}")
    if len(paths) > DRY_RUN_PREVIEW_LIMIT:
        print(f"  ... and {len(paths) - DRY_RUN_PREVIEW_LIMIT} more")


def sync_target(req: SyncTarget) -> None:
    """Clone one product repo, copy files, open a new SHA-scoped sync PR if needed."""
    print(f"\n=== target {req.key}: {req.repo} ===", flush=True)
    branch = sync_branch_name(req.source_sha)
    if req.dry_run:
        print(
            f"dry-run: would copy {len(req.files)} files, "
            f"remove {len(req.orphans)} allowlist orphans, "
            f"open new sync PR on {branch}, "
            "and supersede older open sync PRs",
            flush=True,
        )
        _preview_paths("+", req.files)
        _preview_paths("-", req.orphans)
        return

    if not req.token:
        raise SystemExit("live sync requires DEVINFRA_BOT_TOKEN (or GH_TOKEN for local testing)")

    env = os.environ.copy()
    env["GH_TOKEN"] = req.token
    env["GIT_TERMINAL_PROMPT"] = "0"
    run(["gh", "auth", "setup-git"], env=env)

    with tempfile.TemporaryDirectory(prefix=f"sync-{req.key}-") as tmp:
        dest = Path(tmp) / "repo"
        run(
            ["gh", "repo", "clone", req.repo, str(dest), "--", "--depth", "1"],
            env=env,
        )
        run(["git", "checkout", "-B", branch], cwd=dest, env=env)
        copy_files(req.files, REPO_ROOT, dest)
        removed = remove_orphans(req.orphans, dest)
        if removed:
            print(f"removed {len(removed)} allowlist orphan(s)", flush=True)

        if not git_out(["git", "status", "--porcelain"], cwd=dest, env=env):
            print("no changes vs target tip; skip PR", flush=True)
            return

        _commit_and_open_sync_pr(req, dest=dest, branch=branch, env=env)


def _commit_and_open_sync_pr(req: SyncTarget, *, dest: Path, branch: str, env: dict[str, str]) -> None:
    run(["git", "add", "-A"], cwd=dest, env=env)
    run(
        [
            "git",
            "-c",
            "user.name=fairagro-devinfra-bot",
            "-c",
            "user.email=devinfra-bot@users.noreply.github.com",
            "commit",
            "-m",
            f"chore: sync shared Devinfra paths from {req.source_sha[:SHORT_SHA_LEN]}",
        ],
        cwd=dest,
        env=env,
    )

    # Same Devinfra SHA already has an open sync PR (workflow retry) — reuse it.
    existing = open_sync_pr_number(repo=req.repo, head=branch, cwd=dest, env=env)
    if existing is not None:
        print(f"reusing open sync PR #{existing} on {branch}", flush=True)
        supersede_older_sync_prs(
            repo=req.repo,
            new_pr=existing,
            source_sha=req.source_sha,
            cwd=dest,
            env=env,
        )
        return

    # New branch per source SHA — never force-update a rolling sync ref.
    push_head = branch
    if not try_run(["git", "push", "-u", "origin", "HEAD"], cwd=dest, env=env):
        # Remote SHA branch may exist from a prior run that failed before PR create.
        retry_branch = f"{branch}-retry"
        print(
            f"push of {branch} failed; retrying once as {retry_branch} (no force)",
            flush=True,
        )
        run(["git", "branch", "-M", retry_branch], cwd=dest, env=env)
        run(["git", "push", "-u", "origin", "HEAD"], cwd=dest, env=env)
        push_head = retry_branch

    body = f"""## Summary

Sync allowlisted shared paths from [`fairagro/m4.2_middleware_devinfra@{req.source_sha}`](https://github.com/fairagro/m4.2_middleware_devinfra/commit/{req.source_sha}).

Source of truth: [`docs/synced-paths.yaml`](https://github.com/fairagro/m4.2_middleware_devinfra/blob/main/docs/synced-paths.yaml).

Do **not** hand-edit these paths in this consumer — land fixes in Devinfra, then re-sync.

## Test plan

- [ ] Spot-check diff against allowlist / hard excludes (including deletions)
- [ ] CI green on this PR
"""
    run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            req.repo,
            "--title",
            f"chore: sync shared Devinfra paths ({req.source_sha[:SHORT_SHA_LEN]})",
            "--body",
            body,
            "--head",
            push_head,
        ],
        cwd=dest,
        env=env,
    )
    new_pr = open_sync_pr_number(repo=req.repo, head=push_head, cwd=dest, env=env)
    if new_pr is None:
        raise SystemExit(f"sync PR create reported success but no open PR for head {push_head!r}")
    print(f"opened sync PR #{new_pr} on {push_head}", flush=True)
    supersede_older_sync_prs(
        repo=req.repo,
        new_pr=new_pr,
        source_sha=req.source_sha,
        cwd=dest,
        env=env,
    )


def main(argv: list[str] | None = None) -> int:
    """Run product-repo sync CLI; return process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List resolved files / targets; do not clone or open PRs",
    )
    parser.add_argument("--skip-api", action="store_true")
    parser.add_argument("--skip-sql-to-arc", action="store_true")
    parser.add_argument("--skip-harvester", action="store_true")
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="Print resolved allowlist files and exit",
    )
    parser.add_argument(
        "--ref",
        default="HEAD",
        help="With --list-files: resolve allowlist file set at this git ref (default HEAD)",
    )
    parser.add_argument(
        "--orphan-base",
        default="",
        help="Git ref/SHA for allowlist delta orphans (list(base) - list(HEAD)); empty skips deletes",
    )
    args = parser.parse_args(argv)

    source_sha = git_out(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)

    if args.list_files:
        # Machine-readable only (workflow gate uses exact-line match).
        ref = (args.ref or "HEAD").strip() or "HEAD"
        if ref == "HEAD":
            patterns, excludes = load_allow_exclude(ALLOWLIST_PATH)
            files = resolve_files(patterns, REPO_ROOT, tuple(excludes))
        else:
            files = resolve_files_at_ref(ref, cwd=REPO_ROOT)
        for rel in files:
            print(rel.as_posix())
        return 0

    patterns, excludes = load_allow_exclude(ALLOWLIST_PATH)
    excludes_t = tuple(excludes)
    files = resolve_files(patterns, REPO_ROOT, excludes_t)
    if not files:
        raise SystemExit("allowlist resolved to zero files — check docs/synced-paths.yaml")

    orphans: list[Path] = []
    orphan_base = (args.orphan_base or "").strip()
    if orphan_base:
        base_files = resolve_files_at_ref(orphan_base, cwd=REPO_ROOT)
        head_files = resolve_files_at_ref("HEAD", cwd=REPO_ROOT)
        orphans = orphan_paths(base_files, head_files)
        print(
            f"orphan-base {orphan_base}: {len(base_files)} → HEAD {len(head_files)}; orphans to remove: {len(orphans)}",
            flush=True,
        )

    print(
        f"allowlist patterns: {len(patterns)}; exclude: {len(excludes_t)}; files: {len(files)}",
        flush=True,
    )

    token = resolve_token()
    skips = {
        "api": args.skip_api,
        "sql_to_arc": args.skip_sql_to_arc,
        "harvester": args.skip_harvester,
    }

    for key, repo in TARGETS.items():
        if skips[key]:
            print(f"\n=== skip {key} ({repo}) ===", flush=True)
            continue
        sync_target(
            SyncTarget(
                key=key,
                repo=repo,
                files=files,
                orphans=orphans,
                source_sha=source_sha,
                dry_run=args.dry_run,
                token=token,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
