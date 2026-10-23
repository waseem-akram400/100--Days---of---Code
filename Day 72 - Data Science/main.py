import pandas as pd
from pathlib import Path

# CSV file ka path
DATA_FILE = Path(__file__).parent / "data" / "college_majors.csv"


def main():
    # CSV file ko Pandas DataFrame mein read karna
    df = pd.read_csv(DATA_FILE)

    print("\n===== DAY 72: DATA SCIENCE WITH PANDAS =====")
    print("\n1. Pehli 5 rows:")
    print(df.head())

    print("\n2. Data ki maloomat:")
    df.info()

    print("\n3. Missing values:")
    print(df.isnull().sum())

    # Zaroorat par missing values wali rows hata dein
    df = df.dropna().copy()

    print("\n4. Majors ki tadaad:", len(df))
    print("\n5. Columns:")
    print(df.columns.tolist())

    print("\n6. Sab se zyada starting salary wali 5 degrees:")
    print(
        df.sort_values("Starting Median Salary", ascending=False)
        [["Major", "Starting Median Salary"]]
        .head()
        .to_string(index=False)
    )

    print("\n7. Sab se zyada mid-career salary wali 5 degrees:")
    print(
        df.sort_values("Mid-Career Median Salary", ascending=False)
        [["Major", "Mid-Career Median Salary"]]
        .head()
        .to_string(index=False)
    )

    # Naya column: career mein salary ka izafa
    df["Salary Growth"] = (
        df["Mid-Career Median Salary"] - df["Starting Median Salary"]
    )

    print("\n8. Sab se zyada salary growth wali degrees:")
    print(
        df.sort_values("Salary Growth", ascending=False)
        [["Major", "Salary Growth"]]
        .head()
        .to_string(index=False)
    )

    # Risk ka andaza: 10th percentile salary
    df["Lowest Career Salary"] = df["Mid-Career 10th Percentile"]

    print("\n9. Kam risk ka andaza: sab se zyada 10th percentile salary:")
    print(
        df.sort_values("Lowest Career Salary", ascending=False)
        [["Major", "Lowest Career Salary"]]
        .head()
        .to_string(index=False)
    )

    # Groups aur summary
    df["Salary Group"] = pd.cut(
        df["Mid-Career Median Salary"],
        bins=[0, 70000, 100000, float("inf")],
        labels=["Lower", "Middle", "Higher"]
    )

    print("\n10. Salary group ke mutabiq degrees ki tadaad:")
    print(df.groupby("Salary Group", observed=False).size())

    print("\n11. Salary group ke mutabiq average salary:")
    print(
        df.groupby("Salary Group", observed=False)
        [["Starting Median Salary", "Mid-Career Median Salary"]]
        .mean()
        .round(2)
    )

    # Pivot table
    pivot = pd.pivot_table(
        df,
        index="Salary Group",
        values=["Starting Median Salary", "Mid-Career Median Salary"],
        aggfunc="mean",
        observed=False
    )

    print("\n12. Pivot table:")
    print(pivot.round(2))

    # Cleaned data ko nayi CSV file mein save karna
    output_file = Path(__file__).parent / "cleaned_college_majors.csv"
    df.to_csv(output_file, index=False)

    print(f"\nCleaned data save ho gaya: {output_file}")
    print("\nProject successfully complete!")


if __name__ == "__main__":
    main()
