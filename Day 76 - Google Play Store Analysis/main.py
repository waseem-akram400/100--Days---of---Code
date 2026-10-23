from pathlib import Path
import re

import pandas as pd
import plotly.express as px

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "google_play_apps.csv"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def convert_installs(value):
    """'1,000,000+' jaisi text value ko number mein badlein."""
    if pd.isna(value):
        return None
    digits = re.sub(r"[^0-9]", "", str(value))
    return int(digits) if digits else None


def convert_size(value):
    """App size ko MB mein convert karein."""
    if pd.isna(value):
        return None

    value = str(value).strip().upper()
    if value in {"", "NAN", "VARIES WITH DEVICE"}:
        return None

    try:
        if value.endswith("K"):
            return float(value[:-1]) / 1024
        if value.endswith("M"):
            return float(value[:-1])
        if value.endswith("G"):
            return float(value[:-1]) * 1024
        return float(value)
    except ValueError:
        return None


def save_chart(fig, filename):
    """Interactive Plotly chart ko HTML file mein save karein."""
    output = CHART_DIR / filename
    fig.write_html(output, include_plotlyjs=True)
    print(f"Chart saved: {output.name}")


def main():
    print("\n===== DAY 76: GOOGLE PLAY STORE DATA ANALYSIS =====")

    # 1. CSV data read karna
    df = pd.read_csv(DATA_FILE)

    print("\n1. Pehli 5 rows:")
    print(df.head().to_string(index=False))

    print("\n2. Dataset ka size:", df.shape)
    print("\n3. Missing values:")
    print(df.isnull().sum().to_string())

    # 2. Duplicate records remove karna
    before = len(df)
    df = df.drop_duplicates().copy()
    print(f"\n4. Duplicate rows removed: {before - len(df)}")

    # 3. Zaroori numeric columns clean karna
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df["Installs"] = df["Installs"].apply(convert_installs)
    df["Size_MB"] = df["Size"].apply(convert_size)

    # Price mein dollar sign ho sakta hai
    df["Price"] = (
        df["Price"].astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # Missing app names/categories wale records remove karna
    df = df.dropna(subset=["App", "Category"]).copy()

    print("\n5. Cleaning ke baad rows:", len(df))
    print("\n6. Numeric columns ki types:")
    print(df[["Rating", "Reviews", "Installs", "Size_MB", "Price"]].dtypes)

    # 4. Highest rated apps
    print("\n7. Sab se zyada rating wali apps:")
    print(
        df.dropna(subset=["Rating"])
        .sort_values(["Rating", "Reviews"], ascending=False)
        [["App", "Rating", "Reviews"]]
        .head(5)
        .to_string(index=False)
    )

    # 5. Most reviewed apps
    print("\n8. Sab se zyada reviews wali apps:")
    print(
        df.sort_values("Reviews", ascending=False)
        [["App", "Reviews"]]
        .head(5)
        .to_string(index=False)
    )

    # 6. Largest apps by size
    print("\n9. Sab se bari apps (MB):")
    print(
        df.dropna(subset=["Size_MB"])
        .sort_values("Size_MB", ascending=False)
        [["App", "Size_MB"]]
        .head(5)
        .to_string(index=False)
    )

    # 7. Category pie chart
    category_counts = df["Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "App Count"]

    fig = px.pie(
        category_counts,
        names="Category",
        values="App Count",
        title="Apps by Category"
    )
    save_chart(fig, "category_pie_chart.html")

    # 8. Free vs paid donut chart
    type_counts = df["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "App Count"]

    fig = px.pie(
        type_counts,
        names="Type",
        values="App Count",
        hole=0.45,
        title="Free vs Paid Apps"
    )
    save_chart(fig, "free_paid_donut_chart.html")

    # 9. Installs aur reviews ko category ke mutabiq summarize karna
    category_summary = df.groupby("Category", as_index=False).agg(
        App_Count=("App", "count"),
        Total_Installs=("Installs", "sum"),
        Average_Rating=("Rating", "mean"),
        Total_Reviews=("Reviews", "sum")
    )

    print("\n10. Category summary:")
    print(
        category_summary.sort_values("Total_Installs", ascending=False)
        .round(2)
        .to_string(index=False)
    )
    category_summary.to_csv(BASE_DIR / "category_summary.csv", index=False)

    # 10. Sab se popular categories ka bar chart
    popular = category_summary.nlargest(10, "Total_Installs")
    fig = px.bar(
        popular,
        x="Category",
        y="Total_Installs",
        title="Most Popular Categories by Installs",
        labels={"Total_Installs": "Total Installs"}
    )
    fig.update_layout(xaxis_tickangle=-35)
    save_chart(fig, "popular_categories_bar.html")

    # 11. Category ke mutabiq average rating aur reviews
    competitive = category_summary.dropna(
        subset=["Average_Rating", "Total_Reviews"]
    )
    fig = px.scatter(
        competitive,
        x="Total_Reviews",
        y="Average_Rating",
        size="App_Count",
        hover_name="Category",
        title="Category Ratings vs Reviews",
        labels={
            "Total_Reviews": "Total Reviews",
            "Average_Rating": "Average Rating"
        }
    )
    save_chart(fig, "category_scatter_plot.html")

    # 12. Nested category/type data ko stack karna
    cross_tab = pd.crosstab(df["Category"], df["Type"])
    print("\n11. Category aur app type ka cross-tab:")
    print(cross_tab.to_string())

    stacked = cross_tab.stack().reset_index()
    stacked.columns = ["Category", "Type", "App_Count"]
    stacked.to_csv(BASE_DIR / "category_type_stacked.csv", index=False)

    print("\n12. .stack() se hasil data:")
    print(stacked.head(10).to_string(index=False))

    # 13. Grouped bar chart: free aur paid apps
    fig = px.bar(
        stacked,
        x="Category",
        y="App_Count",
        color="Type",
        barmode="group",
        title="Free and Paid Apps by Category"
    )
    fig.update_layout(xaxis_tickangle=-35)
    save_chart(fig, "grouped_category_bar.html")

    # 14. Box plot: category-wise ratings
    ratings = df.dropna(subset=["Rating"])
    fig = px.box(
        ratings,
        x="Category",
        y="Rating",
        title="App Ratings by Category",
        points="all"
    )
    fig.update_layout(xaxis_tickangle=-35)
    save_chart(fig, "category_box_plot.html")

    # 15. Cleaned data save karna
    df.to_csv(BASE_DIR / "cleaned_apps.csv", index=False)

    print("\n13. Cleaned data aur summary CSV files save ho gayi hain.")
    print("Charts folder:", CHART_DIR)
    print("\nProject successfully complete!")


if __name__ == "__main__":
    main()
