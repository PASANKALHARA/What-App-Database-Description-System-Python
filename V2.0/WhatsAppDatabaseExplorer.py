import sqlite3
from tkinter import *
from tkinter import filedialog
import pandas as pd

class WhatsAppDatabaseExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Database Explorer")
        self.conn = None

        Button(root, text="Load Database", command=self.load_database).pack()
        Label(root, text="Tables:").pack()
        self.tables_listbox = Listbox(root)
        self.tables_listbox.pack(fill=BOTH, expand=True)
        Button(root, text="Display Table", command=self.display_table).pack()
        self.display_text = Text(root, wrap=NONE)
        self.display_text.pack(fill=BOTH, expand=True)

    def load_database(self):
        filepath = filedialog.askopenfilename(
            title="Select WhatsApp Database",
            filetypes=(("SQLite Database", "*.sqlite"), ("All Files", "*.*"))
        )
        if filepath:
            self.conn = sqlite3.connect(filepath)
            self.load_tables()

    def load_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.tables_listbox.delete(0, END)  # Clear existing items
        for table in tables:
            self.tables_listbox.insert(END, table[0])

    def display_table(self):
        if self.conn:
            selected_table = self.tables_listbox.get(ANCHOR)
            if selected_table:
                query = f"SELECT * FROM {selected_table}"
                data = pd.read_sql_query(query, self.conn)
                self.display_text.delete(1.0, END)
                self.display_text.insert(END, data.to_string())
        else:
            self.display_text.insert(END, "No database loaded!")

# Main Application
if __name__ == "__main__":
    root = Tk()
    app = WhatsAppDatabaseExplorer(root)
    root.mainloop()
