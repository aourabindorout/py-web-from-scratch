from database.db import get_connection


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_all_posts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, body FROM posts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, body FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def create_post(title, body):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, body) VALUES (?, ?)", (title, body))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id