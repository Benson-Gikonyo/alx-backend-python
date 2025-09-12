from contextlib import contextmanager
import sqlite3

class ExecuteQuery:
    """reusable context manager that takes a query as input and executes it, managing both connection and the query execution"""
    def __init__(self, dbname, query, params):
        self.dbname="ALX_prodev"
        self.query = query
        self.params=params
        self.conn = None
        self.cursor = None
        self.result = None
    
    def __enter__():
        self.conn = sqlite3.connect(self.dbname) 
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result
    
    def __exit__():
        if self.cursor:
            self.cursor.close()
        
        if self.conn:
            self.conn.close()
            
            
if __name__ == __main__():
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
with ExecuteQuery("ALX_prodev", query, params) as results:
    print (results)
    