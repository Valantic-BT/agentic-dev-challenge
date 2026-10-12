#!/usr/bin/env python3
"""gate-status: runs on every request (UserPromptSubmit). Developer-only file.

Prints the current [GATE] status; the harness adds it to the agent's context,
so the agent never decides on stale information.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ALLOWED, MAIN_BRANCHES, SPEC, approval, current_branch  # noqa: E402


def main() -> None:
    branch = current_branch() or "unknown"
    appr = approval()
    if branch in MAIN_BRANCHES:
        phase = "BLOCKED: main branch. Ask the developer to create a task branch."
    elif appr and appr["branch"] == branch:
        phase = f"PHASE 2 allowed: plan approved by {appr['by']} at {appr['at']}. Implement exactly the approved plan."
    elif appr:
        phase = f"PHASE 1 only: the approved plan belongs to branch '{appr['branch']}' (stale for this task)."
    elif os.path.isfile(SPEC):
        phase = "PHASE 1 only: plan .agent/spec.md written, waiting for developer approval. Do not implement."
    else:
        phase = "PHASE 1 only: no plan yet. Analyse, write .agent/spec.md and stop."
    print(
        "[GATE]\n"
        f"branch: {branch}\n"
        f"status: {phase}\n"
        f"allowed write folders: {', '.join(ALLOWED)} (plus .agent/spec.md in phase 1)\n"
        "never: delete files, empty files, touch .agent/ (except spec.md), .claude/, tools/, .github/\n"
        "[/GATE]"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
