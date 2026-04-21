"""
database.py — SQLite orqali foydalanuvchilar va statistikani saqlash
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "yuristaziz.db")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                full_name   TEXT,
                lang        TEXT DEFAULT 'uz',
                is_lawyer   INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key   TEXT PRIMARY KEY,
                value INTEGER DEFAULT 0
            )
        """)
        # Init stats rows
        cur.execute("INSERT OR IGNORE INTO stats(key,value) VALUES('questions',0)")
        self.conn.commit()

    # ── Users ──────────────────────────────

    def add_user(self, user_id: int, username: str, full_name: str):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO users(user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))
        # Update name/username if already exists
        cur.execute("""
            UPDATE users SET username=?, full_name=?
            WHERE user_id=?
        """, (username, full_name, user_id))
        self.conn.commit()

    def get_all_users(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT user_id FROM users")
        return [row[0] for row in cur.fetchall()]

    def get_users_count(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]

    def get_user_lang(self, user_id: int) -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT lang FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else "uz"

    def set_user_lang(self, user_id: int, lang: str):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
        self.conn.commit()

    def set_lawyer_session(self, user_id: int, active: bool):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE users SET is_lawyer=? WHERE user_id=?",
            (1 if active else 0, user_id)
        )
        self.conn.commit()

    # ── Stats ──────────────────────────────

    def increment_questions(self):
        cur = self.conn.cursor()
        cur.execute("UPDATE stats SET value=value+1 WHERE key='questions'")
        self.conn.commit()

    def get_questions_count(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM stats WHERE key='questions'")
        row = cur.fetchone()
        return row[0] if row else 0
