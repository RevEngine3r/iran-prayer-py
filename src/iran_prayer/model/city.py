"""City enumeration with geographic data for major Iranian cities."""

from enum import Enum


class City(Enum):
    """Enumeration of major Iranian cities with their geographic coordinates.

    Each city contains:
        - Persian name (persianName)
        - Geographic latitude in degrees
        - Geographic longitude in degrees
        - IANA timezone identifier
    """

    TEHRAN = ("تهران", 35.6892, 51.3890, "Asia/Tehran")
    TABRIZ = ("تبریز", 38.0800, 46.2919, "Asia/Tehran")
    MASHHAD = ("مشهد", 36.3264, 59.5433, "Asia/Tehran")
    ISFAHAN = ("اصفهان", 32.6525, 51.6746, "Asia/Tehran")
    SHIRAZ = ("شیراز", 29.5918, 52.5837, "Asia/Tehran")
    QOM = ("قم", 34.6401, 50.8764, "Asia/Tehran")
    AHVAZ = ("اهواز", 31.3203, 48.6692, "Asia/Tehran")
    KERMANSHAH = ("کرمانشاه", 34.3142, 47.0650, "Asia/Tehran")
    RASHT = ("رشت", 37.2808, 49.5831, "Asia/Tehran")
    YAZD = ("یزد", 31.8974, 54.3569, "Asia/Tehran")

    def __init__(
        self, persian_name: str, latitude: float, longitude: float, time_zone: str
    ) -> None:
        """Initialize city with geographic data.

        Args:
            persian_name: Persian name of the city
            latitude: Geographic latitude in degrees
            longitude: Geographic longitude in degrees
            time_zone: IANA timezone identifier
        """
        self.persian_name = persian_name
        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone

    @property
    def display_name(self) -> str:
        """English display name (capitalized enum name).

        Returns:
            Capitalized English name of the city
        """
        return self.name.capitalize()

    def __str__(self) -> str:
        """String representation of the city.

        Returns:
            Display name of the city
        """
        return self.display_name
