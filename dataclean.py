# ============================================================
# Netflix Movies & TV Shows Dataset: Cleaning & Preprocessing
# ============================================================

import pandas as pd
import numpy as np

# 1) Load dataset
df = pd.read_csv("netflix_titles.csv")

print("Original Shape:", df.shape)

# 2) Drop duplicates
df = df.drop_duplicates(subset="show_id")

# 3) Handle missing values
fill_cols = ["director", "cast", "country", "date_added", "rating"]
for col in fill_cols:
    df[col] = df[col].fillna("Unknown")

df["duration"] = df["duration"].fillna("Unknown")

# 4) Convert date_added to datetime with explicit format
df["date_added"] = df["date_added"].astype(str).str.strip()
df["date_added"] = pd.to_datetime(
    df["date_added"], format="%B %d, %Y", errors="coerce"
)

# Extract year and month
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

# 5) Clean text columns
text_cols = ["title", "director", "cast", "country", "listed_in"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# Normalize genres
df["listed_in"] = df["listed_in"].str.lower()

# 6) Split duration into numeric + type
df["duration_num"] = df["duration"].str.extract(r'(\d+)').astype(float)
df["duration_type"] = df["duration"].str.extract(r'([a-zA-Z]+)').fillna("Unknown")

# 7) Fix inconsistent ratings
df["rating"] = df["rating"].replace({
    "UR": "Unrated",
    "NR": "Unrated",
    "84 min": "Unrated"
})

# 8) Multi-hot encoding for genres (listed_in)
# Split by comma and expand
genres_split = df["listed_in"].str.get_dummies(sep=", ")
df = pd.concat([df, genres_split], axis=1)

# 9) Save cleaned dataset to Excel
output_file = "netflix_cleaned.xlsx"
df.to_excel(output_file, index=False)

print("Cleaned Shape:", df.shape)
print(f"Cleaned dataset saved as {output_file}")
print(df.head())
