from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# Day 78: Movie Data Analysis
BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "output"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")
np.random.seed(42)

print("=" * 65)
print("DAY 78 - MOVIE DATA ANALYSIS")
print("=" * 65)

# اگر CSV موجود نہ ہو تو مشق کے لیے نمونہ ڈیٹا بنائیں۔
# یہ اصل فلمی ڈیٹا نہیں بلکہ سیکھنے کے لیے بنایا گیا ڈیٹا ہے۔
csv_path = DATA / "movies.csv"

if not csv_path.exists():
    titles = [
        "Ocean Journey", "City Lights", "Hidden Planet", "Summer Days",
        "The Last Train", "Golden Crown", "Across Borders", "Blue River",
        "Silent Mountain", "Future World", "Lost Letters", "Night Runner",
        "Desert Flower", "Moon Station", "Winter Story", "Open Road",
        "Star Kingdom", "Old Memories", "Wild Earth", "Bright Morning",
        "Foreign Dreams", "Deep Space", "Broken Clock", "New Horizons",
        "River Song", "The Long Way", "Silver Wings", "Hidden Garden",
        "Red Balloon", "Final Chapter", "World Apart", "Small Wonders"
    ]
    countries = [
        "USA", "USA", "UK", "France", "USA", "India", "Japan", "France",
        "USA", "Canada", "Italy", "USA", "India", "Japan", "UK", "USA",
        "USA", "Spain", "Australia", "USA", "South Korea", "USA",
        "Germany", "Canada", "France", "USA", "India", "UK", "Mexico",
        "USA", "Japan", "USA"
    ]
    years = [
        1988, 1994, 2001, 2005, 2010, 2012, 2015, 2017,
        2018, 2019, 2020, 2021, 2022, 2023, 2008, 1999,
        2003, 2011, 2014, 2016, 2024, 2020, 2007, 2013,
        2009, 2018, 2022, 2006, 2017, 2021, 2019, 2015
    ]

    budgets = (np.random.randint(5, 150, len(titles)) * 1_000_000).astype(float)
    revenues = budgets * np.random.uniform(0.5, 4.0, len(titles))
    revenues = revenues.astype(float)

    # چند فلم کے لیے صفر آمدنی اور چند کے لیے خالی ڈیٹا
    revenues[[3, 10, 20]] = 0
    budgets[7] = 0
    revenues[12] = np.nan
    budgets[18] = np.nan

    ratings = np.round(np.random.uniform(4.5, 9.2, len(titles)), 1)
    ratings[5] = np.nan

    df_sample = pd.DataFrame({
        "title": titles,
        "year": years,
        "country": countries,
        "budget": budgets,
        "revenue": revenues,
        "rating": ratings
    })

    # ایک duplicate row شامل کریں تاکہ duplicate removal بھی آزمائی جا سکے۔
    df_sample = pd.concat([df_sample, df_sample.iloc[[0]]], ignore_index=True)
    df_sample.to_csv(csv_path, index=False)

# 1. ڈیٹا پڑھنا اور اس کی جانچ کرنا
df = pd.read_csv(csv_path)

