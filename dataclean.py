# ============================================================
# Netflix Movies & TV Shows Dataset: Cleaning & Preprocessing
# ============================================================

# 1) Import libraries
import pandas as pd
import numpy as np

# 2) Load dataset
df = pd.read_csv("netflix_titles.csv")

print("Original Shape:", df.shape)
print(df.head())

# 3) Drop duplicates
df = df.drop_duplicates(subset="show_id")

# 4) Handle missing values
print("\nMissing values per column:\n", df.isnull().sum())

# Fill missing categorical columns with "Unknown"
fill_cols = ["director", "cast", "country", "date_added", "rating"]
for col in fill_cols:
    df[col] = df[col].fillna("Unknown")

# For 'duration', missing only in TV Shows → replace with "Unknown"
df["duration"] = df["duration"].fillna("Unknown")

# 5) Convert date_added to datetime with explicit format
df["date_added"] = df["date_added"].str.strip()  # remove leading/trailing spaces
df["date_added"] = pd.to_datetime(
    df["date_added"],
    format="%B %d, %Y",  # Example: "September 9, 2019"
    errors="coerce"      # invalid/missing values → NaT
)

# Extract year and month from date_added
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

# 6) Clean text columns
text_cols = ["title", "director", "cast", "country", "listed_in"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# Normalize genres to lowercase
df["listed_in"] = df["listed_in"].str.lower()

# 7) Handle duration (split into numeric + type)
df["duration_num"] = df["duration"].str.extract(r'(\d+)').astype(float)
df["duration_type"] = df["duration"].str.extract(r'([a-zA-Z]+)').fillna("Unknown")

# 8) Standardize ratings (some values inconsistent)
df["rating"] = df["rating"].replace({
    "UR": "Unrated",
    "NR": "Unrated",
    "84 min": "Unrated"  # data issue
})

# 9) Drop irrelevant columns (optional)
# df = df.drop(columns=["description"])  # drop if not needed

# 10) Save cleaned dataset
df.to_csv("netflix_cleaned.csv", index=False)

print("\nCleaned Shape:", df.shape)
print(df.head())
