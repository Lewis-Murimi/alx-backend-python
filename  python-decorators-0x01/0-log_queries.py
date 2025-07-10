import sqlite3
import functools

#### decorator to log SQL queries

def log_queries():
    """
    Decorator that logs the SQL query before executing the function.
    Assumes the first argument to the decorated function is the SQL query string.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = args[0] if args else kwargs.get('query', 'No query provided')
            print(f"[LOG] Executing SQL query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
