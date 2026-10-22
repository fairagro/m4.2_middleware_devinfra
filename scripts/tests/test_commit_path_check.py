"""Pre-push/CI gate: run the commit-path-check Bash fixture harness via pytest."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HARNESS = REPO_ROOT / "scripts" / "tests" / "test-commit-path-check.sh"


def test_commit_path_check_fixtures() -> None:
    result = subprocess.run(
        ["bash", str(HARNESS)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"commit-path-check fixtures failed (exit {result.returncode})\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
