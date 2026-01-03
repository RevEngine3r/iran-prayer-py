"""Example usage of the Iran Prayer Times library."""

from datetime import datetime

from iran_prayer import City, IranPrayerTimes, PrayerTimeCalculator


def simple_city_example() -> None:
    """Example 1: Simple city-based calculation."""
    print("=== Simple City Example ===")

    prayer_times = IranPrayerTimes(City.TABRIZ)
    times = prayer_times.calculate()

    print(f"Prayer times for {prayer_times.city.display_name} ({prayer_times.city.persian_name}):")
    formatted = times.format_all("%H:%M")
    print(f"Fajr:     {formatted['Fajr']}")
    print(f"Sunrise:  {formatted['Sunrise']}")
    print(f"Dhuhr:    {formatted['Dhuhr']}")
    print(f"Asr:      {formatted['Asr']}")
    print(f"Sunset:   {formatted['Sunset']}")
    print(f"Maghrib:  {formatted['Maghrib']}")
    print(f"Isha:     {formatted['Isha']}")
    print(f"Midnight: {formatted['Midnight']}")
    print()


def custom_coordinates_example() -> None:
    """Example 2: Custom coordinates calculation."""
    print("=== Custom Coordinates Example ===")

    calculator = PrayerTimeCalculator()
    today = datetime.now()
    times = calculator.calculate(
        date=today,
        latitude=38.0800,  # Tabriz
        longitude=46.2919,
        time_zone="Asia/Tehran",
    )

    print("Prayer times for custom coordinates:")
    formatted = times.format_all("%H:%M:%S")
    for name, time in formatted.items():
        print(f"{name:8}: {time}")
    print()


def static_method_example() -> None:
    """Example 3: Using the static method."""
    print("=== Static Method Example ===")

    times = IranPrayerTimes.calculate_for_coordinates(
        latitude=35.6892,  # Tehran
        longitude=51.3890,
        time_zone="Asia/Tehran",
    )

    print("Prayer times using static method:")
    print(times)
    print()


def multiple_cities_example() -> None:
    """Example 4: Multiple cities comparison."""
    print("=== Multiple Cities Comparison ===")

    cities = [City.TEHRAN, City.TABRIZ, City.MASHHAD, City.SHIRAZ]

    for city in cities:
        times = IranPrayerTimes.for_city(city).calculate()
        formatted = times.format_all("%H:%M")
        print(
            f"{city.display_name:12} - "
            f"Fajr: {formatted['Fajr']}, "
            f"Dhuhr: {formatted['Dhuhr']}, "
            f"Maghrib: {formatted['Maghrib']}"
        )
    print()


def specific_date_example() -> None:
    """Example 5: Specific date calculation."""
    print("=== Specific Date Example ===")

    prayer_times = IranPrayerTimes(City.ISFAHAN)
    ramadan_start = datetime(2026, 2, 28)  # Example date
    times = prayer_times.calculate(ramadan_start)

    print(f"Prayer times for {prayer_times.city.display_name} on {ramadan_start.date()}:")
    formatted = times.format_all("%H:%M")
    for name, time in formatted.items():
        print(f"{name}: {time}")
    print()


def custom_calculator_example() -> None:
    """Example 6: Using custom calculator parameters."""
    print("=== Custom Calculator Example ===")

    # Create calculator with custom parameters
    custom_calc = PrayerTimeCalculator(
        fajr_angle=18.0,  # Different Fajr angle
        isha_angle=15.0,  # Different Isha angle
        maghrib_offset_minutes=20,  # Different Maghrib offset
    )

    prayer_times = IranPrayerTimes(City.QOM, calculator=custom_calc)
    times = prayer_times.calculate()

    print("Prayer times with custom calculator:")
    print(times)
    print()


def main() -> None:
    """Run all examples."""
    simple_city_example()
    custom_coordinates_example()
    static_method_example()
    multiple_cities_example()
    specific_date_example()
    custom_calculator_example()


if __name__ == "__main__":
    main()
