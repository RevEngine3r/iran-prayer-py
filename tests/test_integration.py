"""Integration tests for complete workflows."""

from datetime import datetime

import pytest

from iran_prayer import City, IranPrayerTimes, PrayerTimeCalculator


class TestIntegration:
    """Integration tests for end-to-end functionality."""

    def test_simple_city_calculation(self) -> None:
        """Test simple city-based calculation workflow."""
        prayer_times = IranPrayerTimes(City.TEHRAN)
        times = prayer_times.calculate()
        
        # Should return valid prayer times
        assert times.fajr < times.sunrise
        assert times.sunrise < times.dhuhr
        assert times.dhuhr < times.asr
        assert times.asr < times.sunset

    def test_factory_method(self) -> None:
        """Test factory method workflow."""
        prayer_times = IranPrayerTimes.for_city(City.MASHHAD)
        times = prayer_times.calculate()
        
        assert times is not None
        assert times.fajr is not None

    def test_static_method_coordinates(self) -> None:
        """Test static method for custom coordinates."""
        times = IranPrayerTimes.calculate_for_coordinates(
            latitude=35.6892,
            longitude=51.3890,
            time_zone="Asia/Tehran"
        )
        
        assert times is not None
        assert times.fajr < times.sunrise

    def test_specific_date_calculation(self) -> None:
        """Test calculation for specific date."""
        prayer_times = IranPrayerTimes(City.SHIRAZ)
        specific_date = datetime(2026, 6, 15)  # Summer date
        times = prayer_times.calculate(specific_date)
        
        assert times.fajr.year == 2026
        assert times.fajr.month == 6
        assert times.fajr.day == 15

    def test_custom_calculator(self) -> None:
        """Test using custom calculator parameters."""
        custom_calc = PrayerTimeCalculator(
            fajr_angle=18.0,
            isha_angle=15.0,
            maghrib_offset_minutes=20
        )
        
        prayer_times = IranPrayerTimes(City.QOM, calculator=custom_calc)
        times = prayer_times.calculate()
        
        # Maghrib should be 20 minutes after sunset (custom offset)
        diff = (times.maghrib - times.sunset).total_seconds() / 60
        assert abs(diff - 20) < 0.1

    def test_multiple_cities(self) -> None:
        """Test calculating for multiple cities."""
        cities = [City.TEHRAN, City.TABRIZ, City.MASHHAD]
        all_times = []
        
        for city in cities:
            times = IranPrayerTimes.for_city(city).calculate()
            all_times.append(times)
        
        assert len(all_times) == 3
        # Each city should have different times due to different coordinates
        assert all_times[0].fajr != all_times[1].fajr

    def test_format_all_integration(self) -> None:
        """Test formatting in complete workflow."""
        prayer_times = IranPrayerTimes(City.ISFAHAN)
        times = prayer_times.calculate()
        
        formatted = times.format_all("%H:%M")
        
        assert len(formatted) == 8
        assert "Fajr" in formatted
        assert "Midnight" in formatted
        # Each time should be in HH:MM format
        for time_str in formatted.values():
            assert len(time_str) == 5
            assert ":" in time_str

    def test_winter_summer_difference(self) -> None:
        """Test that prayer times differ between winter and summer."""
        prayer_times = IranPrayerTimes(City.TEHRAN)
        
        winter = prayer_times.calculate(datetime(2026, 1, 15))
        summer = prayer_times.calculate(datetime(2026, 7, 15))
        
        # Summer Fajr should be earlier than winter Fajr
        assert summer.fajr.hour < winter.fajr.hour or (
            summer.fajr.hour == winter.fajr.hour and summer.fajr.minute < winter.fajr.minute
        )

    def test_all_cities_calculate(self) -> None:
        """Test that all cities can calculate prayer times."""
        for city in City:
            prayer_times = IranPrayerTimes(city)
            times = prayer_times.calculate()
            
            # Basic validation
            assert times.fajr < times.sunrise
            assert times.sunrise < times.dhuhr
            assert times.dhuhr < times.asr
