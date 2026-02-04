import yfinance as yf
import duckdb
import pandas as pd

# 1. CONFIGURATION
TICKERS = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
DB_NAME = 'finance.duckdb'

def extract_data(tickers):
    """Downloads historical data from Yahoo Finance."""
    print(f"Downloading data for: {', '.join(tickers)}...")
    
    # download last 5 years of data
    data = yf.download(tickers, period="5y", group_by='ticker', auto_adjust=True)
    
    # yfinance returns a complex MultiIndex. We need to flatten it for the database.
    # The structure is usually: (Date, Ticker) -> (Open, High, Low, Close, Volume)
    
    # Stack the data to get Ticker as a column
    data = data.stack(level=0).reset_index()
    
    # Rename columns to be database-friendly (no spaces, lowercase)
    data.columns = ['date', 'ticker', 'close', 'high', 'low', 'open', 'volume']
    
    # Ensure date is a proper date object (removes time component)
    data['date'] = data['date'].dt.date
    
    return data

def load_to_duckdb(df, db_name):
    """Loads the pandas DataFrame into a DuckDB table."""
    conn = duckdb.connect(db_name)
    
    # This single line does the magic:
    # 1. Creates table 'raw_stock_data' if missing
    # 2. Replaces it if it exists (for now, we will do full reload for simplicity)
    conn.execute("CREATE OR REPLACE TABLE raw_stock_data AS SELECT * FROM df")
    
    row_count = conn.execute("SELECT COUNT(*) FROM raw_stock_data").fetchone()[0]
    print(f"Success! Loaded {row_count} rows into {db_name}")
    
    # Verify a few rows
    print("\nSample Data:")
    print(conn.execute("SELECT * FROM raw_stock_data LIMIT 5").df())
    
    conn.close()

if __name__ == "__main__":
    df = extract_data(TICKERS)
    load_to_duckdb(df, DB_NAME)