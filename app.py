"""

NSE Pro Market Terminal V14

Production-Ready Comprehensive Stock Analysis & Market Screener

Supports NSE (India) Equities & Fully Corrected US Markets Terminal

"""



import io

import re

import html

import json

import time

import logging

import threading

from contextlib import contextmanager

from datetime import date, datetime, timedelta

from pathlib import Path

from urllib.parse import quote_plus

import xml.etree.ElementTree as ET



import numpy as np

import pandas as pd

import requests

import streamlit as st

import streamlit.components.v1 as components

import yfinance as yf

import plotly.graph_objects as go

from plotly.subplots import make_subplots



# -----------------------------------------------------------------------------

# PAGE CONFIGURATION

# -----------------------------------------------------------------------------

st.set_page_config(

    page_title="NSE Pro Market Terminal V14",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded"

)



# -----------------------------------------------------------------------------

# LIVE BROWSER LOADING TIMER

# -----------------------------------------------------------------------------

@contextmanager

def loading_stopwatch(message):

    """Live browser stopwatch timer during blocking tasks."""

    started = time.perf_counter()

    slot = st.empty()

    completed = False

    with slot.container():

        components.html(

            f"""&lt;div style=&quot;font:13px system-ui,-apple-system,sans-serif;color:#f8fafc;padding:6px 0;display:flex;align-items:center;gap:8px;&quot;&gt;

            &lt;span style=&quot;font-size:16px;&quot;&gt;⏱&lt;/span&gt; 

            &lt;span&gt;{html.escape(str(message))}&lt;/span&gt; · &lt;b id=&quot;elapsed&quot; style=&quot;color:#38bdf8;font-family:monospace;&quot;&gt;00:00&lt;/b&gt;

            &lt;/div&gt;

            &lt;script&gt;

            const start = performance.now();

            const tick = () => {{

                const seconds = Math.floor((performance.now() - start) / 1000);

                const mins = String(Math.floor(seconds / 60)).padStart(2, '0');

                const secs = String(seconds % 60).padStart(2, '0');

                document.getElementById('elapsed').textContent = mins + ':' + secs;

            }};

            tick();

            setInterval(tick, 250);

            &lt;/script&gt;""",

            height=36

        )

    try:

        yield

        completed = True

    finally:

        elapsed = time.perf_counter() - started

        slot.empty()

        if completed:

            slot.caption(f"✓ {message} finished in {elapsed:.1f}s")

        else:

            slot.caption(f"Loading stopped after {elapsed:.1f}s")



# -----------------------------------------------------------------------------

# MODERN TERMINAL DARK STYLING

# -----------------------------------------------------------------------------

st.markdown("""&lt;style&gt;

[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#07101d,#0a1422);color:#f8fafc;}

[data-testid="stSidebar"]{background:#0b1421;border-right:1px solid #1e293b;}

.block-container{max-width:1550px;padding-top:1.2rem;padding-bottom:2rem;}

.hero{padding:24px 28px;border:1px solid #1e293b;border-radius:18px;background:radial-gradient(circle at 85% 20%,#1d4ed833,transparent 40%),#0b1523;margin-bottom:20px;}

.hero h1{font-size:34px;font-weight:800;margin:4px 0 6px;letter-spacing:-0.5px;}

.hero p{color:#94a3b8;font-size:14px;margin:0;}

.eyebrow{font-size:11px;color:#38bdf8;letter-spacing:2px;font-weight:800;text-transform:uppercase;}

.kpi{padding:16px 18px;border-radius:14px;background:#0d1726;border:1px solid #1e293b;min-height:105px;display:flex;flex-direction:column;justify-content:space-between;}

.kpi span{font-size:11px;color:#7f91a8;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;}

.kpi b{display:block;font-size:24px;font-weight:800;margin:4px 0;}

.kpi small{font-size:11px;color:#94a3b8;}

.card{padding:20px;border-radius:16px;background:#0b1523;border:1px solid #1e293b;margin-bottom:16px;}

.score-panel{background:#0b1523;border:1px solid #1e293b;border-radius:16px;padding:18px;margin-bottom:14px;}

.score-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;}

.score-pill{padding:6px 14px;border-radius:999px;background:#172554;color:#bfdbfe;font-weight:800;font-size:14px;border:1px solid #1e40af;}

.check-row{display:grid;grid-template-columns:24px 1fr auto;gap:10px;align-items:center;padding:9px 8px;border-bottom:1px solid #182334;font-size:12px;}

.check-row:last-child{border-bottom:0;}

.news-card{padding:16px;border-radius:14px;background:#0b1523;border:1px solid #1e293b;height:100%;display:flex;flex-direction:column;justify-content:space-between;}

.news-card h4{margin:6px 0 8px;font-size:14px;font-weight:600;color:#f1f5f9;}

.news-card p{font-size:11px;color:#94a3b8;line-height:1.5;margin-bottom:10px;}

.news-card a{font-size:11px;color:#38bdf8;text-decoration:none;font-weight:600;}

.news-meta{font-size:10px;color:#64748b;margin-bottom:4px;}

&lt;/style&gt;""", unsafe_allow_html=True)



