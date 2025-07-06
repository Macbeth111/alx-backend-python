import mysql.connector
from itertools import islice

# --- Database Configuration (Self-contained setup) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 🔐 Replace with your actual MySQL password
}

# Define the target database and table
DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def stream_users():
    """
    Generator function that connects to a MySQL database and yields
    rows from the 'user_data' table one at a time as dictionaries.

    This is useful for memory-efficient streaming of large datasets.
    """
    connection = None
    cursor = None

    try:
        # Add database name to DB config
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME

        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config_with_db)

        # Verify that the connection was successful
        if not connection.is_connected():
            print(f"[ERROR] Failed to connect to database '{DATABASE_NAME}'.")
            return  # Exit the generator if connection fails

        # Create a cursor that returns each row as a dictionary
        cursor = connection.cursor(dictionary=True)

        # Define SQL query to retrieve relevant user data
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        # Stream results one by one using a single loop (as required)
        for row in cursor:
            yield row  # Yield each row as a dictionary

    except mysql.connector.Error as db_err:
        print(f"[MySQL Error] {db_err}")
    except Exception as ex:
        print(f"[Unexpected Error] {ex}")
    finally:
        # Always close the cursor and connection to free resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# --- Example usage of the generator (for demonstration/testing) ---
if __name__ == "__main__":
    print("🔄 Streaming first 6 users from the database:")
    for user in islice(stream_users(), 6):
        print(user)

    print("\n🔁 Streaming next 3 users (new stream instance):")
    # Each call to stream_users() starts a fresh generator
    for user in islice(stream_users(), 3):
        print(user)
