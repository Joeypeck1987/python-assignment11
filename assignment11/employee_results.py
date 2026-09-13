"""Load employee revenue from SQLite and display a Pandas bar chart."""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter


def main():
    # Locate ../db/lesson.db relative to this file in assignment11.
    database_path = Path(__file__).resolve().parent.parent / "db" / "lesson.db"
    if not database_path.is_file():
        raise FileNotFoundError(
            f"Database not found: {database_path}. "
            "Copy the db folder from python_homework to python-assignment11."
        )

    query = """
        SELECT last_name, SUM(price * quantity) AS revenue
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY e.employee_id;
    """

    with sqlite3.connect(database_path) as connection:
        employee_results = pd.read_sql_query(query, connection)

    ax = employee_results.plot(
        x="last_name",
        y="revenue",
        kind="bar",
        color="steelblue",
        title="Total Revenue by Employee",
        legend=False,
        figsize=(10, 6),
        rot=45,
    )
    ax.set_xlabel("Employee Last Name")
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
