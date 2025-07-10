import sqlite3
import functools
from datetime import datetime


def log_queries():
    @functools.wraps()
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or args[0] if args else None
        timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        print(f'{timestamp}[LOG] running sql {query}')
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query


users = fetch_all_users(query="SELECT * FROM users")
