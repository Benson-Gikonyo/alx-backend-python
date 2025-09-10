#!/usr/bin/python3
import mysql.connector
import csv
import uuid
import os

CSV_FILE = "user_data.csv"

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

def insert_data_from_csv(connection, csv_file):
    """Insert data from CSV into user_data table."""
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    data_to_insert = []

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = str(uuid.uuid4())  # generate unique ID
            name = row["name"].strip()
            email = row["email"].strip()
            age = int(row["age"].strip())
            data_to_insert.append((user_id, name, email, age))

    try:
        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records from {csv_file}.")
    except Exception as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    db_conn = connect_to_prodev()
    if not db_conn:
        exit(1)

    insert_data_from_csv(db_conn, CSV_FILE)
    db_conn.close()
