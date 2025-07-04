import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, ttk
import pandas as pd
import json

from modules.excel_handler import read_excel, write_excel
from modules.metadata_handler import read_json_metadata
from modules.sql_dump_parser import parse_sql_dump

# Global Paths
EXCEL_PATH = 'data/users.xlsx'
JSON_PATH = 'data/music_metadata.json'
SQL_PATH = 'data/sales_dump.sql'

# ---------------------------
def show_excel():
    df = read_excel(EXCEL_PATH)
    display_table("Excel Data", df)

def show_metadata():
    data = read_json_metadata(JSON_PATH)
    df = pd.DataFrame(data)
    display_table("Music Metadata", df)

def show_sql():
    inserts = parse_sql_dump(SQL_PATH)
    popup = tk.Toplevel(root)
    popup.title("SQL Inserts")
    text = tk.Text(popup, wrap=tk.WORD)
    text.pack(expand=True, fill=tk.BOTH)
    text.insert(tk.END, "\n".join(inserts[:10]))  # Show first 10

def add_user():
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()

    if not name or not age or not email:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Type Error", "Age must be a number.")
        return

    new_df = pd.DataFrame([[name, age, email]], columns=["Name", "Age", "Email"])

    try:
        old_df = read_excel(EXCEL_PATH)
        updated_df = pd.concat([old_df, new_df], ignore_index=True)
    except:
        updated_df = new_df

    write_excel(updated_df, EXCEL_PATH)
    messagebox.showinfo("Success", "User added successfully!")
    clear_inputs()

def add_column():
    df = read_excel(EXCEL_PATH)
    new_col = simpledialog.askstring("Add Column", "Enter new column name:")
    if new_col:
        if new_col in df.columns:
            messagebox.showerror("Duplicate", f"Column '{new_col}' already exists.")
        else:
            df[new_col] = ""
            write_excel(df, EXCEL_PATH)
            messagebox.showinfo("Success", f"Column '{new_col}' added.")

def remove_column():
    df = read_excel(EXCEL_PATH)
    col_to_remove = simpledialog.askstring("Remove Column", f"Enter column name to remove:\nAvailable: {list(df.columns)}")
    if col_to_remove in df.columns:
        df = df.drop(columns=[col_to_remove])
        write_excel(df, EXCEL_PATH)
        messagebox.showinfo("Success", f"Column '{col_to_remove}' removed.")
    else:
        messagebox.showerror("Not Found", f"Column '{col_to_remove}' not found.")

def rename_column():
    df = read_excel(EXCEL_PATH)
    old_name = simpledialog.askstring("Rename Column", f"Enter existing column name:\nAvailable: {list(df.columns)}")
    if old_name not in df.columns:
        messagebox.showerror("Not Found", f"Column '{old_name}' not found.")
        return

    new_name = simpledialog.askstring("Rename Column", f"Enter new name for column '{old_name}':")
    if new_name:
        df.rename(columns={old_name: new_name}, inplace=True)
        write_excel(df, EXCEL_PATH)
        messagebox.showinfo("Success", f"Renamed '{old_name}' to '{new_name}'.")

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def display_table(title, df):
    popup = tk.Toplevel(root)
    popup.title(title)
    tree = ttk.Treeview(popup)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(expand=True, fill=tk.BOTH)

# ---------------------------
root = tk.Tk()
root.title("Flat-File DBMS UI")
root.geometry("600x400")

# --- Buttons ---
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Show Excel Data", command=show_excel, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame, text="Show Metadata", command=show_metadata, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Show SQL Inserts", command=show_sql, width=20).grid(row=0, column=2, padx=5, pady=5)

# --- Column Edit Buttons ---
col_frame = tk.LabelFrame(root, text="Modify Columns", padx=10, pady=10)
col_frame.pack(padx=10, pady=5, fill="x")

tk.Button(col_frame, text="Add Column", command=add_column).grid(row=0, column=0, padx=10, pady=5)
tk.Button(col_frame, text="Remove Column", command=remove_column).grid(row=0, column=1, padx=10, pady=5)
tk.Button(col_frame, text="Rename Column", command=rename_column).grid(row=0, column=2, padx=10, pady=5)

# --- Form Input ---
form = tk.LabelFrame(root, text="Add New User", padx=10, pady=10)
form.pack(padx=10, pady=10, fill="x")

tk.Label(form, text="Name").grid(row=0, column=0)
tk.Label(form, text="Age").grid(row=0, column=1)
tk.Label(form, text="Email").grid(row=0, column=2)

entry_name = tk.Entry(form, width=15)
entry_age = tk.Entry(form, width=10)
entry_email = tk.Entry(form, width=25)

entry_name.grid(row=1, column=0, padx=5, pady=5)
entry_age.grid(row=1, column=1, padx=5, pady=5)
entry_email.grid(row=1, column=2, padx=5, pady=5)

tk.Button(form, text="Add User", command=add_user).grid(row=1, column=3, padx=10)

# --- Main Loop ---
root.mainloop()