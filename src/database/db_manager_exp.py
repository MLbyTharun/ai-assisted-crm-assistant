import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "crm.db")

def init_db():
    """Creates the database and seeds it with mock records if empty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            company TEXT,
            last_purchase_item TEXT,
            last_interaction_date DATE,
            customer_notes TEXT
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("Alice", "TechCorp", "SaaS Enterprise Subscription", "2022-06-21", "Loves the platform but mentioned budget constraints last quarter."),
            ("Bob", "DesignStudio", "Pro Design Toolkit Bundle","2022-06-22", "Highly engaged, left a great review. Might be ready for an upsell."),
            ("Charlie", "RetailCo", "Basic Analytics Dashboard","2022-06-24", "Ghosted after implementation. Needs a strong re-engagement hook."),
            ("Diana", "GrowthMedia", "Premium API Access", "2022-06-25", "Just onboarded. Experienced a small bug during setup that was fixed.")
        ]
        cursor.executemany('''
            INSERT INTO customers (first_name, company, last_purchase_item, days_since_last_interaction, customer_notes)
            VALUES (?, ?, ?, ?, ?)
        ''', mock_data)
        conn.commit()
    conn.close()

def get_customers_df():
    """Fetches all database entries as a Pandas DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df