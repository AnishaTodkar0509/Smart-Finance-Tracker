import sqlite3
import os
from config import DB_PATH

# Ensure database folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def connect_db():
    return sqlite3.connect(DB_PATH)


# 🔹 Create both tables
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # TRANSACTIONS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Tables created successfully")


# 🔹 Insert transaction
def insert_transaction(t, user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO transactions (amount, category, type, date, user_id) VALUES (?, ?, ?, ?, ?)",
            (t.amount, t.category, t.type, t.date, user_id)
        )
        conn.commit()
        print("✅ Transaction inserted")

    except Exception as e:
        print("❌ Error inserting transaction:", e)

    finally:
        conn.close()


# 🔹 Register user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("✅ User registered")
        return True

    except sqlite3.IntegrityError:
        print("❌ Username already exists")
        return False

    finally:
        conn.close()


# 🔹 Login user
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        print("✅ Login successful")
        return result[0]
    else:
        print("❌ Login failed")
        return None


# 🔹 Get user transactions
def get_user_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount, category, type, date FROM transactions WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()

    print(f"✅ Loaded {len(data)} transactions")

    return data