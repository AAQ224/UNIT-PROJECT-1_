from tripmate.ai_helper import (
    correct_location_name,
    display_ai_recommendations,
    display_selected_recommendation,
    get_travel_recommendations,
    select_ai_destination
)

from tripmate.colors import (
    ai,
    error,
    info,
    success,
    warning
)

from tripmate.expenses import (
    add_expense,
    calculate_total_expenses,
    delete_expense,
    display_trip_expenses,
    get_expense,
    get_trip_expenses,
    update_expense
)

from tripmate.reports import (
    display_all_trips,
    display_trip_details,
    display_trip_report,
    export_trip_to_csv
)

from tripmate.storage import (
    get_next_expense_id,
    get_next_trip_id,
    load_expenses,
    load_trips,
    save_expenses,
    save_trips
)

from tripmate.trip import (
    create_trip,
    delete_trip,
    search_trip,
    update_budget,
    update_city,
    update_country,
    update_dates
)

from tripmate.utils import (
    format_money,
    today_str
)

from tripmate.validation import (
    calculate_end_date,
    get_date,
    get_expense_category,
    get_menu_choice,
    get_non_negative_int,
    get_positive_float,
    get_positive_int,
    get_text_input,
    get_trip_dates,
    get_yes_no
)

from tripmate.weather import (
    display_weather_for_trip,
    find_location
)


trips = load_trips()

expenses = load_expenses()


def print_menu(
    title: str,
    options: list
):

    print(
        "\n================================"
    )

    print(
        f"   {title}"
    )

    print(
        "================================"
    )


    for index, option in enumerate(
        options,
        start=1
    ):

        print(
            f"{index}. {option}"
        )


def warn_if_over_budget(
    trip
):

    spent = calculate_total_expenses(
        expenses,
        trip.trip_id
    )


    if spent > trip.budget:

        warning(
            "Warning: this trip is "
            "over budget "
            f"({format_money(spent)} "
            f"of {format_money(trip.budget)})."
        )


def choose_from(
    title: str,
    options: dict,
    message: str
) -> str:

    ai(
        f"\n{title}"
    )


    for number, label in options.items():

        print(
            f"{number}. {label}"
        )


    choice = get_menu_choice(
        message,
        1,
        len(
            options
        )
    )


    return options[
        choice
    ]


def get_confirmed_location(
    title: str,
    ai_mode: bool = False
):

    while True:

        if ai_mode:

            ai(
                f"\n--- AI: {title} ---"
            )


        else:

            info(
                f"\n--- {title} ---"
            )


        country = get_text_input(
            "Enter country: "
        )


        city = get_text_input(
            "Enter city: "
        )


        ai(
            "\nGemini is checking "
            "the spelling of the location..."
        )


        corrected = correct_location_name(
            city,
            country
        )


        if (
            corrected[
                "city"
            ].lower()
            !=
            city.lower()
            or
            corrected[
                "country"
            ].lower()
            !=
            country.lower()
        ):

            ai(
                f"AI suggestion: "
                f"{corrected['city']}, "
                f"{corrected['country']}"
            )


        info(
            "Validating location with "
            "the location service..."
        )


        location = find_location(
            corrected[
                "city"
            ],
            corrected[
                "country"
            ]
        )


        if location is None:

            error(
                "Could not find this location."
            )


            if get_yes_no(
                "Try again? (y/n): "
            ):

                continue


            return None


        location_city = location.get(
            "name",
            corrected[
                "city"
            ]
        )


        location_country = location.get(
            "country",
            corrected[
                "country"
            ]
        )


        print(
            "\nDid you mean:"
        )


        print(
            f"{location_city}, "
            f"{location_country}"
        )


        if get_yes_no(
            "Use this location? (y/n): "
        ):

            return {
                "city": location_city,
                "country": location_country
            }


        warning(
            "Please enter "
            "the location again."
        )


def create_trip_workflow():

    info(
        "\n--- Create Trip ---"
    )


    destination = (
        get_confirmed_location(
            "Destination"
        )
    )


    if destination is None:

        return


    start_date, end_date = (
        get_trip_dates()
    )


    budget = get_positive_float(
        "Enter budget: "
    )


    create_trip(
        trips,
        get_next_trip_id(
            trips
        ),
        destination[
            "country"
        ],
        destination[
            "city"
        ],
        start_date,
        end_date,
        budget
    )


    save_trips(
        trips
    )


def update_trip_menu(
    trip
):

    while True:

        print_menu(
            "Update Trip",
            [
                "Destination",
                "Dates",
                "Budget",
                "Back"
            ]
        )


        choice = get_menu_choice(
            "What do you want to update? ",
            1,
            4
        )


        if choice == 1:

            destination = (
                get_confirmed_location(
                    "New Destination"
                )
            )


            if destination is None:

                continue


            update_country(
                trip,
                destination[
                    "country"
                ]
            )


            update_city(
                trip,
                destination[
                    "city"
                ]
            )


            save_trips(
                trips
            )


        elif choice == 2:

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


        elif choice == 3:

            budget = get_positive_float(
                "Enter new budget: "
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
                    f"{format_money(current_spent)}"
                )


                print(
                    f"New budget: "
                    f"{format_money(budget)}"
                )


                if not get_yes_no(
                    "Continue? (y/n): "
                ):

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


        elif choice == 4:

            break