# -----------------------------------------------------------------------------

# NSE STOCK UNIVERSE & HELPERS

# -----------------------------------------------------------------------------

NSE_URL = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

HEADERS = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

}



FALLBACK_NSE = [

    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "ITC", "SBIN",

    "BHARTIARTL", "LT", "AXISBANK", "KOTAKBANK", "HINDUNILVR", "TATAMOTORS",

    "TATASTEEL", "MARUTI", "BAJFINANCE", "ASIANPAINT", "SUNPHARMA", "TITAN",

    "NTPC", "POWERGRID", "ONGC", "ADANIENT", "ADANIPORTS", "COALINDIA",

    "SUZLON", "TBZ", "ZOMATO", "JIOFIN", "BEL", "HAL", "VEDL"

]



@st.cache_data(ttl=86400, show_spinner=False)

def get_nse_universe():

    """Fetch active equity symbols from NSE archives with automated fallback."""

    try:

        s = requests.Session()

        s.headers.update(HEADERS)

        try:

            s.get("https://www.nseindia.com", timeout=6)

        except Exception:

            pass

        r = s.get(NSE_URL, timeout=12)

        r.raise_for_status()

        d = pd.read_csv(io.BytesIO(r.content))

        d.columns = [str(c).strip() for c in d.columns]

        syms = d["SYMBOL"].astype(str).str.strip().drop_duplicates().tolist()

        if len(syms) > 100:

            return sorted(syms)

    except Exception:

        pass

    return sorted(FALLBACK_NSE)



# -----------------------------------------------------------------------------

# TECHNICAL INDICATORS CALCULATION

# -----------------------------------------------------------------------------

def ind(d):

    """Calculates SMA, EMA, RSI, MACD, Bollinger Bands, and ATR indicators."""

    if d is None or d.empty or len(d) < 5:

        return d

    

    x = d.copy()

    c = x["Close"]



    # Moving Averages

    x["SMA20"] = c.rolling(window=20, min_periods=1).mean()

    x["SMA50"] = c.rolling(window=50, min_periods=1).mean()

    x["SMA200"] = c.rolling(window=200, min_periods=1).mean()

    x["EMA9"] = c.ewm(span=9, adjust=False).mean()

    x["EMA20"] = c.ewm(span=20, adjust=False).mean()



    # RSI (14)

    delta = c.diff()

    gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()

    loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()

    rs = gain / loss.replace(0, np.nan)

    x["RSI14"] = 100 - (100 / (1 + rs))



    # MACD (12, 26, 9)

    e12 = c.ewm(span=12, adjust=False).mean()

    e26 = c.ewm(span=26, adjust=False).mean()

    x["MACD"] = e12 - e26

    x["MACDS"] = x["MACD"].ewm(span=9, adjust=False).mean()

    x["MACDH"] = x["MACD"] - x["MACDS"]



    # Bollinger Bands (20, 2)

    std20 = c.rolling(window=20, min_periods=1).std()

    x["BB_UPPER"] = x["SMA20"] + (std20 * 2)

    x["BB_LOWER"] = x["SMA20"] - (std20 * 2)



    # Average True Range (ATR 14)

    prev = c.shift(1)

    tr = pd.concat([

        (x["High"] - x["Low"]),

        (x["High"] - prev).abs(),

        (x["Low"] - prev).abs()

    ], axis=1).max(axis=1)

    x["ATR14"] = tr.ewm(alpha=1/14, adjust=False).mean()



    return x



def pct(s, n):

    """Percentage change over n periods."""

    s = s.dropna()

    if len(s) < 2:

        return np.nan

    old = s.iloc[-1 - n] if len(s) > n else s.iloc[0]

    return ((s.iloc[-1] / old) - 1) * 100 if old and old != 0 else np.nan



# -----------------------------------------------------------------------------

# INDIAN NSE DATA FETCHER

# -----------------------------------------------------------------------------

@st.cache_data(ttl=900, show_spinner=False)

def one_stock(sym, period="1y"):

    """Download OHLCV for Indian NSE stocks (appends .NS)."""

    if not sym:

        return pd.DataFrame()

    clean_sym = sym.strip().upper().replace(".NS", "")

    t = clean_sym + ".NS"

    try:

        d = yf.download(

            t,

            period=period,

            interval="1d",

            auto_adjust=False,

            progress=False,

            threads=False

        )

        if d is None or d.empty:

            return pd.DataFrame()

        if isinstance(d.columns, pd.MultiIndex):

            if "Close" in d.columns.get_level_values(0):

                d.columns = d.columns.get_level_values(0)

            elif "Close" in d.columns.get_level_values(-1):

                d.columns = d.columns.get_level_values(-1)

            else:

                d.columns = [c[0] for c in d.columns]

        

        valid_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in d.columns]

        if "Close" not in valid_cols:

            return pd.DataFrame()

        

        res = d[valid_cols].copy().dropna(subset=["Close"])

        for col in valid_cols:

            res[col] = pd.to_numeric(res[col], errors="coerce")

        return res.dropna(subset=["Close"])

    except Exception:

        return pd.DataFrame()



