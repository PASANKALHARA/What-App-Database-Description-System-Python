import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

class WhatAppDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("What App Database Description")
        self.root.geometry("800x600")

        # Database connection
        self.conn = sqlite3.connect('what_app_database.db')
        self.create_tables()

        # Main layout
        self.setup_ui()

    def create_tables(self):
        """Create necessary database tables if they do not exist"""
        cursor = self.conn.cursor()

        # Table for descriptions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table for chat messages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def setup_ui(self):
        """Set up the user interface"""
        # Frame for input
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        # Labels and Entries
        tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Category:").grid(row=0, column=2, sticky=tk.W)
        self.category_entry = tk.Entry(input_frame, width=20)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        # Description Text Area
        tk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW)
        self.description_text = tk.Text(input_frame, height=5, width=50)
        self.description_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(button_frame, text="Add Description", command=self.add_description).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View Descriptions", command=self.view_descriptions).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Manage Chats", command=self.manage_chats).pack(side=tk.LEFT, padx=5)

        # Treeview for displaying descriptions
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Category', 'Created Date'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Created Date', text='Created Date')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Bind double-click to show full description
        self.tree.bind('<Double-1>', self.show_full_description)

    def add_description(self):
        """Add a new description to the database"""
        name = self.name_entry.get()
        category = self.category_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()

        if not name or not description:
            messagebox.showerror("Error", "Name and Description are required!")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO descriptions (name, description, category) 
            VALUES (?, ?, ?)
        ''', (name, description, category))
        self.conn.commit()

        messagebox.showinfo("Success", "Description added successfully!")
        self.clear_inputs()
        self.view_descriptions()

    def view_descriptions(self):
        """View all descriptions in the treeview"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, category, created_date FROM descriptions')
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def show_full_description(self, event):
        """Show full description when double-clicking a row"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id = self.tree.item(selected_item)['values'][0]
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, description, category FROM descriptions WHERE id = ?', (item_id,))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo(f"Description for {result[0]}", 
                                f"Name: {result[0]}\n\n"
                                f"Category: {result[2]}\n\n"
                                f"Description:\n{result[1]}")

    def manage_chats(self):
        """Open a new window to manage chats"""
        chat_window = tk.Toplevel(self.root)
        chat_window.title("Chat Management")
        chat_window.geometry("600x400")

        chat_tree = ttk.Treeview(chat_window, columns=('ID', 'User', 'Message', 'Timestamp'), show='headings')
        chat_tree.heading('ID', text='ID')
        chat_tree.heading('User', text='User')
        chat_tree.heading('Message', text='Message')
        chat_tree.heading('Timestamp', text='Timestamp')
        chat_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        def load_chats():
            for i in chat_tree.get_children():
                chat_tree.delete(i)

            cursor = self.conn.cursor()
            cursor.execute('SELECT id, user, message, timestamp FROM chats')
            for row in cursor.fetchall():
                chat_tree.insert('', tk.END, values=row)

        load_chats()

        tk.Button(chat_window, text="Add Chat", command=lambda: self.add_chat(chat_tree, load_chats)).pack(pady=5)
        tk.Button(chat_window, text="Close", command=chat_window.destroy).pack()

    def add_chat(self, chat_tree, load_chats_callback):
        """Add a new chat entry"""
        user = simpledialog.askstring("Input", "Enter user name:")
        message = simpledialog.askstring("Input", "Enter message:")

        if not user or not message:
            messagebox.showerror("Error", "Both user and message are required!")
            return

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO chats (user, message) VALUES (?, ?)', (user, message))
        self.conn.commit()
        load_chats_callback()

    def clear_inputs(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)

    def __del__(self):
        """Close database connection when app is closed"""
        self.conn.close()

def main():
    root = tk.Tk()
    app = WhatAppDatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
