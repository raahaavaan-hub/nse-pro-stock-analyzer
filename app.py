
import io, re, html, requests, numpy as np, pandas as pd, streamlit as st, yfinance as yf
import requests
import plotly.graph_objects as go
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

st.set_page_config(page_title="NSE Pro Market Terminal V14", page_icon="📈", layout="wide")

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
.pick-card-link{display:block!important;text-decoration:none!important;color:inherit!important;cursor:pointer!important;transition:.16s ease}
.pick-card-link:hover{transform:translateY(-2px);border-color:#38bdf8!important;box-shadow:0 12px 26px rgba(56,189,248,.16)!important}

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
        keys=["revenueGrowth","earningsGrowth","returnOnEquity","returnOnAssets","operatingMargins","grossMargins","ebitdaMargins","debtToEquity","currentRatio","quickRatio","freeCashflow","operatingCashflow","trailingPE","forwardPE","priceToBook","bookValue","trailingEps","forwardEps","dividendYield","beta","profitMargins","marketCap","enterpriseValue","totalRevenue","fullTimeEmployees","longName","sector","industry","longBusinessSummary","website","city","country","companyOfficers","heldPercentInstitutions","heldPercentInsiders"]
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
    city=finfo.get("city") or ""
    country=finfo.get("country") or ""
    business=_short_business(finfo.get("longBusinessSummary"))

    officers=finfo.get("companyOfficers") or []
    key_person="N/A"; key_title=""
    if isinstance(officers,list):
        for o in officers:
            if isinstance(o,dict) and o.get("name"):
                key_person=o.get("name"); key_title=o.get("title") or ""; break

    inst=finfo.get("heldPercentInstitutions")
    insider=finfo.get("heldPercentInsiders")
    promoter=sh.get("promoter_holding")
    fii=sh.get("fii_holding")
    dii=sh.get("dii_holding")
    public=sh.get("public_holding")

    def pctv(v): return "N/A" if v is None else f"{float(v):.2f}%"
    def pct100(v): return "N/A" if v is None else f"{float(v)*100:.2f}%"
    def num(v,dec=2):
        try:
            if v is None or not np.isfinite(float(v)): return "N/A"
            return f"{float(v):,.{dec}f}"
        except Exception:return "N/A"
    def rupee_crore(v):
        try:
            if v is None or not np.isfinite(float(v)): return "N/A"
            return f"₹{float(v)/1e7:,.0f} Cr"
        except Exception:return "N/A"
    def compact_money(v):
        try:
            if v is None or not np.isfinite(float(v)): return "N/A"
            x=float(v)
            if abs(x)>=1e12:return f"₹{x/1e12:.2f} T"
            if abs(x)>=1e9:return f"₹{x/1e9:.2f} B"
            if abs(x)>=1e7:return f"₹{x/1e7:.0f} Cr"
            return f"₹{x:,.0f}"
        except Exception:return "N/A"

    market_cap=finfo.get("marketCap")
    enterprise=finfo.get("enterpriseValue")
    employees=finfo.get("fullTimeEmployees")
    location=", ".join([x for x in [city,country] if x]) or "N/A"

    st.markdown("## 🏢 Company Overview")
    st.markdown(
        '<div class="company-hero">'+
        f'<h2>{html.escape(company)}</h2>'+
        f'<p><b>{html.escape(sector)}</b> · {html.escape(industry)} · {html.escape(location)}</p>'+
        '</div>',unsafe_allow_html=True
    )

    # Identity / size
    st.markdown("### 🏷️ Business & Size")
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Sector</span><b>{html.escape(sector)}</b></div>'+
        f'<div class="company-mini"><span>Industry</span><b>{html.escape(industry)}</b></div>'+
        f'<div class="company-mini"><span>Market Cap</span><b>{rupee_crore(market_cap)}</b></div>'+
        f'<div class="company-mini"><span>Enterprise Value</span><b>{rupee_crore(enterprise)}</b></div>'+
        '</div>',unsafe_allow_html=True
    )

    # Ownership
    st.markdown("### 👥 Ownership")
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Promoter Holding</span><b>{pctv(promoter)}</b></div>'+
        f'<div class="company-mini"><span>FII Holding</span><b>{pctv(fii)}</b></div>'+
        f'<div class="company-mini"><span>DII Holding</span><b>{pctv(dii)}</b></div>'+
        f'<div class="company-mini"><span>Public Holding</span><b>{pctv(public)}</b></div>'+
        '</div>',unsafe_allow_html=True
    )
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Institutional Holding</span><b>{pct100(inst)}</b></div>'+
        f'<div class="company-mini"><span>Insider / Promoter Proxy</span><b>{pct100(insider)}</b></div>'+
        f'<div class="company-mini"><span>Shareholding Quarter</span><b>{html.escape(str(sh.get("quarter","N/A")))}</b></div>'+
        f'<div class="company-mini"><span>Key Person</span><b>{html.escape(str(key_person))}</b></div>'+
        '</div>',unsafe_allow_html=True
    )

    # Valuation & profitability
    st.markdown("### 💹 Valuation & Profitability")
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Trailing P/E</span><b>{num(finfo.get("trailingPE"))}</b></div>'+
        f'<div class="company-mini"><span>Forward P/E</span><b>{num(finfo.get("forwardPE"))}</b></div>'+
        f'<div class="company-mini"><span>Price / Book</span><b>{num(finfo.get("priceToBook"))}</b></div>'+
        f'<div class="company-mini"><span>Book Value / Share</span><b>{num(finfo.get("bookValue"))}</b></div>'+
        '</div>',unsafe_allow_html=True
    )
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>EPS TTM</span><b>{num(finfo.get("trailingEps"))}</b></div>'+
        f'<div class="company-mini"><span>Forward EPS</span><b>{num(finfo.get("forwardEps"))}</b></div>'+
        f'<div class="company-mini"><span>ROE</span><b>{pct100(finfo.get("returnOnEquity"))}</b></div>'+
        f'<div class="company-mini"><span>ROA</span><b>{pct100(finfo.get("returnOnAssets"))}</b></div>'+
        '</div>',unsafe_allow_html=True
    )

    # Growth / margins
    st.markdown("### 📈 Growth & Margins")
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Revenue Growth</span><b>{pct100(finfo.get("revenueGrowth"))}</b></div>'+
        f'<div class="company-mini"><span>Earnings Growth</span><b>{pct100(finfo.get("earningsGrowth"))}</b></div>'+
        f'<div class="company-mini"><span>Operating Margin</span><b>{pct100(finfo.get("operatingMargins"))}</b></div>'+
        f'<div class="company-mini"><span>Profit Margin</span><b>{pct100(finfo.get("profitMargins"))}</b></div>'+
        '</div>',unsafe_allow_html=True
    )

    # Financial strength / trading characteristics
    st.markdown("### 🧾 Financial Strength & Market Characteristics")
    emp_txt="N/A" if employees is None else f"{int(employees):,}"
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Debt / Equity</span><b>{num(finfo.get("debtToEquity"))}</b></div>'+
        f'<div class="company-mini"><span>Current Ratio</span><b>{num(finfo.get("currentRatio"))}</b></div>'+
        f'<div class="company-mini"><span>Beta</span><b>{num(finfo.get("beta"))}</b></div>'+
        f'<div class="company-mini"><span>Employees</span><b>{emp_txt}</b></div>'+
        '</div>',unsafe_allow_html=True
    )
    st.markdown(
        '<div class="company-grid">'+
        f'<div class="company-mini"><span>Dividend Yield</span><b>{pct100(finfo.get("dividendYield"))}</b></div>'+
        f'<div class="company-mini"><span>Free Cash Flow</span><b>{compact_money(finfo.get("freeCashflow"))}</b></div>'+
        f'<div class="company-mini"><span>Operating Cash Flow</span><b>{compact_money(finfo.get("operatingCashflow"))}</b></div>'+
        f'<div class="company-mini"><span>Total Revenue</span><b>{compact_money(finfo.get("totalRevenue"))}</b></div>'+
        '</div>',unsafe_allow_html=True
    )

    st.markdown(
        '<div class="company-section"><h3>💼 What business does it do?</h3>'+
        f'<p style="color:#b9cde2;font-size:11px;line-height:1.7">{html.escape(business)}</p></div>',
        unsafe_allow_html=True
    )

    if key_title:
        st.caption(f"Key management: {key_person} — {key_title}. Exact promoter names may require the official shareholding filing.")

    news=_company_latest_news(sym,company,3)
    st.markdown('<div class="company-section"><h3>📰 Latest News — Short</h3>',unsafe_allow_html=True)
    if news:
        for n in news:
            st.markdown(
                '<div class="news-short">'+
                f'<b>{html.escape(n.get("title",""))}</b>'+
                f'<span>{html.escape(n.get("source",""))} · {html.escape(n.get("published",""))}</span>'+
                '</div>',unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="news-short"><span>No recent matching news found.</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    if website: st.markdown(f"[Company website]({website})")
    if sh.get("source_url"): st.caption("Shareholding source: Screener public company page (best-effort parsing).")



@st.cache_data(ttl=300, show_spinner=False)
def nse_all_indices():
    """Official NSE index snapshot. Returns all indices exposed by NSE's public all-indices endpoint."""
    try:
        s=requests.Session()
        s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
            "Accept-Language":"en-US,en;q=0.9",
            "Accept":"application/json,text/plain,*/*",
            "Referer":"https://www.nseindia.com/market-data/live-market-indices"
        })
        s.get("https://www.nseindia.com",timeout=10)
        r=s.get("https://www.nseindia.com/api/allIndices",timeout=12)
        r.raise_for_status()
        j=r.json()
        rows=j.get("data",[]) if isinstance(j,dict) else []
        out=[]
        for x in rows:
            name=str(x.get("index") or x.get("indexSymbol") or x.get("key") or "").strip()
            if not name: continue
            last=x.get("last")
            pct=x.get("percentChange")
            try:last=float(str(last).replace(",",""))
            except:last=None
            try:pct=float(str(pct).replace(",",""))
            except:pct=None
            out.append({"name":name,"last":last,"pct":pct})
        return out
    except Exception:
        return []

