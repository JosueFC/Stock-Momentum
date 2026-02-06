import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import os

# --- CONFIGURATION ---
# Robust pathing again!
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'finance.duckdb')

st.set_page_config(page_title="Stock Momentum Dashboard", layout="wide")
st.title("📈 Stock Momentum Indicator")
st.markdown("Automated pipeline: **Yahoo Finance -> DuckDB -> dbt -> Streamlit**")

# --- CONNECT TO DATA ---
@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH, read_only=True)
    # We query the FINAL Mart table created by dbt
    df = con.execute("SELECT * FROM mart_momentum_indicators").df()
    con.close()
    return df

try:
    df = load_data()
    
    # --- SIDEBAR FILTERS ---
    tickers = df['ticker_symbol'].unique()
    selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)
    
    # Filter data
    ticker_df = df[df['ticker_symbol'] == selected_ticker].sort_values('market_date')

    # --- METRICS ---
    latest_row = ticker_df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Close", f"${latest_row['close_price']:.2f}")
    col2.metric("Signal", latest_row['momentum_signal'], 
                delta_color="normal" if latest_row['momentum_signal'] == "NEUTRAL" else "inverse")
    
    # --- CHART ---
    st.subheader(f"Price vs Moving Averages: {selected_ticker}")
    
    fig = go.Figure()
    
    # Candlestick
    fig.add_trace(go.Scatter(x=ticker_df['market_date'], y=ticker_df['close_price'],
                             mode='lines', name='Close Price', line=dict(color='black', width=1)))
    
    # 50-Day MA
    fig.add_trace(go.Scatter(x=ticker_df['market_date'], y=ticker_df['ma_50_day'],
                             mode='lines', name='50-Day MA', line=dict(color='blue', width=2)))
    
    # 200-Day MA
    fig.add_trace(go.Scatter(x=ticker_df['market_date'], y=ticker_df['ma_200_day'],
                             mode='lines', name='200-Day MA', line=dict(color='orange', width=2)))

    fig.update_layout(height=600, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # --- RAW DATA VIEW ---
    with st.expander("See Raw Data from Warehouse"):
        st.dataframe(ticker_df.sort_values('market_date', ascending=False))

except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.info("Did you run `python scripts/extract_load.py` and `dbt run` first?")