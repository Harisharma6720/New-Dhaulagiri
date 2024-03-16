import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import the ttk module for Treeview
import mysql.connector

def submit_form():
    # Retrieve data from the form 
    item_name = entry_item_name.get()

    # Validate that all fields are filled
    if not item_name:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new dhaulagiri enterprises"
        )

        cursor = connection.cursor()

        # Insert data into the 'item' table
        query = "INSERT INTO item (item_name) VALUES (%s)"
        cursor.execute(query, (item_name,))

        # Commit the changes
        connection.commit()

        # Display success message
        messagebox.showinfo("Success", "Item details submitted successfully.")

        # Update the Treeview with the entered item
        update_item_treeview()

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        messagebox.showerror("Error", "An error occurred while connecting to the database.")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

        # Clear the form fields
        entry_item_name.delete(0, tk.END)

def update_item_treeview():
    # Clear existing items in the Treeview
    for i in item_treeview.get_children():
        item_treeview.delete(i)

    # Connect to MySQL database to fetch item list
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new dhaulagiri enterprises"
        )

        cursor = connection.cursor()

        # Fetch all items from the 'item' table
        query = "SELECT * FROM item"
        cursor.execute(query)

        # Fetch all results
        items = cursor.fetchall()

        # Populate the Treeview with the retrieved items and column names
        for item in items:
            item_treeview.insert('', tk.END, values=item)

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        messagebox.showerror("Error", "An error occurred while connecting to the database.")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create the main Tkinter window
root = tk.Tk()
root.title("Item Entry Form")

# Form fields
label_item_name = tk.Label(root, text="Item Name:")
label_item_name.pack()
entry_item_name = tk.Entry(root)
entry_item_name.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack(pady=10)

# Treeview to display entered items in a table
columns = ('ID', 'Item Name')
item_treeview = ttk.Treeview(root, columns=columns, show='headings')
item_treeview.heading('ID', text='ID')
item_treeview.heading('Item Name', text='Item Name')
item_treeview.pack()

# Button to update the item list
update_button = tk.Button(root, text="Update Item Table", command=update_item_treeview)
update_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
