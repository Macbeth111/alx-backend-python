import mysql.connector
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def streamusersinbatches(batchsize):
    """
    Generator that fetches rows in batches from the user_data table.
    Yields a list of rows per batch.
    """
    connection = None
    cursor = None
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)

        if not connection.is_connected():
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        while True:
            batch = cursor.fetchmany(batchsize)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batchsize):
    """
    Prints users older than 25, using streamusersinbatches.
    """
    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                print(user)
