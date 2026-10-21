from tripmate.trip import (
    create_trip,
    display_trips,
    search_trip,
    update_trip,
    delete_trip
)

from tripmate.expenses import (
    add_expense,
    display_trip_expenses,
    delete_expense
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

from tripmate.storage import (
    load_trips,
    save_trips,
    load_expenses,
    save_expenses
)


trips = load_trips()
expenses = load_expenses()


while True:

    print("\n========================")
    print("        TRIPMATE")
    print("========================")
    print("1. Create Trip")
    print("2. Display Trips")
    print("3. Search Trip")
    print("4. Update Trip")
    print("5. Delete Trip")
    print("6. Add Expense")
    print("7. Display Trip Expenses")
    print("8. Delete Expense")
    print("9. Exit")

    try:

        choice = int(
            input("Enter your choice: ")
        )

    except ValueError:

        error(
            "Please enter a number only."
        )

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

        save_trips(
            trips
        )


    elif choice == 2:

        display_trips(
            trips
        )


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

            error(
                "Trip not found."
            )

        else:

            print()
            print(
                trip.display_info()
            )


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

            error(
                "Trip not found."
            )

            continue

        print("\nCurrent trip:")

        print(
            trip.display_info()
        )

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

        save_trips(
            trips
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

            error(
                "Trip not found."
            )

            continue

        print()

        print(
            trip.display_info()
        )

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

                save_trips(
                    trips
                )

                break

            elif confirmation == "n":

                warning(
                    "Delete cancelled."
                )

                break

            else:

                error(
                    "Please enter y or n."
                )


    elif choice == 6:

        info("\n--- Add Expense ---")

        trip_id = get_positive_int(
            "Enter trip ID: "
        )

        trip = search_trip(
            trips,
            trip_id
        )

        if trip is None:

            error(
                "Trip not found."
            )

            continue

        title = get_text_input(
            "Enter expense title: "
        )

        category = get_text_input(
            "Enter category: "
        )

        amount = get_positive_float(
            "Enter amount: "
        )

        add_expense(
            expenses,
            trip_id,
            title,
            category,
            amount
        )

        save_expenses(
            expenses
        )


    elif choice == 7:

        info("\n--- Trip Expenses ---")

        trip_id = get_positive_int(
            "Enter trip ID: "
        )

        trip = search_trip(
            trips,
            trip_id
        )

        if trip is None:

            error(
                "Trip not found."
            )

            continue

        print()
        print(
            trip.display_info()
        )

        display_trip_expenses(
            expenses,
            trip_id
        )


    elif choice == 8:

        info("\n--- Delete Expense ---")

        expense_id = get_positive_int(
            "Enter expense ID: "
        )

        delete_expense(
            expenses,
            expense_id
        )

        save_expenses(
            expenses
        )


    elif choice == 9:

        warning(
            "\nProgram ended."
        )

        break


    else:

        error(
            "Invalid choice. "
            "Please choose from 1 to 9."
        )