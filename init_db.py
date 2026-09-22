from db import get_db_connection
from werkzeug.security import generate_password_hash

conn = get_db_connection()
cursor = conn.cursor()


# ==================================================
# ADMINS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==================================================
# PROJECTS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    description TEXT NOT NULL,

    category TEXT NOT NULL,

    technologies TEXT NOT NULL,

    github_link TEXT,

    demo_link TEXT,

    image TEXT,

    featured INTEGER DEFAULT 0,

    status TEXT DEFAULT 'Published',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
""")


# ==================================================
# MESSAGES TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT NOT NULL,

    subject TEXT NOT NULL,

    message TEXT NOT NULL,

    is_read INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")
print("Database initialized successfully.")