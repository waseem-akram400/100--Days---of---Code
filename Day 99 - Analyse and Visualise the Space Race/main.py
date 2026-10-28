
from pathlib import Path
import sys

import pandas as pd
import matplotlib

# Charts ko image files mein save karne ke liye
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


# Project folder aur files ke paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "space_missions.csv"
CHART_DIR = BASE_DIR / "charts"

CHART_DIR.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")


def find_column(df, possible_names):
    """CSV mein column ka naam dhoondta hai."""
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def main():
    # Check karein ke CSV file mojood hai
    if not DATA_FILE.exists():
        print("ERROR: space_missions.csv file nahi mili!")
        print("CSV file yahan honi chahiye:", DATA_FILE)
        sys.exit(1)

    print("CSV file read ho rahi hai...")
    df = pd.read_csv(DATA_FILE, low_memory=False)

    # Column names saaf karein
    df.columns = [
        str(column).strip().replace("\ufeff", "")
        for column in df.columns
    ]

    # CSV mein istemal hone wale mumkin column names
    company_col = find_column(
        df,
        ["Company Name", "Company", "Organisation", "Organization"]
    )

    date_col = find_column(
        df,
        ["Datum", "Date", "Launch Date"]
    )

    status_col = find_column(
        df,
        [
            "Status Mission",
            "MissionStatus",
            "Mission Status",
            "Mission_Status",
        ]
    )

    location_col = find_column(
        df,
        ["Location", "Launch Site"]
    )

    # Zaroori columns check karein
    if company_col is None or date_col is None or status_col is None:
        print("CSV mein zaroori columns nahi mile.")
        print("Available columns:", list(df.columns))
        sys.exit(1)

    # Columns ke naam ek jaise kar dein
    rename_map = {
        company_col: "Company",
        date_col: "Date",
        status_col: "MissionStatus",
    }

    if location_col:
        rename_map[location_col] = "Location"

    df = df.rename(columns=rename_map)

    # Duplicate records hata dein
    df = df.drop_duplicates().copy()

    # Missing company names ko Unknown se replace karein
    df["Company"] = df["Company"].fillna("Unknown").astype(str)

    # Mission status ki safai
    df["MissionStatus"] = (
        df["MissionStatus"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # IMPORTANT:
    # utc=True mukhtalif time zones wali dates ko ek format mein badalta hai.
    # tz_localize(None) time zone ki information hata deta hai.
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
        format="mixed",
        utc=True
    ).dt.tz_localize(None)

    # Jin rows ki date valid nahi, unhein hata dein
    df = df.dropna(subset=["Date"]).copy()

    if df.empty:
        print("CSV mein koi valid date nahi mili.")
        print("CSV ke Date column ka format check karein.")
        sys.exit(1)

    # Year aur month ke columns banayein
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # Analysis report
    print("\n" + "=" * 50)
    print("SPACE RACE ANALYSIS REPORT")
    print("=" * 50)

    print("Total missions:", len(df))
    print("First date:", df["Date"].min().date())
    print("Last date:", df["Date"].max().date())
    print("Organisations:", df["Company"].nunique())

    print("\n--- First 5 Records ---")
    print(df.head().to_string(index=False))

    print("\n--- Mission Status ---")
    print(df["MissionStatus"].value_counts().to_string())

    print("\n--- Top 10 Organisations ---")
    print(df["Company"].value_counts().head(10).to_string())

    # Chart 1: Har saal kitne missions huay
    yearly = df.groupby("Year").size()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=yearly.index, y=yearly.values, marker="o")
    plt.title("Space Missions Per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Missions")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "01_missions_per_year.png", dpi=150)
    plt.close()

    # Chart 2: Sab se zyada missions wali 10 organisations
    top_companies = df["Company"].value_counts().head(10).sort_values()

    plt.figure(figsize=(12, 7))
    top_companies.plot(kind="barh")
    plt.title("Top 10 Organisations by Missions")
    plt.xlabel("Number of Missions")
    plt.ylabel("Organisation")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "02_top_organisations.png", dpi=150)
    plt.close()

    # Chart 3: Mission ke results
    outcomes = df["MissionStatus"].value_counts()

    plt.figure(figsize=(9, 6))
    outcomes.plot(kind="bar")
    plt.title("Mission Outcomes")
    plt.xlabel("Mission Status")
    plt.ylabel("Number of Missions")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "03_mission_outcomes.png", dpi=150)
    plt.close()

    # Chart 4: Har mahine kitne missions huay
    monthly = df["Month"].value_counts().sort_index()
    monthly = monthly.reindex(range(1, 13), fill_value=0)

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=month_names, y=monthly.values)
    plt.title("Space Missions by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Missions")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "04_missions_by_month.png", dpi=150)
    plt.close()

    # Chart 5: Launch locations
    if "Location" in df.columns:
        locations = (
            df["Location"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
        )

        plt.figure(figsize=(12, 7))
        locations.sort_values().plot(kind="barh")
        plt.title("Top 10 Launch Locations")
        plt.xlabel("Number of Missions")
        plt.ylabel("Location")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "05_launch_locations.png", dpi=150)
        plt.close()

    # Saaf kiya hua data CSV file mein save karein
    cleaned_file = BASE_DIR / "cleaned_space_missions.csv"
    df.to_csv(cleaned_file, index=False)

    print("\nSUCCESS! Analysis complete.")
    print("Charts folder:", CHART_DIR)
    print("Cleaned CSV:", cleaned_file)
    print("\nPyCharm mein charts folder khol kar PNG files dekhein.")


if __name__ == "__main__":
    main()
