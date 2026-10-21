from tripmate.colors import (
    success,
    error
)


def generate_expense_id(expenses: list):

    if not expenses:
        return 1

    highest_id = 0

    for expense in expenses:

        if expense["expense_id"] > highest_id:
            highest_id = expense["expense_id"]

    return highest_id + 1


def add_expense(
    expenses: list,
    trip_id: int,
    title: str,
    category: str,
    amount: float
):

    expense_id = generate_expense_id(expenses)

    expense = {
        "expense_id": expense_id,
        "trip_id": trip_id,
        "title": title,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    success("\nExpense added successfully.")
    success(f"Expense ID: {expense_id}")


def display_trip_expenses(
    expenses: list,
    trip_id: int
):

    trip_expenses = []

    for expense in expenses:

        if expense["trip_id"] == trip_id:
            trip_expenses.append(expense)

    if not trip_expenses:
        error("No expenses found for this trip.")
        return

    print("\n========================")
    print("      TRIP EXPENSES")
    print("========================")

    for expense in trip_expenses:

        print(
            f"Expense ID: {expense['expense_id']}"
        )

        print(
            f"Title: {expense['title']}"
        )

        print(
            f"Category: {expense['category']}"
        )

        print(
            f"Amount: {expense['amount']:.2f} SAR"
        )

        print("------------------------")


def delete_expense(
    expenses: list,
    expense_id: int
):

    for expense in expenses:

        if expense["expense_id"] == expense_id:

            expenses.remove(expense)

            success("Expense deleted successfully.")

            return

    error("Expense not found.")