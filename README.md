# 🗃️ Flat-File DBMS Interface (Tkinter GUI)


A lightweight, user-friendly GUI tool built using Python and Tkinter to simulate a Flat-File Database Management System (DBMS) using Excel, JSON, and SQL dump files. Perfect for beginners learning about file-based data storage and manipulation.



### 🚀 Features



* **📊 Excel Record Management**

&nbsp;	View, add, edit, and update user records stored in .xlsx files.

&nbsp;	Dynamically supports any number of columns.



* **🧩 Metadata Viewer**

&nbsp;	Reads and displays structured metadata from .json files.



* **🧾 SQL Dump Parser**

&nbsp;	Extracts and previews SQL INSERT statements from .sql files.



* **🧱 Column Operations**

&nbsp;	Add, remove, and rename columns on-the-fly via the GUI.



* **✏️ Record Editing**

&nbsp;	Search records (by Name), auto-fill into the form, and edit values easily.



* **🖥️ Built with Tkinter**

&nbsp;	Cross-platform Python GUI that runs standalone on Windows, Linux, or macOS.



# 📁 Project Structure


FlatFile\_GUI\_DBMS/
│
├── data/
│   ├── users.xlsx              *# Excel database (acts like a table)*
│   ├── music\_metadata.json     *# JSON metadata store*
│   └── sales\_dump.sql          *# SQL dump with INSERT statements*
│
├── modules/
│   ├── excel\_handler.py        *# Read/write operations on Excel*
│   ├── metadata\_handler.py     *# JSON parser*
│   └── sql\_dump\_parser.py      *# SQL INSERT parser*
│
├── gui.py                      *# Main GUI application*
└── README.md                   *# This file*


### 

### 🛠 Requirements



* Python 3.6+
* Packages:


	**pip install pandas openpyxl**


(Tkinter comes pre-installed with Python.)



### 🧪 How to Run



	**python gui.py**


✨ Future Ideas
---



* Record deletion
* CSV export/import
* Sort/filter capabilities in table view
* Treeview inline editing



### 📚 Educational Value



This project demonstrates:

* Flat-file storage operations
* Dynamic form building in GUI
* Integrating multiple file formats (XLSX, JSON, SQL)
* GUI design with real-world functionality
