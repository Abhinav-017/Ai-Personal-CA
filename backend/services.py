import pandas as pd

# ---------------- SUMMARY ----------------
def get_summary(df):
    total = df["amount"].sum()
    avg = df["amount"].mean()

    return {
        "total_spending": round(total, 2),
        "avg_spending": round(avg, 2)
    }

# ---------------- CATEGORY ----------------
def category_analysis(df):
    data = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return data.to_dict()

# ---------------- TREND ----------------
def spending_trend(df):
    trend = df.groupby("month")["amount"].sum()
    return trend.to_dict()

# ---------------- LEAK DETECTION ----------------
def detect_leaks(df):
    avg = df["amount"].mean()
    
    high_spends = df[df["amount"] > avg * 2]

    return {
        "high_transactions": high_spends[["date", "merchant", "amount"]]
        .head(10)
        .to_dict(orient="records")
    }

# ---------------- TAX INSIGHTS ----------------
def tax_insights(df):
    try:
        # If expense_type doesn't exist, create it dynamically
        if "expense_type" not in df.columns:

            def tag_expense(category):
                category = str(category).lower()

                if "grocery" in category:
                    return "Essential"
                elif "shopping" in category:
                    return "Discretionary"
                elif "health" in category:
                    return "Medical"
                elif "travel" in category:
                    return "Travel"
                else:
                    return "Other"

            df["expense_type"] = df["category"].apply(tag_expense)

        tax_related = df[df["expense_type"].isin(["Medical", "Travel"])]

        return {
            "tax_related_spending": float(tax_related["amount"].sum()),
            "count": int(len(tax_related))
        }

    except Exception as e:
        return {
            "error": str(e),
            "tax_related_spending": 0,
            "count": 0
        }