@st.cache_data(ttl=300, show_spinner=False)
def nse_market_statistics():
    """
    Best-effort parse of NSE's official homepage Market Statistics.
    Returns source='NSE' only when all four breadth figures are successfully parsed.
    """
    try:
        s=requests.Session()
        s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
            "Accept-Language":"en-US,en;q=0.9",
            "Referer":"https://www.nseindia.com/"
        })
        r=s.get("https://www.nseindia.com/?view=desktop",timeout=15)
        r.raise_for_status()
        txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",r.text))
        labels={
            "stock_traded":"Stock Traded",
            "advances":"Advances",
            "declines":"Declines",
            "unchanged":"Unchanged",
            "high52":"No. of Stocks at 52 Week High",
            "low52":"No. of Stocks at 52 Week Low",
            "upper":"No. of Stocks in Upper Circuit",
            "lower":"No. of Stocks in Lower Circuit"
        }
        out={}
        for key,label in labels.items():
            m=re.search(re.escape(label)+r".{0,120}?([0-9][0-9,]*)",txt,re.I)
            if m:
                out[key]=int(m.group(1).replace(",",""))
        tm=re.search(r"As on\s+([0-9]{1,2}-[A-Za-z]{3}-[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}\s+IST)",txt,re.I)
        if tm: out["as_on"]=tm.group(1)
        out["source"]="NSE" if all(k in out for k in ["stock_traded","advances","declines","unchanged"]) else "Unavailable"
        return out
    except Exception:
        return {"source":"Unavailable"}

def _index_lookup(rows):
    return {str(r.get("name","")).upper():r for r in rows}

def _pick_nse_indices(rows, wanted_names):
    lookup=_index_lookup(rows)
    selected=[]
    used=set()
    for wanted in wanted_names:
        w=wanted.upper()
        exact=lookup.get(w)
        if exact and exact["name"] not in used:
            selected.append(exact);used.add(exact["name"]);continue
        # tolerant matching for NSE naming differences
        for name,row in lookup.items():
            if w in name or name in w:
                if row["name"] not in used:
                    selected.append(row);used.add(row["name"]);break
    return selected

@st.cache_data(ttl=900, show_spinner=False)
def brokerage_tags_for_symbols(symbols_tuple):
    """Fast public-news brokerage tagger. Adds broker names only; does not fetch per-call prices."""
    symbols=list(symbols_tuple)
    brokers=["Jefferies","Motilal Oswal","ICICI Securities","HDFC Securities","Axis Securities","CLSA","Nomura","Morgan Stanley","Goldman Sachs","JM Financial"]
    tags={s:[] for s in symbols}
    for broker in brokers:
        try:
            news=google_news_rss(f'"{broker}" (buy OR target OR upgrade OR overweight) stock India',18)
            for n in news:
                txt=(n.get("title","") or "")+" "+(n.get("description","") or "")
                sym=symbol_from_headline(txt,symbols)
                if sym and broker not in tags[sym]:
                    tags[sym].append(broker)
        except Exception:
            pass
    return {k:", ".join(v) for k,v in tags.items() if v}

# V8 safe navigation: resolve requested page before sidebar widgets are created.
_pending_page=st.session_state.pop("pending_page",None)
if _pending_page:
    st.session_state["main_page"]=_pending_page

_qp_page=st.query_params.get("page","")
_qp_stock=st.query_params.get("stock","")
if _qp_page=="pro" and _qp_stock:
    _stock=str(_qp_stock).upper().strip()
    st.session_state["main_page"]="🧠 Pro Analyzer"
    st.session_state["analyzer_symbol"]=_stock
    st.session_state["analyzer_period"]="1y"
    st.session_state["auto_analyze"]=True
    st.query_params.clear()


st.markdown("""
<style>
/* V10 readability */
div[data-testid="stButton"] > button {
 background:#18304d !important;color:#ffffff !important;
 border:1px solid #4da3ff !important;font-weight:800 !important;
}
div[data-testid="stButton"] > button:hover {
 background:#2563eb !important;color:#fff !important;border-color:#93c5fd !important;
}
div[data-testid="stButton"] > button p {color:#ffffff !important;font-weight:800 !important;}
div[data-baseweb="select"] > div {background:#f8fafc !important;color:#0f172a !important;}
div[data-baseweb="select"] * {color:#0f172a !important;}
div[data-testid="stNumberInput"] input {background:#f8fafc !important;color:#0f172a !important;font-weight:700 !important;}
div[data-testid="stNumberInput"] button {color:#0f172a !important;}
label[data-testid="stWidgetLabel"] p {color:#cbd5e1 !important;font-weight:700 !important;}
div[data-testid="stMetric"] label p {color:#9fb3c8 !important;}
div[data-testid="stMetricValue"] {color:#f8fafc !important;}
</style>
""",unsafe_allow_html=True)


st.markdown("""
<style>
/* V14 compact heat map */
.nse-heat-grid{
  display:grid;
  grid-template-columns:repeat(6,minmax(0,1fr));
  gap:8px;
  margin:8px 0 18px;
}
.nse-heat-card{
  min-height:72px;
  padding:9px 10px;
  border-radius:9px;
  color:#fff;
  box-shadow:0 3px 10px rgba(2,8,23,.12);
}
.nse-heat-name{
  font-size:9px;
  line-height:1.15;
  font-weight:900;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.nse-heat-value{
  font-size:14px;
  line-height:1.2;
  font-weight:900;
  margin-top:8px;
}
.nse-heat-change{
  font-size:11px;
  font-weight:900;
  margin-top:3px;
}
@media(max-width:1100px){.nse-heat-grid{grid-template-columns:repeat(4,minmax(0,1fr));}}
@media(max-width:700px){.nse-heat-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
</style>
""",unsafe_allow_html=True)

st.sidebar.markdown("## 📈 NSE PRO")
page=st.sidebar.radio("Open module",["🏠 Dashboard","🔥 Market Heatmap","🧠 Pro Analyzer","🚀 Swing Screeners","📰 Stock News","🎯 Brokerage Calls","🌐 All NSE Performance","🏦 Institutional Watch","💾 Market Data Hub"],key="main_page")