print("\n1. اصل ڈیٹا کی پہلی 5 قطاریں:")
print(df.head())
print("\nڈیٹا کا سائز (rows, columns):", df.shape)
print("\nخالی اقدار کی تعداد:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# 2. ڈیٹا صاف کرنا
df = df.drop_duplicates().copy()

for column in ["year", "budget", "revenue", "rating"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["country"] = df["country"].fillna("Unknown")
df["title"] = df["title"].fillna("Untitled")
df["decade"] = (df["year"] // 10 * 10).astype("Int64")

# Regression کے لیے صرف ضروری numeric values والی قطاریں استعمال کریں۔
clean_df = df.dropna(subset=["year", "budget", "revenue", "rating"]).copy()
clean_df.to_csv(OUT / "clean_movies.csv", index=False)

print("\n2. صفائی کے بعد ڈیٹا:")
print("قطاروں کی تعداد:", len(clean_df))
print(clean_df.head())
print("\nصاف ڈیٹا محفوظ کیا گیا:", OUT / "clean_movies.csv")

# 3. صفر آمدنی والی فلمیں
zero_revenue = df[df["revenue"] == 0]
print("\n3. صفر آمدنی والی فلمیں:")
if zero_revenue.empty:
    print("کوئی فلم نہیں ملی۔")
else:
    print(zero_revenue[["title", "year", "budget", "revenue"]])
zero_revenue.to_csv(OUT / "zero_revenue_movies.csv", index=False)

# 4. متعدد شرائط: غیر امریکی فلمیں جن کی آمدنی صفر سے زیادہ ہے
international = clean_df[
    (clean_df["country"] != "USA") &
    (clean_df["revenue"] > 0) &
    (clean_df["budget"] > 0)
].copy()

print("\n4. بین الاقوامی فلمیں (USA کے علاوہ، مثبت آمدنی):")
print(international[["title", "country", "year", "budget", "revenue"]].head(10))
international.to_csv(OUT / "international_movies.csv", index=False)

# 5. Bubble chart: بجٹ، آمدنی، اور rating
bubble_df = clean_df[
    (clean_df["budget"] > 0) & (clean_df["revenue"] > 0)
].copy()

if not bubble_df.empty:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=bubble_df,
        x="budget",
        y="revenue",
        size="rating",
        hue="rating",
        sizes=(50, 450),
        palette="viridis",
        alpha=0.8
    )
    plt.title("Movie Budget vs Revenue (Bubble Chart)")
    plt.xlabel("Budget")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(OUT / "bubble_chart.png", dpi=150)
    plt.close()

# 6. دہائی کے حساب سے فلموں کی تعداد
decade_counts = (
    df.dropna(subset=["year"])
    .assign(decade=lambda x: (x["year"] // 10 * 10).astype(int))
    .groupby("decade")
    .size()
    .reset_index(name="movie_count")
)
print("\n6. دہائی کے حساب سے فلموں کی تعداد:")
print(decade_counts)
decade_counts.to_csv(OUT / "movies_by_decade.csv", index=False)

plt.figure(figsize=(9, 5))
sns.barplot(data=decade_counts, x="decade", y="movie_count")
plt.title("Number of Movies by Decade")
plt.xlabel("Decade")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "movies_by_decade.png", dpi=150)
plt.close()

# 7. Seaborn regression line
if len(bubble_df) >= 2:
    plt.figure(figsize=(9, 5))
    sns.regplot(
        data=bubble_df,
        x="budget",
        y="revenue",
        scatter_kws={"alpha": 0.7},
        line_kws={"color": "red"}
    )
    plt.title("Linear Regression: Budget vs Revenue")
    plt.tight_layout()
    plt.savefig(OUT / "seaborn_regression.png", dpi=150)
    plt.close()

# 8. scikit-learn سے اپنا Linear Regression ماڈل
model_df = clean_df[
    (clean_df["budget"] > 0) & (clean_df["revenue"] >= 0)
].copy()

if len(model_df) >= 3:
    X = model_df[["budget"]]
    y = model_df["revenue"]

    # اس سادہ مشق میں پورے دستیاب ڈیٹا پر ماڈل fit کیا جاتا ہے۔
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)

    print("\n8. scikit-learn Linear Regression:")
    print("Slope / coefficient:", round(float(model.coef_[0]), 4))
    print("Intercept:", round(float(model.intercept_), 2))
    print("R-squared:", round(float(r2_score(y, predictions)), 4))
    print("Mean Absolute Error:", round(float(mean_absolute_error(y, predictions)), 2))

    # بجٹ کی ایک مثال کے لیے اندازاً آمدنی
    example_budget = pd.DataFrame({"budget": [50_000_000]})
    predicted_revenue = model.predict(example_budget)[0]
    print("5 کروڑ بجٹ کے لیے اندازاً آمدنی:", round(float(predicted_revenue), 2))

    model_results = model_df[["title", "budget", "revenue"]].copy()
    model_results["predicted_revenue"] = predictions
    model_results.to_csv(OUT / "regression_predictions.csv", index=False)

    plt.figure(figsize=(9, 5))
    plt.scatter(X["budget"], y, label="Actual movies")
    plt.plot(X["budget"], predictions, color="red", label="Model prediction")
    plt.title("scikit-learn: Budget vs Revenue")
    plt.xlabel("Budget")
    plt.ylabel("Revenue")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "sklearn_regression.png", dpi=150)
    plt.close()
else:
    print("\nRegression کے لیے کافی صاف ڈیٹا موجود نہیں۔")

print("\nچارٹس اور نتائج محفوظ ہیں:", OUT)
print("Day 78 مکمل ہوگیا!")
