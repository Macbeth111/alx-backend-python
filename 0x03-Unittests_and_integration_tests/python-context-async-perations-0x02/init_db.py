import sqlite3


def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER
        )
    ''')

    # Insert sample users
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 45),
        ("Eve", "eve@example.com", 22)
    ]

    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users)
    conn.commit()
    conn.close()
    print("Database initialized with sample data.")


if __name__ == "__main__":
    initialize_db()