st.sidebar.markdown("---")
st.sidebar.link_button(
    "🛠️ Open app.py on GitHub",
    "https://github.com/raahaavaan-hub/nse-pro-stock-analyzer/blob/main/app.py",
    use_container_width=True
)
st.sidebar.caption("Open the live app.py file directly when you want to update the website.")


@st.cache_data(ttl=3600,show_spinner=False)
def PA_nse_shareholding(symbol):
    """Best-effort official NSE shareholding pattern loader."""
    base="https://www.nseindia.com"
    h={"User-Agent":"Mozilla/5.0","Accept":"application/json,text/plain,*/*",
       "Referer":base+"/companies-listing/corporate-filings-shareholding-pattern"}
    sess=requests.Session(); sess.headers.update(h)
    try:sess.get(base,timeout=8)
    except Exception:pass
    urls=[
      f"{base}/api/corporate-share-holdings-master?index=equities&symbol={symbol}",
      f"{base}/api/corporate-share-holdings?index=equities&symbol={symbol}"
    ]
    payload=None
    for u in urls:
        try:
            rr=sess.get(u,timeout=12)
            if rr.ok and rr.text.strip():
                payload=rr.json()
                if payload:break
        except Exception:pass
    if not payload:return pd.DataFrame()

    records=[]
    def walk(v):
        if isinstance(v,list):
            for z in v:walk(z)
        elif isinstance(v,dict):
            lk=" ".join(str(k).lower() for k in v)
            if any(w in lk for w in ["fii","dii","promoter","public","foreign institutional","foreign portfolio"]):
                records.append(v)
            for z in v.values():
                if isinstance(z,(dict,list)):walk(z)
    walk(payload)

    def val(d,terms):
        for k,v in d.items():
            k=str(k).lower().replace("_"," ")
            if any(t in k for t in terms):
                try:return float(str(v).replace("%","").replace(",","").strip())
                except:pass
        return None
    rows=[]
    for d in records:
        period=""
        for k,v in d.items():
            if any(t in str(k).lower() for t in ["date","quarter","period","as on"]):
                if v not in (None,""):period=str(v);break
        row={"Period":period,
             "Promoters":val(d,["promoter"]),
             "FII":val(d,["fii","foreign institutional","foreign portfolio"]),
             "DII":val(d,["dii","domestic institutional","mutual fund"]),
             "Government":val(d,["government"]),
             "Public":val(d,["public"]),
             "Others":val(d,["others","other"]),
             "Shareholders":val(d,["shareholder"])}
        if any(row[k] is not None for k in ["Promoters","FII","DII","Government","Public","Others"]):rows.append(row)
    return pd.DataFrame(rows).drop_duplicates().tail(12) if rows else pd.DataFrame()

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

elif page=="🔥 Market Heatmap":
    st.markdown("<div class='hero'><div class='eyebrow'>NSE STOCK HEATMAP</div><h1>🔥 Individual Stock Heatmap</h1><p>Green = stock up, red = stock down. Review an index group or the full NSE equity universe.</p></div>",unsafe_allow_html=True)

    f1,f2,f3,f4=st.columns([2,2,2,1])
    with f1:
        universe_name=st.selectbox("Stocks",["ALL NSE","NIFTY 50","NIFTY 100","NIFTY 200","NIFTY 500"],index=0,key="heat_stock_universe")
    with f2:
        heat_period=st.selectbox("Performance",["1 Day","1 Week","1 Month","3 Months","6 Months","1 Year","5 Years"],index=0,key="heat_period")
    with f3:
        sort_mode=st.selectbox("Arrange",["🟢 Green first → 🔴 Red last","🚀 Highest % first","🔻 Lowest % first","A → Z"],index=0,key="heat_sort_mode")
    with f4:
        if st.button("↻ Refresh",use_container_width=True,key="heat_stock_refresh"):
            st.cache_data.clear(); st.rerun()

    move_filter=st.radio("Show",["All","🟢 Gainers","🔴 Losers","⚪ Unchanged"],horizontal=True,key="heat_move_filter")

    nifty50=["ADANIENT","ADANIPORTS","APOLLOHOSP","ASIANPAINT","AXISBANK","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BEL","BHARTIARTL","CIPLA","COALINDIA","DRREDDY","EICHERMOT","ETERNAL","GRASIM","HCLTECH","HDFCBANK","HDFCLIFE","HEROMOTOCO","HINDALCO","HINDUNILVR","ICICIBANK","INDUSINDBK","INFY","ITC","JIOFIN","JSWSTEEL","KOTAKBANK","LT","M&M","MARUTI","NESTLEIND","NTPC","ONGC","POWERGRID","RELIANCE","SBILIFE","SBIN","SHRIRAMFIN","SUNPHARMA","TATACONSUM","TATAMOTORS","TATASTEEL","TCS","TECHM","TITAN","TRENT","ULTRACEMCO","WIPRO"]

    all_syms=list(dict.fromkeys(universe()))
    if universe_name=="ALL NSE":
        syms=all_syms
    else:
        target={"NIFTY 50":50,"NIFTY 100":100,"NIFTY 200":200,"NIFTY 500":500}[universe_name]
        syms=(nifty50+[s for s in all_syms if s not in nifty50])[:target]

    @st.cache_data(ttl=300,show_spinner=False)
    def stock_heat_prices(symbols,period_label):
        cfg={
            "1 Day":("5d",1),
            "1 Week":("1mo",5),
            "1 Month":("3mo",21),
            "3 Months":("6mo",63),
            "6 Months":("1y",126),
            "1 Year":("2y",252),
            "5 Years":("5y",1260),
        }
        yf_period,lookback=cfg[period_label]
        result=[]
        loaded=set()

        def add_row(s,c):
            c=c.dropna()
            if len(c)<1:return
            last=float(c.iloc[-1])
            base=float(c.iloc[-(lookback+1)]) if len(c)>lookback else float(c.iloc[0])
            ch=last-base
            pct=(ch/base*100) if base else 0
            result.append((s,last,ch,pct))
            loaded.add(s)

        # Fast batch pass
        for k in range(0,len(symbols),100):
            batch=symbols[k:k+100]; tick=[s+".NS" for s in batch]
            try:
                data=yf.download(tick,period=yf_period,interval="1d",group_by="ticker",auto_adjust=False,progress=False,threads=True)
            except Exception:
                data=None
            if data is not None:
                for s,t in zip(batch,tick):
                    try:
                        d=data if len(batch)==1 else data[t]
                        add_row(s,d["Close"])
                    except Exception:
                        pass

        # Retry missing stocks one-by-one. This prevents a partial Yahoo batch
        # response from turning NIFTY 50 into only 20/42 visible tiles.
        missing=[s for s in symbols if s not in loaded]
        for s in missing:
            try:
                d=yf.download(s+".NS",period=yf_period,interval="1d",auto_adjust=False,progress=False,threads=False)
                if isinstance(d.columns,pd.MultiIndex):
                    d.columns=[c[0] for c in d.columns]
                add_row(s,d["Close"])
            except Exception:
                pass

        order={s:i for i,s in enumerate(symbols)}
        return sorted(result,key=lambda x:order.get(x[0],999999))

    with st.spinner(f"Loading {len(syms):,} {universe_name} stocks · {heat_period}..."):
        rows=stock_heat_prices(syms,heat_period)

    if not rows:
        st.warning("Stock data unavailable. Press Refresh.")
    else:
        up=sum(x[3]>0 for x in rows); down=sum(x[3]<0 for x in rows); flat=len(rows)-up-down
        m=st.columns(4)
        m[0].metric("Stocks loaded",len(rows));m[1].metric("🟢 Up",up);m[2].metric("🔴 Down",down);m[3].metric("⚪ Flat",flat)
        if universe_name=="NIFTY 50" and len(rows)<50:
            missing_symbols=[s for s in syms if s not in {r[0] for r in rows}]
            st.warning(f"Price provider returned {len(rows)}/50 NIFTY 50 stocks. Missing: {', '.join(missing_symbols)}")

        if move_filter=="🟢 Gainers": rows=[x for x in rows if x[3]>0]
        elif move_filter=="🔴 Losers": rows=[x for x in rows if x[3]<0]
        elif move_filter=="⚪ Unchanged": rows=[x for x in rows if x[3]==0]

        if sort_mode=="🟢 Green first → 🔴 Red last":
            rows=sorted(rows,key=lambda x:(x[3]<=0,-x[3] if x[3]>0 else x[3]))
            gainers=sorted([x for x in rows if x[3]>0],key=lambda x:x[3],reverse=True)
            flatrows=[x for x in rows if x[3]==0]
            losers=sorted([x for x in rows if x[3]<0],key=lambda x:x[3],reverse=True)
            rows=gainers+flatrows+losers
        elif sort_mode=="🚀 Highest % first": rows=sorted(rows,key=lambda x:x[3],reverse=True)
        elif sort_mode=="🔻 Lowest % first": rows=sorted(rows,key=lambda x:x[3])
        else: rows=sorted(rows,key=lambda x:x[0])

        def hc(x):
            if x>=5:return "#04783d"
            if x>=2:return "#0b9f50"
            if x>0:return "#38b96b"
            if x<=-5:return "#a40f1d"
            if x<=-2:return "#d7273b"
            if x<0:return "#ef7a86"
            return "#64748b"

        cards=[]
        for s,last,ch,pct in rows:
            # Query parameter lets a heatmap tile deep-link into Pro Analyzer.
            href=f"?page=pro&stock={s}"
            cards.append(f"<a href='{href}' target='_self' style='text-decoration:none;color:white'><div class='nse-heat-card' style='background:{hc(pct)};min-height:82px;cursor:pointer'><div class='nse-heat-name' style='font-size:11px'>{html.escape(s)}</div><div class='nse-heat-value'>₹{last:,.2f}</div><div class='nse-heat-change'>{ch:+,.2f} &nbsp; {pct:+.2f}%</div></div></a>")
        st.caption(f"{universe_name} · {len(rows):,} displayed · {heat_period} performance · click a stock to open Pro Analyzer")
        st.markdown("<div class='nse-heat-grid'>"+"".join(cards)+"</div>",unsafe_allow_html=True)

