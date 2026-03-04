# Description

Briefly describe what this PR does and why.

Fixes # (issue)

## Type of Change

- [ ] Bug fix
- [ ] New game feature
- [ ] Refactoring / code quality
- [ ] Documentation update
- [ ] Test coverage improvement

## How Has This Been Tested?

Describe how you tested your changes.

- [ ] Ran test suite: `pytest STRR/tests/`
- [ ] Manual gameplay testing (describe scenario)

## Checklist

### Code Quality
- [ ] Code follows hybrid architecture (MVC + Component pattern)
- [ ] SOLID principles maintained
- [ ] Type hints added to all new functions/methods
- [ ] Docstrings use the project's standard header format

### Testing
- [ ] Tests pass: `pytest STRR/tests/`
- [ ] Type checking passes: `mypy STRR/src/`
- [ ] Linting passes: `ruff check STRR/`
- [ ] Formatting: `black --check STRR/`

### Game-Specific
- [ ] Turn-based mechanics respected (actions consume turns, initiative order maintained)
- [ ] 3D coordinates used where applicable (`Position(x, y, z)`)
- [ ] State transitions follow the defined state machine

### Branch & Documentation
- [ ] Changes were developed on `testing` branch (not `main`)
- [ ] This PR targets `testing` (not `main`)
- [ ] CHANGELOG.md updated if this is a non-trivial change
- [ ] README updated if needed

## Screenshots / Logs (if applicable)

```
Paste logs or describe gameplay test results here
```
