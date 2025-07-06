import mysql.connector
import sys

# --- Database Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 🔐 Replace with your actual MySQL password
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def connect_to_database():
    """
    Establishes a connection to the ALX_prodev MySQL database.

    Returns:
        MySQLConnection or None: A connection object if successful, otherwise None.
    """
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"[Connection Error] Failed to connect to '{DATABASE_NAME}': {err}", file=sys.stderr)
        return None


def paginate_users(limit, offset):
    """
    Fetches a single page of users using LIMIT and OFFSET.

    Args:
        limit (int): Number of users to fetch.
        offset (int): Starting row number.

    Returns:
        list[dict]: A list of user rows as dictionaries.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_database()
        if not connection or not connection.is_connected():
            return []

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"[Database Error] paginate_users failed: {err}", file=sys.stderr)
    except Exception as e:
        print(f"[Unexpected Error] paginate_users failed: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return []


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of user data.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list[dict]: A page of user records.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


def stream_user_ages():
    """
    Generator that yields user ages one at a time.

    Yields:
        int or float: Age of a user.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_database()
        if not connection or not connection.is_connected():
            print(f"[Error] Cannot stream ages: connection to '{DATABASE_NAME}' failed.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT age FROM {TABLE_NAME}")

        for row in cursor:
            yield row.get('age')

    except mysql.connector.Error as err:
        print(f"[Database Error] stream_user_ages failed: {err}", file=sys.stderr)
    except Exception as e:
        print(f"[Unexpected Error] stream_user_ages failed: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Calculates and prints the average age of users using a memory-efficient stream.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        if age is not None:
            total_age += age
            count += 1

    if count > 0:
        avg = total_age / count
        print(f"📊 Average age of users: {avg:.2f}")
    else:
        print("⚠️ No user data available to calculate average age.")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    PAGE_SIZE = 100

    print(f"🔄 Lazy Pagination with page size = {PAGE_SIZE}")
    try:
        for page_number, page in enumerate(lazy_paginate(PAGE_SIZE), start=1):
            print(f"\n--- Page {page_number} ---")
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()
    except Exception as e:
        print(f"[Runtime Error] Lazy pagination failed: {e}", file=sys.stderr)

    print("\n" + "=" * 50 + "\n")

    print("🧮 Calculating Average Age from Stream:")
    calculate_average_age()
