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
    get_date,
    calculate_end_date,
    get_expense_category
)

from tripmate.colors import (
    error,
    warning,
    info,
    ai
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
    display_weather_for_trip,
    find_location
)

from tripmate.ai_helper import (
    correct_location_name,
    get_travel_recommendations,
    display_ai_recommendations,
    display_selected_recommendation,
    select_ai_destination
)


trips = load_trips()
expenses = load_expenses()


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


        if ai_mode:

            ai(
                "\nAI is checking and correcting "
                "the location..."
            )

        else:

            info(
                "\nChecking location..."
            )


        corrected = (
            correct_location_name(
                city,
                country
            )
        )


        corrected_city = (
            corrected["city"]
        )

        corrected_country = (
            corrected["country"]
        )


        location = find_location(
            corrected_city,
            corrected_country
        )


        if location is None:

            error(
                "Could not find this location."
            )


            retry = get_yes_no(
                "Try again? (y/n): "
            )


            if retry:

                continue


            return None


        location_city = location.get(
            "name",
            corrected_city
        )

        location_country = location.get(
            "country",
            corrected_country
        )


        print(
            "\nDid you mean:"
        )

        print(
            f"{location_city}, "
            f"{location_country}"
        )


        confirmed = get_yes_no(
            "Use this location? (y/n): "
        )


        if confirmed:

            return {
                "city": location_city,
                "country": location_country
            }


        warning(
            "Please enter the location again."
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


    trip_id = (
        get_next_trip_id()
    )


    create_trip(
        trips,
        trip_id,
        destination["country"],
        destination["city"],
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

        print(
            "\n--- Update Trip ---"
        )

        print(
            "1. Destination"
        )

        print(
            "2. Dates"
        )

        print(
            "3. Budget"
        )

        print(
            "4. Back"
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
                destination["country"]
            )

            update_city(
                trip,
                destination["city"]
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

            return


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


def delete_expense_workflow(
    trip
):

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

        return


    display_trip_expenses(
        expenses,
        trip.trip_id
    )


    expense_id = (
        get_positive_int(
            "Enter expense ID to delete: "
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

        return


    print(
        "\nSelected Expense:"
    )

    print(
        f"{expense['title']} | "
        f"{expense['category']} | "
        f"{expense['amount']:,.2f} SAR"
    )


    confirm = get_yes_no(
        "Delete this expense? (y/n): "
    )


    if not confirm:

        warning(
            "Delete cancelled."
        )

        return


    deleted = delete_expense(
        expenses,
        trip.trip_id,
        expense_id
    )


    if deleted:

        save_expenses(
            expenses
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


        choice = get_menu_choice(
            "Enter your choice: ",
            1,
            8
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

            delete_expense_workflow(
                trip
            )


        elif choice == 5:

            display_trip_report(
                trip,
                expenses
            )


        elif choice == 6:

            display_weather_for_trip(
                trip
            )


        elif choice == 7:

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


        elif choice == 8:

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
        "How many days do you want "
        "to travel? "
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
        f"End date calculated automatically: "
        f"{end_date}"
    )


    ai(
        "\nSTEP 5 - WEATHER PREFERENCE"
    )

    print(
        "1. Cold"
    )

    print(
        "2. Mild"
    )

    print(
        "3. Warm"
    )

    print(
        "4. No Preference"
    )


    weather_choice = (
        get_menu_choice(
            "Choose weather: ",
            1,
            4
        )
    )


    weather_options = {
        1: "Cold",
        2: "Mild",
        3: "Warm",
        4: "No preference"
    }


    weather_preference = (
        weather_options[
            weather_choice
        ]
    )


    ai(
        "\nSTEP 6 - ACTIVITIES"
    )

    print(
        "1. Nature"
    )

    print(
        "2. Shopping"
    )

    print(
        "3. Culture and History"
    )

    print(
        "4. Relaxation"
    )

    print(
        "5. Adventure"
    )


    activity_choice = (
        get_menu_choice(
            "Choose activity type: ",
            1,
            5
        )
    )


    activity_options = {
        1: "Nature",
        2: "Shopping",
        3: "Culture and History",
        4: "Relaxation",
        5: "Adventure"
    }


    activity_preference = (
        activity_options[
            activity_choice
        ]
    )


    ai(
        "\nSTEP 7 - TRAVEL STYLE"
    )

    print(
        "1. Budget"
    )

    print(
        "2. Comfortable"
    )

    print(
        "3. Luxury"
    )


    style_choice = (
        get_menu_choice(
            "Choose travel style: ",
            1,
            3
        )
    )


    styles = {
        1: "Budget",
        2: "Comfortable",
        3: "Luxury"
    }


    travel_style = (
        styles[
            style_choice
        ]
    )


    ai(
        "\nGemini is analyzing your "
        "travel preferences..."
    )

    ai(
        "Generating AI recommendations..."
    )


    recommendations = (
        get_travel_recommendations(
            budget,
            days,
            start_date,
            end_date,
            departure["city"],
            departure["country"],
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


    create_from_ai = get_yes_no(
        "\nWould you like to create a trip "
        "from one of these AI recommendations? "
        "(y/n): "
    )


    if not create_from_ai:

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
            "The AI recommendation could not "
            "be validated as a real location."
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


    trip_id = (
        get_next_trip_id()
    )


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


    ai(
        "\nAI recommendation completed."
    )

    info(
        "Trip added to My Trips."
    )


def main():

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
            "4. AI Travel Planner"
        )

        print(
            "5. Exit"
        )


        choice = get_menu_choice(
            "Enter your choice: ",
            1,
            5
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

    main()