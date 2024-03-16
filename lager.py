import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime

# Database initialization
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="new dhaulagiri enterprises"
)
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        debit DECIMAL(10, 2),
        credit DECIMAL(10, 2),
        transaction_date DATE,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
''')
conn.commit()

# Tkinter GUI
class CustomerLedgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Ledger App")

        # Customer information
        tk.Label(root, text="Select Customer:").grid(row=0, column=0, padx=10, pady=5)
        self.customer_name_combobox = ttk.Combobox(root)
        self.customer_name_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.customer_name_combobox.bind("<<ComboboxSelected>>", self.load_customer_info)

        tk.Label(root, text="Address:").grid(row=1, column=0, padx=10, pady=5)
        self.address_entry = tk.Entry(root, state='readonly')
        self.address_entry.grid(row=1, column=1, padx=10, pady=5)

        # Transaction information
        tk.Label(root, text="Debit Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.debit_entry = tk.Entry(root)
        self.debit_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Credit Amount:").grid(row=3, column=0, padx=10, pady=5)
        self.credit_entry = tk.Entry(root)
        self.credit_entry.grid(row=3, column=1, padx=10, pady=5)

        # Date entry
        tk.Label(root, text="Transaction Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Save Transaction", command=self.save_transaction).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="View Ledger", command=self.view_ledger).grid(row=8, column=0, columnspan=5, pady=10)

        # Populate customer names in the combo box
        self.populate_customer_names()

    def populate_customer_names(self):
        cursor.execute("SELECT name FROM customers")
        customer_names = [name[0] for name in cursor.fetchall()]
        self.customer_name_combobox['values'] = customer_names

    def load_customer_info(self, event):
        selected_customer_name = self.customer_name_combobox.get()
        if selected_customer_name:
            cursor.execute("SELECT id, address FROM customers WHERE name = %s", (selected_customer_name,))
            customer_info = cursor.fetchone()
            if customer_info:
                customer_id, customer_address = customer_info
                self.address_entry.config(state='normal')
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, customer_address)
                self.address_entry.config(state='readonly')

    def save_transaction(self):
        selected_customer_name = self.customer_name_combobox.get()
        address = self.address_entry.get()
        debit = self.debit_entry.get()
        credit = self.credit_entry.get()
        transaction_date = self.date_entry.get()

        if selected_customer_name and address and (debit or credit) and transaction_date:
            try:
                # Get customer ID
                cursor.execute("SELECT id FROM customers WHERE name = %s", (selected_customer_name,))
                customer_id = cursor.fetchone()[0]

                # Save transaction information
                cursor.execute("INSERT INTO transactions (customer_id, debit, credit, transaction_date) VALUES (%s, %s, %s, %s)",
                               (customer_id, debit or None, credit or None, transaction_date))
                conn.commit()

                messagebox.showinfo("Success", "Transaction saved successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all required fields.")

    def view_ledger(self):
        ledger_window = tk.Toplevel(self.root)
        ledger_window.title("Customer Ledger")

        tk.Label(ledger_window, text="Customer Ledger").grid(row=0, column=0, columnspan=3, pady=10)

        # Display ledger in a listbox
        ledger_listbox = tk.Listbox(ledger_window, width=50)
        ledger_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Fetch and display ledger information
        cursor.execute("SELECT c.id, c.name, c.address FROM customers c")
        customers = cursor.fetchall()

        for customer in customers:
            customer_id, customer_name, customer_address = customer
            ledger_listbox.insert(tk.END, f"Customer ID: {customer_id}, Name: {customer_name}, Address: {customer_address}")

            # Calculate total and remaining amounts for each customer
            cursor.execute("SELECT SUM(debit) AS total_debit, SUM(credit) AS total_credit FROM transactions WHERE customer_id = %s", (customer_id,))
            result = cursor.fetchone()
            total_debit = result[0] or 0
            total_credit = result[1] or 0
            remaining_amount = total_debit - total_credit

            ledger_listbox.insert(tk.END, f"Total Debit: {total_debit}, Total Credit: {total_credit}, Remaining Amount: {remaining_amount}")
            ledger_listbox.insert(tk.END, "-" * 50)  # Separator

        ledger_listbox.config(state=tk.DISABLED)  # Disable editing of listbox

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerLedgerApp(root)
    root.mainloop()
