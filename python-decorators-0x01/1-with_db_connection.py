import sqlite3 
import functools

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
        return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)