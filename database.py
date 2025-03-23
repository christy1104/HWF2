import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for storing users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert a sample admin user (username: admin, password: admin123)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete!")