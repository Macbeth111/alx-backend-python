import mysql.connector
import sys

# --- Database Configuration (Self-contained for reuse) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 🔐 Replace with your actual MySQL root password
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def connect_to_database():
    """
    Establishes a connection to the ALX_prodev MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection or None:
        Connection object if successful, None otherwise.
    """
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"[Connection Error] Could not connect to '{DATABASE_NAME}': {err}", file=sys.stderr)
        return None


def fetch_user_page(page_size, offset):
    """
    Fetches a single page of user records using LIMIT and OFFSET.

    Args:
        page_size (int): Number of records to fetch.
        offset (int): Number of records to skip before starting.

    Returns:
        List[dict]: A list of user rows as dictionaries.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_database()
        if not connection or not connection.is_connected():
            return []

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"[Database Error] fetch_user_page failed: {err}", file=sys.stderr)
    except Exception as ex:
        print(f"[Unexpected Error] fetch_user_page failed: {ex}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return []


def lazy_paginate_users(page_size):
    """
    Lazily paginates through the user_data table, yielding one page at a time.

    Args:
        page_size (int): Number of records per page.

    Yields:
        List[dict]: A page of user rows.
    """
    offset = 0
    while True:
        page = fetch_user_page(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# --- Example Usage (For Testing or Integration) ---
if __name__ == "__main__":
    DEMO_PAGE_SIZE = 100  # Set desired page size

    print(f"📄 Lazy pagination of users with page size: {DEMO_PAGE_SIZE}\n")

    try:
        for page_num, page in enumerate(lazy_paginate_users(DEMO_PAGE_SIZE), start=1):
            print(f"--- Page {page_num} (Offset: {(page_num - 1) * DEMO_PAGE_SIZE}) ---")
            for user in page:
                print(user)
    except BrokenPipeError:
        # Handles cases like piping output to `head`
        sys.stderr.close()
    except Exception as err:
        print(f"[Runtime Error] Pagination failed: {err}", file=sys.stderr)
