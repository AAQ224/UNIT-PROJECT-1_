from tripmate.trip import (
    create_trip,
    search_trip,
    update_country,
    update_city,
    update_dates,
    update_budget,
    delete_trip
)

from tripmate.expenses import (
    add_expense,
    get_trip_expenses,
    get_expense,
    calculate_total_expenses,
    display_trip_expenses,
    delete_expense
)

from tripmate.validation import (
    get_text_input,
    get_positive_float,
    get_positive_int,
    get_non_negative_int,
    get_menu_choice,
    get_yes_no,
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

from tripmate.weather import (
    display_weather_for_trip
)


trips = load_trips()
expenses = load_expenses()


while True:

    print(
        "\n================================"
    )

    print(
        "            TRIPMATE"
    )

    print(
        "================================"
    )

    print(
        "1. Create Trip"
    )

    print(
        "2. My Trips"
    )

    print(
        "3. Manage Trip"
    )

    print(
        "4. Exit"
    )

    choice = get_menu_choice(
        "Enter your choice: ",
        1,
        4
    )


    # ==========================
    # CREATE TRIP
    # ==========================
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


    # ==========================
    # MY TRIPS
    # ==========================
    elif choice == 2:

        display_all_trips(
            trips,
            expenses
        )


    # ==========================
    # MANAGE TRIP
    # ==========================
    elif choice == 3:

        if not trips:

            warning(
                "No trips available."
            )

            continue


        display_all_trips(
            trips,
            expenses
        )

        print(
            "\nEnter 0 to go back."
        )

        trip_id = get_non_negative_int(
            "Enter trip ID: "
        )


        if trip_id == 0:

            continue


        trip = search_trip(
            trips,
            trip_id
        )


        if trip is None:

            error(
                "Trip not found."
            )

            continue


        while True:

            print(
                "\n================================"
            )

            print(
                f"   {trip.city}, "
                f"{trip.country}"
            )

            print(
                "================================"
            )

            print(
                "1. View Trip Details"
            )

            print(
                "2. Update Trip"
            )

            print(
                "3. Add Expense"
            )

            print(
                "4. Delete Expense"
            )

            print(
                "5. Trip Report"
            )

            print(
                "6. Check Trip Weather"
            )

            print(
                "7. Delete Trip"
            )

            print(
                "8. Back"
            )

            trip_choice = get_menu_choice(
                "Enter your choice: ",
                1,
                8
            )


            # ==================
            # VIEW DETAILS
            # ==================
            if trip_choice == 1:

                display_trip_details(
                    trip,
                    expenses
                )


            # ==================
            # UPDATE TRIP
            # ==================
            elif trip_choice == 2:

                while True:

                    print(
                        "\n--- Update Trip ---"
                    )

                    print(
                        "1. Country"
                    )

                    print(
                        "2. City"
                    )

                    print(
                        "3. Dates"
                    )

                    print(
                        "4. Budget"
                    )

                    print(
                        "5. Back"
                    )

                    update_choice = (
                        get_menu_choice(
                            "What do you want "
                            "to update? ",
                            1,
                            5
                        )
                    )


                    if update_choice == 1:

                        country = get_text_input(
                            "Enter new country: "
                        )

                        update_country(
                            trip,
                            country
                        )

                        save_trips(
                            trips
                        )


                    elif update_choice == 2:

                        city = get_text_input(
                            "Enter new city: "
                        )

                        update_city(
                            trip,
                            city
                        )

                        save_trips(
                            trips
                        )


                    elif update_choice == 3:

                        start_date, end_date = (
                            get_trip_dates()
                        )

                        update_dates(
                            trip,
                            start_date,
                            end_date
                        )

                        save_trips(
                            trips
                        )


                    elif update_choice == 4:

                        budget = (
                            get_positive_float(
                                "Enter new budget: "
                            )
                        )

                        current_spent = (
                            calculate_total_expenses(
                                expenses,
                                trip.trip_id
                            )
                        )


                        if budget < current_spent:

                            warning(
                                "\nNew budget is lower "
                                "than current spending."
                            )

                            print(
                                f"Current spending: "
                                f"{current_spent:,.2f} SAR"
                            )

                            print(
                                f"New budget: "
                                f"{budget:,.2f} SAR"
                            )

                            confirm = get_yes_no(
                                "Continue? (y/n): "
                            )


                            if not confirm:

                                warning(
                                    "Budget update cancelled."
                                )

                                continue


                        update_budget(
                            trip,
                            budget
                        )

                        save_trips(
                            trips
                        )


                    elif update_choice == 5:

                        break


            # ==================
            # ADD EXPENSE
            # ==================
            elif trip_choice == 3:

                info(
                    "\n--- Add Expense ---"
                )

                print(
                    f"Trip: "
                    f"{trip.city}, "
                    f"{trip.country}"
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

                current_spent = (
                    calculate_total_expenses(
                        expenses,
                        trip.trip_id
                    )
                )

                remaining = (
                    trip.budget
                    - current_spent
                )


                if amount > remaining:

                    warning(
                        "\nThis expense exceeds "
                        "your remaining budget."
                    )

                    print(
                        f"Remaining budget: "
                        f"{remaining:,.2f} SAR"
                    )

                    print(
                        f"Expense amount: "
                        f"{amount:,.2f} SAR"
                    )

                    confirm = get_yes_no(
                        "Add it anyway? (y/n): "
                    )


                    if not confirm:

                        warning(
                            "Expense cancelled."
                        )

                        continue


                expense_id = (
                    get_next_expense_id()
                )

                add_expense(
                    expenses,
                    expense_id,
                    trip.trip_id,
                    title,
                    category,
                    amount
                )

                save_expenses(
                    expenses
                )


            # ==================
            # DELETE EXPENSE
            # ==================
            elif trip_choice == 4:

                info(
                    "\n--- Delete Expense ---"
                )

                trip_expenses = (
                    get_trip_expenses(
                        expenses,
                        trip.trip_id
                    )
                )


                if not trip_expenses:

                    warning(
                        "This trip has no expenses."
                    )

                    continue


                display_trip_expenses(
                    expenses,
                    trip.trip_id
                )

                expense_id = (
                    get_positive_int(
                        "Enter expense ID "
                        "to delete: "
                    )
                )

                expense = get_expense(
                    expenses,
                    trip.trip_id,
                    expense_id
                )


                if expense is None:

                    error(
                        "That expense does not "
                        "belong to this trip."
                    )

                    continue


                print(
                    "\nSelected Expense:"
                )

                print(
                    f"{expense['title']} | "
                    f"{expense['category']} | "
                    f"{expense['amount']:,.2f} SAR"
                )

                confirm = get_yes_no(
                    "Delete this expense? "
                    "(y/n): "
                )


                if not confirm:

                    warning(
                        "Delete cancelled."
                    )

                    continue


                deleted = delete_expense(
                    expenses,
                    trip.trip_id,
                    expense_id
                )


                if deleted:

                    save_expenses(
                        expenses
                    )


            # ==================
            # TRIP REPORT
            # ==================
            elif trip_choice == 5:

                display_trip_report(
                    trip,
                    expenses
                )


            # ==================
            # WEATHER
            # ==================
            elif trip_choice == 6:

                info(
                    "\n--- Trip Weather ---"
                )

                display_weather_for_trip(
                    trip
                )


            # ==================
            # DELETE TRIP
            # ==================
            elif trip_choice == 7:

                display_trip_details(
                    trip,
                    expenses
                )

                warning(
                    "\nDeleting this trip will "
                    "also delete all its expenses."
                )

                confirm = get_yes_no(
                    "Delete this trip? (y/n): "
                )


                if not confirm:

                    warning(
                        "Delete cancelled."
                    )

                    continue


                deleted = delete_trip(
                    trips,
                    expenses,
                    trip.trip_id
                )


                if deleted:

                    save_trips(
                        trips
                    )

                    save_expenses(
                        expenses
                    )

                    break


            # ==================
            # BACK
            # ==================
            elif trip_choice == 8:

                break


    # ==========================
    # EXIT
    # ==========================
    elif choice == 4:

        warning(
            "\nProgram ended."
        )

        break