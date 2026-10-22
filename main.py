from tripmate.trip import (
    create_trip,
    search_trip,
    update_trip,
    delete_trip
)

from tripmate.expenses import (
    add_expense,
    delete_expense
)

from tripmate.validation import (
    get_text_input,
    get_positive_float,
    get_positive_int,
    get_trip_dates,
    get_expense_category
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
    save_expenses,
    get_next_trip_id,
    get_next_expense_id
)

from tripmate.reports import (
    display_all_trips,
    display_trip_details,
    display_trip_report
)


trips = load_trips()
expenses = load_expenses()


while True:

    print("\n================================")
    print("            TRIPMATE")
    print("================================")

    print("1. Create Trip")
    print("2. My Trips")
    print("3. View Trip Details")
    print("4. Update Trip")
    print("5. Delete Trip")
    print("6. Add Expense")
    print("7. Delete Expense")
    print("8. Trip Report")
    print("9. Exit")

    try:

        choice = int(
            input(
                "Enter your choice: "
            )
        )

    except ValueError:

        error(
            "Please enter a number only."
        )

        continue


    if choice == 1:

        info(
            "\n--- Create Trip ---"
        )

        country = get_text_input(
            "Enter country: "
        )

        city = get_text_input(
            "Enter city: "
        )

        start_date, end_date = (
            get_trip_dates()
        )

        budget = get_positive_float(
            "Enter budget: "
        )

        trip_id = get_next_trip_id()

        create_trip(
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


    elif choice == 2:

        display_all_trips(
            trips,
            expenses
        )


    elif choice == 3:

        info(
            "\n--- Trip Details ---"
        )

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

        display_trip_details(
            trip,
            expenses
        )


    elif choice == 4:

        info(
            "\n--- Update Trip ---"
        )

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

        print(
            "\nCurrent trip:"
        )

        print(
            trip.display_info()
        )

        print(
            "\nEnter new information:"
        )

        country = get_text_input(
            "Enter new country: "
        )

        city = get_text_input(
            "Enter new city: "
        )

        start_date, end_date = (
            get_trip_dates()
        )

        budget = get_positive_float(
            "Enter new budget: "
        )

        updated = update_trip(
            trips,
            trip_id,
            country,
            city,
            start_date,
            end_date,
            budget
        )

        if updated:

            save_trips(
                trips
            )


    elif choice == 5:

        info(
            "\n--- Delete Trip ---"
        )

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

        display_trip_details(
            trip,
            expenses
        )

        while True:

            confirmation = input(
                "\nDelete this trip and all "
                "its expenses? (y/n): "
            ).strip().lower()

            if confirmation == "y":

                deleted = delete_trip(
                    trips,
                    expenses,
                    trip_id
                )

                if deleted:

                    save_trips(
                        trips
                    )

                    save_expenses(
                        expenses
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

        info(
            "\n--- Add Expense ---"
        )

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

        print(
            f"\nAdding expense to: "
            f"{trip.city}, {trip.country}"
        )

        title = get_text_input(
            "Enter expense title: "
        )

        category = (
            get_expense_category()
        )

        amount = get_positive_float(
            "Enter amount: "
        )

        expense_id = (
            get_next_expense_id()
        )

        add_expense(
            expenses,
            expense_id,
            trip_id,
            title,
            category,
            amount
        )

        save_expenses(
            expenses
        )


    elif choice == 7:

        info(
            "\n--- Delete Expense ---"
        )

        expense_id = get_positive_int(
            "Enter expense ID: "
        )

        deleted = delete_expense(
            expenses,
            expense_id
        )

        if deleted:

            save_expenses(
                expenses
            )


    elif choice == 8:

        info(
            "\n--- Trip Report ---"
        )

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

        display_trip_report(
            trip,
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