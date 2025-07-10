import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# ✅ Use the context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    for row in results:
        print(row)