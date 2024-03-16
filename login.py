import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

# Function to validate user login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new dhaulagiri enterprises"
        )

        cursor = connection.cursor()

        # Execute SQL query to check if the username and password are valid
        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            open_another_file()
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        messagebox.showerror("Error", "An error occurred while connecting to the database")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def open_another_file():
    try:
        subprocess.Popen(['python',r'C:\Users\ASUS\Desktop\new dhaulagiri\menubar.py'])
    except Exception as e:
        print(f"Error opening the file: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("welcome to new dhaulagiri enterprises")

# Username and password entry fields
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Login button
login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()