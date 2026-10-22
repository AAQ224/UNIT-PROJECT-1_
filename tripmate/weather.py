import requests

from datetime import (
    datetime,
    date
)

from rich.console import Console
from rich.panel import Panel

from tripmate.colors import (
    error,
    warning
)


console = Console()


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


def get_weather_description(
    weather_code: int
) -> str:

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Light rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        85: "Light snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail"
    }

    return weather_codes.get(
        weather_code,
        "Unknown weather"
    )


def find_location(
    city: str,
    country: str
):

    try:

        response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 10,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        error(
            "Could not connect to "
            "the location service."
        )

        return None


    results = data.get(
        "results"
    )

    if not results:

        error(
            "Location not found."
        )

        return None


    # Try to find the city
    # inside the entered country.
    for result in results:

        result_country = result.get(
            "country",
            ""
        )

        if (
            result_country.lower()
            ==
            country.lower()
        ):

            return result


    # If no country matches exactly,
    # return the first city result.
    return results[0]


def get_current_weather(
    latitude: float,
    longitude: float
):

    try:

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "apparent_temperature,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        error(
            "Could not connect to "
            "the weather service."
        )

        return None


    current = data.get(
        "current"
    )

    if current is None:

        error(
            "Current weather data "
            "is unavailable."
        )

        return None


    return {
        "temperature": current.get(
            "temperature_2m"
        ),

        "feels_like": current.get(
            "apparent_temperature"
        ),

        "humidity": current.get(
            "relative_humidity_2m"
        ),

        "wind_speed": current.get(
            "wind_speed_10m"
        ),

        "condition": (
            get_weather_description(
                current.get(
                    "weather_code",
                    -1
                )
            )
        )
    }


def get_trip_forecast(
    latitude: float,
    longitude: float,
    trip_date: str
):

    try:

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,

                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "apparent_temperature_max,"
                    "apparent_temperature_min,"
                    "precipitation_probability_max,"
                    "wind_speed_10m_max"
                ),

                "timezone": "auto",

                "start_date": trip_date,

                "end_date": trip_date
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        error(
            "Could not retrieve "
            "the trip forecast."
        )

        return None


    daily = data.get(
        "daily"
    )

    if not daily:

        return None


    if not daily.get(
        "time"
    ):

        return None


    return {
        "date": daily["time"][0],

        "condition": (
            get_weather_description(
                daily[
                    "weather_code"
                ][0]
            )
        ),

        "max_temperature": (
            daily[
                "temperature_2m_max"
            ][0]
        ),

        "min_temperature": (
            daily[
                "temperature_2m_min"
            ][0]
        ),

        "max_feels_like": (
            daily[
                "apparent_temperature_max"
            ][0]
        ),

        "min_feels_like": (
            daily[
                "apparent_temperature_min"
            ][0]
        ),

        "rain_probability": (
            daily[
                "precipitation_probability_max"
            ][0]
        ),

        "max_wind_speed": (
            daily[
                "wind_speed_10m_max"
            ][0]
        )
    }


def get_current_recommendation(
    weather: dict
) -> str:

    recommendations = []

    temperature = weather[
        "temperature"
    ]

    condition = weather[
        "condition"
    ].lower()


    if temperature is not None:

        if temperature <= 10:

            recommendations.append(
                "Take warm clothing."
            )

        elif temperature >= 30:

            recommendations.append(
                "Wear light clothes "
                "and stay hydrated."
            )

        else:

            recommendations.append(
                "The temperature is suitable "
                "for outdoor activities."
            )


    if (
        "rain" in condition
        or
        "drizzle" in condition
    ):

        recommendations.append(
            "Take an umbrella."
        )


    if "snow" in condition:

        recommendations.append(
            "Wear warm and waterproof clothes."
        )


    if "thunderstorm" in condition:

        recommendations.append(
            "Avoid outdoor activities "
            "during the storm."
        )


    if not recommendations:

        return (
            "Check the weather again "
            "before going out."
        )


    return " ".join(
        recommendations
    )


def get_forecast_recommendation(
    forecast: dict
) -> str:

    recommendations = []

    max_temperature = forecast[
        "max_temperature"
    ]

    min_temperature = forecast[
        "min_temperature"
    ]

    rain_probability = forecast[
        "rain_probability"
    ]

    condition = forecast[
        "condition"
    ].lower()


    if min_temperature <= 10:

        recommendations.append(
            "Pack warm clothing."
        )


    if max_temperature >= 30:

        recommendations.append(
            "Pack light clothes "
            "and stay hydrated."
        )


    if (
        rain_probability is not None
        and
        rain_probability >= 50
    ):

        recommendations.append(
            "There is a good chance of rain, "
            "so take an umbrella."
        )


    if "snow" in condition:

        recommendations.append(
            "Prepare for snowy weather "
            "and pack waterproof clothing."
        )


    if "thunderstorm" in condition:

        recommendations.append(
            "Outdoor plans may need "
            "to be adjusted."
        )


    if not recommendations:

        recommendations.append(
            "Weather conditions look "
            "generally comfortable."
        )


    return " ".join(
        recommendations
    )


