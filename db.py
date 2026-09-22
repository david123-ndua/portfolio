import os
import sqlite3


# ==================================================
# DATABASE LOCATION
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "instance",
    "portfolio.db"
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db_connection():

    # Make sure the instance folder exists
    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    """Create tables if they don't exist. Safe to run every startup."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            technologies TEXT,
            github_link TEXT,
            image TEXT,
            featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
    def seed_admin():
    """Create a default admin if the admins table is empty."""
    conn = get_db_connection()

    existing = conn.execute(
        "SELECT COUNT(*) FROM admins"
    ).fetchone()[0]

    if existing == 0:
        from werkzeug.security import generate_password_hash

        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD", "changeme123")

        conn.execute(
            """
            INSERT INTO admins (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                generate_password_hash(password)
            )
        )
        conn.commit()
        print(f"✅ Default admin created: {username}")

    conn.close()