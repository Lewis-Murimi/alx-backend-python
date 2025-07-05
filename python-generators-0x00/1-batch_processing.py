import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
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

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error fetching batches: {e}")
        return


def batch_processing(batch_size):
    """
    Processes users in batches, yielding only those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user['age'] > 25:
                print(user)
