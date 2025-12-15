import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import date

# Database Connection using PyMySQL
db = pymysql.connect(
    host="localhost",
    user="sourav",
    password="sourav@123",
    database="librarybooks"
)
cursor = db.cursor()

# Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x500")
root.configure(bg="#f2f2f2")

# Title Label
title_lbl = tk.Label(root, text="Library Management System", font=("Arial", 20, "bold"), bg="#f2f2f2")
title_lbl.pack(pady=10)

# Add Book Frame
form = tk.Frame(root, bg="white", bd=2, relief="groove")
form.pack(pady=10)

# Variables
title = tk.StringVar()
author = tk.StringVar()
qty = tk.IntVar()

# Labels & Entries
tk.Label(form, text="Book Title", bg="white").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(form, textvariable=title).grid(row=0, column=1, padx=10, pady=5)

tk.Label(form, text="Author", bg="white").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(form, textvariable=author).grid(row=1, column=1, padx=10, pady=5)

tk.Label(form, text="Quantity", bg="white").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(form, textvariable=qty).grid(row=2, column=1, padx=10, pady=5)

# Add Book Function
def add_book():
    if title.get() == "" or author.get() == "" or qty.get() <= 0:
        messagebox.showerror("Error", "All fields are required")
        return

    sql = "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title.get(), author.get(), qty.get()))
    db.commit()
    messagebox.showinfo("Success", "Book Added Successfully")
    load_books()

# Add Button
tk.Button(form, text="Add Book", command=add_book, bg="#4CAF50", fg="white", width=15).grid(row=3, column=1, pady=10)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Book Table
columns = ("ID", "Title", "Author", "Quantity")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree.pack(fill=tk.BOTH, expand=True)

# Scrollbar
scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Load Books
def load_books():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

load_books()

root.mainloop()
