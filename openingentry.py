import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class OpeningEntryForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Opening Entry")

        # Combobox to select item
        self.combo_item = ttk.Combobox(root, state="edit", width=30)
        self.combo_item.set("Select Item")
        self.combo_item.pack(padx=10, pady=10)

        # Entry fields for MRP, date, and quantity
        self.entry_mrp = tk.Entry(root)
        self.entry_date = tk.Entry(root)
        self.entry_quantity = tk.Entry(root)
        self.entry_date.insert(0, self.get_current_date())  # Insert current date

        # Labels for MRP, date, and quantity
        label_mrp = tk.Label(root, text="MRP:")
        label_date = tk.Label(root, text="Date:")
        label_quantity = tk.Label(root, text="Quantity:")

        # Submit button
        submit_button = tk.Button(root, text="Submit", command=self.submit_form)

        # Arrange fields and labels on the form
        label_mrp.pack(pady=5)
        self.entry_mrp.pack(pady=5)
        label_date.pack(pady=5)
        self.entry_date.pack(pady=5)
        label_quantity.pack(pady=5)
        self.entry_quantity.pack(pady=5)
        submit_button.pack(pady=10)

        # Fetch and display item names in the combo box
        self.update_item_combobox()

        # Create and populate the table
        self.create_table()

    def update_item_combobox(self):
        # Clear existing items in the combo box
        self.combo_item['values'] = ()

        # Connect to MySQL database to fetch item names
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="new dhaulagiri enterprises"
            )

            cursor = connection.cursor()

            # Fetch item names from the 'item' table
            query = "SELECT item_name FROM item"
            cursor.execute(query)

            # Fetch all results
            items = cursor.fetchall()

            # Populate the combo box with the retrieved item names
            item_names = [item[0] for item in items]
            self.combo_item['values'] = tuple(item_names)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            messagebox.showerror("Error", "An error occurred while connecting to the database.")

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

    def submit_form(self):
        # Retrieve selected item from the combo box
        selected_item = self.combo_item.get()

        if not selected_item or selected_item == "Select Item":
            messagebox.showerror("Error", "Please select an item.")
            return

        # Retrieve MRP, date, and quantity from entry fields
        mrp = self.entry_mrp.get()
        date = self.entry_date.get()
        quantity = self.entry_quantity.get()

        # Validate that all fields are filled
        if not mrp or not date or not quantity:
            messagebox.showerror("Error", "Please fill in all details.")
            return

        # Connect to MySQL database to save opening entry
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="new dhaulagiri enterprises"
            )

            cursor = connection.cursor()

            # Check if the item already exists in the opening_entry_table
            query_check = "SELECT quantity FROM stock WHERE item_name = %s"
            cursor.execute(query_check, (selected_item,))
            existing_quantity = cursor.fetchone()

            if existing_quantity:
                # If the item exists, update the quantity
                new_quantity = int(existing_quantity[0]) + int(quantity)
                query_update = "UPDATE stock SET quantity = %s WHERE item_name = %s"
                cursor.execute(query_update, (new_quantity, selected_item))
            else:
                # If the item does not exist, insert a new row
                query_insert = "INSERT INTO stock (item_name,quantity,MRP,date) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_insert, (selected_item, quantity, mrp, date))

            # Commit the changes
            connection.commit()

            # Display success message
            messagebox.showinfo("Success", "Opening entry submitted successfully.")

            # Refresh the table after submission
            self.create_table()

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            messagebox.showerror("Error", "An error occurred while connecting to the database.")

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_table(self):
        # Create a treeview widget for the table
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("item_name", "quantity", "MRP", "date")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("MRP", text="MRP")
        self.tree.heading("date", text="Date")

        # Remove existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch data from the "stock" table
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="new dhaulagiri enterprises"
            )

            cursor = connection.cursor()

            # Fetch all rows from the "stock" table
            query_select = "SELECT item_name, quantity, MRP, date FROM stock"
            cursor.execute(query_select)

            # Populate the treeview with the retrieved data
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            messagebox.showerror("Error", "An error occurred while connecting to the database.")

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()
            
        # Pack the treeview widget
        self.tree.pack(pady=10)

    def get_current_date(self):
        # Return the current date in the format 'dd-mm-yyyy'
        return datetime.now().strftime('%Y-%M-%d')

if __name__ == "__main__":
    root = tk.Tk()
    opening_entry_form = OpeningEntryForm(root)
    root.mainloop()
