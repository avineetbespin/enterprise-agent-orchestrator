import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_data():
    """Generate sample sales data for the Multi-Agent Orchestration demo"""

    # Generate dates for the last year
    start_date = datetime.now() - timedelta(days=365)
    dates = [start_date + timedelta(days=i) for i in range(365)]

    # Generate sample sales data
    np.random.seed(42)  # For reproducible results

    products = ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y']
    regions = ['North', 'South', 'East', 'West']

    data = []
    for date in dates:
        for _ in range(np.random.randint(5, 15)):  # 5-15 sales per day
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product': np.random.choice(products),
                'region': np.random.choice(regions),
                'quantity': np.random.randint(1, 10),
                'price': np.random.uniform(10, 100),
                'customer_id': np.random.randint(1000, 9999)
            })

    df = pd.DataFrame(data)
    df['revenue'] = df['quantity'] * df['price']

    return df

def setup_database():
    """Create SQLite database with sample sales data"""

    # Create database connection
    conn = sqlite3.connect('data/sales.db')
    cursor = conn.cursor()

    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product TEXT NOT NULL,
            region TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            revenue REAL NOT NULL,
            customer_id INTEGER NOT NULL
        )
    ''')

    # Generate and insert sample data
    df = create_sample_data()

    # Insert data
    df.to_sql('sales', conn, if_exists='replace', index=False)

    # Create some useful views
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS monthly_sales AS
        SELECT
            strftime('%Y-%m', date) as month,
            SUM(revenue) as total_revenue,
            SUM(quantity) as total_quantity,
            COUNT(*) as num_sales
        FROM sales
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
    ''')

    cursor.execute('''
        CREATE VIEW IF NOT EXISTS product_performance AS
        SELECT
            product,
            SUM(revenue) as total_revenue,
            SUM(quantity) as total_quantity,
            AVG(price) as avg_price,
            COUNT(*) as num_sales
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
    ''')

    cursor.execute('''
        CREATE VIEW IF NOT EXISTS regional_performance AS
        SELECT
            region,
            SUM(revenue) as total_revenue,
            SUM(quantity) as total_quantity,
            COUNT(*) as num_sales
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    ''')

    conn.commit()
    conn.close()

    print("Database created successfully with sample sales data!")
    print(f"Generated {len(df)} sales records")

if __name__ == "__main__":
    setup_database()