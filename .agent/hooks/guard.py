#!/usr/bin/env python3
"""guard: runs BEFORE every tool call (PreToolUse). Developer-only file.

Exit 0 = allow. Exit 2 = block; the message on stderr goes back to the agent.
Rules:
  1. No deletions, ever (shell).
  2. Governance files are developer-only (shell).
  3. Writes only inside src/, tests/ and docs/ (plus the plan .agent/spec.md).
  4. Never on the main branch; code only with a plan approved for the current branch.
  5. No emptying files (a deletion in disguise).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ALLOWED, MAIN_BRANCHES, approval, current_branch, relative  # noqa: E402

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
PLAN = ".agent/spec.md"

DELETE = re.compile(
    r"(?<![\w.-])(rm|rmdir|del|erase|unlink|shred|truncate|Remove-Item)(?![\w-])"
    r"|\bgit\s+(rm|clean)\b|os\.remove|os\.unlink|shutil\.rmtree|\.unlink\(|\.rmdir\(",
    re.IGNORECASE,
)
GOVERNANCE = re.compile(
    r"\.agent[\\/]|spec\.approved|\.claude[\\/]|approve_spec|[\\/]hooks[\\/]|settings(\.local)?\.json",
    re.IGNORECASE,
)


def block(msg: str) -> None:
    print(f"[GUARD] {msg}", file=sys.stderr)
    sys.exit(2)


def check_shell(command: str) -> None:
    if DELETE.search(command):
        block("Deleting is not allowed. Propose the deletion in the plan; the developer deletes.")
    if GOVERNANCE.search(command):
        block("Governance files (.agent/, .claude/, approval, hooks) are developer-only.")


def check_write(tool: str, tool_input: dict) -> None:
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    rel = relative(path)
    if rel.startswith(".."):
        block(f"Outside the project: {path}")

    branch = current_branch()
    if branch is None:
        block("Cannot determine the git branch. Work inside the repository, on a task branch.")
    if branch in MAIN_BRANCHES:
        block(f"Never work on '{branch}'. The developer creates a task branch first.")

    if tool == "Write" and isinstance(tool_input.get("content"), str) and not tool_input["content"].strip():
        block("Emptying a file is not allowed.")

    if rel == PLAN:
        return  # Phase 1: the agent writes its plan here
    if not rel.startswith(ALLOWED):
        block(f"Not an allowed path: {rel}. Allowed: {', '.join(ALLOWED)}")

    appr = approval()
    if appr is None:
        block("No approved plan. Phase 2 needs .agent/spec.approved.md, created by the developer.")
    if appr["branch"] != branch:
        block(f"The approved plan is for branch '{appr['branch']}', not '{branch}'. A new task needs a new plan.")


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        block("Invalid hook input.")
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if tool in SHELL_TOOLS:
        check_shell(tool_input.get("command", ""))
    elif tool in WRITE_TOOLS:
        check_write(tool, tool_input)
    sys.exit(0)


if __name__ == "__main__":
    main()
