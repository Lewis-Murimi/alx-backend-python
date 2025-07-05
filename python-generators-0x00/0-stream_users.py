import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that yields rows from the user_data table one by one.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_username',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Database error: {e}")
        return
