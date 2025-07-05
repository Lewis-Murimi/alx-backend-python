import seed


def paginate_users(page_size, offset):
    """
    Fetch a page of users with LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily yields each page of users using pagination.
    Uses only one loop and fetches the next page only when needed.
    """
    offset = 0
    while True:  # This counts as the ONE allowed loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
