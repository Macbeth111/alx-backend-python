import mysql.connector
import sys

# --- Database Configuration (Self-contained and reusable) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 🔐 Replace with your actual password before use
}

# Database and table settings
DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def stream_users_in_batches(batch_size):
    """
    Streams users from the database in batches of a specified size.

    This function connects to the MySQL database and yields a list of
    user records (as dictionaries) per batch. It's efficient for handling
    large datasets that can't be loaded all at once.

    Args:
        batch_size (int): Number of rows to fetch per batch.

    Yields:
        List[dict]: A batch (list) of user rows.
    """
    connection = None
    cursor = None
    try:
        # Merge DB config with specific database name
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME

        # Establish the database connection
        connection = mysql.connector.connect(**config)

        if not connection.is_connected():
            print(f"[ERROR] Could not connect to database: '{DATABASE_NAME}'")
            return  # Exit early if connection fails

        # Create a dictionary-style cursor for readable column access
        cursor = connection.cursor(dictionary=True)

        # Execute the query to retrieve user data
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        # Continuously fetch data in batches until no more data remains
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break  # Exit loop when no more data
            yield batch  # Yield each batch as a list of dictionaries

    except mysql.connector.Error as db_err:
        print(f"[MySQL Error] {db_err}")
    except Exception as ex:
        print(f"[Unexpected Error] {ex}")
    finally:
        # Always clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Generator that filters user data streamed in batches.

    It filters users whose age is greater than 25.

    Args:
        batch_size (int): Size of each database fetch batch.

    Yields:
        dict: A dictionary representing a filtered user record.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:  # Use .get() for safety
                yield user


# --- Main Execution Block (Demonstration) ---
if __name__ == "__main__":
    demo_batch_size = 50  # Adjust this as needed

    print(f"🔄 Streaming users in batches of {demo_batch_size}, filtering age > 25:\n")

    try:
        for user in batch_processing(demo_batch_size):
            print(user)
    except BrokenPipeError:
        # Handle early termination (e.g., when piped to `head`)
        sys.stderr.close()
    except Exception as err:
        print(f"[Runtime Error] {err}", file=sys.stderr)
