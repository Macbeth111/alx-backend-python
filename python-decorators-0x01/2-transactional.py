# File: 2-transactional.py
import sqlite3
import functools

# ✅ Reusing the connection decorator from Task 1


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ New transactional decorator


def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction failed: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))


# ✅ Test the transactional decorator
update_user_email(user_id=1, new_email='new_email@example.com')