elif page=="🧠 Pro Analyzer":
    st.markdown("<div class='hero'><div class='eyebrow'>COMPLETE STOCK RESEARCH</div><h1>🧠 Pro Analyzer</h1><p>Fundamentals + financial statements + ownership + technicals + swing setup in one page.</p></div>",unsafe_allow_html=True)

    # Heatmap deep-link preloads this key before sidebar widgets are created.
    _default_symbol=str(st.session_state.get("analyzer_symbol","RELIANCE")).replace(".NS","").upper()
    _all_symbols=list(dict.fromkeys(universe()))
    if _default_symbol not in _all_symbols:_all_symbols=[_default_symbol]+_all_symbols

    pa1,pa2=st.columns([4,1])
    with pa1:
        symbol=st.selectbox("NSE stock",_all_symbols,index=_all_symbols.index(_default_symbol),key="pro_analyzer_stock")
    with pa2:
        st.write("")
        analyze=st.button("🔎 Analyze",use_container_width=True,key="pro_analyze_btn")
    ticker=symbol+".NS"

    @st.cache_data(ttl=900,show_spinner=False)
    def PA_bundle(t):
        tk=yf.Ticker(t)
        try: info=tk.info or {}
        except Exception: info={}
        try: hist=tk.history(period="5y",auto_adjust=False)
        except Exception: hist=pd.DataFrame()
        def safe_df(attr):
            try:
                x=getattr(tk,attr)
                return x if isinstance(x,pd.DataFrame) else pd.DataFrame()
            except Exception:return pd.DataFrame()
        return info,hist,safe_df("quarterly_financials"),safe_df("financials"),safe_df("quarterly_balance_sheet"),safe_df("balance_sheet"),safe_df("quarterly_cashflow"),safe_df("cashflow"),safe_df("major_holders"),safe_df("institutional_holders")

    def PA_num(x):
        try:
            if x is None:return None
            v=float(x)
            return v if pd.notna(v) else None
        except:return None

    def PA_money(x):
        v=PA_num(x)
        if v is None:return "N/A"
        av=abs(v)
        if av>=1e12:return f"₹{v/1e12:,.2f}T"
        if av>=1e7:return f"₹{v/1e7:,.2f} Cr"
        if av>=1e5:return f"₹{v/1e5:,.2f}L"
        return f"₹{v:,.2f}"

    def PA_pct(x,decimal=True):
        v=PA_num(x)
        if v is None:return "N/A"
        if decimal and abs(v)<=2:v*=100
        return f"{v:.2f}%"

    def PA_val(info,*keys):
        for k in keys:
            v=info.get(k)
            if v is not None:return v
        return None

    def PA_statement(df,title):
        st.markdown(f"### {title}")
        if df is None or df.empty:
            st.info("Statement data is not available from the current market-data provider.")
            return
        x=df.copy()
        x.columns=[c.strftime("%b %Y") if hasattr(c,"strftime") else str(c) for c in x.columns]
        wanted=["Total Revenue","Operating Revenue","Gross Profit","Operating Income","EBIT","EBITDA","Pretax Income","Net Income","Basic EPS",
                "Total Assets","Current Assets","Cash Cash Equivalents And Short Term Investments","Total Liabilities Net Minority Interest","Current Liabilities","Stockholders Equity","Total Debt","Net Debt",
                "Operating Cash Flow","Investing Cash Flow","Financing Cash Flow","Free Cash Flow","Capital Expenditure"]
        keep=[i for i in wanted if i in x.index]
        if keep:x=x.loc[keep]
        x=x.iloc[:,:6]
        def fmt(v):
            try:
                if pd.isna(v):return "—"
                if abs(float(v))>=1e7:return f"{float(v)/1e7:,.2f} Cr"
                return f"{float(v):,.2f}"
            except:return str(v)
        st.dataframe(x.map(fmt) if hasattr(x,"map") else x.applymap(fmt),use_container_width=True)

    with st.spinner(f"Loading complete research for {symbol}..."):
        info,hist,qpl,apl,qbs,abs_,qcf,acf,major,inst=PA_bundle(ticker)

    last=PA_num(PA_val(info,"currentPrice","regularMarketPrice"))
    if last is None and not hist.empty:last=float(hist["Close"].dropna().iloc[-1])
    prev=PA_num(PA_val(info,"previousClose"))
    change=(last-prev) if last is not None and prev else None
    pct=(change/prev*100) if change is not None and prev else None
    name=PA_val(info,"longName","shortName") or symbol

    st.markdown(f"## {name}  ·  NSE: {symbol}")
    if last is not None:
        st.markdown(f"### ₹{last:,.2f} &nbsp; <span style='color:{'#22c55e' if (pct or 0)>=0 else '#ef4444'}'>{pct:+.2f}%</span>" if pct is not None else f"### ₹{last:,.2f}",unsafe_allow_html=True)

    tabs=st.tabs(["Overview","Chart","Analysis","Peers","Quarters","Profit & Loss","Balance Sheet","Cash Flow","Ratios","Investors","News"])

    with tabs[0]:
        vals=[
            ("Market Cap",PA_money(PA_val(info,"marketCap"))),
            ("Current Price",PA_money(last)),
            ("52W High / Low",f"{PA_money(PA_val(info,'fiftyTwoWeekHigh'))} / {PA_money(PA_val(info,'fiftyTwoWeekLow'))}"),
            ("Stock P/E",f"{PA_num(PA_val(info,'trailingPE')):.2f}" if PA_num(PA_val(info,'trailingPE')) is not None else "N/A"),
            ("Forward P/E",f"{PA_num(PA_val(info,'forwardPE')):.2f}" if PA_num(PA_val(info,'forwardPE')) is not None else "N/A"),
            ("Book Value",PA_money(PA_val(info,"bookValue"))),
            ("Price / Book",f"{PA_num(PA_val(info,'priceToBook')):.2f}" if PA_num(PA_val(info,'priceToBook')) is not None else "N/A"),
            ("Dividend Yield",PA_pct(PA_val(info,"dividendYield"))),
            ("ROE",PA_pct(PA_val(info,"returnOnEquity"))),
            ("ROA",PA_pct(PA_val(info,"returnOnAssets"))),
            ("Debt / Equity",f"{PA_num(PA_val(info,'debtToEquity')):.2f}" if PA_num(PA_val(info,'debtToEquity')) is not None else "N/A"),
            ("EPS",f"₹{PA_num(PA_val(info,'trailingEps')):.2f}" if PA_num(PA_val(info,'trailingEps')) is not None else "N/A"),
        ]
        for row in range(0,len(vals),4):
            cs=st.columns(4)
            for c,(lab,val) in zip(cs,vals[row:row+4]):c.metric(lab,val)
        l,r=st.columns([2,1])
        with l:
            st.markdown("### About")
            st.write(PA_val(info,"longBusinessSummary") or "Company description is unavailable from the current provider.")
        with r:
            st.markdown("### Company")
            st.write("**Sector:**",PA_val(info,"sector") or "N/A")
            st.write("**Industry:**",PA_val(info,"industry") or "N/A")
            st.write("**Employees:**",f"{int(PA_val(info,'fullTimeEmployees')):,}" if PA_val(info,"fullTimeEmployees") else "N/A")
            st.write("**Website:**",PA_val(info,"website") or "N/A")

    with tabs[1]:
        period=st.radio("Chart period",["1mo","3mo","6mo","1y","2y","5y"],index=3,horizontal=True,key="pa_chart_period")
        try:
            ch=yf.Ticker(ticker).history(period=period,auto_adjust=False)
            if not ch.empty:st.line_chart(ch["Close"],use_container_width=True)
            else:st.info("Chart data unavailable.")
        except Exception:st.info("Chart data unavailable.")

    with tabs[2]:
        st.markdown("### Strengths / Risks")
        pros=[];cons=[]
        pe=PA_num(PA_val(info,"trailingPE")); roe=PA_num(PA_val(info,"returnOnEquity")); de=PA_num(PA_val(info,"debtToEquity"))
        gm=PA_num(PA_val(info,"grossMargins")); om=PA_num(PA_val(info,"operatingMargins")); eg=PA_num(PA_val(info,"earningsGrowth")); rg=PA_num(PA_val(info,"revenueGrowth"))
        if roe is not None:
            (pros if roe>=.15 else cons).append(f"Return on equity is {roe*100:.1f}%.")
        if de is not None:
            (pros if de<=50 else cons).append(f"Debt-to-equity reported by the provider is {de:.1f}.")
        if rg is not None:
            (pros if rg>0 else cons).append(f"Revenue growth is {rg*100:.1f}%.")
        if eg is not None:
            (pros if eg>0 else cons).append(f"Earnings growth is {eg*100:.1f}%.")
        if om is not None and om>0:pros.append(f"Operating margin is {om*100:.1f}%.")
        if pe is not None and pe>60:cons.append(f"Trailing P/E is {pe:.1f}, indicating a relatively high earnings multiple.")
        if PA_num(PA_val(info,"dividendYield")) in (None,0):cons.append("No regular dividend yield is currently reported by the provider.")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("#### ✅ Strengths")
            if pros:
                for x in pros:st.write("•",x)
            else:st.write("No rule-based strength triggered from available fields.")
        with c2:
            st.markdown("#### ⚠️ Risks / Watch")
            if cons:
                for x in cons:st.write("•",x)
            else:st.write("No rule-based risk triggered from available fields.")
        st.caption("These are rule-based observations from available financial fields, not a buy/sell recommendation.")

    with tabs[3]:
        st.markdown("### Peers")
        sector=PA_val(info,"sector")
        peer_syms=[]
        if sector:
            # lightweight peer discovery from the app universe using cached ticker info
            for ps in _all_symbols[:120]:
                if ps==symbol:continue
                try:
                    pi=yf.Ticker(ps+".NS").info
                    if pi.get("sector")==sector:
                        peer_syms.append(ps)
                    if len(peer_syms)>=8:break
                except:pass
        if not peer_syms:st.info("Automatic peer discovery is unavailable for this stock.")
        else:
            pdata=[]
            for ps in peer_syms:
                try:
                    pi=yf.Ticker(ps+".NS").info
                    pdata.append({"Stock":ps,"Price":pi.get("currentPrice"),"Market Cap":pi.get("marketCap"),"P/E":pi.get("trailingPE"),"ROE %":(pi.get("returnOnEquity") or 0)*100})
                except:pass
            st.dataframe(pd.DataFrame(pdata),use_container_width=True,hide_index=True)

    with tabs[4]:
        st.markdown("### Quarterly Results")
        PA_statement(qpl,"Recent quarters")

    with tabs[5]:
        PA_statement(apl,"Annual Profit & Loss")

    with tabs[6]:
        PA_statement(abs_,"Annual Balance Sheet")

    with tabs[7]:
        PA_statement(acf,"Annual Cash Flow")

    with tabs[8]:
        st.markdown("### Valuation")
        rv=[
            ("P/E",PA_val(info,"trailingPE")),("Forward P/E",PA_val(info,"forwardPE")),("P/B",PA_val(info,"priceToBook")),
            ("EV/EBITDA",PA_val(info,"enterpriseToEbitda")),("PEG",PA_val(info,"pegRatio")),
            ("Profit Margin",PA_pct(PA_val(info,"profitMargins"))),("Operating Margin",PA_pct(PA_val(info,"operatingMargins"))),
            ("Gross Margin",PA_pct(PA_val(info,"grossMargins"))),("ROE",PA_pct(PA_val(info,"returnOnEquity"))),
            ("ROA",PA_pct(PA_val(info,"returnOnAssets"))),("Current Ratio",PA_val(info,"currentRatio")),("Quick Ratio",PA_val(info,"quickRatio")),
            ("Debt/Equity",PA_val(info,"debtToEquity")),("Revenue Growth",PA_pct(PA_val(info,"revenueGrowth"))),("Earnings Growth",PA_pct(PA_val(info,"earningsGrowth")))
        ]
        rdf=pd.DataFrame(rv,columns=["Ratio","Value"])
        st.dataframe(rdf,use_container_width=True,hide_index=True)

    with tabs[9]:
        st.markdown("### Shareholding Pattern")
        st.caption("Quarterly ownership. Official NSE filing data is attempted first; Yahoo data is used only as fallback.")
        sh=PA_nse_shareholding(symbol)
        if not sh.empty:
            latest=sh.iloc[-1]; previous=sh.iloc[-2] if len(sh)>1 else None
            boxes=st.columns(4)
            for box,col,label in zip(boxes,["FII","DII","Promoters","Public"],["FII","DII","Promoters","Public"]):
                v=latest.get(col)
                delta=None
                if previous is not None and pd.notna(v) and pd.notna(previous.get(col)):
                    delta=f"{float(v)-float(previous.get(col)):+.2f} pp"
                box.metric(label,f"{float(v):.2f}%" if pd.notna(v) else "N/A",delta)
            use=[c for c in ["Promoters","FII","DII","Government","Public","Others","Shareholders"] if c in sh and sh[c].notna().any()]
            table=sh.set_index("Period")[use].T
            disp=table.copy().astype(object)
            for rr in disp.index:
                for cc in disp.columns:
                    v=disp.loc[rr,cc]
                    if pd.isna(v):disp.loc[rr,cc]="—"
                    elif rr=="Shareholders":disp.loc[rr,cc]=f"{int(float(v)):,}"
                    else:disp.loc[rr,cc]=f"{float(v):.2f}%"
            st.dataframe(disp,use_container_width=True)
            if previous is not None:
                st.markdown("#### Latest-quarter ownership movement")
                for col,label in [("FII","FII"),("DII","DII"),("Promoters","Promoters"),("Public","Public")]:
                    a=latest.get(col);b=previous.get(col)
                    if pd.notna(a) and pd.notna(b):
                        d=float(a)-float(b)
                        st.write(f"{'🟢' if d>0 else '🔴' if d<0 else '⚪'} **{label}:** {d:+.2f} percentage points")
            st.caption("Source: NSE corporate shareholding-pattern feed.")
        else:
            st.warning("NSE quarterly shareholding data is temporarily unavailable for this symbol. Showing fallback holder data.")
            ih=PA_num(PA_val(info,"heldPercentInstitutions")); insider=PA_num(PA_val(info,"heldPercentInsiders"))
            x1,x2=st.columns(2);x1.metric("Institutions",PA_pct(ih));x2.metric("Insiders",PA_pct(insider))
            if inst is not None and not inst.empty:
                st.markdown("#### Institutional holders")
                st.dataframe(inst,use_container_width=True,hide_index=True)
            if major is not None and not major.empty:
                st.markdown("#### Major-holder summary")
                st.dataframe(major,use_container_width=True)
            st.caption("Fallback source: Yahoo Finance. The app does not invent quarterly FII/DII percentages when NSE data cannot be retrieved.")

    with tabs[10]:
        st.markdown("### Latest company news")
        try:
            news=yf.Ticker(ticker).news or []
        except Exception:news=[]
        if not news:st.info("No recent news returned by the current provider.")
        for n in news[:15]:
            c=n.get("content",n) if isinstance(n,dict) else {}
            title=c.get("title") or n.get("title","News")
            summary=c.get("summary") or ""
            provider=(c.get("provider") or {}).get("displayName","") if isinstance(c.get("provider"),dict) else ""
            st.markdown(f"**{title}**")
            if provider:st.caption(provider)
            if summary:st.write(summary)

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
                    f'<a class="pick-card pick-card-link" href="?page=pro&stock={r["Symbol"]}" target="_self">'
                    f'<span class="pick-badge">Score {int(r["Score"])}</span>'
                    f'<b>{r["Symbol"]}</b>'
                    f'<span>₹{r["Latest"]:.2f}</span>'
                    f'<small>1W {r["1W %"]:+.2f}% · 1M {r["1M %"]:+.2f}% · RSI {r["RSI14"]:.1f}</small>'
                    f'<small>{risk}</small>'
                    f'<small style="margin-top:10px;color:#67e8f9;font-weight:900">Click card → Full Pro Analysis</small>'
                    f'</a>',
                    unsafe_allow_html=True
                )

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
                st.session_state["pending_page"]="🧠 Pro Analyzer"
                st.rerun()
        st.download_button("⬇️ Download CSV",res.to_csv(index=False).encode(),name.replace(" ","_")+".csv","text/csv")


