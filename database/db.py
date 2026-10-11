import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)


    # Seed initial sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("john", "john123"))

    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO posts (title, body) VALUES (?, ?)",
            ("Learning Python", "Python is a versatile programming language with a clean, readable syntax.")
        )
        cursor.execute(
            "INSERT INTO posts (title, body) VALUES (?, ?)",
            ("Building My Own Web Framework", "Building web frameworks from scratch helps you understand sockets, HTTP protocols, and routing.")
        )

    conn.commit()
    conn.close()

