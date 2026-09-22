import time
import yfinance as yf

def fetch_stock_data(ticker_symbol, retries=3):
    ticker = yf.Ticker(ticker_symbol)
    for attempt in range(retries):
        try:
            # Fetch data with explicit timeout limit
            data = ticker.history(period="1y", timeout=10)
            if not data.empty:
                return data
        except Exception as e:
            time.sleep(1)  # Pause briefly before retrying
    return None
