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
global selected_index
selected_index = None


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
    df = read_excel(EXCEL_PATH)
    row_data = {}

    for col, entry in form_entries.items():
        val = entry.get()
        if col.lower() == 'age':
            try:
                val = int(val)
            except:
                messagebox.showerror("Error", f"Invalid Age value.")
                return
        row_data[col] = val

    new_df = pd.DataFrame([row_data])
    df = pd.concat([df, new_df], ignore_index=True)
    write_excel(df, EXCEL_PATH)
    messagebox.showinfo("Success", "New record added.")
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
            build_dynamic_form()


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
    for entry in form_entries.values():
        entry.delete(0, tk.END)


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

def search_record():
    global selected_index
    name = simpledialog.askstring("Search", "Enter Name to edit:")
    if not name:
        return

    df = read_excel(EXCEL_PATH)
    if "Name" not in df.columns:
        messagebox.showerror("Not Found", "No 'Name' column found in file.")
        return

    matches = df[df["Name"] == name]
    if matches.empty:
        messagebox.showerror("Not Found", f"No record found with Name '{name}'.")
        return

    selected_index = matches.index[0]
    row = matches.iloc[0]

    for col, entry in form_entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, str(row.get(col, "")))

    messagebox.showinfo("Record Found", f"Editing record for '{name}'.")


def save_edited_record():
    global selected_index
    if selected_index is None:
        messagebox.showwarning("Warning", "Search a record to edit first.")
        return

    df = read_excel(EXCEL_PATH)
    for col, entry in form_entries.items():
        val = entry.get()
        if col.lower() == 'age':
            try:
                val = int(val)
            except:
                messagebox.showerror("Error", f"Invalid value for Age.")
                return
        df.at[selected_index, col] = val

    write_excel(df, EXCEL_PATH)
    messagebox.showinfo("Updated", "Record saved.")
    selected_index = None
    clear_inputs()

def build_dynamic_form():
    global form_entries, selected_index
    for widget in form_frame.winfo_children():
        widget.destroy()
    form_entries.clear()

    df = read_excel(EXCEL_PATH)
    columns = list(df.columns)

    for idx, col in enumerate(columns):
        tk.Label(form_frame, text=col).grid(row=0, column=idx, padx=5)
        entry = tk.Entry(form_frame, width=15)
        entry.grid(row=1, column=idx, padx=5)
        form_entries[col] = entry

    tk.Button(form_frame, text="Add New", command=add_user).grid(row=2, column=0, pady=5)
    tk.Button(form_frame, text="Search & Edit", command=search_record).grid(row=2, column=1, pady=5)
    tk.Button(form_frame, text="Save Changes", command=save_edited_record).grid(row=2, column=2, pady=5)

    selected_index = None  # important!



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

form_frame = tk.LabelFrame(root, text="Record Editor", padx=10, pady=10)
form_frame.pack(padx=10, pady=10, fill="x")

form_entries = {}  # column_name -> tk.Entry


# --- Main Loop ---
build_dynamic_form()
root.mainloop()