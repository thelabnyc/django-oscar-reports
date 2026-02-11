# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

django-oscar-reports is a Django app that extends django-oscar's Dashboard with an improved report generation system. It enables asynchronous report generation using django-tasks.

## Development Commands

**IMPORTANT**: All test, mypy, and tox commands MUST be run inside Docker containers because the project requires PostgreSQL. Use `docker compose run --rm test <command>` for all testing and type checking commands.

### Environment Setup
```bash
# Start PostgreSQL service
docker compose up -d postgres

# Install dependencies (for local development/editing only)
# Note: For running tests, dependencies are installed automatically in Docker
uv sync --all-extras

# Install pre-commit hooks (local only)
make install_precommit
```

### Testing
**All test commands must run in Docker:**

```bash
# Run all tests across all Python/Django/Oscar combinations
docker compose run --rm test bash -c "uv sync --all-extras && uv run tox"

# Run tests for specific Python version (e.g., py313 only)
docker compose run --rm -e TOX_SKIP_ENV="^(?!py313-)" test bash -c "uv sync --all-extras && uv run tox"

# Run a single tox environment
docker compose run --rm test bash -c "uv sync --all-extras && uv run tox -e py313-django420-oscar40"

# Run Django tests directly (requires specific Django/Oscar versions in container)
docker compose run --rm test ./manage.py test oscarreports -v 2 --buffer --noinput

# Run tests with coverage
docker compose run --rm test bash -c "coverage erase && coverage run ./manage.py test oscarreports -v 2 --buffer --noinput && coverage report"
```

### Type Checking
**mypy must run in Docker:**

```bash
# Run mypy type checking via tox
docker compose run --rm test bash -c "uv sync --all-extras && uv run tox -e py313-types"

# Run mypy directly
docker compose run --rm test bash -c "uv sync --all-extras && uv run mypy oscarreports/ sandbox/"
```

### Code Quality
```bash
# Run all pre-commit checks
make test_precommit

# Format code with ruff
make fmt

# Run ruff linting
ruff check .
```

### Local Development Server
**Note**: Development server can run locally if PostgreSQL is accessible at `localhost:5432`, or run in Docker:

```bash
# Option 1: Run locally (requires PostgreSQL at localhost:5432)
./manage.py migrate
./manage.py runserver

# Option 2: Run in Docker container
docker compose up -d postgres
docker compose run --rm -p 8000:8000 test bash -c "./manage.py migrate && ./manage.py runserver 0.0.0.0:8000"
```

## Architecture

### Core Components

**Report Model** (`oscarreports/models.py`):
- Central model representing an asynchronous report generation job
- Tracks lifecycle: created → queued → in-progress → completed
- Stores metadata: owner, type_code, description, date_range, task_id
- Generates and stores report files using Django's FileField
- Sends email alerts when reports complete

**Task System** (`oscarreports/tasks.py`):
- Uses django-tasks `@task()` decorator for async task execution
- `generate_report` task handles report generation in the background

**Views** (`oscarreports/views.py`):
- `IndexView`: Dashboard view displaying report list and generation form
- `ReportDownloadView`: Serves generated report files with proper MIME types
- `ReportDeleteView`: Handles report deletion

**Generator Repository** (`oscarreports/utils.py`):
- Extends Oscar's report generator registry system
- Allows registration of custom report generators
- Integrates with Oscar's existing `ReportGenerator` classes

### Key Patterns

**Report Lifecycle**:
1. User submits form via `IndexView.post()`
2. `Report` instance created with type_code and date_range
3. `report.queue()` schedules async task and updates status
4. Task calls `report.generate()` which:
   - Instantiates appropriate `ReportGenerator`
   - Generates report content
   - Saves file to `MEDIA_ROOT/{OSCAR_REPORTS_UPLOAD_PREFIX}/{YYYY}/{MM}/{DD}/{uuid}.{ext}`
   - Sends completion email
5. User downloads via `ReportDownloadView`

**Signal Handlers** (`oscarreports/handlers.py`):
- `pre_delete` signal auto-deletes associated file when Report is deleted

**Type Safety**:
- Project uses strict mypy configuration (see `pyproject.toml` [tool.mypy])
- Uses `django-stubs` and `django-stubs-ext` for Django type checking
- Functions require full type annotations

## Configuration Settings

**Required Database**: PostgreSQL (uses `DateTimeRangeField` from django.contrib.postgres)

**Settings**:
- `OSCAR_REPORTS_UPLOAD_PREFIX`: Directory prefix for uploaded reports (default: "oscar-reports")
- `OSCAR_FROM_EMAIL`: Email address for report completion alerts

## Integration with Oscar

This app replaces Oscar's default `oscar.apps.dashboard.reports` app. Note in `sandbox/settings.py` that the standard `ReportsDashboardConfig` is commented out and `oscarreports` is added instead.

Custom report generators should:
1. Subclass `oscar.apps.dashboard.reports.reports.ReportGenerator`
2. Register via `GeneratorRepository.register(MyReportGenerator)`
3. Implement required attributes: `code`, `description`

## Testing Configuration

- **PostgreSQL Required**: Tests MUST run in Docker containers (see Testing section above)
- Uses `unittest-xml-reporting` for JUnit XML output
- Tests run against PostgreSQL service provided by docker-compose
- Coverage tracked via coverage.py (configured in `pyproject.toml`)
- Uses `freezegun` for time-based test control
- Uses `django-webtest`/`WebTest` for integration tests
- Docker container has Python 3.13; use `TOX_SKIP_ENV` to run only py313 tests locally

## CI/CD

- GitLab CI configuration in `.gitlab-ci.yml`
- Tests run in parallel for py312 and py313
- Uses thelabnyc CI components for pre-commit checks and releases
- Automated publishing to PyPI and GitLab releases
- Version managed via commitizen (conventional commits)

## Code Standards

- Python 3.12+ required
- Strict mypy type checking enabled
- Ruff for linting and formatting (replaces black/flake8)
- isort for import sorting (from-first style)
- Pre-commit hooks enforce: pyupgrade, django-upgrade, ruff, conventional commits
- Target Django 4.2+ compatibility
