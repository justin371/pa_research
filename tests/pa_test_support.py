"""Isolated fixtures for the documentation validator's integration tests."""

from contextlib import contextmanager
from pathlib import Path
import shutil
import subprocess
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def isolated_repo():
    """Copy a fresh fixture without Git, runtimes or private task artifacts."""
    with tempfile.TemporaryDirectory(prefix="pa-doc-validator-") as directory:
        root = Path(directory) / "repo"
        shutil.copytree(
            REPO_ROOT,
            root,
            ignore=shutil.ignore_patterns(
                ".git", ".codex", ".venv", "node_modules", "__pycache__", "*.pyc"
            ),
        )
        yield root


def run_docs_validator(root):
    """Use the project's PowerShell 7 runtime; keep every failure diagnostic."""
    return subprocess.run(
        [
            "pwsh", "-NoProfile", "-File",
            str(root / "scripts" / "validate_pa_research_docs.ps1"),
            "-RepoRoot", str(root),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )
