import tkinter as tk
from tkinter import ttk
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.create_table()

    def create_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS colorcode (
                id INT AUTO_INCREMENT PRIMARY KEY,
                costumer_name VARCHAR(255),
                address VARCHAR(255),
                color_code VARCHAR(255),
                Base VARCHAR(255),
                product VARCHAR(255)
            )
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()

    def insert_data(self, values):
        query = 'INSERT INTO colorcode(costumer_name, address, color_code, Base, product) VALUES (%s, %s, %s, %s, %s)'
        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
        self.conn.commit()

    def retrieve_data(self, search_term=None):
        if search_term:
            query = 'SELECT * FROM colorcode WHERE costumer_name LIKE %s'
            search_pattern = f'%{search_term}%'
            with self.conn.cursor() as cursor:
                cursor.execute(query, (search_pattern,))
        else:
            query = 'SELECT * FROM colorcode'
            with self.conn.cursor() as cursor:
                cursor.execute(query)

        return cursor.fetchall()

    def delete_data(self, id):
        query = 'DELETE FROM colorcode WHERE id = %s'
        with self.conn.cursor() as cursor:
            cursor.execute(query, (id,))
        self.conn.commit()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("color code entry")

        # Update these parameters with your MySQL server details
        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'new dhaulagiri enterprises'
        }

        self.db_manager = DatabaseManager(**db_params)

        # Entry widgets for data input
        self.entry_values = [tk.StringVar() for _ in range(5)]
        entry_labels = ["costumer_name", "address", "color_code", "Base", "product"]

        for i, label_text in enumerate(entry_labels):
            tk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            tk.Entry(root, textvariable=self.entry_values[i]).grid(row=i, column=1, padx=10, pady=5)

        # Search box
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search Costumer Name:").grid(row=0, column=1,sticky='NW',padx=10, pady=5)
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=3, padx=10, pady=5)
        tk.Button(root, text="Search", command=self.search_data).grid(row=0, column=4, pady=5)

        # Button to insert data
        tk.Button(root, text="Insert Data", command=self.insert_data).grid(row=6, column=0, pady=10)

        # Treeview to display data
        self.tree = ttk.Treeview(root, columns=("ID", "costumer_name", "address", "color_code", "Base", "product"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("costumer_name", text="costumer_name")
        self.tree.heading("address", text="address")
        self.tree.heading("color_code", text="color_code")
        self.tree.heading("Base", text="Base")
        self.tree.heading("product", text="product")
        self.tree.grid(row=7, column=0, padx=10, pady=10)

        # Bind the Treeview click event to populate entry widgets
        self.tree.bind('<ButtonRelease-1>', self.populate_entry_widgets)

        # Button to retrieve data
        tk.Button(root, text="Retrieve Data", command=self.retrieve_data).grid(row=8, column=0, pady=10)

        # Button to delete selected data
        tk.Button(root, text="Delete Selected", command=self.delete_data).grid(row=9, column=0,  pady=10)

    def insert_data(self):
        values = [value.get() for value in self.entry_values]
        self.db_manager.insert_data(values)
        self.clear_entry_fields()
        self.retrieve_data()

    def retrieve_data(self):
        # Clear existing treeview items
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_var.get()
        data = self.db_manager.retrieve_data(search_term)
        for row in data:
            self.tree.insert("", "end", values=row)

    def search_data(self):
        self.retrieve_data()

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return  # No item selected

        # Get the ID of the selected item
        id_to_delete = self.tree.item(selected_item, 'values')[0]

        # Delete data from the database
        self.db_manager.delete_data(id_to_delete)

        # Refresh the data in the Treeview
        self.retrieve_data()

    def populate_entry_widgets(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return  # No item selected

        # Fill entry widgets with data from the selected item
        for i, value in enumerate(self.tree.item(selected_item, 'values')[1:]):
            self.entry_values[i].set(value)

    def clear_entry_fields(self):
        for entry in self.entry_values:
            entry.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
