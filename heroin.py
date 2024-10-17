import tkinter as tk
from tkinter import scrolledtext, messagebox
import psycopg2
import random
from faker import Faker
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

insert_logger = logging.getLogger("insert_logger")
insert_handler = logging.FileHandler("insert.log")
insert_handler.setLevel(logging.INFO)
insert_logger.addHandler(insert_handler)

update_logger = logging.getLogger("update_logger")
update_handler = logging.FileHandler("update.log")
update_handler.setLevel(logging.INFO)
update_logger.addHandler(update_handler)

delete_logger = logging.getLogger("delete_logger")
delete_handler = logging.FileHandler("delete.log")
delete_handler.setLevel(logging.INFO)
delete_logger.addHandler(delete_handler)

select_logger = logging.getLogger("select_logger")
select_handler = logging.FileHandler("select.log")
select_handler.setLevel(logging.INFO)
select_logger.addHandler(select_handler)

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

    def insert_records(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            fake = Faker()
            table_name = self.entry_table.get()
            try:
                num_records = int(self.entry_count.get())
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                for _ in range(num_records):
                    if table_name == 'users':
                        name = fake.name()
                        age = random.randint(25, 68)
                        insert_query = f"INSERT INTO {table_name} (name, age) VALUES (%s, %s)"
                        cur.execute(insert_query, (name, age))
                        insert_logger.info(f"Inserted into {table_name}: name={name}, age={age}")
                    elif table_name == 'customers':
                        customer_name = fake.name()
                        email = fake.email()
                        insert_query = f"INSERT INTO {table_name} (customer_name, email) VALUES (%s, %s)"
                        cur.execute(insert_query, (customer_name, email))
                        insert_logger.info(f"Inserted into {table_name}: customer_name={customer_name}, email={email}")
                    elif table_name == 'products':
                        product_name = fake.word()
                        price = round(random.uniform(10.0, 100.0), 2)
                        insert_query = f"INSERT INTO {table_name} (product_name, price) VALUES (%s, %s)"
                        cur.execute(insert_query, (product_name, price))
                        insert_logger.info(f"Inserted into {table_name}: product_name={product_name}, price={price}")
                    elif table_name == 'orders':
                        customer_id = random.randint(1, 10)  # Предположим, что у вас есть 10 покупателей
                        total_amount = round(random.uniform(20.0, 500.0), 2)
                        insert_query = f"INSERT INTO {table_name} (customer_id, total_amount) VALUES (%s, %s)"
                        cur.execute(insert_query, (customer_id, total_amount))
                        insert_logger.info(f"Inserted into {table_name}: customer_id={customer_id}, total_amount={total_amount}")
                    elif table_name == 'reviews':
                        product_id = random.randint(1, 10)  # Предположим, что у вас есть 10 продуктов
                        user_id = random.randint(1, 10)  # Предположим, что у вас есть 10 пользователей
                        rating = random.randint(1, 5)
                        comment = fake.sentence()
                        insert_query = f"INSERT INTO {table_name} (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"
                        cur.execute(insert_query, (product_id, user_id, rating, comment))
                        insert_logger.info(f"Inserted into {table_name}: product_id={product_id}, user_id={user_id}, rating={rating}, comment={comment}")
                    self.output_area.insert(tk.END, f"Executed: {insert_query} with values...\n")
                conn.commit()
                self.output_area.insert(tk.END, f"Inserted {num_records} records successfully into {table_name}.\n")
            except ValueError:
                self.output_area.insert(tk.END, "Please enter a valid number for records.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def update_records(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            table_name = self.entry_table.get()
            try:
                if table_name == 'users':
                    age_condition = random.randint(25, 68)
                    update_query = f"UPDATE {table_name} SET age = age + 1 WHERE age = {age_condition}"
                    update_logger.info(f"Updated in {table_name}: age_condition={age_condition}")
                elif table_name == 'customers':
                    update_query = f"UPDATE {table_name} SET email = 'updated_email@example.com' WHERE customer_id = 1"  # Пример
                    update_logger.info(f"Updated in {table_name}: email updated for customer_id=1")
                elif table_name == 'products':
                    update_query = f"UPDATE {table_name} SET price = price + 5 WHERE product_id = 1"  # Пример
                    update_logger.info(f"Updated in {table_name}: price updated for product_id=1")
                elif table_name == 'orders':
                    update_query = f"UPDATE {table_name} SET total_amount = total_amount + 10 WHERE order_id = 1"  # Пример
                    update_logger.info(f"Updated in {table_name}: total_amount updated for order_id=1")
                elif table_name == 'reviews':
                    update_query = f"UPDATE {table_name} SET rating = 5 WHERE review_id = 1"  # Пример
                    update_logger.info(f"Updated in {table_name}: rating updated for review_id=1")

                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(update_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {update_query}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def delete_specific(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            table_name = self.entry_table.get()
            try:
                if table_name == 'users':
                    age_condition = random.randint(25, 68)
                    delete_query = f"DELETE FROM {table_name} WHERE age = {age_condition}"
                    delete_logger.info(f"Deleted from {table_name}: age_condition={age_condition}")
                elif table_name == 'customers':
                    delete_query = f"DELETE FROM {table_name} WHERE customer_id = 1"  # Пример
                    delete_logger.info(f"Deleted from {table_name}: deleted customer_id=1")
                elif table_name == 'products':
                    delete_query = f"DELETE FROM {table_name} WHERE product_id = 1"  # Пример
                    delete_logger.info(f"Deleted from {table_name}: deleted product_id=1")
                elif table_name == 'orders':
                    delete_query = f"DELETE FROM {table_name} WHERE order_id = 1"  # Пример
                    delete_logger.info(f"Deleted from {table_name}: deleted order_id=1")
                elif table_name == 'reviews':
                    delete_query = f"DELETE FROM {table_name} WHERE review_id = 1"  # Пример
                    delete_logger.info(f"Deleted from {table_name}: deleted review_id=1")

                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(delete_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {delete_query}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

    def delete_all(self):
        conn = self.connect_db()
        if conn:
            cur = conn.cursor()
            table_name = self.entry_table.get()
            try:
                delete_query = f"DELETE FROM {table_name}"
                self.output_area.delete(1.0, tk.END)  # Очистка текстового поля перед выводом новой информации
                cur.execute(delete_query)
                conn.commit()
                self.output_area.insert(tk.END, f"Executed: {delete_query}\n")
                self.output_area.insert(tk.END, f"Deleted all records from {table_name}.\n")
                delete_logger.info(f"Deleted all records from {table_name}.")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
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
                select_logger.info(f"Selected data from {table_name}.")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                cur.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
