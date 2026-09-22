import streamlit as st

st.set_page_config(page_title="NSE PRO", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
.nse-card { padding:18px; border:1px solid rgba(128,128,128,.25); border-radius:12px; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📈 NSE PRO")
st.sidebar.caption("Stock analysis platform")
page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🔎 Stock Analyzer", "🚀 Swing Screener", "📰 News", "🏦 Institutional Watch"])
st.sidebar.divider()
st.sidebar.caption("Step 1 — Clean base application")

if page == "🏠 Dashboard":
    st.title("📈 NSE PRO")
    st.subheader("Indian Stock Market Analysis")
    st.info("This is the clean starting version of NSE PRO. Market-data modules will be added after the base application is confirmed working.")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("NIFTY 50", "—", "Waiting")
    with c2: st.metric("BANK NIFTY", "—", "Waiting")
    with c3: st.metric("FII", "—", "Waiting")
    with c4: st.metric("DII", "—", "Waiting")
    st.divider()
    st.markdown("### Modules")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="nse-card"><h3>🔎 Stock Analyzer</h3><p>Analyze an individual NSE stock using price, technical and fundamental data.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="nse-card"><h3>🚀 Swing Screener</h3><p>Find stocks matching swing-trading conditions.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="nse-card"><h3>📰 News</h3><p>Track important company and market events.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="nse-card"><h3>🏦 Institutional Watch</h3><p>Track institutional activity and related market information.</p></div>', unsafe_allow_html=True)

elif page == "🔎 Stock Analyzer":
    st.title("🔎 Stock Analyzer")
    symbol = st.text_input("Enter NSE stock symbol", placeholder="Example: TCS, INFY, HDFCBANK, RELIANCE").strip().upper()
    if symbol:
        st.success(f"Selected stock: {symbol}")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Current Price", "—")
        with c2: st.metric("Today's Change", "—")
        with c3: st.metric("Volume", "—")
        st.warning("Live market data is intentionally not connected in Step 1. This keeps the application fast and gives us a stable base.")
    else:
        st.info("Enter an NSE symbol to begin.")

elif page == "🚀 Swing Screener":
    st.title("🚀 Swing Screener")
    st.write("Swing-trading conditions will be added here.")
    st.markdown("### Planned filters")
    for item in ["Price > ₹100", "Near 52-week high", "20 EMA > 50 EMA", "RSI condition", "Volume expansion", "Breakout condition", "Fundamental filters"]:
        st.checkbox(item, value=False, disabled=True)
    st.info("Step 1: screener engine is not connected yet.")

elif page == "📰 News":
    st.title("📰 Stock News")
    st.info("Fresh NSE/company news will be connected in the next step.")
    st.markdown("### Planned event categories")
    for item in ["Block / Bulk Deal", "Order Win", "Results", "Dividend", "Buyback", "M&A / Stake Purchase", "Government / Regulatory", "Brokerage Calls"]:
        st.write(f"• {item}")

elif page == "🏦 Institutional Watch":
    st.title("🏦 Institutional Watch")
    st.info("FII/DII and institutional activity will be connected after the basic application is confirmed working.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### FII")
        st.metric("Net Activity", "—")
    with c2:
        st.markdown("### DII")
        st.metric("Net Activity", "—")

st.divider()
st.caption("NSE PRO • Step 1 • Clean base version")
