import sqlite3

DB_PATH = "referral_bot.db"

# ✅ Bazani yaratish
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            invited_by INTEGER
        )
    """)
    conn.commit()
    conn.close()


# ✅ Foydalanuvchini qo‘shish
def add_user(user_id: int, invited_by: int = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Agar foydalanuvchi mavjud bo‘lmasa qo‘shamiz
    cur.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (user_id, invited_by) VALUES (?, ?)", (user_id, invited_by))
    
    conn.commit()
    conn.close()


# ✅ Foydalanuvchining referallar soni
def count_referrals(user_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE invited_by=?", (user_id,))
    result = cur.fetchone()[0]
    conn.close()
    return result
