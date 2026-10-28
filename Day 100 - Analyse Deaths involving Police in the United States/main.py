from pathlib import Path
import sys
import pandas as pd
import matplotlib

# Charts ko files mein save karne ke liye
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Deaths_by_Police_US.csv"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")


def main():
    # Dataset file check karein
    if not DATA_FILE.exists():
        print("ERROR: Deaths_by_Police_US.csv file nahi mili.")
        print("Dataset CSV file is folder mein copy karein:")
        print(BASE_DIR)
        print("Phir main.py dobara run karein.")
        sys.exit(1)

    print("Police deaths dataset read ho raha hai...")

    # Mukhtalif encodings try karein
    try:
        df = pd.read_csv(DATA_FILE, encoding="utf-8", encoding_errors="replace")
    except Exception:
        df = pd.read_csv(DATA_FILE, encoding="cp1252")

    df.columns = [str(col).strip().replace("\ufeff", "") for col in df.columns]

    required = ["date", "age", "gender", "state"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        print("Dataset mein zaroori columns nahi mile:", missing)
        print("Available columns:", list(df.columns))
        sys.exit(1)

    # Dates aur numeric age ko saaf karein
    df["date"] = pd.to_datetime(
        df["date"], format="mixed", errors="coerce"
    )
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Date ke baghair rows ko yearly analysis se hata dein
    df = df.dropna(subset=["date"]).copy()
    df["year"] = df["date"].dt.year

    print("\n" + "=" * 50)
    print("POLICE-RELATED DEATHS: DATA ANALYSIS")
    print("=" * 50)
    print("Total records:", len(df))
    print("Date range:", df["date"].min().date(), "to", df["date"].max().date())
    print("States represented:", df["state"].nunique())

    print("\n--- First 5 records ---")
    print(df.head().to_string(index=False))

    print("\n--- Records by year ---")
    print(df["year"].value_counts().sort_index().to_string())

    print("\n--- Records by gender ---")
    print(df["gender"].fillna("Unknown").value_counts().to_string())

    print("\n--- Top 10 states by recorded deaths ---")
    print(df["state"].value_counts().head(10).to_string())

    print("\n--- Age summary ---")
    print(df["age"].describe().round(2).to_string())

    # Chart 1: Recorded deaths per year
    yearly = df.groupby("year").size()
    plt.figure(figsize=(10, 5))
    yearly.plot(kind="bar")
    plt.title("Recorded Police-Related Deaths by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of records")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "01_deaths_by_year.png", dpi=150)
    plt.close()

    # Chart 2: Top 10 states
    states = df["state"].value_counts().head(10).sort_values()
    plt.figure(figsize=(10, 6))
    states.plot(kind="barh")
    plt.title("Top 10 States by Recorded Deaths")
    plt.xlabel("Number of records")
    plt.ylabel("State")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "02_top_states.png", dpi=150)
    plt.close()

    # Chart 3: Age distribution
    ages = df["age"].dropna()
    if not ages.empty:
        plt.figure(figsize=(10, 5))
        sns.histplot(ages, bins=25, kde=True)
        plt.title("Age Distribution in the Dataset")
        plt.xlabel("Age")
        plt.ylabel("Number of records")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "03_age_distribution.png", dpi=150)
        plt.close()

    # Chart 4: Gender
    plt.figure(figsize=(8, 5))
    df["gender"].fillna("Unknown").value_counts().plot(kind="bar")
    plt.title("Records by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Number of records")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "04_gender.png", dpi=150)
    plt.close()

    # Chart 5: Armed status, if column exists
    if "armed" in df.columns:
        armed = df["armed"].fillna("Unknown").value_counts().head(10)
        plt.figure(figsize=(10, 6))
        armed.sort_values().plot(kind="barh")
        plt.title("Most Common Recorded Armed Status")
        plt.xlabel("Number of records")
        plt.ylabel("Recorded status")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "05_armed_status.png", dpi=150)
        plt.close()

    # Chart 6: Signs of mental illness, if column exists
    if "signs_of_mental_illness" in df.columns:
        mental = (
            df["signs_of_mental_illness"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )
        plt.figure(figsize=(8, 5))
        mental.plot(kind="bar")
        plt.title("Recorded Signs of Mental Illness")
        plt.xlabel("Recorded value")
        plt.ylabel("Number of records")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(CHART_DIR / "06_mental_illness.png", dpi=150)
        plt.close()

    # Chart 7: Body camera, if column exists
    if "body_camera" in df.columns:
        camera = (
            df["body_camera"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )
        plt.figure(figsize=(8, 5))
        camera.plot(kind="bar")
        plt.title("Body Camera Records")
        plt.xlabel("Recorded value")
        plt.ylabel("Number of records")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(CHART_DIR / "07_body_camera.png", dpi=150)
        plt.close()

    # Cleaned data save karein
    cleaned_file = BASE_DIR / "cleaned_police_deaths.csv"
    df.to_csv(cleaned_file, index=False)

    print("\nSUCCESS! Analysis complete.")
    print("Charts folder:", CHART_DIR)
    print("Cleaned dataset:", cleaned_file)
    print("\nCharts dekhne ke liye PyCharm mein charts folder kholein.")
    print("\nNote: Yeh descriptive records hain; in se apne aap causation sabit nahi hoti.")


if __name__ == "__main__":
    main()
