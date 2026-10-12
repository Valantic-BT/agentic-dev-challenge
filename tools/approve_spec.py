#!/usr/bin/env python3
"""approve-spec: the developer approves the agent's plan. Run it yourself, in your own terminal.

    python tools/approve_spec.py

Copies .agent/spec.md to .agent/spec.approved.md with a header (branch, approver, timestamp).
The guard hook allows code changes only while that approval matches the current branch.
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, ".agent", "spec.md")
APPROVED = os.path.join(ROOT, ".agent", "spec.approved.md")


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def main() -> None:
    if not sys.stdin.isatty():
        sys.exit("Run this in your own terminal: approval is a human decision.")
    if not os.path.isfile(SPEC):
        sys.exit("No plan found: .agent/spec.md does not exist (Phase 1 first).")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch or branch in ("main", "master"):
        sys.exit("Create a task branch first; plans are never approved on main.")
    who = git("config", "user.name") or os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"

    print(f"Plan: {os.path.relpath(SPEC, ROOT)}\nBranch: {branch}\nApprover: {who}\n")
    print("Before approving, check: assumptions, impact, alternatives, one test per acceptance criterion,")
    print("files to change (no deletions), out of scope.\n")
    if input("Have you read and understood the whole plan, and do you approve it? [y/N] ").strip().lower() != "y":
        sys.exit("Not approved.")

    if os.path.isfile(APPROVED):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive = os.path.join(ROOT, ".agent", "archive")
        os.makedirs(archive, exist_ok=True)
        shutil.move(APPROVED, os.path.join(archive, f"{stamp}-superseded.approved.md"))

    at = datetime.now().astimezone().isoformat(timespec="seconds")
    with open(SPEC, encoding="utf-8") as src, open(APPROVED, "w", encoding="utf-8") as dst:
        dst.write(f"<!-- approved: branch={branch}; by={who}; at={at} -->\n")
        dst.write(src.read())
    print(f"Approved: {os.path.relpath(APPROVED, ROOT)}. Phase 2 can start.")


if __name__ == "__main__":
    main()
