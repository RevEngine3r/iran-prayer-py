from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo
from enum import Enum

from iran_prayer_calculator import IranPrayerCalculator


# --- City Enum ---
class IranCity(Enum):
    TEHRAN = "Tehran"
    TABRIZ = "Tabriz"
    MASHHAD = "Mashhad"
    ISFAHAN = "Isfahan"
    SHIRAZ = "Shiraz"
    QOM = "Qom"
    AHVAZ = "Ahvaz"
    KERMANSHAH = "Kermanshah"
    RASHT = "Rasht"
    YAZD = "Yazd"


# --- Coordinates dictionary ---
CITY_COORDS: dict[IranCity, dict[str, float | str]] = {
    IranCity.TEHRAN: {"lat": 35.6892, "lon": 51.3890, "tz": "Asia/Tehran"},
    IranCity.TABRIZ: {"lat": 38.0800, "lon": 46.2919, "tz": "Asia/Tehran"},
    IranCity.MASHHAD: {"lat": 36.3264, "lon": 59.5433, "tz": "Asia/Tehran"},
    IranCity.ISFAHAN: {"lat": 32.6525, "lon": 51.6746, "tz": "Asia/Tehran"},
    IranCity.SHIRAZ: {"lat": 29.5918, "lon": 52.5837, "tz": "Asia/Tehran"},
    IranCity.QOM: {"lat": 34.6401, "lon": 50.8764, "tz": "Asia/Tehran"},
    IranCity.AHVAZ: {"lat": 31.3203, "lon": 48.6692, "tz": "Asia/Tehran"},
    IranCity.KERMANSHAH: {"lat": 34.3142, "lon": 47.0650, "tz": "Asia/Tehran"},
    IranCity.RASHT: {"lat": 37.2808, "lon": 49.5831, "tz": "Asia/Tehran"},
    IranCity.YAZD: {"lat": 31.8974, "lon": 54.3569, "tz": "Asia/Tehran"},
}


@dataclass
class IranPrayerTimes:
    city: IranCity

    def compute(self, d: date | None = None):
        coords = CITY_COORDS[self.city]
        tz = ZoneInfo(coords["tz"])
        if d is None:
            d = datetime.now(tz).date()

        # Use match/case for clarity if you want to branch by city later
        match self.city:
            case IranCity.TEHRAN:
                pass  # could add Tehran-specific tweaks
            case IranCity.TABRIZ:
                pass  # could add Tabriz-specific tweaks
            case _:
                pass

        calc = IranPrayerCalculator()
        return calc.compute(d, coords["lat"], coords["lon"], coords["tz"])


if __name__ == "__main__":
    ipt = IranPrayerTimes(IranCity.TABRIZ)
    times = ipt.compute()

    print("Fajr:     ", times.fajr.strftime("%H:%M %d-%m-%Y"))
    print("Sunrise:  ", times.sunrise.strftime("%H:%M %d-%m-%Y"))
    print("Zuhr:     ", times.dhuhr.strftime("%H:%M %d-%m-%Y"))
    print("Asr:     ", times.asr.strftime("%H:%M %d-%m-%Y"))
    print("Sunset:   ", times.sunset.strftime("%H:%M %d-%m-%Y"))
    print("Maghrib:  ", times.maghrib.strftime("%H:%M %d-%m-%Y"))
    print("Isha:   ", times.isha.strftime("%H:%M %d-%m-%Y"))
    print("Midnight: ", times.midnight.strftime("%H:%M %d-%m-%Y"))
