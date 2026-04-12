import pandas as pd
import time
from sqlalchemy import create_engine, text

# --- DATABASE SETUP ---
DB_USER = 'root'
DB_PASSWORD = 'Mani0804' 
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'olist_db'

engine = create_engine(
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', 
    pool_pre_ping=True
)

# --- FILE MAP ---
files = {
    'customers': 'data/olist_customers_dataset.csv',
    'sellers': 'data/olist_sellers_dataset.csv',
    'products': 'data/olist_products_dataset.csv',
    'orders': 'data/olist_orders_dataset.csv',
    'order_items': 'data/olist_order_items_dataset.csv',
    'order_payments': 'data/olist_order_payments_dataset.csv',
    'order_reviews': 'data/olist_order_reviews_dataset.csv',
    'geolocation': 'data/olist_geolocation_dataset.csv',
    'product_category_name_translation': 'data/product_category_name_translation.csv'
}

# --- THE FIX: TRUNCATE AND APPEND ---
# --- THE FINAL FIX: TRUNCATE IF EXISTS, ELSE CREATE ---
# --- SIMPLIFIED LOAD LOOP ---
with engine.connect() as conn:
    # Disable foreign key checks globally for this session
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    for table_name, filepath in files.items():
        print(f'Loading {table_name}...', end='', flush=True)
        start = time.time()
        
        df = pd.read_csv(filepath, low_memory=False)
        
        # Let Pandas handle the creation/replacement completely
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=1000
        )
        
        elapsed = round(time.time() - start, 1)
        print(f' {len(df):,} rows loaded in {elapsed}s')

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    conn.commit()

print('All tables loaded successfully!')