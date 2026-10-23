from pathlib import Path

import pandas as pd
import matplotlib

# Charts ko screen par kholne ke bajaye files mein save karein
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def load_time_series(filename, date_column="Date"):
    """CSV parhein aur date column ko datetime mein badlein."""
    df = pd.read_csv(DATA_DIR / filename)
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=[date_column])
    df = df.sort_values(date_column)
    return df


def main():
    print("\n===== DAY 75: TIME SERIES DATA VISUALIZATION =====")

    # 1. Google Search data explore karna
    google = load_time_series(
        "google_trends.csv",
        date_column="Month"
    )

    print("\n1. Google Search data ki pehli rows:")
    print(google.head().to_string(index=False))
    print("\nGoogle data ki missing values:")
    print(google.isnull().sum())

    # 2. Time series resampling
    # Resampling se data ko doosri time frequency mein jama karte hain.
    google = google.set_index("Month")
    monthly_google = google["Google Search Interest"].resample("ME").mean()

    print("\n2. Month ke mutabiq Google Search interest:")
    print(monthly_google.to_string())

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_google.index, monthly_google.values, marker="o")
    plt.title("Google Search Interest Over Time")
    plt.xlabel("Month")
    plt.ylabel("Search Interest (Sample Index)")
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "google_search_trends.png")
    plt.close()

    # 3. Tesla line chart
    tesla = load_time_series("tesla.csv")
    print("\n3. Tesla sample data:")
    print(tesla.head().to_string(index=False))

    plt.figure(figsize=(10, 5))
    plt.plot(
        tesla["Date"],
        tesla["Close"],
        linestyle="-",
        marker="o",
        label="Tesla"
    )
    plt.title("Tesla Stock Price Over Time (Sample Data)")
    plt.xlabel("Date")
    plt.ylabel("Price (Illustrative USD)")
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "tesla_line_chart.png")
    plt.close()

    # 4. Bitcoin line chart with style and markers
    bitcoin = load_time_series("bitcoin.csv")

    print("\n4. Bitcoin sample data:")
    print(bitcoin.head().to_string(index=False))

    plt.figure(figsize=(10, 5))
    plt.plot(
        bitcoin["Date"],
        bitcoin["Price"],
        linestyle="--",
        marker="s",
        label="Bitcoin"
    )
    plt.title("Bitcoin Price Over Time (Sample Data)")
    plt.xlabel("Date")
    plt.ylabel("Price (Illustrative USD)")
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "bitcoin_line_chart.png")
    plt.close()

    # 5. Unemployment data and grid
    unemployment = load_time_series("unemployment.csv")
    print("\n5. Unemployment sample data:")
    print(unemployment.head().to_string(index=False))

    plt.figure(figsize=(10, 5))
    plt.plot(
        unemployment["Date"],
        unemployment["Unemployment Rate"],
        marker="o",
        linestyle="-",
        label="Unemployment Rate"
    )
    plt.title("Unemployment Rate Over Time (Sample Data)")
    plt.xlabel("Date")
    plt.ylabel("Rate (%)")
    plt.legend()
    plt.grid(True, which="major", linestyle=":")
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "unemployment_chart.png")
    plt.close()

    # 6. Naye data ka asar: pehle 6 aur tamam months ka muqabla
    first_half = unemployment.head(6)["Unemployment Rate"].mean()
    full_period = unemployment["Unemployment Rate"].mean()

    print("\n6. Unemployment rate ka muqabla:")
    print(f"First 6 months average: {first_half:.2f}%")
    print(f"All months average: {full_period:.2f}%")

    # 7. Rolling average se short-term changes smooth karna
    unemployment["Rolling Average"] = (
        unemployment["Unemployment Rate"].rolling(window=3).mean()
    )

    print("\n7. 3-month rolling average:")
    print(
        unemployment[["Date", "Unemployment Rate", "Rolling Average"]]
        .round(2)
        .to_string(index=False)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        unemployment["Date"],
        unemployment["Unemployment Rate"],
        marker="o",
        label="Monthly Rate"
    )
    plt.plot(
        unemployment["Date"],
        unemployment["Rolling Average"],
        linestyle="--",
        marker="s",
        label="3-Month Average"
    )
    plt.title("Unemployment Rate: Monthly and Smoothed")
    plt.xlabel("Date")
    plt.ylabel("Rate (%)")
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "unemployment_rolling_average.png")
    plt.close()

    # Cleaned data save karna
    google.to_csv(BASE_DIR / "cleaned_google_trends.csv")
    tesla.to_csv(BASE_DIR / "cleaned_tesla.csv", index=False)
    bitcoin.to_csv(BASE_DIR / "cleaned_bitcoin.csv", index=False)
    unemployment.to_csv(BASE_DIR / "cleaned_unemployment.csv", index=False)

    print("\n8. Charts aur cleaned CSV files save ho gayi hain.")
    print("Charts folder:", CHART_DIR)
    print("\nProject successfully complete!")


if __name__ == "__main__":
    main()
