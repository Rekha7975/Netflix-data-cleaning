import pandas as pd
import numpy as np

df = pd.read_csv("Netflix.csv")

print("Original Shape:", df.shape)
print(df.head())

df = df.drop_duplicates(subset="show_id")

print("\nMissing values per column:\n", df.isnull().sum())

fill_cols = ["director", "cast", "country", "date_added", "rating"]
for col in fill_cols:
    df[col] = df[col].fillna("Unknown")

df["duration"] = df["duration"].fillna("Unknown")

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

df["title"] = df["title"].str.strip()
df["director"] = df["director"].str.strip()
df["cast"] = df["cast"].str.strip()
df["country"] = df["country"].str.strip()

df["listed_in"] = df["listed_in"].str.lower()

df["duration_num"] = df["duration"].str.extract(r'(\d+)').astype(float)
df["duration_type"] = df["duration"].str.extract(r'([a-zA-Z]+)').fillna("Unknown")

df["rating"] = df["rating"].replace({
    "UR": "Unrated",
    "NR": "Unrated",
    "84 min": "Unrated" 
})

df.to_csv("netflix_cleaned.csv", index=False)

print("\nCleaned Shape:", df.shape)
print(df.head())
