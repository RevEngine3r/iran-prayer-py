```markdown
# Iran Prayer Times (Tehran Method)

A pure Python 3.10+ library for calculating Islamic prayer times in Iran using the **Tehran method** (Institute of Geophysics, University of Tehran).  
No external C libraries, no shapefiles — just clean Python code.

## Features
- Calculates **Fajr, Sunrise, Dhuhr, Asr, Sunset, Maghrib, Isha, Midnight**.
- Uses official **Tehran method angles** (Fajr 17.7°, Isha 14°).
- Supports **major Iranian cities** via an `Enum` (`IranCity`).
- Automatically applies **Iran timezone (UTC+3:30)**.
- Maghrib offset configurable (default +19 minutes to match Iranian timetables).
- Written for **Python 3.10+** with modern syntax (`match/case`, type hints, dataclasses).

## Installation
Clone the repo and use directly:

```bash
git clone https://github.com/yourname/iran-prayer-times.git
cd iran-prayer-times
```

No external dependencies required.  
Only Python standard library is used.

## Usage

```python
from iran_prayer_times import IranPrayerTimes, IranCity

# Select city
ipt = IranPrayerTimes(IranCity.TABRIZ)

# Compute for today
times = ipt.compute()

print("Fajr:    ", times.fajr.strftime("%H:%M"))
print("Sunrise: ", times.sunrise.strftime("%H:%M"))
print("Dhuhr:   ", times.dhuhr.strftime("%H:%M"))
print("Asr:     ", times.asr.strftime("%H:%M"))
print("Sunset:  ", times.sunset.strftime("%H:%M"))
print("Maghrib: ", times.maghrib.strftime("%H:%M"))
print("Isha:    ", times.isha.strftime("%H:%M"))
print("Midnight:", times.midnight.strftime("%H:%M"))
```

### Example Output (Tabriz, Nov 16, 2025)

```
Fajr:     05:35
Sunrise:  07:06
Dhuhr:    12:10
Asr:      15:31
Sunset:   17:12
Maghrib:  17:31
Isha:     18:22
Midnight: 23:24
```

## Notes
- **Maghrib**: By default, offset +19 minutes after sunset (Iranian convention).  
- **Midnight**: Defined as midpoint between sunset and next day’s Fajr.  
- Works offline, no internet required.

## License
MIT License.
```