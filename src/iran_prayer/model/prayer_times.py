"""Prayer times data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class PrayerTimes:
    """Data class representing Islamic prayer times for a specific date.

    Attributes:
        fajr: Dawn prayer time (before sunrise)
        sunrise: Sunrise time
        dhuhr: Noon prayer time
        asr: Afternoon prayer time
        sunset: Sunset time
        maghrib: Evening prayer time (after sunset)
        isha: Night prayer time
        midnight: Islamic midnight (midpoint between sunset and next Fajr)
    """

    fajr: datetime
    sunrise: datetime
    dhuhr: datetime
    asr: datetime
    sunset: datetime
    maghrib: datetime
    isha: datetime
    midnight: datetime

    def format_all(self, pattern: str = "%H:%M") -> Dict[str, str]:
        """Format all prayer times using the specified pattern.

        Args:
            pattern: strftime pattern (e.g., "%H:%M", "%H:%M:%S")
                Default is "%H:%M" for 24-hour format without seconds.

        Returns:
            Dictionary mapping prayer names to formatted time strings

        Example:
            >>> times.format_all("%H:%M:%S")
            {'Fajr': '04:30:00', 'Sunrise': '06:15:00', ...}
        """
        return {
            "Fajr": self.fajr.strftime(pattern),
            "Sunrise": self.sunrise.strftime(pattern),
            "Dhuhr": self.dhuhr.strftime(pattern),
            "Asr": self.asr.strftime(pattern),
            "Sunset": self.sunset.strftime(pattern),
            "Maghrib": self.maghrib.strftime(pattern),
            "Isha": self.isha.strftime(pattern),
            "Midnight": self.midnight.strftime(pattern),
        }

    def __str__(self) -> str:
        """Pretty-printed representation of prayer times.

        Returns:
            Formatted string with all prayer times in HH:MM format
        """
        formatted = self.format_all("%H:%M")
        return (
            "Prayer Times:\n"
            f"Fajr:     {formatted['Fajr']}\n"
            f"Sunrise:  {formatted['Sunrise']}\n"
            f"Dhuhr:    {formatted['Dhuhr']}\n"
            f"Asr:      {formatted['Asr']}\n"
            f"Sunset:   {formatted['Sunset']}\n"
            f"Maghrib:  {formatted['Maghrib']}\n"
            f"Isha:     {formatted['Isha']}\n"
            f"Midnight: {formatted['Midnight']}"
        )
