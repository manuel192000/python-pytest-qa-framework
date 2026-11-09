# Python Pytest QA Framework

Test automation framework built with Python and Pytest for QA.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`brew install uv`)

## Setup

```bash
uv sync
```

## Common commands

```bash
uv run pytest -v              # run the tests
uv run ruff check .           # lint
uv run ruff format .          # format
```

## Project structure

```
.
├── src/qa_framework/   # Framework code: page objects, API clients, utilities
├── tests/
│   ├── conftest.py     # Shared fixtures
│   └── unit/           # Unit and smoke tests
├── pyproject.toml      # Project metadata, dependencies and tool config
└── uv.lock             # Locked dependency versions (reproducible installs)
```

## Roadmap

- [x] Project scaffold (uv, pytest, ruff)
- [x] Fixtures and parametrization
- [ ] Playwright UI tests with Page Object Model
- [ ] API tests
- [ ] CI with GitHub Actions
- [ ] Reporting and flaky test handling
- [ ] AI evals

## Author

Manuel — [@manuel192000](https://github.com/manuel192000)
