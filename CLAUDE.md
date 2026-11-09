# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Portfolio project: a Python/Pytest QA automation framework that will grow into Playwright UI tests (Page Object Model), API tests and AI evals. Follow modern professional team practices, and never use code from the owner's employer in this repo.

## Commands

Package manager is `uv`. Python is pinned in `.python-version`.

```bash
uv sync                                   # create .venv and install from uv.lock
uv run pytest -v                          # run all tests
uv run pytest tests/unit/test_validators.py::test_default_user_passes_all_rules -v   # one test
uv run pytest -k "email" -v               # tests by name expression
uv run pytest -m smoke                    # tests by marker (smoke, regression)
uv run ruff check .                       # lint (add --fix to autofix)
uv run ruff format .                      # format (use --check in CI)
uv run pre-commit install                 # once per clone: enable the git hook
uv run pre-commit run --all-files         # run every hook against the whole repo
```

## Architecture

- `src/qa_framework/` is the installable package (src layout, built with hatchling). Framework code goes here and tests import it as `qa_framework`. Tests must run against the installed package, so always go through `uv run`.
- `tests/` holds tests only. `tests/conftest.py` is for shared fixtures; tests are grouped by kind (`tests/unit/` now, UI/API/evals later).
- `pyproject.toml` is the single config for metadata (including the only copy of the version), the dev dependency group, pytest (`--strict-markers --strict-config`: every marker must be registered) and ruff.
- `uv.lock` is committed and never edited by hand.
- `.pre-commit-config.yaml` pins hook versions; keep the ruff hook `rev` equal to the ruff version in `uv.lock`.
- `.github/workflows/ci.yml` runs the same `uv run` commands as local on pull requests and pushes to `main`. pytest exits non-zero when it collects no tests, so `tests/` must always contain at least one test or CI fails.
- `main` is protected by the `Protect main` ruleset: pull request required, `Lint and tests` check required, no force pushes, no deletion.

## Workflow rules

- Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `ci:`). Work happens on branches and reaches `main` through squash-merged Pull Requests.
- Reply in Spanish, one concept per step and in short messages; the owner has said it is hard to keep up with long explanations.
- By default the owner types git write commands to learn them: give the exact command and explain it. Read-only commands are fine to run. Run write commands only when the owner explicitly asks for that task.

## Mentoring format

The owner is learning this stack. After creating or changing anything, explain why, when it is used in real projects, and how to create it by hand. Interview questions always include a broad, detailed answer.

## Learning notes

`docs/learning/` stores what the owner learns, one file per topic, with `docs/learning/README.md` as the index. Add new concepts to the matching file.

## Plan

- The owner will rewrite the tests from scratch while learning Playwright. Keep the infrastructure (uv, pre-commit, CI, ruleset). Replace `validators.py` and its tests only once a new test exists, so CI keeps collecting tests.
- Next: demonstrate the ruleset with a deliberately failing PR, Python refresher, Playwright + Page Object Model against a real demo site, API tests, Azure Pipelines comparison, AI evals.
- Before job applications start (around January 2027): move `docs/learning/` and the mentoring sections of this file to a private repo, then remove them from the public history (rewrite with the ruleset temporarily disabled, or publish a fresh repo).
