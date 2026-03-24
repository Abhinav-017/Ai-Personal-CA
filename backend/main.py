from fastapi import FastAPI, Body
from services import (
    get_user_data,
    get_summary,
    category_analysis,
    spending_trend,
    detect_leaks,
    tax_insights,
    advanced_ai_insights
)
from database import get_connection

app = FastAPI()

# ---------------- DATABASE INIT ----------------
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    date TEXT,
    amount REAL,
    category TEXT,
    merchant TEXT
)
""")

conn.commit()
conn.close()

# ---------------- ROUTES ----------------

@app.get("/")
def home():
    return {"message": "AI Personal CA Backend Running 🚀"}


# ---------------- USER BASED APIs ----------------

@app.get("/summary/{user_id}")
def summary(user_id: str):
    df = get_user_data(user_id)
    return get_summary(df)


@app.get("/category/{user_id}")
def category(user_id: str):
    df = get_user_data(user_id)
    return category_analysis(df)


@app.get("/trend/{user_id}")
def trend(user_id: str):
    df = get_user_data(user_id)
    return spending_trend(df)


@app.get("/leaks/{user_id}")
def leaks(user_id: str):
    df = get_user_data(user_id)
    return detect_leaks(df)


@app.get("/tax/{user_id}")
def tax(user_id: str):
    df = get_user_data(user_id)
    return tax_insights(df)


@app.get("/ai/{user_id}")
def ai(user_id: str):
    df = get_user_data(user_id)
    return {"insights": advanced_ai_insights(df)}


# ---------------- ADD TRANSACTION ----------------

@app.post("/add_transaction")
def add_transaction(data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (user_id, date, amount, category, merchant)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["user_id"],
        data["date"],
        data["amount"],
        data["category"],
        data["merchant"]
    ))

    conn.commit()
    conn.close()

    return {"message": "Transaction added successfully"}
