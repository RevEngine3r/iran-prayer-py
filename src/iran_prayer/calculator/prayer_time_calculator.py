"""Calculator for Islamic prayer times using astronomical algorithms."""

import math
from datetime import datetime, timedelta, timezone
from typing import Tuple
from zoneinfo import ZoneInfo

from iran_prayer.model.prayer_times import PrayerTimes


class PrayerTimeCalculator:
    """Calculator for Islamic prayer times using astronomical algorithms.

    This implementation uses:
    - Julian day calculations for accurate date handling
    - Solar position algorithms (declination, equation of time)
    - Hour angle calculations for different prayer times

    Attributes:
        fajr_angle: Sun angle below horizon for Fajr in degrees (default: 17.7)
        isha_angle: Sun angle below horizon for Isha in degrees (default: 14.0)
        sunrise_sunset_altitude: Geometric altitude for sunrise/sunset (default: -0.833)
        asr_shadow_factor: Shadow length ratio for Asr (1.0=Shafii, 2.0=Hanafi)
        maghrib_offset_minutes: Minutes to add after sunset for Maghrib (default: 21)
    """

    def __init__(
        self,
        fajr_angle: float = 17.7,
        isha_angle: float = 14.0,
        sunrise_sunset_altitude: float = -0.833,
        asr_shadow_factor: float = 1.0,
        maghrib_offset_minutes: int = 21,
    ) -> None:
        """Initialize prayer time calculator with configurable parameters.

        Args:
            fajr_angle: Sun angle below horizon for Fajr (degrees)
            isha_angle: Sun angle below horizon for Isha (degrees)
            sunrise_sunset_altitude: Geometric altitude for sunrise/sunset calculations
            asr_shadow_factor: Shadow length ratio (1.0 for Shafii, 2.0 for Hanafi)
            maghrib_offset_minutes: Minutes to add after sunset for Maghrib
        """
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle
        self.sunrise_sunset_altitude = sunrise_sunset_altitude
        self.asr_shadow_factor = asr_shadow_factor
        self.maghrib_offset_minutes = maghrib_offset_minutes

    def calculate(
        self, date: datetime, latitude: float, longitude: float, time_zone: str
    ) -> PrayerTimes:
        """Compute prayer times for a specific date and location.

        Args:
            date: Date for which to calculate prayer times
            latitude: Geographic latitude in degrees (positive for North)
            longitude: Geographic longitude in degrees (positive for East)
            time_zone: IANA timezone identifier (e.g., "Asia/Tehran")

        Returns:
            PrayerTimes object containing all calculated prayer times

        Example:
            >>> calc = PrayerTimeCalculator()
            >>> times = calc.calculate(
            ...     datetime(2026, 1, 2),
            ...     35.6892,  # Tehran latitude
            ...     51.3890,  # Tehran longitude
            ...     "Asia/Tehran"
            ... )
        """
        zone_info = ZoneInfo(time_zone)
        midnight_base = datetime(date.year, date.month, date.day, tzinfo=zone_info)
        tz_offset_minutes = int(midnight_base.utcoffset().total_seconds() / 60)  # type: ignore

        julian_day = self._calculate_julian_day(date)
        declination, equation_of_time = self._calculate_solar_parameters(julian_day)
        latitude_rad = math.radians(latitude)
        solar_noon = 720.0 - 4.0 * longitude - equation_of_time

        # Sunrise and Sunset
        sun_hour_angle = self._calculate_hour_angle(
            self.sunrise_sunset_altitude, latitude_rad, declination
        )
        sunrise = self._convert_to_local_time(
            date, solar_noon - 4.0 * math.degrees(sun_hour_angle), tz_offset_minutes, zone_info
        )
        sunset = self._convert_to_local_time(
            date, solar_noon + 4.0 * math.degrees(sun_hour_angle), tz_offset_minutes, zone_info
        )

        # Fajr and Isha
        fajr_hour_angle = self._calculate_hour_angle(-self.fajr_angle, latitude_rad, declination)
        isha_hour_angle = self._calculate_hour_angle(-self.isha_angle, latitude_rad, declination)
        fajr = self._convert_to_local_time(
            date, solar_noon - 4.0 * math.degrees(fajr_hour_angle), tz_offset_minutes, zone_info
        )
        isha = self._convert_to_local_time(
            date, solar_noon + 4.0 * math.degrees(isha_hour_angle), tz_offset_minutes, zone_info
        )

        # Dhuhr (solar noon)
        dhuhr = self._convert_to_local_time(date, solar_noon, tz_offset_minutes, zone_info)

        # Asr
        asr_hour_angle = self._calculate_asr_hour_angle(
            self.asr_shadow_factor, latitude_rad, declination
        )
        asr = self._convert_to_local_time(
            date, solar_noon + 4.0 * math.degrees(asr_hour_angle), tz_offset_minutes, zone_info
        )

        # Maghrib (sunset + offset)
        maghrib = sunset + timedelta(minutes=self.maghrib_offset_minutes)

        # Midnight (midpoint between sunset and next Fajr)
        next_date = date + timedelta(days=1)
        next_julian_day = self._calculate_julian_day(next_date)
        next_declination, next_eq_time = self._calculate_solar_parameters(next_julian_day)
        next_solar_noon = 720.0 - 4.0 * longitude - next_eq_time
        next_fajr_hour_angle = self._calculate_hour_angle(
            -self.fajr_angle, latitude_rad, next_declination
        )
        next_fajr = self._convert_to_local_time(
            next_date,
            next_solar_noon - 4.0 * math.degrees(next_fajr_hour_angle),
            tz_offset_minutes,
            zone_info,
        )
        midnight = sunset + (next_fajr - sunset) / 2

        return PrayerTimes(
            fajr=fajr,
            sunrise=sunrise,
            dhuhr=dhuhr,
            asr=asr,
            sunset=sunset,
            maghrib=maghrib,
            isha=isha,
            midnight=midnight,
        )

    def _calculate_solar_parameters(self, julian_day: float) -> Tuple[float, float]:
        """Calculate solar parameters (declination and equation of time).

        Args:
            julian_day: Julian day number

        Returns:
            Tuple of (declination in radians, equation of time in minutes)
        """
        days_since_epoch = julian_day - 2451545.0
        mean_anomaly = math.radians(357.529 + 0.98560028 * days_since_epoch)
        mean_longitude = 280.459 + 0.98564736 * days_since_epoch
        ecliptic_longitude = math.radians(
            (mean_longitude + 1.915 * math.sin(mean_anomaly) + 0.020 * math.sin(2 * mean_anomaly))
            % 360
        )
        obliquity = math.radians(23.439 - 0.00000036 * days_since_epoch)

        right_ascension = math.atan2(
            math.cos(obliquity) * math.sin(ecliptic_longitude), math.cos(ecliptic_longitude)
        )
        declination = math.asin(math.sin(obliquity) * math.sin(ecliptic_longitude))

        # Normalize right ascension to 0-360 range
        right_ascension_degrees = math.degrees(right_ascension)
        if right_ascension_degrees < 0:
            right_ascension_degrees += 360

        # Normalize mean longitude
        normalized_mean_longitude = ((mean_longitude % 360) + 360) % 360

        # Calculate equation of time with proper angle wrapping
        eq_time_delta = normalized_mean_longitude - right_ascension_degrees
        if eq_time_delta > 180:
            eq_time_delta -= 360
        if eq_time_delta < -180:
            eq_time_delta += 360
        equation_of_time = 4.0 * eq_time_delta

        return declination, equation_of_time

    def _calculate_hour_angle(
        self, altitude_degrees: float, latitude: float, declination: float
    ) -> float:
        """Calculate hour angle for a given altitude, latitude, and solar declination.

        Args:
            altitude_degrees: Altitude angle in degrees
            latitude: Latitude in radians
            declination: Solar declination in radians

        Returns:
            Hour angle in radians
        """
        altitude = math.radians(altitude_degrees)
        cos_hour_angle = (math.sin(altitude) - math.sin(latitude) * math.sin(declination)) / (
            math.cos(latitude) * math.cos(declination)
        )
        return math.acos(max(-1.0, min(1.0, cos_hour_angle)))

    def _calculate_asr_hour_angle(
        self, shadow_factor: float, latitude: float, declination: float
    ) -> float:
        """Calculate hour angle for Asr prayer based on shadow length ratio.

        Args:
            shadow_factor: Shadow length ratio (1.0 for Shafii, 2.0 for Hanafi)
            latitude: Latitude in radians
            declination: Solar declination in radians

        Returns:
            Hour angle in radians
        """
        tan_altitude = 1.0 / (shadow_factor + math.tan(abs(latitude - declination)))
        altitude = math.atan(tan_altitude)
        cos_hour_angle = (math.sin(altitude) - math.sin(latitude) * math.sin(declination)) / (
            math.cos(latitude) * math.cos(declination)
        )
        return math.acos(max(-1.0, min(1.0, cos_hour_angle)))

    def _convert_to_local_time(
        self, date: datetime, utc_minutes: float, timezone_offset_minutes: int, zone_info: ZoneInfo
    ) -> datetime:
        """Convert UTC minutes to local time for a specific date and timezone.

        Uses proper rounding (round half up) to avoid systematic bias.

        Args:
            date: Date for the time calculation
            utc_minutes: UTC time in minutes since midnight
            timezone_offset_minutes: Timezone offset in minutes
            zone_info: ZoneInfo object for timezone

        Returns:
            Timezone-aware datetime object
        """
        total_minutes = utc_minutes + timezone_offset_minutes

        # Use proper rounding: add 0.5 before converting to int (round half up)
        total_seconds = int((total_minutes * 60.0) + 0.5)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return datetime(date.year, date.month, date.day, tzinfo=zone_info) + timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        )

    def _calculate_julian_day(self, date: datetime) -> float:
        """Calculate Julian day number for a given Gregorian date.

        Args:
            date: Gregorian date

        Returns:
            Julian day number
        """
        year = date.year
        month = date.month
        day = date.day

        if month <= 2:
            year -= 1
            month += 12

        a = year // 100
        b = 2 - a + a // 4

        return (
            int(365.25 * (year + 4716))
            + int(30.6001 * (month + 1))
            + day
            + b
            - 1524.5
        )