elif page=="📰 Stock News":
    st.markdown("<div class='hero'><div class='eyebrow'>FRESH CATALYST RADAR</div><h1>📰 Stock News & Event Radar</h1><p>Fresh Indian stock-market catalysts, newest first. General scan works even when the stock box is empty.</p></div>",unsafe_allow_html=True)

    @st.cache_data(ttl=180,show_spinner=False)
    def NEWS_rss(query,limit=100):
        import urllib.parse, xml.etree.ElementTree as ET
        from email.utils import parsedate_to_datetime
        from datetime import timezone
        url="https://news.google.com/rss/search?q="+urllib.parse.quote_plus(query)+"&hl=en-IN&gl=IN&ceid=IN:en"
        out=[]
        try:
            r=requests.get(url,timeout=15,headers={"User-Agent":"Mozilla/5.0"})
            root=ET.fromstring(r.content)
            for it in root.findall(".//item")[:limit]:
                pub=it.findtext("pubDate") or ""
                try:
                    dt=parsedate_to_datetime(pub)
                    if dt.tzinfo is None:dt=dt.replace(tzinfo=timezone.utc)
                    dt=dt.astimezone(timezone.utc)
                except:continue
                sn=it.find("source")
                out.append({"title":(it.findtext("title") or "").strip(),"link":(it.findtext("link") or "").strip(),
                            "source":((sn.text or "").strip() if sn is not None else "News"),"dt":dt})
        except Exception:pass
        return out

    def NEWS_tag(title):
        x=title.lower()
        rules=[
          ("🔴 Block/Bulk Deal",["block deal","bulk deal","stake sale","stake sell","offload"]),
          ("🟢 Order Win",["bags order","wins order","order win","receives order","contract win","letter of award","letter of acceptance"]),
          ("🟢 Government/Regulatory",["government approval","government approves","cabinet approval","cabinet approves","ministry approval","regulatory approval","sebi approval","rbi approval","dcgi approval"]),
          ("🟢 Corporate Action",["buyback","bonus issue","stock split","dividend","rights issue"]),
          ("🟣 Results",["quarterly results","q1 results","q2 results","q3 results","q4 results","profit rises","profit jumps","profit falls"]),
          ("🟡 M&A / Stake",["acquisition","acquires","merger","demerger","buys stake","stake purchase","mou"]),
          ("🔵 Brokerage",["brokerage","target price","jefferies","motilal oswal","nomura","ubs","goldman sachs","morgan stanley","upgrade","downgrade"]),
          ("⚠️ Legal/Negative",["penalty","fraud","probe","investigation","insolvency","default","court order","restriction"]),
        ]
        for lab,keys in rules:
            if any(k in x for k in keys):return lab
        return "📰 Market/Company News"

    def NEWS_age(dt):
        from datetime import datetime,timezone
        sec=max(0,(datetime.now(timezone.utc)-dt).total_seconds())
        if sec<3600:return f"{max(1,int(sec//60))} min ago"
        if sec<86400:return f"{int(sec//3600)} hr ago"
        return f"{int(sec//86400)} day(s) ago"

    def NEWS_hint(tag,title):
        x=title.lower()
        if "block/bulk" in tag:return "Watch supply, buyer/seller identity and deal price"
        if "order win" in tag:return "Potential business catalyst; compare order size with revenue"
        if "government" in tag:return "Regulatory/policy catalyst; verify effective date and conditions"
        if "corporate action" in tag:return "Corporate-action catalyst; check record/ex-date and terms"
        if "legal" in tag:return "Risk event; verify financial/material impact"
        if "downgrade" in x or "profit falls" in x:return "Potential negative catalyst"
        if "upgrade" in x or "profit jumps" in x:return "Potential positive catalyst"
        return "Read details before judging price impact"

    q1,q2,q3=st.columns([1.4,1,0.7])
    with q1: term=st.text_input("Stock / company / topic","",placeholder="Leave blank for all-market latest news")
    with q2: kind=st.selectbox("News type",["All","Block/Bulk Deals","Order Wins","Government/Regulatory","Results","Corporate Actions","Brokerage","M&A / Stake","Legal/Negative"])
    with q3: fresh=st.selectbox("Freshness",["Today / 24 Hours","3 Days","7 Days"],index=1)
    count=st.slider("Articles",10,60,30,10)

    from datetime import datetime,timezone,timedelta
    age_limit={"Today / 24 Hours":timedelta(hours=24),"3 Days":timedelta(days=3),"7 Days":timedelta(days=7)}[fresh]
    cutoff=datetime.now(timezone.utc)-age_limit

    # IMPORTANT: do not require all publisher names in one query. Run several broad feeds and merge.
    when={"Today / 24 Hours":"when:1d","3 Days":"when:3d","7 Days":"when:7d"}[fresh]
    base=(term.strip()+" NSE stock ") if term.strip() else "India NSE stocks "
    queries=[
        base+f"(block deal OR bulk deal OR order OR contract OR approval OR acquisition OR buyback OR dividend OR results) {when}",
        base+f"(Moneycontrol OR CNBC-TV18 OR NDTV Profit OR Reuters) {when}",
        base+f'("stocks to watch" OR "stock in focus" OR "market moving") {when}',
    ]
    all_items=[]
    with st.spinner("Loading fresh market catalysts..."):
        for qq in queries:all_items.extend(NEWS_rss(qq,100))

    # Merge, hard-filter dates locally, dedupe, newest first.
    seen=set(); items=[]
    for z in sorted(all_items,key=lambda a:a["dt"],reverse=True):
        if z["dt"]<cutoff:continue
        key=re.sub(r"[^a-z0-9]+"," ",z["title"].lower()).strip()
        if key in seen:continue
        seen.add(key)
        tag=NEWS_tag(z["title"])
        filters={"Block/Bulk Deals":"Block/Bulk","Order Wins":"Order Win","Government/Regulatory":"Government",
                 "Results":"Results","Corporate Actions":"Corporate Action","Brokerage":"Brokerage","M&A / Stake":"M&A","Legal/Negative":"Legal"}
        if kind!="All" and filters[kind].lower() not in tag.lower():continue
        z["tag"]=tag;items.append(z)
        if len(items)>=count:break

    st.markdown(f"### Latest market-moving news · {len(items)} headlines")
    st.caption(f"Showing only items published inside the selected {fresh} window, newest first. Event hints are not price predictions.")
    if not items:
        st.warning("No matching headlines were found for this exact filter. Try All or 7 Days. The page no longer shows old articles just to fill the list.")
    for z in items:
        title=z["title"].replace("<","&lt;").replace(">","&gt;")
        hint=NEWS_hint(z["tag"],z["title"])
        st.markdown(f"""<div style="border:1px solid rgba(120,160,210,.28);border-radius:14px;padding:14px 16px;margin:9px 0;background:rgba(15,42,72,.38)">
        <div style="font-size:12px;font-weight:800">{z['tag']} &nbsp; • &nbsp; {hint}</div>
        <div style="font-size:17px;font-weight:800;line-height:1.35;margin-top:5px">{title}</div>
        <div style="opacity:.72;font-size:13px;margin-top:6px">{z['source']} &nbsp; • &nbsp; {NEWS_age(z['dt'])}</div>
        <div style="margin-top:8px"><a href="{z['link']}" target="_blank">Open full story ↗</a></div></div>""",unsafe_allow_html=True)

    st.markdown("### What this radar is meant to catch")
    st.write("Block/bulk deals • large order wins • government/regulatory approvals • results • buybacks/dividends • acquisitions • brokerage actions • material company events")
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
    st.markdown("<div class='hero'><div class='eyebrow'>NSE PERFORMANCE</div><h1>🌐 All NSE Performance</h1><p>Start with market statistics, then explore heat maps, then choose Classic Table or Smart Scanner.</p></div>",unsafe_allow_html=True)

    st.markdown("## 📊 Market Statistics")
    official_stats=nse_market_statistics()

    if official_stats.get("source")=="NSE":
        total_traded=official_stats.get("stock_traded",0)
        advances=official_stats.get("advances",0)
        declines=official_stats.get("declines",0)
        unchanged=official_stats.get("unchanged",0)
        high52=official_stats.get("high52",0)
        low52=official_stats.get("low52",0)
        upper_circuit=official_stats.get("upper",0)
        lower_circuit=official_stats.get("lower",0)
        as_on=official_stats.get("as_on","Latest NSE update")
        st.caption(f"Official NSE Market Statistics · {as_on}")
    else:
        st.warning("Official NSE Market Statistics could not be fetched right now. I am not showing an estimated substitute, so the numbers will not mislead you.")
        total_traded=advances=declines=unchanged=high52=low52=upper_circuit=lower_circuit=0

    s1,s2,s3,s4=st.columns(4)
    s1.metric("Stock Traded",f"{total_traded:,}" if total_traded else "—")
    s2.metric("Advances",f"{advances:,}" if advances else "—")
    s3.metric("Declines",f"{declines:,}" if declines else "—")
    s4.metric("Unchanged",f"{unchanged:,}" if unchanged else "—")
    t1,t2,t3,t4=st.columns(4)
    t1.metric("52 Week High",f"{high52:,}" if high52 else "—")
    t2.metric("52 Week Low",f"{low52:,}" if low52 else "—")
    t3.metric("Upper Circuit",f"{upper_circuit:,}" if upper_circuit else "—")
    t4.metric("Lower Circuit",f"{lower_circuit:,}" if lower_circuit else "—")

    st.markdown("## 🟩 Heat Map")
    heat_mode=st.radio("Choose heat map",["Broad Market Indices","Sectoral Indices"],horizontal=True,key="heat_mode")

    def heat_color(v):
        try:x=float(v)
        except:x=0
        if x>=3:return "#08783e"
        if x>=1:return "#109b52"
        if x>0:return "#38b96b"
        if x<=-3:return "#a80f16"
        if x<=-1:return "#d01b2c"
        if x<0:return "#ef7a86"
        return "#64748b"

    all_idx=nse_all_indices()
    broad_names=[
        "NIFTY 50","NIFTY NEXT 50","NIFTY MIDCAP 50","NIFTY MIDCAP 100","NIFTY MIDCAP 150",
        "NIFTY SMLCAP 50","NIFTY SMLCAP 100","NIFTY SMLCAP 250","NIFTY MIDSMALLCAP 400",
        "NIFTY 100","NIFTY 200","NIFTY 500","NIFTY LARGEMIDCAP 250","NIFTY MID SELECT",
        "NIFTY TOTAL MARKET","NIFTY MICROCAP 250","NIFTY500 MULTICAP 50:25:25","NIFTY FPI 150",
        "NIFTY500 LARGE MID SMALL EQUAL-CAP WEIGHTED","NIFTY MIDSMALLCAP 400"
    ]
    sector_names=[
        "NIFTY AUTO","NIFTY BANK","NIFTY FINANCIAL SERVICES","NIFTY FINANCIAL SERVICES 25/50",
        "NIFTY FMCG","NIFTY IT","NIFTY MEDIA","NIFTY METAL","NIFTY PHARMA","NIFTY PSU BANK",
        "NIFTY PRIVATE BANK","NIFTY REALTY","NIFTY HEALTHCARE INDEX","NIFTY CONSUMER DURABLES",
        "NIFTY OIL & GAS","NIFTY MIDSMALL HEALTHCARE","NIFTY CHEMICALS","NIFTY500 HEALTHCARE",
        "NIFTY FINANCIAL SERVICES EX-BANK","NIFTY MIDSMALL FINANCIAL SERVICES",
        "NIFTY MIDSMALL IT & TELECOM","NIFTY CEMENT","NIFTY REITS & INVITS"
    ]
    tile_rows=_pick_nse_indices(all_idx,broad_names if heat_mode=="Broad Market Indices" else sector_names)

    if not tile_rows:
        st.warning("NSE index feed is temporarily unavailable.")
    else:
        st.caption(f"Official NSE index feed · {len(tile_rows)} {heat_mode.lower()} shown")
        cards=[]
        for row in tile_rows:
            name=row.get("name","")
            val=row.get("last")
            chg=row.get("pct")
            val_txt="—" if val is None else f"{val:,.2f}"
            chg_txt="—" if chg is None else f"{chg:+.2f}%"
            cards.append(
                f"<div class='nse-heat-card' style='background:{heat_color(chg)}'>"
                f"<div class='nse-heat-name'>{html.escape(name)}</div>"
                f"<div class='nse-heat-value'>{val_txt}</div>"
                f"<div class='nse-heat-change'>{chg_txt}</div>"
                f"</div>"
            )
        st.markdown("<div class='nse-heat-grid'>"+"".join(cards)+"</div>",unsafe_allow_html=True)

    st.markdown("## 📋 Stock Performance")
    view=st.radio("Choose view",["📋 Classic Table (Excel Style)","⚡ Smart Scanner"],horizontal=True,key="allnse_view")

    universe_group=st.selectbox(
        "Universe",
        ["NIFTY 50","NIFTY 100","NIFTY 200","NIFTY 500","NIFTY Midcap","NIFTY Smallcap","All NSE"],
        key="universe_group"
    )

    syms=universe()
    if universe_group=="NIFTY 50": use_syms=syms[:50]
    elif universe_group=="NIFTY 100": use_syms=syms[:100]
    elif universe_group=="NIFTY 200": use_syms=syms[:200]
    elif universe_group=="NIFTY 500": use_syms=syms[:500]
    elif universe_group=="NIFTY Midcap": use_syms=syms[100:250]
    elif universe_group=="NIFTY Smallcap": use_syms=syms[250:500]
    else: use_syms=syms

    if view=="📋 Classic Table (Excel Style)":
        st.markdown("### 📋 Classic Performance Table")
        c1,c2,c3=st.columns(3)
        history=c1.selectbox("History",["1y","2y","5y"],index=2,key="classic_history")
        sort_by=c2.selectbox("Sort by",["Symbol","Brokerage Call","Latest","1D %","1W %","1M %","3M %","6M %","1Y %","5Y %","RSI14","SMA20","SMA50","SMA200","52W High","52W Low","% of 52W High","Volume","Volume Ratio","Up Days 20"],index=2,key="classic_sort")
        order_options=["A → Z","Z → A"] if sort_by in ["Symbol","Brokerage Call"] else ["Largest → Smallest","Smallest → Largest"]
        order=c3.selectbox("Order",order_options,key="classic_order")

        if st.button("📊 Build / Refresh Classic Table",type="primary",use_container_width=True,key="classic_build"):
            with st.spinner(f"Loading {len(use_syms):,} stocks..."):
                st.session_state["classic_df"]=bulk_snapshot(tuple(use_syms),history)

        classic=st.session_state.get("classic_df")
        if isinstance(classic,pd.DataFrame) and not classic.empty:
            d=classic.copy()
            if sort_by=="Symbol":
                d=d.sort_values("Symbol",ascending=(order=="A → Z"),na_position="last")
            elif sort_by!="Brokerage Call" and sort_by in d.columns:
                d[sort_by]=pd.to_numeric(d[sort_by],errors="coerce")
                d=d.sort_values(sort_by,ascending=(order=="Smallest → Largest"),na_position="last")

            show_brokerage=st.checkbox("🔵 Check recent public brokerage calls",value=True,key="classic_brokerage")
            if show_brokerage:
                with st.spinner("Checking recent brokerage-call headlines..."):
                    broker_map=brokerage_tags_for_symbols(tuple(d["Symbol"].astype(str).tolist()))
                d["Brokerage Call"]=d["Symbol"].astype(str).map(broker_map).fillna("")
            else:
                d["Brokerage Call"]=""

            broker_choices=[
                "All Stocks","Only Stocks With Brokerage Calls","No Brokerage Call",
                "Jefferies","Motilal Oswal","ICICI Securities","HDFC Securities",
                "Axis Securities","CLSA","Nomura","Morgan Stanley","Goldman Sachs","JM Financial"
            ]
            broker_filter=st.selectbox("Brokerage filter",broker_choices,key="classic_broker_filter")
            if broker_filter=="Only Stocks With Brokerage Calls":
                d=d[d["Brokerage Call"].astype(str).str.strip()!=""]
            elif broker_filter=="No Brokerage Call":
                d=d[d["Brokerage Call"].astype(str).str.strip()==""]
            elif broker_filter!="All Stocks":
                d=d[d["Brokerage Call"].astype(str).str.contains(broker_filter,case=False,na=False)]

            # Re-apply selected sort after brokerage tagging/filtering.
            if sort_by in ["Symbol","Brokerage Call"]:
                d=d.sort_values(sort_by,ascending=(order=="A → Z"),na_position="last")
            elif sort_by in d.columns:
                d[sort_by]=pd.to_numeric(d[sort_by],errors="coerce")
                d=d.sort_values(sort_by,ascending=(order=="Smallest → Largest"),na_position="last")

            d=d.reset_index(drop=True)
            d.insert(0,"S.No",range(1,len(d)+1))

            cols_show=["S.No","Symbol","Latest","1D %","1W %","1M %","3M %","6M %","1Y %","5Y %","RSI14","SMA20","SMA50","SMA200","52W High","52W Low","% of 52W High","Volume","Volume Ratio","Up Days 20","Brokerage Call"]
            cols_show=[c for c in cols_show if c in d.columns]
            classic_display=clean_display(d[cols_show])
            if "Brokerage Call" in classic_display.columns:
                def _broker_row_style(row):
                    has_call=bool(str(row.get("Brokerage Call","")).strip())
                    return ["background-color:#dbeafe;color:#0f172a;font-weight:700" if has_call else "" for _ in row]
                styled=classic_display.style.apply(_broker_row_style,axis=1)
                st.dataframe(styled,use_container_width=True,height=700,hide_index=True)
                st.caption("🔵 Blue row = recent public brokerage-call headline detected. The final column shows the brokerage name(s).")
            else:
                st.dataframe(classic_display,use_container_width=True,height=700,hide_index=True)

            st.markdown("### 🧠 Inspect a Candidate")
            a1,a2=st.columns([3,1])
            selected=a1.selectbox("Select stock for full analysis",d["Symbol"].astype(str).tolist(),key="classic_selected")
            if a2.button("Open Pro Analyzer →",type="primary",use_container_width=True,key="classic_open"):
                st.query_params.clear();st.query_params["page"]="pro";st.query_params["stock"]=selected;st.rerun()
            st.download_button("⬇️ Export Classic Table CSV",d[cols_show].to_csv(index=False).encode(),"nse_classic_performance.csv","text/csv")

    else:
        st.markdown("### ⚡ Smart Scanner")
        f1,f2,f3,f4=st.columns(4)
        history=f1.selectbox("History",["1y","2y","5y"],index=2,key="smart_history")
        rank_by=f2.selectbox("Rank by",["1D %","1W %","1M %","3M %","6M %","1Y %","5Y %","RSI14","% of 52W High","Volume"],index=2,key="smart_rank")
        direction=f3.selectbox("Direction",["Highest first","Lowest first"],key="smart_direction")
        min_price=f4.number_input("Minimum price ₹",min_value=0.0,value=20.0,step=10.0,key="smart_price")

        g1,g2,g3=st.columns(3)
        min_volume=g1.number_input("Minimum volume",min_value=0,value=100000,step=50000,key="smart_volume")
        rsi_zone=g2.selectbox("RSI filter",["All","40–60 Balanced","50–70 Momentum","60–75 Strong","Below 35 Oversold","Above 75 Overbought"],key="smart_rsi")
        trend_filter=g3.selectbox("Trend filter",["All","Price > SMA20","Price > SMA50","SMA20 > SMA50","SMA50 > SMA200","Price > SMA20 > SMA50"],key="smart_trend")

        if st.button("⚡ Scan NSE Market",type="primary",use_container_width=True,key="smart_scan"):
            with st.spinner("Scanning selected universe..."):
                d=bulk_snapshot(tuple(use_syms),history)

            if isinstance(d,pd.DataFrame) and not d.empty:
                for col in ["Latest","1D %","1W %","1M %","3M %","6M %","1Y %","5Y %","RSI14","SMA20","SMA50","SMA200","52W High","52W Low","% of 52W High","Volume"]:
                    if col in d.columns:d[col]=pd.to_numeric(d[col],errors="coerce")

                if "Latest" in d.columns:d=d[d["Latest"]>=min_price]
                if "Volume" in d.columns:d=d[d["Volume"]>=min_volume]

                if rsi_zone!="All":
                    if rsi_zone=="40–60 Balanced":d=d[d["RSI14"].between(40,60)]
                    elif rsi_zone=="50–70 Momentum":d=d[d["RSI14"].between(50,70)]
                    elif rsi_zone=="60–75 Strong":d=d[d["RSI14"].between(60,75)]
                    elif rsi_zone=="Below 35 Oversold":d=d[d["RSI14"]<35]
                    elif rsi_zone=="Above 75 Overbought":d=d[d["RSI14"]>75]

                if trend_filter!="All":
                    if trend_filter=="Price > SMA20":d=d[d["Latest"].gt(d["SMA20"])]
                    elif trend_filter=="Price > SMA50":d=d[d["Latest"].gt(d["SMA50"])]
                    elif trend_filter=="SMA20 > SMA50":d=d[d["SMA20"].gt(d["SMA50"])]
                    elif trend_filter=="SMA50 > SMA200":d=d[d["SMA50"].gt(d["SMA200"])]
                    elif trend_filter=="Price > SMA20 > SMA50":d=d[d["Latest"].gt(d["SMA20"]) & d["SMA20"].gt(d["SMA50"])]

                d=d.sort_values(rank_by,ascending=(direction=="Lowest first"),na_position="last")
                d=d.reset_index(drop=True)
                d.insert(0,"S.No",range(1,len(d)+1))
                st.dataframe(clean_display(d),use_container_width=True,height=620,hide_index=True)

                st.markdown("### 🧠 Inspect a Candidate")
                a1,a2=st.columns([3,1])
                selected=a1.selectbox("Select stock for full analysis",d["Symbol"].astype(str).tolist(),key="smart_selected")
                if a2.button("Open Pro Analyzer →",type="primary",use_container_width=True,key="smart_open"):
                    st.query_params.clear();st.query_params["page"]="pro";st.query_params["stock"]=selected;st.rerun()
                st.download_button("⬇️ Export Smart Scan CSV",d.to_csv(index=False).encode(),"nse_smart_scan.csv","text/csv")
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
