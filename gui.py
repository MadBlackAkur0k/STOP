import tkinter as tk
from tkinter import scrolledtext, messagebox
from database import DatabaseManager

class GuiManager:
    def __init__(self, master):
        self.master = master
        master.title("Database Management App")

        # Ввод данных
        self.label_host = tk.Label(master, text="Host:")
        self.label_host.grid(row=0, column=0)
        self.entry_host = tk.Entry(master)
        self.entry_host.grid(row=0, column=1)

        self.label_port = tk.Label(master, text="Port:")
        self.label_port.grid(row=1, column=0)
        self.entry_port = tk.Entry(master)
        self.entry_port.grid(row=1, column=1)

        self.label_db = tk.Label(master, text="Database:")
        self.label_db.grid(row=2, column=0)
        self.entry_db = tk.Entry(master)
        self.entry_db.grid(row=2, column=1)

        self.label_user = tk.Label(master, text="User:")
        self.label_user.grid(row=3, column=0)
        self.entry_user = tk.Entry(master)
        self.entry_user.grid(row=3, column=1)

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.grid(row=4, column=0)
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.grid(row=4, column=1)

        self.label_count = tk.Label(master, text="Number of Records:")
        self.label_count.grid(row=5, column=0)
        self.entry_count = tk.Entry(master)
        self.entry_count.grid(row=5, column=1)

        self.label_table = tk.Label(master, text="Table Name:")
        self.label_table.grid(row=6, column=0)
        self.entry_table = tk.Entry(master)
        self.entry_table.grid(row=6, column=1)

        # Кнопки
        self.button_show_tables = tk.Button(master, text="Show Tables", command=self.show_tables)
        self.button_show_tables.grid(row=7, column=0, columnspan=2)

        self.button_select = tk.Button(master, text="Select Data", command=self.select_data)
        self.button_select.grid(row=8, column=0, columnspan=2)

        self.button_insert_all = tk.Button(master, text="Insert Records", command=self.insert_records)
        self.button_insert_all.grid(row=9, column=0, columnspan=2)

        self.button_update = tk.Button(master, text="Update Records", command=self.update_records)
        self.button_update.grid(row=10, column=0, columnspan=2)

        self.button_delete_specific = tk.Button(master, text="Delete Specific Records", command=self.delete_specific)
        self.button_delete_specific.grid(row=11, column=0, columnspan=2)

        self.button_delete_all = tk.Button(master, text="Delete All Records", command=self.delete_all)
        self.button_delete_all.grid(row=12, column=0, columnspan=2)

        self.button_show_schema = tk.Button(master, text="Show Table Schema", command=self.show_table_schema)
        self.button_show_schema.grid(row=13, column=0, columnspan=2)

        # Текстовое поле для вывода информации
        self.output_area = scrolledtext.ScrolledText(master, width=40, height=10)
        self.output_area.grid(row=14, column=0, columnspan=2)

        self.db_manager = DatabaseManager()

    def connect_db(self):
        db = self.entry_db.get()
        host = self.entry_host.get()
        port = self.entry_port.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        conn = self.db_manager.connect_db(db, host, port, user, password)
        if conn is None:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return conn

    def show_tables(self):
        conn = self.connect_db()
        if conn:
            tables = self.db_manager.get_tables(conn)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, "List of tables:\n")
            for table in tables:
                self.output_area.insert(tk.END, f"{table[0]}\n")
            conn.close()

    def select_data(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            results = self.db_manager.select_data(conn, table_name)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Data from {table_name}:\n")
            for row in results:
                self.output_area.insert(tk.END, f"{row}\n")
            conn.close()

    def insert_records(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            num_records = int(self.entry_count.get())
            self.db_manager.insert_records(conn, table_name, num_records)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Inserted {num_records} records into {table_name}\n")
            conn.close()

    def update_records(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            self.db_manager.update_records(conn, table_name)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Records updated in {table_name}\n")
            conn.close()

    def delete_specific(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            self.db_manager.delete_specific_records(conn, table_name)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Specific records deleted from {table_name}\n")
            conn.close()

    def delete_all(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            self.db_manager.delete_all_records(conn, table_name)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"All records deleted from {table_name}\n")
            conn.close()

    def show_table_schema(self):
        conn = self.connect_db()
        if conn:
            table_name = self.entry_table.get()
            schema = self.db_manager.get_table_schema(conn, table_name)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Schema of {table_name}:\n")
            for col in schema:
                self.output_area.insert(tk.END, f"Column: {col[0]}, Type: {col[1]}\n")
            conn.close()
