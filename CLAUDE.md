# CLAUDE.md - Coding Agent Instructions

## Project Setup
- This project uses **uv** for package management
- Use `uv add <package>` to add dependencies
- Use `uv run <command>` to execute commands

## Quick Testing
```bash
# CLI testing (recommended for coding agents)
uv run python -m src.cli -i test_input.json -o output.png
```

## API Server
- Start server: `uv run python -m src.main`
- **Note**: API server testing should be done by the user, not coding agents
- Server runs on http://localhost:8000

## Code Guidelines
- Keep comments in English
- Follow existing patterns
- See `docs/architecture.md` for detailed project structure

## Key Files
- `src/`: Main source code
- `test_input.json`: Sample data for testing
- `docs/architecture.md`: Detailed architecture documentation
