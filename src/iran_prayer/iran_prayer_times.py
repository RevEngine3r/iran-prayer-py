"""Main API for calculating prayer times for Iranian cities."""

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from iran_prayer.calculator.prayer_time_calculator import PrayerTimeCalculator
from iran_prayer.model.city import City
from iran_prayer.model.prayer_times import PrayerTimes


class IranPrayerTimes:
    """Main API for calculating prayer times for Iranian cities.

    This class provides a convenient interface for calculating Islamic prayer times
    for pre-configured Iranian cities.

    Attributes:
        city: The Iranian city for which to calculate prayer times
        calculator: Calculator instance for prayer time calculations

    Example:
        >>> from iran_prayer import IranPrayerTimes, City
        >>> prayer_times = IranPrayerTimes(City.TEHRAN)
        >>> times = prayer_times.calculate()
        >>> print(times)
    """

    def __init__(
        self, city: City, calculator: Optional[PrayerTimeCalculator] = None
    ) -> None:
        """Initialize prayer times calculator for a specific city.

        Args:
            city: The Iranian city for which to calculate prayer times
            calculator: Custom calculator instance (optional, uses defaults if not provided)
        """
        self.city = city
        self.calculator = calculator if calculator is not None else PrayerTimeCalculator()

    def calculate(self, date: Optional[datetime] = None) -> PrayerTimes:
        """Calculate prayer times for the specified city.

        Args:
            date: Date for which to calculate prayer times.
                  Defaults to today in the city's timezone.

        Returns:
            PrayerTimes object containing all prayer times for the specified date

        Example:
            >>> from datetime import datetime
            >>> prayer_times = IranPrayerTimes(City.MASHHAD)
            >>> # Calculate for today
            >>> times_today = prayer_times.calculate()
            >>> # Calculate for specific date
            >>> times_ramadan = prayer_times.calculate(datetime(2026, 2, 28))
        """
        zone_info = ZoneInfo(self.city.time_zone)
        effective_date = date if date is not None else datetime.now(zone_info)

        return self.calculator.calculate(
            date=effective_date,
            latitude=self.city.latitude,
            longitude=self.city.longitude,
            time_zone=self.city.time_zone,
        )

    @classmethod
    def for_city(cls, city: City) -> "IranPrayerTimes":
        """Create an instance for a specific city.

        This is a factory method that provides a cleaner alternative to
        direct instantiation.

        Args:
            city: The city for which to calculate prayer times

        Returns:
            IranPrayerTimes instance configured for the specified city

        Example:
            >>> prayer_times = IranPrayerTimes.for_city(City.SHIRAZ)
            >>> times = prayer_times.calculate()
        """
        return cls(city)

    @staticmethod
    def calculate_for_coordinates(
        latitude: float,
        longitude: float,
        date: Optional[datetime] = None,
        time_zone: str = "Asia/Tehran",
        calculator: Optional[PrayerTimeCalculator] = None,
    ) -> PrayerTimes:
        """Calculate prayer times for custom coordinates.

        This static method allows calculating prayer times for any location,
        not just pre-configured cities.

        Args:
            latitude: Geographic latitude in degrees (positive for North)
            longitude: Geographic longitude in degrees (positive for East)
            date: Date for calculation (defaults to today)
            time_zone: IANA timezone identifier (defaults to "Asia/Tehran")
            calculator: Custom calculator instance (optional, uses defaults if not provided)

        Returns:
            PrayerTimes object for the specified coordinates and date

        Example:
            >>> # Calculate for custom location
            >>> times = IranPrayerTimes.calculate_for_coordinates(
            ...     latitude=36.3264,   # Mashhad
            ...     longitude=59.5433,
            ...     date=datetime(2026, 1, 2),
            ...     time_zone="Asia/Tehran"
            ... )
        """
        calc = calculator if calculator is not None else PrayerTimeCalculator()
        effective_date = date if date is not None else datetime.now(ZoneInfo(time_zone))

        return calc.calculate(
            date=effective_date,
            latitude=latitude,
            longitude=longitude,
            time_zone=time_zone,
        )
