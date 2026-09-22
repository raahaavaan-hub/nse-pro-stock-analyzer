import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as gg

st.set_page_config(
    page_title="NSE PRO", 
    page_icon="📈", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
.nse-card { padding: 18px; border: 1px solid rgba(128,128,128,.25); border-radius: 12px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# Sidebar Routing
st.sidebar.title("📈 NSE PRO")
st.sidebar.caption("Stock analysis platform")
page = st.sidebar.radio("MENU", [
    "🏠 Dashboard", 
    "🔎 Stock Analyzer", 
    "🚀 Swing Screener", 
    "📰 News", 
    "🏛️ Institutional Watch"
])
st.sidebar.divider()

# Helper Functions for Indicators
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Page: Stock Analyzer
if page == "🔎 Stock Analyzer":
    st.title("🔎 Stock Analyzer")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        ticker_input = st.text_input("Enter NSE Stock Ticker (e.g., RELIANCE, TATAMOTORS, INFYS)", value="RELIANCE")
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    with col3:
        interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

    # Convert to yfinance NSE format (.NS)
    symbol = ticker_input.strip().upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    try:
        data = yf.download(symbol, period=period, interval=interval)
        
        if data.empty:
            st.error(f"No data found for symbol `{symbol}`.")
        else:
            # Calculate Indicators
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
            data['RSI'] = compute_rsi(data)
            
            # Bollinger Bands
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['STD20'] = data['Close'].rolling(window=20).std()
            data['Upper_BB'] = data['MA20'] + (data['STD20'] * 2)
            data['Lower_BB'] = data['MA20'] - (data['STD20'] * 2)

            latest = data.iloc[-1]
            prev = data.iloc[-2]
            
            # Metrics Overview
            m1, m2, m3, m4 = st.columns(4)
            current_price = float(latest['Close'])
            prev_price = float(prev['Close'])
            chg = current_price - prev_price
            pct_chg = (chg / prev_price) * 100
            
            m1.metric("Current Price", f"₹{current_price:,.2f}", f"{chg:+.2f} ({pct_chg:+.2f}%)")
            m2.metric("RSI (14)", f"{float(latest['RSI']):.2f}")
            m3.metric("20 EMA", f"₹{float(latest['EMA_20']):,.2f}")
            m4.metric("50 EMA", f"₹{float(latest['EMA_50']):,.2f}")

            # Candlestick Chart
            fig = gg.Figure()
            
            # Candlesticks
            fig.add_trace(gg.Candlestick(
                x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                name="Price"
            ))
            
            # Overlay EMAs
            fig.add_trace(gg.Scatter(x=data.index, y=data['EMA_20'], line=dict(color='orange', width=1.5), name="EMA 20"))
            fig.add_trace(gg.Scatter(x=data.index, y=data['EMA_50'], line=dict(color='blue', width=1.5), name="EMA 50"))
            
            # Bollinger Bands
            fig.add_trace(gg.Scatter(x=data.index, y=data['Upper_BB'], line=dict(color='gray', dash='dash'), name="Upper BB"))
            fig.add_trace(gg.Scatter(x=data.index, y=data['Lower_BB'], line=dict(color='gray', dash='dash'), name="Lower BB"))

            fig.update_layout(
                title=f"{symbol} Technical Chart",
                yaxis_title="Price (INR)",
                template="plotly_dark",
                height=550,
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Signal Summary
            st.subheader("Signal Breakdown")
            rsi_val = float(latest['RSI'])
            if rsi_val > 70:
                st.warning("⚠️ **RSI Signal:** Overbought status (>70). Potential pullback risk.")
            elif rsi_val < 30:
                st.success("🟢 **RSI Signal:** Oversold status (<30). Potential bounce opportunity.")
            else:
                st.info("ℹ️ **RSI Signal:** Neutral trend range.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Default Dashboard View
elif page == "🏠 Dashboard":
    st.title("📈 NSE PRO")
    st.subheader("Indian Stock Market Analysis")
    st.info("Select 'Stock Analyzer' from the sidebar menu to view charts and indicators.")
