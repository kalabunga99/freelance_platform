import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="freelance_platform"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not connect to the MySQL database.\n\nDetails: {e}\n\nPlease check if your MySQL server is running."
        )
        return None
