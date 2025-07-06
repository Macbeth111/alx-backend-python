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
    Generator that fetches rows from the user_data table in batches of `batchsize`.
    Yields a list of user records per batch.
    """
    connection = None
    cursor = None
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME

        connection = mysql.connector.connect(**config)

        if not connection.is_connected():
            print(f"Could not connect to database '{DATABASE_NAME}'")
            return

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        while True:
            batch = cursor.fetchmany(batchsize)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batchsize):
    """
    Generator that filters users older than 25 from batches.
    """
    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                print(user)  # As per test expectations, print instead of yield
