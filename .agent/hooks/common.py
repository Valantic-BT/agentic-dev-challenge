"""Shared helpers for the governance hooks. Developer-only file."""
import os
import re
import subprocess

ROOT = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
AGENT_DIR = os.path.join(ROOT, ".agent")
SPEC = os.path.join(AGENT_DIR, "spec.md")
APPROVED = os.path.join(AGENT_DIR, "spec.approved.md")
ARCHIVE = os.path.join(AGENT_DIR, "archive")
MAIN_BRANCHES = {"main", "master"}
ALLOWED = ("src/", "tests/", "docs/")

_HEADER = re.compile(r"<!--\s*approved:\s*branch=(?P<branch>[^;]+);\s*by=(?P<by>[^;]*);\s*at=(?P<at>[^>]*?)\s*-->")


def current_branch() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def approval() -> dict | None:
    """Header of .agent/spec.approved.md: {'branch', 'by', 'at'} or None if missing/invalid."""
    if not os.path.isfile(APPROVED):
        return None
    with open(APPROVED, encoding="utf-8") as fh:
        first = fh.readline()
    m = _HEADER.search(first)
    return {k: v.strip() for k, v in m.groupdict().items()} if m else None


def relative(path: str) -> str:
    """Path relative to the project root, with forward slashes ('..' prefix if outside)."""
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    return os.path.relpath(os.path.abspath(full), ROOT).replace("\\", "/")
