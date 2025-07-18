# File: 0-databaseconnection.py

import sqlite3


class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # gives you access to use it

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()  # always closes even if there's an error


# ✅ Use the context manager to run a query
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
