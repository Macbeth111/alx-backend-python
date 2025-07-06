import mysql.connector
import csv
import uuid
import os
import sys

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 🔐 Replace with your actual MySQL root password
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'


def connect_to_mysql_server():
    """Establish connection to MySQL server (no DB selected)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL server.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ MySQL server connection error: {err}", file=sys.stderr)
        return None


def create_database_if_not_exists(connection):
    """Create the database if it doesn't already exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
            print(f"✅ Database '{DATABASE_NAME}' ready.")
    except mysql.connector.Error as err:
        print(f"❌ Database creation error: {err}", file=sys.stderr)


def connect_to_database():
    """Connect to the specific database (ALX_prodev)."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        conn = mysql.connector.connect(**config)
        print(f"✅ Connected to database '{DATABASE_NAME}'.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}", file=sys.stderr)
        return None


def create_user_table(connection):
    """Create user_data table with constraints if it doesn't exist."""
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3, 0) NOT NULL
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print(f"✅ Table '{TABLE_NAME}' ready.")
    except mysql.connector.Error as err:
        print(f"❌ Table creation error: {err}", file=sys.stderr)


def read_csv(filepath):
    """Reads user data from CSV into a list of dictionaries."""
    if not os.path.exists(filepath):
        print(f"⚠️ CSV file not found at '{filepath}'")
        return []

    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            print(f"📥 Loaded {len(data)} rows from CSV.")
            return data
    except Exception as e:
        print(f"❌ Error reading CSV: {e}", file=sys.stderr)
        return []


def insert_user_data(connection, rows):
    """Insert users into the database. Skips duplicates based on email."""
    if not rows:
        print("⚠️ No user data to insert.")
        return

    insert_query = f"""
    INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    inserted_count = 0

    try:
        with connection.cursor() as cursor:
            for row in rows:
                try:
                    age = int(float(row['age']))
                    values = (str(uuid.uuid4()), row['name'], row['email'], age)
                    cursor.execute(insert_query, values)
                    if cursor.rowcount > 0:
                        inserted_count += 1
                except (ValueError, KeyError) as err:
                    print(f"⚠️ Skipping invalid row: {row} | Error: {err}")
                except mysql.connector.Error as err:
                    print(f"❌ Insert error: {err} | Row: {row}", file=sys.stderr)

            connection.commit()
            print(f"✅ Inserted {inserted_count} new users.")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"❌ Batch insert failed: {err}", file=sys.stderr)


def create_sample_csv(filepath):
    """Creates a sample CSV file if it doesn't exist."""
    sample_data = [
        ['name', 'email', 'age'],
        ['John Doe', 'john.doe@example.com', '30'],
        ['Jane Smith', 'jane.smith@example.com', '25'],
        ['Peter Jones', 'peter.jones@example.com', '40'],
        ['Alice Brown', 'alice.brown@example.com', '35'],
        ['Bob White', 'bob.white@example.com', '28'],
        ['Charlie Green', 'charlie.green@example.com', '45'],
    ]
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    print(f"📄 Created sample CSV at '{filepath}'.")


def main():
    # Create dummy CSV for demonstration
    if not os.path.exists(CSV_FILE):
        create_sample_csv(CSV_FILE)

    server_conn = connect_to_mysql_server()
    if not server_conn:
        sys.exit("🚫 Exiting: Unable to connect to MySQL server.")
    create_database_if_not_exists(server_conn)
    server_conn.close()

    db_conn = connect_to_database()
    if not db_conn:
        sys.exit("🚫 Exiting: Unable to connect to database.")

    create_user_table(db_conn)
    csv_data = read_csv(CSV_FILE)
    insert_user_data(db_conn, csv_data)

    db_conn.close()
    print("✅ ETL process complete. Connection closed.")


if __name__ == "__main__":
    main()
