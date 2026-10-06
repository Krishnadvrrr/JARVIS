# Skill: Python Clean Code Standards
keywords: [python, backend, script, cli, oop, functions, clean code]

## 1. Principles
- Follow PEP 8 naming conventions: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE` for constants.
- Include explicit type hints (`typing.List`, `typing.Dict`, `typing.Optional`, `typing.Tuple`).
- Every module, class, and public function must have clear docstrings.

## 2. Robust Error Handling
- Never use bare `except:`; always catch specific exceptions (`except (ValueError, KeyError) as e:`).
- Gracefully handle file I/O using context managers (`with open(...) as f:`).
- Always clean up resources and use logging instead of raw print statements where applicable.

## 3. Modular Architecture
- Separate concerns: configuration, business logic, persistence, and presentation/CLI.
- Avoid global mutable state. Pass dependencies explicitly or via configuration classes.
- Make code testable with pure functions where possible.
