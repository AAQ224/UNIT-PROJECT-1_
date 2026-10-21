from datetime import datetime, date
from tripmate.colors import error


def get_text_input(message: str) -> str:
    while True:
        value = input(message).strip()

        if not value:
            error("Input cannot be empty.")
            continue

        if len(value) < 2:
            error("Input is too short.")
            continue

        if not any(char.isalpha() for char in value):
            error("Please enter a valid text value.")
            continue

        return value


def get_positive_float(message: str) -> float:
    while True:
        try:
            value = float(input(message))

            if value <= 0:
                error("Value must be greater than 0.")
                continue

            return value

        except ValueError:
            error("Please enter a valid number.")


def get_positive_int(message: str) -> int:
    while True:
        try:
            value = int(input(message))

            if value <= 0:
                error("Value must be greater than 0.")
                continue

            return value

        except ValueError:
            error("Please enter a valid number.")


def get_date(message: str) -> str:
    while True:
        date_input = input(message).strip()

        try:
            entered_date = datetime.strptime(
                date_input,
                "%Y-%m-%d"
            ).date()

            if entered_date < date.today():
                error("Date cannot be in the past.")
                continue

            return date_input

        except ValueError:
            error("Please use this format: YYYY-MM-DD")


def get_trip_dates():
    while True:
        start_date = get_date(
            "Enter start date (YYYY-MM-DD): "
        )

        end_date = get_date(
            "Enter end date (YYYY-MM-DD): "
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
            error("End date cannot be before start date.")
            continue

        return start_date, end_date