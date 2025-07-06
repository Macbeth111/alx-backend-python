import mysql.connector
import sys

# --- Database Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # IMPORTANT: Replace with your MySQL root password
}
DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def connect_to_prodev():
    """Connects to the ALX_prodev MySQL database."""
    try:
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        return mysql.connector.connect(**db_config_with_db)
    except mysql.connector.Error as err:
        print(f"Connection error: {err}", file=sys.stderr)
        return None

def paginate_users(page_size, offset):
    """
    Fetches a page of user data from the user_data table using LIMIT and OFFSET.
    """
    try:
        connection = connect_to_prodev()
        if not connection or not connection.is_connected():
            return []
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(f"Error in paginate_users: {e}", file=sys.stderr)
        return []

def lazypaginate(page_size):
    """
    Generator that lazily fetches user pages from the database one page at a time.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        yield users
        offset += page_size

# Example usage
if __name__ == "__main__":
    try:
        for page in lazypaginate(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()
