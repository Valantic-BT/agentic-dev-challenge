#!/usr/bin/env python3
"""archive-approval: runs at session start (SessionStart). Developer-only file.

An approval is valid for one task (one branch). When the current branch is not the
branch of the approved plan, the approval and its plan are moved to .agent/archive/,
so the next task needs a new plan. Nothing is deleted.
"""
import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import APPROVED, ARCHIVE, SPEC, approval, current_branch  # noqa: E402


def main() -> None:
    appr = approval()
    branch = current_branch()
    if not os.path.isfile(APPROVED) or (appr and appr["branch"] == branch):
        sys.exit(0)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = (appr["branch"] if appr else "unknown").replace("/", "_")
    os.makedirs(ARCHIVE, exist_ok=True)
    shutil.move(APPROVED, os.path.join(ARCHIVE, f"{stamp}-{tag}.approved.md"))
    if os.path.isfile(SPEC):
        shutil.move(SPEC, os.path.join(ARCHIVE, f"{stamp}-{tag}.spec.md"))
    print(f"[GATE] Approval for branch '{tag}' archived. This task starts in Phase 1 with a new plan.")
    sys.exit(0)


if __name__ == "__main__":
    main()
