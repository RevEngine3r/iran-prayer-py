from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
import math


@dataclass
class PrayerTimes:
    fajr: datetime
    sunrise: datetime
    dhuhr: datetime
    asr: datetime
    sunset: datetime
    maghrib: datetime
    isha: datetime
    midnight: datetime


class IranPrayerCalculator:
    def __init__(self,
                 fajr_angle: float = 17.7,
                 isha_angle: float = 14.0,
                 sunrise_sunset_altitude: float = -0.833,
                 asr_shadow_factor: float = 1.0,
                 maghrib_offset_minutes: int = 19):
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle
        self.sunrise_sunset_altitude = sunrise_sunset_altitude
        self.asr_shadow_factor = asr_shadow_factor
        self.maghrib_offset_minutes = maghrib_offset_minutes

    def compute(self, d: date, lat: float, lon: float, tz: str) -> PrayerTimes:
        zone = ZoneInfo(tz)
        tz_offset_minutes = int(datetime.combine(d, time(0), tzinfo=zone).utcoffset().total_seconds() // 60)

        jd = self._julian_day(d)
        dec, eq_time = self._solar_params(jd)
        phi = math.radians(lat)

        solar_noon = 720 - 4 * lon - eq_time

        # Sunrise / Sunset
        Hsun = self._hour_angle(self.sunrise_sunset_altitude, phi, dec)
        sunrise = self._to_local(d, solar_noon - 4 * math.degrees(Hsun), tz_offset_minutes, zone)
        sunset = self._to_local(d, solar_noon + 4 * math.degrees(Hsun), tz_offset_minutes, zone)

        # Fajr / Isha
        Hfajr = self._hour_angle(-self.fajr_angle, phi, dec)
        Hijsa = self._hour_angle(-self.isha_angle, phi, dec)
        fajr = self._to_local(d, solar_noon - 4 * math.degrees(Hfajr), tz_offset_minutes, zone)
        isha = self._to_local(d, solar_noon + 4 * math.degrees(Hijsa), tz_offset_minutes, zone)

        # Dhuhr
        dhuhr = self._to_local(d, solar_noon, tz_offset_minutes, zone)

        # Asr
        Hasr = self._hour_angle_asr(self.asr_shadow_factor, phi, dec)
        asr = self._to_local(d, solar_noon + 4 * math.degrees(Hasr), tz_offset_minutes, zone)

        # Maghrib (sunset + offset)
        maghrib = sunset + timedelta(minutes=self.maghrib_offset_minutes)

        # Midnight: midpoint between sunset and next day’s Fajr
        jd_next = self._julian_day(d + timedelta(days=1))
        dec_next, eq_time_next = self._solar_params(jd_next)
        solar_noon_next = 720 - 4 * lon - eq_time_next
        Hfajr_next = self._hour_angle(-self.fajr_angle, phi, dec_next)
        fajr_next = self._to_local(d + timedelta(days=1),
                                   solar_noon_next - 4 * math.degrees(Hfajr_next),
                                   tz_offset_minutes, zone)
        midnight = sunset + (fajr_next - sunset) / 2

        return PrayerTimes(fajr, sunrise, dhuhr, asr, sunset, maghrib, isha, midnight)

    # --- Astronomy helpers ---
    def _solar_params(self, jd: float):
        d = jd - 2451545.0
        g = math.radians(357.529 + 0.98560028 * d)
        q = 280.459 + 0.98564736 * d
        L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)
        e = math.radians(23.439 - 0.00000036 * d)
        ra = math.atan2(math.cos(e) * math.sin(L), math.cos(L))
        dec = math.asin(math.sin(e) * math.sin(L))
        ra_deg = (math.degrees(ra) % 360)
        eq_time = 4 * (((q % 360) - ra_deg + 540) % 360 - 180)
        return dec, eq_time

    def _hour_angle(self, alt_deg, phi, dec):
        alt = math.radians(alt_deg)
        cosH = (math.sin(alt) - math.sin(phi) * math.sin(dec)) / (math.cos(phi) * math.cos(dec))
        return math.acos(max(-1, min(1, cosH)))

    def _hour_angle_asr(self, k, phi, dec):
        t = math.tan(abs(phi - dec))
        alpha = -math.atan(1 / (k + t))
        cosH = (math.sin(alpha) - math.sin(phi) * math.sin(dec)) / (math.cos(phi) * math.cos(dec))
        return math.acos(max(-1, min(1, cosH)))

    def _to_local(self, base_date, utc_minutes, tz_minutes, zone):
        total = utc_minutes + tz_minutes
        h = int(total // 60)
        m = int(total % 60)
        s = int((total * 60) % 60)
        return datetime.combine(base_date, time(0), tzinfo=zone) + timedelta(hours=h, minutes=m, seconds=s)

    def _julian_day(self, d: date) -> float:
        y, m, day = d.year, d.month, d.day
        if m <= 2:
            y -= 1
            m += 12
        A = y // 100
        B = 2 - A + A // 4
        return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day + B - 1524.5


if __name__ == "__main__":
    calc = IranPrayerCalculator()  # Tehran method: Maghrib at sunset
    d = datetime.now(ZoneInfo("Asia/Tehran")).date()
    lat, lon = 38.0800, 46.2919  # Tabriz coordinates
    tz = "Asia/Tehran"

    times = calc.compute(d, lat, lon, tz)

    print("Fajr:     ", times.fajr.strftime("%H:%M:%S %d-%m-%Y"))
    print("Sunrise:  ", times.sunrise.strftime("%H:%M:%S %d-%m-%Y"))
    print("Ẓuhr:     ", times.dhuhr.strftime("%H:%M:%S %d-%m-%Y"))
    print("Sunset:   ", times.sunset.strftime("%H:%M:%S %d-%m-%Y"))
    print("Maghrib:  ", times.maghrib.strftime("%H:%M:%S %d-%m-%Y"))
    print("Midnight: ", times.midnight.strftime("%H:%M:%S %d-%m-%Y"))
