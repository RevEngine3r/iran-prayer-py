"""Unit tests for model classes."""

from datetime import datetime

import pytest
from zoneinfo import ZoneInfo

from iran_prayer.model.city import City
from iran_prayer.model.prayer_times import PrayerTimes


class TestCity:
    """Test suite for City enum."""

    def test_all_cities_exist(self) -> None:
        """Test all 10 cities are defined."""
        cities = list(City)
        assert len(cities) == 10

    def test_tehran_coordinates(self) -> None:
        """Test Tehran has correct coordinates."""
        assert City.TEHRAN.latitude == 35.6892
        assert City.TEHRAN.longitude == 51.3890
        assert City.TEHRAN.time_zone == "Asia/Tehran"

    def test_persian_names(self) -> None:
        """Test Persian names are set correctly."""
        assert City.TEHRAN.persian_name == "تهران"
        assert City.TABRIZ.persian_name == "تبریز"
        assert City.MASHHAD.persian_name == "مشهد"

    def test_display_name(self) -> None:
        """Test display_name property returns capitalized name."""
        assert City.TEHRAN.display_name == "Tehran"
        assert City.TABRIZ.display_name == "Tabriz"
        assert City.MASHHAD.display_name == "Mashhad"

    def test_str_representation(self) -> None:
        """Test string representation."""
        assert str(City.TEHRAN) == "Tehran"
        assert str(City.MASHHAD) == "Mashhad"

    def test_all_cities_have_required_attributes(self) -> None:
        """Test all cities have all required attributes."""
        for city in City:
            assert hasattr(city, "persian_name")
            assert hasattr(city, "latitude")
            assert hasattr(city, "longitude")
            assert hasattr(city, "time_zone")
            assert city.time_zone == "Asia/Tehran"


class TestPrayerTimes:
    """Test suite for PrayerTimes dataclass."""

    def test_creation(self) -> None:
        """Test PrayerTimes can be created."""
        tz = ZoneInfo("Asia/Tehran")
        times = PrayerTimes(
            fajr=datetime(2026, 1, 2, 5, 41, tzinfo=tz),
            sunrise=datetime(2026, 1, 2, 7, 11, tzinfo=tz),
            dhuhr=datetime(2026, 1, 2, 12, 13, tzinfo=tz),
            asr=datetime(2026, 1, 2, 14, 54, tzinfo=tz),
            sunset=datetime(2026, 1, 2, 17, 14, tzinfo=tz),
            maghrib=datetime(2026, 1, 2, 17, 35, tzinfo=tz),
            isha=datetime(2026, 1, 2, 18, 36, tzinfo=tz),
            midnight=datetime(2026, 1, 2, 23, 28, tzinfo=tz),
        )
        
        assert times.fajr.hour == 5
        assert times.dhuhr.hour == 12

    def test_immutability(self) -> None:
        """Test PrayerTimes is immutable (frozen dataclass)."""
        tz = ZoneInfo("Asia/Tehran")
        times = PrayerTimes(
            fajr=datetime(2026, 1, 2, 5, 41, tzinfo=tz),
            sunrise=datetime(2026, 1, 2, 7, 11, tzinfo=tz),
            dhuhr=datetime(2026, 1, 2, 12, 13, tzinfo=tz),
            asr=datetime(2026, 1, 2, 14, 54, tzinfo=tz),
            sunset=datetime(2026, 1, 2, 17, 14, tzinfo=tz),
            maghrib=datetime(2026, 1, 2, 17, 35, tzinfo=tz),
            isha=datetime(2026, 1, 2, 18, 36, tzinfo=tz),
            midnight=datetime(2026, 1, 2, 23, 28, tzinfo=tz),
        )
        
        with pytest.raises(Exception):  # Should raise FrozenInstanceError
            times.fajr = datetime(2026, 1, 2, 6, 0, tzinfo=tz)  # type: ignore

    def test_format_all_default(self) -> None:
        """Test format_all with default pattern."""
        tz = ZoneInfo("Asia/Tehran")
        times = PrayerTimes(
            fajr=datetime(2026, 1, 2, 5, 41, tzinfo=tz),
            sunrise=datetime(2026, 1, 2, 7, 11, tzinfo=tz),
            dhuhr=datetime(2026, 1, 2, 12, 13, tzinfo=tz),
            asr=datetime(2026, 1, 2, 14, 54, tzinfo=tz),
            sunset=datetime(2026, 1, 2, 17, 14, tzinfo=tz),
            maghrib=datetime(2026, 1, 2, 17, 35, tzinfo=tz),
            isha=datetime(2026, 1, 2, 18, 36, tzinfo=tz),
            midnight=datetime(2026, 1, 2, 23, 28, tzinfo=tz),
        )
        
        formatted = times.format_all()
        assert formatted["Fajr"] == "05:41"
        assert formatted["Dhuhr"] == "12:13"
        assert formatted["Midnight"] == "23:28"

    def test_format_all_custom_pattern(self) -> None:
        """Test format_all with custom pattern."""
        tz = ZoneInfo("Asia/Tehran")
        times = PrayerTimes(
            fajr=datetime(2026, 1, 2, 5, 41, 30, tzinfo=tz),
            sunrise=datetime(2026, 1, 2, 7, 11, 45, tzinfo=tz),
            dhuhr=datetime(2026, 1, 2, 12, 13, 15, tzinfo=tz),
            asr=datetime(2026, 1, 2, 14, 54, 0, tzinfo=tz),
            sunset=datetime(2026, 1, 2, 17, 14, 0, tzinfo=tz),
            maghrib=datetime(2026, 1, 2, 17, 35, 0, tzinfo=tz),
            isha=datetime(2026, 1, 2, 18, 36, 0, tzinfo=tz),
            midnight=datetime(2026, 1, 2, 23, 28, 0, tzinfo=tz),
        )
        
        formatted = times.format_all("%H:%M:%S")
        assert formatted["Fajr"] == "05:41:30"
        assert formatted["Sunrise"] == "07:11:45"

    def test_str_representation(self) -> None:
        """Test string representation."""
        tz = ZoneInfo("Asia/Tehran")
        times = PrayerTimes(
            fajr=datetime(2026, 1, 2, 5, 41, tzinfo=tz),
            sunrise=datetime(2026, 1, 2, 7, 11, tzinfo=tz),
            dhuhr=datetime(2026, 1, 2, 12, 13, tzinfo=tz),
            asr=datetime(2026, 1, 2, 14, 54, tzinfo=tz),
            sunset=datetime(2026, 1, 2, 17, 14, tzinfo=tz),
            maghrib=datetime(2026, 1, 2, 17, 35, tzinfo=tz),
            isha=datetime(2026, 1, 2, 18, 36, tzinfo=tz),
            midnight=datetime(2026, 1, 2, 23, 28, tzinfo=tz),
        )
        
        result = str(times)
        assert "Prayer Times:" in result
        assert "Fajr:" in result
        assert "05:41" in result
        assert "Midnight:" in result
