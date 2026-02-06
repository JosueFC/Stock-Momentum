import yfinance as yf
import duckdb
import pandas as pd
import os

# --- 1. ROBUST PATH CONFIGURATION ---
# Get the absolute path of the folder where this script lives (.../Stock-Momentum/scripts)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project root (.../Stock-Momentum)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Define the path to the data folder
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Ensure the 'data' folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Define the full path to the database file
DB_PATH = os.path.join(DATA_DIR, 'finance.duckdb')

TICKERS = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

def extract_data(tickers):
    """Downloads historical data from Yahoo Finance."""
    print(f"Downloading data for: {', '.join(tickers)}...")
    
    # Download last 5 years of data
    data = yf.download(tickers, period="5y", group_by='ticker', auto_adjust=True)
    
    # FIX for the Warning: stack the data to get Ticker as a column
    # We use future_stack=True to silence the Pandas warning
    data = data.stack(level=0, future_stack=True).reset_index()
    
    # Rename columns to be database-friendly
    data.columns = ['date', 'ticker', 'close', 'high', 'low', 'open', 'volume']
    
    # Ensure date is a proper date object
    data['date'] = data['date'].dt.date
    
    return data

def load_to_duckdb(df, db_path):
    """Loads the pandas DataFrame into a DuckDB table."""
    print(f"Connecting to database at: {db_path}")
    conn = duckdb.connect(db_path)
    
    # Create or replace the table
    conn.execute("CREATE OR REPLACE TABLE raw_stock_data AS SELECT * FROM df")
    
    row_count = conn.execute("SELECT COUNT(*) FROM raw_stock_data").fetchone()[0]
    print(f"Success! Loaded {row_count} rows.")
    
    # Verify a few rows
    print("\nSample Data:")
    print(conn.execute("SELECT * FROM raw_stock_data LIMIT 5").df())
    
    conn.close()

if __name__ == "__main__":
    try:
        df = extract_data(TICKERS)
        load_to_duckdb(df, DB_PATH)
    except Exception as e:
        print(f"\n❌ Error: {e}")