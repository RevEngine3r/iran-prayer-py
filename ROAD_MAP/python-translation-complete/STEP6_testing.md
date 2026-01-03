# STEP 6: Testing Suite

## Objective

Create comprehensive test suite with unit tests, integration tests, and test fixtures to ensure code quality and correctness.

## Tasks

- ✅ Create test directory structure
- ✅ Add unit tests for calculator (astronomical algorithms)
- ✅ Add unit tests for model classes
- ✅ Add integration tests for end-to-end workflows
- ✅ Configure pytest with coverage reporting
- ✅ Add test documentation

## Implementation Details

### Test Structure

```
tests/
├── __init__.py
├── test_calculator.py       # Unit tests for calculator
├── test_models.py           # Unit tests for models
├── test_integration.py      # Integration tests
└── README.md                # Test documentation
```

### Unit Tests - Calculator (test_calculator.py)

**11 Test Methods:**

1. `test_default_parameters` - Verify default calculator params
2. `test_custom_parameters` - Verify custom params accepted
3. `test_julian_day_calculation` - Julian day accuracy
4. `test_solar_parameters` - Solar declination/equation of time
5. `test_hour_angle_calculation` - Hour angle validity
6. `test_calculate_returns_prayer_times` - Return type validation
7. `test_prayer_times_logical_order` - Chronological order
8. `test_maghrib_offset` - Maghrib offset accuracy
9. `test_timezone_awareness` - All times timezone-aware

**Coverage:** Astronomical algorithms, parameter validation, time calculations

### Unit Tests - Models (test_models.py)

**City Tests (6 methods):**
- `test_all_cities_exist` - All 10 cities defined
- `test_tehran_coordinates` - Coordinate accuracy
- `test_persian_names` - Persian name validation
- `test_display_name` - Display name formatting
- `test_str_representation` - String conversion
- `test_all_cities_have_required_attributes` - Complete data

**PrayerTimes Tests (5 methods):**
- `test_creation` - Dataclass instantiation
- `test_immutability` - Frozen dataclass enforcement
- `test_format_all_default` - Default formatting
- `test_format_all_custom_pattern` - Custom patterns
- `test_str_representation` - String output

**Coverage:** Data model validation, formatting, immutability

### Integration Tests (test_integration.py)

**10 Test Methods:**

1. `test_simple_city_calculation` - Basic workflow
2. `test_factory_method` - Factory method pattern
3. `test_static_method_coordinates` - Static method usage
4. `test_specific_date_calculation` - Date parameter
5. `test_custom_calculator` - Custom parameters
6. `test_multiple_cities` - Multi-city calculations
7. `test_format_all_integration` - Formatting workflow
8. `test_winter_summer_difference` - Seasonal variation
9. `test_all_cities_calculate` - All cities work

**Coverage:** End-to-end workflows, API patterns, real-world usage

### Test Configuration

**pyproject.toml pytest settings:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=iran_prayer",
    "--cov-report=term-missing",
    "--cov-report=html",
]
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=iran_prayer

# Specific file
pytest tests/test_calculator.py

# Verbose
pytest -v
```

### Test Coverage

**Target Coverage:**
- Overall: >80%
- Calculator: >90%
- Models: 100%
- Main API: >85%

**Key Areas Tested:**
- Astronomical calculations
- Data model integrity
- API usability
- Edge cases
- Timezone handling
- Date variations
- Parameter validation

## Test Documentation

**tests/README.md:**
- Test structure overview
- Running instructions
- Coverage goals
- Writing new tests
- CI/CD integration

## Files Created

1. `tests/__init__.py` - Test package init
2. `tests/test_calculator.py` - Calculator unit tests (196 lines)
3. `tests/test_models.py` - Model unit tests (150 lines)
4. `tests/test_integration.py` - Integration tests (144 lines)
5. `tests/README.md` - Test documentation

**Total:** 490+ lines of test code

## Test Quality

- ✅ All tests have type hints
- ✅ Descriptive docstrings
- ✅ AAA pattern (Arrange, Act, Assert)
- ✅ Clear test names
- ✅ Isolated tests (no dependencies)
- ✅ Fast execution

## Next Step

Finalize package with CI/CD, documentation updates, and final polish.
