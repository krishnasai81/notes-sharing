import sqlite3

def connect_db():
    return sqlite3.connect("database.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # Create notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        author TEXT
    )
    """)

    # ✅ Insert default user (only if not exists)
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            ("admin", "1234", "student")
        )
        print("✅ Default user created: admin / 1234")

    conn.commit()
    conn.close()