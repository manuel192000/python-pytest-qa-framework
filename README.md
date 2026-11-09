# Python Pytest QA Framework

![CI](https://github.com/manuel192000/python-pytest-qa-framework/actions/workflows/ci.yml/badge.svg)

Test automation framework built with Python and Pytest for QA.

## Requirements

- [uv](https://docs.astral.sh/uv/) (`brew install uv`). It installs the Python version pinned in `.python-version`.

## Setup

```bash
uv sync
uv run pre-commit install
```

## Common commands

```bash
uv run pytest -v                    # run the tests
uv run pytest -m smoke              # run only the smoke tests
uv run ruff check .                 # lint
uv run ruff format .                # format
uv run pre-commit run --all-files   # run every pre-commit hook
```

## Project structure

```
.
├── .github/workflows/  # CI pipeline
├── src/qa_framework/   # Framework code: page objects, API clients, utilities
├── tests/
│   ├── conftest.py     # Shared fixtures
│   └── unit/           # Unit tests
├── pyproject.toml      # Project metadata, dependencies and tool config
└── uv.lock             # Locked dependency versions (reproducible installs)
```

## Quality gates

- **Before each commit:** pre-commit runs ruff and basic file checks.
- **On each pull request and push to `main`:** GitHub Actions runs lint, format check and tests.
- **`main` is protected:** changes arrive through pull requests with a passing CI check.

## Roadmap

- [x] Project scaffold (uv, pytest, ruff)
- [x] Fixtures and parametrization
- [x] Pre-commit hooks
- [x] CI with GitHub Actions
- [x] Branch protection
- [ ] Playwright UI tests with Page Object Model
- [ ] API tests
- [ ] Reporting and flaky test handling
- [ ] AI evals

## Author

Manuel — [@manuel192000](https://github.com/manuel192000)
