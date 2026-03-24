from fastapi import FastAPI
import pandas as pd
from backend.services import *

app = FastAPI()

# Load cleaned data
df = pd.read_csv("data/cleaned_transactions.csv")
df["date"] = pd.to_datetime(df["date"])

# ------------------- ROUTES -------------------

@app.get("/")
def home():
    return {"message": "AI Personal CA Backend Running 🚀"}

# 1️⃣ SUMMARY KPI
@app.get("/summary")
def summary():
    return get_summary(df)

# 2️⃣ CATEGORY ANALYSIS
@app.get("/category")
def category():
    return category_analysis(df)

# 3️⃣ SPENDING TREND
@app.get("/trend")
def trend():
    return spending_trend(df)

# 4️⃣ MONEY LEAK DETECTION
@app.get("/leaks")
def leaks():
    return detect_leaks(df)

# 5️⃣ TAX / EXPENSE INSIGHTS
@app.get("/tax")
def tax():
    return tax_insights(df)