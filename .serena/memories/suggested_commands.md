# STRR — Development Commands

```bash
uv run python -m STRR.main                    # Run the game
uv run pytest STRR/tests/ -v                  # Run all tests
uv run pytest STRR/tests/ -m unit -v          # Unit tests only (no display)
uv run mypy STRR/src/                         # Type check
uv run ruff check STRR/src/ STRR/tests/       # Lint
```

## Git
- Work on `testing` branch
- Never push to `main`
