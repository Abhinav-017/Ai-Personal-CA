import pandas as pd
from backend.database import get_connection
from sklearn.ensemble import IsolationForest

# -------- FETCH USER DATA --------
def get_user_data(user_id):
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE user_id = ?",
        conn,
        params=(user_id,)
    )

    conn.close()
    return df


# -------- SUMMARY --------
def get_summary(df):
    if df.empty:
        return {"total_spending": 0, "avg_spending": 0}

    return {
        "total_spending": float(df["amount"].sum()),
        "avg_spending": float(df["amount"].mean())
    }


# -------- CATEGORY --------
def category_analysis(df):
    if df.empty:
        return {}

    return df.groupby("category")["amount"].sum().to_dict()


# -------- TREND --------
def spending_trend(df):
    if df.empty:
        return {}

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df.groupby("month")["amount"].sum().to_dict()


# -------- LEAKS --------
def detect_leaks(df):
    if df.empty:
        return {"high_transactions": []}

    avg = df["amount"].mean()
    high = df[df["amount"] > avg * 2]

    return {
        "high_transactions": high[["date", "merchant", "amount"]]
        .to_dict(orient="records")
    }


# -------- TAX --------
def tax_insights(df):
    if df.empty:
        return {"tax_related_spending": 0, "count": 0}

    df["category"] = df["category"].str.lower()

    tax_df = df[df["category"].isin(["medical", "travel"])]

    return {
        "tax_related_spending": float(tax_df["amount"].sum()),
        "count": int(len(tax_df))
    }


# -------- AI INSIGHTS --------
def advanced_ai_insights(df):
    if df.empty:
        return ["Start adding transactions"]

    insights = []

    total = df["amount"].sum()
    avg = df["amount"].mean()

    insights.append(f"💰 Total spending: ₹{round(total,2)}")

    if (df["amount"] > avg * 2).any():
        insights.append("🚨 Unusual high transactions detected")

    cat = df.groupby("category")["amount"].sum()
    top = cat.idxmax()
    percent = (cat.max() / total) * 100

    insights.append(f"📊 {top} = {round(percent,1)}% of spending")

    if percent > 40:
        insights.append(f"⚠️ Reduce {top} spending")

    insights.append(f"🔁 Frequent: {df['merchant'].value_counts().idxmax()}")

    return insights


# -------- ML ANOMALY --------
def detect_anomalies_ml(df):
    if df.empty or len(df) < 5:
        return {"anomalies": []}

    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month

    X = df[["amount", "day", "month"]].values

    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly"] = model.fit_predict(X)

    anomalies = df[df["anomaly"] == -1]

    return {
        "anomalies": anomalies[["date", "merchant", "amount"]]
        .to_dict(orient="records")
    }