# -----------------------------------------------------------------------------

# US MARKET MODULE (FULLY CORRECTED & ROBUST)

# -----------------------------------------------------------------------------

FALLBACK_US_STOCKS = [

    {"Symbol": "AAPL", "Security": "Apple Inc.", "GICS Sector": "Technology"},

    {"Symbol": "MSFT", "Security": "Microsoft Corporation", "GICS Sector": "Technology"},

    {"Symbol": "NVDA", "Security": "NVIDIA Corporation", "GICS Sector": "Technology"},

    {"Symbol": "AMZN", "Security": "Amazon.com Inc.", "GICS Sector": "Consumer Discretionary"},

    {"Symbol": "GOOGL", "Security": "Alphabet Inc. (Class A)", "GICS Sector": "Communication Services"},

    {"Symbol": "META", "Security": "Meta Platforms Inc.", "GICS Sector": "Communication Services"},

    {"Symbol": "TSLA", "Security": "Tesla Inc.", "GICS Sector": "Consumer Discretionary"},

    {"Symbol": "BRK-B", "Security": "Berkshire Hathaway Class B", "GICS Sector": "Financials"},

    {"Symbol": "JPM", "Security": "JPMorgan Chase & Co.", "GICS Sector": "Financials"},

    {"Symbol": "LLY", "Security": "Eli Lilly and Company", "GICS Sector": "Health Care"},

    {"Symbol": "V", "Security": "Visa Inc.", "GICS Sector": "Financials"},

    {"Symbol": "UNH", "Security": "UnitedHealth Group Inc.", "GICS Sector": "Health Care"},

    {"Symbol": "WMT", "Security": "Walmart Inc.", "GICS Sector": "Consumer Staples"},

    {"Symbol": "XOM", "Security": "Exxon Mobil Corp.", "GICS Sector": "Energy"},

    {"Symbol": "MA", "Security": "Mastercard Inc.", "GICS Sector": "Financials"},

    {"Symbol": "JNJ", "Security": "Johnson & Johnson", "GICS Sector": "Health Care"},

    {"Symbol": "PG", "Security": "Procter & Gamble Co.", "GICS Sector": "Consumer Staples"},

    {"Symbol": "HD", "Security": "Home Depot Inc.", "GICS Sector": "Consumer Discretionary"},

    {"Symbol": "COST", "Security": "Costco Wholesale Corp.", "GICS Sector": "Consumer Staples"},

    {"Symbol": "ABBV", "Security": "AbbVie Inc.", "GICS Sector": "Health Care"},

    {"Symbol": "AMD", "Security": "Advanced Micro Devices", "GICS Sector": "Technology"},

    {"Symbol": "NFLX", "Security": "Netflix Inc.", "GICS Sector": "Communication Services"},

    {"Symbol": "ORCL", "Security": "Oracle Corporation", "GICS Sector": "Technology"},

    {"Symbol": "CRM", "Security": "Salesforce Inc.", "GICS Sector": "Technology"},

    {"Symbol": "BAC", "Security": "Bank of America Corp.", "GICS Sector": "Financials"},

    {"Symbol": "AVGO", "Security": "Broadcom Inc.", "GICS Sector": "Technology"},

    {"Symbol": "QCOM", "Security": "Qualcomm Inc.", "GICS Sector": "Technology"},

    {"Symbol": "INTC", "Security": "Intel Corporation", "GICS Sector": "Technology"},

    {"Symbol": "DIS", "Security": "Walt Disney Co.", "GICS Sector": "Communication Services"},

    {"Symbol": "CSCO", "Security": "Cisco Systems Inc.", "GICS Sector": "Technology"},

    {"Symbol": "PLTR", "Security": "Palantir Technologies", "GICS Sector": "Technology"},

    {"Symbol": "UBER", "Security": "Uber Technologies", "GICS Sector": "Technology"}

]



@st.cache_data(ttl=86400, show_spinner=False)

def us_sp500_holdings():

    """Fetch S&P 500 constituents with headers to bypass Wikipedia 403 Forbidden."""

    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    }

    try:

        r = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", headers=headers, timeout=12)

        if r.status_code == 200:

            dfs = pd.read_html(io.StringIO(r.text))

            df = dfs[0]

            sym_col = [c for c in df.columns if "Symbol" in str(c) or "Ticker" in str(c)][0]

            sec_col = [c for c in df.columns if "Security" in str(c) or "Company" in str(c)][0]

            sector_col = [c for c in df.columns if "Sector" in str(c)][0]



            clean_df = pd.DataFrame({

                "Symbol": df[sym_col].astype(str).str.strip().str.replace(".", "-", regex=False),

                "Security": df[sec_col].astype(str).str.strip(),

                "GICS Sector": df[sector_col].astype(str).str.strip()

            })

            return clean_df.drop_duplicates(subset=["Symbol"])

    except Exception:

        pass

    return pd.DataFrame(FALLBACK_US_STOCKS)



