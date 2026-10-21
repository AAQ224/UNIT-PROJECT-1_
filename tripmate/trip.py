from tripmate.colors import success, error


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
            f"Country: {self.country}\n"
            f"City: {self.city}\n"
            f"Start Date: {self.start_date}\n"
            f"End Date: {self.end_date}\n"
            f"Budget: {self.budget:.2f} SAR"
        )


def generate_trip_id(trips: list):

    if not trips:
        return 1

    highest_id = 0

    for trip in trips:
        if trip.trip_id > highest_id:
            highest_id = trip.trip_id

    return highest_id + 1


def create_trip(
    trips: list,
    country: str,
    city: str,
    start_date: str,
    end_date: str,
    budget: float
):

    trip_id = generate_trip_id(trips)

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


def display_trips(trips: list):

    if not trips:
        error("\nNo trips found.")
        return

    print("\n========================")
    print("        MY TRIPS")
    print("========================")

    for trip in trips:
        print()
        print(trip.display_info())
        print("------------------------")


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
        return

    trip.country = country
    trip.city = city
    trip.start_date = start_date
    trip.end_date = end_date
    trip.budget = budget

    success("Trip updated successfully.")


def delete_trip(
    trips: list,
    trip_id: int
):

    trip = search_trip(
        trips,
        trip_id
    )

    if trip is None:
        error("Trip not found.")
        return

    trips.remove(trip)

    success("Trip deleted successfully.")