from tripmate.colors import (
    success,
    error
)


class Trip:

    def __init__(
        self,
        trip_id: int,
        country: str,
        city: str,
        start_date: str,
        end_date: str,
        budget: float
    ):
        self.trip_id = trip_id
        self.country = country
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget


    def display_info(self):
        return (
            f"Trip ID: {self.trip_id}\n"
            f"Destination: {self.city}, {self.country}\n"
            f"Start Date: {self.start_date}\n"
            f"End Date: {self.end_date}\n"
            f"Budget: {self.budget:,.2f} SAR"
        )


def create_trip(
    trips: list,
    trip_id: int,
    country: str,
    city: str,
    start_date: str,
    end_date: str,
    budget: float
):

    trip = Trip(
        trip_id,
        country,
        city,
        start_date,
        end_date,
        budget
    )

    trips.append(trip)

    success("\nTrip created successfully.")
    success(f"Trip ID: {trip_id}")


def search_trip(
    trips: list,
    trip_id: int
):

    for trip in trips:

        if trip.trip_id == trip_id:
            return trip

    return None


def update_trip(
    trips: list,
    trip_id: int,
    country: str,
    city: str,
    start_date: str,
    end_date: str,
    budget: float
):

    trip = search_trip(
        trips,
        trip_id
    )

    if trip is None:
        error("Trip not found.")
        return False

    trip.country = country
    trip.city = city
    trip.start_date = start_date
    trip.end_date = end_date
    trip.budget = budget

    success("Trip updated successfully.")

    return True


def delete_trip(
    trips: list,
    expenses: list,
    trip_id: int
):

    trip = search_trip(
        trips,
        trip_id
    )

    if trip is None:
        error("Trip not found.")
        return False

    # Delete all expenses linked to this trip
    expenses[:] = [
        expense
        for expense in expenses
        if expense["trip_id"] != trip_id
    ]

    trips.remove(trip)

    success(
        "Trip and all related expenses "
        "deleted successfully."
    )

    return True