import psycopg2
from faker import Faker
import random
from logging_setup import insert_logger, update_logger, delete_logger, select_logger

class DatabaseManager:
    def __init__(self):
        self.fake = Faker()

    def connect_db(self, db, host, port, user, password):
        try:
            conn = psycopg2.connect(database=db, host=host, port=port, user=user, password=password)
            return conn
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def get_tables(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cur.fetchall()
        cur.close()
        return tables

    def insert_records(self, conn, table_name, num_records):
        cur = conn.cursor()
        for _ in range(num_records):
            if table_name == 'users':
                name = self.fake.name()
                age = random.randint(25, 68)
                insert_query = f"INSERT INTO {table_name} (name, age) VALUES (%s, %s)"
                cur.execute(insert_query, (name, age))
                insert_logger.info(f"Inserted into {table_name}: name={name}, age={age}")
        conn.commit()
        cur.close()

    def select_data(self, conn, table_name):
        cur = conn.cursor()
        select_query = f"SELECT * FROM {table_name}"
        cur.execute(select_query)
        results = cur.fetchall()
        cur.close()
        return results

    def update_records(self, conn, table_name):
        cur = conn.cursor()
        update_query = f"UPDATE {table_name} SET age = age + 1 WHERE age > 30"
        cur.execute(update_query)
        conn.commit()
        update_logger.info(f"Updated records in {table_name}")
        cur.close()

    def delete_specific_records(self, conn, table_name):
        cur = conn.cursor()
        delete_query = f"DELETE FROM {table_name} WHERE age < 30"
        cur.execute(delete_query)
        conn.commit()
        delete_logger.info(f"Deleted specific records in {table_name}")
        cur.close()

    def delete_all_records(self, conn, table_name):
        cur = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cur.execute(delete_query)
        conn.commit()
        delete_logger.info(f"Deleted all records in {table_name}")
        cur.close()

    def get_table_schema(self, conn, table_name):
        cur = conn.cursor()
        query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
        cur.execute(query)
        schema = cur.fetchall()
        cur.close()
        return schema
