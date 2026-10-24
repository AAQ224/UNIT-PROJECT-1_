import os
import json

from dotenv import load_dotenv
from google import genai

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from tripmate.colors import (
    error,
    warning
)


console = Console()

load_dotenv()


API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = (
    "gemini-3.5-flash-lite"
)


def get_ai_client():

    if not API_KEY:

        error(
            "Gemini API key was not found."
        )

        return None

    return genai.Client(
        api_key=API_KEY
    )


def clean_json_response(
    text: str
) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def correct_location_name(
    city: str,
    country: str
):

    client = get_ai_client()

    if client is None:

        return {
            "city": city,
            "country": country
        }


    prompt = f"""
Correct the spelling and formatting of this
travel destination.

City:
{city}

Country:
{country}

Return ONLY valid JSON.

Example:
{{
    "city": "Dammam",
    "country": "Saudi Arabia"
}}

Rules:
- Correct spelling mistakes.
- Use the official common English names.
- Do not change the intended location.
- Do not explain anything.
- Return JSON only.
"""


    try:

        response = (
            client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        )

        if not response.text:

            return {
                "city": city,
                "country": country
            }

        cleaned_response = (
            clean_json_response(
                response.text
            )
        )

        result = json.loads(
            cleaned_response
        )

        corrected_city = result.get(
            "city",
            city
        )

        corrected_country = result.get(
            "country",
            country
        )

        return {
            "city": corrected_city,
            "country": corrected_country
        }

    except Exception:

        warning(
            "AI location correction "
            "is currently unavailable."
        )

        return {
            "city": city,
            "country": country
        }


def get_travel_recommendations(
    budget: float,
    days: int,
    start_date: str,
    end_date: str,
    departure_city: str,
    departure_country: str,
    weather_preference: str,
    activity_preference: str,
    travel_style: str
):

    client = get_ai_client()

    if client is None:

        return []


    prompt = f"""
You are a travel recommendation assistant
inside a Python CLI application called TripMate.

Traveler information:

Departure location:
{departure_city}, {departure_country}

Total trip budget:
{budget} SAR

Trip duration:
{days} days

Travel dates:
{start_date} to {end_date}

Preferred weather:
{weather_preference}

Preferred activities:
{activity_preference}

Travel style:
{travel_style}

Recommend exactly 3 realistic international
travel destinations.

Important:
- Consider the departure location.
- Consider the travel dates and season.
- Consider the total budget in Saudi Riyals.
- The budget should reasonably include flights,
  accommodation, food, transport and activities.
- Consider the preferred weather.
- Avoid destinations that are clearly unrealistic
  for the provided budget.

For each destination return:

- city
- country
- short reason
- budget suitability
- three suggested activities

Return ONLY valid JSON.

Use exactly this structure:

[
    {{
        "city": "City Name",
        "country": "Country Name",
        "reason": "Short reason",
        "budget_suitability": "Short explanation",
        "activities": [
            "Activity 1",
            "Activity 2",
            "Activity 3"
        ]
    }}
]

Do not include markdown.
Do not include extra text.
"""


    try:

        response = (
            client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        )

    except Exception as exception:

        error(
            "\nCould not connect to Gemini."
        )

        print(
            exception
        )

        return []


    if not response.text:

        error(
            "Gemini returned "
            "an empty response."
        )

        return []


    try:

        cleaned_response = (
            clean_json_response(
                response.text
            )
        )

        recommendations = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError:

        error(
            "Gemini returned "
            "an invalid response format."
        )

        return []


    if not isinstance(
        recommendations,
        list
    ):

        error(
            "Invalid recommendation format."
        )

        return []


    if not recommendations:

        warning(
            "No destinations were recommended."
        )

        return []


    return recommendations


def display_ai_recommendations(
    recommendations: list
):

    if not recommendations:

        return


    table = Table(
        title="AI Travel Recommendations",
        header_style="bold cyan"
    )

    table.add_column(
        "#",
        justify="center",
        width=3
    )

    table.add_column(
        "Destination",
        max_width=25
    )

    table.add_column(
        "Why It Fits",
        max_width=50
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        city = recommendation.get(
            "city",
            "Unknown"
        )

        country = recommendation.get(
            "country",
            "Unknown"
        )

        reason = recommendation.get(
            "reason",
            "No reason provided."
        )


        table.add_row(
            str(index),
            f"{city}, {country}",
            reason
        )


    console.print()

    console.print(
        table
    )


def display_selected_recommendation(
    recommendation: dict
):

    city = recommendation.get(
        "city",
        "Unknown"
    )

    country = recommendation.get(
        "country",
        "Unknown"
    )

    reason = recommendation.get(
        "reason",
        "Not available."
    )

    budget = recommendation.get(
        "budget_suitability",
        "Not available."
    )

    activities = recommendation.get(
        "activities",
        []
    )


    activities_text = ""

    for activity in activities:

        activities_text += (
            f"• {activity}\n"
        )


    if not activities_text:

        activities_text = (
            "No activities provided."
        )


    content = (
        f"[bold]Destination:[/bold] "
        f"{city}, {country}\n\n"

        f"[bold]Why it fits:[/bold]\n"
        f"{reason}\n\n"

        f"[bold]Budget:[/bold]\n"
        f"{budget}\n\n"

        f"[bold]Suggested Activities:[/bold]\n"
        f"{activities_text.rstrip()}"
    )


    console.print()

    console.print(
        Panel(
            content,
            title="Selected Recommendation",
            border_style="cyan"
        )
    )


def select_ai_destination(
    recommendations: list
):

    if not recommendations:

        return None


    while True:

        try:

            choice = int(
                input(
                    "\nChoose a destination "
                    "number or enter 0 to cancel: "
                )
            )

        except ValueError:

            error(
                "Please enter a number only."
            )

            continue


        if choice == 0:

            return None


        if (
            choice < 1
            or
            choice > len(recommendations)
        ):

            error(
                "Invalid destination number."
            )

            continue


        return recommendations[
            choice - 1
        ]