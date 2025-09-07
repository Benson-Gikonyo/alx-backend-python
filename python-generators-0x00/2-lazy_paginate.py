#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a page of users from user_data table with LIMIT + OFFSET."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches pages of users (one loop only)."""
    offset = 0
    while True:   # ✅ only one loop
        page = paginate_users(page_size, offset)
        if not page:   # stop when no more rows
            return
        yield page
        offset += page_size
