from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

print("=" * 60)
print("DAY 79 - NOBEL PRIZE DATA ANALYSIS")
print("=" * 60)

# 1. ڈیٹا پڑھنا اور صاف کرنا
df = pd.read_csv(DATA / "nobel_prizes.csv")
print("\n1. ڈیٹا کی پہلی 5 قطاریں:")
print(df.head())
print("\nڈیٹا کا سائز:", df.shape)
print("\nخالی اقدار:")
print(df.isnull().sum())

df = df.drop_duplicates().copy()
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["category"] = df["category"].fillna("Unknown")
df["sex"] = df["sex"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)
df.to_csv(OUT / "clean_nobel_prizes.csv", index=False)

# 2. ہر شعبے میں انعامات کی تعداد
category_counts = (
    df.groupby("category").size()
    .reset_index(name="prize_count")
    .sort_values("prize_count", ascending=False)
)
print("\n2. شعبے کے حساب سے انعامات:")
print(category_counts)
category_counts.to_csv(OUT / "prizes_by_category.csv", index=False)

fig = px.bar(
    category_counts, x="category", y="prize_count",
    title="Nobel Prizes by Category",
    labels={"category": "Prize Category", "prize_count": "Number of Prizes"},
    text="prize_count"
)
fig.write_html(OUT / "prizes_by_category.html")

# 3. خواتین اور مرد انعام یافتگان
sex_counts = df["sex"].value_counts().reset_index()
sex_counts.columns = ["sex", "prize_count"]
print("\n3. جنس کے حساب سے انعامات:")
print(sex_counts)
sex_counts.to_csv(OUT / "prizes_by_sex.csv", index=False)

fig = px.pie(
    sex_counts, names="sex", values="prize_count",
    hole=0.45, title="Nobel Prize Laureates by Sex"
)
fig.write_html(OUT / "prizes_by_sex_donut.html")

women = df[df["sex"].str.lower() == "female"]
print("\nخواتین انعام یافتگان کی تعداد:", len(women))
print(women[["year", "category", "laureate", "country"]].to_string(index=False))

# 4. وقت کے ساتھ انعامات کی تعداد
year_counts = df.groupby("year").size().reset_index(name="prize_count")
year_counts.to_csv(OUT / "prizes_over_time.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(year_counts["year"], year_counts["prize_count"], marker="o")
plt.title("Nobel Prize Records by Year (Sample Dataset)")
plt.xlabel("Year")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(OUT / "prizes_over_time.png", dpi=150)
plt.close()

# 5. ممالک کے حساب سے انعامات کا نقشہ
country_counts = (
    df.groupby(["country", "country_code"])
    .size().reset_index(name="prize_count")
)
country_counts.to_csv(OUT / "prizes_by_country.csv", index=False)

fig = px.choropleth(
    country_counts,
    locations="country_code",
    color="prize_count",
    hover_name="country",
    color_continuous_scale="Viridis",
    title="Nobel Prize Records by Country (Sample Dataset)",
    labels={"prize_count": "Prize Records"}
)
fig.write_html(OUT / "nobel_world_map.html")

print("\n5. زیادہ انعامات والے ممالک:")
print(country_counts.sort_values("prize_count", ascending=False).head(10))

# 6. خطے، ملک اور شعبے کے لحاظ سے Sunburst چارٹ
sunburst_data = (
    df.groupby(["region", "country", "category"])
    .size().reset_index(name="prize_count")
)
fig = px.sunburst(
    sunburst_data,
    path=["region", "country", "category"],
    values="prize_count",
    title="Nobel Prize Records: Region → Country → Category"
)
fig.write_html(OUT / "nobel_sunburst.html")

# 7. انعام حاصل کرتے وقت عمر
age_df = df.dropna(subset=["age"]).copy()
print("\n7. انعام حاصل کرتے وقت عمر:")
print("اوسط عمر:", round(age_df["age"].mean(), 1))
print("کم سے کم عمر:", int(age_df["age"].min()))
print("زیادہ سے زیادہ عمر:", int(age_df["age"].max()))

age_df.to_csv(OUT / "laureate_ages.csv", index=False)

plt.figure(figsize=(9, 5))
plt.hist(age_df["age"], bins=8, edgecolor="black")
plt.title("Laureate Age at the Time of the Prize")
plt.xlabel("Age")
plt.ylabel("Number of Laureates")
plt.tight_layout()
plt.savefig(OUT / "laureate_age_histogram.png", dpi=150)
plt.close()

fig = px.box(
    age_df, x="category", y="age", color="category",
    title="Laureate Age by Prize Category"
)
fig.write_html(OUT / "age_by_category.html")

print("\nتمام نتائج اور چارٹس یہاں محفوظ ہیں:", OUT)
print("Day 79 مکمل ہوگیا!")
print("نوٹ: یہ مشق کے لیے نمونہ ڈیٹا ہے، مکمل تاریخی Nobel dataset نہیں۔")
