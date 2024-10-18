import psycopg2
from faker import Faker
import random

class DatabaseActions:
    def __init__(self):
        self.fake = Faker()

    def connect_to_db(self, host, port, dbname, user, password):
        """
        Подключение к базе данных PostgreSQL.
        Возвращает объект соединения или None в случае ошибки.
        """
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            return conn
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return None

    def show_tables(self, conn):
        """
        Возвращает список таблиц из базы данных.
        """
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        cur = conn.cursor()
        cur.execute(query)
        tables = cur.fetchall()
        cur.close()
        return query, tables

    def show_table_structure(self, conn, table_name):
        """
        Возвращает структуру таблицы: названия колонок, их типы и возможность NULL.
        """
        query = """
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """
        cur = conn.cursor()
        cur.execute(query, (table_name,))
        structure = cur.fetchall()
        cur.close()
        return query, structure

    def show_table_data(self, conn, table_name):
        """
        Возвращает все данные из указанной таблицы.
        """
        query = f"SELECT * FROM {table_name};"
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return query, rows

    def insert_data(self, conn, table_name, num_queries):
        """
        Вставляет данные в указанную таблицу.
        Генерирует случайные данные в зависимости от таблицы.
        """
        cur = conn.cursor()
        queries = []

        for _ in range(num_queries):
            if table_name == 'users':
                name = self.fake.name()
                age = random.randint(25, 68)
                insert_query = f"INSERT INTO {table_name} (name, age) VALUES (%s, %s)"
                cur.execute(insert_query, (name, age))
                queries.append(insert_query % (name, age))

            elif table_name == 'customers':
                customer_name = self.fake.company()
                email = self.fake.email()
                insert_query = f"INSERT INTO {table_name} (customer_name, email) VALUES (%s, %s)"
                cur.execute(insert_query, (customer_name, email))
                queries.append(insert_query % (customer_name, email))

            elif table_name == 'products':
                product_name = self.fake.word()
                price = round(random.uniform(10.0, 1000.0), 2)
                insert_query = f"INSERT INTO {table_name} (product_name, price) VALUES (%s, %s)"
                cur.execute(insert_query, (product_name, price))
                queries.append(insert_query % (product_name, price))

            elif table_name == 'orders':
                customer_id = random.randint(1, 100)
                total_amount = round(random.uniform(50.0, 5000.0), 2)
                insert_query = f"INSERT INTO {table_name} (customer_id, total_amount) VALUES (%s, %s)"
                cur.execute(insert_query, (customer_id, total_amount))
                queries.append(insert_query % (customer_id, total_amount))

            elif table_name == 'reviews':
                product_id = random.randint(1, 100)
                user_id = random.randint(1, 100)
                rating = random.randint(1, 5)
                comment = self.fake.text()
                insert_query = f"INSERT INTO {table_name} (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"
                cur.execute(insert_query, (product_id, user_id, rating, comment))
                queries.append(insert_query % (product_id, user_id, rating, comment))

        conn.commit()
        cur.close()
        return queries

    def delete_all_records(self, conn, table_name):
        """
        Удаляет все записи из указанной таблицы.
        """
        cur = conn.cursor()
        delete_query = f"DELETE FROM {table_name};"
        cur.execute(delete_query)
        conn.commit()
        cur.close()
        return delete_query

    def delete_specific_records(self, conn, table_name):
        """
        Удаляет случайные записи на основе случайно выбранных значений.
        """
        cur = conn.cursor()

        if table_name == 'users':
            cur.execute(f"SELECT DISTINCT age FROM {table_name};")
            existing_ages = cur.fetchall()
            if existing_ages:
                random_age = random.choice(existing_ages)[0]
                delete_query = f"DELETE FROM {table_name} WHERE age = %s;"
                cur.execute(delete_query, (random_age,))
                conn.commit()
                cur.close()
                return delete_query % random_age

        elif table_name == 'customers':
            cur.execute(f"SELECT DISTINCT email FROM {table_name};")
            existing_emails = cur.fetchall()
            if existing_emails:
                random_email = random.choice(existing_emails)[0]
                delete_query = f"DELETE FROM {table_name} WHERE email = %s;"
                cur.execute(delete_query, (random_email,))
                conn.commit()
                cur.close()
                return delete_query % random_email

        elif table_name == 'products':
            cur.execute(f"SELECT DISTINCT price FROM {table_name};")
            existing_prices = cur.fetchall()
            if existing_prices:
                random_price = random.choice(existing_prices)[0]
                delete_query = f"DELETE FROM {table_name} WHERE price = %s;"
                cur.execute(delete_query, (random_price,))
                conn.commit()
                cur.close()
                return delete_query % random_price

        elif table_name == 'orders':
            cur.execute(f"SELECT DISTINCT customer_id FROM {table_name};")
            existing_customer_ids = cur.fetchall()
            if existing_customer_ids:
                random_customer_id = random.choice(existing_customer_ids)[0]
                delete_query = f"DELETE FROM {table_name} WHERE customer_id = %s;"
                cur.execute(delete_query, (random_customer_id,))
                conn.commit()
                cur.close()
                return delete_query % random_customer_id

        elif table_name == 'reviews':
            cur.execute(f"SELECT DISTINCT rating FROM {table_name};")
            existing_ratings = cur.fetchall()
            if existing_ratings:
                random_rating = random.choice(existing_ratings)[0]
                delete_query = f"DELETE FROM {table_name} WHERE rating = %s;"
                cur.execute(delete_query, (random_rating,))
                conn.commit()
                cur.close()
                return delete_query % random_rating

    def update_records(self, conn, table_name):
        """
        Обновляет случайные записи в таблице, используя случайно выбранные значения.
        """
        cur = conn.cursor()

        if table_name == 'users':
            cur.execute(f"SELECT id FROM {table_name};")
            existing_ids = cur.fetchall()
            if existing_ids:
                random_id = random.choice(existing_ids)[0]
                new_name = self.fake.name()
                update_query = f"UPDATE {table_name} SET name = %s WHERE id = %s;"
                cur.execute(update_query, (new_name, random_id))
                conn.commit()
                cur.close()
                return update_query % (new_name, random_id)

        elif table_name == 'customers':
            cur.execute(f"SELECT customer_id FROM {table_name};")
            existing_ids = cur.fetchall()
            if existing_ids:
                random_customer_id = random.choice(existing_ids)[0]
                new_email = self.fake.email()
                update_query = f"UPDATE {table_name} SET email = %s WHERE customer_id = %s;"
                cur.execute(update_query, (new_email, random_customer_id))
                conn.commit()
                cur.close()
                return update_query % (new_email, random_customer_id)

        elif table_name == 'products':
            cur.execute(f"SELECT product_id FROM {table_name};")
            existing_ids = cur.fetchall()
            if existing_ids:
                random_product_id = random.choice(existing_ids)[0]
                new_price = round(random.uniform(10.0, 1000.0), 2)
                update_query = f"UPDATE {table_name} SET price = %s WHERE product_id = %s;"
                cur.execute(update_query, (new_price, random_product_id))
                conn.commit()
                cur.close()
                return update_query % (new_price, random_product_id)

        elif table_name == 'orders':
            cur.execute(f"SELECT order_id FROM {table_name};")
            existing_ids = cur.fetchall()
            if existing_ids:
                random_order_id = random.choice(existing_ids)[0]
                new_total_amount = round(random.uniform(50.0, 5000.0), 2)
                update_query = f"UPDATE {table_name} SET total_amount = %s WHERE order_id = %s;"
                cur.execute(update_query, (new_total_amount, random_order_id))
                conn.commit()
                cur.close()
                return update_query % (new_total_amount, random_order_id)

        elif table_name == 'reviews':
            cur.execute(f"SELECT review_id FROM {table_name};")
            existing_ids = cur.fetchall()
            if existing_ids:
                random_review_id = random.choice(existing_ids)[0]
                new_rating = random.randint(1, 5)
                update_query = f"UPDATE {table_name} SET rating = %s WHERE review_id = %s;"
                cur.execute(update_query, (new_rating, random_review_id))
                conn.commit()
                cur.close()
                return update_query % (new_rating, random_review_id)
