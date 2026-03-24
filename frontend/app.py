import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Personal CA", layout="wide")

st.title("💸 AI Personal CA Dashboard")

# -------- USER --------
user_id = st.sidebar.text_input("Enter User ID")

# -------- ADD TRANSACTION --------
st.sidebar.subheader("➕ Add Transaction")

date = st.sidebar.date_input("Date")
amount = st.sidebar.number_input("Amount", min_value=0.0)

category = st.sidebar.selectbox("Category", [
    "Food", "Shopping", "Transport", "Bills", "Medical", "Travel", "Other"
])

merchant = st.sidebar.text_input("Merchant")

if st.sidebar.button("Add Transaction"):
    payload = {
        "user_id": user_id,
        "date": str(date),
        "amount": amount,
        "category": category,
        "merchant": merchant
    }

    res = requests.post(f"{BASE_URL}/add_transaction", json=payload)

    if res.status_code == 200:
        st.success("Added ✅")
        st.rerun()

# -------- DASHBOARD --------
if user_id:

    # KPI
    summary = requests.get(f"{BASE_URL}/summary/{user_id}").json()

    col1, col2 = st.columns(2)
    col1.metric("Total", f"₹{summary.get('total_spending',0)}")
    col2.metric("Average", f"₹{summary.get('avg_spending',0)}")

    # Category
    cat = requests.get(f"{BASE_URL}/category/{user_id}").json()
    if cat:
        df = pd.DataFrame(list(cat.items()), columns=["Category", "Amount"])
        st.plotly_chart(px.pie(df, names="Category", values="Amount"), width="stretch")

    # Trend
    trend = requests.get(f"{BASE_URL}/trend/{user_id}").json()
    if trend:
        df = pd.DataFrame(list(trend.items()), columns=["Month", "Amount"])
        st.plotly_chart(px.line(df, x="Month", y="Amount"), width="stretch")

    # AI
    st.subheader("🤖 AI Insights")
    ai = requests.get(f"{BASE_URL}/ai/{user_id}").json()
    for i in ai["insights"]:
        st.info(i)

    # ML
    st.subheader("🧠 ML Anomalies")
    ml = requests.get(f"{BASE_URL}/ml-anomalies/{user_id}").json()

    if ml["anomalies"]:
        st.dataframe(pd.DataFrame(ml["anomalies"]))
    else:
        st.success("No anomalies detected")

else:
    st.info("Enter User ID to start")