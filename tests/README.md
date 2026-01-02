# Test Suite

Comprehensive test suite for the Iran Prayer Times library.

## Test Structure

```
tests/
├── __init__.py
├── test_calculator.py       # Unit tests for calculator algorithms
├── test_models.py           # Unit tests for model classes
├── test_integration.py      # Integration tests
└── README.md                # This file
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_calculator.py
pytest tests/test_models.py
pytest tests/test_integration.py
```

### Run with Coverage

```bash
pytest --cov=iran_prayer --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test

```bash
pytest tests/test_calculator.py::TestPrayerTimeCalculator::test_default_parameters
```

## Test Categories

### Unit Tests - Calculator (`test_calculator.py`)

Tests for astronomical calculation algorithms:
- Default and custom parameters
- Julian day calculations
- Solar parameter calculations (declination, equation of time)
- Hour angle calculations
- Prayer time logical order
- Maghrib offset validation
- Timezone awareness

### Unit Tests - Models (`test_models.py`)

Tests for data models:
- City enum attributes and properties
- Persian names and coordinates
- PrayerTimes dataclass creation
- Immutability (frozen dataclass)
- Formatting methods
- String representations

### Integration Tests (`test_integration.py`)

End-to-end workflow tests:
- Simple city calculations
- Factory method usage
- Static method for custom coordinates
- Specific date calculations
- Custom calculator parameters
- Multiple cities comparison
- Format integration
- Seasonal differences
- All cities validation

## Test Coverage Goals

- **Overall:** >80% coverage
- **Calculator:** >90% coverage
- **Models:** 100% coverage
- **Main API:** >85% coverage

## Writing New Tests

### Test Naming Convention

```python
def test_<feature_being_tested>(self) -> None:
    """Brief description of what is being tested."""
```

### Test Structure

```python
class Test<ClassName>:
    """Test suite for <ClassName>."""
    
    def test_<scenario>(self) -> None:
        """Test description."""
        # Arrange
        setup_code()
        
        # Act
        result = method_under_test()
        
        # Assert
        assert result == expected
```

### Type Hints

All test methods should have return type annotation `-> None`.

## CI/CD Integration

Tests are run automatically on:
- Pull requests
- Commits to main branch
- Release tags

## Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

Install with:
```bash
pip install -e ".[dev]"
```