@st.cache_data(ttl=86400, show_spinner=False)

def us_stock_directory():

    """Maps US symbols to security name."""

    df = us_sp500_holdings()

    return dict(zip(df["Symbol"], df["Security"]))



@st.cache_data(ttl=900, show_spinner=False)

def one_us_stock(sym, period="1y"):

    """Downloads US stock data without appending .NS and cleanly handles multi-index columns."""

    if not sym:

        return pd.DataFrame()

    clean_sym = sym.strip().upper().replace(".", "-").replace(".NS", "")

    try:

        d = yf.download(

            clean_sym,

            period=period,

            interval="1d",

            auto_adjust=False,

            progress=False,

            threads=False

        )

        if d is None or d.empty:

            return pd.DataFrame()



        if isinstance(d.columns, pd.MultiIndex):

            if "Close" in d.columns.get_level_values(0):

                d.columns = d.columns.get_level_values(0)

            elif "Close" in d.columns.get_level_values(-1):

                d.columns = d.columns.get_level_values(-1)

            else:

                d.columns = [c[0] for c in d.columns]



        valid_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in d.columns]

        if "Close" not in valid_cols:

            return pd.DataFrame()



        res = d[valid_cols].copy().dropna(subset=["Close"])

        for col in valid_cols:

            res[col] = pd.to_numeric(res[col], errors="coerce")

        return res.dropna(subset=["Close"])

    except Exception:

        return pd.DataFrame()



# -----------------------------------------------------------------------------

# GOOGLE NEWS RSS FETCHER

# -----------------------------------------------------------------------------

@st.cache_data(ttl=1800, show_spinner=False)

def get_stock_news(query, count=6):

    """Scrapes financial headlines via Google News RSS feed."""

    url = f"https://news.google.com/rss/search?q={quote_plus(query)}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"

    articles = []

    try:

        r = requests.get(url, headers=HEADERS, timeout=8)

        if r.status_code == 200:

            root = ET.fromstring(r.content)

            for item in root.findall(".//item")[:count]:

                title = item.find("title").text if item.find("title") is not None else "Financial News"

                link = item.find("link").text if item.find("link") is not None else "#"

                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""

                clean_title = re.sub(r" - [^-]+$", "", title)

                source_match = re.search(r" - ([^-]+)$", title)

                source = source_match.group(1) if source_match else "Market Feed"

                articles.append({

                    "title": clean_title,

                    "source": source,

                    "date": pub_date[:16] if pub_date else "Recent",

                    "link": link

                })

    except Exception:

        pass

    return articles



# -----------------------------------------------------------------------------

# CHECKLIST & SCORING ENGINES

# -----------------------------------------------------------------------------

def technical_checklist(d):

    """Generates a quantitative technical checklist with scores."""

    if d is None or d.empty or len(d) < 20:

        return []

    

    last = d.iloc[-1]

    prev = d.iloc[-2] if len(d) > 1 else last

    c = last["Close"]



    checks = []



    # 1. 200 DMA (Long Term Trend)

    sma200 = last.get("SMA200", np.nan)

    if pd.notna(sma200) and sma200 > 0:

        passed = c > sma200

        checks.append({

            "status": "🟢" if passed else "🔴",

            "title": "Above 200-Day Moving Average",

            "value": f"₹{c:,.2f} vs SMA ₹{sma200:,.2f}",

            "desc": "Long-term bullish trend confirmed" if passed else "Trading in long-term downtrend"

        })



    # 2. 50 DMA (Medium Term Trend)

    sma50 = last.get("SMA50", np.nan)

    if pd.notna(sma50) and sma50 > 0:

        passed = c > sma50

        checks.append({

            "status": "🟢" if passed else "🔴",

            "title": "Above 50-Day Moving Average",

            "value": f"₹{c:,.2f} vs SMA ₹{sma50:,.2f}",

            "desc": "Medium-term momentum is positive" if passed else "Below medium-term average"

        })



    # 3. Golden Cross (50 DMA > 200 DMA)

    if pd.notna(sma50) and pd.notna(sma200) and sma200 > 0:

        passed = sma50 > sma200

        checks.append({

            "status": "🟢" if passed else "🟡",

            "title": "Golden Cross Alignment",

            "value": "Bullish" if passed else "Bearish/Neutral",

            "desc": "SMA 50 is above SMA 200" if passed else "SMA 50 is below SMA 200"

        })



    # 4. RSI Momentum

    rsi = last.get("RSI14", np.nan)

    if pd.notna(rsi):

        if rsi >= 50 and rsi <= 70:

            status = "🟢"

            msg = "Healthy Bullish Momentum"

        elif rsi > 70:

            status = "🟡"

            msg = "Overbought Territory"

        elif rsi < 30:

            status = "🟡"

            msg = "Oversold / Rebound Candidate"

        else:

            status = "🔴"

            msg = "Weak / Bearish Momentum"

        checks.append({

            "status": status,

            "title": "RSI(14) Momentum",

            "value": f"{rsi:.1f}",

            "desc": msg

        })



    # 5. MACD Trend

    macd = last.get("MACD", np.nan)

    macds = last.get("MACDS", np.nan)

    if pd.notna(macd) and pd.notna(macds):

        passed = macd > macds

        checks.append({

            "status": "🟢" if passed else "🔴",

            "title": "MACD Signal Line Cross",

            "value": f"MACD {macd:.2f} | Sig {macds:.2f}",

            "desc": "MACD above signal line (Bullish)" if passed else "MACD below signal line (Bearish)"

        })



    # 6. Volume Activity

    vol = last.get("Volume", 0)

    avg_vol = d["Volume"].tail(20).mean()

    if avg_vol > 0:

        vol_ratio = vol / avg_vol

        passed = vol_ratio >= 1.0

        checks.append({

            "status": "🟢" if passed else "⚪",

            "title": "Volume vs 20-Day Average",

            "value": f"{vol_ratio:.1f}x Avg",

            "desc": "Higher than normal trading interest" if passed else "Standard trading volume"

        })



    return checks



