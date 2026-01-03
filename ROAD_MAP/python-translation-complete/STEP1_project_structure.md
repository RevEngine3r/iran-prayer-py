# STEP 1: Project Structure and Build Configuration

## Objective

Create a modern Python project structure following current best practices with proper packaging configuration.

## Tasks

- ✅ Create `pyproject.toml` with setuptools configuration
- ✅ Add comprehensive `.gitignore` for Python projects
- ✅ Add MIT LICENSE file
- ✅ Create src layout: `src/iran_prayer/`
- ✅ Create subpackages: `calculator/`, `model/`, `examples/`
- ✅ Add `__init__.py` files with proper imports
- ✅ Add `py.typed` marker for type checking

## Implementation Details

### Build System

- Using setuptools (>=68.0) as build backend
- Python 3.10+ requirement for modern type hints
- Proper package discovery with src layout

### Development Tools

- **pytest**: Testing framework
- **mypy**: Static type checking
- **ruff**: Fast linting
- **black**: Code formatting

### Package Structure

```
src/iran_prayer/
├── __init__.py          # Main exports
├── py.typed             # Type marker
├── calculator/
│   └── __init__.py
├── model/
│   └── __init__.py
└── examples/
    └── __init__.py
```

## Files Created

1. `pyproject.toml` - Modern Python packaging configuration
2. `.gitignore` - Comprehensive Python ignore patterns
3. `LICENSE` - MIT license
4. `src/iran_prayer/__init__.py` - Main package init
5. `src/iran_prayer/py.typed` - Type checking marker
6. `src/iran_prayer/calculator/__init__.py` - Calculator subpackage
7. `src/iran_prayer/model/__init__.py` - Model subpackage
8. `src/iran_prayer/examples/__init__.py` - Examples subpackage

## Next Step

Translate model classes (City enum and PrayerTimes dataclass) from Kotlin to Python.
