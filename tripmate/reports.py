from tripmate.colors import (
    info,
    warning
)

from tripmate.expenses import (
    get_trip_expenses,
    calculate_total_expenses,
    EXPENSE_CATEGORIES
)


def display_trip_details(
    trip,
    expenses: list
):

    total_spent = calculate_total_expenses(
        expenses,
        trip.trip_id
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
        f"Start Date: {trip.start_date}"
    )

    print(
        f"End Date: {trip.end_date}"
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

    print("\nExpenses:")
    print("--------------------------------")

    if not trip_expenses:

        print(
            "No expenses recorded."
        )

        return

    for expense in trip_expenses:

        print(
            f"#{expense['expense_id']} "
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

        print("--------------------------------")


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


def display_trip_report(
    trip,
    expenses: list
):

    trip_expenses = get_trip_expenses(
        expenses,
        trip.trip_id
    )

    total_spent = calculate_total_expenses(
        expenses,
        trip.trip_id
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

    highest_expense = trip_expenses[0]

    for expense in trip_expenses:

        if (
            expense["amount"]
            >
            highest_expense["amount"]
        ):

            highest_expense = expense

    print("\nHighest Expense:")

    print(
        f"{highest_expense['title']} - "
        f"{highest_expense['amount']:,.2f} SAR"
    )

    print("\nExpense Breakdown:")

    highest_category = None
    highest_category_total = 0

    for category in EXPENSE_CATEGORIES:

        category_total = 0

        for expense in trip_expenses:

            if (
                expense["category"]
                == category
            ):

                category_total += (
                    expense["amount"]
                )

        if category_total > 0:

            print(
                f"{category}: "
                f"{category_total:,.2f} SAR"
            )

        if (
            category_total
            >
            highest_category_total
        ):

            highest_category_total = (
                category_total
            )

            highest_category = (
                category
            )

    if highest_category is not None:

        print(
            "\nHighest Spending Category:"
        )

        print(
            f"{highest_category} - "
            f"{highest_category_total:,.2f} SAR"
        )

    if percentage_used >= 100:

        warning(
            "\nYou have exceeded your budget."
        )

    elif percentage_used >= 80:

        warning(
            "\nYou have used more than "
            "80% of your budget."
        )