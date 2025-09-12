from contextlib import contextmanager
import sqlite3


class DatabaseConnection:
    def __init__(self):
        dbname="ALX_prodev"
        self.cursor = None
        self.connection =  None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname) 
        self.cursor = self.connection.cursor()
        return self.cursor
        
    def __exit__(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.close()
        

with DatabaseConnection("ALX_prodev") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print (results)
        
        