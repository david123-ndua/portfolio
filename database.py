import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "portfolio.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ==========================
    # Admin Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Projects Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT NOT NULL,

            technologies TEXT NOT NULL,

            github TEXT,

            live_demo TEXT,

            image TEXT,

            featured INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Create Default Admin
    # ==========================

    cursor.execute(
        "SELECT id FROM admins WHERE username=?",
        ("admin",)
    )

    admin_exists = cursor.fetchone()

    if admin_exists is None:

        password = generate_password_hash("admin123")

        cursor.execute("""
            INSERT INTO admins
            (username, password_hash)
            VALUES (?, ?)
        """, ("admin", password))

        print("✓ Default admin created")

    else:

        print("✓ Admin already exists")

    conn.commit()
    conn.close()

    print("✓ Database Ready")


if __name__ == "__main__":
    create_database()