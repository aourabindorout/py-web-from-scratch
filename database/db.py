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
            name TEXT NOT NULL DEFAULT '',
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            user_id INTEGER,
            author_name TEXT DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
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

    # Migrations for existing databases
    user_cols = [r[1] for r in cursor.execute("PRAGMA table_info(users)").fetchall()]
    if "name" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN name TEXT DEFAULT ''")

    post_cols = [r[1] for r in cursor.execute("PRAGMA table_info(posts)").fetchall()]
    if "user_id" not in post_cols:
        cursor.execute("ALTER TABLE posts ADD COLUMN user_id INTEGER DEFAULT 1")
    if "author_name" not in post_cols:
        cursor.execute("ALTER TABLE posts ADD COLUMN author_name TEXT DEFAULT 'Admin'")
    if "created_at" not in post_cols:
        cursor.execute("ALTER TABLE posts ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    # Seed initial sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        from utils.security import hash_password
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            ("Administrator", "admin", hash_password("admin123"))
        )
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            ("John Doe", "john", hash_password("john123"))
        )

    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO posts (title, body, user_id, author_name) VALUES (?, ?, ?, ?)",
            ("Learning Python", "Python is a versatile programming language with a clean, readable syntax.", 1, "Administrator")
        )
        cursor.execute(
            "INSERT INTO posts (title, body, user_id, author_name) VALUES (?, ?, ?, ?)",
            ("Building My Own Web Framework", "Building web frameworks from scratch helps you understand sockets, HTTP protocols, and routing.", 2, "John Doe")
        )

    conn.commit()
    conn.close()


