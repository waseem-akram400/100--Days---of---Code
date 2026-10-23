from pathlib import Path

import pandas as pd
import matplotlib

# Charts ko file mein save karne ke liye
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Project ke folders ke paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "language_data.csv"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def main():
    # 1. CSV file parhna
    df = pd.read_csv(DATA_FILE)

    print("\n===== DAY 73: PROGRAMMING LANGUAGE ANALYSIS =====")
    print("\n1. Pehli 5 rows:")
    print(df.head().to_string(index=False))

    # 2. Data ki basic information
    print("\n2. Data ki information:")
    print(df.info())

    print("\n3. Missing values:")
    print(df.isnull().sum())

    # 3. Date column ko asal date format mein badalna
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Zaroori columns mein missing values wali rows hata dein
    df = df.dropna(subset=["date", "tag", "posts"]).copy()

    # Posts ko number mein convert karna
    df["posts"] = pd.to_numeric(df["posts"], errors="coerce")
    df = df.dropna(subset=["posts"]).copy()

    print("\n4. Safai ke baad total records:", len(df))
    print("Date range:", df["date"].min(), "se", df["date"].max())

    # 4. Har programming language ke total posts
    language_totals = (
        df.groupby("tag")["posts"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n5. Har language ke total posts:")
    print(language_totals.to_string())

    # Bar chart
    plt.figure(figsize=(9, 5))
    language_totals.plot(kind="bar")
    plt.title("Total Posts by Programming Language")
    plt.xlabel("Programming Language")
    plt.ylabel("Total Posts")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "language_totals.png")
    plt.close()

    # 5. DataFrame ko pivot karna
    pivot_df = df.pivot_table(
        index="date",
        columns="tag",
        values="posts",
        aggfunc="sum"
    ).sort_index()

    print("\n6. Pivot table:")
    print(pivot_df.to_string())

    pivot_df.to_csv(BASE_DIR / "pivoted_language_data.csv")

    # 6. Multi-line chart: waqt ke saath posts
    plt.figure(figsize=(11, 6))
    for language in pivot_df.columns:
        plt.plot(
            pivot_df.index,
            pivot_df[language],
            marker="o",
            label=language
        )

    plt.title("Programming Language Posts Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "language_trends.png")
    plt.close()

    # 7. Moving average: data ke utar charhao ko smooth karna
    rolling_df = pivot_df.rolling(window=3, min_periods=1).mean()

    print("\n7. 3-period moving average ki aakhri 5 rows:")
    print(rolling_df.tail().round(2).to_string())

    plt.figure(figsize=(11, 6))
    for language in rolling_df.columns:
        plt.plot(
            rolling_df.index,
            rolling_df[language],
            marker="o",
            label=language
        )

    plt.title("Smoothed Programming Language Trends")
    plt.xlabel("Date")
    plt.ylabel("3-Period Moving Average")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "smoothed_trends.png")
    plt.close()

    # 8. Har language ka aakhri aur pehla record compare karna
    comparison = pd.DataFrame({
        "First Posts": pivot_df.iloc[0],
        "Latest Posts": pivot_df.iloc[-1],
    })
    comparison["Change"] = (
        comparison["Latest Posts"] - comparison["First Posts"]
    )

    print("\n8. Pehle aur aakhri record ka muqabla:")
    print(comparison.sort_values("Change", ascending=False).to_string())

    comparison.to_csv(BASE_DIR / "language_comparison.csv")

    # Saaf kiya hua data save karna
    df.to_csv(BASE_DIR / "cleaned_language_data.csv", index=False)

    print("\n9. Charts yahan save hue:", CHART_DIR)
    print(" - language_totals.png")
    print(" - language_trends.png")
    print(" - smoothed_trends.png")
    print("\nProject successfully complete!")


if __name__ == "__main__":
    main()
