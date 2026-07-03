CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

CREATE TABLE IF NOT EXISTS customers (
    customer_id     VARCHAR(36) PRIMARY KEY,
    customer_name   VARCHAR(100) NOT NULL,
    email           VARCHAR(150),
    city            VARCHAR(100),
    state           VARCHAR(100),
    country         VARCHAR(100),
    registration_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id      VARCHAR(36) PRIMARY KEY,
    product_name    VARCHAR(200) NOT NULL,
    category        VARCHAR(100),
    price           DECIMAL(10,2),
    cost            DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR(36) PRIMARY KEY,
    customer_id     VARCHAR(36),
    order_date      DATE,
    status          VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id   INT AUTO_INCREMENT PRIMARY KEY,
    order_id        VARCHAR(36),
    product_id      VARCHAR(36),
    quantity        INT,
    unit_price      DECIMAL(10,2),
    discount        DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id        VARCHAR(36),
    payment_date    DATE,
    amount          DECIMAL(10,2),
    method          VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
