"""Iran Prayer Times - Islamic prayer times calculator for Iranian cities.

This package provides accurate Islamic prayer time calculations for major cities
in Iran using astronomical algorithms.
"""

__version__ = "1.0.0"
__author__ = "RevEngine3r"

from iran_prayer.iran_prayer_times import IranPrayerTimes
from iran_prayer.model.city import City
from iran_prayer.model.prayer_times import PrayerTimes
from iran_prayer.calculator.prayer_time_calculator import PrayerTimeCalculator

__all__ = [
    "IranPrayerTimes",
    "City",
    "PrayerTimes",
    "PrayerTimeCalculator",
]
