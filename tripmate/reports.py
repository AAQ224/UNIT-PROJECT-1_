from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from tripmate.colors import (
    warning
)

from tripmate.expenses import (
    get_trip_expenses,
    calculate_total_expenses
)


console = Console()


def display_all_trips(
    trips: list,
    expenses: list
):

    if not trips:

        warning(
            "No trips found."
        )

        return

    table = Table(
        title="My Trips",
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column(
        "ID",
        justify="center"
    )

    table.add_column(
        "Destination"
    )

    table.add_column(
        "Dates",
        justify="center"
    )

    table.add_column(
        "Budget",
        justify="right"
    )

    table.add_column(
        "Spent",
        justify="right"
    )

    table.add_column(
        "Remaining",
        justify="right"
    )

    table.add_column(
        "Used",
        justify="right"
    )


    for trip in trips:

        spent = calculate_total_expenses(
            expenses,
            trip.trip_id
        )

        remaining = (
            trip.budget - spent
        )

        percentage_used = (
            spent / trip.budget
        ) * 100


        if remaining < 0:

            remaining_text = (
                f"[red]"
                f"{remaining:,.2f} SAR"
                f"[/red]"
            )

        else:

            remaining_text = (
                f"[green]"
                f"{remaining:,.2f} SAR"
                f"[/green]"
            )


        if percentage_used >= 100:

            percentage_text = (
                f"[red]"
                f"{percentage_used:.1f}%"
                f"[/red]"
            )

        elif percentage_used >= 80:

            percentage_text = (
                f"[yellow]"
                f"{percentage_used:.1f}%"
                f"[/yellow]"
            )

        else:

            percentage_text = (
                f"[green]"
                f"{percentage_used:.1f}%"
                f"[/green]"
            )


        table.add_row(
            str(
                trip.trip_id
            ),

            f"{trip.city}, "
            f"{trip.country}",

            f"{trip.start_date}\n"
            f"{trip.end_date}",

            f"{trip.budget:,.2f} SAR",

            f"{spent:,.2f} SAR",

            remaining_text,

            percentage_text
        )


    console.print()

    console.print(
        table
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


    details = (
        f"[bold]Trip ID:[/bold] "
        f"{trip.trip_id}\n"

        f"[bold]Destination:[/bold] "
        f"{trip.city}, {trip.country}\n"

        f"[bold]Start Date:[/bold] "
        f"{trip.start_date}\n"

        f"[bold]End Date:[/bold] "
        f"{trip.end_date}\n\n"

        f"[bold]Budget:[/bold] "
        f"{trip.budget:,.2f} SAR\n"

        f"[bold]Spent:[/bold] "
        f"{total_spent:,.2f} SAR\n"

        f"[bold]Remaining:[/bold] "
        f"{remaining:,.2f} SAR\n"

        f"[bold]Budget Used:[/bold] "
        f"{percentage_used:.1f}%"
    )


    console.print()

    console.print(
        Panel(
            details,
            title="Trip Details",
            border_style="cyan"
        )
    )


    if remaining < 0:

        console.print(
            "[bold red]"
            "Warning: You are over budget!"
            "[/bold red]"
        )


    trip_expenses = get_trip_expenses(
        expenses,
        trip.trip_id
    )


    if not trip_expenses:

        console.print(
            "\n[yellow]"
            "No expenses recorded."
            "[/yellow]"
        )

        return


    table = Table(
        title="Expenses",
        header_style="bold cyan"
    )

    table.add_column(
        "ID",
        justify="center"
    )

    table.add_column(
        "Title"
    )

    table.add_column(
        "Category"
    )

    table.add_column(
        "Amount",
        justify="right"
    )


    for expense in trip_expenses:

        table.add_row(
            str(
                expense["expense_id"]
            ),

            expense["title"],

            expense["category"],

            f"{expense['amount']:,.2f} SAR"
        )


    console.print()

    console.print(
        table
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


    summary_table = Table(
        title="Trip Report",
        header_style="bold cyan"
    )

    summary_table.add_column(
        "Destination"
    )

    summary_table.add_column(
        "Budget",
        justify="right"
    )

    summary_table.add_column(
        "Spent",
        justify="right"
    )

    summary_table.add_column(
        "Remaining",
        justify="right"
    )

    summary_table.add_column(
        "Used",
        justify="right"
    )


    summary_table.add_row(
        f"{trip.city}, "
        f"{trip.country}",

        f"{trip.budget:,.2f} SAR",

        f"{total_spent:,.2f} SAR",

        f"{remaining:,.2f} SAR",

        f"{percentage_used:.1f}%"
    )


    console.print()

    console.print(
        summary_table
    )


    if not trip_expenses:

        console.print(
            "\n[yellow]"
            "No expenses available "
            "for analysis."
            "[/yellow]"
        )

        return


    highest_expense = max(
        trip_expenses,
        key=lambda expense: expense["amount"]
    )


    category_totals = {}

    for expense in trip_expenses:

        category = expense[
            "category"
        ]

        if category not in category_totals:

            category_totals[
                category
            ] = 0

        category_totals[
            category
        ] += expense[
            "amount"
        ]


    category_table = Table(
        title="Expense Breakdown",
        header_style="bold cyan"
    )

    category_table.add_column(
        "Category"
    )

    category_table.add_column(
        "Amount",
        justify="right"
    )


    for category, amount in (
        category_totals.items()
    ):

        category_table.add_row(
            category,
            f"{amount:,.2f} SAR"
        )


    console.print()

    console.print(
        category_table
    )


    highest_category = max(
        category_totals,
        key=category_totals.get
    )


    console.print(
        Panel(
            (
                f"[bold]Highest Expense:[/bold]\n"
                f"{highest_expense['title']} - "
                f"{highest_expense['amount']:,.2f} SAR"
                f"\n\n"
                f"[bold]Highest Spending Category:[/bold]\n"
                f"{highest_category} - "
                f"{category_totals[highest_category]:,.2f} SAR"
            ),
            title="Highlights",
            border_style="cyan"
        )
    )


    if percentage_used >= 100:

        console.print(
            "[bold red]"
            "You have exceeded your budget."
            "[/bold red]"
        )

    elif percentage_used >= 80:

        console.print(
            "[bold yellow]"
            "You have used more than "
            "80% of your budget."
            "[/bold yellow]"
        )