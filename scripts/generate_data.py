import csv
import uuid
import random
from datetime import date, timedelta
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty", "Food & Grocery"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
STATES = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Telangana", "Maharashtra", "Gujarat"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
ORDER_STATUSES = ["delivered", "delivered", "delivered", "cancelled", "returned"]

PRODUCT_NAMES = {
    "Electronics":    ["Smartphone X12", "Laptop Pro", "Wireless Earbuds", "Smart TV 43\"", "Tablet Z", "Bluetooth Speaker"],
    "Clothing":       ["Cotton T-Shirt", "Denim Jeans", "Summer Dress", "Formal Shirt", "Woolen Jacket", "Track Pants"],
    "Home & Garden":  ["Coffee Maker", "Air Purifier", "Bedsheet Set", "Curtains", "Garden Hose", "LED Bulb Pack"],
    "Sports":         ["Yoga Mat", "Dumbbells 5kg", "Running Shoes", "Cricket Bat", "Badminton Racket", "Cycling Helmet"],
    "Books":          ["Python Cookbook", "Data Science 101", "Business Strategy", "Fiction Novel", "Self Help Guide", "History of Art"],
    "Toys":           ["LEGO Classic Set", "Remote Car", "Board Game", "Stuffed Elephant", "Puzzle 1000pc", "Action Figure"],
    "Beauty":         ["Face Serum", "Sunscreen SPF50", "Shampoo 400ml", "Lipstick Set", "Moisturizer", "Perfume 50ml"],
    "Food & Grocery": ["Organic Honey", "Mixed Nuts 500g", "Green Tea 100bags", "Olive Oil 1L", "Protein Bar 12pk", "Coffee Beans"],
}

PRICE_RANGE = {
    "Electronics": (3000, 80000),
    "Clothing":    (299, 3000),
    "Home & Garden": (199, 15000),
    "Sports":      (399, 8000),
    "Books":       (99, 999),
    "Toys":        (199, 5000),
    "Beauty":      (149, 3000),
    "Food & Grocery": (99, 1500),
}

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = date(2022, 1, 1)
end_date   = date(2024, 12, 31)

# --- Customers ---
NUM_CUSTOMERS = 2000
customers = []
for _ in range(NUM_CUSTOMERS):
    idx = random.randint(0, len(CITIES) - 1)
    reg = random_date(date(2020, 1, 1), date(2022, 6, 30))
    customers.append({
        "customer_id": str(uuid.uuid4()),
        "customer_name": f"Customer_{random.randint(1000,9999)}",
        "email": f"user{random.randint(10000,99999)}@example.com",
        "city": CITIES[idx],
        "state": STATES[idx],
        "country": "India",
        "registration_date": reg.isoformat(),
    })

with open(os.path.join(OUTPUT_DIR, "customers.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=customers[0].keys())
    w.writeheader(); w.writerows(customers)
print(f"Generated {len(customers)} customers")

# --- Products ---
products = []
for cat, names in PRODUCT_NAMES.items():
    lo, hi = PRICE_RANGE[cat]
    for name in names:
        price = round(random.uniform(lo, hi), 2)
        cost  = round(price * random.uniform(0.4, 0.7), 2)
        products.append({
            "product_id":   str(uuid.uuid4()),
            "product_name": name,
            "category":     cat,
            "price":        price,
            "cost":         cost,
        })

with open(os.path.join(OUTPUT_DIR, "products.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=products[0].keys())
    w.writeheader(); w.writerows(products)
print(f"Generated {len(products)} products")

# --- Orders & Order Items & Payments ---
NUM_ORDERS = 15000
orders, order_items, payments = [], [], []

for _ in range(NUM_ORDERS):
    customer   = random.choice(customers)
    order_date = random_date(start_date, end_date)
    status     = random.choice(ORDER_STATUSES)
    order_id   = str(uuid.uuid4())

    orders.append({
        "order_id":    order_id,
        "customer_id": customer["customer_id"],
        "order_date":  order_date.isoformat(),
        "status":      status,
    })

    num_items  = random.randint(1, 5)
    order_total = 0.0
    for _ in range(num_items):
        product  = random.choice(products)
        qty      = random.randint(1, 4)
        discount = round(random.choice([0, 0, 0, 5, 10, 15]), 2)
        order_items.append({
            "order_id":    order_id,
            "product_id":  product["product_id"],
            "quantity":    qty,
            "unit_price":  product["price"],
            "discount":    discount,
        })
        order_total += product["price"] * qty * (1 - discount / 100)

    if status != "cancelled":
        pay_date = order_date + timedelta(days=random.randint(0, 3))
        payments.append({
            "order_id":     order_id,
            "payment_date": pay_date.isoformat(),
            "amount":       round(order_total, 2),
            "method":       random.choice(PAYMENT_METHODS),
        })

with open(os.path.join(OUTPUT_DIR, "orders.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=orders[0].keys())
    w.writeheader(); w.writerows(orders)
print(f"Generated {len(orders)} orders")

with open(os.path.join(OUTPUT_DIR, "order_items.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=order_items[0].keys())
    w.writeheader(); w.writerows(order_items)
print(f"Generated {len(order_items)} order items")

with open(os.path.join(OUTPUT_DIR, "payments.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=payments[0].keys())
    w.writeheader(); w.writerows(payments)
print(f"Generated {len(payments)} payments")

print("\nAll CSV files saved to data/raw/")
