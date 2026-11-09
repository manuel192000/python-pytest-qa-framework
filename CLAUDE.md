# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Public portfolio project: a Python/Pytest QA automation framework that the owner (Manuel, GitHub `manuel192000`) will defend in SDET interviews. It is meant to grow into Playwright UI tests (Page Object Model), API tests, CI/CD and AI evals. Decisions must be defensible as senior-level and follow modern professional team practices, not generic tutorials. Never use code from the owner's employer in this repo.

## Commands

Package manager is `uv` (installed via Homebrew). Python >= 3.12.

```bash
uv sync                                   # create .venv and install from uv.lock
uv run pytest -v                          # run all tests
uv run pytest tests/unit/test_smoke.py::test_addition -v   # one test
uv run pytest -k "addition" -v            # tests by name expression
uv run ruff check .                       # lint (add --fix to autofix)
uv run ruff format .                      # format (use --check in CI)
```

## Architecture

- `src/qa_framework/` is the installable package (src layout, built with hatchling). Framework code (page objects, API clients, utilities) goes here, and tests import it as `qa_framework`. Tests must run against the installed package, so always go through `uv run`.
- `tests/` holds tests only. `tests/conftest.py` is for shared fixtures; tests are grouped by kind (`tests/unit/` now, UI/API/evals later).
- `pyproject.toml` is the single config for project metadata, dev dependency group, pytest (`--strict-markers --strict-config`: every marker must be registered) and ruff (rules E, F, I, UP, B; line length 100).
- `uv.lock` is committed and must never be edited by hand.

## Workflow rules

- Git history uses Conventional Commits (`chore:`, `feat:`, `fix:`, `docs:`, `test:`, `refactor:`). Work happens on branches and reaches `main` through Pull Requests.
- The owner types all git write commands himself to learn them. Do not run `git add`, `commit`, `push`, `switch`, `merge` or `gh pr` for him; give the exact command and ask him to run it (suggest the `! ` prefix). Read-only commands (`status`, `log`, `diff`) are fine.
- Reply in Spanish.

## Mentoring format

The owner is learning git, Python, pytest, Playwright, CI/CD, Azure DevOps release management and AI evals. After creating or changing anything, always explain: why, when it is used in real projects, and how to create it by hand. Interview questions must always include a broad, detailed answer.

## Learning notes

`docs/learning/` stores what the owner learns (concepts, configuration, interview Q&A), one file per topic. When something relevant is created or explained, add it to the matching file and keep `docs/learning/README.md` as the index. Record significant project decisions in this file.

## Status

- Done: repo, `main`, scaffold (uv, pytest, ruff, src layout, smoke test) via PR #1.
- Next: fixtures and parametrization, pre-commit, GitHub Actions CI, Playwright + Page Object Model, API tests, Azure Pipelines comparison, AI evals.
