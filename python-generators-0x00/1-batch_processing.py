import mysql.connector
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Replace if necessary
    'database': 'ALX_prodev'
}

TABLE_NAME = 'user_data'


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from the database in batches.
    Yields each batch as a list of dictionaries.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def batch_processing(batch_size):
    """
    Processes users in batches and prints only those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