def display_current_weather(
    location: dict
):

    weather = get_current_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather is None:

        return


    recommendation = (
        get_current_recommendation(
            weather
        )
    )


    weather_text = (
        f"[bold]Location:[/bold] "
        f"{location.get('name')}, "
        f"{location.get('country')}\n\n"

        f"[bold]Temperature:[/bold] "
        f"{weather['temperature']} °C\n"

        f"[bold]Feels Like:[/bold] "
        f"{weather['feels_like']} °C\n"

        f"[bold]Condition:[/bold] "
        f"{weather['condition']}\n"

        f"[bold]Humidity:[/bold] "
        f"{weather['humidity']}%\n"

        f"[bold]Wind Speed:[/bold] "
        f"{weather['wind_speed']} km/h\n\n"

        f"[bold cyan]"
        f"Recommendation:"
        f"[/bold cyan]\n"

        f"{recommendation}"
    )


    console.print()

    console.print(
        Panel(
            weather_text,
            title="Current Weather",
            border_style="blue"
        )
    )


def display_trip_forecast(
    location: dict,
    start_date: str
):

    forecast = get_trip_forecast(
        location["latitude"],
        location["longitude"],
        start_date
    )

    if forecast is None:

        error(
            "Forecast is currently unavailable."
        )

        return


    recommendation = (
        get_forecast_recommendation(
            forecast
        )
    )


    forecast_text = (
        f"[bold]Location:[/bold] "
        f"{location.get('name')}, "
        f"{location.get('country')}\n"

        f"[bold]Trip Date:[/bold] "
        f"{forecast['date']}\n\n"

        f"[bold]Condition:[/bold] "
        f"{forecast['condition']}\n"

        f"[bold]Maximum Temperature:[/bold] "
        f"{forecast['max_temperature']} °C\n"

        f"[bold]Minimum Temperature:[/bold] "
        f"{forecast['min_temperature']} °C\n"

        f"[bold]Feels Like:[/bold] "
        f"{forecast['min_feels_like']} °C"
        f" - "
        f"{forecast['max_feels_like']} °C\n"

        f"[bold]Rain Probability:[/bold] "
        f"{forecast['rain_probability']}%\n"

        f"[bold]Maximum Wind Speed:[/bold] "
        f"{forecast['max_wind_speed']} km/h\n\n"

        f"[bold cyan]"
        f"Travel Recommendation:"
        f"[/bold cyan]\n"

        f"{recommendation}"
    )


    console.print()

    console.print(
        Panel(
            forecast_text,
            title="Trip Weather Forecast",
            border_style="green"
        )
    )


def display_weather_for_trip(
    trip
):

    location = find_location(
        trip.city,
        trip.country
    )

    if location is None:

        return


    trip_date = datetime.strptime(
        trip.start_date,
        "%Y-%m-%d"
    ).date()

    today = date.today()

    days_until_trip = (
        trip_date - today
    ).days


    # Trip starts today.
    if days_until_trip == 0:

        console.print(
            "\n[cyan]"
            "Your trip starts today."
            "[/cyan]"
        )

        display_current_weather(
            location
        )

        return


    # Forecast is available
    # for up to 16 days.
    if 1 <= days_until_trip <= 16:

        console.print(
            f"\n[cyan]"
            f"Your trip starts in "
            f"{days_until_trip} day(s)."
            f"[/cyan]"
        )

        display_trip_forecast(
            location,
            trip.start_date
        )

        return


    # Old trip data.
    if days_until_trip < 0:

        warning(
            "This trip date is in the past."
        )

        display_current_weather(
            location
        )

        return


    # The trip is too far away
    # for an accurate forecast.
    console.print(
        "\n[yellow]"
        "An accurate forecast is not "
        "available yet because your trip "
        f"is {days_until_trip} days away."
        "[/yellow]"
    )

    console.print(
        "[yellow]"
        "Trip forecasts are available "
        "when the departure date is "
        "within 16 days."
        "[/yellow]"
    )

    console.print(
        "\nCurrent weather is shown "
        "below for reference only."
    )

    display_current_weather(
        location
    )