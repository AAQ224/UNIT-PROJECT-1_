"""Location input, AI correction and validation workflow."""

from tripmate.services.ai_helper import (
    correct_location_name
)

from tripmate.core.colors import (
    ai,
    error,
    info,
    warning
)

from tripmate.core.validation import (
    get_text_input,
    get_yes_no
)

from tripmate.services.weather import (
    find_location
)


def get_confirmed_location(
    title: str,
    ai_mode: bool = False
):

    while True:

        if ai_mode:

            ai(
                f"\n--- AI: {title} ---"
            )

        else:

            info(
                f"\n--- {title} ---"
            )


        country = get_text_input(
            "Enter country: "
        )

        city = get_text_input(
            "Enter city: "
        )


        ai(
            "\nGemini is checking "
            "the spelling of the location..."
        )


        corrected = correct_location_name(
            city,
            country
        )


        corrected_city = corrected[
            "city"
        ]

        corrected_country = corrected[
            "country"
        ]


        if (
            corrected_city.lower()
            != city.lower()
            or
            corrected_country.lower()
            != country.lower()
        ):

            ai(
                f"AI suggestion: "
                f"{corrected_city}, "
                f"{corrected_country}"
            )


        info(
            "Validating location with "
            "the location service..."
        )


        location = find_location(
            corrected_city,
            corrected_country
        )


        if location is None:

            error(
                "Could not find this location."
            )

            retry = get_yes_no(
                "Try again? (y/n): "
            )

            if retry:

                continue

            return None


        location_city = location.get(
            "name",
            corrected_city
        )

        location_country = location.get(
            "country",
            corrected_country
        )


        print(
            "\nDid you mean:"
        )

        print(
            f"{location_city}, "
            f"{location_country}"
        )


        confirmed = get_yes_no(
            "Use this location? (y/n): "
        )


        if confirmed:

            return {
                "city": location_city,
                "country": location_country
            }


        warning(
            "Please enter "
            "the location again."
        )