import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    """ decorator that automatically handles opening and closing database connections""" 
    def wrapper(*args, **kwargs):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",          # replace with your MySQL username
                password="password",  # replace with your MySQL password
                database="ALX_prodev"
            )            
            return func(connection, *args, **kwargs)
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        
        finally:
            if connection:
                connection.close()
                
def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        else:
            print("Executing query and caching result:", query)
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

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
