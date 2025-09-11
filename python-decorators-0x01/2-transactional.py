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

def transactional(func):
    """decorator that manages database transactions by automatically committing or rolling back changes"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back due to error:", e)
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
