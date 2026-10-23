from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "output"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")
np.random.seed(80)

print("=" * 65)
print("DAY 80 - THE EFFECT OF HANDWASHING")
print("=" * 65)

# 1. سیکھنے کے لیے نمونہ ڈیٹا بنائیں۔
# یہ اصل تاریخی ویانا ہسپتال کا ڈیٹا نہیں ہے۔
csv_path = DATA / "hospital_monthly_data.csv"

if not csv_path.exists():
    months = pd.date_range("1846-01-01", "1849-12-01", freq="MS")
    rows = []

    for date in months:
        year = date.year
        month = date.month

        # 1847 کے وسط میں ہاتھ دھونے کی پالیسی متعارف ہونے کا فرضی مرحلہ
        handwashing = date >= pd.Timestamp("1847-06-01")

        for clinic in ["Clinic 1", "Clinic 2"]:
            births = int(np.random.randint(250, 401))

            # نمونہ ڈیٹا میں پالیسی کے بعد Clinic 1 کی فرضی شرح کم رکھی گئی ہے۔
            if clinic == "Clinic 1":
                death_rate = 0.10 if not handwashing else 0.03
            else:
                death_rate = 0.05 if not handwashing else 0.045

            # ماہ بہ ماہ قدرتی اتار چڑھاؤ شامل کریں
            death_rate += np.random.normal(0, 0.008)
            death_rate = float(np.clip(death_rate, 0.005, 0.20))
            deaths = int(round(births * death_rate))

            rows.append({
                "date": date,
                "year": year,
                "month": month,
                "clinic": clinic,
                "births": births,
                "deaths": deaths,
                "handwashing": handwashing
            })

    pd.DataFrame(rows).to_csv(csv_path, index=False)

# 2. ڈیٹا پڑھیں اور بنیادی معلومات دیکھیں
df = pd.read_csv(csv_path, parse_dates=["date"])
df = df.drop_duplicates().copy()
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["births"] = pd.to_numeric(df["births"], errors="coerce")
df["deaths"] = pd.to_numeric(df["deaths"], errors="coerce")
df = df.dropna(subset=["date", "year", "clinic", "births", "deaths"])
df = df[(df["births"] > 0) & (df["deaths"] >= 0)]
df["year"] = df["year"].astype(int)
df["mortality_rate"] = df["deaths"] / df["births"] * 100
df["handwashing"] = df["handwashing"].astype(str).str.lower().isin(
    ["true", "1", "yes"]
)

print("\n1. ڈیٹا کی پہلی 5 قطاریں:")
print(df.head())
print("\nکل قطاریں اور کالم:", df.shape)
print("\nخالی اقدار:")
print(df.isnull().sum())
print("\nکل پیدائشیں:", int(df["births"].sum()))
print("کل اموات:", int(df["deaths"].sum()))

df.to_csv(OUT / "clean_hospital_data.csv", index=False)

# 3. سال اور کلینک کے لحاظ سے ڈیٹا
yearly = (
    df.groupby(["year", "clinic"], as_index=False)
    .agg(
        births=("births", "sum"),
        deaths=("deaths", "sum")
    )
)
yearly["mortality_rate"] = yearly["deaths"] / yearly["births"] * 100

print("\n2. سال اور کلینک کے لحاظ سے اموات کی شرح:")
print(yearly.to_string(index=False))
yearly.to_csv(OUT / "yearly_clinic_summary.csv", index=False)

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=yearly, x="year", y="mortality_rate",
    hue="clinic", marker="o"
)
plt.title("Yearly Mortality Rate by Clinic")
plt.xlabel("Year")
plt.ylabel("Deaths per 100 Births (%)")
plt.tight_layout()
plt.savefig(OUT / "yearly_mortality_by_clinic.png", dpi=150)
plt.close()

# 4. ہاتھ دھونے سے پہلے اور بعد کا موازنہ
before_after = (
    df.groupby("handwashing", as_index=False)
    .agg(
        births=("births", "sum"),
        deaths=("deaths", "sum")
    )
)
before_after["period"] = before_after["handwashing"].map({
    False: "Before handwashing",
    True: "After handwashing"
})
before_after["mortality_rate"] = (
    before_after["deaths"] / before_after["births"] * 100
)

print("\n3. ہاتھ دھونے سے پہلے اور بعد:")
print(before_after[["period", "births", "deaths", "mortality_rate"]].to_string(index=False))
before_after.to_csv(OUT / "before_after_summary.csv", index=False)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=before_after, x="period", y="mortality_rate"
)
plt.title("Mortality Rate Before vs After Handwashing")
plt.xlabel("Period")
plt.ylabel("Deaths per 100 Births (%)")
plt.tight_layout()
plt.savefig(OUT / "before_after_handwashing.png", dpi=150)
plt.close()

# 5. ہر مہینے کی شرح کا فرق اور تقسیم
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df, x="mortality_rate", hue="handwashing",
    bins=15, kde=True, element="step"
)
plt.title("Distribution of Monthly Mortality Rates")
plt.xlabel("Deaths per 100 Births (%)")
plt.tight_layout()
plt.savefig(OUT / "mortality_distribution.png", dpi=150)
plt.close()

# 6. Statistical Significance کے لیے Welch's t-test
before = df.loc[~df["handwashing"], "mortality_rate"]
after = df.loc[df["handwashing"], "mortality_rate"]

print("\n4. Statistical Significance Test")
if len(before) >= 2 and len(after) >= 2:
    statistic, p_value = ttest_ind(before, after, equal_var=False)
    print("Before period monthly records:", len(before))
    print("After period monthly records:", len(after))
    print("t-statistic:", round(float(statistic), 4))
    print("p-value:", round(float(p_value), 6))

    if p_value < 0.05:
        print("نتیجہ: اس نمونہ ڈیٹا میں دونوں ادوار کے درمیان شماریاتی فرق ملا (p < 0.05).")
    else:
        print("نتیجہ: اس نمونہ ڈیٹا میں واضح شماریاتی فرق نہیں ملا (p >= 0.05).")
else:
    print("ٹیسٹ کے لیے دونوں ادوار میں کافی ریکارڈ موجود نہیں۔")

print("\nتمام نتائج محفوظ ہیں:", OUT)
print("Day 80 مکمل ہوگیا!")
print("نوٹ: یہ فرضی مشقی ڈیٹا ہے، اصل تاریخی شواہد نہیں۔")