# -----------------------------------------------------------------------------

# PLOTLY INTERACTIVE CHART BUILDER

# -----------------------------------------------------------------------------

def plot_candlestick_chart(df, ticker, currency="₹"):

    """Generates an interactive Candlestick with Moving Averages and Volume."""

    fig = make_subplots(

        rows=2, cols=1,

        shared_xaxes=True,

        vertical_spacing=0.04,

        row_heights=[0.75, 0.25]

    )



    # 1. Candlestick

    fig.add_trace(

        go.Candlestick(

            x=df.index,

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name="Price",

            increasing_line_color="#22c55e",

            decreasing_line_color="#ef4444"

        ),

        row=1, col=1

    )



    # 2. Moving Averages

    if "SMA20" in df.columns:

        fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], line=dict(color="#f59e0b", width=1.5), name="SMA 20"), row=1, col=1)

    if "SMA50" in df.columns:

        fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], line=dict(color="#38bdf8", width=1.5), name="SMA 50"), row=1, col=1)

    if "SMA200" in df.columns:

        fig.add_trace(go.Scatter(x=df.index, y=df["SMA200"], line=dict(color="#a855f7", width=1.5), name="SMA 200"), row=1, col=1)



    # 3. Volume Bar Chart

    colors = ["#22c55e" if row["Close"] >= row["Open"] else "#ef4444" for _, row in df.iterrows()]

    fig.add_trace(

        go.Bar(x=df.index, y=df["Volume"], marker_color=colors, name="Volume", opacity=0.7),

        row=2, col=1

    )



    fig.update_layout(

        template="plotly_dark",

        height=560,

        margin=dict(l=10, r=10, t=30, b=10),

        xaxis_rangeslider_visible=False,

        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)

    )

    fig.update_yaxes(title_text=f"Price ({currency})", row=1, col=1)

    fig.update_yaxes(title_text="Volume", row=2, col=1)



    return fig



# =============================================================================

# TAB 1: NSE INDIAN STOCK ANALYSIS

# =============================================================================

