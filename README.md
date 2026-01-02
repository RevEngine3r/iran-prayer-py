# Iran Prayer Times

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Type Hints](https://img.shields.io/badge/type%20hints-mypy-blue.svg)](https://mypy.readthedocs.io/)

A modern Python library for calculating accurate Islamic prayer times for major cities in Iran using astronomical algorithms.

Translated from the [iran-prayer-kt](https://github.com/RevEngine3r/iran-prayer-kt) Kotlin library with full feature parity.

## ✨ Features

- 🕌 Calculate all daily prayer times (Fajr, Sunrise, Dhuhr, Asr, Sunset, Maghrib, Isha, Midnight)
- 🇮🇷 Pre-configured coordinates for 10 major Iranian cities
- 🌍 Support for custom coordinates and timezones
- 🔬 Astronomical calculations using Julian day and solar position algorithms
- ⏰ Accurate timezone handling with ZoneInfo
- 🎯 Configurable calculation parameters (Fajr/Isha angles, Asr shadow factor)
- 📝 Full type hints for IDE support and type checking
- 🏗️ Modern Python package with src layout
- ✅ Compatible with Python 3.10+

## 🏛️ Supported Cities

| English | Persian | Coordinates |
|---------|---------|-------------|
| Tehran | تهران | 35.69°N, 51.39°E |
| Tabriz | تبریز | 38.08°N, 46.29°E |
| Mashhad | مشهد | 36.33°N, 59.54°E |
| Isfahan | اصفهان | 32.65°N, 51.67°E |
| Shiraz | شیراز | 29.59°N, 52.58°E |
| Qom | قم | 34.64°N, 50.88°E |
| Ahvaz | اهواز | 31.32°N, 48.67°E |
| Kermanshah | کرمانشاه | 34.31°N, 47.07°E |
| Rasht | رشت | 37.28°N, 49.58°E |
| Yazd | یزد | 31.90°N, 54.36°E |

## 📋 Requirements

- **Python:** 3.10 or higher
- **Dependencies:** None (uses standard library only)

## 🚀 Installation

### From Source

```bash
git clone https://github.com/RevEngine3r/iran-prayer-py.git
cd iran-prayer-py
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## 💻 Usage

### Basic Usage - City-based Calculation

```python
from iran_prayer import IranPrayerTimes, City

# Create instance for a city
prayer_times = IranPrayerTimes(City.TEHRAN)

# Calculate prayer times for today
times = prayer_times.calculate()

# Print all times
print(times)
# Output:
# Prayer Times:
# Fajr:     05:41
# Sunrise:  07:11
# Dhuhr:    12:13
# Asr:      14:54
# Sunset:   17:14
# Maghrib:  17:35
# Isha:     18:36
# Midnight: 23:28
```

### Custom Date

```python
from datetime import datetime

prayer_times = IranPrayerTimes(City.MASHHAD)
ramadan_start = datetime(2026, 2, 28)
times = prayer_times.calculate(ramadan_start)
```

### Format Times

```python
times = IranPrayerTimes(City.SHIRAZ).calculate()

# Format all times with custom pattern
formatted = times.format_all("%H:%M:%S")
for name, time in formatted.items():
    print(f"{name}: {time}")
```

### Custom Coordinates

```python
times = IranPrayerTimes.calculate_for_coordinates(
    latitude=36.3264,   # Mashhad
    longitude=59.5433,
    time_zone="Asia/Tehran"
)
```

### Factory Method

```python
# Alternative syntax using class method
prayer_times = IranPrayerTimes.for_city(City.TABRIZ)
times = prayer_times.calculate()
```

### Custom Calculator Parameters

```python
from iran_prayer import PrayerTimeCalculator

custom_calculator = PrayerTimeCalculator(
    fajr_angle=17.7,              # Degrees below horizon
    isha_angle=14.0,              # Degrees below horizon
    sunrise_sunset_altitude=-0.833,  # Geometric correction
    asr_shadow_factor=1.0,        # 1.0 = Shafii, 2.0 = Hanafi
    maghrib_offset_minutes=21     # Minutes after sunset
)

prayer_times = IranPrayerTimes(City.QOM, calculator=custom_calculator)
times = prayer_times.calculate()
```

## 📚 API Documentation

### Main Classes

#### `IranPrayerTimes`
Main API for calculating prayer times.

```python
class IranPrayerTimes:
    def __init__(self, city: City, calculator: Optional[PrayerTimeCalculator] = None)
    def calculate(self, date: Optional[datetime] = None) -> PrayerTimes
    
    @classmethod
    def for_city(cls, city: City) -> "IranPrayerTimes"
    
    @staticmethod
    def calculate_for_coordinates(
        latitude: float,
        longitude: float,
        date: Optional[datetime] = None,
        time_zone: str = "Asia/Tehran",
        calculator: Optional[PrayerTimeCalculator] = None,
    ) -> PrayerTimes
```

#### `PrayerTimeCalculator`
Core calculator with astronomical algorithms.

```python
class PrayerTimeCalculator:
    def __init__(
        self,
        fajr_angle: float = 17.7,
        isha_angle: float = 14.0,
        sunrise_sunset_altitude: float = -0.833,
        asr_shadow_factor: float = 1.0,
        maghrib_offset_minutes: int = 21,
    )
    
    def calculate(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        time_zone: str
    ) -> PrayerTimes
```

#### `City` (Enum)
Pre-configured Iranian cities.

```python
class City(Enum):
    TEHRAN = (...)
    TABRIZ = (...)
    MASHHAD = (...)
    # ... and 7 more cities
    
    @property
    def persian_name(self) -> str
    
    @property
    def latitude(self) -> float
    
    @property
    def longitude(self) -> float
    
    @property
    def time_zone(self) -> str
    
    @property
    def display_name(self) -> str
```

#### `PrayerTimes` (Dataclass)
Contains all calculated prayer times.

```python
@dataclass(frozen=True)
class PrayerTimes:
    fajr: datetime
    sunrise: datetime
    dhuhr: datetime
    asr: datetime
    sunset: datetime
    maghrib: datetime
    isha: datetime
    midnight: datetime
    
    def format_all(self, pattern: str = "%H:%M") -> Dict[str, str]
    def __str__(self) -> str
```

## 🔬 Calculation Methodology

### Prayer Time Definitions

- **Fajr**: Sun is 17.7° below horizon (dawn)
- **Sunrise**: Sun crosses horizon with 0.833° correction
- **Dhuhr**: Solar noon (midday)
- **Asr**: Shadow length equals object height + noon shadow (Shafii)
- **Sunset**: Sun crosses horizon
- **Maghrib**: 21 minutes after sunset
- **Isha**: Sun is 14° below horizon (night)
- **Midnight**: Midpoint between sunset and next Fajr

### Algorithms

1. **Julian Day Conversion** - Accurate date handling for astronomy
2. **Solar Position** - Calculates declination and equation of time
3. **Hour Angle** - Determines sun position relative to observer
4. **Time Conversion** - Converts astronomical time to local timezone

### Default Parameters (Iran)

- Fajr angle: **17.7°** (Institute of Geophysics, University of Tehran)
- Isha angle: **14°** (Shia Ithna Ashari)
- Maghrib offset: **21 minutes** after sunset
- Asr method: **Shafii** (shadow factor = 1.0)

## 📁 Project Structure

```
iran-prayer-py/
├── pyproject.toml              # Build configuration
├── README.md                   # This file
├── LICENSE                     # MIT License
└── src/
    └── iran_prayer/
        ├── __init__.py              # Main exports
        ├── py.typed                 # Type checking marker
        ├── iran_prayer_times.py     # Main API
        ├── calculator/
        │   ├── __init__.py
        │   └── prayer_time_calculator.py  # Core calculator
        ├── model/
        │   ├── __init__.py
        │   ├── city.py                     # City enum
        │   └── prayer_times.py             # Data class
        └── examples/
            ├── __init__.py
            └── main.py                     # Usage examples
```

## 🧪 Examples

Run the examples:

```bash
python -m iran_prayer.examples.main
```

See `src/iran_prayer/examples/main.py` for complete examples:

1. **Simple city calculation** - Basic usage with pre-configured cities
2. **Custom coordinates** - Calculate for any location
3. **Static method** - Using factory methods
4. **Multiple cities comparison** - Compare times across cities
5. **Specific date calculation** - Calculate for future dates
6. **Custom calculator** - Using different calculation parameters

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/RevEngine3r/iran-prayer-py.git
cd iran-prayer-py

# Install with development dependencies
pip install -e ".[dev]"
```

### Code Quality Tools

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/

# Run tests (when available)
pytest
```

## 🤝 Contributing

Contributions are welcome! Areas for contribution:

- ✅ Add more Iranian cities
- ✅ Add unit tests
- ✅ Support different calculation methods (e.g., MWL, ISNA)
- ✅ Add Hijri calendar support
- ✅ Optimize astronomical calculations
- ✅ Add Qibla direction calculation
- ✅ Create PyPI package

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow Python coding conventions (PEP 8)
4. Add type hints to new code
5. Add tests for new features
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

MIT License - feel free to use this library in your projects.

## 🙏 Acknowledgments

- Astronomical algorithms based on Jean Meeus's "Astronomical Algorithms"
- Prayer time methodology from Institute of Geophysics, University of Tehran
- Calculation parameters validated against official Iranian prayer time sources
- Translated from [iran-prayer-kt](https://github.com/RevEngine3r/iran-prayer-kt) Kotlin library

## 👨‍💻 Author

**RevEngine3r**
- GitHub: [@RevEngine3r](https://github.com/RevEngine3r)
- Website: [RevEngine3r.iR](https://www.RevEngine3r.iR)
- Location: Tabriz, Iran

## 📦 Related Projects

- [iran-prayer-kt](https://github.com/RevEngine3r/iran-prayer-kt) - Kotlin version of this library

## 📣 Support

If you find this library helpful, please give it a ⭐ on GitHub!

For issues, questions, or suggestions, please [open an issue](https://github.com/RevEngine3r/iran-prayer-py/issues).

---

*Made with ❤️ for the Muslim community in Iran*
