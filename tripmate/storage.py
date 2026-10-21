import json
import os

from tripmate.trip import Trip


DATA_FOLDER = "data"

TRIPS_FILE = os.path.join(
    DATA_FOLDER,
    "trips.json"
)

EXPENSES_FILE = os.path.join(
    DATA_FOLDER,
    "expenses.json"
)


def initialize_storage():

    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)

    if not os.path.exists(TRIPS_FILE):

        with open(
            TRIPS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

    if not os.path.exists(EXPENSES_FILE):

        with open(
            EXPENSES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def save_trips(trips: list):

    trips_data = []

    for trip in trips:

        trip_data = {
            "trip_id": trip.trip_id,
            "country": trip.country,
            "city": trip.city,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "budget": trip.budget
        }

        trips_data.append(
            trip_data
        )

    with open(
        TRIPS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            trips_data,
            file,
            indent=4
        )


def load_trips():

    initialize_storage()

    with open(
        TRIPS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        trips_data = json.load(file)

    trips = []

    for trip_data in trips_data:

        trip = Trip(
            trip_data["trip_id"],
            trip_data["country"],
            trip_data["city"],
            trip_data["start_date"],
            trip_data["end_date"],
            trip_data["budget"]
        )

        trips.append(
            trip
        )

    return trips


def save_expenses(expenses: list):

    with open(
        EXPENSES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            expenses,
            file,
            indent=4
        )


def load_expenses():

    initialize_storage()

    with open(
        EXPENSES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        expenses = json.load(file)

    return expenses