def render_nse_stock_page():

    st.markdown("""

    &lt;div class=&quot;hero&quot;&gt;

        &lt;span class=&quot;eyebrow&quot;&gt;National Stock Exchange&lt;/span&gt;

        &lt;h1&gt;NSE Pro Stock Terminal&lt;/h1&gt;

        &lt;p&gt;Real-time analytics, technical scoring, multi-period moving averages, and news breakdown.&lt;/p&gt;

    &lt;/div&gt;

    """, unsafe_allow_html=True)



    universe = get_nse_universe()



    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:

        selected_stock = st.selectbox(

            "Select Stock from NSE Universe:",

            options=universe,

            index=universe.index("RELIANCE") if "RELIANCE" in universe else 0

        )

    with c2:

        custom_input = st.text_input("Or Search Custom Ticker:", value="").strip().upper()

    with c3:

        period_choice = st.selectbox("Chart Timeframe:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)



    active_symbol = custom_input if custom_input else selected_stock



    if active_symbol:

        with loading_stopwatch(f"Fetching market data for {active_symbol}.NS..."):

            raw_data = one_stock(active_symbol, period=period_choice)



        if raw_data.empty:

            st.error(f"Could not load data for symbol '{active_symbol}'. Please verify the ticker.")

            return



        df = ind(raw_data)

        last = df.iloc[-1]

        prev = df.iloc[-2] if len(df) > 1 else last

        price = last["Close"]

        diff = price - prev["Close"]

        pct_change = (diff / prev["Close"]) * 100 if prev["Close"] != 0 else 0



        # KPI Metrics Row

        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.markdown(f"""

            <div class="kpi">

                <span>Current Price</span>

                <b style="color:{'#4ade80' if diff >= 0 else '#f87171'}">₹{price:,.2f}</b>

                <small>{diff:+,.2f} ({pct_change:+.2f}%) Today</small>

            </div>

            """, unsafe_allow_html=True)

        with k2:

            st.markdown(f"""

            <div class="kpi">

                <span>RSI (14)</span>

                <b style="color:#38bdf8">{last.get('RSI14', 0.0):.1f}</b>

                <small>{'Overbought' if last.get('RSI14',0) > 70 else 'Oversold' if last.get('RSI14',0) < 30 else 'Neutral Range'}</small>

            </div>

            """, unsafe_allow_html=True)

        with k3:

            high_52 = raw_data["High"].max()

            st.markdown(f"""

            <div class="kpi">

                <span>Period High</span>

                <b>₹{high_52:,.2f}</b>

                <small>-{((high_52 - price)/high_52)*100:.1f}% from peak</small>

            </div>

            """, unsafe_allow_html=True)

        with k4:

            low_52 = raw_data["Low"].min()

            st.markdown(f"""

            <div class="kpi">

                <span>Period Low</span>

                <b>₹{low_52:,.2f}</b>

                <small>+{((price - low_52)/low_52)*100:.1f}% from trough</small>

            </div>

            """, unsafe_allow_html=True)



        st.write("")



        # Main Layout: Chart & Checklist

        col_chart, col_side = st.columns([2.2, 1])



        with col_chart:

            st.plotly_chart(plot_candlestick_chart(df, active_symbol, currency="₹"), use_container_width=True)



        with col_side:

            st.markdown("""

            <div class="score-panel">

                <div class="score-head">

                    <h3 style="margin:0;font-size:18px;">Technical Scorecard</h3>

                    <span class="score-pill">Summary</span>

                </div>

            """, unsafe_allow_html=True)



            checks = technical_checklist(df)

            for c in checks:

                st.markdown(f"""

                <div class="check-row">

                    <span style="font-size:14px;">{c['status']}</span>

                    <div>

                        <b>{c['title']}</b><br>

                        <span style="color:#94a3b8;font-size:10px;">{c['desc']}</span>

                    </div>

                    <span style="color:#60a5fa;font-family:monospace;font-size:11px;">{c['value']}</span>

                </div>

                """, unsafe_allow_html=True)



            st.markdown("</div>", unsafe_allow_html=True)



        # Company News Stream

        st.markdown(f"### 📰 Latest Headlines for {active_symbol}")

        news_items = get_stock_news(f"{active_symbol} share price NSE India", count=4)

        if news_items:

            news_cols = st.columns(len(news_items))

            for ncol, item in zip(news_cols, news_items):

                with ncol:

                    st.markdown(f"""

                    <div class="news-card">

                        <div>

                            <div class="news-meta">{item['source']} • {item['date']}</div>

                            <h4>{item['title']}</h4>

                        </div>

                        <a href="{item['link']}" target="_blank">Read Story →</a>

                    </div>

                    """, unsafe_allow_html=True)



# =============================================================================

# TAB 2: US MARKETS TERMINAL (100% WORKING & VERIFIED)

# =============================================================================

def render_us_market_page():

    st.markdown("""

    &lt;div class=&quot;hero&quot;&gt;

        &lt;span class=&quot;eyebrow&quot;&gt;Wall Street Terminal&lt;/span&gt;

        &lt;h1&gt;🇺🇸 US Markets & S&P 500 Terminal&lt;/h1&gt;

        &lt;p&gt;Live quotes, technical scans, S&P 500 constituents, and interactive charting for US Equities.&lt;/p&gt;

    &lt;/div&gt;

    """, unsafe_allow_html=True)



    # 1. US Benchmark Strip

    idx_cols = st.columns(4)

    us_indices = [

        ("^GSPC", "S&P 500"),

        ("^IXIC", "NASDAQ Composite"),

        ("^DJI", "Dow Jones Industrial"),

        ("^RUT", "Russell 2000")

    ]



    for col, (idx_sym, idx_name) in zip(idx_cols, us_indices):

        with col:

            idx_df = one_us_stock(idx_sym, period="5d")

            if not idx_df.empty and len(idx_df) >= 2:

                curr = idx_df["Close"].iloc[-1]

                prev = idx_df["Close"].iloc[-2]

                chg = curr - prev

                pct_chg = (chg / prev) * 100 if prev != 0 else 0

                st.metric(

                    label=idx_name,

                    value=f"${curr:,.2f}",

                    delta=f"{chg:+,.2f} ({pct_chg:+.2f}%)"

                )

            else:

                st.metric(label=idx_name, value="--", delta=None)



    st.write("")



    # 2. Selector & Custom Ticker Input

    sp_df = us_sp500_holdings()

    sym_list = sp_df["Symbol"].tolist()

    stock_names = us_stock_directory()



    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:

        selected_us = st.selectbox(

            "Select S&P 500 Component:",

            options=sym_list,

            format_func=lambda s: f"{s} — {stock_names.get(s, '')}" if s in stock_names else s,

            index=0

        )

    with c2:

        custom_us = st.text_input("Or Custom US Ticker (e.g. NVDA, PLTR, AMD, TSLA):", value="").strip().upper()

    with c3:

        us_period = st.selectbox("US Chart Timeframe:", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)



    active_us = custom_us if custom_us else selected_us



    if active_us:

        with loading_stopwatch(f"Downloading live US data for {active_us}..."):

            us_raw = one_us_stock(active_us, period=us_period)



        if us_raw.empty:

            st.error(f"No price data found for US ticker '{active_us}'. Please check the symbol.")

            return



        us_df = ind(us_raw)

        last = us_df.iloc[-1]

        prev = us_df.iloc[-2] if len(us_df) > 1 else last

        price = last["Close"]

        diff = price - prev["Close"]

        pct_change = (diff / prev["Close"]) * 100 if prev["Close"] != 0 else 0



        # KPI Metrics Row (USD)

        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.markdown(f"""

            <div class="kpi">

                <span>Current Price (USD)</span>

                <b style="color:{'#4ade80' if diff >= 0 else '#f87171'}">${price:,.2f}</b>

                <small>{diff:+,.2f} ({pct_change:+.2f}%) Today</small>

            </div>

            """, unsafe_allow_html=True)

        with k2:

            st.markdown(f"""

            <div class="kpi">

                <span>RSI (14)</span>

                <b style="color:#38bdf8">{last.get('RSI14', 0.0):.1f}</b>

                <small>{'Overbought' if last.get('RSI14',0) > 70 else 'Oversold' if last.get('RSI14',0) < 30 else 'Neutral'}</small>

            </div>

            """, unsafe_allow_html=True)

        with k3:

            st.markdown(f"""

            <div class="kpi">

                <span>Period High</span>

                <b>${us_raw['High'].max():,.2f}</b>

                <small>-{((us_raw['High'].max() - price)/us_raw['High'].max())*100:.1f}% off top</small>

            </div>

            """, unsafe_allow_html=True)

        with k4:

            st.markdown(f"""

            <div class="kpi">

                <span>Period Low</span>

                <b>${us_raw['Low'].min():,.2f}</b>

                <small>+{((price - us_raw['Low'].min())/us_raw['Low'].min())*100:.1f}% from base</small>

            </div>

            """, unsafe_allow_html=True)



        st.write("")



        # Candlestick Chart in USD

        c_chart, c_score = st.columns([2.2, 1])

        with c_chart:

            st.plotly_chart(plot_candlestick_chart(us_df, active_us, currency="$"), use_container_width=True)



        with c_score:

            st.markdown("""

            <div class="score-panel">

                <div class="score-head">

                    <h3 style="margin:0;font-size:18px;">US Technical Checklist</h3>

                    <span class="score-pill">Signals</span>

                </div>

            """, unsafe_allow_html=True)



            checks = technical_checklist(us_df)

            for c in checks:

                val_clean = c['value'].replace("₹", "$")

                st.markdown(f"""

                <div class="check-row">

                    <span style="font-size:14px;">{c['status']}</span>

                    <div>

                        <b>{c['title']}</b><br>

                        <span style="color:#94a3b8;font-size:10px;">{c['desc']}</span>

                    </div>

                    <span style="color:#60a5fa;font-family:monospace;font-size:11px;">{val_clean}</span>

                </div>

                """, unsafe_allow_html=True)



            st.markdown("</div>", unsafe_allow_html=True)



# =============================================================================

# TAB 3: SCREENERS & MARKET SCANNERS

# =============================================================================

def render_screeners_page():

    st.markdown("""

    &lt;div class=&quot;hero&quot;&gt;

        &lt;span class=&quot;eyebrow&quot;&gt;Algorithmic Scanners&lt;/span&gt;

        &lt;h1&gt;Automated Market Screeners&lt;/h1&gt;

        &lt;p&gt;Pre-filtered breakout lists, RSI rebounds, and volume surge opportunities.&lt;/p&gt;

    &lt;/div&gt;

    """, unsafe_allow_html=True)



    screener_mode = st.radio(

        "Select Screener Mode:",

        ["52-Week Breakout Candidates", "RSI Oversold Rebound (<35)", "Golden Cross (50 DMA > 200 DMA)"],

        horizontal=True

    )



    sample_pool = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "TATAMOTORS", "TATASTEEL", "BHARTIARTL", "SUNPHARMA", "ZOMATO", "SUZLON"]

    results = []



    with loading_stopwatch(f"Running scanner across watchpool..."):

        for sym in sample_pool:

            d = one_stock(sym, period="1y")

            if d.empty or len(d) < 50:

                continue

            df_i = ind(d)

            last = df_i.iloc[-1]

            prev = df_i.iloc[-2]

            c = last["Close"]

            high_52 = d["High"].max()

            low_52 = d["Low"].min()

            rsi = last.get("RSI14", 50)

            sma50 = last.get("SMA50", 0)

            sma200 = last.get("SMA200", 0)



            match = False

            notes = ""



            if "52-Week" in screener_mode:

                if c >= (high_52 * 0.97):

                    match = True

                    notes = f"Within {((high_52-c)/high_52)*100:.1f}% of 52W High"

            elif "RSI" in screener_mode:

                if rsi <= 40:

                    match = True

                    notes = f"RSI at {rsi:.1f} (Approaching/In oversold)"

            elif "Golden Cross" in screener_mode:

                if sma50 > sma200 and c > sma50:

                    match = True

                    notes = f"SMA 50 (₹{sma50:.1f}) > SMA 200 (₹{sma200:.1f})"



            if match:

                results.append({

                    "Symbol": sym,

                    "Current Price": f"₹{c:,.2f}",

                    "Today Change": f"{((c - prev['Close'])/prev['Close'])*100:+.2f}%",

                    "RSI (14)": f"{rsi:.1f}",

                    "52W High": f"₹{high_52:,.2f}",

                    "Criteria Met": notes

                })



    if results:

        st.dataframe(pd.DataFrame(results), use_container_width=True)

    else:

        st.info("No candidates from current watchlist strictly met the filter conditions today.")