def add_expense_workflow(
    trip
):

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


    expense_date = get_date(
        (
            "Enter expense date "
            "(YYYY-MM-DD, "
            "press Enter for today): "
        ),
        allow_past=True,
        allow_future=False,
        default=today_str()
    )


    remaining = (
        trip.budget
        -
        calculate_total_expenses(
            expenses,
            trip.trip_id
        )
    )


    if amount > remaining:

        warning(
            "\nThis expense exceeds "
            "your remaining budget."
        )


        print(
            f"Remaining budget: "
            f"{format_money(remaining)}"
        )


        print(
            f"Expense amount: "
            f"{format_money(amount)}"
        )


        if not get_yes_no(
            "Add it anyway? (y/n): "
        ):

            warning(
                "Expense cancelled."
            )

            return


    add_expense(
        expenses,
        get_next_expense_id(
            expenses
        ),
        trip.trip_id,
        title,
        category,
        amount,
        expense_date
    )


    save_expenses(
        expenses
    )


def select_expense(
    trip,
    action: str
):

    if not get_trip_expenses(
        expenses,
        trip.trip_id
    ):

        warning(
            "This trip has no expenses."
        )

        return None


    display_trip_expenses(
        expenses,
        trip.trip_id
    )


    expense_id = get_positive_int(
        f"Enter expense ID "
        f"to {action}: "
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


    return expense


def edit_expense_workflow(
    trip
):

    info(
        "\n--- Edit Expense ---"
    )


    expense = select_expense(
        trip,
        "edit"
    )


    if expense is None:

        return


    print_menu(
        "Edit Expense",
        [
            "Title",
            "Category",
            "Amount",
            "Date",
            "Cancel"
        ]
    )


    choice = get_menu_choice(
        "What do you want to edit? ",
        1,
        5
    )


    if choice == 1:

        update_expense(
            expense,
            title=get_text_input(
                "Enter new title: "
            )
        )


    elif choice == 2:

        update_expense(
            expense,
            category=(
                get_expense_category()
            )
        )


    elif choice == 3:

        update_expense(
            expense,
            amount=get_positive_float(
                "Enter new amount: "
            )
        )


    elif choice == 4:

        update_expense(
            expense,
            date=get_date(
                "Enter new date "
                "(YYYY-MM-DD): ",
                allow_past=True,
                allow_future=False
            )
        )


    elif choice == 5:

        warning(
            "Edit cancelled."
        )

        return


    save_expenses(
        expenses
    )


    warn_if_over_budget(
        trip
    )


def delete_expense_workflow(
    trip
):

    info(
        "\n--- Delete Expense ---"
    )


    expense = select_expense(
        trip,
        "delete"
    )


    if expense is None:

        return


    print(
        "\nSelected Expense:"
    )


    print(
        f"{expense.title} | "
        f"{expense.category} | "
        f"{format_money(expense.amount)}"
    )


    if not get_yes_no(
        "Delete this expense? (y/n): "
    ):

        warning(
            "Delete cancelled."
        )

        return


    if delete_expense(
        expenses,
        trip.trip_id,
        expense.expense_id
    ):

        save_expenses(
            expenses
        )


def export_report_workflow(
    trip
):

    path = export_trip_to_csv(
        trip,
        expenses
    )


    if path is not None:

        success(
            f"Report saved to: {path}"
        )


def manage_trip_workflow():

    if not trips:

        warning(
            "No trips available."
        )

        return


    display_all_trips(
        trips,
        expenses
    )


    print(
        "\nEnter 0 to go back."
    )


    trip_id = (
        get_non_negative_int(
            "Enter trip ID: "
        )
    )


    if trip_id == 0:

        return


    trip = search_trip(
        trips,
        trip_id
    )


    if trip is None:

        error(
            "Trip not found."
        )

        return


    options = [
        "View Trip Details",
        "Update Trip",
        "Add Expense",
        "Edit Expense",
        "Delete Expense",
        "Trip Report",
        "Export Report (CSV)",
        "Check Trip Weather",
        "Delete Trip",
        "Back"
    ]


    while True:

        print_menu(
            f"{trip.city}, "
            f"{trip.country}",
            options
        )


        choice = get_menu_choice(
            "Enter your choice: ",
            1,
            len(
                options
            )
        )


        if choice == 1:

            display_trip_details(
                trip,
                expenses
            )


        elif choice == 2:

            update_trip_menu(
                trip
            )


        elif choice == 3:

            add_expense_workflow(
                trip
            )


        elif choice == 4:

            edit_expense_workflow(
                trip
            )


        elif choice == 5:

            delete_expense_workflow(
                trip
            )


        elif choice == 6:

            display_trip_report(
                trip,
                expenses
            )


        elif choice == 7:

            export_report_workflow(
                trip
            )


        elif choice == 8:

            display_weather_for_trip(
                trip
            )


        elif choice == 9:

            display_trip_details(
                trip,
                expenses
            )


            warning(
                "\nDeleting this trip "
                "will also delete "
                "all its expenses."
            )


            if not get_yes_no(
                "Delete this trip? (y/n): "
            ):

                warning(
                    "Delete cancelled."
                )

                continue


            if delete_trip(
                trips,
                expenses,
                trip.trip_id
            ):

                save_trips(
                    trips
                )

                save_expenses(
                    expenses
                )

                break


        elif choice == 10:

            break


def ai_recommendation_workflow():

    ai(
        "\n================================"
    )

    ai(
        "        AI TRAVEL PLANNER"
    )

    ai(
        "================================"
    )

    ai(
        "Gemini will use your answers "
        "to recommend destinations."
    )


    ai(
        "\nSTEP 1 - DEPARTURE LOCATION"
    )


    print(
        "Where are you traveling from?"
    )


    departure = (
        get_confirmed_location(
            "Departure Location",
            ai_mode=True
        )
    )


    if departure is None:

        return


    ai(
        "\nSTEP 2 - BUDGET"
    )


    budget = get_positive_float(
        "Enter your total budget (SAR): "
    )


    ai(
        "\nSTEP 3 - TRIP DURATION"
    )


    days = get_positive_int(
        "How many days do you "
        "want to travel? "
    )


    ai(
        "\nSTEP 4 - START DATE"
    )


    start_date = get_date(
        "Enter start date "
        "(YYYY-MM-DD): "
    )


    end_date = calculate_end_date(
        start_date,
        days
    )


    info(
        f"End date calculated "
        f"automatically: {end_date}"
    )


    weather_preference = (
        choose_from(
            "STEP 5 - WEATHER PREFERENCE",
            {
                1: "Cold",
                2: "Mild",
                3: "Warm",
                4: "No preference"
            },
            "Choose weather: "
        )
    )


    activity_preference = (
        choose_from(
            "STEP 6 - ACTIVITIES",
            {
                1: "Nature",
                2: "Shopping",
                3: "Culture and History",
                4: "Relaxation",
                5: "Adventure"
            },
            "Choose activity type: "
        )
    )


    travel_style = (
        choose_from(
            "STEP 7 - TRAVEL STYLE",
            {
                1: "Budget",
                2: "Comfortable",
                3: "Luxury"
            },
            "Choose travel style: "
        )
    )


    ai(
        "\nGemini is analyzing "
        "your travel preferences..."
    )


    ai(
        "Generating AI recommendations..."
    )


    info(
        "Budget fit is estimated "
        "and does not use live "
        "flight prices."
    )


    recommendations = (
        get_travel_recommendations(
            budget,
            days,
            start_date,
            end_date,
            departure[
                "city"
            ],
            departure[
                "country"
            ],
            weather_preference,
            activity_preference,
            travel_style
        )
    )


    if not recommendations:

        return


    display_ai_recommendations(
        recommendations
    )


    if not get_yes_no(
        "\nWould you like to create "
        "a trip from one of these "
        "AI recommendations? (y/n): "
    ):

        return


    selected = (
        select_ai_destination(
            recommendations
        )
    )


    if selected is None:

        warning(
            "Trip creation cancelled."
        )

        return


    display_selected_recommendation(
        selected
    )


    selected_city = selected.get(
        "city"
    )


    selected_country = selected.get(
        "country"
    )


    if (
        not selected_city
        or
        not selected_country
    ):

        error(
            "Invalid destination information."
        )

        return


    ai(
        "\nAI recommendation selected."
    )


    info(
        "Validating destination "
        "with location service..."
    )


    location = find_location(
        selected_city,
        selected_country
    )


    if location is None:

        error(
            "The AI recommendation "
            "could not be validated "
            "as a real location."
        )

        return


    city = location.get(
        "name",
        selected_city
    )


    country = location.get(
        "country",
        selected_country
    )


    print(
        "\nValidated Destination:"
    )


    print(
        f"{city}, {country}"
    )


    create_trip(
        trips,
        get_next_trip_id(
            trips
        ),
        country,
        city,
        start_date,
        end_date,
        budget
    )


    save_trips(
        trips
    )


    ai(
        "\nAI recommendation completed."
    )


    info(
        "Trip added to My Trips."
    )


def main():

    options = [
        "Create Trip",
        "My Trips",
        "Manage Trip",
        "AI Travel Planner",
        "Exit"
    ]


    while True:

        print_menu(
            "TRIPMATE",
            options
        )


        choice = get_menu_choice(
            "Enter your choice: ",
            1,
            len(
                options
            )
        )


        if choice == 1:

            create_trip_workflow()


        elif choice == 2:

            display_all_trips(
                trips,
                expenses
            )


        elif choice == 3:

            manage_trip_workflow()


        elif choice == 4:

            ai_recommendation_workflow()


        elif choice == 5:

            warning(
                "\nProgram ended."
            )

            break


if __name__ == "__main__":

    try:

        main()


    except (
        KeyboardInterrupt,
        EOFError
    ):

        print(
            "\n\nProgram ended."
        )