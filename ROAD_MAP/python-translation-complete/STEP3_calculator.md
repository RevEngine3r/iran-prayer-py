# STEP 3: Core Calculator Implementation

## Objective

Translate the PrayerTimeCalculator from Kotlin to Python with complete astronomical algorithms for accurate prayer time calculations.

## Tasks

- ✅ Translate PrayerTimeCalculator.kt → prayer_time_calculator.py
- ✅ Implement Julian day calculations
- ✅ Implement solar position algorithms (declination, equation of time)
- ✅ Implement hour angle calculations
- ✅ Add Asr calculation with shadow factor
- ✅ Add configurable parameters
- ✅ Full type hints and documentation

## Implementation Details

### Class Structure

**PrayerTimeCalculator** - Main calculator class with configurable parameters:

**Constructor Parameters:**
- `fajr_angle` (float): Sun angle below horizon for Fajr (default: 17.7°)
- `isha_angle` (float): Sun angle below horizon for Isha (default: 14.0°)
- `sunrise_sunset_altitude` (float): Geometric altitude (default: -0.833°)
- `asr_shadow_factor` (float): Shadow ratio - 1.0 for Shafii, 2.0 for Hanafi
- `maghrib_offset_minutes` (int): Minutes after sunset (default: 21)

### Astronomical Algorithms

#### 1. Julian Day Calculation
```python
def _calculate_julian_day(self, date: datetime) -> float
```
- Converts Gregorian calendar date to Julian day number
- Used for accurate astronomical calculations
- Handles month/year adjustments for Jan/Feb

#### 2. Solar Parameters
```python
def _calculate_solar_parameters(self, julian_day: float) -> Tuple[float, float]
```
- Calculates solar declination (angle relative to celestial equator)
- Calculates equation of time (difference between solar and mean time)
- Uses mean anomaly, ecliptic longitude, and obliquity
- Returns: (declination in radians, equation of time in minutes)

#### 3. Hour Angle Calculations
```python
def _calculate_hour_angle(altitude_degrees, latitude, declination) -> float
```
- Determines when sun reaches specific altitude angle
- Used for Fajr, Sunrise, Sunset, Isha calculations
- Uses spherical trigonometry

```python
def _calculate_asr_hour_angle(shadow_factor, latitude, declination) -> float
```
- Special calculation for Asr based on shadow length
- Shadow factor 1.0 = Shafii method (shadow = object height)
- Shadow factor 2.0 = Hanafi method (shadow = 2× object height)

#### 4. Time Conversion
```python
def _convert_to_local_time(date, utc_minutes, tz_offset, zone_info) -> datetime
```
- Converts UTC minutes since midnight to local datetime
- Applies timezone offset
- Uses proper rounding (round half up) to avoid bias
- Returns timezone-aware datetime

### Prayer Time Calculations

**Main method:**
```python
def calculate(date, latitude, longitude, time_zone) -> PrayerTimes
```

**Calculation Steps:**

1. **Setup:**
   - Calculate timezone offset
   - Get Julian day
   - Calculate solar parameters
   - Determine solar noon

2. **Sunrise/Sunset:**
   - Use sunrise_sunset_altitude (-0.833° for atmospheric refraction)
   - Calculate symmetric around solar noon

3. **Fajr/Isha:**
   - Use configured angles (17.7° and 14.0° for Iran)
   - Calculate before/after solar noon

4. **Dhuhr:**
   - Exact solar noon (sun at highest point)

5. **Asr:**
   - Based on shadow length ratio
   - Calculate hour angle from shadow factor

6. **Maghrib:**
   - Sunset + configured offset (21 minutes)

7. **Midnight:**
   - Midpoint between sunset and next day's Fajr
   - Requires calculating next day's Fajr first

### Key Translation Differences

**Kotlin → Python:**

1. **Math Functions:**
   - `Math.toRadians()` → `math.radians()`
   - `Math.toDegrees()` → `math.degrees()`
   - `kotlin.math.sin()` → `math.sin()`

2. **DateTime:**
   - `ZonedDateTime` → `datetime` with `ZoneInfo`
   - `Duration.between()` → timedelta arithmetic
   - `plusMinutes()` → `+ timedelta(minutes=...)`

3. **Type Safety:**
   - All methods have type hints
   - Return types explicitly declared
   - Tuple type hints for multiple returns

4. **Naming Conventions:**
   - `camelCase` → `snake_case`
   - Private methods prefixed with `_`

## Accuracy Considerations

- **Rounding:** Uses round-half-up to avoid systematic bias
- **Angle Wrapping:** Proper handling of 0-360° range
- **Clamping:** Hour angle cosine clamped to [-1, 1] for acos
- **Timezone:** Proper handling of DST and timezone offsets

## Default Parameters (Iran)

Following Institute of Geophysics, University of Tehran:
- **Fajr angle:** 17.7° below horizon
- **Isha angle:** 14.0° below horizon (Shia Ithna Ashari)
- **Maghrib offset:** 21 minutes after sunset
- **Asr method:** Shafii (shadow factor = 1.0)

## File Created

`src/iran_prayer/calculator/prayer_time_calculator.py` (293 lines)
- Complete astronomical calculator
- 8 methods (1 public, 7 private)
- Full type hints and docstrings
- Exact functional parity with Kotlin version

## Next Step

Implement the main API class (IranPrayerTimes) that provides high-level interface for users.
