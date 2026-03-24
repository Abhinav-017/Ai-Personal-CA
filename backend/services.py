import pandas as pd
from database import get_connection
import pandas as pd

def get_user_data(user_id):
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE user_id = ?",
        conn,
        params=(user_id,)
    )

    conn.close()
    return df

# ---------------- SUMMARY ----------------
def get_summary(df):
    if df.empty:
        return {
            "total_spending": 0,
            "avg_spending": 0
        }

    total = df["amount"].sum()
    avg = df["amount"].mean()

    return {
        "total_spending": float(round(total, 2)),
        "avg_spending": float(round(avg, 2))
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
    
def advanced_ai_insights(df):
    insights = []

    if df.empty:
        return ["Start adding transactions to get insights"]

    total = df["amount"].sum()
    avg = df["amount"].mean()

    insights.append(f"💰 Total spending: ₹{round(total,2)}")

    # Overspending
    high = df[df["amount"] > avg * 2]
    if not high.empty:
        insights.append("🚨 You have unusually high transactions")

    # Category analysis
    cat = df.groupby("category")["amount"].sum()
    top = cat.idxmax()
    percent = (cat.max() / total) * 100

    insights.append(f"📊 {top} takes {round(percent,1)}% of your spending")

    if percent > 40:
        insights.append(f"⚠️ Reduce {top} spending")

    # Frequent merchant
    frequent = df["merchant"].value_counts().idxmax()
    insights.append(f"🔁 You frequently spend at {frequent}")

    return insights