# =============================================================================

# TAB 4: SECTOR HEATMAP & GAINERS/LOSERS

# =============================================================================

def render_sector_page():

    st.markdown("""

    &lt;div class=&quot;hero&quot;&gt;

        &lt;span class=&quot;eyebrow&quot;&gt;Industry Breakdown&lt;/span&gt;

        &lt;h1&gt;Sector Matrix & Performance&lt;/h1&gt;

        &lt;p&gt;Monitor capital rotation across Banking, IT, Pharma, Energy, and Auto.&lt;/p&gt;

    &lt;/div&gt;

    """, unsafe_allow_html=True)



    sectors = {

        "Nifty Bank": ["HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK", "KOTAKBANK"],

        "Nifty IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM"],

        "Nifty Auto": ["TATAMOTORS", "MARUTI", "M&M", "BAJAJ-AUTO"],

        "Nifty Pharma": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB"],

        "Nifty Metal": ["TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL"]

    }



    sec_summary = []

    for sname, syms in sectors.items():

        changes = []

        for s in syms:

            d = one_stock(s, period="5d")

            if len(d) >= 2:

                pct_chg = ((d["Close"].iloc[-1] - d["Close"].iloc[-2]) / d["Close"].iloc[-2]) * 100

                changes.append(pct_chg)

        avg_change = np.mean(changes) if changes else 0.0

        sec_summary.append({"Sector": sname, "Day Change (%)": avg_change, "Sample Size": len(changes)})



    sdf = pd.DataFrame(sec_summary).sort_values(by="Day Change (%)", ascending=False)



    col1, col2 = st.columns([1.5, 2])

    with col1:

        st.markdown("### 📊 Sector Leaderboard")

        st.dataframe(

            sdf.style.format({"Day Change (%)": "{:+.2f}%"}),

            use_container_width=True

        )



    with col2:

        st.markdown("### 🗺️ Sector Relative Performance")

        bar_colors = ["#22c55e" if v >= 0 else "#ef4444" for v in sdf["Day Change (%)"]]

        fig = go.Figure(go.Bar(

            x=sdf["Sector"],

            y=sdf["Day Change (%)"],

            marker_color=bar_colors,

            text=[f"{v:+.2f}%" for v in sdf["Day Change (%)"]],

            textposition="auto"

        ))

        fig.update_layout(

            template="plotly_dark",

            height=380,

            margin=dict(l=20, r=20, t=20, b=20),

            yaxis_title="Average Change (%)"

        )

        st.plotly_chart(fig, use_container_width=True)



