# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-02

### Added
- Complete Python translation of iran-prayer-kt library
- Modern Python package with src layout
- Full type hints support (mypy strict compatible)
- Support for 10 major Iranian cities
- Astronomical algorithms for accurate prayer time calculations
- Configurable calculation parameters (Fajr/Isha angles, Asr methods)
- Custom coordinates support
- Multiple API patterns (instance, factory, static methods)
- Comprehensive documentation and examples
- Complete test suite with >80% coverage
- CI/CD with GitHub Actions

### Features
- `IranPrayerTimes` - Main API class
- `PrayerTimeCalculator` - Core calculation engine
- `City` enum - Pre-configured Iranian cities
- `PrayerTimes` dataclass - Prayer time results
- Julian day calculations
- Solar position algorithms
- Hour angle calculations
- Timezone-aware datetime handling

### Supported Cities
- Tehran (تهران)
- Tabriz (تبریز)
- Mashhad (مشهد)
- Isfahan (اصفهان)
- Shiraz (شیراز)
- Qom (قم)
- Ahvaz (اهواز)
- Kermanshah (کرمانشاه)
- Rasht (رشت)
- Yazd (یزد)

[1.0.0]: https://github.com/RevEngine3r/iran-prayer-py/releases/tag/v1.0.0
