import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
from reportlab.pdfgen import canvas
import subprocess

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sell item")

        # Date label
        self.label_date = tk.Label(root, text=f"Date: {self.get_current_date()}")
        self.label_date.pack(pady=5)

        # Customer details
        self.customer_name = tk.StringVar()
        self.customer_address = tk.StringVar()
        self.quantity = tk.StringVar()
        self.discount_percent = tk.StringVar()

        # Entry fields for customer details
        tk.Label(root, text="Customer Name:").pack(pady=3)
        tk.Entry(root, textvariable=self.customer_name).pack(pady=3)

        tk.Label(root, text="Customer Address:").pack(pady=3)
        tk.Entry(root, textvariable=self.customer_address).pack(pady=3)

        # Combo box to select item
        tk.Label(root, text="Item Name:").pack(pady=3)
        self.combo_item = ttk.Combobox(root, state="readonly", width=30)
        self.combo_item.set("Select Item")
        self.combo_item.pack(pady=5)

        # Entry field for quantity
        tk.Label(root, text="Quantity:").pack(pady=3)
        tk.Entry(root, textvariable=self.quantity).pack(pady=3)

        # Entry field for discount
        tk.Label(root, text="Discount (%):").pack(pady=3)
        tk.Entry(root, textvariable=self.discount_percent).pack(pady=3)

        # Button to add item to the table
        add_button = tk.Button(root, text="Add Item", command=self.add_item_to_table)
        add_button.pack(pady=10)

        # Table to display items in the bill
        self.tree = ttk.Treeview(root, columns=("S.No.", "Item", "Quantity", "MRP", "Discount", "Total"))
        self.tree.heading("#1", text="S.No.")
        self.tree.heading("#2", text="Item")
        self.tree.heading("#3", text="Quantity")
        self.tree.heading("#4", text="MRP")
        self.tree.heading("#5", text="Discount (%)")
        self.tree.heading("#6", text="Total")
        self.tree.pack(pady=5)

        # Submit button
        submit_button = tk.Button(root, text="Generate Bill", command=self.generate_bill)
        submit_button.pack(pady=10)

        # Fetch and display item names in the combo box
        self.update_item_combobox()

    def update_item_combobox(self):
        # Clear existing items in the combo box
        self.combo_item['values'] = ()

        # Connect to MySQL database to fetch item names
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="new dhaulagiri enterprises"  # Replace with your actual database name
            )

            cursor = connection.cursor()

            # Fetch item names from the 'items' table
            query = "SELECT item_name FROM stock"
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

    def add_item_to_table(self):
        selected_item = self.combo_item.get()
        quantity = self.quantity.get()

        if not selected_item or selected_item == "Select Item" or not quantity:
            messagebox.showerror("Error", "Please select an item and enter a quantity.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="new dhaulagiri enterprises"  # Replace with your actual database name
            )

            cursor = connection.cursor()

            # Fetch MRP from the 'items' table
            query_mrp = "SELECT MRP FROM stock WHERE item_name = %s"
            cursor.execute(query_mrp, (selected_item,))
            mrp = cursor.fetchone()[0]

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            messagebox.showerror("Error", "An error occurred while connecting to the database.")
            return

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

        # Calculate total cost based on quantity and MRP
        total_cost = float(quantity) * float(mrp)

        # Apply discount if provided
        discount_percent = self.discount_percent.get()
        if discount_percent:
            discount_amount = (float(discount_percent) / 100) * total_cost
            total_cost -= discount_amount

        # Insert item into the table
        serial_number = len(self.tree.get_children()) + 1
        self.tree.insert("", tk.END, values=(serial_number, selected_item, quantity, mrp, discount_percent, total_cost))

        # Clear the combo box, quantity entry, and discount entry
        self.combo_item.set("Select Item")
        self.quantity.set("")
        self.discount_percent.set("")

    def generate_bill(self):
        # Retrieve customer details
        customer_name = self.customer_name.get()
        customer_address = self.customer_address.get()

        if not customer_name:
            messagebox.showerror("Error", "Please enter the customer name.")
            return

        # Create a PDF file for the bill
        pdf_filename = f"bill_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_canvas = canvas.Canvas(pdf_filename)

        # Display the bill in the PDF
        pdf_canvas.drawString(100, 800, f"Date: {self.get_current_date()}")
        pdf_canvas.drawString(100, 780, f"Customer Name: {customer_name}")
        pdf_canvas.drawString(100, 760, f"Customer Address: {customer_address}")
        pdf_canvas.drawString(100, 740, "Items:")

        grand_total = 0
        y_position = 720

        for item_id in self.tree.get_children():
            item_values = self.tree.item(item_id, "values")
            _, item, quantity, mrp, discount_percent, total = item_values
            grand_total += float(total)

            item_line = f"{item} x{quantity} - MRP: {mrp}, Discount: {discount_percent}%, Total: {total}"
            pdf_canvas.drawString(100, y_position, item_line)
            y_position -= 20

        pdf_canvas.drawString(100, y_position - 20, f"Grand Total: {grand_total}")

        # Save the PDF file
        pdf_canvas.save()

        # Open the PDF file with the default PDF viewer on Windows
        subprocess.Popen(["start", "", pdf_filename], shell=True)

        messagebox.showinfo("Bill Details", f"Bill generated successfully!\nPDF opened.")

    def get_current_date(self):
        # Return the current date in the format 'dd-mm-yyyy'
        return datetime.now().strftime('%d-%m-%y')

if __name__ == "__main__":
    root = tk.Tk()
    billing_app = BillingApp(root)
    root.mainloop()
