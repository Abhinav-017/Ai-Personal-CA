import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Personal CA", layout="wide")

# -------- CUSTOM CSS --------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: #1E1E2F;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("💸 AI Personal CA Dashboard")

# -------- SESSION --------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------- AUTH --------
st.sidebar.title("🔐 Authentication")

mode = st.sidebar.radio("Mode", ["Login", "Register"])

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
            st.sidebar.error("Invalid credentials")

# -------- USER --------
user_id = st.session_state.user_id

if user_id:

    st.sidebar.success(f"👤 {user_id}")

    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.rerun()

    # -------- ADD TRANSACTION --------
    st.sidebar.subheader("➕ Add Transaction")

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

    # -------- KPI --------
    summary = requests.get(f"{BASE_URL}/summary/{user_id}").json()
    prediction = requests.get(f"{BASE_URL}/predict/{user_id}").json()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Spending", f"₹{summary.get('total_spending',0)}")
    col2.metric("📊 Avg Spending", f"₹{summary.get('avg_spending',0)}")
    col3.metric("🔮 Next Month (Predicted)", f"₹{prediction.get('prediction',0)}")

    st.markdown("---")

    # -------- CHARTS --------
    colA, colB = st.columns(2)

    # Category Pie
    cat = requests.get(f"{BASE_URL}/category/{user_id}").json()
    if cat:
        df = pd.DataFrame(cat.items(), columns=["Category","Amount"])
        fig = px.pie(df, names="Category", values="Amount", hole=0.4)
        colA.plotly_chart(fig, use_container_width=True)

    # Trend
    trend = requests.get(f"{BASE_URL}/trend/{user_id}").json()
    if trend:
        df = pd.DataFrame(trend.items(), columns=["Month","Amount"])
        fig = px.line(df, x="Month", y="Amount", markers=True)
        colB.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------- AI --------
    st.subheader("🤖 AI Insights")
    ai = requests.get(f"{BASE_URL}/ai/{user_id}").json()
    for i in ai["insights"]:
        st.info(i)

    # -------- ML --------
    st.subheader("🧠 ML Anomaly Detection")
    ml = requests.get(f"{BASE_URL}/ml/{user_id}").json()

    if ml["anomalies"]:
        st.dataframe(pd.DataFrame(ml["anomalies"]))
    else:
        st.success("No anomalies detected")

else:
    st.warning("Please login to access your dashboard")