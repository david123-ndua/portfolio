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