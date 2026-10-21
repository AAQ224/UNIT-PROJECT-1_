from tripmate.trip import (
    create_trip,
    display_trips,
    search_trip,
    update_trip,
    delete_trip
)

from tripmate.validation import (
    get_text_input,
    get_positive_float,
    get_positive_int,
    get_trip_dates
)

from tripmate.colors import (
    error,
    warning,
    info
)


trips = []


while True:

    print("\n========================")
    print("        TRIPMATE")
    print("========================")
    print("1. Create Trip")
    print("2. Display Trips")
    print("3. Search Trip")
    print("4. Update Trip")
    print("5. Delete Trip")
    print("6. Exit")

    try:
        choice = int(
            input("Enter your choice: ")
        )

    except ValueError:
        error("Please enter a number only.")
        continue


    if choice == 1:

        info("\n--- Create Trip ---")

        country = get_text_input(
            "Enter country: "
        )

        city = get_text_input(
            "Enter city: "
        )

        start_date, end_date = get_trip_dates()

        budget = get_positive_float(
            "Enter budget: "
        )

        create_trip(
            trips,
            country,
            city,
            start_date,
            end_date,
            budget
        )


    elif choice == 2:

        display_trips(trips)


    elif choice == 3:

        info("\n--- Search Trip ---")

        trip_id = get_positive_int(
            "Enter trip ID: "
        )

        trip = search_trip(
            trips,
            trip_id
        )

        if trip is None:
            error("Trip not found.")

        else:
            print()
            print(trip.display_info())


    elif choice == 4:

        info("\n--- Update Trip ---")

        trip_id = get_positive_int(
            "Enter trip ID: "
        )

        trip = search_trip(
            trips,
            trip_id
        )

        if trip is None:
            error("Trip not found.")
            continue

        print("\nCurrent trip:")
        print(trip.display_info())

        print("\nEnter new information:")

        country = get_text_input(
            "Enter new country: "
        )

        city = get_text_input(
            "Enter new city: "
        )

        start_date, end_date = get_trip_dates()

        budget = get_positive_float(
            "Enter new budget: "
        )

        update_trip(
            trips,
            trip_id,
            country,
            city,
            start_date,
            end_date,
            budget
        )


    elif choice == 5:

        info("\n--- Delete Trip ---")

        trip_id = get_positive_int(
            "Enter trip ID: "
        )

        trip = search_trip(
            trips,
            trip_id
        )

        if trip is None:
            error("Trip not found.")
            continue

        print()
        print(trip.display_info())

        while True:

            confirmation = input(
                "\nAre you sure you want to delete "
                "this trip? (y/n): "
            ).strip().lower()

            if confirmation == "y":

                delete_trip(
                    trips,
                    trip_id
                )

                break

            elif confirmation == "n":

                warning("Delete cancelled.")
                break

            else:

                error("Please enter y or n.")


    elif choice == 6:

        warning("\nProgram ended.")
        break


    else:

        error(
            "Invalid choice. "
            "Please choose from 1 to 6."
        )