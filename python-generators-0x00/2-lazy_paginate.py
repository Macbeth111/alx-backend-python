import mysql.connector
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}
DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def connect_to_prodev():
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Connection error: {err}", file=sys.stderr)
        return None

def paginate_users(pagesize, offset):
    try:
        connection = connect_to_prodev()
        if not connection or not connection.is_connected():
            return []
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s"
        cursor.execute(query, (pagesize, offset))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(f"Error in paginate_users: {e}", file=sys.stderr)
        return []

def lazypaginate(pagesize):
    offset = 0
    while True:
        page = paginate_users(pagesize, offset)
        if not page:
            break
        yield page
        offset += pagesize
