
import io, requests, numpy as np, pandas as pd, streamlit as st, yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="NSE Pro Market Terminal", page_icon="📈", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#07101d,#0a1422);color:#f8fafc}
[data-testid="stSidebar"]{background:#0b1421;border-right:1px solid #1e293b}
.block-container{max-width:1500px;padding-top:1.2rem}
.hero{padding:28px;border:1px solid #1e293b;border-radius:20px;background:radial-gradient(circle at 85% 20%,#1d4ed833,transparent 35%),#0b1523;margin-bottom:16px}
.hero h1{font-size:42px;margin:4px 0}.hero p{color:#94a3b8}.eyebrow{font-size:10px;color:#60a5fa;letter-spacing:2px;font-weight:900}
.kpi{padding:16px;border-radius:14px;background:#0d1726;border:1px solid #1e293b;min-height:110px}.kpi span,.kpi small{display:block}.kpi span{font-size:9px;color:#7f91a8;font-weight:900}.kpi b{display:block;font-size:24px;margin:9px 0}.kpi small{font-size:9px;color:#94a3b8}
.signal{padding:18px;border-radius:15px;background:#0b1523;border:1px solid #1e293b;min-height:260px}.badge{display:inline-block;padding:9px 14px;border-radius:8px;font-weight:900;background:#16a34a;margin:8px 0}.factor{padding:8px 10px;background:#0d1726;border-left:3px solid #334155;border-radius:7px;margin:7px 0;font-size:11px}
.card{padding:16px;border-radius:14px;background:#0b1523;border:1px solid #1e293b}
</style>

<style>
.top-picks-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}
.pick-card{padding:16px;border-radius:15px;background:linear-gradient(145deg,#0b1523,#101c2c);border:1px solid #1e293b;min-height:150px}
.pick-card b,.pick-card span,.pick-card small{display:block}.pick-card b{font-size:19px;margin:7px 0}.pick-card span{color:#94a3b8;font-size:10px}.pick-card small{font-size:10px;margin-top:7px}
.pick-badge{display:inline-block!important;width:max-content;padding:5px 8px;border-radius:999px;background:#14532d;color:#86efac!important;font-weight:900}
.risk-box{padding:10px 12px;border-radius:10px;background:#2a1606;border:1px solid #78350f;color:#fbbf24;font-size:11px;margin:10px 0}
.clean-table-note{font-size:10px;color:#94a3b8;margin:6px 0 10px}
.signal-strong{color:#4ade80}.signal-watch{color:#fbbf24}.signal-avoid{color:#fb7185}
@media(max-width:900px){.top-picks-grid{grid-template-columns:1fr}}
</style>

""", unsafe_allow_html=True)

NSE_URL="https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
HEADERS={"User-Agent":"Mozilla/5.0"}
FALLBACK=["RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","ITC","SBIN","LT","AXISBANK","SUZLON","TBZ"]

@st.cache_data(ttl=86400, show_spinner=False)
def universe():
    try:
        s=requests.Session(); s.headers.update(HEADERS)
        try:s.get("https://www.nseindia.com",timeout=8)
        except:pass
        r=s.get(NSE_URL,timeout=15); r.raise_for_status()
        d=pd.read_csv(io.BytesIO(r.content)); d.columns=[str(c).strip() for c in d.columns]
        return d["SYMBOL"].astype(str).str.strip().drop_duplicates().tolist()
    except:
        return FALLBACK

@st.cache_data(ttl=900, show_spinner=False)
def one_stock(sym, period):
    t=sym+".NS"
    d=yf.download(t,period=period,interval="1d",auto_adjust=False,progress=False,threads=False)
    if isinstance(d.columns,pd.MultiIndex): d.columns=[c[0] for c in d.columns]
    return d[["Open","High","Low","Close","Volume"]].dropna(subset=["Close"])

def ind(d):
    x=d.copy(); c=x.Close
    x["SMA20"]=c.rolling(20).mean();x["SMA50"]=c.rolling(50).mean();x["SMA200"]=c.rolling(200).mean()
    x["EMA9"]=c.ewm(span=9,adjust=False).mean();x["EMA20"]=c.ewm(span=20,adjust=False).mean()
    delta=c.diff();gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False).mean();loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
    rs=gain/loss.replace(0,np.nan);x["RSI14"]=100-100/(1+rs)
    e12=c.ewm(span=12,adjust=False).mean();e26=c.ewm(span=26,adjust=False).mean();x["MACD"]=e12-e26;x["MACDS"]=x.MACD.ewm(span=9,adjust=False).mean()
    prev=c.shift(1);tr=pd.concat([(x.High-x.Low),(x.High-prev).abs(),(x.Low-prev).abs()],axis=1).max(axis=1);x["ATR14"]=tr.ewm(alpha=1/14,adjust=False).mean()
    return x

def pct(s,n):
    s=s.dropna()
    if len(s)<2:return np.nan
    old=s.iloc[-1-n] if len(s)>n else s.iloc[0]
    return (s.iloc[-1]/old-1)*100 if old else np.nan

@st.cache_data(ttl=3600, show_spinner=False)
def bulk_snapshot(symbols_tuple, period="5y"):
    syms=list(symbols_tuple); rows=[]
    for k in range(0,len(syms),70):
        batch=syms[k:k+70]; ticks=[s+".NS" for s in batch]
        try:d=yf.download(ticks,period=period,interval="1d",group_by="column",auto_adjust=False,progress=False,threads=True)
        except:continue
        if d is None or d.empty:continue
        for s,t in zip(batch,ticks):
            try:
                close=d["Close"][t] if isinstance(d.columns,pd.MultiIndex) else d["Close"]
                high=d["High"][t] if isinstance(d.columns,pd.MultiIndex) else d["High"]
                low=d["Low"][t] if isinstance(d.columns,pd.MultiIndex) else d["Low"]
                vol=d["Volume"][t] if isinstance(d.columns,pd.MultiIndex) else d["Volume"]
                close=close.dropna()
                if close.empty:continue
                latest=float(close.iloc[-1]); hi52=float(high.tail(252).max()); lo52=float(low.tail(252).min())
                sma20=float(close.tail(20).mean()) if len(close)>=20 else np.nan
                sma50=float(close.tail(50).mean()) if len(close)>=50 else np.nan
                sma200=float(close.tail(200).mean()) if len(close)>=200 else np.nan
                delta=close.diff();gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False).mean();loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean();rs=gain/loss.replace(0,np.nan)
                rsi=float((100-100/(1+rs)).iloc[-1]) if len(close)>=15 else np.nan
                v=float(vol.dropna().iloc[-1]) if not vol.dropna().empty else 0
                va=float(vol.tail(20).mean()) if len(vol.dropna())>=5 else np.nan
                rows.append({"Symbol":s,"Latest":latest,"1D %":pct(close,1),"1W %":pct(close,5),"1M %":pct(close,21),"3M %":pct(close,63),"6M %":pct(close,126),"1Y %":pct(close,252),"5Y %":pct(close,1260),"RSI14":rsi,"SMA20":sma20,"SMA50":sma50,"SMA200":sma200,"52W High":hi52,"52W Low":lo52,"% of 52W High":latest/hi52*100 if hi52 else np.nan,"Volume":int(v),"Volume Ratio":v/va if va and np.isfinite(va) else np.nan,"Up Days 20":int((close.diff().tail(20)>0).sum())})
            except:continue
    return pd.DataFrame(rows)

SCREENERS={
"52W Breakout Leaders":"Near 52W high + above SMA50",
"RSI Pullback in Uptrend":"RSI 38–45 + above SMA50",
"Golden Cross Trend":"SMA50 > SMA200 + price above SMA50",
"High Volume Breakout":"Volume ratio ≥1.3 + near 52W high",
"Darvas-Style Breakout":"Near 52W high + 1M strength",
"CAN SLIM Technical":"Near highs + positive 1M/1Y + trend",
"Consistent Uptrend":"12+ up days in 20 + positive 1M/3M",
"Oversold Rebound Watch":"RSI ≤40 + price above SMA200"
}


def clean_display(df):
    if df is None or df.empty:
        return df
    x=df.copy()
    pct_cols=[c for c in x.columns if c.endswith("%") or c in ["RSI14","Volume Ratio","% of 52W High"]]
    for c in pct_cols:
        if c in x.columns:
            x[c]=pd.to_numeric(x[c],errors="coerce").round(2)
    for c in ["Latest","SMA20","SMA50","SMA200","52W High","52W Low"]:
        if c in x.columns:
            x[c]=pd.to_numeric(x[c],errors="coerce").round(2)
    return x

def run_screen(df,name):
    x=df.copy()
    if name=="52W Breakout Leaders":x=x[(x["% of 52W High"]>=95)&(x.Latest>x.SMA50)]
    elif name=="RSI Pullback in Uptrend":x=x[x.RSI14.between(38,45)&(x.Latest>x.SMA50)]
    elif name=="Golden Cross Trend":x=x[(x.SMA50>x.SMA200)&(x.Latest>x.SMA50)]
    elif name=="High Volume Breakout":x=x[(x["Volume Ratio"]>=1.3)&(x["% of 52W High"]>=90)]
    elif name=="Darvas-Style Breakout":x=x[(x["% of 52W High"]>=95)&(x["1M %"]>=5)&(x.Latest>x.SMA50)]
    elif name=="CAN SLIM Technical":x=x[(x["% of 52W High"]>=90)&(x["1M %"]>0)&(x["1Y %"]>0)&(x.Latest>x.SMA50)]
    elif name=="Consistent Uptrend":x=x[(x["Up Days 20"]>=12)&(x["1M %"]>0)&(x["3M %"]>0)]
    elif name=="Oversold Rebound Watch":x=x[(x.RSI14<=40)&(x.Latest>x.SMA200)]
    return x

st.sidebar.markdown("## 📈 NSE PRO")
page=st.sidebar.radio("Open module",["🏠 Dashboard","🧠 Pro Analyzer","🚀 Swing Screeners","🌐 All NSE Performance","🏦 Institutional Watch","💾 Market Data Hub"])

if page=="🏠 Dashboard":
    st.markdown('<div class="hero"><div class="eyebrow">NSE MARKET INTELLIGENCE</div><h1>One terminal. Less manual work.</h1><p>Analyze stocks, scan swing setups and stop typing closing prices by hand.</p></div>',unsafe_allow_html=True)
    c=st.columns(4)
    vals=[("PRO ANALYZER","Internet OHLCV","Single stock"),("SWING LIBRARY",str(len(SCREENERS))+" presets","Rule-based"),("PERFORMANCE","1D → 5Y","All NSE"),("MANUAL FEEDING","0","Refresh + export")]
    for col,v in zip(c,vals):
        with col:st.markdown(f'<div class="kpi"><span>{v[0]}</span><b>{v[1]}</b><small>{v[2]}</small></div>',unsafe_allow_html=True)

elif page=="🧠 Pro Analyzer":
    syms=universe();sym=st.selectbox("NSE symbol",syms,index=syms.index("TBZ") if "TBZ" in syms else 0);period=st.select_slider("Period",["3mo","6mo","1y","2y","5y"],value="1y")
    if st.button("⚡ Analyze",type="primary"):
        with st.spinner("Fetching market data..."):d=one_stock(sym,period)
        if d.empty:st.error("No data returned. Try again.")
        else:
            x=ind(d);latest=float(x.Close.iloc[-1]);prev=float(x.Close.iloc[-2]);rsi=float(x.RSI14.iloc[-1]);year=x.tail(252);hi=float(year.High.max());lo=float(year.Low.min())
            score=0;factors=[];warnings=[]
            if pd.notna(x.SMA50.iloc[-1]) and latest>x.SMA50.iloc[-1]:
                score+=2;factors.append("✅ Price above SMA50")
            else:
                score-=1;warnings.append("⚠️ Price is below SMA50")
            if pd.notna(x.SMA200.iloc[-1]) and pd.notna(x.SMA50.iloc[-1]) and x.SMA50.iloc[-1]>x.SMA200.iloc[-1]:
                score+=2;factors.append("✅ SMA50 above SMA200")
            elif pd.notna(x.SMA200.iloc[-1]):
                score-=1;warnings.append("⚠️ SMA50 is not above SMA200")
            if latest>x.EMA9.iloc[-1]:
                score+=1;factors.append("✅ Price above EMA9")
            else:
                score-=1;warnings.append("⚠️ Price below EMA9")
            if x.MACD.iloc[-1]>x.MACDS.iloc[-1]:
                score+=1;factors.append("✅ MACD bullish")
            else:
                score-=1;warnings.append("⚠️ MACD not confirmed")
            if np.isfinite(rsi):
                if 55<=rsi<=70:
                    score+=1;factors.append(f"✅ RSI {rsi:.1f} supports momentum")
                elif rsi>80:
                    score-=2;warnings.append(f"⚠️ RSI {rsi:.1f} is extremely overbought — chase risk is high")
                elif rsi>70:
                    score-=1;warnings.append(f"⚠️ RSI {rsi:.1f} is overbought")
                elif rsi<40:
                    score-=1;warnings.append(f"⚠️ RSI {rsi:.1f} is weak")
            if latest/hi*100>=98:
                warnings.append("⚠️ Price is very close to the 52W high; breakout confirmation matters.")
            label="STRONG BUY" if score>=6 else "BUY" if score>=3 else "WATCH" if score>=0 else "AVOID"
            cs=st.columns(4)
            for col,v in zip(cs,[("LATEST",f"₹{latest:,.2f}",f"{(latest/prev-1)*100:+.2f}%"),("52W RANGE",f"₹{lo:,.0f}–₹{hi:,.0f}",f"{latest/hi*100:.1f}% of high"),("RSI14",f"{rsi:.1f}","Momentum"),("CONSENSUS",label,f"Score +{score}")]):
                with col:st.markdown(f'<div class="kpi"><span>{v[0]}</span><b>{v[1]}</b><small>{v[2]}</small></div>',unsafe_allow_html=True)
            fig=go.Figure(go.Candlestick(x=x.index,open=x.Open,high=x.High,low=x.Low,close=x.Close,name=sym))
            for col,color in [("SMA20","#f59e0b"),("SMA50","#a78bfa"),("SMA200","#38bdf8"),("EMA9","#22c55e")]:fig.add_trace(go.Scatter(x=x.index,y=x[col],name=col,line=dict(color=color,width=1.4)))
            fig.update_layout(height=620,template="plotly_dark",xaxis_rangeslider_visible=False)
            st.plotly_chart(fig,use_container_width=True)
            if warnings:
                st.markdown('<div class="risk-box"><b>Risk checks:</b><br>'+ "<br>".join(warnings) +'</div>', unsafe_allow_html=True)

            a,b=st.columns(2)
            with a:
                st.markdown("### 🎯 Medium-Term Investment")
                st.markdown(f'<div class="badge">{label}</div>',unsafe_allow_html=True)
                [st.markdown(f'<div class="factor">{f}</div>',unsafe_allow_html=True) for f in factors]
                [st.markdown(f'<div class="factor">{w}</div>',unsafe_allow_html=True) for w in warnings[:3]]
            with b:
                st.markdown("### ⚡ Short-Term Swing")
                swing_factors=(factors[-3:] if len(factors)>=3 else factors)
                [st.markdown(f'<div class="factor">{f}</div>',unsafe_allow_html=True) for f in swing_factors]
                [st.markdown(f'<div class="factor">{w}</div>',unsafe_allow_html=True) for w in warnings[:2]]
            atr=float(x.ATR14.iloc[-1]);stop=latest-1.5*atr;risk=latest-stop;t1=latest+1.5*risk;t2=latest+3*risk
            st.markdown("### 🛡️ Trade Execution & Risk")
            cs=st.columns(5)
            for col,v in zip(cs,[("ENTRY",latest),("STOP LOSS",stop),("TARGET 1",t1),("TARGET 2",t2),("R:R","1 : 3.0")]):
                with col:st.markdown(f'<div class="kpi"><span>{v[0]}</span><b>{("₹"+format(v[1],",.2f")) if isinstance(v[1],float) else v[1]}</b></div>',unsafe_allow_html=True)

elif page=="🚀 Swing Screeners":
    st.markdown("## 🚀 Famous Swing-Trading Screener Library")
    st.caption("Rule-based candidates only. The app now penalizes extreme overbought conditions instead of blindly rewarding momentum.")

    if st.button("🏆 Build Top Swing Picks Today", type="primary", key="top_picks"):
        syms=universe()[:500]
        with st.spinner("Scanning 500 liquid-listed symbols for technical setups..."):
            snap=bulk_snapshot(tuple(syms),"1y")
        if snap is not None and not snap.empty:
            z=snap.copy()
            z["Score"]=0
            z.loc[(z["% of 52W High"]>=95),"Score"]+=2
            z.loc[(z["Latest"]>z["SMA50"]),"Score"]+=2
            z.loc[(z["SMA50"]>z["SMA200"]),"Score"]+=2
            z.loc[(z["1W %"]>0),"Score"]+=1
            z.loc[(z["1M %"]>0),"Score"]+=1
            z.loc[(z["Volume Ratio"]>=1.3),"Score"]+=1
            z.loc[(z["RSI14"]>80),"Score"]-=3
            z.loc[(z["RSI14"]>70)&(z["RSI14"]<=80),"Score"]-=1
            z=z.sort_values(["Score","1M %"],ascending=False).head(9)
            st.session_state["top_picks_today"]=z

    top=st.session_state.get("top_picks_today")
    if isinstance(top,pd.DataFrame) and not top.empty:
        st.markdown("### 🏆 Top Swing Picks Today")
        st.markdown('<div class="clean-table-note">Scored from trend, breakout, recent returns, volume and RSI risk filters.</div>',unsafe_allow_html=True)
        cols=st.columns(3)
        for i,(_,r) in enumerate(top.iterrows()):
            with cols[i%3]:
                risk="High overbought risk" if r["RSI14"]>80 else "Overbought watch" if r["RSI14"]>70 else "Normal"
                st.markdown(
                    f'<div class="pick-card"><span class="pick-badge">Score {int(r["Score"])}</span><b>{r["Symbol"]}</b><span>₹{r["Latest"]:.2f}</span><small>1W {r["1W %"]:+.2f}% · 1M {r["1M %"]:+.2f}% · RSI {r["RSI14"]:.1f}</small><small>{risk}</small></div>',
                    unsafe_allow_html=True
                )

    name=st.selectbox("Preset",list(SCREENERS));st.info(SCREENERS[name]);size=st.selectbox("Universe size",[100,250,500,1000,"All"],index=1)
    if st.button("🔥 Run Screener",type="primary"):
        syms=universe();syms=syms if size=="All" else syms[:int(size)]
        with st.spinner("Downloading market history in batches..."):snap=bulk_snapshot(tuple(syms),"1y");res=run_screen(snap,name)
        res=clean_display(res);st.dataframe(res,use_container_width=True,height=600,hide_index=True);st.download_button("⬇️ Download CSV",res.to_csv(index=False).encode(),name.replace(" ","_")+".csv","text/csv")

elif page=="🌐 All NSE Performance":
    st.markdown("## 🌐 All NSE Performance & Closing-Price Hub");syms=universe();st.success(f"Universe loaded: {len(syms):,} symbols")
    c1,c2,c3=st.columns(3)
    with c1:size=st.selectbox("Stocks",[100,250,500,1000,"All"],index=1)
    with c2:period=st.selectbox("History",["1y","2y","5y"],index=2)
    with c3:sort=st.selectbox("Rank by",["1D %","1W %","1M %","3M %","6M %","1Y %","5Y %"],index=2)
    if st.button("⚡ Build / Refresh Table",type="primary"):
        use=syms if size=="All" else syms[:int(size)]
        with st.spinner(f"Fetching {period} history for {len(use)} stocks..."):p=bulk_snapshot(tuple(use),period)
        st.session_state.perf=p
    p=st.session_state.get("perf")
    if isinstance(p,pd.DataFrame) and not p.empty:
        p=p.sort_values(sort,ascending=False,na_position="last");p=clean_display(p);st.dataframe(p,use_container_width=True,height=650,hide_index=True);st.download_button("⬇️ Download Performance CSV",p.to_csv(index=False).encode(),"nse_performance.csv","text/csv")

elif page=="🏦 Institutional Watch":
    st.markdown("## 🏦 Institutional / FII-DII Watch")
    st.warning("Price/volume cannot prove FII/DII buying. This page separates verified ownership/deal evidence from technical participation.")

    t1,t2,t3=st.tabs(["📈 Quarterly Holding Change","💼 Bulk / Block Deals","📊 Institutional-Style Momentum"])
    with t1:
        st.markdown("### Upload shareholding history")
        st.caption("Expected columns can include: Symbol, FII Current %, FII Previous %, DII Current %, DII Previous %.")
        up=st.file_uploader("Upload FII/DII holding CSV",type=["csv"],key="fii_holdings")
        if up:
            d=pd.read_csv(up)
            for a,b,n in [("FII Current %","FII Previous %","FII Change"),("DII Current %","DII Previous %","DII Change")]:
                if a in d.columns and b in d.columns:
                    d[n]=pd.to_numeric(d[a],errors="coerce")-pd.to_numeric(d[b],errors="coerce")
            sort_cols=[c for c in ["FII Change","DII Change"] if c in d.columns]
            if sort_cols:
                d=d.sort_values(sort_cols,ascending=False)
            st.dataframe(clean_display(d),use_container_width=True,height=560)
    with t2:
        st.markdown("### Verified disclosed deals layer")
        st.info("This V2 keeps the UI ready for real NSE bulk/block deal ingestion. Do not treat unusual volume as a disclosed institutional deal.")
        st.write("Next reliable integration: scheduled ingestion of NSE bulk/block deal files or broker/API disclosure feed.")
    with t3:
        st.markdown("### Participation proxy")
        st.caption("This is a technical proxy only — not FII/DII ownership evidence.")
        if st.button("Run High Volume Breakout Proxy",key="inst_proxy"):
            syms=universe()[:500]
            with st.spinner("Scanning price + volume participation..."):
                snap=bulk_snapshot(tuple(syms),"1y")
                res=run_screen(snap,"High Volume Breakout")
            st.dataframe(clean_display(res),use_container_width=True,height=560,hide_index=True)

else:
    st.markdown("## 💾 Market Data Hub")
    st.markdown("### ✅ Yes — you can stop manually typing closing prices.")
    st.write("Use the All NSE Performance module to calculate 1D, 1W, 1M, 3M, 6M, 1Y and 5Y returns and export them to CSV.")
    st.write("For speed: single-stock analysis is quick; the first full-universe 5-year refresh is a large job and can take longer. Cache makes repeated use faster.")
