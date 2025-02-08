import sqlite3
from tkinter import *
from tkinter import filedialog, ttk
import pandas as pd

# Global connection variable
conn = None

def load_database():
    global conn
    filepath = filedialog.askopenfilename(
        title="Select WhatsApp Database",
        filetypes=(("SQLite Database", "*.sqlite"), ("All Files", "*.*"))
    )
    if filepath:
        conn = sqlite3.connect(filepath)
        load_tables()

def load_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tables_listbox.delete(0, END)  # Clear existing items
    for table in tables:
        tables_listbox.insert(END, table[0])

def display_table():
    if conn:
        selected_table = tables_listbox.get(ANCHOR)
        if selected_table:
            query = f"SELECT * FROM {selected_table}"
            data = pd.read_sql_query(query, conn)
            display_text.delete(1.0, END)
            display_text.insert(END, data.to_string())
    else:
        display_text.insert(END, "No database loaded!")

# GUI Setup
app = Tk()
app.title("WhatsApp Database Explorer")

Button(app, text="Load Database", command=load_database).pack()
Label(app, text="Tables:").pack()
tables_listbox = Listbox(app)
tables_listbox.pack(fill=BOTH, expand=True)
Button(app, text="Display Table", command=display_table).pack()
display_text = Text(app, wrap=NONE)
display_text.pack(fill=BOTH, expand=True)

app.mainloop()
