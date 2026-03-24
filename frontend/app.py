import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Personal CA", layout="wide")

st.title("💸 AI Personal CA Dashboard")

# ---------------- USER INPUT ----------------
st.sidebar.header("👤 User")

user_id = st.sidebar.text_input("Enter User ID")

# ---------------- ADD TRANSACTION ----------------
st.sidebar.subheader("➕ Add Transaction")

date = st.sidebar.date_input("Date")
amount = st.sidebar.number_input("Amount", min_value=0.0)

category_input = st.sidebar.selectbox("Category", [
    "Food", "Shopping", "Transport", "Bills", "Medical", "Travel", "Other"
])

merchant = st.sidebar.text_input("Merchant")

if st.sidebar.button("Add Transaction"):
    if user_id:
        payload = {
            "user_id": user_id,
            "date": str(date),
            "amount": amount,
            "category": category_input,
            "merchant": merchant
        }

        res = requests.post(f"{BASE_URL}/add_transaction", json=payload)

        if res.status_code == 200:
            st.success("Transaction Added ✅")
            st.rerun()
        else:
            st.error("Error adding transaction")
    else:
        st.warning("Please enter User ID")

# ---------------- DASHBOARD ----------------
if user_id:

    # -------- KPI --------
    response = requests.get(f"{BASE_URL}/summary/{user_id}")

    col1, col2 = st.columns(2)

    if response.status_code == 200:
        summary = response.json()
        col1.metric("Total Spending", f"₹{summary.get('total_spending', 0)}")
        col2.metric("Average Spending", f"₹{summary.get('avg_spending', 0)}")
    else:
        st.error("Failed to load summary")

    # -------- CATEGORY --------
    st.subheader("📊 Category Breakdown")

    response = requests.get(f"{BASE_URL}/category/{user_id}")

    if response.status_code == 200:
        category = response.json()

        if category:
            cat_df = pd.DataFrame(list(category.items()), columns=["Category", "Amount"])
            fig = px.pie(cat_df, names="Category", values="Amount", title="Spending Distribution")
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No data available")
    else:
        st.error("Failed to load category data")

    # -------- TREND --------
    st.subheader("📈 Spending Trend")

    response = requests.get(f"{BASE_URL}/trend/{user_id}")

    if response.status_code == 200:
        trend = response.json()

        if trend:
            trend_df = pd.DataFrame(list(trend.items()), columns=["Month", "Amount"])
            fig2 = px.line(trend_df, x="Month", y="Amount", markers=True)
            st.plotly_chart(fig2, width="stretch")
        else:
            st.info("No trend data available")
    else:
        st.error("Failed to load trend data")

    # -------- LEAKS --------
    st.subheader("🚨 High Spending Alerts")

    response = requests.get(f"{BASE_URL}/leaks/{user_id}")

    if response.status_code == 200:
        leaks = response.json()

        if leaks.get("high_transactions"):
            leak_df = pd.DataFrame(leaks["high_transactions"])
            st.dataframe(leak_df)
        else:
            st.success("No major anomalies detected")
    else:
        st.error("Failed to load leaks data")

    # -------- TAX --------
    st.subheader("💰 Tax Insights")

    response = requests.get(f"{BASE_URL}/tax/{user_id}")

    if response.status_code == 200:
        tax = response.json()
        st.write(f"Tax-related spending: ₹{tax.get('tax_related_spending', 0)}")
        st.write(f"Relevant transactions: {tax.get('count', 0)}")
    else:
        st.error("Failed to load tax data")

    # -------- AI --------
    st.subheader("🤖 AI Financial Advisor")

    response = requests.get(f"{BASE_URL}/ai/{user_id}")

    if response.status_code == 200:
        ai = response.json()

        for insight in ai.get("insights", []):
            st.info(insight)
    else:
        st.error("Failed to load AI insights")

else:
    st.info("👈 Enter a User ID to view your dashboard")