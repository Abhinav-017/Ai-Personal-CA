import pandas as pd
import os

# Get project root path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input file path
input_path = os.path.join(BASE_DIR, "data", "transactions.csv")

# Output file path
output_path = os.path.join(BASE_DIR, "data", "cleaned_transactions.csv")

print("📂 Loading file from:", input_path)

# Load dataset
df = pd.read_csv(input_path)

print("✅ Loaded successfully")
print(df.head())

# ---------------- CLEANING ----------------

# Drop useless columns
df.drop(columns=[
    "Unnamed: 0",
    "cc_num",
    "first",
    "last",
    "gender",
    "street"
], inplace=True, errors='ignore')

# Rename columns
df.rename(columns={
    "trans_date_trans_time": "date",
    "amt": "amount"
}, inplace=True)

# Convert types
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["amount", "date"])

# Clean merchant
df["merchant"] = df["merchant"].astype(str).str.lower().str.strip()

# Format category
df["category"] = df["category"].str.title()

# Add time features
df["month"] = df["date"].dt.to_period("M").astype(str)
df["day"] = df["date"].dt.date

# Save cleaned file
df.to_csv(output_path, index=False)

print("\n🎉 CLEANING COMPLETE")
print("💾 Saved to:", output_path)
print("📊 Rows:", len(df))