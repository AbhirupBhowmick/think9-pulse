# Think9 Pulse Test Suite

This directory contains automated unit and integration tests for the Think9 Pulse backend.

## Running Tests

From the root project directory:

```bash
pytest tests/backend
```

Or from `backend/`:

```bash
python -m pytest ../tests/backend
```

## Test Structure
- `conftest.py`: In-memory SQLite database setup, session overrides, and seed data fixtures.
- `test_health.py`: Validates `GET /api/v1/health` and database connectivity status.
- `test_brands.py`: Validates Think9 brand listing and ID lookup endpoints.
- `test_signals.py`: Validates consumer signal listing and ID lookup endpoints.
- `test_opportunities.py`: Validates opportunity listing, detailed workbench responses, and evidence linkage.
