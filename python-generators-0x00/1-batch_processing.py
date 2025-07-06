import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that yields individual users from the database in batches.
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

        for row in rows:
            yield row  # ✅ Yield individual user, not a batch

        offset += batch_size

def batch_processing(batch_size):
    """
    Processes each user from stream_users_in_batches and filters users older than 25.
    """
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            print(user)
