from tripmate.colors import (
    success,
    error
)


EXPENSE_CATEGORIES = [
    "Accommodation",
    "Transport",
    "Food",
    "Activities",
    "Shopping",
    "Other"
]


def add_expense(
    expenses: list,
    expense_id: int,
    trip_id: int,
    title: str,
    category: str,
    amount: float
):

    expense = {
        "expense_id": expense_id,
        "trip_id": trip_id,
        "title": title,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    success(
        "\nExpense added successfully."
    )

    success(
        f"Expense ID: {expense_id}"
    )


def get_trip_expenses(
    expenses: list,
    trip_id: int
):

    trip_expenses = []

    for expense in expenses:

        if expense["trip_id"] == trip_id:

            trip_expenses.append(
                expense
            )

    return trip_expenses


def get_expense(
    expenses: list,
    trip_id: int,
    expense_id: int
):

    for expense in expenses:

        if (
            expense["trip_id"] == trip_id
            and
            expense["expense_id"] == expense_id
        ):

            return expense

    return None


def calculate_total_expenses(
    expenses: list,
    trip_id: int
):

    total = 0

    for expense in expenses:

        if expense["trip_id"] == trip_id:

            total += expense["amount"]

    return total


def display_trip_expenses(
    expenses: list,
    trip_id: int
):

    trip_expenses = get_trip_expenses(
        expenses,
        trip_id
    )

    if not trip_expenses:

        print(
            "No expenses recorded "
            "for this trip."
        )

        return False

    print(
        "\n--------------------------------"
    )

    print(
        "            EXPENSES"
    )

    print(
        "--------------------------------"
    )

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

    return True


def delete_expense(
    expenses: list,
    trip_id: int,
    expense_id: int
):

    expense = get_expense(
        expenses,
        trip_id,
        expense_id
    )

    if expense is None:

        error(
            "Expense not found "
            "for this trip."
        )

        return False

    expenses.remove(
        expense
    )

    success(
        "Expense deleted successfully."
    )

    return True