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
                {
                    "next_trip_id": 1,
                    "trips": []
                },
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
                {
                    "next_expense_id": 1,
                    "expenses": []
                },
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
        data = json.load(file)

    # Support old JSON format
    if isinstance(data, list):
        old_trips = data

        highest_id = 0

        for trip in old_trips:
            if trip["trip_id"] > highest_id:
                highest_id = trip["trip_id"]

        data = {
            "next_trip_id": highest_id + 1,
            "trips": old_trips
        }

        with open(
            TRIPS_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

    trips = []

    for trip_data in data["trips"]:
        trip = Trip(
            trip_data["trip_id"],
            trip_data["country"],
            trip_data["city"],
            trip_data["start_date"],
            trip_data["end_date"],
            trip_data["budget"]
        )

        trips.append(trip)

    return trips


def save_trips(trips: list):
    initialize_storage()

    with open(
        TRIPS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        current_data = json.load(file)

    if isinstance(current_data, list):
        highest_id = 0

        for trip in current_data:
            if trip["trip_id"] > highest_id:
                highest_id = trip["trip_id"]

        next_trip_id = highest_id + 1

    else:
        next_trip_id = current_data["next_trip_id"]

    trips_data = []

    for trip in trips:
        trips_data.append(
            {
                "trip_id": trip.trip_id,
                "country": trip.country,
                "city": trip.city,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "budget": trip.budget
            }
        )

    data = {
        "next_trip_id": next_trip_id,
        "trips": trips_data
    }

    with open(
        TRIPS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )


def get_next_trip_id():
    initialize_storage()

    with open(
        TRIPS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    if isinstance(data, list):
        highest_id = 0

        for trip in data:
            if trip["trip_id"] > highest_id:
                highest_id = trip["trip_id"]

        data = {
            "next_trip_id": highest_id + 1,
            "trips": data
        }

    trip_id = data["next_trip_id"]

    data["next_trip_id"] += 1

    with open(
        TRIPS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    return trip_id


def load_expenses():
    initialize_storage()

    with open(
        EXPENSES_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    # Support old JSON format
    if isinstance(data, list):
        old_expenses = data

        highest_id = 0

        for expense in old_expenses:
            if expense["expense_id"] > highest_id:
                highest_id = expense["expense_id"]

        data = {
            "next_expense_id": highest_id + 1,
            "expenses": old_expenses
        }

        with open(
            EXPENSES_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

    return data["expenses"]


def save_expenses(expenses: list):
    initialize_storage()

    with open(
        EXPENSES_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        current_data = json.load(file)

    if isinstance(current_data, list):
        highest_id = 0

        for expense in current_data:
            if expense["expense_id"] > highest_id:
                highest_id = expense["expense_id"]

        next_expense_id = highest_id + 1

    else:
        next_expense_id = current_data["next_expense_id"]

    data = {
        "next_expense_id": next_expense_id,
        "expenses": expenses
    }

    with open(
        EXPENSES_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )


def get_next_expense_id():
    initialize_storage()

    with open(
        EXPENSES_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    if isinstance(data, list):
        highest_id = 0

        for expense in data:
            if expense["expense_id"] > highest_id:
                highest_id = expense["expense_id"]

        data = {
            "next_expense_id": highest_id + 1,
            "expenses": data
        }

    expense_id = data["next_expense_id"]

    data["next_expense_id"] += 1

    with open(
        EXPENSES_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    return expense_id