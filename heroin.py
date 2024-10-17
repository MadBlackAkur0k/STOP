import tkinter as tk
from tkinter import scrolledtext, messagebox
import psycopg2
import random
from faker import Faker

class DatabaseApp:
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

        # Ввод названия таблицы
        self.label_table = tk.Label(master, text="Table Name:")
        self.label_table.grid(row=6, column=0)
        self.entry_table = tk.Entry(master)
        self.entry_table.grid(row=6, column=1)

        # Кнопки
        self.button_show_tables = tk.Button(master, text="Show Tables", command=self.show_tables)
        self.button_show_tables.grid(row=7, column=0, columnspan=2)

        self.button_select = tk.Button(master, text="Select Data", command=self.select_data)
        self.button_select.grid(row=8, column=0, columnspan=2)

        self.button_insert_all = tk.Button(master, text="Insert Records", command=self.insert_all)
        self.button_insert_all.grid(row=9, column=0, columnspan=2)

        self.button_update = tk.Button(master, text="Update Records", command=self.update)
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

    def connect_db(self):
        db = self.entry_db.get()
        host = self.entry_host.get()
        port = self.entry_port.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        try:
            conn = psycopg2.connect(database=db, host=host, port=port, user=user, password=password)
            return conn
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return None

    def show_table_schema(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            table_name = self.entry_table.get()
            self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
            try:
                query = f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                """
                cur.execute(query)
                columns = cur.fetchall()
                if columns:
                    self.output_area.insert(tk.END, f"Schema of table '{table_name}':\n")
                    for column in columns:
                        self.output_area.insert(tk.END, f"Column: {column[0]}, Type: {column[1]}\n")
                else:
                    self.output_area.insert(tk.END, f"No columns found for table '{table_name}'.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def insert_all(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            fake = Faker()
            try:
                num_records = int(self.entry_count.get())
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                for _ in range(num_records):
                    name = fake.name()
                    age = random.randint(25, 68)  # Возраст от 25 до 68
                    insert_query = f"INSERT INTO {self.entry_table.get()} (name, age) VALUES (%s, %s)"
                    cur.execute(insert_query, (name, age))
                    self.output_area.insert(tk.END, f"Executed: {insert_query} with values ({name}, {age})\n")
                conn.commit()
                self.output_area.insert(tk.END, f"Inserted {num_records} records successfully into {self.entry_table.get()}.\n")
            except ValueError:
                self.output_area.insert(tk.END, "Please enter a valid number for records.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def update(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            try:
                table_name = self.entry_table.get()
                age_condition = random.randint(25, 68)  # Случайный возраст для условия обновления
                update_query = f"UPDATE {table_name} SET age = age + 1 WHERE age = {age_condition}"
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(update_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {update_query}\n")
                self.output_area.insert(tk.END, f"Updated records in {table_name} where age = {age_condition}.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def delete_specific(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            try:
                table_name = self.entry_table.get()
                age_condition = random.randint(25, 68)  # Случайный возраст для условия удаления
                delete_query = f"DELETE FROM {table_name} WHERE age = {age_condition}"
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(delete_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {delete_query}\n")
                self.output_area.insert(tk.END, f"Deleted specific records from {table_name} where age = {age_condition}.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def delete_all(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            try:
                table_name = self.entry_table.get()
                delete_query = f"DELETE FROM {table_name}"
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(delete_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {delete_query}\n")
                self.output_area.insert(tk.END, f"Deleted all records from {table_name}.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def show_tables(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cur.fetchall()
            self.output_area.insert(tk.END, "List of tables:\n")
            for table in tables:
                self.output_area.insert(tk.END, f"{table[0]}\n")
            cur.close()
            conn.close()

    def select_data(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            table_name = self.entry_table.get()
            select_query = f"SELECT * FROM {table_name}"
            self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
            try:
                cur.execute(select_query)
                results = cur.fetchall()
                self.output_area.insert(tk.END, f"Executed: {select_query}\n")
                for row in results:
                    self.output_area.insert(tk.END, f"{row}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
