import tkinter as tk
from tkinter import filedialog
import openingentry
import itementry 
import purchaseentry
import sellitem
import subprocess

def open_file():
    file_path = filedialog.askopenfilename(title="Open File")
    if file_path:
        # Do something with the selected file path (e.g., print it)
        print(f"Selected file: {file_path}")

def save_file():
    file_path = filedialog.asksaveasfilename(title="Save File")
    if file_path:
        # Do something with the selected file path (e.g., print it)
        print(f"Saved file to: {file_path}")
def openingentry():
    try:
        subprocess.Popen(['python',r'C:\Users\ASUS\Desktop\new dhaulagiri\openingentry.py'])
    except Exception as e:
        print(f"Error opening the file: {e}")

def purchaseentry():
    try:
        subprocess.Popen(['python',r'C:\Users\ASUS\Desktop\new dhaulagiri\purchaseentry.py'])
    except Exception as e:
        print(f"Error opening the file: {e}")

def itementry():
    try:
        subprocess.Popen(['python',r'C:\Users\ASUS\Desktop\new dhaulagiri\itementry.py'])
    except Exception as e:
        print(f"Error opening the file: {e}")
def sellitem():
    try:
        subprocess.Popen(['python',r'C:\Users\ASUS\Desktop\new dhaulagiri\sellitem.py'])
    except Exception as e:
        print(f"Error opening the file: {e}")


def exit_app():
    root.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.title("New Dhaulagiri Enterprises")

# Create a menubar
menubar = tk.Menu(root)

# Create a "File" menu
file_menu = tk.Menu(menubar, tearoff=0)
home_menu = tk.Menu(menubar, tearoff=0)
bill_menu = tk.Menu(menubar, tearoff=0)
leger_menu = tk.Menu(menubar, tearoff=0)
stock_menu = tk.Menu(menubar, tearoff=0)
supplier_menu = tk.Menu(menubar, tearoff=0)
report_menu = tk.Menu(menubar, tearoff=0)

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Exit", command=exit_app)


leger_menu.add_cascade(label="Open leger")

# Add a command to open the Opening Entry functionality
stock_menu.add_command(label="Item Entry", command=itementry)
stock_menu.add_command(label="Opening Entry", command=openingentry)
stock_menu.add_cascade(label="Purchase Entry",command=purchaseentry)
bill_menu.add_cascade(label="Cash Sell",command=sellitem)



# Add the "File" menu to the menubar
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Home", menu=home_menu)
menubar.add_cascade(label="Billing", menu=bill_menu)
menubar.add_cascade(label="Leger", menu=leger_menu)
menubar.add_cascade(label="Supplier", menu=supplier_menu)
menubar.add_cascade(label="Stock", menu=stock_menu)
menubar.add_cascade(label="Report", menu=supplier_menu)

# Configure the root window to use the menubar
root.config(menu=menubar)

root.mainloop()
