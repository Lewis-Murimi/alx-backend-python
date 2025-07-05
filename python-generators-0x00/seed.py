import csv
import uuid
import mysql.connector
from mysql.connector import Error


def connect_db():
    """Connect to MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_username',
            password='your_mysql_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_username',
            password='your_mysql_password',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def read_csv_generator(filename):
    """Generator that reads the CSV file row by row."""
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield {
                'user_id': str(uuid.uuid4()),
                'name': row['name'],
                'email': row['email'],
                'age': float(row['age'])  # ensure age is numeric
            }


def insert_data(connection, csv_file):
    """Insert data from CSV into the database using a generator."""
    try:
        cursor = connection.cursor()
        existing_ids = set()

        # Optional optimization: track existing records
        cursor.execute("SELECT user_id FROM user_data")
        existing_ids.update(row[0] for row in cursor.fetchall())

        for row in read_csv_generator(csv_file):
            if row['user_id'] in existing_ids:
                continue
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
