import tkinter as tk
from tkinter import scrolledtext
from database import DatabaseActions
from performance import record_performance
from logging_util import setup_logging
import time

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("База данных PostgreSQL")
        self.root.geometry("700x1100")

        # Инициализация действий с БД и логирования
        self.db_actions = DatabaseActions()
        self.loggers = setup_logging()

        # Настройки для растягивания окна
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(25, weight=1)

        # Поля для ввода данных подключения
        self.entry_host = self.create_labeled_entry("Хост:", 0)
        self.entry_port = self.create_labeled_entry("Порт:", 2)
        self.entry_dbname = self.create_labeled_entry("Имя базы данных:", 4)
        self.entry_user = self.create_labeled_entry("Пользователь:", 6)
        self.entry_password = self.create_labeled_entry("Пароль:", 8, show="*")
        self.entry_table = self.create_labeled_entry("Имя таблицы:", 10)
        self.entry_num_queries = self.create_labeled_entry("Количество запросов:", 12)

        # Кнопки для действий
        self.button_show_tables = tk.Button(self.root, text="Показать список таблиц", command=self.show_tables, width=40)
        self.button_show_tables.grid(row=14, column=0, pady=5)

        self.button_show_structure = tk.Button(self.root, text="Показать структуру таблицы", command=self.show_table_structure, width=40)
        self.button_show_structure.grid(row=15, column=0, pady=5)

        self.button_show_data = tk.Button(self.root, text="Показать данные из таблицы", command=self.show_table_data, width=40)
        self.button_show_data.grid(row=16, column=0, pady=5)

        self.button_insert_data = tk.Button(self.root, text="Вставить данные в таблицу", command=self.insert_data, width=40)
        self.button_insert_data.grid(row=17, column=0, pady=5)

        self.button_delete_records = tk.Button(self.root, text="Удалить все записи", command=self.delete_all_records, width=40)
        self.button_delete_records.grid(row=18, column=0, pady=5)

        self.button_delete_specific_records = tk.Button(self.root, text="Удалить определённые записи", command=self.delete_specific_records, width=40)
        self.button_delete_specific_records.grid(row=19, column=0, pady=5)

        self.button_update_records = tk.Button(self.root, text="Обновить данные в таблице", command=self.update_records, width=40)
        self.button_update_records.grid(row=20, column=0, pady=5)

        self.button_exit = tk.Button(self.root, text="Выйти", command=self.exit_program, width=40)
        self.button_exit.grid(row=21, column=0, pady=5)

        # Окно для вывода информации
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.output_text.grid(row=22, column=0, pady=10, padx=10, sticky='nsew')

        # Поля для вывода характеристик производительности
        self.performance_label = tk.Label(self.root, text="Характеристики производительности:")
        self.performance_label.grid(row=23, column=0, sticky='w', padx=10)

        self.performance_text = scrolledtext.ScrolledText(self.root, height=5, wrap=tk.WORD)
        self.performance_text.grid(row=24, column=0, padx=10, pady=5, sticky='nsew')

    def create_labeled_entry(self, label_text, row, show=None):
        label = tk.Label(self.root, text=label_text, width=20, anchor='w')
        label.grid(row=row, column=0, padx=0, pady=0)
        entry = tk.Entry(self.root, width=30, show=show)
        entry.grid(row=row + 1, column=0, padx=0, pady=0)
        return entry

    def show_tables(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        if conn:
            try:
                start_time = time.time()
                query, tables = self.db_actions.show_tables(conn)
                for table in tables:
                    self.output_text.insert(tk.END, f"{table[0]}\n")
                self.loggers['show_tables'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def show_table_structure(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()
        if conn and table_name:
            try:
                start_time = time.time()
                query, structure = self.db_actions.show_table_structure(conn, table_name)
                if structure:
                    for column in structure:
                        self.output_text.insert(tk.END, f"Колонка: {column[0]}, Тип: {column[1]}, NULL: {column[2]}\n")
                else:
                    self.output_text.insert(tk.END, f"Таблица {table_name} не найдена.\n")
                self.loggers['show_structure'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def show_table_data(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()
        if conn and table_name:
            try:
                start_time = time.time()
                query, rows = self.db_actions.show_table_data(conn, table_name)
                for row in rows:
                    self.output_text.insert(tk.END, f"{row}\n")
                self.loggers['show_data'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def insert_data(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()
        num_queries = int(self.entry_num_queries.get())

        if conn and table_name and num_queries:
            try:
                start_time = time.time()
                queries = self.db_actions.insert_data(conn, table_name, num_queries)
                for query in queries:
                    self.output_text.insert(tk.END, f"{query}\n")
                self.loggers['insert_data'].info(f"SQL Queries: {queries}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def delete_all_records(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()

        if conn and table_name:
            try:
                start_time = time.time()
                query = self.db_actions.delete_all_records(conn, table_name)
                self.output_text.insert(tk.END, f"Все записи из таблицы {table_name} были удалены.\n")
                self.loggers['delete_records'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def delete_specific_records(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()

        if conn and table_name:
            try:
                start_time = time.time()
                query = self.db_actions.delete_specific_records(conn, table_name)
                self.output_text.insert(tk.END, f"Удаление записей из таблицы {table_name} выполнено.\n")
                self.loggers['delete_records'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def update_records(self):
        self.output_text.delete(1.0, tk.END)
        conn = self.db_actions.connect_to_db(
            self.entry_host.get(), self.entry_port.get(), self.entry_dbname.get(), 
            self.entry_user.get(), self.entry_password.get()
        )
        table_name = self.entry_table.get()

        if conn and table_name:
            try:
                start_time = time.time()
                query = self.db_actions.update_records(conn, table_name)
                self.output_text.insert(tk.END, f"Обновление записей в таблице {table_name} выполнено.\n")
                self.loggers['update_records'].info(f"SQL Query: {query}")
                record_performance(start_time, self.performance_text)
            finally:
                conn.close()

    def exit_program(self):
        self.root.quit()
