import seed


def stream_user_ages():
    """
    Generator that yields ages of all users one by one.
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # Tuple unpacking from single-column fetch
            yield age

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")


def compute_average_age():
    """
    Computes and prints the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # First and only loop
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
