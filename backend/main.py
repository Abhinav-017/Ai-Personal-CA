from fastapi import FastAPI, Body
from backend.services import *
from backend.database import get_connection

app = FastAPI()

# -------- DB INIT --------
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

# -------- AUTH --------
@app.post("/register")
def register(data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data["username"], data["password"])
        )
        conn.commit()
        return {"message": "User created"}
    except:
        return {"error": "User exists"}
    finally:
        conn.close()


@app.post("/login")
def login(data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"user_id": data["username"]}
    return {"error": "Invalid credentials"}


# -------- APIs --------
@app.get("/summary/{user_id}")
def summary(user_id: str):
    return get_summary(get_user_data(user_id))


@app.get("/category/{user_id}")
def category(user_id: str):
    return category_analysis(get_user_data(user_id))


@app.get("/trend/{user_id}")
def trend(user_id: str):
    return spending_trend(get_user_data(user_id))


@app.get("/leaks/{user_id}")
def leaks(user_id: str):
    return detect_leaks(get_user_data(user_id))


@app.get("/tax/{user_id}")
def tax(user_id: str):
    return tax_insights(get_user_data(user_id))


@app.get("/ai/{user_id}")
def ai(user_id: str):
    return {"insights": advanced_ai_insights(get_user_data(user_id))}


@app.get("/ml/{user_id}")
def ml(user_id: str):
    return detect_anomalies_ml(get_user_data(user_id))


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

    return {"message": "Added"}
