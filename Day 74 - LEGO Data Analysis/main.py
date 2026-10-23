from pathlib import Path

import pandas as pd
import matplotlib

# Charts ko save karne ke liye non-interactive backend
matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def main():
    # 1. CSV files parhna
    sets = pd.read_csv(DATA_DIR / "sets.csv")
    colors = pd.read_csv(DATA_DIR / "colors.csv")
    themes = pd.read_csv(DATA_DIR / "themes.csv")

    print("\n===== DAY 74: LEGO DATA ANALYSIS =====")

    # 2. Data ka pehla jaiza
    print("\n1. LEGO sets ki pehli 5 rows:")
    print(sets.head().to_string(index=False))

    print("\n2. Sets ki information:")
    sets.info()

    print("\n3. Missing values:")
    print(sets.isnull().sum())

    # 3. Sab se purane sets
    print("\n4. Sab se purane 5 LEGO sets:")
    print(
        sets.sort_values(["year", "name"])
        [["name", "year", "num_parts"]]
        .head()
        .to_string(index=False)
    )

    # 4. Sab se zyada parts wale sets
    print("\n5. Sab se bare 5 sets:")
    print(
        sets.sort_values("num_parts", ascending=False)
        [["name", "year", "num_parts"]]
        .head()
        .to_string(index=False)
    )

    # 5. Har saal kitne sets release hue
    sets_per_year = sets.groupby("year")["set_num"].count()

    print("\n6. Har saal release hone wale sets:")
    print(sets_per_year.to_string())

    plt.figure(figsize=(10, 5))
    sets_per_year.plot(kind="line", marker="o")
    plt.title("Number of LEGO Sets Released by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Sets")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sets_per_year.png")
    plt.close()

    # 6. agg() se aik se zyada calculations
    print("\n7. Har saal sets ka summary:")
    yearly_summary = sets.groupby("year").agg(
        total_sets=("set_num", "count"),
        average_parts=("num_parts", "mean"),
        largest_set_parts=("num_parts", "max")
    )
    print(yearly_summary.round(2).to_string())
    yearly_summary.to_csv(BASE_DIR / "yearly_summary.csv")

    # 7. Do mukhtalif measurements ka chart
    yearly_parts = sets.groupby("year")["num_parts"].mean()
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(
        sets_per_year.index,
        sets_per_year.values,
        marker="o",
        label="Number of Sets"
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Number of Sets")

    ax2 = ax1.twinx()
    ax2.plot(
        yearly_parts.index,
        yearly_parts.values,
        marker="s",
        label="Average Parts"
    )
    ax2.set_ylabel("Average Parts per Set")
    plt.title("LEGO Sets and Average Parts by Year")
    fig.tight_layout()
    plt.savefig(CHART_DIR / "sets_and_parts.png")
    plt.close()

    # 8. Scatter plot: saal aur parts
    plt.figure(figsize=(10, 5))
    plt.scatter(sets["year"], sets["num_parts"])
    plt.title("Average Parts per LEGO Set: Individual Sets")
    plt.xlabel("Year")
    plt.ylabel("Number of Parts")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "parts_scatter.png")
    plt.close()

    # 9. Relational database: themes ko sets ke saath merge karna
    # sets.theme_id aur themes.id aik doosre se link hote hain
    merged = pd.merge(
        sets,
        themes,
        left_on="theme_id",
        right_on="id",
        how="left",
        suffixes=("_set", "_theme")
    )

    print("\n8. Themes ke saath merged data:")
    print(
        merged[["name_set", "year", "name_theme", "num_parts"]]
        .head(10)
        .to_string(index=False)
    )

    # 10. Theme ke mutabiq sets aur parts
    theme_summary = merged.groupby("name_theme").agg(
        total_sets=("set_num", "count"),
        total_parts=("num_parts", "sum"),
        average_parts=("num_parts", "mean")
    ).sort_values("total_sets", ascending=False)

    print("\n9. Theme ke mutabiq summary:")
    print(theme_summary.round(2).to_string())
    theme_summary.to_csv(BASE_DIR / "theme_summary.csv")

    plt.figure(figsize=(9, 5))
    theme_summary["total_sets"].plot(kind="bar")
    plt.title("Number of LEGO Sets by Theme")
    plt.xlabel("Theme")
    plt.ylabel("Number of Sets")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sets_by_theme.png")
    plt.close()

    # 11. Colors file ki exploration
    print("\n10. LEGO colors:")
    print(colors.head(10).to_string(index=False))
    print("\nTotal color records:", len(colors))
    print("Transparent colors:", (colors["is_trans"] == True).sum())

    # Output files save karna
    sets.to_csv(BASE_DIR / "cleaned_sets.csv", index=False)
    merged.to_csv(BASE_DIR / "sets_with_themes.csv", index=False)

    print("\n11. Charts charts folder mein save ho gaye.")
    print("12. Output CSV files bhi ban gayi hain.")
    print("\nProject successfully complete!")


if __name__ == "__main__":
    main()
