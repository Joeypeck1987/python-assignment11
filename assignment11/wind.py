"""Create an interactive scatter plot from Plotly's wind dataset."""

from pathlib import Path

import plotly.express as px
import plotly.data as pldata


def main():
    df = pldata.wind(return_type="pandas")
    print("First 10 rows:")
    print(df.head(10).to_string(index=False))
    print("\nLast 10 rows:")
    print(df.tail(10).to_string(index=False))

    # Preserve the original category for hover details.
    df["strength_category"] = df["strength"]
    # Represent ranges by their lower bound: '0-1' -> 0.0, '6+' -> 6.0.
    df["strength"] = (
        df["strength"]
        .str.replace(r"-.*$|\+$", "", regex=True)
        .astype(float)
    )

    fig = px.scatter(
        df,
        x="strength",
        y="frequency",
        color="direction",
        hover_data=["strength_category"],
        title="Wind Strength vs. Frequency by Direction",
        labels={
            "strength": "Wind Strength (Category Lower Bound)",
            "frequency": "Frequency",
            "direction": "Direction",
            "strength_category": "Original Strength Category",
        },
        template="plotly_white",
    )
    fig.update_traces(marker_size=9)
    output_path = Path(__file__).resolve().parent / "wind.html"
    fig.write_html(str(output_path), include_plotlyjs=True, auto_open=True)
    print(f"\nSaved interactive chart to {output_path}")


if __name__ == "__main__":
    main()
