import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("💸 AI Personal CA")

# -------- SESSION --------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------- AUTH --------
st.sidebar.title("🔐 Auth")

mode = st.sidebar.selectbox("Mode", ["Login", "Register"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if mode == "Register":
    if st.sidebar.button("Register"):
        res = requests.post(f"{BASE_URL}/register",
                            json={"username": username, "password": password})
        st.sidebar.success(res.json().get("message", res.json().get("error")))

if mode == "Login":
    if st.sidebar.button("Login"):
        res = requests.post(f"{BASE_URL}/login",
                            json={"username": username, "password": password})
        data = res.json()

        if "user_id" in data:
            st.session_state.user_id = data["user_id"]
            st.rerun()
        else:
            st.sidebar.error("Invalid login")

# -------- USER --------
user_id = st.session_state.user_id

if user_id:
    st.sidebar.write(f"👤 {user_id}")

    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.rerun()

    # -------- ADD --------
    st.sidebar.subheader("Add Transaction")

    date = st.sidebar.date_input("Date")
    amount = st.sidebar.number_input("Amount", 0.0)

    category = st.sidebar.selectbox("Category",
        ["Food","Shopping","Transport","Bills","Medical","Travel","Other"])

    merchant = st.sidebar.text_input("Merchant")

    if st.sidebar.button("Add"):
        requests.post(f"{BASE_URL}/add_transaction", json={
            "user_id": user_id,
            "date": str(date),
            "amount": amount,
            "category": category,
            "merchant": merchant
        })
        st.rerun()

    # -------- DASHBOARD --------
    summary = requests.get(f"{BASE_URL}/summary/{user_id}").json()

    col1, col2 = st.columns(2)
    col1.metric("Total", summary.get("total_spending",0))
    col2.metric("Average", summary.get("avg_spending",0))

    # Category
    cat = requests.get(f"{BASE_URL}/category/{user_id}").json()
    if cat:
        df = pd.DataFrame(cat.items(), columns=["Category","Amount"])
        st.plotly_chart(px.pie(df, names="Category", values="Amount"))

    # Trend
    trend = requests.get(f"{BASE_URL}/trend/{user_id}").json()
    if trend:
        df = pd.DataFrame(trend.items(), columns=["Month","Amount"])
        st.plotly_chart(px.line(df, x="Month", y="Amount"))

    # AI
    st.subheader("🤖 AI Insights")
    ai = requests.get(f"{BASE_URL}/ai/{user_id}").json()
    for i in ai["insights"]:
        st.info(i)

    # ML
    st.subheader("🧠 ML Anomalies")
    ml = requests.get(f"{BASE_URL}/ml/{user_id}").json()
    if ml["anomalies"]:
        st.dataframe(pd.DataFrame(ml["anomalies"]))
    else:
        st.success("No anomalies")

else:
    st.info("Login to continue")