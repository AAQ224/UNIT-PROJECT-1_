import re

from datetime import (
    datetime,
    date
)

from tripmate.colors import (
    error
)

from tripmate.expenses import (
    EXPENSE_CATEGORIES
)


def get_text_input(
    message: str
) -> str:

    while True:

        value = input(
            message
        ).strip()

        if not value:

            error(
                "Input cannot be empty."
            )

            continue

        if len(value) < 2:

            error(
                "Input is too short."
            )

            continue

        if not any(
            character.isalpha()
            for character in value
        ):

            error(
                "Please enter a valid text value."
            )

            continue

        return value


def get_positive_float(
    message: str
) -> float:

    while True:

        try:

            value = float(
                input(message)
            )

            if value <= 0:

                error(
                    "Value must be greater than 0."
                )

                continue

            return value

        except ValueError:

            error(
                "Please enter a valid number."
            )


def get_positive_int(
    message: str
) -> int:

    while True:

        try:

            value = int(
                input(message)
            )

            if value <= 0:

                error(
                    "Value must be greater than 0."
                )

                continue

            return value

        except ValueError:

            error(
                "Please enter a valid number."
            )


def get_non_negative_int(
    message: str
) -> int:

    while True:

        try:

            value = int(
                input(message)
            )

            if value < 0:

                error(
                    "Value cannot be negative."
                )

                continue

            return value

        except ValueError:

            error(
                "Please enter a valid number."
            )


def get_menu_choice(
    message: str,
    minimum: int,
    maximum: int
) -> int:

    while True:

        try:

            choice = int(
                input(message)
            )

        except ValueError:

            error(
                "Please enter a number only."
            )

            continue

        if (
            choice < minimum
            or
            choice > maximum
        ):

            error(
                f"Please choose from "
                f"{minimum} to {maximum}."
            )

            continue

        return choice


def get_yes_no(
    message: str
) -> bool:

    while True:

        answer = input(
            message
        ).strip().lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        error(
            "Please enter y or n."
        )


def get_date(
    message: str
) -> str:

    while True:

        date_input = input(
            message
        ).strip()

        # Force exactly YYYY-MM-DD
        if not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}",
            date_input
        ):

            error(
                "Please use this format: "
                "YYYY-MM-DD"
            )

            continue

        try:

            entered_date = datetime.strptime(
                date_input,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            error(
                "Invalid date."
            )

            continue

        if entered_date < date.today():

            error(
                "Date cannot be in the past."
            )

            continue

        maximum_year = (
            date.today().year + 10
        )

        if entered_date.year > maximum_year:

            error(
                "Trip date cannot be more "
                "than 10 years in the future."
            )

            continue

        return date_input


def get_trip_dates():

    while True:

        start_date = get_date(
            "Enter start date "
            "(YYYY-MM-DD): "
        )

        end_date = get_date(
            "Enter end date "
            "(YYYY-MM-DD): "
        )

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()

        if end < start:

            error(
                "End date cannot be "
                "before start date."
            )

            continue

        return (
            start_date,
            end_date
        )


def get_expense_category():

    while True:

        print(
            "\nChoose expense category:"
        )

        for index, category in enumerate(
            EXPENSE_CATEGORIES,
            start=1
        ):

            print(
                f"{index}. {category}"
            )

        choice = get_menu_choice(
            "Enter category number: ",
            1,
            len(EXPENSE_CATEGORIES)
        )

        return EXPENSE_CATEGORIES[
            choice - 1
        ]