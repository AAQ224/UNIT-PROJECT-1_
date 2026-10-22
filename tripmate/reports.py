from tripmate.colors import (
    info,
    warning
)

from tripmate.expenses import (
    get_trip_expenses,
    calculate_total_expenses
)


def display_all_trips(
    trips: list,
    expenses: list
):

    if not trips:

        warning(
            "No trips found."
        )

        return

    info(
        "\n================================"
    )

    info(
        "            MY TRIPS"
    )

    info(
        "================================"
    )

    for trip in trips:

        spent = calculate_total_expenses(
            expenses,
            trip.trip_id
        )

        remaining = (
            trip.budget - spent
        )

        print(
            f"\nID: {trip.trip_id} | "
            f"{trip.city}, {trip.country}"
        )

        print(
            f"Budget: "
            f"{trip.budget:,.2f} SAR"
        )

        print(
            f"Spent: "
            f"{spent:,.2f} SAR"
        )

        print(
            f"Remaining: "
            f"{remaining:,.2f} SAR"
        )

        print(
            "--------------------------------"
        )


def display_trip_details(
    trip,
    expenses: list
):

    total_spent = (
        calculate_total_expenses(
            expenses,
            trip.trip_id
        )
    )

    remaining = (
        trip.budget - total_spent
    )

    percentage_used = (
        total_spent / trip.budget
    ) * 100

    info(
        "\n================================"
    )

    info(
        "          TRIP DETAILS"
    )

    info(
        "================================"
    )

    print(
        f"Trip ID: {trip.trip_id}"
    )

    print(
        f"Destination: "
        f"{trip.city}, {trip.country}"
    )

    print(
        f"Start Date: "
        f"{trip.start_date}"
    )

    print(
        f"End Date: "
        f"{trip.end_date}"
    )

    print()

    print(
        f"Budget:    "
        f"{trip.budget:,.2f} SAR"
    )

    print(
        f"Spent:     "
        f"{total_spent:,.2f} SAR"
    )

    print(
        f"Remaining: "
        f"{remaining:,.2f} SAR"
    )

    print(
        f"Used:      "
        f"{percentage_used:.1f}%"
    )

    if remaining < 0:

        warning(
            "\nWarning: You are over budget!"
        )

    trip_expenses = get_trip_expenses(
        expenses,
        trip.trip_id
    )

    print(
        "\nExpenses:"
    )

    print(
        "--------------------------------"
    )

    if not trip_expenses:

        print(
            "No expenses recorded."
        )

        return

    for expense in trip_expenses:

        print(
            f"#{expense['expense_id']} | "
            f"{expense['title']}"
        )

        print(
            f"Category: "
            f"{expense['category']}"
        )

        print(
            f"Amount: "
            f"{expense['amount']:,.2f} SAR"
        )

        print(
            "--------------------------------"
        )


def display_trip_report(
    trip,
    expenses: list
):

    trip_expenses = get_trip_expenses(
        expenses,
        trip.trip_id
    )

    total_spent = (
        calculate_total_expenses(
            expenses,
            trip.trip_id
        )
    )

    remaining = (
        trip.budget - total_spent
    )

    percentage_used = (
        total_spent / trip.budget
    ) * 100

    info(
        "\n================================"
    )

    info(
        "           TRIP REPORT"
    )

    info(
        "================================"
    )

    print(
        f"Destination: "
        f"{trip.city}, {trip.country}"
    )

    print(
        f"Budget: "
        f"{trip.budget:,.2f} SAR"
    )

    print(
        f"Total Spent: "
        f"{total_spent:,.2f} SAR"
    )

    print(
        f"Remaining: "
        f"{remaining:,.2f} SAR"
    )

    print(
        f"Budget Used: "
        f"{percentage_used:.1f}%"
    )

    if not trip_expenses:

        print(
            "\nNo expenses available "
            "for analysis."
        )

        return

    highest_expense = max(
        trip_expenses,
        key=lambda expense: expense["amount"]
    )

    print(
        "\nHighest Expense:"
    )

    print(
        f"{highest_expense['title']} - "
        f"{highest_expense['amount']:,.2f} SAR"
    )

    category_totals = {}

    for expense in trip_expenses:

        category = expense["category"]

        if category not in category_totals:

            category_totals[
                category
            ] = 0

        category_totals[
            category
        ] += expense["amount"]

    print(
        "\nExpense Breakdown:"
    )

    for category, amount in (
        category_totals.items()
    ):

        print(
            f"{category}: "
            f"{amount:,.2f} SAR"
        )

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    print(
        "\nHighest Spending Category:"
    )

    print(
        f"{highest_category} - "
        f"{category_totals[highest_category]:,.2f} SAR"
    )

    if percentage_used >= 100:

        warning(
            "\nYou have exceeded "
            "your budget."
        )

    elif percentage_used >= 80:

        warning(
            "\nYou have used more than "
            "80% of your budget."
        )