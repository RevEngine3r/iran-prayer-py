# STEP 4: Main API Implementation

## Objective

Translate the main IranPrayerTimes class from Kotlin to Python, providing a clean, user-facing API for prayer time calculations.

## Tasks

- ✅ Translate IranPrayerTimes.kt → iran_prayer_times.py
- ✅ Implement main class with city integration
- ✅ Add factory method (for_city)
- ✅ Add static method for custom coordinates
- ✅ Full type hints and documentation
- ✅ Add usage examples in docstrings

## Implementation Details

### Class Structure

**IranPrayerTimes** - Main user-facing API class

**Constructor:**
```python
def __init__(self, city: City, calculator: Optional[PrayerTimeCalculator] = None)
```
- Takes a City enum value
- Optional custom calculator for advanced users
- Stores city and calculator for reuse

**Instance Method:**
```python
def calculate(self, date: Optional[datetime] = None) -> PrayerTimes
```
- Calculate prayer times for the configured city
- Date defaults to today in city's timezone
- Returns complete PrayerTimes object

**Class Method (Factory):**
```python
@classmethod
def for_city(cls, city: City) -> "IranPrayerTimes"
```
- Alternative constructor syntax
- Cleaner for simple use cases
- Returns configured instance

**Static Method:**
```python
@staticmethod
def calculate_for_coordinates(
    latitude: float,
    longitude: float,
    date: Optional[datetime] = None,
    time_zone: str = "Asia/Tehran",
    calculator: Optional[PrayerTimeCalculator] = None,
) -> PrayerTimes
```
- For custom locations (not pre-configured cities)
- All parameters explicit
- Returns PrayerTimes directly

## Usage Patterns

### Pattern 1: Simple City-Based
```python
from iran_prayer import IranPrayerTimes, City

prayer_times = IranPrayerTimes(City.TEHRAN)
times = prayer_times.calculate()
print(times)
```

### Pattern 2: Factory Method
```python
prayer_times = IranPrayerTimes.for_city(City.MASHHAD)
times = prayer_times.calculate()
```

### Pattern 3: Specific Date
```python
from datetime import datetime

prayer_times = IranPrayerTimes(City.SHIRAZ)
ramadan_times = prayer_times.calculate(datetime(2026, 2, 28))
```

### Pattern 4: Custom Coordinates
```python
times = IranPrayerTimes.calculate_for_coordinates(
    latitude=36.3264,
    longitude=59.5433,
    date=datetime(2026, 1, 2),
    time_zone="Asia/Tehran"
)
```

### Pattern 5: Custom Calculator
```python
from iran_prayer import PrayerTimeCalculator

custom_calc = PrayerTimeCalculator(
    fajr_angle=18.0,  # Different angle
    isha_angle=15.0,
    maghrib_offset_minutes=20
)

prayer_times = IranPrayerTimes(City.QOM, calculator=custom_calc)
times = prayer_times.calculate()
```

## Key Translation Differences

**Kotlin → Python:**

1. **Companion Object:**
   - Kotlin: `companion object { fun forCity() }`
   - Python: `@classmethod` and `@staticmethod`

2. **Default Parameters:**
   - Kotlin: `date: LocalDate? = null`
   - Python: `date: Optional[datetime] = None`

3. **Optional/Nullable:**
   - Kotlin: Nullable types with `?`
   - Python: `Optional[Type]` from typing

4. **Property Access:**
   - Kotlin: `city.timeZone` (camelCase)
   - Python: `city.time_zone` (snake_case)

5. **DateTime:**
   - Kotlin: `LocalDate.now(zoneId)`
   - Python: `datetime.now(zone_info)`

## Design Principles

1. **Simplicity First:**
   - Most common use case (city + today) requires minimal code
   - `IranPrayerTimes(City.TEHRAN).calculate()`

2. **Flexibility:**
   - Support custom dates
   - Support custom calculators
   - Support arbitrary coordinates

3. **Type Safety:**
   - All parameters and returns typed
   - Optional parameters clearly marked
   - Compatible with mypy strict mode

4. **Documentation:**
   - Every method has comprehensive docstring
   - Usage examples in docstrings
   - Clear parameter descriptions

## API Surface

**Public Methods:**
- `__init__(city, calculator=None)` - Constructor
- `calculate(date=None)` - Instance method
- `for_city(city)` - Class method factory
- `calculate_for_coordinates(...)` - Static method

**Public Attributes:**
- `city` - The configured City enum
- `calculator` - The calculator instance

## Integration with Other Components

**Dependencies:**
- `City` from `iran_prayer.model.city`
- `PrayerTimes` from `iran_prayer.model.prayer_times`
- `PrayerTimeCalculator` from `iran_prayer.calculator.prayer_time_calculator`

**Used By:**
- End users (direct API)
- Example scripts
- Applications and libraries

## File Created

`src/iran_prayer/iran_prayer_times.py` (127 lines)
- Main API class
- 4 public methods
- Complete type hints
- Extensive docstrings with examples
- Clean, Pythonic interface

## Next Step

Create examples and comprehensive documentation (README, usage examples, API reference).
