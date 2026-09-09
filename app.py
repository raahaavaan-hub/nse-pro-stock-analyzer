
import io, re, html, requests, numpy as np, pandas as pd, streamlit as st, yfinance as yf
import plotly.graph_objects as go
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

st.set_page_config(page_title="NSE Pro Market Terminal V7", page_icon="📈", layout="wide")

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
.score-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:16px 0}
.score-panel{background:#0b1523;border:1px solid #1e293b;border-radius:16px;padding:18px}
.score-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}
.score-head h3{margin:0;font-size:21px}.score-pill{min-width:88px;text-align:center;padding:8px 12px;border-radius:999px;background:#172554;color:#bfdbfe;font-weight:900;font-size:16px}
.check-row{display:grid;grid-template-columns:24px 1fr auto;gap:8px;align-items:center;padding:9px 8px;border-bottom:1px solid #182334;font-size:11px}
.check-row:last-child{border-bottom:0}.check-row .status{font-size:16px}.check-row .value{color:#94a3b8;font-size:10px;text-align:right}
.rating-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:14px 0}
.rating-card{background:linear-gradient(145deg,#0b1523,#101c2c);border:1px solid #1e293b;border-radius:15px;padding:17px;min-height:150px}
.rating-card span,.rating-card small{display:block}.rating-card span{font-size:9px;color:#94a3b8;font-weight:900;letter-spacing:.5px}
.rating-card b{display:inline-block;margin:11px 0 8px;padding:7px 12px;border-radius:8px;font-size:19px}.rating-card small{font-size:10px;color:#94a3b8;line-height:1.45}
.rating-buy{background:#14532d;color:#86efac}.rating-hold{background:#78350f;color:#fde68a}.rating-no{background:#7f1d1d;color:#fecaca}
.overall-score-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}
.overall-score-box{padding:13px;border-radius:12px;background:#0d1726;border:1px solid #1e293b;text-align:center}
.overall-score-box span{display:block;font-size:9px;color:#94a3b8}.overall-score-box b{display:block;font-size:23px;margin-top:5px}
@media(max-width:900px){.score-grid{grid-template-columns:1fr}.rating-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.rating-grid,.overall-score-strip{grid-template-columns:1fr}}
</style>

<style>
.news-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:12px}
.news-card{padding:15px;border-radius:14px;background:#0b1523;border:1px solid #1e293b}
.news-card h4{margin:6px 0 8px;font-size:15px}.news-card p{font-size:10px;color:#9fb0c4;line-height:1.5}
.news-card a{font-size:10px;color:#60a5fa;text-decoration:none}.news-meta{font-size:9px;color:#64748b;margin-bottom:5px}
.news-tag{display:inline-block;padding:4px 7px;border-radius:999px;background:#172554;color:#bfdbfe;font-size:8px;font-weight:900}
@media(max-width:900px){.news-grid{grid-template-columns:1fr}}
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


@st.cache_data(ttl=600, show_spinner=False)
def google_news_rss(query, limit=25):
    url="https://news.google.com/rss/search?q="+quote_plus(query)+"&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        r=requests.get(url,headers=HEADERS,timeout=12)
        r.raise_for_status()
        root=ET.fromstring(r.content)
        rows=[]
        for item in root.findall(".//item")[:limit]:
            title=html.unescape(item.findtext("title") or "")
            link=item.findtext("link") or ""
            pub=item.findtext("pubDate") or ""
            src=item.find("source")
            source=src.text if src is not None and src.text else ""
            desc=html.unescape(item.findtext("description") or "")
            desc=re.sub("<[^>]+>"," ",desc)
            desc=re.sub(r"\s+"," ",desc).strip()
            rows.append({"title":title,"link":link,"published":pub,"source":source,"description":desc})
        return rows
    except Exception:
        return []

def classify_news(title):
    t=title.lower()
    if "buyback" in t or "buy back" in t: return "Buyback"
    if any(k in t for k in ["q1","q2","q3","q4","quarter","results","profit","revenue","earnings"]): return "Results"
    if any(k in t for k in ["order","contract","wins","deal"]): return "Order/Deal"
    if any(k in t for k in ["falls","drops","slumps","weak","loss","decline"]): return "Negative Move"
    if any(k in t for k in ["rises","jumps","surges","gains","record high"]): return "Positive Move"
    if any(k in t for k in ["dividend","bonus","split"]): return "Corporate Action"
    return "Market News"

def target_from_text(text):
    pats=[
        r"(?:target(?: price)?|price target|pt)\s*(?:of|at|to|:|-)?\s*(?:rs\.?|₹)?\s*([0-9][0-9,]*(?:\.[0-9]+)?)",
        r"(?:rs\.?|₹)\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:target|price target)"
    ]
    for p in pats:
        m=re.search(p,text,re.I)
        if m:
            try:return float(m.group(1).replace(",",""))
            except:return None
    return None

def symbol_from_headline(text, symbols):
    up=" "+re.sub(r"[^A-Z0-9&-]"," ",text.upper())+" "
    for s in symbols:
        if f" {s} " in up:
            return s
    aliases={
        "RELIANCE INDUSTRIES":"RELIANCE","TATA CONSULTANCY SERVICES":"TCS",
        "HDFC BANK":"HDFCBANK","ICICI BANK":"ICICIBANK","STATE BANK OF INDIA":"SBIN",
        "BHARTI AIRTEL":"BHARTIARTL","LARSEN TOUBRO":"LT","LARSEN & TOUBRO":"LT"
    }
    for name,s in aliases.items():
        if name in text.upper(): return s
    return None

@st.cache_data(ttl=900, show_spinner=False)
def current_and_call_price(symbol, call_date_text):
    try:
        d=yf.download(symbol+".NS",period="1y",interval="1d",auto_adjust=False,progress=False,threads=False)
        if isinstance(d.columns,pd.MultiIndex): d.columns=[c[0] for c in d.columns]
        if d.empty:return None,None
        cur=float(d["Close"].dropna().iloc[-1])
        call=None
        try:
            dt=pd.to_datetime(call_date_text,utc=True).tz_convert(None)
            hist=d[d.index>=dt]
            if not hist.empty: call=float(hist["Close"].dropna().iloc[0])
        except: pass
        return cur,call
    except:
        return None,None

def broker_calls_from_news(broker, symbols, limit=20):
    q=f'"{broker}" (buy OR target OR overweight OR upgrade) stock India'
    news=google_news_rss(q,limit)
    rows=[]
    for n in news:
        txt=n["title"]+" "+n["description"]
        sym=symbol_from_headline(txt,symbols)
        tgt=target_from_text(txt)
        if not sym and not tgt: continue
        cur,call=(None,None)
        if sym: cur,call=current_and_call_price(sym,n["published"])
        status="Open"
        if cur and tgt: status="Target Hit" if cur>=tgt else "Below Target"
        ret=((cur/call)-1)*100 if cur and call else None
        rows.append({"Broker":broker,"Symbol":sym or "—","Headline":n["title"],"Published":n["published"],
                     "Target":tgt,"Call Price":call,"Current":cur,"Return Since Call %":ret,
                     "Status":status,"Source":n["source"],"Link":n["link"]})
    return rows


@st.cache_data(ttl=21600, show_spinner=False)
def fundamentals_for_stock(sym):
    try:
        info=yf.Ticker(sym+".NS").info or {}
        keys=["revenueGrowth","earningsGrowth","returnOnEquity","operatingMargins","debtToEquity","currentRatio","freeCashflow","operatingCashflow","trailingPE","profitMargins","marketCap","longName","sector","industry","longBusinessSummary","website","city","country","companyOfficers","heldPercentInstitutions","heldPercentInsiders"]
        return {k:info.get(k) for k in keys}
    except Exception:
        return {}

@st.cache_data(ttl=300, show_spinner=False)
def intraday_stock(sym):
    try:
        d=yf.download(sym+".NS",period="5d",interval="15m",auto_adjust=False,progress=False,threads=False)
        if isinstance(d.columns,pd.MultiIndex): d.columns=[c[0] for c in d.columns]
        if d is None or d.empty:return pd.DataFrame()
        return d[["Open","High","Low","Close","Volume"]].dropna(subset=["Close"])
    except Exception:
        return pd.DataFrame()

def _pct_display(v):
    try:
        if v is None or not np.isfinite(float(v)): return "N/A"
        return f"{float(v)*100:.1f}%"
    except Exception:return "N/A"

def _num_display(v):
    try:
        if v is None or not np.isfinite(float(v)): return "N/A"
        return f"{float(v):,.2f}"
    except Exception:return "N/A"

def fundamental_checklist(info):
    checks=[]
    def add(name,val,passed,display,neutral=False):
        checks.append({"name":name,"value":display,"passed":passed,"neutral":neutral})
    rg=info.get("revenueGrowth"); add("Revenue growth > 10%",rg,rg is not None and rg>0.10,_pct_display(rg),rg is None)
    eg=info.get("earningsGrowth"); add("Earnings growth > 10%",eg,eg is not None and eg>0.10,_pct_display(eg),eg is None)
    roe=info.get("returnOnEquity"); add("ROE >= 15%",roe,roe is not None and roe>=0.15,_pct_display(roe),roe is None)
    om=info.get("operatingMargins"); add("Operating margin >= 10%",om,om is not None and om>=0.10,_pct_display(om),om is None)
    de=info.get("debtToEquity"); add("Debt / Equity <= 100",de,de is not None and de<=100,_num_display(de),de is None)
    cr=info.get("currentRatio"); add("Current ratio >= 1.2",cr,cr is not None and cr>=1.2,_num_display(cr),cr is None)
    fcf=info.get("freeCashflow"); add("Free cash flow positive",fcf,fcf is not None and fcf>0,"Positive" if fcf is not None and fcf>0 else ("Negative" if fcf is not None else "N/A"),fcf is None)
    ocf=info.get("operatingCashflow"); add("Operating cash flow positive",ocf,ocf is not None and ocf>0,"Positive" if ocf is not None and ocf>0 else ("Negative" if ocf is not None else "N/A"),ocf is None)
    pe=info.get("trailingPE"); add("P/E between 0 and 40",pe,pe is not None and pe>0 and pe<=40,_num_display(pe),pe is None)
    pm=info.get("profitMargins"); add("Profit margin >= 8%",pm,pm is not None and pm>=0.08,_pct_display(pm),pm is None)
    score=sum(1 if c["passed"] else (0.5 if c["neutral"] else 0) for c in checks)
    return checks,round(score,1)

def technical_checklist(x):
    last=x.iloc[-1]; close=float(last["Close"]); w=pct(x["Close"],5); m=pct(x["Close"],21)
    avg_vol=float(x["Volume"].tail(20).mean()) if len(x)>=5 else np.nan; vol=float(x["Volume"].iloc[-1]); up20=int((x["Close"].diff().tail(20)>0).sum())
    checks=[]
    def add(name,passed,display,neutral=False):checks.append({"name":name,"value":display,"passed":bool(passed) if not neutral else False,"neutral":neutral})
    sma20=last["SMA20"]; sma50=last["SMA50"]; sma200=last["SMA200"]; ema9=last["EMA9"]; ema20=last["EMA20"]; rsi=last["RSI14"]
    add("Price > SMA20",pd.notna(sma20) and close>sma20,f"Rs {sma20:.2f}" if pd.notna(sma20) else "N/A",pd.isna(sma20))
    add("Price > SMA50",pd.notna(sma50) and close>sma50,f"Rs {sma50:.2f}" if pd.notna(sma50) else "N/A",pd.isna(sma50))
    add("SMA50 > SMA200",pd.notna(sma50) and pd.notna(sma200) and sma50>sma200,f"{sma50:.1f} > {sma200:.1f}" if pd.notna(sma50) and pd.notna(sma200) else "N/A",pd.isna(sma50) or pd.isna(sma200))
    add("EMA9 > EMA20",pd.notna(ema9) and pd.notna(ema20) and ema9>ema20,f"{ema9:.1f} > {ema20:.1f}" if pd.notna(ema9) and pd.notna(ema20) else "N/A",pd.isna(ema9) or pd.isna(ema20))
    add("MACD bullish",pd.notna(last["MACD"]) and pd.notna(last["MACDS"]) and last["MACD"]>last["MACDS"],f"{last['MACD']:.2f} / {last['MACDS']:.2f}")
    add("RSI healthy: 50-70",pd.notna(rsi) and 50<=rsi<=70,f"{rsi:.1f}" if pd.notna(rsi) else "N/A",pd.isna(rsi))
    add("1-week return positive",np.isfinite(w) and w>0,f"{w:+.2f}%" if np.isfinite(w) else "N/A",not np.isfinite(w))
    add("1-month return positive",np.isfinite(m) and m>0,f"{m:+.2f}%" if np.isfinite(m) else "N/A",not np.isfinite(m))
    add("Volume > 20-day average",np.isfinite(avg_vol) and avg_vol>0 and vol>avg_vol,f"{vol/avg_vol:.2f}x avg" if np.isfinite(avg_vol) and avg_vol>0 else "N/A",not np.isfinite(avg_vol))
    add("11+ up days in last 20",up20>=11,f"{up20}/20 up days")
    score=sum(1 if c["passed"] else (0.5 if c["neutral"] else 0) for c in checks)
    return checks,round(score,1)

def render_checklist(title,checks,score):
    st.markdown(f'<div class="score-panel"><div class="score-head"><h3>{title}</h3><div class="score-pill">{score:.1f}/10</div></div>',unsafe_allow_html=True)
    for c in checks:
        icon="✅" if c["passed"] else ("⚪" if c["neutral"] else "❌")
        st.markdown('<div class="check-row">'+f'<span class="status">{icon}</span>'+f'<span>{html.escape(c["name"])}</span>'+f'<span class="value">{html.escape(str(c["value"]))}</span>'+'</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def _rating(score,buy_at,hold_at):
    if score>=buy_at:return "BUY","rating-buy"
    if score>=hold_at:return "HOLD","rating-hold"
    return "NO","rating-no"

def horizon_ratings(x,fundamental_score,intraday_df):
    last=x.iloc[-1]; close=float(last["Close"]); rsi=float(last["RSI14"]) if pd.notna(last["RSI14"]) else np.nan
    w=pct(x["Close"],5); m=pct(x["Close"],21); six=pct(x["Close"],126); yr=pct(x["Close"],252)
    intra_score=0; intra_notes=[]
    if intraday_df is not None and not intraday_df.empty and len(intraday_df)>=10:
        z=intraday_df.copy(); z["EMA9"]=z["Close"].ewm(span=9,adjust=False).mean(); z["EMA20"]=z["Close"].ewm(span=20,adjust=False).mean()
        dd=z["Close"].diff(); gg=dd.clip(lower=0).ewm(alpha=1/14,adjust=False).mean(); ll=(-dd.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean(); z["RSI"]=100-100/(1+gg/ll.replace(0,np.nan)); li=z.iloc[-1]
        if li["Close"]>li["EMA9"]: intra_score+=1; intra_notes.append("Price > 15m EMA9")
        if li["EMA9"]>li["EMA20"]: intra_score+=1; intra_notes.append("EMA9 > EMA20")
        if pd.notna(li["RSI"]) and 50<=li["RSI"]<=70: intra_score+=1; intra_notes.append(f"15m RSI {li['RSI']:.1f}")
        if z["Close"].iloc[-1]>z["Close"].iloc[-2]: intra_score+=1; intra_notes.append("Latest 15m candle positive")
        if len(z)>=20 and z["Volume"].iloc[-1]>z["Volume"].tail(20).mean(): intra_score+=1; intra_notes.append("Volume confirmation")
        il,ic=_rating(intra_score,4,2)
    else: il,ic="HOLD","rating-hold"; intra_notes=["Intraday feed unavailable"]
    ws=0; wn=[]
    if np.isfinite(w) and w>0:ws+=1;wn.append(f"1W {w:+.1f}%")
    if close>last["EMA9"]:ws+=1;wn.append("Price > EMA9")
    if last["MACD"]>last["MACDS"]:ws+=1;wn.append("MACD bullish")
    if np.isfinite(rsi) and 50<=rsi<=70:ws+=1;wn.append(f"RSI {rsi:.1f}")
    if np.isfinite(rsi) and rsi>80:ws-=2;wn.append("Extremely overbought")
    wl,wc=_rating(ws,3,1)
    ms=0; mn=[]
    if np.isfinite(m) and m>0:ms+=1;mn.append(f"1M {m:+.1f}%")
    if pd.notna(last["SMA20"]) and close>last["SMA20"]:ms+=1;mn.append("Price > SMA20")
    if pd.notna(last["SMA50"]) and close>last["SMA50"]:ms+=1;mn.append("Price > SMA50")
    if last["MACD"]>last["MACDS"]:ms+=1;mn.append("MACD bullish")
    if np.isfinite(rsi) and rsi>80:ms-=1;mn.append("Overbought risk")
    ml,mc=_rating(ms,3,1)
    ls=0; ln=[]
    if pd.notna(last["SMA200"]) and close>last["SMA200"]:ls+=1;ln.append("Price > SMA200")
    if pd.notna(last["SMA50"]) and pd.notna(last["SMA200"]) and last["SMA50"]>last["SMA200"]:ls+=1;ln.append("SMA50 > SMA200")
    if np.isfinite(six) and six>0:ls+=1;ln.append(f"6M {six:+.1f}%")
    if np.isfinite(yr) and yr>0:ls+=1;ln.append(f"1Y {yr:+.1f}%")
    if fundamental_score>=6.5:ls+=2;ln.append(f"Fundamental {fundamental_score:.1f}/10")
    elif fundamental_score>=5:ls+=1;ln.append(f"Fundamental {fundamental_score:.1f}/10")
    ll,lc=_rating(ls,4,2)
    return [("INTRADAY",il,ic,intra_notes),("1 WEEK",wl,wc,wn),("1 MONTH",ml,mc,mn),("LONG TERM",ll,lc,ln)]


st.markdown("""
<style>
/* V5 PRESENTATION UPGRADE */
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(circle at 82% 8%,rgba(37,99,235,.18),transparent 30%),
    radial-gradient(circle at 18% 82%,rgba(14,165,233,.10),transparent 30%),
    linear-gradient(180deg,#07111f 0%,#081522 50%,#07101b 100%)!important;
}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#07101c,#0b1827)!important;
  border-right:1px solid #23405f!important;
}
[data-testid="stSidebar"] h2{color:#f8fafc!important;font-weight:900!important;letter-spacing:.7px}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{color:#dbeafe!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:8px 10px!important;border-radius:10px!important;margin:2px 0!important}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#13263b!important}

.hero{
  position:relative!important;overflow:hidden!important;padding:34px!important;
  border:1px solid #2b5279!important;
  background:linear-gradient(120deg,rgba(7,17,31,.96),rgba(16,38,67,.92))!important;
  box-shadow:0 20px 45px rgba(2,8,23,.30)!important;
}
.hero:after{
  content:"";position:absolute;right:-55px;top:-75px;width:250px;height:250px;border-radius:50%;
  background:radial-gradient(circle,#38bdf844,transparent 67%);
}
.hero h1{color:#fff!important;font-size:46px!important;line-height:1.05!important}
.hero p{color:#cbd5e1!important;font-size:15px!important;max-width:760px}
.eyebrow{color:#67e8f9!important;background:#083344;padding:6px 9px;border-radius:999px;display:inline-block}

.kpi{
  min-height:125px!important;padding:18px!important;border:1px solid #294866!important;
  background:linear-gradient(145deg,#0b1928,#10243a)!important;
  box-shadow:0 10px 24px rgba(2,8,23,.18)!important;
}
.kpi span{color:#93c5fd!important;font-size:10px!important}
.kpi b{color:#fff!important;font-size:25px!important}
.kpi small{color:#a8bdd3!important;font-size:10px!important}

.score-panel{
  background:linear-gradient(145deg,#0b1928,#0e2034)!important;
  border:1px solid #294866!important;box-shadow:0 12px 28px rgba(2,8,23,.18)!important;
}
.score-head h3{color:#f8fafc!important}
.score-pill{background:linear-gradient(135deg,#1d4ed8,#0891b2)!important;color:#fff!important}
.check-row{border-bottom-color:#1d334a!important}
.check-row .value{color:#93c5fd!important}

.overall-score-box{background:linear-gradient(145deg,#0d1d2e,#112840)!important;border-color:#2c5276!important}
.overall-score-box:nth-child(1){border-top:3px solid #22c55e!important}
.overall-score-box:nth-child(2){border-top:3px solid #38bdf8!important}
.overall-score-box:nth-child(3){border-top:3px solid #a78bfa!important}

.rating-card{
  background:linear-gradient(145deg,#0b1928,#10243a)!important;
  border-color:#294866!important;box-shadow:0 10px 24px rgba(2,8,23,.15)!important;
}
.rating-card span{color:#93c5fd!important}
.rating-card small{color:#b6c8d9!important}
.rating-buy{background:#14532d!important;color:#bbf7d0!important}
.rating-hold{background:#713f12!important;color:#fde68a!important}
.rating-no{background:#7f1d1d!important;color:#fecaca!important}

.stButton>button{border-radius:10px!important;font-weight:800!important}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* V6 COMPANY OVERVIEW */
.company-hero{padding:22px;border-radius:16px;background:linear-gradient(135deg,#0a1b2c,#123152);border:1px solid #2e5b85}
.company-hero h2{margin:0 0 6px;color:#fff}.company-hero p{margin:0;color:#b9cde2;font-size:11px;line-height:1.6}
.company-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0}
.company-mini{padding:14px;border-radius:12px;background:#0c1c2c;border:1px solid #294866}
.company-mini span{display:block;font-size:8px;color:#7fb7e5;font-weight:900;text-transform:uppercase}.company-mini b{display:block;font-size:17px;color:#fff;margin-top:5px}
.company-section{margin-top:12px;padding:16px;border-radius:14px;background:#0b1928;border:1px solid #294866}
.company-section h3{margin:0 0 10px;color:#f8fafc}
.news-short{padding:10px 12px;margin:7px 0;border-radius:9px;background:#10243a;border-left:3px solid #38bdf8}
.news-short b{display:block;color:#fff;font-size:11px}.news-short span{display:block;color:#9fb6cb;font-size:9px;margin-top:4px}
@media(max-width:900px){.company-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.company-grid{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=21600, show_spinner=False)
def screener_shareholding(sym):
    try:
        s=requests.Session()
        s.headers.update({"User-Agent":"Mozilla/5.0"})
        q=s.get("https://www.screener.in/api/company/search/?q="+quote_plus(sym),timeout=12)
        q.raise_for_status()
        results=q.json()
        if not results:return {}
        url=results[0].get("url","")
        if not url:return {}
        h=s.get("https://www.screener.in"+url,timeout=12)
        h.raise_for_status()
        htmltxt=h.text
        m=re.search(r"<section[^>]+id=['\"]shareholding['\"][\\s\\S]*?</section>",htmltxt,re.I)
        section=m.group(0) if m else htmltxt
        rows=re.findall(r"<tr[^>]*>([\\s\\S]*?)</tr>",section,re.I)
        parsed=[]
        for row in rows:
            cells=re.findall(r"<t[hd][^>]*>([\\s\\S]*?)</t[hd]>",row,re.I)
            clean=[re.sub(r"\\s+"," ",re.sub(r"<[^>]+>"," ",c)).strip() for c in cells]
            if clean:parsed.append(clean)
        if not parsed:return {}
        header=parsed[0]
        latest_q=header[-1] if len(header)>1 else "Latest"
        out={"quarter":latest_q,"source_url":"https://www.screener.in"+url}
        for row in parsed[1:]:
            if len(row)<2:continue
            name=row[0].lower(); val=row[-1]
            mm=re.search(r"([0-9]+(?:\\.[0-9]+)?)",val.replace(",",""))
            num=float(mm.group(1)) if mm else None
            if "promoter" in name: out["promoter_holding"]=num
            elif "fii" in name: out["fii_holding"]=num
            elif "dii" in name: out["dii_holding"]=num
            elif "public" in name: out["public_holding"]=num
        return out
    except Exception:
        return {}

def _short_business(text,limit=520):
    t=re.sub(r"\\s+"," ",str(text or "")).strip()
    if not t:return "Business summary unavailable from the current data source."
    return t if len(t)<=limit else t[:limit].rsplit(" ",1)[0]+"…"

def _company_latest_news(sym,company_name,limit=3):
    q=(company_name or sym)+" stock India NSE"
    rows=google_news_rss(q,limit=limit+3)
    out=[];seen=set()
    for n in rows:
        title=n.get("title","").strip()
        if not title or title in seen:continue
        seen.add(title);out.append(n)
        if len(out)>=limit:break
    return out

def render_company_overview(sym,finfo):
    sh=screener_shareholding(sym)
    company=finfo.get("longName") or sym
    sector=finfo.get("sector") or "N/A"
    industry=finfo.get("industry") or "N/A"
    website=finfo.get("website") or ""
    business=_short_business(finfo.get("longBusinessSummary"))

    officers=finfo.get("companyOfficers") or []
    key_person="N/A"; key_title=""
    if isinstance(officers,list):
        for o in officers:
            if isinstance(o,dict) and o.get("name"):
                key_person=o.get("name"); key_title=o.get("title") or ""; break

    inst=finfo.get("heldPercentInstitutions")
    insider=finfo.get("heldPercentInsiders")
    promoter=sh.get("promoter_holding"); fii=sh.get("fii_holding"); dii=sh.get("dii_holding"); public=sh.get("public_holding")

    def pctv(v): return "N/A" if v is None else f"{float(v):.2f}%"

    st.markdown("## 🏢 Company Overview")
    st.markdown('<div class="company-hero">'+
                f'<h2>{html.escape(company)}</h2>'+
                f'<p><b>{html.escape(sector)}</b> · {html.escape(industry)}</p>'+
                '</div>',unsafe_allow_html=True)

    st.markdown('<div class="company-grid">'+
                f'<div class="company-mini"><span>Promoter Holding</span><b>{pctv(promoter)}</b></div>'+
                f'<div class="company-mini"><span>FII Holding</span><b>{pctv(fii)}</b></div>'+
                f'<div class="company-mini"><span>DII Holding</span><b>{pctv(dii)}</b></div>'+
                f'<div class="company-mini"><span>Public Holding</span><b>{pctv(public)}</b></div>'+
                '</div>',unsafe_allow_html=True)

    inst_txt="N/A" if inst is None else f"{float(inst)*100:.2f}%"
    insider_txt="N/A" if insider is None else f"{float(insider)*100:.2f}%"
    st.markdown('<div class="company-grid">'+
                f'<div class="company-mini"><span>Institutional Holding</span><b>{inst_txt}</b></div>'+
                f'<div class="company-mini"><span>Insider / Promoter Proxy</span><b>{insider_txt}</b></div>'+
                f'<div class="company-mini"><span>Latest Shareholding Quarter</span><b>{html.escape(str(sh.get("quarter","N/A")))}</b></div>'+
                f'<div class="company-mini"><span>Key Person</span><b>{html.escape(str(key_person))}</b></div>'+
                '</div>',unsafe_allow_html=True)

    st.markdown('<div class="company-section"><h3>💼 What business does it do?</h3>'+
                f'<p style="color:#b9cde2;font-size:11px;line-height:1.7">{html.escape(business)}</p></div>',unsafe_allow_html=True)

    if key_title:
        st.caption(f"Key management: {key_person} — {key_title}. Exact promoter names may require the official shareholding filing.")

    news=_company_latest_news(sym,company,3)
    st.markdown('<div class="company-section"><h3>📰 Latest News — Short</h3>',unsafe_allow_html=True)
    if news:
        for n in news:
            st.markdown('<div class="news-short">'+
                        f'<b>{html.escape(n.get("title",""))}</b>'+
                        f'<span>{html.escape(n.get("source",""))} · {html.escape(n.get("published",""))}</span>'+
                        '</div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="news-short"><span>No recent matching news found.</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    if website: st.markdown(f"[Company website]({website})")
    if sh.get("source_url"): st.caption("Shareholding source: Screener public company page (best-effort parsing).")

st.sidebar.markdown("## 📈 NSE PRO")
page=st.sidebar.radio("Open module",["🏠 Dashboard","🧠 Pro Analyzer","🚀 Swing Screeners","📰 Stock News","🎯 Brokerage Calls","🌐 All NSE Performance","🏦 Institutional Watch","💾 Market Data Hub"],key="main_page")

if page=="🏠 Dashboard":
    st.markdown('<div class="hero"><div class="eyebrow">NSE MARKET INTELLIGENCE</div><h1>Smart stock research.<br>One fast terminal.</h1><p>Analyze fundamentals and technicals, scan swing opportunities, follow stock news and brokerage calls, and stop maintaining closing prices manually.</p></div>',unsafe_allow_html=True)
    c=st.columns(4)
    vals=[("🧠 PRO ANALYZER","10 + 10 Score","Fundamental + Technical"),
          ("🚀 SWING LIBRARY",str(len(SCREENERS))+" Screeners","Momentum & Breakout"),
          ("📰 MARKET INTEL","News + Calls","Events & Broker Targets"),
          ("🌐 NSE PERFORMANCE","1D → 5Y","Automatic Market Data")]
    for col,v in zip(c,vals):
        with col:
            st.markdown(f'<div class="kpi"><span>{v[0]}</span><b>{v[1]}</b><small>{v[2]}</small></div>',unsafe_allow_html=True)

elif page=="🧠 Pro Analyzer":
    syms=universe()
    if "analyzer_symbol" not in st.session_state:
        st.session_state["analyzer_symbol"]="TBZ" if "TBZ" in syms else syms[0]
    elif st.session_state["analyzer_symbol"] not in syms:
        st.session_state["analyzer_symbol"]="TBZ" if "TBZ" in syms else syms[0]

    sym=st.selectbox("NSE symbol",syms,key="analyzer_symbol")
    period=st.select_slider("Period",["3mo","6mo","1y","2y","5y"],value=st.session_state.get("analyzer_period","1y"),key="analyzer_period")
    analyze_clicked=st.button("⚡ Analyze",type="primary")
    auto_analyze=bool(st.session_state.pop("auto_analyze",False))

    if analyze_clicked or auto_analyze:
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

            with st.spinner("Loading fundamentals and intraday confirmation..."):
                finfo=fundamentals_for_stock(sym)
                intraday_df=intraday_stock(sym)

            fundamental_checks,fundamental_score=fundamental_checklist(finfo)
            technical_checks,technical_score=technical_checklist(x)

            st.markdown("## ✅ Fundamental & Technical Scorecard")
            left,right=st.columns(2)
            with left:render_checklist("🏢 Fundamental Checklist",fundamental_checks,fundamental_score)
            with right:render_checklist("📊 Technical Checklist",technical_checks,technical_score)

            overall=(fundamental_score+technical_score)/2
            st.markdown('<div class="overall-score-strip">'+
                        f'<div class="overall-score-box"><span>Fundamental</span><b>{fundamental_score:.1f}/10</b></div>'+
                        f'<div class="overall-score-box"><span>Technical</span><b>{technical_score:.1f}/10</b></div>'+
                        f'<div class="overall-score-box"><span>Overall</span><b>{overall:.1f}/10</b></div>'+
                        '</div>',unsafe_allow_html=True)

            st.markdown("## ⏱️ Buy / Hold / No by Time Horizon")
            ratings=horizon_ratings(x,fundamental_score,intraday_df)
            rcols=st.columns(4)
            for rc,(horizon,rating,rcls,notes) in zip(rcols,ratings):
                with rc:
                    note_text=" · ".join(notes[:3]) if notes else "No confirmation"
                    st.markdown('<div class="rating-card">'+f'<span>{horizon}</span>'+f'<b class="{rcls}">{rating}</b>'+f'<small>{html.escape(note_text)}</small>'+'</div>',unsafe_allow_html=True)

            st.caption("BUY / HOLD / NO is a rule-based signal from available market and fundamental data, not a guarantee or personalized investment recommendation.")
            atr=float(x.ATR14.iloc[-1]);stop=latest-1.5*atr;risk=latest-stop;t1=latest+1.5*risk;t2=latest+3*risk
            st.markdown("### 🛡️ Trade Execution & Risk")
            cs=st.columns(5)
            for col,v in zip(cs,[("ENTRY",latest),("STOP LOSS",stop),("TARGET 1",t1),("TARGET 2",t2),("R:R","1 : 3.0")]):
                with col:st.markdown(f'<div class="kpi"><span>{v[0]}</span><b>{("₹"+format(v[1],",.2f")) if isinstance(v[1],float) else v[1]}</b></div>',unsafe_allow_html=True)

            render_company_overview(sym,finfo)

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
                if st.button(f'🔎 Open {r["Symbol"]} in Pro Analyzer',key=f'open_pick_{r["Symbol"]}',use_container_width=True):
                    st.session_state["analyzer_symbol"]=r["Symbol"]
                    st.session_state["analyzer_period"]="1y"
                    st.session_state["auto_analyze"]=True
                    st.session_state["main_page"]="🧠 Pro Analyzer"
                    st.rerun()

    name=st.selectbox("Preset",list(SCREENERS));st.info(SCREENERS[name]);size=st.selectbox("Universe size",[100,250,500,1000,"All"],index=1)
    if st.button("🔥 Run Screener",type="primary"):
        syms=universe();syms=syms if size=="All" else syms[:int(size)]
        with st.spinner("Downloading market history in batches..."):snap=bulk_snapshot(tuple(syms),"1y");res=run_screen(snap,name)
        res=clean_display(res)
        st.dataframe(res,use_container_width=True,height=600,hide_index=True)
        if not res.empty:
            chosen_symbol=st.selectbox("Open a matched stock in Pro Analyzer",res["Symbol"].astype(str).tolist(),key="screen_result_symbol")
            if st.button("🧠 Open Selected Stock Analysis",type="primary",use_container_width=True):
                st.session_state["analyzer_symbol"]=chosen_symbol
                st.session_state["analyzer_period"]="1y"
                st.session_state["auto_analyze"]=True
                st.session_state["main_page"]="🧠 Pro Analyzer"
                st.rerun()
        st.download_button("⬇️ Download CSV",res.to_csv(index=False).encode(),name.replace(" ","_")+".csv","text/csv")


elif page=="📰 Stock News":
    st.markdown("## 📰 Stock News & Event Radar")
    st.caption("Search stock-specific news for results, buybacks, corporate actions, price moves and company events.")
    c1,c2,c3=st.columns([1.2,1,1])
    with c1: q=st.text_input("Stock / company / topic",value="TBZ")
    with c2: mode=st.selectbox("News type",["All","Results","Buyback","Corporate Action","Positive Move","Negative Move"])
    with c3: count=st.selectbox("Articles",[10,20,30],index=1)

    if st.button("⚡ Load Latest News",type="primary"):
        with st.spinner("Fetching latest news..."):
            rows=google_news_rss(q+" stock India NSE",count)
        outrows=[]
        for n in rows:
            n=n.copy(); n["type"]=classify_news(n["title"])
            if mode=="All" or n["type"]==mode: outrows.append(n)
        st.session_state["news_rows"]=outrows

    rows=st.session_state.get("news_rows",[])
    if rows:
        st.markdown(f"### Latest matching stories ({len(rows)})")
        for n in rows:
            card = (
                '<div class="news-card">'
                + '<span class="news-tag">'+html.escape(n["type"])+'</span>'
                + '<div class="news-meta">'+html.escape(n["source"])+' | '+html.escape(n["published"])+'</div>'
                + '<h4>'+html.escape(n["title"])+'</h4>'
                + '<p>'+html.escape(n["description"][:260])+'</p>'
                + '<a href="'+n["link"]+'" target="_blank">Open article ↗</a>'
                + '</div>'
            )
            st.markdown(card,unsafe_allow_html=True)

    st.markdown("### Quick event searches")
    qcols=st.columns(4)
    quick=[("TBZ / GRT Buyback","TBZ GRT buyback stock India"),
           ("Quarterly Results","Q1 results India stocks profit revenue"),
           ("PVR INOX","PVR INOX shares fall reason"),
           ("Milky Mist","Milky Mist Q1 results")]
    for col,(label,qq) in zip(qcols,quick):
        with col:
            if st.button(label,use_container_width=True,key="news_"+label):
                with st.spinner("Fetching..."):
                    st.session_state["news_rows"]=[dict(x,type=classify_news(x["title"])) for x in google_news_rss(qq,20)]
                st.rerun()

elif page=="🎯 Brokerage Calls":
    st.markdown("## 🎯 Brokerage Calls & Target Tracker")
    st.caption("Tracks public brokerage-call headlines, target prices when detectable, current price and return since the call date.")
    brokers=["Jefferies","Motilal Oswal","ICICI Securities","HDFC Securities","Axis Securities","Morgan Stanley","Goldman Sachs","CLSA","Nomura","JM Financial"]
    chosen=st.multiselect("Brokerages",brokers,default=["Jefferies","Motilal Oswal"])
    limit=st.selectbox("Headlines per brokerage",[10,20,30],index=1)
    if st.button("⚡ Refresh Brokerage Calls",type="primary"):
        syms=universe()
        allrows=[]
        with st.spinner("Searching brokerage calls and comparing market prices..."):
            for b in chosen:
                allrows.extend(broker_calls_from_news(b,syms,limit))
        st.session_state["broker_rows"]=allrows

    rows=st.session_state.get("broker_rows",[])
    if rows:
        df=pd.DataFrame(rows)
        for c in ["Target","Call Price","Current","Return Since Call %"]:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce").round(2)
        k1,k2,k3=st.columns(3)
        with k1: st.metric("Calls found",len(df))
        with k2: st.metric("Targets hit",int((df["Status"]=="Target Hit").sum()))
        with k3: st.metric("Below target",int((df["Status"]=="Below Target").sum()))
        show=["Broker","Symbol","Published","Target","Call Price","Current","Return Since Call %","Status","Source","Headline"]
        st.dataframe(df[show],use_container_width=True,height=620,hide_index=True)
        st.download_button("⬇️ Download Brokerage Calls CSV",df.to_csv(index=False).encode(),"brokerage_calls.csv","text/csv")
        st.info("Target and symbol are parsed only when clearly present in public news text. Blank means not confidently detected.")

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
