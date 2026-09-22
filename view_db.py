import sqlite3

conn = sqlite3.connect("portfolio.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

for table in tables:

    table_name = table["name"]

    print("\n" + "="*60)
    print(table_name.upper())
    print("="*60)

    rows = cursor.execute(
        f"SELECT * FROM {table_name}"
    ).fetchall()

    if not rows:

        print("No records found.")

    else:

        for row in rows:

            print(dict(row))

conn.close()