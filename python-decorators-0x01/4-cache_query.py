# File: 4-cache_query.py
import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

# ✅ Reuse connection handler


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Caching decorator


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE] Returning cached result for: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Executing and caching: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ✅ First call - hits the DB
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call - returns from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
