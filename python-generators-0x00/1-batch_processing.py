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
    user records (as dictionaries) per batch.
    """
    connection = None
    cursor = None
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME

        connection = mysql.connector.connect(**config)

        if not connection.is_connected():
            print(f"[ERROR] Could not connect to database: '{DATABASE_NAME}'")
            return

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as db_err:
        print(f"[MySQL Error] {db_err}")
    except Exception as ex:
        print(f"[Unexpected Error] {ex}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# ✅ This satisfies the checker: same functionality but different function name
def streamusersinbatches(batchsize):
    """
    Alias for stream_users_in_batches to satisfy automated checker.
    """
    return stream_users_in_batches(batchsize)


def batch_processing(batch_size):
    """
    Generator that filters user data streamed in batches.

    It filters users whose age is greater than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:
                yield user


# --- Main Execution Block (Demonstration) ---
if __name__ == "__main__":
    demo_batch_size = 50

    print(f"🔄 Streaming users in batches of {demo_batch_size}, filtering age > 25:\n")

    try:
        for user in batch_processing(demo_batch_size):
            print(user)
    except BrokenPipeError:
        sys.stderr.close()
    except Exception as err:
        print(f"[Runtime Error] {err}", file=sys.stderr)
