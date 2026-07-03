import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import mysql.connector
from config import DB_CONFIG

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def truncate_tables(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for t in ["payments", "order_items", "orders", "products", "customers"]:
        cursor.execute(f"TRUNCATE TABLE {t}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("Tables cleared.")

def load_csv(cursor, conn, table, file_name, transform=None):
    path = os.path.join(DATA_DIR, file_name)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if transform:
        rows = [transform(r) for r in rows]

    cols   = rows[0].keys()
    placeholders = ", ".join(["%s"] * len(cols))
    col_names    = ", ".join(cols)
    sql = f"INSERT IGNORE INTO {table} ({col_names}) VALUES ({placeholders})"

    batch = [tuple(r[c] for c in cols) for r in rows]
    cursor.executemany(sql, batch)
    conn.commit()
    print(f"Loaded {cursor.rowcount} rows into {table}")

def clean_customers(row):
    row["customer_name"] = row["customer_name"].strip().title()
    row["email"]         = row["email"].strip().lower()
    return row

def clean_order_items(row):
    row["quantity"]   = int(row["quantity"])
    row["unit_price"] = float(row["unit_price"])
    row["discount"]   = float(row["discount"])
    return row

def main():
    conn   = get_conn()
    cursor = conn.cursor()

    truncate_tables(cursor)

    load_csv(cursor, conn, "customers",   "customers.csv",   transform=clean_customers)
    load_csv(cursor, conn, "products",    "products.csv")
    load_csv(cursor, conn, "orders",      "orders.csv")
    load_csv(cursor, conn, "order_items", "order_items.csv", transform=clean_order_items)
    load_csv(cursor, conn, "payments",    "payments.csv")

    cursor.close()
    conn.close()
    print("\nAll data loaded successfully.")

if __name__ == "__main__":
    main()
