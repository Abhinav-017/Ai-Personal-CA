import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Personal CA", layout="wide")

st.title("💸 AI Personal CA Dashboard")

# ---------------- KPI ----------------
summary = requests.get(f"{BASE_URL}/summary").json()

col1, col2 = st.columns(2)

col1.metric("Total Spending", f"₹{summary['total_spending']}")
col2.metric("Average Spending", f"₹{summary['avg_spending']}")

# ---------------- CATEGORY ----------------
st.subheader("📊 Category Breakdown")

category = requests.get(f"{BASE_URL}/category").json()
cat_df = pd.DataFrame(list(category.items()), columns=["Category", "Amount"])

fig = px.pie(cat_df, names="Category", values="Amount", title="Spending Distribution")
st.plotly_chart(fig, use_container_width=True)

# ---------------- TREND ----------------
st.subheader("📈 Spending Trend")

trend = requests.get(f"{BASE_URL}/trend").json()
trend_df = pd.DataFrame(list(trend.items()), columns=["Month", "Amount"])

fig2 = px.line(trend_df, x="Month", y="Amount", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- LEAKS ----------------
st.subheader("🚨 High Spending Alerts")

leaks = requests.get(f"{BASE_URL}/leaks").json()

if leaks["high_transactions"]:
    leak_df = pd.DataFrame(leaks["high_transactions"])
    st.dataframe(leak_df)
else:
    st.success("No major anomalies detected")

# ---------------- TAX ----------------
st.subheader("💰 Tax Insights")

tax = requests.get(f"{BASE_URL}/tax").json()

st.write(f"Tax-related spending: ₹{tax['tax_related_spending']}")
st.write(f"Relevant transactions: {tax['count']}")