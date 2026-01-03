"""Unit tests for PrayerTimeCalculator."""

import math
from datetime import datetime

import pytest
from zoneinfo import ZoneInfo

from iran_prayer.calculator.prayer_time_calculator import PrayerTimeCalculator


class TestPrayerTimeCalculator:
    """Test suite for prayer time calculator."""

    def test_default_parameters(self) -> None:
        """Test calculator initializes with correct default parameters."""
        calc = PrayerTimeCalculator()
        assert calc.fajr_angle == 17.7
        assert calc.isha_angle == 14.0
        assert calc.sunrise_sunset_altitude == -0.833
        assert calc.asr_shadow_factor == 1.0
        assert calc.maghrib_offset_minutes == 21

    def test_custom_parameters(self) -> None:
        """Test calculator accepts custom parameters."""
        calc = PrayerTimeCalculator(
            fajr_angle=18.0,
            isha_angle=15.0,
            sunrise_sunset_altitude=-0.5,
            asr_shadow_factor=2.0,
            maghrib_offset_minutes=20,
        )
        assert calc.fajr_angle == 18.0
        assert calc.isha_angle == 15.0
        assert calc.sunrise_sunset_altitude == -0.5
        assert calc.asr_shadow_factor == 2.0
        assert calc.maghrib_offset_minutes == 20

    def test_julian_day_calculation(self) -> None:
        """Test Julian day calculation for known dates."""
        calc = PrayerTimeCalculator()
        
        # J2000.0 epoch: January 1, 2000, 12:00 TT
        date = datetime(2000, 1, 1)
        jd = calc._calculate_julian_day(date)
        assert abs(jd - 2451544.5) < 0.1  # Allow small difference
        
        # Another known date
        date = datetime(2026, 1, 2)
        jd = calc._calculate_julian_day(date)
        assert jd > 2451544.5  # Should be after J2000

    def test_solar_parameters(self) -> None:
        """Test solar parameter calculations return valid values."""
        calc = PrayerTimeCalculator()
        jd = calc._calculate_julian_day(datetime(2026, 1, 2))
        declination, eq_time = calc._calculate_solar_parameters(jd)
        
        # Declination should be between -23.5 and +23.5 degrees
        assert -math.radians(23.5) <= declination <= math.radians(23.5)
        
        # Equation of time should be reasonable (within -20 to +20 minutes)
        assert -20 <= eq_time <= 20

    def test_hour_angle_calculation(self) -> None:
        """Test hour angle calculation."""
        calc = PrayerTimeCalculator()
        
        # Test with reasonable values
        altitude = -17.7  # Fajr angle
        latitude = math.radians(35.6892)  # Tehran
        declination = math.radians(0)  # Equinox
        
        hour_angle = calc._calculate_hour_angle(altitude, latitude, declination)
        
        # Hour angle should be a valid radian value
        assert 0 <= hour_angle <= math.pi

    def test_calculate_returns_prayer_times(self) -> None:
        """Test calculate method returns PrayerTimes object."""
        calc = PrayerTimeCalculator()
        date = datetime(2026, 1, 2)
        
        times = calc.calculate(
            date=date,
            latitude=35.6892,
            longitude=51.3890,
            time_zone="Asia/Tehran"
        )
        
        # Check all times are present and are datetime objects
        assert isinstance(times.fajr, datetime)
        assert isinstance(times.sunrise, datetime)
        assert isinstance(times.dhuhr, datetime)
        assert isinstance(times.asr, datetime)
        assert isinstance(times.sunset, datetime)
        assert isinstance(times.maghrib, datetime)
        assert isinstance(times.isha, datetime)
        assert isinstance(times.midnight, datetime)

    def test_prayer_times_logical_order(self) -> None:
        """Test that prayer times are in logical chronological order."""
        calc = PrayerTimeCalculator()
        date = datetime(2026, 1, 2)
        
        times = calc.calculate(
            date=date,
            latitude=35.6892,
            longitude=51.3890,
            time_zone="Asia/Tehran"
        )
        
        # Verify chronological order
        assert times.fajr < times.sunrise
        assert times.sunrise < times.dhuhr
        assert times.dhuhr < times.asr
        assert times.asr < times.sunset
        assert times.sunset < times.maghrib
        assert times.maghrib < times.isha

    def test_maghrib_offset(self) -> None:
        """Test that Maghrib is sunset + offset."""
        calc = PrayerTimeCalculator(maghrib_offset_minutes=21)
        date = datetime(2026, 1, 2)
        
        times = calc.calculate(
            date=date,
            latitude=35.6892,
            longitude=51.3890,
            time_zone="Asia/Tehran"
        )
        
        # Maghrib should be 21 minutes after sunset
        diff = (times.maghrib - times.sunset).total_seconds() / 60
        assert abs(diff - 21) < 0.1  # Within 6 seconds

    def test_timezone_awareness(self) -> None:
        """Test that all returned times are timezone-aware."""
        calc = PrayerTimeCalculator()
        date = datetime(2026, 1, 2)
        
        times = calc.calculate(
            date=date,
            latitude=35.6892,
            longitude=51.3890,
            time_zone="Asia/Tehran"
        )
        
        # All times should have timezone info
        assert times.fajr.tzinfo is not None
        assert times.sunrise.tzinfo is not None
        assert times.dhuhr.tzinfo is not None
        assert times.asr.tzinfo is not None
        assert times.sunset.tzinfo is not None
        assert times.maghrib.tzinfo is not None
        assert times.isha.tzinfo is not None
        assert times.midnight.tzinfo is not None
