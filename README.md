# 52
# SQL схема для проекта
# 52

```sql
-- Таблица для хранения информации о пользователях
-- 'id': Уникальный идентификатор для каждого пользователя (генерируется автоматически)
-- 'name': Имя пользователя, не может быть NULL (обязательно для заполнения)
-- 'age': Возраст пользователя, не может быть NULL (обязательно для заполнения)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,         -- Уникальный идентификатор пользователя
    name VARCHAR(100) NOT NULL,    -- Имя пользователя (максимум 100 символов)
    age INTEGER NOT NULL           -- Возраст пользователя (должно быть целым числом)
);

-- Таблица для хранения информации о клиентах
-- 'customer_id': Уникальный идентификатор для каждого клиента (генерируется автоматически)
-- 'customer_name': Имя клиента, обязательно для заполнения
-- 'email': Электронная почта клиента, обязательно для заполнения
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,       -- Уникальный идентификатор клиента
    customer_name VARCHAR(100) NOT NULL,  -- Имя клиента (максимум 100 символов)
    email VARCHAR(100) NOT NULL           -- Электронная почта клиента
);

-- Таблица для хранения информации о продуктах
-- 'product_id': Уникальный идентификатор для каждого продукта (генерируется автоматически)
-- 'product_name': Название продукта, обязательно для заполнения
-- 'price': Цена продукта с точностью до двух десятичных знаков, обязательно для заполнения
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,        -- Уникальный идентификатор продукта
    product_name VARCHAR(100) NOT NULL,   -- Название продукта (максимум 100 символов)
    price DECIMAL(10, 2) NOT NULL         -- Цена продукта (формат: до 10 цифр, 2 после запятой)
);

-- Таблица для хранения информации о заказах
-- 'order_id': Уникальный идентификатор для каждого заказа (генерируется автоматически)
-- 'customer_id': Идентификатор клиента, который сделал заказ
-- 'order_date': Дата и время заказа, по умолчанию устанавливается текущее время
-- 'total_amount': Общая сумма заказа с точностью до двух десятичных знаков
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,          -- Уникальный идентификатор заказа
    customer_id INTEGER NOT NULL,         -- Идентификатор клиента (ссылка на клиента)
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата и время заказа (по умолчанию текущее время)
    total_amount DECIMAL(10, 2) NOT NULL  -- Общая сумма заказа (формат: до 10 цифр, 2 после запятой)
);

-- Таблица для хранения отзывов на продукты
-- 'review_id': Уникальный идентификатор для каждого отзыва (генерируется автоматически)
-- 'product_id': Идентификатор продукта, на который написан отзыв
-- 'user_id': Идентификатор пользователя, который оставил отзыв
-- 'rating': Оценка продукта (от 1 до 5), обязательно для заполнения
-- 'comment': Текстовый комментарий к продукту
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,         -- Уникальный идентификатор отзыва
    product_id INTEGER NOT NULL,          -- Идентификатор продукта (ссылка на продукт)
    user_id INTEGER NOT NULL,             -- Идентификатор пользователя (ссылка на пользователя)
    rating INTEGER NOT NULL,              -- Оценка продукта (должна быть целым числом от 1 до 5)
    comment TEXT                          -- Комментарий к продукту
);
