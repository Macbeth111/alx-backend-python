import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches from the user_data table.
    """
    offset = 0
    while True:
        conn = connect_to_prodev()
        if not conn:
            break
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            break

        yield rows  # Yield a full batch (list of dicts)
        offset += batch_size

def batch_processing(batch_size):
    """
    Processes each batch from the generator, filters users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
