"""Display cumulative order revenue using a Pandas line plot."""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter


def main():
    database_path = Path(__file__).resolve().parent.parent / "db" / "lesson.db"
    if not database_path.is_file():
        raise FileNotFoundError(f"Database not found: {database_path}")

    query = """
        SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
        FROM orders o
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id;
    """

    with sqlite3.connect(database_path) as connection:
        df = pd.read_sql_query(query, connection)

    # Each value includes this order's revenue and all preceding orders.
    df["cumulative"] = df["total_price"].cumsum()

    ax = df.plot(
        x="order_id",
        y="cumulative",
        kind="line",
        color="steelblue",
        title="Cumulative Revenue by Order",
        legend=False,
        figsize=(10, 6),
    )
    ax.set_xlabel("Order ID")
    ax.set_ylabel("Cumulative Revenue")
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
