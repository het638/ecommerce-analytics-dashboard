"""
Run this once to set up the entire project:
  1. Creates the MySQL database and tables
  2. Generates sample data CSVs
  3. Loads data into MySQL
  4. Creates all analytics views
"""
import os
import sys
import subprocess
import mysql.connector
from mysql.connector import errorcode

sys.path.insert(0, os.path.dirname(__file__))
from config import DB_CONFIG

BASE = os.path.dirname(__file__)

def run_sql_file(path, conn):
    with open(path, "r", encoding="utf-8") as f:
        statements = [s.strip() for s in f.read().split(";") if s.strip()]
    cursor = conn.cursor()
    for stmt in statements:
        try:
            cursor.execute(stmt)
            conn.commit()
        except mysql.connector.Error as e:
            if e.errno not in (errorcode.ER_TABLE_EXISTS_ERROR,):
                print(f"  Warning: {e}")
    cursor.close()

def step(msg):
    print(f"\n{'='*55}\n  {msg}\n{'='*55}")

# ── Step 1: Create DB + tables ────────────────────────────────
step("Step 1/4 — Creating database and tables")
cfg_no_db = {k: v for k, v in DB_CONFIG.items() if k != "database"}
conn = mysql.connector.connect(**cfg_no_db)
run_sql_file(os.path.join(BASE, "sql", "schema.sql"), conn)
conn.close()
print("  Done.")

# ── Step 2: Generate CSVs ─────────────────────────────────────
step("Step 2/4 — Generating sample data")
subprocess.run([sys.executable, os.path.join(BASE, "scripts", "generate_data.py")], check=True)

# ── Step 3: Load data ─────────────────────────────────────────
step("Step 3/4 — Loading data into MySQL")
subprocess.run([sys.executable, os.path.join(BASE, "scripts", "load_data.py")], check=True)

# ── Step 4: Create views ──────────────────────────────────────
step("Step 4/4 — Creating analytics views")
conn = mysql.connector.connect(**DB_CONFIG)
run_sql_file(os.path.join(BASE, "sql", "views.sql"), conn)
conn.close()
print("  Done.")

print("\n" + "="*55)
print("  Setup complete! Connect Power BI to MySQL:")
print("  Server: localhost   Database: ecommerce_analytics")
print("="*55)
