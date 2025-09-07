import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# db connection
def connect_db():
    """Connect to MySQL server (no specific database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # replace with your MySQL username
            password="password"   # replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # replace with your MySQL username
            password="password",  # replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table user_data ready.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert user data if it does not already exist."""
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    data_to_insert = []
    with open('user_data.csv', newline="") as f:
        reader = csv.DictReader(f)  # handles quoted headers automatically
        for row in reader:
            user_id = str(uuid.uuid4())  # generate a UUID
            name = row["name"].strip('"')   # remove surrounding quotes if any
            email = row["email"].strip('"')
            age = int(row["age"].strip('"'))  # convert age to integer
            data_to_insert.append((user_id, name, email, age))

    try:
        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records.")
    except Exception as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

# ---------- MAIN SCRIPT ----------
if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    server_conn = connect_db()
    if not server_conn:
        exit(1)

    # Step 2: Create database if not exists
    create_database(server_conn)
    server_conn.close()

    # Step 3: Connect to ALX_prodev
    db_conn = connect_to_prodev()
    if not db_conn:
        exit(1)

    # Step 4: Create table if not exists
    create_table(db_conn)

    # Step 5: Read CSV data
    data_to_insert = []
    with open("user_data.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())  
            name = row["name"]
            email = row["email"]
            age = row["age"]
            data_to_insert.append((user_id, name, email, age))

    # Step 6: Insert into DB
    insert_data(db_conn, data_to_insert)

    # Step 7: Close DB connection
    db_conn.close()
