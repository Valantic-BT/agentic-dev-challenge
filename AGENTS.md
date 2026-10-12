# AGENTS.md

## Stack and commands
- Python 3.11+, FastAPI. Code in `src/orders_api/`, tests in `tests/`, docs in `docs/`.
- Install: `pip install -e ".[dev]"`
- Lint: `ruff check .`
- Tests: `pytest -q` (summary output; show only failures)
- Run: `uvicorn orders_api.main:app --reload --app-dir src`

## Workflow
- Phase 1: analyse, write the plan to `.agent/spec.md`, then stop and wait for the developer.
- Phase 2: only with `.agent/spec.approved.md` for the current branch; implement exactly the plan.
- After every change: lint and tests until green. Report what was not verified.
- Roles: architect (plan), contradictor (challenge the plan), developer-specialist (implement),
  tester (tests from acceptance criteria), qa (verify against the plan), documenter (docs/).

## A good plan contains
- Goal and verifiable acceptance criteria; assumptions; open questions; out of scope.
- Files to create or change.
- Approach and rejected alternatives; impact (who uses what changes).
- One test per acceptance criterion; risks.

## Rules
- Money: use `Decimal`, never `float`. Round to cents with ROUND_HALF_UP.
- Naming: snake_case for Python, camelCase for JSON fields.
- No new dependency unless it is in the approved plan.
