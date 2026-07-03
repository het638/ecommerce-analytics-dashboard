import os

DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "localhost"),
    "user":     os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),   # set DB_PASSWORD env var before running
    "database": "ecommerce_analytics",
}