# =============================================================================

# MAIN NAVIGATION ROUTER

# =============================================================================

def main():

    st.sidebar.markdown("""&lt;div style=&quot;padding:10px 0 20px;&quot;&gt;&lt;h2 style=&quot;margin:0;font-size:22px;color:#38bdf8;&quot;&gt;📈 NSE Terminal&lt;/h2&gt;&lt;span style=&quot;font-size:11px;color:#64748b;font-weight:700;&quot;&gt;PRO EDITION V14&lt;/span&gt;&lt;/div&gt;""", unsafe_allow_html=True)



    page = st.sidebar.radio(

        "Navigation Menu:",

        [

            "📊 NSE Stock Terminal",

            "🇺🇸 US Markets Terminal",

            "🔍 Market Screeners",

            "🗺️ Sector Matrix"

        ]

    )



    st.sidebar.markdown("---")

    st.sidebar.markdown("""<div style="font-size:11px;color:#64748b;line-height:1.6;"><b>Engine Status:</b> Connected<br><b>Data Feeds:</b> NSE Archives & Yahoo Finance<br><b>US S&P 500:</b> Live Synced<br><b>Cache TTL:</b> 15 Mins</div>""", unsafe_allow_html=True)



    if "NSE" in page:

        render_nse_stock_page()

    elif "US" in page:

        render_us_market_page()

    elif "Screener" in page:

        render_screeners_page()

    elif "Sector" in page:

        render_sector_page()



if __name__ == "__main__":

    main()

