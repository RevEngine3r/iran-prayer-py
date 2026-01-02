# STEP 2: Model Classes Translation

## Objective

Translate Kotlin model classes (City enum and PrayerTimes data class) to Python with full type safety and documentation.

## Tasks

- ✅ Translate City.kt → city.py
- ✅ Translate PrayerTimes.kt → prayer_times.py
- ✅ Add comprehensive type hints
- ✅ Add detailed docstrings
- ✅ Implement utility methods (format_all, __str__)

## Implementation Details

### City Enum (city.py)

**Translation Approach:**
- Kotlin `enum class` → Python `Enum`
- Properties passed to enum constructor
- All 10 Iranian cities with coordinates
- Persian names, lat/long, timezone data

**Features:**
- `persian_name`: Persian city name (e.g., "تهران")
- `latitude`: Geographic latitude in degrees
- `longitude`: Geographic longitude in degrees  
- `time_zone`: IANA timezone ("Asia/Tehran")
- `display_name` property: Capitalized English name
- `__str__` method for string representation

**Cities Included:**
1. Tehran (تهران)
2. Tabriz (تبریز)
3. Mashhad (مشهد)
4. Isfahan (اصفهان)
5. Shiraz (شیراز)
6. Qom (قم)
7. Ahvaz (اهواز)
8. Kermanshah (کرمانشاه)
9. Rasht (رشت)
10. Yazd (یزد)

### PrayerTimes Dataclass (prayer_times.py)

**Translation Approach:**
- Kotlin `data class` → Python `@dataclass(frozen=True)`
- Immutable for safety (frozen=True)
- Using `datetime` instead of `ZonedDateTime`
- Type hints for all fields

**Attributes (all datetime):**
- `fajr`: Dawn prayer
- `sunrise`: Sunrise time
- `dhuhr`: Noon prayer
- `asr`: Afternoon prayer
- `sunset`: Sunset time
- `maghrib`: Evening prayer
- `isha`: Night prayer
- `midnight`: Islamic midnight

**Methods:**
- `format_all(pattern)`: Format all times with custom pattern
- `__str__()`: Pretty-printed prayer times

## Key Differences from Kotlin

1. **Enum Implementation:**
   - Kotlin: Properties in enum constructor
   - Python: Tuple values with `__init__` method

2. **DateTime Handling:**
   - Kotlin: `ZonedDateTime` (java.time)
   - Python: `datetime` (stdlib, timezone-aware)

3. **Immutability:**
   - Kotlin: `data class` immutable by default
   - Python: `@dataclass(frozen=True)` for immutability

4. **String Formatting:**
   - Kotlin: `DateTimeFormatter.ofPattern()`
   - Python: `datetime.strftime()`

## Files Created

1. `src/iran_prayer/model/city.py` - City enumeration with geographic data
2. `src/iran_prayer/model/prayer_times.py` - Prayer times dataclass

## Type Safety

- All methods have complete type hints
- Return types explicitly declared
- Compatible with mypy strict mode
- py.typed marker enables type checking

## Next Step

Translate the core calculator with astronomical algorithms from PrayerTimeCalculator.kt.
