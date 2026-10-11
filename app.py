
import io, re, html, requests, numpy as np, pandas as pd, streamlit as st, yfinance as yf
import json
import time
import logging
import threading
from contextlib import contextmanager
import streamlit.components.v1 as components
from datetime import date, datetime
from datetime import timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import gspread
import requests
import plotly.graph_objects as go
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

st.set_page_config(page_title="NSE Pro Market Terminal V14", page_icon="📈", layout="wide")



@contextmanager
def loading_stopwatch(message):
    """Live browser timer during blocking work; final elapsed time uses server clock."""
    started=time.perf_counter();slot=st.empty();completed=False
    with slot.container():
        components.html("""<div style="font:13px system-ui;color:#f8fafc;padding:4px 0">
        ⏱ <span>"""+html.escape(str(message))+"""</span> · <b id="elapsed">00:00</b></div>
        <script>const start=performance.now();
        const tick=()=>{const seconds=Math.floor((performance.now()-start)/1000);
        document.getElementById('elapsed').textContent=String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0');};
        tick();setInterval(tick,250);</script>""",height=32)
    try:
        yield
        completed=True
    finally:
        elapsed=time.perf_counter()-started
        slot.empty()
        if completed:slot.caption(f'✓ {message} Finished in {elapsed:.1f} seconds.')
        else:slot.caption(f'Loading stopped after {elapsed:.1f} seconds.')


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

MARKET_CACHE_TAB="NSE Price Cache"
MARKET_CACHE_HEADER=["Symbol","Last Price Date","Last Checked IST","Close History 1","Close History 2","Recent High Low Volume","Format"]
MARKET_CACHE_COLUMNS=list(range(1,8))

@st.cache_resource(show_spinner=False)
def market_cache_worksheet():
    """Use a separate tab in the configured workbook; never touch transaction tabs."""
    sheet_id=str(st.secrets.get("market_sheet_id","")).strip()
    account=st.secrets.get("gcp_service_account")
    if not sheet_id or not account:
        return None
    client=gspread.service_account_from_dict(dict(account))
    book=client.open_by_key(sheet_id)
    try:
        tab=book.worksheet(MARKET_CACHE_TAB)
    except gspread.WorksheetNotFound:
        tab=book.add_worksheet(title=MARKET_CACHE_TAB,rows=4000,cols=7)
    if tab.acell("A1").value!="Symbol":
        tab.update(values=[MARKET_CACHE_HEADER],range_name="A1:G1",raw=True)
    return tab

def market_cache_state():
    if "shared_nse_price_cache" not in st.session_state:
        st.session_state.shared_nse_price_cache={"loaded":False,"records":{},"positions":{},"sheet":None,"next_row":2}
    state=st.session_state.shared_nse_price_cache
    if state["loaded"]:
        return state
    try:
        tab=market_cache_worksheet()
        state["sheet"]=tab
        if tab is not None:
            sheet_values=tab.get_all_values()
            state["next_row"]=len(sheet_values)+1
            for row_number,values in enumerate(sheet_values[1:],start=2):
                if not values or not values[0].strip():
                    continue
                symbol=values[0].strip().upper()
                values=(values+[""]*7)[:7]
                try:
                    if values[6]!="v1":
                        continue
                    closes=json.loads(values[3])+json.loads(values[4])
                    recent=json.loads(values[5])
                    state["records"][symbol]={"closes":closes,"recent":recent,
                                               "last_date":values[1],"checked":values[2]}
                    state["positions"][symbol]=row_number
                except (ValueError,TypeError):
                    continue
        else:
            st.info("Shared NSE cache is using this session only. Set market_sheet_id and gcp_service_account in Streamlit secrets to save it to Google Sheets.")
    except Exception as error:
        st.warning(f"NSE Sheet cache unavailable; using this session only: {error}")
    state["loaded"]=True
    return state

def market_cache_row(symbol,record):
    closes=record["closes"]
    return [symbol,record["last_date"],record["checked"],
            json.dumps(closes[:650],separators=(",",":")),
            json.dumps(closes[650:],separators=(",",":")),
            json.dumps(record["recent"],separators=(",",":")),"v1"]

def market_cache_save(state,changed):
    tab=state["sheet"]
    if tab is None or not changed:
        return
    existing=[];new=[]
    for symbol in changed:
        row=market_cache_row(symbol,state["records"][symbol])
        if symbol in state["positions"]:
            position=state["positions"][symbol]
            existing.append({"range":f"A{position}:G{position}","values":[row]})
        else:
            new.append((symbol,row))
    try:
        for start in range(0,len(existing),40):
            tab.batch_update(existing[start:start+40],value_input_option="RAW")
        for start in range(0,len(new),40):
            batch=new[start:start+40]
            tab.append_rows([row for _,row in batch],value_input_option="RAW")
            next_row=state["next_row"]
            for offset,(symbol,_) in enumerate(batch):
                state["positions"][symbol]=next_row+offset
            state["next_row"]+=len(batch)
    except Exception as error:
        st.warning(f"Recent prices are visible, but saving them to Google Sheets failed: {error}")

def market_cache_frame(download,symbol,ticker,batch_size):
    if download is None or download.empty:
        return pd.DataFrame()
    try:
        if isinstance(download.columns,pd.MultiIndex):
            if ticker in download.columns.get_level_values(0):
                return download[ticker]
            return download.xs(ticker,axis=1,level=1)
        if batch_size==1:
            return download
    except (KeyError,ValueError):
        pass
    return pd.DataFrame()

@st.cache_resource(show_spinner=False)
def price_request_state():
    return {'lock':threading.Lock(),'until':0.0,'last':0.0,'classic':{}}

class PriceRateLimited(Exception):pass

class PriceLimitLog(logging.Handler):
    def __init__(self):super().__init__();self.limited=False
    def emit(self,record):
        message=record.getMessage().lower()
        if '429' in message or 'rate limit' in message or 'too many requests' in message:self.limited=True

def limited_price_download(tickers,**options):
    state=price_request_state()
    with state['lock']:
        if time.monotonic()<state['until']:raise PriceRateLimited('Price requests paused for five minutes after rate limiting.')
        delay=1.0-(time.monotonic()-state['last'])
        if delay>0:time.sleep(delay)
        handler=PriceLimitLog();logger=logging.getLogger('yfinance');logger.addHandler(handler)
        try:
            result=yf.download(tickers,threads=4,timeout=15,**options)
        except Exception as error:
            if any(text in str(error).lower() for text in ['429','rate limit','too many requests']):handler.limited=True
            if handler.limited:state['until']=time.monotonic()+300
            raise
        finally:
            logger.removeHandler(handler);state['last']=time.monotonic()
        if handler.limited:state['until']=time.monotonic()+300
        return result,handler.limited

def market_cache_fetch(symbols,start=None):
    result={}
    for offset in range(0,len(symbols),70):
        batch=symbols[offset:offset+70];tickers=[symbol+'.NS' for symbol in batch]
        opts={'start':start} if start else {'period':'5y'}
        try:
            downloaded,limited=limited_price_download(tickers,interval='1d',group_by='ticker',auto_adjust=False,progress=False,**opts)
        except Exception:
            break
        for symbol,ticker in zip(batch,tickers):
            frame=market_cache_frame(downloaded,symbol,ticker,len(batch))
            if not frame.empty and 'Close' in frame:result[symbol]=frame
        if limited or not result:break
    return result

def market_cache_merge(previous,frame,checked):
    close_by_date={str(day):float(value) for day,value in (previous or {}).get("closes",[])}
    recent_by_date={str(day):[float(high),float(low),int(volume)] for day,high,low,volume
                    in (previous or {}).get("recent",[])}
    for index,row in frame.iterrows():
        try:
            day=pd.Timestamp(index).date().isoformat()
            close=float(row["Close"])
            if not np.isfinite(close) or close<=0:
                continue
            close_by_date[day]=round(close,4)
            high=float(row.get("High",close));low=float(row.get("Low",close))
            volume=float(row.get("Volume",0))
            recent_by_date[day]=[round(high,4) if np.isfinite(high) else close,
                                 round(low,4) if np.isfinite(low) else close,
                                 int(volume) if np.isfinite(volume) else 0]
        except (ValueError,TypeError,KeyError):
            continue
    days=sorted(close_by_date)[-1261:]
    if not days:
        return previous
    recent_days=[day for day in sorted(recent_by_date) if day in close_by_date][-260:]
    return {"closes":[[day,close_by_date[day]] for day in days],
            "recent":[[day,*recent_by_date[day]] for day in recent_days],
            "last_date":days[-1],"checked":checked}

def market_cache_metrics(symbol,record):
    close=pd.Series([value for _,value in record["closes"]],dtype=float)
    if close.empty:
        return None
    recent=record["recent"]
    high=pd.Series([row[1] for row in recent],dtype=float)
    low=pd.Series([row[2] for row in recent],dtype=float)
    vol=pd.Series([row[3] for row in recent],dtype=float)
    latest=float(close.iloc[-1])
    hi52=float(high.tail(252).max()) if not high.empty else np.nan
    lo52=float(low.tail(252).min()) if not low.empty else np.nan
    delta=close.diff()
    gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False).mean()
    loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
    rs=gain/loss.replace(0,np.nan)
    volume=float(vol.iloc[-1]) if not vol.empty else 0
    volume_average=float(vol.tail(20).mean()) if len(vol)>=5 else np.nan
    return {"Symbol":symbol,"Latest":latest,"1D %":pct(close,1),"1W %":pct(close,5),
            "1M %":pct(close,21),"3M %":pct(close,63),"6M %":pct(close,126),
            "1Y %":pct(close,252),"5Y %":pct(close,1260),
            "RSI14":float((100-100/(1+rs)).iloc[-1]) if len(close)>=15 else np.nan,
            "SMA20":float(close.tail(20).mean()) if len(close)>=20 else np.nan,
            "SMA50":float(close.tail(50).mean()) if len(close)>=50 else np.nan,
            "SMA200":float(close.tail(200).mean()) if len(close)>=200 else np.nan,
            "52W High":hi52,"52W Low":lo52,
            "% of 52W High":latest/hi52*100 if hi52 else np.nan,
            "Volume":int(volume),
            "Volume Ratio":volume/volume_average if volume_average and np.isfinite(volume_average) else np.nan,
            "Up Days 20":int((close.diff().tail(20)>0).sum())}

def shared_market_snapshot(symbols,force_refresh=False):
    state=market_cache_state()
    symbols=list(dict.fromkeys(str(symbol).strip().upper() for symbol in symbols if symbol))
    checked=datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat()
    missing=[symbol for symbol in symbols if symbol not in state["records"]]
    stale=[symbol for symbol in symbols if symbol in state["records"] and
           (force_refresh or state["records"][symbol]["checked"]!=checked)]
    changed=[]
    for symbol,frame in market_cache_fetch(missing).items():
        record=market_cache_merge(None,frame,checked)
        if record:
            state["records"][symbol]=record;changed.append(symbol)
    # Existing symbols fetch only the latest few days. Group by saved date so
    # every Yahoo batch can share one start date and one network request.
    groups={}
    for symbol in stale:
        last=state["records"][symbol]["last_date"]
        start=(date.fromisoformat(last)-timedelta(days=5)).isoformat()
        groups.setdefault(start,[]).append(symbol)
    for start,group in groups.items():
        fresh=market_cache_fetch(group,start=start)
        for symbol in group:
            old=state["records"][symbol]
            record=market_cache_merge(old,fresh[symbol],checked) if symbol in fresh else dict(old,checked=checked)
            state["records"][symbol]=record;changed.append(symbol)
    market_cache_save(state,changed)
    rows=[]
    for symbol in symbols:
        record=state["records"].get(symbol)
        if record:
            metrics=market_cache_metrics(symbol,record)
            if metrics:rows.append(metrics)
    return pd.DataFrame(rows)

def classic_period_snapshot(symbols_tuple,period):
    """Reuse saved per-period records and stop requests on rate limiting."""
    symbols=list(dict.fromkeys(symbols_tuple));state=price_request_state()
    saved=state['classic'].setdefault(period,{})
    now=time.monotonic();todo=[symbol for symbol in symbols if symbol not in saved or now-saved[symbol]['saved_at']>=900]
    checked=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat()
    progress=st.progress(0);status=st.empty();notice='';empty_batches=0
    try:
        for offset in range(0,len(todo),70):
            batch=todo[offset:offset+70];tickers=[symbol+'.NS' for symbol in batch]
            try:
                downloaded,limited=limited_price_download(tickers,period=period,interval='1d',group_by='ticker',auto_adjust=False,progress=False)
            except Exception as error:
                notice='Price downloads stopped. Showing saved data where available. '+str(error);break
            available=0
            for symbol,ticker in zip(batch,tickers):
                frame=market_cache_frame(downloaded,symbol,ticker,len(batch))
                record=market_cache_merge(None,frame,checked) if not frame.empty else None
                if record:
                    saved[symbol]={'record':record,'saved_at':time.monotonic()};available+=1
            done=min(offset+len(batch),len(todo));progress.progress(done/max(len(todo),1))
            status.caption(f'Prices checked: {done:,}/{len(todo):,} · saved results retained')
            empty_batches=empty_batches+1 if available==0 else 0
            if limited:
                notice='Price service rate-limited requests. Downloads paused for five minutes; saved prices are shown.';break
            if empty_batches>=2:
                notice='Two batches returned no prices. Downloads stopped; saved prices are shown.';break
    finally:progress.empty();status.empty()
    rows=[];failed=[]
    for symbol in symbols:
        entry=saved.get(symbol)
        if not entry:failed.append(symbol);continue
        row=market_cache_metrics(symbol,entry['record'])
        if row:
            if period!='5y':row['5Y %']=np.nan
            row['Price Date']=entry['record']['last_date'];rows.append(row)
    st.session_state['classic_load_notice']=notice
    return pd.DataFrame(rows),failed


def bulk_snapshot(symbols_tuple,period="5y",force_refresh=False):
    # Keep the old caller interface. Shorter history still uses the same
    # stored 5-year series; only its selected output columns are displayed.
    return shared_market_snapshot(symbols_tuple,force_refresh=force_refresh)

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

def _nse_statistics_count(value):
    if value is None or isinstance(value, bool):
        return None
    text = str(value).strip().replace(",", "")
    if not re.fullmatch(r"[0-9]+(?:\.0+)?", text):
        return None
    return int(float(text))


def _parse_nse_market_statistics(payload):
    """Parse the exact fields used by NSE's current homepage component."""
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    if not isinstance(data, dict):
        return {"source": "Unavailable", "error": "Unexpected NSE response format."}
    mapping = {
        "stock_traded": ("snapshotCapitalMarket", "total"),
        "advances": ("snapshotCapitalMarket", "advances"),
        "declines": ("snapshotCapitalMarket", "declines"),
        "unchanged": ("snapshotCapitalMarket", "unchange"),
        "high52": ("fiftyTwoWeek", "high"),
        "low52": ("fiftyTwoWeek", "low"),
        "upper": ("circuit", "upper"),
        "lower": ("circuit", "lower"),
    }
    out = {}
    for key, (section, field) in mapping.items():
        values = data.get(section, {})
        out[key] = _nse_statistics_count(values.get(field)) if isinstance(values, dict) else None
    if all(out[k] is None for k in mapping):
        return {"source": "Unavailable", "error": "NSE returned no statistics."}
    out.update(source="NSE", as_on=str(data.get("asOnDate") or data.get("timestamp") or "Timestamp not supplied"))
    return out


@st.cache_data(ttl=60, show_spinner=False)
def nse_market_statistics():
    """Read NSE's JSON feed instead of its JavaScript-rendered HTML placeholders."""
    try:
        with requests.Session() as session:
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json,text/plain,*/*",
                "Referer": "https://www.nseindia.com/",
            })
            session.get("https://www.nseindia.com/", timeout=(5, 10))
            response = session.get(
                "https://www.nseindia.com/api/NextApi/apiClient",
                params={"functionName": "getMarketStatistics"}, timeout=(5, 15),
            )
            response.raise_for_status()
            return _parse_nse_market_statistics(response.json())
    except requests.exceptions.HTTPError as exc:
        return {"source": "Unavailable", "error": f"NSE returned HTTP {exc.response.status_code}."}
    except requests.exceptions.Timeout:
        return {"source": "Unavailable", "error": "NSE request timed out."}
    except Exception as exc:
        return {"source": "Unavailable", "error": f"NSE request failed ({type(exc).__name__})."}


def _nse_stat_display(value):
    return "—" if value is None else f"{value:,}"

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

# Separate NSE circuit scanner: never infer circuit status from percentage alone.
def circuit_csv(content):
    d=pd.read_csv(io.BytesIO(content))
    d.columns=[str(c).strip().upper() for c in d.columns]
    for c in d.select_dtypes(include='object'):
        d[c]=d[c].astype(str).str.strip()
    return d


def circuit_join_reports(bhav,bands,hitters,day):
    required={'SYMBOL','SERIES','PREV_CLOSE','CLOSE_PRICE','HIGH_PRICE','LOW_PRICE','TTL_TRD_QNTY'}
    if not required.issubset(bhav.columns): raise ValueError('Closing report format changed')
    if not {'SYMBOL','SERIES','BAND'}.issubset(bands.columns): raise ValueError('Band report format changed')
    if not {'SYMBOL','SERIES','HIGH/LOW'}.issubset(hitters.columns): raise ValueError('Band-hitter report format changed')
    b=bands.drop_duplicates(['SYMBOL','SERIES'])
    d=bhav.merge(b,on=['SYMBOL','SERIES'],how='inner',validate='many_to_one')
    for c in ['PREV_CLOSE','CLOSE_PRICE','HIGH_PRICE','LOW_PRICE','TTL_TRD_QNTY']:
        d[c]=pd.to_numeric(d[c],errors='coerce')
    d=d[d.TTL_TRD_QNTY.gt(0)&d.PREV_CLOSE.gt(0)&d.CLOSE_PRICE.gt(0)]
    d['Band %']=pd.to_numeric(d.BAND.astype(str).str.replace('%','',regex=False),errors='coerce')
    upper=set(map(tuple,hitters.loc[hitters['HIGH/LOW'].eq('H'),['SYMBOL','SERIES']].values))
    lower=set(map(tuple,hitters.loc[hitters['HIGH/LOW'].eq('L'),['SYMBOL','SERIES']].values))
    records=[]
    for _,r in d.iterrows():
        key=(r.SYMBOL,r.SERIES)
        fixed=pd.notna(r['Band %']) and r['Band %'] in [2,5,10,20]
        dynamic=str(r.BAND).lower().replace(' ','') in ['noband','no-band']
        if not (fixed or dynamic): continue
        for side,keys,extreme in [('Upper',upper,r.HIGH_PRICE),('Lower',lower,r.LOW_PRICE)]:
            if key not in keys: continue
            # Report explicitly confirms an intraday band hit; compare official close to extreme.
            closed=bool(np.isclose(r.CLOSE_PRICE,extreme,rtol=0,atol=0.005))
            records.append({'Date':day.isoformat(),'Symbol':r.SYMBOL,'Series':r.SERIES,
                'Company':r.get('SECURITY NAME',r.SYMBOL),'Band %':r['Band %'],
                'Type':'Fixed' if fixed else 'Dynamic','Direction':side,
                'Close (₹)':r.CLOSE_PRICE,'Change %':(r.CLOSE_PRICE/r.PREV_CLOSE-1)*100,
                'Status':('Closed at circuit' if closed else 'Touched only') if fixed else 'Dynamic boundary touched',
                'Volume':r.TTL_TRD_QNTY})
    columns=['Date','Symbol','Series','Company','Band %','Type','Direction','Close (₹)','Change %','Status','Volume']
    return pd.DataFrame(records,columns=columns)

def circuit_parse_reports(day, bodies):
    import zipfile
    stamp=day.strftime('%d%m%Y')
    bhav=circuit_csv(bodies[0]); bands=circuit_csv(bodies[1])
    if 'DATE1' not in bhav.columns:
        raise ValueError('Closing CSV is missing DATE1; use Full Bhavcopy and Security Deliverable data.')
    dates=pd.to_datetime(bhav['DATE1'],format='%d-%b-%Y',errors='coerce').dt.date
    if dates.dropna().empty or not dates.dropna().eq(day).all():
        raise ValueError('Closing report date does not match the selected date.')
    with zipfile.ZipFile(io.BytesIO(bodies[2])) as archive:
        accepted={f'bh{stamp}.csv',f'bh{day.strftime("%d%m%y")}.csv'}
        filename=next((n for n in archive.namelist() if n.replace('\\','/').split('/')[-1].lower() in accepted),None)
        if filename is None:
            raise ValueError('PR archive has no dated band-hitter CSV (bh'+stamp+'.csv).')
        hitters=circuit_csv(archive.read(filename))
    return {'rows':circuit_join_reports(bhav,bands,hitters,day),'coverage':len(bhav),'date':day.isoformat()}


@st.cache_data(ttl=900,show_spinner=False)
def circuit_day_report(day):
    stamp=day.strftime('%d%m%Y')
    paths=[f'products/content/sec_bhavdata_full_{stamp}.csv',
           f'content/equities/sec_list_{stamp}.csv',
           f'archives/equities/bhavcopy/pr/PR{day.strftime("%d%m%y")}.zip']
    labels=['Closing report','Price-band list','PR band-hitter archive']
    bodies=[]
    with requests.Session() as session:
        session.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36',
            'Accept':'*/*','Accept-Language':'en-US,en;q=0.9','Referer':'https://www.nseindia.com/all-reports'})
        warmed=False
        for path,label in zip(paths,labels):
            errors=[];body=None
            for attempt in range(2):
                if attempt and not warmed:
                    try: session.get('https://www.nseindia.com/all-reports',timeout=(5,8))
                    except requests.RequestException: pass
                    warmed=True
                try:
                    response=session.get('https://nsearchives.nseindia.com/'+path,timeout=(5,20))
                    response.raise_for_status()
                    content=response.content
                    if not content or content.lstrip().lower().startswith((b'<!doctype html',b'<html')):
                        raise ValueError('NSE returned an empty page or HTML instead of a report')
                    body=content;break
                except (requests.RequestException,ValueError) as exc:
                    errors.append(str(exc))
            if body is None:
                raise RuntimeError(f'{label} for {day:%d %b %Y} failed: {errors[-1]}')
            bodies.append(body)
    return circuit_parse_reports(day,bodies)


@st.cache_data(ttl=3600,show_spinner=False)
def circuit_holidays():
    # Holiday feed is optional: unknown missing weekdays stop verification.
    try:
        s=requests.Session();s.headers.update(HEADERS)
        s.get('https://www.nseindia.com/',timeout=(5,8))
        r=s.get('https://www.nseindia.com/api/holiday-master?type=trading',timeout=(5,12));r.raise_for_status()
        return {pd.to_datetime(x['tradingDate'],format='%d-%b-%Y').date() for x in r.json().get('CM',[])}
    except Exception: return set()


def circuit_streaks(current,history,limit_reached=False):
    out=current.copy(); labels=[]
    for _,r in out.iterrows():
        count=1; uncertain=False; bounded=True
        for day,report in history:
            if report is None: uncertain=True;bounded=False;break
            rows=report['rows']
            match=rows[(rows.Symbol==r.Symbol)&(rows.Series==r.Series)&(rows.Direction==r.Direction)&
                       (rows.Type=='Fixed')&(rows.Status=='Closed at circuit')]
            if match.empty: bounded=False;break
            count+=1
        if uncertain: label=f'{count}+ (earlier data unavailable)'
        elif bounded and limit_reached: label=f'{count}+ (scan limit)'
        else: label=str(count)
        labels.append(label)
    out['Consecutive trading days']=labels
    return out


def circuit_move_date(amount):
    today=datetime.now(ZoneInfo('Asia/Kolkata')).date()
    current=st.session_state.get('circuit_date',today)
    st.session_state['circuit_date']=min(current+timedelta(days=amount),today)
    st.session_state.pop('circuit_result',None)


@st.cache_data(ttl=60,show_spinner=False)
def circuit_live_snapshot():
    with requests.Session() as session:
        session.headers.update(HEADERS)
        session.get('https://www.nseindia.com/',timeout=(5,8))
        r=session.get('https://www.nseindia.com/api/live-analysis-price-band-hitter',timeout=(5,15))
        r.raise_for_status();payload=r.json()
    records=[]; timestamps=[]
    for key,side in [('upper','Upper'),('lower','Lower')]:
        section=payload.get(key,{}).get('AllSec',{})
        if section.get('timestamp'):timestamps.append(section['timestamp'])
        for x in section.get('data',[]):
            band=pd.to_numeric(x.get('priceBand'),errors='coerce')
            ltp=pd.to_numeric(x.get('ltp'),errors='coerce')
            extreme=pd.to_numeric(x.get('highPrice' if side=='Upper' else 'lowPrice'),errors='coerce')
            if pd.isna(ltp) or pd.isna(band):continue
            # Official hitter feed plus LTP at the reported extreme; not a final close.
            if not np.isclose(ltp,extreme,rtol=0,atol=0.005):continue
            records.append({'Symbol':x.get('symbol'),'Series':x.get('series'),
                'Reported band %':band,'Direction':side,'Latest (₹)':ltp,
                'Change %':pd.to_numeric(x.get('pChange'),errors='coerce'),
                'Status':'Currently at reported boundary (not final close)'})
    if not timestamps:raise ValueError('Missing exchange timestamp')
    stamps=pd.to_datetime(timestamps,format='%d-%b-%Y %H:%M:%S',errors='coerce')
    if stamps.isna().any():raise ValueError('Invalid exchange timestamp')
    return pd.DataFrame(records,columns=['Symbol','Series','Reported band %','Direction','Latest (₹)','Change %','Status']),stamps.min().to_pydatetime()


def render_circuit_live(today):
    with st.expander('📡 Today — current boundary snapshot',expanded=False):
        st.caption('Separate from final closing streaks. This feed can be delayed and does not confirm trading is halted or a dynamic range was expanded.')
        if st.button('Refresh current boundary snapshot',key='circuit_live_refresh'):
            circuit_live_snapshot.clear()
            try:
                frame,stamp=circuit_live_snapshot()
                st.session_state['circuit_live']=(frame,stamp)
            except Exception:st.warning('NSE current feed is unavailable. Try again later.')
        saved=st.session_state.get('circuit_live')
        if saved:
            frame,stamp=saved
            st.caption(f'Exchange timestamp: {stamp:%d %b %Y %H:%M:%S} IST')
            if stamp.date()!=today:
                st.warning('This is an older exchange snapshot, not today’s current data.');return
            if (datetime.now(ZoneInfo('Asia/Kolkata')).replace(tzinfo=None)-stamp).total_seconds()>900:
                st.warning('Snapshot is over 15 minutes old. It may be an end-of-session snapshot.')
            for band in [2,5,10,20]:
                part=frame[frame['Reported band %'].eq(band)]
                st.markdown(f'**{band}% reported band · {len(part)} stocks at boundary**')
                st.dataframe(part.round(2),hide_index=True,use_container_width=True)


def circuit_readable_rows(rows):
    """Full-width wrapped rows; compact stacked cards on phone screens."""
    cards=[]
    def number(value,digits=2):
        try:return f'{float(value):,.{digits}f}' if pd.notna(value) else '—'
        except (TypeError,ValueError):return '—'
    for _,r in rows.iterrows():
        cells=[('<b>'+html.escape(str(r.Symbol))+'</b><small>'+html.escape(str(r.Company))+' · '+html.escape(str(r.Series))+'</small>','Stock'),
               (number(r['Close (₹)']),'Close ₹'),(number(r['Change %'])+'%','Change'),
               (html.escape(str(r['Consecutive trading days'])),'Trading days'),(number(r.Volume,0),'Volume')]
        cards.append('<tr>'+''.join('<td data-label="'+label+'">'+value+'</td>' for value,label in cells)+'</tr>')
    st.markdown('<div class="circuit-readable"><table><thead><tr><th>Stock / Company</th><th>Close ₹</th><th>Change</th><th>Consecutive days</th><th>Volume</th></tr></thead><tbody>'+''.join(cards)+'</tbody></table></div>',unsafe_allow_html=True)


def render_circuit_page():
    st.markdown('## ⚡ Circuit & Volatility')
    st.markdown("""<style>
    .circuit-readable{width:100%;margin-bottom:20px}
    .circuit-readable table{width:100%;table-layout:fixed;border-collapse:collapse;background:#0b1523;color:#e2e8f0}
    .circuit-readable th,.circuit-readable td{padding:12px 10px;text-align:left;border-bottom:1px solid #253349;white-space:normal;overflow-wrap:anywhere;font-size:13px}
    .circuit-readable th:first-child{width:38%}.circuit-readable th{font-size:12px;color:#94a3b8}
    .circuit-readable small{display:block;color:#94a3b8;font-size:11px;margin-top:5px;line-height:1.5}
    @media(max-width:650px){.circuit-readable table,.circuit-readable tbody{display:block;width:100%}.circuit-readable thead{display:none}.circuit-readable tr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);background:#0d1726;border:1px solid #253349;border-radius:12px;margin:10px 0;padding:8px}.circuit-readable td{display:block;border:0;min-width:0;padding:8px}.circuit-readable td:first-child{grid-column:1 / -1}.circuit-readable td:not(:first-child)::before{content:attr(data-label);display:block;font-size:11px;color:#94a3b8;margin-bottom:4px}}
    </style>""",unsafe_allow_html=True)
    today=datetime.now(ZoneInfo('Asia/Kolkata')).date()
    if 'circuit_date' not in st.session_state:st.session_state['circuit_date']=today
    a,b,c,e=st.columns([1,4,1,1])
    a.button('←',on_click=circuit_move_date,args=(-1,),key='circuit_previous',help='Previous calendar day')
    selected=b.date_input('Report date',max_value=today,key='circuit_date')
    c.button('→',on_click=circuit_move_date,args=(1,),key='circuit_next',disabled=selected>=today,help='Next calendar day')
    e.button('Today',key='circuit_today',on_click=circuit_move_date,args=((today-st.session_state['circuit_date']).days,))
    st.caption('NSE official closing reports · Reported security series · Green = upper, red = lower. Each date uses its own assigned band. Calendar arrows include weekends.')
    st.caption('Final reports arrive after market close. An unavailable report is not interpreted as zero circuits. Intraday touching does not establish a closing circuit.')
    if selected==today:render_circuit_live(today)
    lookback=st.selectbox('Maximum streak verification',['1 trading day','2 trading days','5 trading days','10 trading days','20 trading days','60 trading days'],index=4,key='circuit_lookback')
    limit=int(lookback.split()[0])
    if st.session_state.get('circuit_load_failed')==selected:
        st.link_button('Open NSE official reports','https://www.nseindia.com/all-reports')
        with st.expander('Load downloaded NSE reports if automatic download is blocked',expanded=True):
            st.caption('Download these three reports for the selected date from NSE. They are used only for Circuit & Volatility.')
            closing=st.file_uploader('Full Bhavcopy and Security Deliverable data (CSV)',type=['csv'],key='circuit_upload_close')
            band_file=st.file_uploader('CM - Price Band complete list (CSV)',type=['csv'],key='circuit_upload_band')
            press=st.file_uploader('Bhavcopy (PR) (ZIP)',type=['zip'],key='circuit_upload_pr')
            if st.button('Read uploaded reports',key='circuit_read_upload'):
                if closing is None or band_file is None or press is None:
                    st.warning('Choose all three files for the selected date.')
                else:
                    try:
                        report=circuit_parse_reports(selected,[closing.getvalue(),band_file.getvalue(),press.getvalue()])
                        fixed=report['rows'];fixed=fixed[(fixed.Type=='Fixed')&(fixed.Status=='Closed at circuit')]
                        fixed=circuit_streaks(fixed,[],True)
                        st.session_state['circuit_result']={'date':selected,'report':report,'fixed':fixed,'limit':1,'loaded':datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%d %b %Y %H:%M IST')}
                        st.success('Uploaded reports loaded. Historical streaks have not been verified.')
                    except Exception as exc: st.error('Could not read uploaded reports: '+str(exc))
    if st.button('Load / refresh circuits and streaks',type='primary',key='circuit_scan'):
        circuit_day_report.clear()
        holidays=circuit_holidays()
        if selected.weekday()>=5 or selected in holidays:
            st.info('No regular trading session on this date. Select a trading day.');return
        with loading_stopwatch('Reading official closing, band and band-hitter reports…'):
            try: result=circuit_day_report(selected)
            except Exception as exc:
                result=None
                st.warning(f'NSE reports could not be loaded for {selected:%d %b %Y}. No circuit counts were calculated.')
                st.error(str(exc))
                st.session_state['circuit_load_failed']=selected
        if result is None:
            return
        st.session_state.pop('circuit_load_failed',None)
        fixed=result['rows'];fixed=fixed[(fixed.Type=='Fixed')&(fixed.Status=='Closed at circuit')]
        history=[];cursor=selected;status=st.empty()
        # Stop once all current candidates have a verified end to their streak.
        active={(r.Symbol,r.Series,r.Direction) for _,r in fixed.iterrows()}
        for i in range(limit-1):
            if not active:break
            cursor-=timedelta(days=1)
            while cursor.weekday()>=5 or cursor in holidays:cursor-=timedelta(days=1)
            status.caption(f'Checking {cursor:%d %b %Y} · {len(active)} continuing streaks')
            try: previous=circuit_day_report(cursor)
            except Exception: previous=None
            history.append((cursor,previous))
            if previous is None:break
            p=previous['rows'];p=p[(p.Type=='Fixed')&(p.Status=='Closed at circuit')]
            keys={(r.Symbol,r.Series,r.Direction) for _,r in p.iterrows()}
            active &= keys
        status.empty()
        fixed=circuit_streaks(fixed,history,bool(active) and len(history)>=limit-1)
        st.session_state['circuit_result']={'date':selected,'report':result,'fixed':fixed,'limit':limit,
            'loaded':datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%d %b %Y %H:%M IST')}
    saved=st.session_state.get('circuit_result')
    if not saved or saved['date']!=selected:
        st.info('Choose a date, then load the report.');return
    st.caption(f"Report: {selected:%d %b %Y} · Loaded {saved['loaded']} · Streak verification up to {saved['limit']} trading days")
    tabs=st.tabs(['📌 Closed at fixed circuit','↗ Dynamic ranges','👆 Touched during the day'])
    rows=saved['report']['rows'];fixed=saved['fixed']
    with tabs[0]:
        bands=st.multiselect('Show bands',[2,5,10,20],default=[2,5,10],key='circuit_bands')
        chosen=fixed[fixed['Band %'].isin(bands)]
        direction=st.radio('Direction',['Both','Upper','Lower'],horizontal=True,key='circuit_direction')
        if direction!='Both':chosen=chosen[chosen.Direction.eq(direction)]
        metrics=st.columns(3)
        metrics[0].metric('Closed upper',len(chosen[chosen.Direction.eq('Upper')]))
        metrics[1].metric('Closed lower',len(chosen[chosen.Direction.eq('Lower')]))
        metrics[2].metric('Report securities',saved['report']['coverage'])
        st.caption('Counts are security series. Streaks continue across band changes when the same stock series closes at the same-side fixed circuit. “+” means the exact starting date could not be verified.')
        for side,heading in [('Upper','🟢 Upper circuits'),('Lower','🔴 Lower circuits')]:
            if direction!='Both' and direction!=side:continue
            st.markdown('## '+heading)
            side_rows=chosen[chosen.Direction.eq(side)]
            st.caption(f'{len(side_rows)} stocks · {selected:%d %b %Y}')
            for band in bands:
                part=side_rows[side_rows['Band %'].eq(band)].copy()
                st.markdown(f'### {band}% circuit · {len(part)} stocks')
                if part.empty:st.caption('No matching closes.');continue
                part['_rank']=part['Consecutive trading days'].str.extract(r'^(\d+)')[0].astype(int)
                part=part.sort_values('_rank',ascending=False)
                circuit_readable_rows(part)
        st.download_button('Download circuit closes',chosen.to_csv(index=False),'nse_circuit_'+selected.isoformat()+'.csv','text/csv')
    with tabs[1]:
        dynamic=rows[rows.Type.eq('Dynamic')]
        st.info('These securities have “No Band” in the dated NSE list and appear in the official boundary-hitter report. This confirms a boundary touch, not a halt or a range expansion. Expansion times and revised limits are not supplied by these files.')
        st.dataframe(dynamic.drop(columns=['Band %']).round(2),hide_index=True,use_container_width=True)
    with tabs[2]:
        touched=rows[(rows.Type=='Fixed')&(rows.Status=='Touched only')]
        st.caption('Touched a fixed circuit during the session, but the official closing price was away from it. Not counted in closing streaks.')
        st.dataframe(touched.round(2),hide_index=True,use_container_width=True)
    st.link_button('NSE original reports','https://www.nseindia.com/all-reports')


# US market functions are separate from NSE calculations and ticker handling.
@st.cache_data(ttl=86400, show_spinner=False)
def us_stock_directory():
    rows=[]
    for filename, exchange in [('nasdaqlisted.txt','Nasdaq'),('otherlisted.txt','NYSE')]:
        r=requests.get('https://www.nasdaqtrader.com/dynamic/SymDir/'+filename,timeout=25)
        r.raise_for_status()
        d=pd.read_csv(io.StringIO(r.text),sep='|',dtype=str)
        if exchange=='NYSE':
            d=d[d['Exchange'].eq('N')]
        d=d[d['Test Issue'].eq('N') & d['ETF'].eq('N')]
        symbol_col='Symbol' if exchange=='Nasdaq' else 'ACT Symbol'
        # Listed non-ETF equities; preferred shares and warrants may be included.
        for _, x in d.iterrows():
            symbol=str(x[symbol_col]).strip()
            if not symbol or symbol=='nan': continue
            rows.append({'Symbol':symbol,'Ticker':symbol.replace('.','-'),
                         'Company':x['Security Name'],'Exchange':exchange})
    return pd.DataFrame(rows).drop_duplicates('Symbol').reset_index(drop=True)

def us_parse_holdings(text):
    import csv
    lines=text.lstrip('\ufeff').splitlines()
    start=next((i for i,line in enumerate(lines)
                if [x.strip() for x in next(csv.reader([line]),[])] and
                next(csv.reader([line]),[])[0].strip()=='Ticker'),None)
    if start is None:raise ValueError('Source did not return a holdings CSV')
    d=pd.read_csv(io.StringIO('\n'.join(lines[start:])),on_bad_lines='skip')
    d.columns=d.columns.str.strip()
    if not {'Ticker','Sector','Asset Class'}.issubset(d.columns):raise ValueError('Missing holdings columns')
    d=d[d['Asset Class'].astype(str).str.strip().eq('Equity')]
    ticker=d['Ticker'].astype(str).str.strip().str.replace(r'[.\s]+','-',regex=True)
    valid=ticker.str.fullmatch(r'[A-Z0-9]+(?:-[A-Z0-9]+)*')
    result=dict(zip(ticker[valid],d.loc[valid,'Sector'].fillna('Unclassified')))
    if len(result)<450:raise ValueError('Incomplete S&P 500 holdings download')
    return result

@st.cache_data(ttl=86400, show_spinner=False)
def us_sp500_holdings():
    urls=[
      'https://www.ishares.com/us/products/239726/ishares-core-s-p-500-etf/latest-holdings.csv',
      'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf-ivv/1467271812596.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund'
    ]
    errors=[]
    with requests.Session() as session:
        session.headers.update({'User-Agent':'Mozilla/5.0','Accept':'text/csv,*/*'})
        for url in urls:
            try:
                r=session.get(url,timeout=(5,25));r.raise_for_status()
                return us_parse_holdings(r.content.decode('utf-8-sig',errors='replace'))
            except Exception as exc:errors.append(type(exc).__name__)
    raise ValueError('Holdings sources unavailable: '+', '.join(errors))


def us_price_metrics(frame, symbol):
    f=frame.dropna(subset=['Close']).copy()
    if len(f)<2: return None
    close=pd.to_numeric(f['Close'],errors='coerce'); last=float(close.iloc[-1])
    if not np.isfinite(last) or last<=0: return None
    result={'Ticker':symbol,'Latest ($)':last,'Price date':str(f.index[-1].date())}
    for label,n in [('1D %',1),('2D %',2),('1W %',5),('1M %',21),('3M %',63),('6M %',126),('1Y %',252)]:
        result[label]=(last/float(close.iloc[-n-1])-1)*100 if len(close)>n and close.iloc[-n-1]>0 else np.nan
    span=(f.index[-1]-f.index[0]).days
    result['5Y %']=(last/float(close.iloc[0])-1)*100 if span>=1780 and close.iloc[0]>0 else np.nan
    result['Daily high']=f['High'].iloc[-1];result['Daily low']=f['Low'].iloc[-1]
    for n in [20,50,200]: result['SMA'+str(n)]=close.tail(n).mean() if len(close)>=n else np.nan
    delta=close.diff(); gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    result['RSI14']=float((100-100/(1+gain/loss)).iloc[-1]) if loss.iloc[-1]>0 else (100.0 if gain.iloc[-1]>0 else 50.0)
    volume=pd.to_numeric(f['Volume'],errors='coerce')
    result['Volume']=volume.iloc[-1]
    avg=volume.iloc[-21:-1].mean()
    result['Volume ratio']=volume.iloc[-1]/avg if avg>0 else np.nan
    result['52W high']=f['High'].tail(252).max(); result['52W low']=f['Low'].tail(252).min()
    return result

@st.cache_data(ttl=900, show_spinner=False)
def us_download_batch(symbols,period="2y"):
    data=yf.download(list(symbols),period=period,interval='1d',auto_adjust=True,
                     group_by='ticker',threads=4,progress=False,timeout=15)
    rows=[]
    for symbol in symbols:
        try:
            f=data[symbol] if isinstance(data.columns,pd.MultiIndex) else data
            row=us_price_metrics(f,symbol)
            if row: rows.append(row)
        except (KeyError,ValueError,TypeError,IndexError): pass
    return pd.DataFrame(rows)

@st.cache_data(ttl=900, show_spinner=False)
def us_detail(symbol):
    stock=yf.Ticker(symbol)
    history=stock.history(period='2y',auto_adjust=True)
    try: info=stock.get_info()
    except Exception: info={}
    try: news=stock.get_news(count=8)
    except Exception: news=[]
    return history,info,news


def us_heatmap(frame, group, title):
    import plotly.express as px
    d=frame.dropna(subset=['1D %']).copy()
    if d.empty: st.info('No price changes available for this heatmap.'); return
    d['Tile size']=1
    fig=px.treemap(d,path=[group,'Symbol'],values='Tile size',color='1D %',
                   color_continuous_scale=['#b91c1c','#182334','#15803d'],color_continuous_midpoint=0,
                   hover_data=['Company','Latest ($)','1D %'],title=title)
    fig.update_traces(texttemplate='%{label}<br>%{color:.2f}%')
    fig.update_layout(height=530,margin=dict(t=45,l=0,r=0,b=0),paper_bgcolor='#0b1523',font_color='#e2e8f0')
    st.plotly_chart(fig,use_container_width=True)


def render_us_market():
    st.markdown('## 🇺🇸 All US Stocks')
    st.caption('NYSE + Nasdaq · USD · Daily Yahoo Finance prices (may be delayed). This page uses separate US data.')
    scope=st.selectbox('Stock universe',['All NYSE + Nasdaq','NYSE only','Nasdaq only','S&P 500'])
    controls=st.columns(3)
    history=controls[0].selectbox('History',['1y','2y','5y'],index=2,key='us_history')
    rank=controls[1].selectbox('Sort by',['Latest ($)','1D %','2D %','1W %','1M %','3M %','6M %','1Y %','5Y %','Volume','Volume ratio','RSI14'],key='us_rank')
    ascending=controls[2].selectbox('Order',['Largest → Smallest','Smallest → Largest'],key='us_order')=='Smallest → Largest'
    c1,c2=st.columns(2)
    reload_directory=c1.button('Refresh stock directory',key='us_directory_refresh')
    if reload_directory:
        us_stock_directory.clear(); us_sp500_holdings.clear()
    try:
        directory=us_stock_directory()
    except Exception as e:
        st.error('US listing source is unavailable. Try Refresh stock directory again.'); return
    try: sectors=us_sp500_holdings()
    except Exception: sectors={}
    directory['Sector']=directory['Ticker'].map(sectors).fillna('Unclassified')
    if scope=='NYSE only': directory=directory[directory.Exchange.eq('NYSE')]
    elif scope=='Nasdaq only': directory=directory[directory.Exchange.eq('Nasdaq')]
    elif scope=='S&P 500':
        if not sectors: st.error('S&P 500 holdings source unavailable. Please retry later.'); return
        directory=directory[directory.Ticker.isin(sectors)]
        st.caption('S&P 500 membership / sectors use the iShares IVV equity holdings as a constituent proxy.')
    st.caption(f'{len(directory):,} listed non-ETF equities. Listings can include preferred shares or warrants. Sector labels cover IVV holdings; other listings are Unclassified.')
    st.download_button('Download selected stock directory',directory.to_csv(index=False),'us_stock_directory.csv','text/csv')
    load=c2.button('📊 Build / Refresh Classic Table',type='primary',key='us_prices_refresh')
    if load:
        us_download_batch.clear()
        frames=[]; errors=0; symbols=directory.Ticker.tolist(); progress=st.progress(0)
        status=st.empty()
        for start in range(0,len(symbols),100):
            status.caption(f'Loading {start+1:,}–{min(start+100,len(symbols)):,} of {len(symbols):,}. Full US coverage can take several minutes.')
            try: frames.append(us_download_batch(tuple(symbols[start:start+100]),history))
            except Exception: errors+=1
            progress.progress(min((start+100)/max(len(symbols),1),1.0))
        prices=pd.concat(frames,ignore_index=True) if frames else pd.DataFrame()
        st.session_state['us_snapshot']={'scope':scope,'history':history,'prices':prices,'loaded':datetime.now(ZoneInfo('America/New_York')).strftime('%Y-%m-%d %H:%M %Z'),'errors':errors}
        status.empty(); progress.empty()
    saved=st.session_state.get('us_snapshot')
    if not saved or saved['scope']!=scope or saved.get('history')!=history:
        st.info('Click Build / Refresh Classic Table to load the selected universe and history. No stock-count limit is applied.'); return
    prices=saved['prices']
    if prices.empty: st.warning('No prices returned. The provider may be rate limiting requests. Try again later.'); return
    d=directory.merge(prices,on='Ticker',how='inner')
    if d.empty: st.warning('The directory changed. Reload prices.'); return
    asof=d['Price date'].max(); latest=d[d['Price date'].eq(asof)&d.Volume.gt(0)]
    st.caption(f"Loaded {saved['loaded']} · {len(d):,}/{len(directory):,} stocks have prices · Breadth uses {len(latest):,} traded stocks dated {asof}. Prices are split/dividend adjusted.")
    missing=directory[~directory.Ticker.isin(d.Ticker)]
    if not missing.empty:
        st.warning(f'{len(missing):,} listings have no usable prices. These are excluded from heatmaps and statistics.')
        st.download_button('Download unavailable listings',missing.to_csv(index=False),'us_unavailable.csv','text/csv')
    st.markdown('### US Market Statistics')
    st.caption('Calculated from available prices in the selected universe; not an official exchange-wide live feed.')
    stats=[('Stocks traded',len(latest)),('Advances',latest['1D %'].gt(0).sum()),
           ('Declines',latest['1D %'].lt(0).sum()),('Unchanged',latest['1D %'].eq(0).sum()),
           ('52W high',latest['Daily high'].ge(latest['52W high']).sum()),
           ('52W low',latest['Daily low'].le(latest['52W low']).sum()),
           ('Above SMA200',(latest['Latest ($)']>latest.SMA200).sum()),
           ('Volume ≥ 2× average',latest['Volume ratio'].ge(2).sum())]
    for start in [0,4]:
        for col,(label,value) in zip(st.columns(4),stats[start:start+4]):col.metric(label,f'{value:,}')
    st.caption('52-week extremes use up to 252 available sessions; recently listed stocks have shorter histories. US volatility cards use trend / volume, not Indian fixed-circuit rules.')
    heat,table,report=st.tabs(['🔥 Heatmaps','📊 Table / Smart Scanner','🔎 Stock Report'])
    with heat:
        st.markdown('### 🟩 Heat Map')
        mode=st.radio('Choose heat map',['Broad Market Indices','Sectoral Indices','Stocks by Exchange','Stocks by Sector'],horizontal=True,key='us_heatmap_mode')
        if mode in ['Broad Market Indices','Sectoral Indices']:
            names=({'^GSPC':'S&P 500','^IXIC':'Nasdaq Composite','^DJI':'Dow Jones','^RUT':'Russell 2000'} if mode=='Broad Market Indices' else
                   {'XLK':'Technology','XLF':'Financials','XLE':'Energy','XLV':'Health Care','XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLI':'Industrials','XLB':'Materials','XLU':'Utilities','XLRE':'Real Estate','XLC':'Communication'})
            try: indices=us_download_batch(tuple(names))
            except Exception:indices=pd.DataFrame()
            if indices.empty:st.info('Index / sector price source is temporarily unavailable.')
            else:
                st.caption('Sector ETFs are proxies for S&P 500 sectors.' if mode=='Sectoral Indices' else 'Broad market indices are independent of the selected stock universe.')
                for start in range(0,len(indices),4):
                    for col,(_,row) in zip(st.columns(4),indices.iloc[start:start+4].iterrows()):
                        change=row['1D %'];colour='#14532d' if change>=0 else '#7f1d1d'
                        with col:
                            st.markdown(f'<div style="background:{colour};padding:18px;border-radius:12px;margin-bottom:12px"><b>{html.escape(names.get(row.Ticker,row.Ticker))}</b><br><strong>{row["Latest ($)"]:,.2f}</strong><br>{change:+.2f}%<br><small>{row["Price date"]}</small></div>',unsafe_allow_html=True)
        else:
            group='Exchange' if mode=='Stocks by Exchange' else 'Sector'
            st.caption('Equal-size stock tiles; colour shows daily % change. Sector labels cover S&P 500 holdings; other stocks are Unclassified.')
            us_heatmap(latest,group,'US stock daily performance')
            if group=='Sector':
                classified=latest[latest.Sector.ne('Unclassified')]
                if not classified.empty:
                    st.bar_chart(classified.groupby('Sector')['1D %'].mean().sort_values())
                    st.caption('Equal-weight sector averages for classified stocks in the selected universe.')
    with table:
        st.markdown('### 📋 Classic Performance Table / Smart Scanner')
        st.caption(f'Selected history: {history} · Sort: {rank}. Change history above, then rebuild prices.')
        style=st.radio('View',['Classic Table','Smart Scanner'],horizontal=True,key='us_table_mode')
        search=st.text_input('Search stock symbol or company',key='us_search')
        filtered=d.copy()
        if search: filtered=filtered[filtered.Symbol.str.contains(search,case=False,regex=False)|filtered.Company.str.contains(search,case=False,regex=False)]
        if style=='Smart Scanner':
            a,b,c=st.columns(3)
            trend=a.selectbox('Trend',['All','Above SMA50','Above SMA200','Below SMA200'])
            min_volume=b.number_input('Minimum daily volume',min_value=0,value=0,step=100000)
            rsi=c.slider('RSI range',0,100,(0,100))
            filtered=filtered[filtered.Volume.ge(min_volume)&filtered.RSI14.between(*rsi)]
            if trend=='Above SMA50': filtered=filtered[filtered['Latest ($)']>filtered.SMA50]
            elif trend=='Above SMA200': filtered=filtered[filtered['Latest ($)']>filtered.SMA200]
            elif trend=='Below SMA200': filtered=filtered[filtered['Latest ($)']<filtered.SMA200]
        filtered=filtered.sort_values(rank,ascending=ascending,na_position='last')
        st.caption(f'{len(filtered):,} matching stocks')
        st.dataframe(filtered.drop(columns=['Ticker','Daily high','Daily low']).round(2),use_container_width=True,hide_index=True,height=550)
        st.download_button('Export US scan',filtered.to_csv(index=False),'us_stock_scan.csv','text/csv')
    with report:
        choices=directory.Ticker.tolist()
        companies=directory.set_index('Ticker').Company.to_dict()
        symbol=st.selectbox('Select a US stock',choices,format_func=lambda x:f'{x} — {companies.get(x,"")}',key='us_report_stock')
        if st.button('Get stock report',key='us_report_load'):
            with loading_stopwatch('Loading stock report…'):
                try:
                    history,info,news=us_detail(symbol)
                    st.subheader(info.get('longName',companies.get(symbol,symbol)))
                    if not history.empty: st.line_chart(history['Close'])
                    fields=st.columns(4)
                    for col,label,key in zip(fields,['Market cap ($)','Trailing P/E','Sector','Industry'],['marketCap','trailingPE','sector','industry']): col.metric(label,str(info.get(key,'Unavailable')))
                    if info.get('longBusinessSummary'): st.write(info['longBusinessSummary'])
                    st.markdown('### Available news')
                    count=0
                    for item in news:
                        content=item.get('content',item); title=content.get('title')
                        link=(content.get('canonicalUrl') or {}).get('url') or content.get('link')
                        if title:
                            st.write(title)
                            if link and link.startswith('https://'): st.link_button('Read source',link)
                            count+=1
                    if not count: st.info('No matching news returned by the provider.')
                    st.link_button('Open Yahoo Finance',f'https://finance.yahoo.com/quote/{symbol}/')
                except Exception: st.error('Stock report is temporarily unavailable. Try again later.')


@st.cache_data(ttl=86400,show_spinner=False)
def nse_sector_constituents(group):
    files={'NIFTY 50':'ind_nifty50list.csv','NIFTY 100':'ind_nifty100list.csv',
           'NIFTY 200':'ind_nifty200list.csv','NIFTY 500':'ind_nifty500list.csv',
           'NIFTY Midcap':'ind_niftymidcap150list.csv','NIFTY Smallcap':'ind_niftysmallcap250list.csv',
           'Total Market':'ind_niftytotalmarket_list.csv'}
    filename=files[group]
    last_error=None
    for host in ['https://nsearchives.nseindia.com/content/indices/','https://www.niftyindices.com/IndexConstituent/']:
        try:
            r=requests.get(host+filename,headers=HEADERS,timeout=(5,15));r.raise_for_status()
            d=pd.read_csv(io.BytesIO(r.content));d.columns=d.columns.str.strip()
            if not {'Symbol','Industry','Company Name'}.issubset(d.columns):raise ValueError('Constituent format changed')
            d=d[['Symbol','Industry','Company Name']].dropna(subset=['Symbol']).copy()
            d['Symbol']=d.Symbol.astype(str).str.strip()
            return d.drop_duplicates('Symbol')
        except Exception as exc:last_error=exc
    raise ValueError('NSE constituent source unavailable') from last_error

@st.cache_data(ttl=604800,show_spinner=False)
def nse_extra_sector(symbol):
    try:
        info=yf.Ticker(symbol+'.NS').get_info()
        value=str(info.get('sector') or info.get('industry') or '').strip()
        return {'sector':value,'company':str(info.get('longName') or symbol)} if value else {}
    except Exception:return {}


def nse_sector_return(record,sessions):
    closes=(record or {}).get('closes',[])
    if not closes:return np.nan
    if len(closes)<=sessions:
        # Yahoo's five-year calendar window need not contain exactly 1260 sessions.
        if sessions!=1260:return np.nan
        end=pd.Timestamp(closes[-1][0]);boundary=end-pd.DateOffset(years=5)
        if pd.Timestamp(closes[0][0])>boundary+pd.Timedelta(days=7):return np.nan
        baseline=closes[0][1]
    else:baseline=closes[-sessions-1][1]
    last=closes[-1][1]
    return (float(last)/float(baseline)-1)*100 if baseline and float(baseline)>0 else np.nan


def nse_sector_colour(value):
    if pd.isna(value):return '#64748b'
    if value==0:return '#374151'
    strength=min(np.log1p(abs(float(value)))/np.log(21),1)
    if value>0:return f'rgb(18,{int(95+65*strength)},65)'
    return f'rgb({int(120+70*strength)},35,45)'


def nse_sector_figure(frame,period):
    ids=['root'];labels=['NSE stocks'];parents=[''];values=[len(frame)];colours=['#0b1523'];texts=[''];custom=[['','','','']]
    for i,(sector,part) in enumerate(frame.groupby('Sector',sort=True)):
        group_id='group-'+str(i);ids.append(group_id);labels.append(html.escape(str(sector)));parents.append('root');values.append(len(part));colours.append('#17283e');texts.append(str(len(part))+' stocks');custom.append(['','','',''])
        for _,r in part.iterrows():
            ids.append('stock-'+str(r.Symbol));labels.append(html.escape(str(r.Symbol)));parents.append(group_id);values.append(1)
            colours.append(nse_sector_colour(r.Return));ret='Unavailable' if pd.isna(r.Return) else f'{r.Return:+.2f}%'
            texts.append(ret);custom.append([html.escape(str(r.Company)),ret,'—' if pd.isna(r.Latest) else f'₹{r.Latest:,.2f}',str(r.Date)])
    fig=go.Figure(go.Treemap(ids=ids,labels=labels,parents=parents,values=values,branchvalues='total',
             marker=dict(colors=colours,line=dict(width=1,color='#0b1523')),text=texts,texttemplate='%{label}<br>%{text}',
             textfont=dict(color='white',size=11),customdata=custom,
             hovertemplate='<b>%{label}</b><br>%{customdata[0]}<br>'+html.escape(period)+': %{customdata[1]}<br>%{customdata[2]}<br>Price date: %{customdata[3]}<extra></extra>',
             pathbar=dict(visible=True,textfont=dict(color='white'))))
    fig.update_layout(height=420,margin=dict(t=0,l=0,r=0,b=0),paper_bgcolor='#0b1523',font_color='#f8fafc',uniformtext=dict(minsize=10,mode='hide'))
    return fig


def nse_sector_compact_html(frame):
    panels=[]
    for sector,part in frame.groupby('Sector',sort=True):
        tiles=[]
        for _,r in part.iterrows():
            ret='N/A' if pd.isna(r.Return) else f'{r.Return:+.2f}%'
            detail=f'{r.Company} | {ret} | Price date: {r.Date}'
            tiles.append(f'<div class="sector-tile" title="{html.escape(detail,quote=True)}" style="background:{nse_sector_colour(r.Return)}"><b>{html.escape(str(r.Symbol))}</b><span>{ret}</span></div>')
        panels.append(f'<section class="sector-panel"><h4>{html.escape(str(sector))} <small>({len(part)})</small></h4><div class="sector-tiles">'+''.join(tiles)+'</div></section>')
    return """<style>
    .sector-grid{columns:4;column-gap:7px}
    .sector-panel{break-inside:avoid;background:#101c2c;border:1px solid #26364a;border-radius:6px;padding:5px;margin:0 0 7px}
    .sector-panel h4{color:#e2e8f0;font:600 12px system-ui;margin:0 0 5px;line-height:1.25}
    .sector-panel small{color:#94a3b8;font-size:10px}
    .sector-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:3px}
    .sector-tile{padding:4px 5px;border-radius:3px;color:white;min-width:0;line-height:1.25;font:11px system-ui}
    .sector-tile b{display:block;overflow-wrap:anywhere}.sector-tile span{display:block;margin-top:2px}
    @media(max-width:1000px){.sector-grid{columns:3}}
    @media(max-width:700px){.sector-grid{columns:2}}
    @media(max-width:400px){.sector-grid{columns:1}}
    </style><div class="sector-grid">"""+''.join(panels)+'</div>'


NSE_PERCENT_PERIODS={'1 Day':1,'1 Week':5,'2 Weeks':10,'1 Month':21,'3 Months':63,'6 Months':126,'1 Year':252,'2 Years':504,'5 Years':1260}

def nse_percentage_return(record,period):
    closes=(record or {}).get('closes',[]);sessions=NSE_PERCENT_PERIODS[period]
    if len(closes)>sessions:return nse_sector_return(record,sessions)
    # Calendar windows can contain fewer sessions; accept only a full year span.
    if period not in ['1 Year','2 Years','5 Years'] or not closes:return np.nan
    years={'1 Year':1,'2 Years':2,'5 Years':5}[period]
    boundary=pd.Timestamp(closes[-1][0])-pd.DateOffset(years=years)
    if pd.Timestamp(closes[0][0])>boundary+pd.Timedelta(days=7):return np.nan
    baseline=float(closes[0][1]);last=float(closes[-1][1])
    return (last/baseline-1)*100 if baseline>0 and np.isfinite(last) else np.nan

def nse_percentage_filter(frame,direction,threshold):
    if frame.empty:return frame.copy()
    column=pd.to_numeric(frame['Change %'],errors='coerce')
    mask=column.ge(float(threshold)) if direction=='Gainer' else column.le(-float(threshold))
    return frame.loc[mask].sort_values('Change %',ascending=direction=='Loser').reset_index(drop=True)

def nse_percentage_style(frame):
    palette=['#dbeafe','#ede9fe','#fef3c7','#cffafe','#fce7f3','#e0e7ff']
    sector_colours={sector:palette[i%len(palette)] for i,sector in enumerate(sorted(frame['Sector / Business'].unique()) if 'Sector / Business' in frame else [])}
    def colour_row(row):
        base='#f8fafc' if row.name%2 else '#ffffff'
        styles=['background-color:'+base+';color:#172033' for _ in row]
        for i,column in enumerate(frame.columns):
            if column=='Symbol':styles[i]='background-color:#dbeafe;color:#1e40af;font-weight:bold'
            elif column=='Stock Name':styles[i]='background-color:#eff6ff;color:#172033'
            elif column=='Change %':
                gain=row[column]>=0
                styles[i]='background-color:'+('#dcfce7' if gain else '#fee2e2')+';color:'+('#166534' if gain else '#b91c1c')+';font-weight:bold'
            elif column=='Sector / Business':styles[i]='background-color:'+sector_colours[row[column]]+';color:#312e81'
            elif column=='No.':styles[i]='background-color:#e0e7ff;color:#3730a3;font-weight:bold'
        return styles
    formats={'Change %':'{:+.2f}%'}
    for col in ['Market Cap (₹ Cr)','P/E','P/B','Latest Price (₹)']:
        if col in frame:formats[col]='{:,.0f}' if col=='Market Cap (₹ Cr)' else '{:,.2f}'
    for col in ['Promoter %','FII %','DII %']:
        if col in frame:formats[col]='{:.2f}%'
    return frame.style.apply(colour_row,axis=1).format(formats,na_rep='—')


STEADY_PERIODS={'1 Week':5,'2 Weeks':10,'1 Month':21,'3 Months':63,'6 Months':126,'1 Year':252,'2 Years':504,'5 Years':1260,'10 Years':2520,'15 Years':3780,'25 Years':6300}

def nse_steady_pattern(record,sessions,max_pullback=15.0):
    """Screen daily closing-price swings; confirmed pivots exclude endpoints."""
    import math
    history=(record or {}).get('closes',[])
    by_date={str(item[0]):float(item[1]) for item in history}
    points=sorted(by_date.items())
    if len(points)<sessions+1:return None
    points=points[-(sessions+1):];values=[v for _,v in points]
    if any(not math.isfinite(v) or v<=0 for v in values):return None
    gain=(values[-1]/values[0]-1)*100
    logs=[math.log(v) for v in values];n=len(logs);xm=(n-1)/2;ym=sum(logs)/n
    xx=sum((i-xm)**2 for i in range(n));yy=sum((v-ym)**2 for v in logs)
    xy=sum((i-xm)*(v-ym) for i,v in enumerate(logs));slope=xy/xx
    r2=xy*xy/(xx*yy) if yy else 0
    highs=[values[i] for i in range(1,n-1) if values[i]>values[i-1] and values[i]>=values[i+1]]
    lows=[values[i] for i in range(1,n-1) if values[i]<values[i-1] and values[i]<=values[i+1]]
    if len(highs)<2 or len(lows)<2:return None
    hh=highs[-1]>highs[-2];hl=lows[-1]>lows[-2]
    peak=values[0];drawdown=0
    for v in values:
        peak=max(peak,v);drawdown=max(drawdown,(1-v/peak)*100)
    latest_pullback=(1-values[-1]/max(values))*100
    window=min(10,max(2,n//2));shift=min(5,n-window)
    ma_now=sum(values[-window:])/window;ma_before=sum(values[-window-shift:-shift])/window
    if not (gain>0 and slope>0 and r2>=0.55 and hh and hl and drawdown<=max_pullback and values[-1]>=ma_now and ma_now>ma_before):return None
    return {'Gain %':gain,'Latest pullback %':latest_pullback,'Largest pullback %':drawdown,
        'Trend consistency':round(r2*100,1),'Price Date':points[-1][0],'Price chart':values}


def nse_steady_load_history(symbols_tuple,period):
    sessions=STEADY_PERIODS[period]
    if sessions<=504:
        classic_period_snapshot(symbols_tuple,'2y' if sessions>252 else '1y')
        return
    state=price_request_state();saved=state['classic'].setdefault('steady_max',{})
    shared=st.session_state.get('shared_nse_price_cache',{}).get('records',{})
    todo=[]
    for symbol in symbols_tuple:
        candidates=[shared.get(symbol)]+[bucket.get(symbol,{}).get('record') for bucket in state['classic'].values()]
        if not any(r and len(r.get('closes',[]))>=sessions+1 for r in candidates):
            entry=saved.get(symbol)
            if not entry or time.monotonic()-entry.get('saved_at',0)>=900:todo.append(symbol)
    progress=st.progress(0);status=st.empty();notice='';empty_batches=0
    try:
        for offset in range(0,len(todo),70):
            batch=todo[offset:offset+70];tickers=[symbol+'.NS' for symbol in batch]
            try:
                downloaded,limited=limited_price_download(tickers,period='max',interval='1d',group_by='ticker',auto_adjust=False,progress=False)
            except Exception as exc:
                notice='Historical downloads stopped. Saved prices retained. '+str(exc);break
            found=0
            for symbol,ticker in zip(batch,tickers):
                frame=market_cache_frame(downloaded,symbol,ticker,len(batch))
                if frame.empty or 'Close' not in frame:continue
                close=pd.to_numeric(frame['Close'],errors='coerce').dropna();close=close[close>0].sort_index()
                if close.empty:continue
                closes=[[pd.Timestamp(d).date().isoformat(),float(v)] for d,v in close.items()]
                saved[symbol]={'record':{'closes':closes,'last_date':closes[-1][0]},'saved_at':time.monotonic()};found+=1
            progress.progress(min(offset+len(batch),len(todo))/max(1,len(todo)))
            status.caption(f'Long history checked: {min(offset+len(batch),len(todo)):,}/{len(todo):,}')
            empty_batches=empty_batches+1 if not found else 0
            if limited or empty_batches>=2:
                notice='Price service returned limited / unavailable data. Saved prices retained.';break
    finally:progress.empty();status.empty()
    st.session_state['classic_load_notice']=notice


def nse_steady_valuation(info):
    """Latest available valuation; market cap in INR crore, missing stays blank."""
    import math
    def number(key):
        try:
            value=float(info.get(key))
            return value if math.isfinite(value) else None
        except (TypeError,ValueError):return None
    cap=number('marketCap')
    return {'Market Cap (₹ Cr)':cap/10000000 if cap is not None and cap>0 else None,
            'P/E':number('trailingPE'),'P/B':number('priceToBook')}


def render_nse_steady_view(group,default_symbols):
    st.markdown('#### 📈 Steady Uptrend')
    controls=st.columns(2)
    period=controls[0].selectbox('Pattern period',list(STEADY_PERIODS),index=2,key='steady_period')
    maximum=controls[1].number_input('Maximum pullback %',min_value=1.0,max_value=50.0,value=15.0,step=1.0,key='steady_pullback')
    st.caption('Daily closing prices: positive trend, last two confirmed swing highs and lows rising, trend consistency ≥55%, rising moving average and pullbacks within your limit. This is a pattern screen, not a prediction. Splits / corporate actions can affect unadjusted prices.')
    state=st.session_state.setdefault('nse_steady_data',{})
    if st.button('Load / Update uptrend data',type='primary',key='steady_load'):
        with loading_stopwatch('Loading prices and sector labels for uptrend patterns…'):
            try:
                catalog=nse_sector_constituents('Total Market' if group=='All NSE' else group)
                symbols=list(default_symbols) if group=='All NSE' else catalog.Symbol.tolist()
                metadata={str(r.Symbol):{'company':str(r['Company Name']),'sector':str(r.Industry)} for _,r in catalog.iterrows()}
                nse_steady_load_history(tuple(symbols),period)
                state.update(group=group,symbols=symbols,metadata=metadata)
            except Exception as exc:st.error('Could not load uptrend data: '+str(exc));return
    prior=st.session_state.get('nse_percentage_data',{})
    active=state if state.get('group')==group else prior if prior.get('group')==group else {}
    symbols=active.get('symbols',list(default_symbols));metadata=active.get('metadata',{})
    shared=st.session_state.get('shared_nse_price_cache',{}).get('records',{})
    saved=price_request_state()['classic'];rows=[];available=0
    sessions=STEADY_PERIODS[period]
    for symbol in symbols:
        candidates=[shared.get(symbol)]+[bucket.get(symbol,{}).get('record') for bucket in saved.values()]
        candidates=[r for r in candidates if r and len(r.get('closes',[]))>=sessions+1]
        if not candidates:continue
        record=max(candidates,key=lambda r:(r.get('last_date',''),len(r['closes'])))
        available+=1
        try:pattern=nse_steady_pattern(record,sessions,maximum)
        except (ValueError,TypeError,IndexError):continue
        if pattern:
            info=metadata.get(symbol,{})
            rows.append({'Symbol':symbol,'Stock Name':info.get('company',symbol),'Sector':info.get('sector','Unclassified'),**pattern})
    st.caption(f'{available:,}/{len(symbols):,} stocks have enough saved history · {len(rows):,} match. Changing period or pullback limit reuses saved prices. Click Load / Update if the longer period needs more history. Years require 252 trading sessions each; 25 years requires 6,301 daily closes.')
    if st.session_state.get('classic_load_notice'):st.warning(st.session_state['classic_load_notice'])
    if not rows:
        st.info('No matching patterns in available history. Load prices if coverage is incomplete, or change the period / pullback limit.');return
    frame=pd.DataFrame(rows).sort_values(['Trend consistency','Gain %'],ascending=False)
    sectors=sorted(frame.Sector.unique())
    selected=st.multiselect('Sectors',sectors,default=sectors,key='steady_sectors_'+group)
    frame=frame[frame.Sector.isin(selected)].reset_index(drop=True)
    valuations=st.session_state.setdefault('nse_steady_valuations',{})
    st.caption('Valuation details are latest available, not historical values for the selected pattern period. Market cap is in ₹ crore; P/E is trailing. Blank means unavailable. Loading details does not change the pattern filter.')
    if st.button('Load valuation details for filtered matches',key='steady_valuation_load',disabled=frame.empty):
        with loading_stopwatch('Loading market cap, P/E and P/B for matching stocks…'):
            progress=st.progress(0.0)
            for i,symbol in enumerate(frame.Symbol.tolist()):
                valuations[symbol]=nse_steady_valuation(fundamentals_for_stock(symbol))
                progress.progress((i+1)/len(frame))
            progress.empty()
    for column in ['Market Cap (₹ Cr)','P/E','P/B']:
        frame[column]=[valuations.get(symbol,{}).get(column) for symbol in frame.Symbol]
    columns=list(frame.columns)
    for column in ['Market Cap (₹ Cr)','P/E','P/B']:columns.remove(column)
    location=columns.index('Sector')+1
    columns[location:location]=['Market Cap (₹ Cr)','P/E','P/B']
    frame=frame[columns]
    st.dataframe(frame,hide_index=True,use_container_width=True,height=min(650,38+len(frame)*35),column_config={
        'Market Cap (₹ Cr)':st.column_config.NumberColumn(format='%.2f'),
        'P/E':st.column_config.NumberColumn(format='%.2f'),
        'P/B':st.column_config.NumberColumn(format='%.2f'),
        'Price chart':st.column_config.LineChartColumn('Price chart',width='medium'),
        'Gain %':st.column_config.NumberColumn(format='%.2f%%'),
        'Latest pullback %':st.column_config.NumberColumn(format='%.2f%%'),
        'Largest pullback %':st.column_config.NumberColumn(format='%.2f%%'),
        'Trend consistency':st.column_config.NumberColumn('Trend consistency /100',format='%.1f')})
    st.download_button('Download uptrend matches',frame.drop(columns=['Price chart']).to_csv(index=False),'steady_uptrend.csv','text/csv',key='steady_csv')



def nse_screener_url(symbol):
    from urllib.parse import quote
    return 'https://www.screener.in/company/'+quote(str(symbol).removesuffix('.NS'),safe='')+'/'


def nse_membership_label(symbol,memberships):
    labels=[label for label in ['N50','N100','N500'] if memberships.get(label) is not None and symbol in memberships[label]]
    missing=any(memberships.get(label) is None for label in ['N50','N100','N500'])
    if labels:return ' · '.join(labels)+(' · Other index data unavailable' if missing else '')
    return 'Unavailable' if missing else 'Outside Nifty 500'


def nse_market_cap_crore(info):
    try:
        value=float((info or {}).get('marketCap'))
        return value/10000000 if np.isfinite(value) and value>0 else np.nan
    except (TypeError,ValueError):return np.nan


def nse_percentage_membership_cap(frame):
    from concurrent.futures import ThreadPoolExecutor,as_completed
    memberships={}
    for label,index in [('N50','NIFTY 50'),('N100','NIFTY 100'),('N500','NIFTY 500')]:
        try:memberships[label]=set(nse_sector_constituents(index).Symbol.tolist())
        except Exception:memberships[label]=None
    frame['Nifty Membership']=[nse_membership_label(symbol,memberships) for symbol in frame.Symbol]
    cache=st.session_state.setdefault('nse_percentage_market_caps',{})
    todo=[symbol for symbol in frame.Symbol if symbol not in cache or time.time()-cache[symbol]['saved_at']>=21600]
    if todo:
        with loading_stopwatch('Loading market caps for filtered stocks…'):
            progress=st.progress(0.0)
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures={executor.submit(fundamentals_for_stock,symbol):symbol for symbol in todo}
                for i,future in enumerate(as_completed(futures)):
                    try:value=nse_market_cap_crore(future.result())
                    except Exception:value=np.nan
                    cache[futures[future]]={'value':value,'saved_at':time.time()}
                    progress.progress((i+1)/len(todo))
            progress.empty()
    frame['Market Cap (₹ Cr)']=[cache.get(symbol,{}).get('value',np.nan) for symbol in frame.Symbol]
    st.caption('Nifty memberships use current official index lists. Market cap is the latest available Yahoo Finance value in ₹ crore, rounded for display; it is not historical market cap for the selected period. — means unavailable. Cached for 6 hours; only matching stocks are fetched.')
    return frame


def render_nse_percentage_view(group,default_symbols):
    st.markdown('#### 📊 By Percentage')
    controls=st.columns([2,1,1])
    period=controls[0].selectbox('Trading period',list(NSE_PERCENT_PERIODS),key='nse_pct_period')
    direction=controls[1].selectbox('Show',['Gainer','Loser'],key='nse_pct_direction')
    threshold=controls[2].number_input('Minimum move %',min_value=0.0,value=50.0,step=5.0,key='nse_pct_threshold')
    history='5y' if period=='5 Years' else '2y' if period in ['1 Year','2 Years'] else '1y'
    st.caption('Gainer 50: +50% or higher · Loser 50: −50% or lower. No upper cap. Weeks/months use 5/10/21/63/126 trading sessions. Year windows use 252/504/1260 sessions, or a complete calendar-year span.')
    state=st.session_state.setdefault('nse_percentage_data',{})
    if st.button('Load / Update percentage data',type='primary',key='nse_pct_build',use_container_width=True):
        with loading_stopwatch('Loading selected-period prices and sector labels…'):
            try:
                symbols=list(dict.fromkeys(default_symbols)) if group=='All NSE' else nse_sector_constituents(group).Symbol.tolist()
            except Exception as error:
                st.error('Could not load the selected index constituents: '+str(error));return
            metadata={}
            for catalog in dict.fromkeys(['Total Market','NIFTY 500',group if group!='All NSE' else 'Total Market']):
                try:
                    for _,r in nse_sector_constituents(catalog).iterrows():metadata[str(r.Symbol)]={'company':str(r['Company Name']),'sector':str(r.Industry)}
                except Exception:pass
            classic_period_snapshot(tuple(symbols),history)
            state.update(group=group,symbols=symbols,metadata=metadata)
    symbols=state.get('symbols',list(default_symbols)) if state.get('group')==group else list(default_symbols)
    metadata=state.get('metadata',{}) if state.get('group')==group else {}
    shared=st.session_state.get('shared_nse_price_cache',{}).get('records',{})
    saved=price_request_state()['classic'];rows=[]
    for symbol in symbols:
        candidates=[shared.get(symbol)]+[bucket.get(symbol,{}).get('record') for bucket in saved.values()]
        candidates=[r for r in candidates if r and r.get('closes')]
        record=max(candidates,key=lambda r:(r['last_date'],len(r['closes']))) if candidates else None
        value=nse_percentage_return(record,period)
        data=metadata.get(symbol,{})
        rows.append({'Symbol':symbol,'Stock Name':data.get('company',symbol),'Change %':value,'Sector / Business':data.get('sector','Unclassified'),'Price Date':(record or {}).get('last_date','Unavailable')})
    frame=pd.DataFrame(rows)
    if frame.empty:st.info('No stocks available for this universe.');return
    available=int(frame['Change %'].notna().sum());result=nse_percentage_filter(frame,direction,threshold)
    st.caption(f'{available:,}/{len(symbols):,} stocks have sufficient saved history · {len(result):,} match · dates shown per stock. Unavailable history is excluded. Sector labels use NSE industry classifications.')
    if st.session_state.get('classic_load_notice'):st.warning(st.session_state['classic_load_notice'])
    if available==0:st.info('Click Load / Update percentage data. Changing the threshold or Gainer/Loser uses saved prices without downloading again.');return
    if result.empty:st.info(f'No stocks match {direction.lower()} ≥ {threshold:g}% for {period} in the available data.');return
    result=nse_percentage_membership_cap(result.copy())
    result['Screener']=[nse_screener_url(symbol) for symbol in result.Symbol]
    result.insert(0,'No.',range(1,len(result)+1))
    st.caption('🟢 Gains · 🔴 Falls · Coloured sector cells identify groups. Click View on Screener to open the stock’s details in a new tab.')
    st.dataframe(nse_percentage_style(result),use_container_width=True,hide_index=True,height=min(650,38+len(result)*35),column_config={'Market Cap (₹ Cr)':st.column_config.NumberColumn(format='%.0f'),'Screener':st.column_config.LinkColumn('Screener',display_text='View on Screener')})
    st.download_button('Download matching stocks',result.to_csv(index=False),'nse_percentage_matches.csv','text/csv',key='nse_pct_csv')


@st.cache_resource(show_spinner=False)
def fast_percentage_store():
    import sqlite3
    folder=Path('.nse_fast');folder.mkdir(exist_ok=True)
    store={'lock':threading.RLock(),'records':{},'meta':{},'groups':{},'frame':pd.DataFrame(),'path':str(folder/'percentage.sqlite3'),'version':0}
    with sqlite3.connect(store['path']) as db:
        db.execute('CREATE TABLE IF NOT EXISTS stocks (symbol TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS config (name TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        for symbol,payload in db.execute('SELECT symbol,payload FROM stocks'):
            try:store['records'][symbol]=json.loads(payload)
            except Exception:pass
        for name,payload in db.execute('SELECT name,payload FROM config'):
            try:store[name]=json.loads(payload)
            except Exception:pass
    fast_percentage_rebuild(store)
    return store


def fast_percentage_merge(old,record,full=False):
    previous=(old or {}).get('record',{})
    dates={str(day):float(value) for day,value in previous.get('closes',[]) if float(value)>0}
    for day,value in (record or {}).get('closes',[]):
        if np.isfinite(float(value)) and float(value)>0:dates[str(day)]=float(value)
    days=sorted(dates)[-1261:]
    return {'record':{'closes':[[day,dates[day]] for day in days],'last_date':days[-1] if days else ''},
            'full':bool(full or (old or {}).get('full'))}


def fast_percentage_rebuild(store):
    rows=[]
    for symbol,entry in store['records'].items():
        record=entry['record'];meta=store['meta'].get(symbol,{})
        row={'Symbol':symbol,'Stock Name':meta.get('company',symbol),'Sector / Business':meta.get('sector','Unclassified'),
             'Price Date':record.get('last_date',''),'Nifty Membership':meta.get('membership','Unavailable'),
             'Market Cap (₹ Cr)':meta.get('cap',np.nan),'Screener':nse_screener_url(symbol)}
        for period in NSE_PERCENT_PERIODS:row['return:'+period]=nse_percentage_return(record,period)
        rows.append(row)
    store['frame']=pd.DataFrame(rows);store['version']+=1


def fast_percentage_save(store,symbols):
    import sqlite3
    with sqlite3.connect(store['path'],timeout=30) as db:
        db.executemany('INSERT OR REPLACE INTO stocks VALUES (?,?)',[(symbol,json.dumps(store['records'][symbol])) for symbol in symbols if symbol in store['records']])
        for name in ['meta','groups']:
            db.execute('INSERT OR REPLACE INTO config VALUES (?,?)',(name,json.dumps(store[name])))


def fast_percentage_import(store):
    # Copy already downloaded prices; this does not request or alter old views.
    changed=[]
    sources=[st.session_state.get('shared_nse_price_cache',{}).get('records',{})]
    for bucket in price_request_state()['classic'].values():sources.append({symbol:entry.get('record') for symbol,entry in bucket.items()})
    for source in sources:
        for symbol,record in source.items():
            if not record or not record.get('closes'):continue
            previous=store['records'].get(symbol)
            current=fast_percentage_merge(previous,record)
            if current!=previous:store['records'][symbol]=current;changed.append(symbol)
    if changed:fast_percentage_save(store,set(changed));fast_percentage_rebuild(store)


def fast_percentage_update(store,symbols):
    from collections import defaultdict
    today=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat()
    requests_by_start=defaultdict(list)
    for symbol in symbols:
        entry=store['records'].get(symbol,{})
        if entry.get('full') and entry.get('record',{}).get('last_date'):
            start=(pd.Timestamp(entry['record']['last_date'])-pd.Timedelta(days=7)).date().isoformat()
        else:start=None
        requests_by_start[start].append(symbol)
    total=len(symbols);done=0;notice='';progress=st.progress(0.0);status=st.empty()
    try:
        for start,group in requests_by_start.items():
            for offset in range(0,len(group),70):
                batch=group[offset:offset+70];tickers=[symbol+'.NS' for symbol in batch]
                opts={'start':start} if start else {'period':'5y'}
                try:downloaded,limited=limited_price_download(tickers,interval='1d',group_by='ticker',auto_adjust=False,progress=False,**opts)
                except Exception as exc:notice='Update stopped; saved prices retained. '+str(exc);return notice
                changed=[]
                for symbol,ticker in zip(batch,tickers):
                    frame=market_cache_frame(downloaded,symbol,ticker,len(batch))
                    if frame.empty or 'Close' not in frame:continue
                    record=market_cache_merge(None,frame,today)
                    if record:
                        store['records'][symbol]=fast_percentage_merge(store['records'].get(symbol),record,full=start is None)
                        changed.append(symbol)
                fast_percentage_save(store,changed)
                done+=len(batch);progress.progress(done/max(total,1));status.caption(f'Updated {done:,}/{total:,} stocks · existing prices retained')
                if limited:return 'Price provider limited requests. Saved prices retained; try updating later.'
    finally:
        progress.empty();status.empty();fast_percentage_rebuild(store)
    return notice


def fast_percentage_price_pair(latest,change):
    try:
        latest=float(latest);factor=1+float(change)/100
        if not np.isfinite(latest) or not np.isfinite(factor) or latest<=0 or factor<=0:return 'Unavailable'
        old=latest/factor
        number=lambda value:format(value,',.2f').rstrip('0').rstrip('.')
        return '₹'+number(old)+' → ₹'+number(latest)
    except (TypeError,ValueError):return 'Unavailable'


def fast_percentage_trend_svg(record,period):
    import math
    history=(record or {}).get('closes',[])
    count=NSE_PERCENT_PERIODS[period]
    values=[float(v) for _,v in history[-count-1:] if math.isfinite(float(v)) and float(v)>0]
    if len(values)<2:return 'Unavailable'
    colour='#16a34a' if values[-1]>values[0] else '#dc2626' if values[-1]<values[0] else '#64748b'
    minimum=min(values);maximum=max(values);span=maximum-minimum
    indices=sorted(set([0,len(values)-1]+[round(i*(len(values)-1)/119) for i in range(min(120,len(values)))])) if len(values)>120 else list(range(len(values)))
    points=' '.join(f'{4+88*i/(len(values)-1):.2f},{22-18*(values[i]-minimum)/span if span else 13:.2f}' for i in indices)
    ticks={
        '1 Day':[(0,'Prev'),(1,'1d')],
        '1 Week':[(1,'1d'),(3,'3d'),(5,'5d')],
        '2 Weeks':[(1,'1d'),(5,'5d'),(10,'10d')],
        '1 Month':[(5,'1w'),(10,'2w'),(21,'1m')],
        '3 Months':[(21,'1m'),(42,'2m'),(63,'3m')],
        '6 Months':[(21,'1m'),(63,'3m'),(126,'6m')],
        '1 Year':[(63,'3m'),(126,'6m'),(252,'1y')],
        '2 Years':[(126,'6m'),(252,'1y'),(504,'2y')],
        '5 Years':[(252,'1y'),(756,'3y'),(1260,'5y')],
    }[period]
    available=len(values)-1
    axis=''
    for session,label in ticks:
        if session>available:continue
        x=4+88*session/available
        anchor='start' if x<16 else 'end' if x>82 else 'middle'
        axis+=f'<line x1="{x:.2f}" y1="24" x2="{x:.2f}" y2="26" stroke="#64748b"/><text x="{x:.2f}" y="33" text-anchor="{anchor}" font-size="8" fill="#334155">{label}</text>'
    title=html.escape(f'{period}: ₹{values[0]:,.2f} → ₹{values[-1]:,.2f}. Saved closing prices; labels show elapsed trading sessions (1 week = 5, 1 month = 21).')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="35" viewBox="0 0 96 35" role="img" aria-label="{title}"><title>{title}</title><polyline points="{points}" fill="none" stroke="{colour}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/><line x1="4" y1="24" x2="92" y2="24" stroke="#cbd5e1" stroke-width="0.5"/>{axis}</svg>'



def fast_percentage_centered_table(frame):
    display=frame.copy()
    for column in display.select_dtypes(include=['object','string']).columns:
        display[column]=display[column].map(lambda value:html.escape(str(value)) if pd.notna(value) else '—')
    display['Screener']=[
        '<a href="'+html.escape(str(url),quote=True)+'" target="_blank" rel="noopener noreferrer">Screener ↗</a>' for url in frame['Screener']]
    if 'Trend' in frame:display['Trend']=frame['Trend']
    styled=nse_percentage_style(display).hide(axis='index').set_properties(**{'text-align':'center','vertical-align':'middle'})
    styled=styled.set_table_styles([{'selector':'th','props':[('text-align','center'),('vertical-align','middle')]}])
    st.markdown('<style>.fast-centred{overflow-x:auto;border-radius:10px}.fast-centred table{width:100%;border-collapse:collapse;font-size:13px}.fast-centred th,.fast-centred td{text-align:center!important;vertical-align:middle!important;padding:3px 5px;border:1px solid #e2e8f0;white-space:nowrap}.fast-centred th{background:#e0e7ff;color:#172033}.fast-centred svg{display:block;margin:auto}.fast-centred a{color:#1d4ed8;text-decoration:none}.fast-centred a:hover{text-decoration:underline}</style><div class="fast-centred">'+styled.to_html()+'</div>',unsafe_allow_html=True)


def fast_percentage_filter_sort(frame,min_cap=None,max_cap=None,sort_by='Percentage Change',sort_order='High → Low'):
    result=frame.copy()
    result['Market Cap (₹ Cr)']=pd.to_numeric(result['Market Cap (₹ Cr)'],errors='coerce')
    if min_cap is not None:result=result[result['Market Cap (₹ Cr)']>=min_cap]
    if max_cap is not None:result=result[result['Market Cap (₹ Cr)']<=max_cap]
    column='Market Cap (₹ Cr)' if sort_by=='Market Cap' else 'Change %'
    result[column]=pd.to_numeric(result[column],errors='coerce')
    return result.sort_values(column,ascending=sort_order=='Low → High',na_position='last',kind='mergesort').reset_index(drop=True)


def render_fast_percentage():
    st.markdown('## ⚡ Fast — By Percentage')
    st.caption('Separate trial page. Filters use precomputed saved returns and make no market-data requests. Prices update only when you click Update prices.')
    store=fast_percentage_store()
    controls=st.columns([2,2,1,1])
    group=controls[0].selectbox('Universe',['All NSE','NIFTY 50','NIFTY 100','NIFTY 500','NIFTY Midcap','NIFTY Smallcap'],index=1,key='fast_universe')
    period=controls[1].selectbox('Trading period',list(NSE_PERCENT_PERIODS),key='fast_period')
    direction=controls[2].selectbox('Show',['Gainer','Loser'],key='fast_direction')
    threshold=controls[3].number_input('Minimum move %',min_value=0.0,value=50.0,step=5.0,key='fast_threshold')
    extra=st.columns(4)
    min_text=extra[0].text_input('Min market cap (₹ crore)',placeholder='No minimum',key='fast_min_cap')
    max_text=extra[1].text_input('Max market cap (₹ crore)',placeholder='No maximum',key='fast_max_cap')
    sort_by=extra[2].selectbox('Sort by',['Percentage Change','Market Cap'],key='fast_sort_by')
    sort_order=extra[3].selectbox('Order',['High → Low','Low → High'],key='fast_sort_order')
    try:
        min_cap=float(min_text.replace(',','').strip()) if min_text.strip() else None
        max_cap=float(max_text.replace(',','').strip()) if max_text.strip() else None
        if any(value is not None and (not np.isfinite(value) or value<0) for value in (min_cap,max_cap)):
            raise ValueError('Use a finite, non-negative amount.')
        if min_cap is not None and max_cap is not None and min_cap>max_cap:
            raise ValueError('Minimum market cap must not exceed maximum.')
    except ValueError as exc:
        st.error('Check market-cap limits: '+str(exc));return
    buttons=st.columns(3)
    import_existing=buttons[0].button('Use already loaded prices',key='fast_import')
    update=buttons[1].button('Update prices',type='primary',key='fast_update')
    details=buttons[2].button('Update Nifty labels / market caps',key='fast_details')
    with store['lock']:
        if import_existing:
            with loading_stopwatch('Copying existing prices into Fast…'):fast_percentage_import(store)
        if update:
            with loading_stopwatch('Updating Fast prices…'):
                try:
                    if group=='All NSE':symbols=universe()
                    else:
                        catalog=nse_sector_constituents(group);symbols=catalog.Symbol.tolist()
                        for _,r in catalog.iterrows():store['meta'].setdefault(r.Symbol,{}).update(company=str(r['Company Name']),sector=str(r.Industry))
                    store['groups'][group]=symbols
                    fast_percentage_import(store)
                    notice=fast_percentage_update(store,symbols)
                    if notice:st.warning(notice)
                except Exception as exc:st.error('Update failed; saved data kept. '+str(exc))
        table=store['frame'].copy()
        symbols=store['groups'].get(group)
        if symbols is not None and not table.empty:table=table[table.Symbol.isin(symbols)]
        elif group!='All NSE':table=pd.DataFrame()
        if table.empty:
            st.info('Click Update prices once to build this universe. For a first trial, NIFTY 50 is selected. Later filter changes reuse the saved dataset.');return
        result=table.rename(columns={'return:'+period:'Change %'})
        result=result.drop(columns=[c for c in result if c.startswith('return:')])
        result=nse_percentage_filter(result,direction,threshold)
        if details:
            with loading_stopwatch('Updating labels and market caps for filtered stocks…'):
                memberships={}
                for label,index in [('N50','NIFTY 50'),('N100','NIFTY 100'),('N500','NIFTY 500')]:
                    try:memberships[label]=set(nse_sector_constituents(index).Symbol)
                    except Exception:memberships[label]=None
                for symbol in result.Symbol:
                    meta=store['meta'].setdefault(symbol,{})
                    meta['membership']=nse_membership_label(symbol,memberships)
                    meta['cap']=nse_market_cap_crore(fundamentals_for_stock(symbol))
                fast_percentage_save(store,[]);fast_percentage_rebuild(store)
                caps={symbol:store['meta'][symbol] for symbol in result.Symbol}
                result['Nifty Membership']=[caps[s].get('membership','Unavailable') for s in result.Symbol]
                result['Market Cap (₹ Cr)']=[caps[s].get('cap',np.nan) for s in result.Symbol]
    result=fast_percentage_filter_sort(result,min_cap,max_cap,sort_by,sort_order)
    if min_cap is not None or max_cap is not None:
        st.caption('Market-cap limits use saved values in ₹ crore. Stocks without a saved cap are excluded. Use Update Nifty labels / market caps to fill them.')
    st.caption(f'{table["Change %"].notna().sum() if "Change %" in table else table["return:"+period].notna().sum():,}/{len(table):,} stocks have sufficient history · {len(result):,} match. Price dates shown per stock; saved data may be old until updated.')
    st.caption('First build downloads up to 5 years. Later updates merge recent dates with a 7-day overlap, without downloading the whole history. Older gaps are not automatically audited. Local cache survives browser sessions but hosting resets may erase it; Google Sheet backup is not connected in this trial.')
    if result.empty:st.info('No saved stocks match this filter.');return
    latest={symbol:entry['record']['closes'][-1][1] for symbol,entry in store['records'].items() if entry['record'].get('closes')}
    result['Price']=[fast_percentage_price_pair(latest.get(symbol),change) for symbol,change in zip(result.Symbol,result['Change %'])]
    result['Date']=pd.to_datetime(result['Price Date'],errors='coerce').dt.strftime('%d/%m/%Y').fillna('Unavailable')
    st.caption('Price: starting close for your selected period → latest saved close.')
    result['Trend']=[fast_percentage_trend_svg(store['records'].get(symbol,{}).get('record'),period) for symbol in result.Symbol]
    result=result[['Stock Name','Date','Change %','Price','Market Cap (₹ Cr)','Nifty Membership','Screener','Trend']].copy()
    result.insert(0,'No.',range(1,len(result)+1))
    st.caption('Trend: green = net increase, red = decrease, grey = unchanged. Bottom labels show elapsed trading time: d = sessions, w = 5 sessions, m = 21 sessions, y = 252 sessions. Long graphs are sampled.')
    fast_percentage_centered_table(result)
    st.download_button('Download Fast results',result.drop(columns=['Trend']).to_csv(index=False),'fast_percentage.csv','text/csv',key='fast_csv')


@st.cache_data(ttl=900,show_spinner=False)
def independent_stock_chart_data(symbol,mode,selected_date,period):
    today=datetime.now(ZoneInfo('Asia/Kolkata')).date()
    intraday=mode=='Date' or period=='1 Day'
    if intraday:
        start=date.fromisoformat(selected_date) if mode=='Date' else today
        # Sundays/holidays stay empty in Date mode; never substitute another day.
        if mode=='Period':
            options={'period':'5d','interval':'5m'}
        else:
            options={'start':start.isoformat(),'end':(start+timedelta(days=1)).isoformat(),'interval':'5m'}
    else:
        offsets={'1 Week':pd.DateOffset(weeks=1),'1 Month':pd.DateOffset(months=1),
                 '3 Months':pd.DateOffset(months=3),'6 Months':pd.DateOffset(months=6),
                 '1 Year':pd.DateOffset(years=1),'2 Years':pd.DateOffset(years=2),'5 Years':pd.DateOffset(years=5)}
        start=(pd.Timestamp(today)-offsets[period]).date()
        options={'start':start.isoformat(),'end':(today+timedelta(days=1)).isoformat(),'interval':'1d'}
    frame,limited=limited_price_download([symbol+'.NS'],auto_adjust=False,progress=False,**options)
    if limited:raise PriceRateLimited('Price provider limited requests. Please try later.')
    if frame.empty:return frame
    if isinstance(frame.columns,pd.MultiIndex):frame.columns=frame.columns.get_level_values(0)
    frame=frame.dropna(subset=['Close']).copy()
    index=pd.DatetimeIndex(frame.index)
    if intraday:
        index=index.tz_localize('Asia/Kolkata') if index.tz is None else index.tz_convert('Asia/Kolkata')
        frame.index=index
        target=date.fromisoformat(selected_date) if mode=='Date' else index[-1].date()
        frame=frame[index.date==target]
    return frame


def render_independent_stock_charts():
    st.markdown('## 📈 Charts')
    st.caption('Two independent views: one selected date, or a recent period ending at the latest available trading day.')
    saved=fast_percentage_store()
    symbols=sorted(set(saved['records'])|set(FALLBACK))
    if st.button('Load full NSE stock list',key='chart_load_symbols'):
        st.session_state['chart_symbols']=universe()
    symbols=sorted(set(symbols)|set(st.session_state.get('chart_symbols',[])))
    with st.form('independent_chart_form'):
        stock=st.selectbox('Stock — type to search',symbols,key='chart_stock')
        custom=st.text_input('Or enter another NSE symbol',placeholder='Example: AUGMONT',key='chart_custom_symbol')
        mode=st.radio('Graph option',['Date','Period'],horizontal=True,key='chart_mode')
        cols=st.columns(2)
        chosen=cols[0].date_input('Date — used only in Date mode',value=datetime.now(ZoneInfo('Asia/Kolkata')).date(),format='DD/MM/YYYY',key='chart_date')
        period=cols[1].selectbox('Period — used only in Period mode',['1 Day','1 Week','1 Month','3 Months','6 Months','1 Year','2 Years','5 Years'],key='chart_range')
        submit=st.form_submit_button('Show graph',type='primary')
    if submit:
        symbol=(custom.strip() or stock).upper().removesuffix('.NS')
        if not re.fullmatch(r'[A-Z0-9&._-]+',symbol):st.error('Enter a valid NSE symbol.');return
        if mode=='Date' and chosen>datetime.now(ZoneInfo('Asia/Kolkata')).date():
            st.warning('Future dates have no trading data.');return
        try:
            with loading_stopwatch('Loading selected stock graph…'):
                frame=independent_stock_chart_data(symbol,mode,chosen.isoformat(),period)
            st.session_state['independent_chart_result']=(symbol,mode,chosen.isoformat(),period,frame)
        except Exception as exc:
            st.session_state.pop('independent_chart_result',None)
            st.error('Graph unavailable: '+str(exc));return
    result=st.session_state.get('independent_chart_result')
    if result is None:return
    symbol,mode,chosen,period,frame=result
    title=symbol+' · '+(date.fromisoformat(chosen).strftime('%d/%m/%Y') if mode=='Date' else period)
    st.markdown('#### '+html.escape(title))
    if frame.empty:
        st.info('No prices available for this selection. A selected date may be a holiday, or its intraday history may be unavailable from the provider. Another day is not substituted.');return
    colour='#16a34a' if float(frame.Close.iloc[-1])>=float(frame.Close.iloc[0]) else '#dc2626'
    fig=go.Figure(go.Scatter(x=frame.index,y=frame.Close,mode='lines',line=dict(color=colour,width=2),name='Price',hovertemplate='%{x}<br>₹%{y:,.2f}<extra></extra>'))
    fig.update_layout(height=320,margin=dict(l=10,r=10,t=10,b=10),xaxis_title='Time (IST)' if mode=='Date' or period=='1 Day' else 'Date',yaxis_title='Price (₹)',showlegend=False)
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Displayed data: '+frame.index[0].strftime('%d/%m/%Y')+' to '+frame.index[-1].strftime('%d/%m/%Y')+'. Date / 1 Day charts use 5-minute prices when available; longer periods use daily closes. Prices are cached for 15 minutes.')


def render_nse_sector_view(group):
    st.markdown('#### 🧩 Sector-wise Stocks')
    periods={'1 Day':1,'5 Days':5,'1 Month':21,'3 Months':63,'6 Months':126,'1 Year':252,'5 Years':1260}
    controls=st.columns([2,1])
    period=controls[0].selectbox('Performance period',list(periods),key='nse_sector_period')
    layout=controls[1].selectbox('Display',['Compact tiles','Treemap'],key='nse_sector_layout')
    st.caption('Green = positive · Red = negative · Dark neutral = zero · Grey = insufficient / unavailable history. Compact tiles show symbol + change without empty space. Hover for details; Treemap supports sector zoom.')
    with loading_stopwatch('Preparing stock list and sector labels…'):
        try:
            if group=='All NSE':symbols=list(dict.fromkeys(universe()))
            else:symbols=nse_sector_constituents(group).Symbol.tolist()
        except Exception:
            st.error('The selected NSE constituent list is unavailable. Please retry later.');return
        metadata={}
        for catalog_group in ['Total Market','NIFTY 500',group if group!='All NSE' else 'Total Market']:
            try:
                for _,r in nse_sector_constituents(catalog_group).iterrows():metadata[str(r.Symbol)]={'sector':str(r.Industry),'company':str(r['Company Name'])}
            except Exception:pass
    st.caption(f'{len(symbols):,} requested stocks · NSE industry classifications are used as sector groups. Additional Yahoo sector labels are marked “Yahoo”.')
    col1,col2=st.columns(2)
    if col1.button('Build / Refresh Sector Heatmap',type='primary',use_container_width=True,key='nse_sector_build'):
        with loading_stopwatch(f'Loading saved prices / updating {len(symbols):,} stocks…'):
            bulk_snapshot(tuple(symbols),'5y',force_refresh=True)
        st.session_state['nse_sector_loaded']=tuple(symbols)
    extra=st.session_state.setdefault('nse_sector_extra',{})
    unknown=[symbol for symbol in symbols if symbol not in metadata and symbol not in extra]
    if col2.button('Fetch missing sector labels',use_container_width=True,key='nse_sector_labels',disabled=not unknown):
        from concurrent.futures import ThreadPoolExecutor,as_completed
        status=st.empty();progress=st.progress(0)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures={executor.submit(nse_extra_sector,symbol):symbol for symbol in unknown}
            for i,future in enumerate(as_completed(futures)):
                data=future.result()
                if data:extra[futures[future]]=data
                progress.progress((i+1)/len(unknown));status.caption(f'Sector labels checked: {i+1:,}/{len(unknown):,}')
        progress.empty();status.empty()
    records=market_cache_state()['records'];rows=[]
    for symbol in symbols:
        record=records.get(symbol);closes=(record or {}).get('closes',[])
        data=metadata.get(symbol) or extra.get(symbol) or {}
        label=data.get('sector') or 'Unclassified'
        if symbol not in metadata and label!='Unclassified':label+=' · Yahoo'
        rows.append({'Symbol':symbol,'Company':data.get('company') or symbol,'Sector':label,
                     'Return':nse_sector_return(record,periods[period]),'Latest':float(closes[-1][1]) if closes else np.nan,
                     'Date':closes[-1][0] if closes else 'Unavailable'})
    frame=pd.DataFrame(rows)
    if not frame.Latest.notna().any():
        st.info('Click Build / Refresh Sector Heatmap to load prices.');return
    st.caption(f'{frame.Latest.notna().sum():,}/{len(frame):,} stocks have prices · {frame.Return.notna().sum():,} have enough history for {period} · {frame.Sector.eq("Unclassified").sum():,} unclassified. Price dates are shown on hover; cached stocks can have different dates.')
    if layout=='Compact tiles':st.markdown(nse_sector_compact_html(frame),unsafe_allow_html=True)
    else:st.plotly_chart(nse_sector_figure(frame,period),use_container_width=True)
    st.download_button('Export selected-period sector data',frame.to_csv(index=False),'nse_sector_performance.csv','text/csv')



st.markdown("""<style>
/* Keep previous content legible while a refresh runs. */
[data-stale="true"]{opacity:1!important}
/* Contrast fixes apply to controls across all modules. */
[data-testid="stWidgetLabel"] p,[data-testid="stRadio"] label p,[data-testid="stCheckbox"] label p{color:#e2e8f0!important;opacity:1!important}
[data-testid="stTabs"] [role="tab"]{color:#cbd5e1!important;opacity:1!important}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#60a5fa!important;font-weight:700}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]{color:#e2e8f0}
[data-testid="stButton"] button,[data-testid="stDownloadButton"] button,[data-testid="stLinkButton"] a{background-color:#14243c;color:#f8fafc;border-color:#38577d}
[data-testid="stButton"] button p,[data-testid="stDownloadButton"] button p,[data-testid="stLinkButton"] a p{color:inherit!important}
[data-testid="stButton"] button[kind="primary"]{background:#1d4ed8;color:white}
[data-baseweb="select"]{color:#172033}
[data-baseweb="select"] input,[data-baseweb="input"] input,[data-baseweb="textarea"] textarea{color:#172033!important}
</style>""",unsafe_allow_html=True)

st.sidebar.markdown("## 📈 NSE PRO")
page=st.sidebar.radio("Open module",["🏠 Dashboard","📌 Watchlist","🔥 Market Heatmap","🧠 Pro Analyzer","🚀 Swing Screeners","📰 Stock News","🎯 Brokerage Calls","🌐 All NSE Performance","⚡ Fast","📈 Charts","🇺🇸 All US Stocks","⚡ Circuit & Volatility","🏦 Institutional Watch","💾 Market Data Hub"],key="main_page")


st.sidebar.markdown("---")
st.sidebar.link_button(
    "🛠️ Open app.py on GitHub",
    "https://github.com/raahaavaan-hub/nse-pro-stock-analyzer/blob/main/app.py",
    use_container_width=True
)
st.sidebar.caption("Open the live app.py file directly when you want to update the website.")

WATCHLIST_FILE=Path(__file__).with_name("watchlists.json")

def WL_default():
    return {"lists":[{"name":f"Watchlist {i}","stocks":[]} for i in range(1,11)]}

def WL_normalize(raw):
    source=raw.get("lists",[]) if isinstance(raw,dict) else []
    result=WL_default()
    for i in range(10):
        entry=source[i] if i<len(source) and isinstance(source[i],dict) else {}
        result["lists"][i]["name"]=str(entry.get("name") or f"Watchlist {i+1}").strip()[:32]
        stocks=[]
        for item in entry.get("stocks",[]) if isinstance(entry.get("stocks",[]),list) else []:
            if not isinstance(item,dict):continue
            symbol=str(item.get("symbol","")).strip().upper().removesuffix(".NS")
            if not re.fullmatch(r"[A-Z0-9&.\-]{1,20}",symbol):continue
            try:dt=date.fromisoformat(str(item.get("date",""))).isoformat()
            except ValueError:dt=date.today().isoformat()
            def level(key):
                try:
                    v=float(item.get(key))
                    return v if np.isfinite(v) and v>0 else None
                except (TypeError,ValueError):return None
            stocks.append({"date":dt,"stock":str(item.get("stock") or symbol).strip()[:70],
                           "symbol":symbol,"high":level("high"),"stoploss":level("stoploss")})
        result["lists"][i]["stocks"]=stocks[:1000]
    return result

def WL_load():
    try:return WL_normalize(json.loads(WATCHLIST_FILE.read_text(encoding="utf-8")))
    except (OSError,ValueError,TypeError):return WL_default()

def WL_save(value):
    try:
        WATCHLIST_FILE.write_text(json.dumps(WL_normalize(value),ensure_ascii=False,indent=2),encoding="utf-8")
        return True
    except OSError:return False

@st.cache_data(ttl=86400,show_spinner=False)
def WL_catalog():
    try:
        session=requests.Session();session.headers.update(HEADERS)
        try:session.get("https://www.nseindia.com",timeout=8)
        except Exception:pass
        response=session.get(NSE_URL,timeout=15);response.raise_for_status()
        frame=pd.read_csv(io.BytesIO(response.content));frame.columns=[str(x).strip() for x in frame.columns]
        names=[]
        for _,row in frame.iterrows():
            symbol=str(row.get("SYMBOL","")).strip().upper()
            company=str(row.get("NAME OF COMPANY",symbol)).strip()
            if re.fullmatch(r"[A-Z0-9&.\-]{1,20}",symbol):names.append((company,symbol))
        if names:return sorted(set(names),key=lambda x:x[0].lower())
    except Exception:pass
    return [(symbol,symbol) for symbol in sorted(set(universe()))]

@st.cache_data(ttl=300,show_spinner=False)
def WL_quotes(symbols):
    out={}
    for start in range(0,len(symbols),100):
        batch=list(symbols[start:start+100]);tickers=[symbol+".NS" for symbol in batch]
        try:
            prices=yf.download(tickers,period="5d",interval="1d",group_by="ticker",
                               auto_adjust=False,progress=False,threads=True)
            if prices is None or prices.empty:continue
            for symbol,ticker in zip(batch,tickers):
                try:
                    closes=(prices[ticker]["Close"] if isinstance(prices.columns,pd.MultiIndex) else prices["Close"]).dropna()
                    if closes.empty:continue
                    latest=float(closes.iloc[-1]);previous=float(closes.iloc[-2]) if len(closes)>1 else None
                    if np.isfinite(latest):out[symbol]={"latest":latest,"previous":previous if previous and np.isfinite(previous) else None,
                                                       "asof":str(closes.index[-1].date())}
                except Exception:continue
        except Exception:continue
    return out

def WL_market_rows(stocks,quotes):
    rows=[]
    for number,item in enumerate(stocks,1):
        q=quotes.get(item["symbol"])
        latest=q["latest"] if q else None
        previous=q["previous"] if q else None
        daily=(latest/previous-1)*100 if latest is not None and previous else None
        high=item.get("high");stop=item.get("stoploss")
        price=f"₹{latest:,.2f}" if latest is not None else "—"
        if daily is not None:price+=f" {'▲' if daily>=0 else '▼'} {daily:+.2f}%"
        rows.append({"Sl. No.":number,"Date":item["date"],"Stock Name":item["stock"],
                     "Stop Loss":f"₹{stop:,.2f}" if stop else "—",
                     "Current Market Price":price,
                     "Target Price":f"₹{high:,.2f}" if high else "—"})
    return rows


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

elif page=="📌 Watchlist":
    st.markdown("<div class='hero'><div class='eyebrow'>MY STOCK IDEAS</div><h1>📌 Watchlist</h1><p>Ten named lists. Enter your target price and stop loss; compare them with the latest available NSE daily close.</p></div>",unsafe_allow_html=True)
    watch=WL_load()
    a,b,c=st.columns([1,1,2])
    with a:
        st.download_button("⬇️ Back up watchlists",data=json.dumps(watch,ensure_ascii=False,indent=2),
                           file_name="nse-pro-watchlists.json",mime="application/json",use_container_width=True)
    with b:
        uploaded=st.file_uploader("Restore backup",type="json",key="wl_restore")
    with c:
        if st.button("↻ Refresh market prices",use_container_width=True):
            WL_quotes.clear();st.rerun()
    if uploaded and st.button("Restore 10 lists from backup"):
        try:
            restored=WL_normalize(json.loads(uploaded.getvalue().decode("utf-8")))
            if WL_save(restored):st.rerun()
            else:st.error("Could not save the restored lists on this server.")
        except (ValueError,UnicodeDecodeError):st.error("Choose a valid watchlist JSON backup.")
    st.caption("Current Market Price shows the latest available daily close and its daily move, cached for five minutes. It may lag the live market. Your target price and stop loss remain your own entries. Back up the lists before redeploying the app.")
    labels=[f"{n+1} · {part['name']}" for n,part in enumerate(watch["lists"])]
    selected=st.radio("Your 10 watchlist tabs",labels,horizontal=True,key="wl_active_tab")
    i=labels.index(selected);current=watch["lists"][i]
    st.markdown(f"#### {html.escape(current['name'])} · {len(current['stocks'])}/1,000 stocks")
    rename_col,save_col=st.columns([4,1])
    with rename_col:new_name=st.text_input("Edit this tab name",value=current["name"],max_chars=32,key=f"wl_name_{i}")
    with save_col:
        st.write("")
        if st.button("Save name",key=f"wl_rename_{i}",use_container_width=True):
            watch["lists"][i]["name"]=new_name.strip() or f"Watchlist {i+1}"
            if WL_save(watch):st.rerun()
            else:st.error("Could not save on this server.")

    with st.form(f"wl_add_{i}",clear_on_submit=True):
        st.markdown("##### ＋ Add stock")
        catalog=WL_catalog()
        options=["Search by company name or NSE symbol..."]+[f"{name} · {symbol}" for name,symbol in catalog]
        chosen=st.selectbox("Stock name",options,key=f"wl_stock_search_{i}",
                            help="Click here and type the company name; matching NSE stocks appear in the dropdown.")
        when,high_col,stop_col=st.columns(3)
        with when:entry_date=st.date_input("Date",value=date.today(),key=f"wl_date_{i}")
        with high_col:high=st.number_input("Target Price ₹",min_value=0.0,step=0.05,value=0.0,key=f"wl_high_{i}")
        with stop_col:stop=st.number_input("Stop Loss ₹",min_value=0.0,step=0.05,value=0.0,key=f"wl_stop_{i}")
        add=st.form_submit_button("＋ Add stock",type="primary")
    if add:
        if chosen==options[0]:st.error("Choose a stock from the name search.")
        elif len(current["stocks"])>=1000:st.error("This tab already contains 1,000 stocks. Choose another tab.")
        elif high<=0 or stop<=0:st.error("Enter a target price and stop loss above ₹0.")
        else:
            name,symbol=catalog[options.index(chosen)-1]
            current["stocks"].append({"date":entry_date.isoformat(),"stock":name,"symbol":symbol,
                                      "high":float(high),"stoploss":float(stop)})
            if WL_save(watch):st.rerun()
            else:st.error("Could not save on this server. Download a backup of the lists.")

    if current["stocks"]:
        st.markdown("##### Saved stocks and price movement")
        symbols=tuple(sorted({row["symbol"] for row in current["stocks"]}))
        with loading_stopwatch("Loading latest available market closes..."):
            quotes=WL_quotes(symbols)
        st.dataframe(pd.DataFrame(WL_market_rows(current["stocks"],quotes)),hide_index=True,use_container_width=True)
        choices=[f"{j+1}. {row['stock']} · {row['symbol']} · {row['date']}" for j,row in enumerate(current["stocks"])]
        chosen_row=st.selectbox("Choose a saved stock to edit or delete",choices,key=f"wl_selected_row_{i}")
        row_index=choices.index(chosen_row);row=current["stocks"][row_index]
        with st.expander("✏️ Edit selected stock"):
            with st.form(f"wl_edit_{i}_{row_index}"):
                ec1,ec2,ec3=st.columns(3)
                with ec1:new_date=st.date_input("Date",value=date.fromisoformat(row["date"]),key=f"wl_edit_date_{i}_{row_index}")
                with ec2:new_high=st.number_input("Target Price ₹",min_value=0.0,value=float(row.get("high") or 0),key=f"wl_edit_high_{i}_{row_index}")
                with ec3:new_stop=st.number_input("Stop Loss ₹",min_value=0.0,value=float(row.get("stoploss") or 0),key=f"wl_edit_stop_{i}_{row_index}")
                update=st.form_submit_button("Save changes")
            if update:
                if new_high<=0 or new_stop<=0:st.error("Enter a target price and stop loss above ₹0.")
                else:
                    row.update({"date":new_date.isoformat(),"high":float(new_high),"stoploss":float(new_stop)})
                    if WL_save(watch):st.rerun()
                    else:st.error("Could not save on this server.")
        if st.button("🗑 Delete selected stock",key=f"wl_delete_{i}"):
            current["stocks"].pop(row_index)
            if WL_save(watch):st.rerun()
            else:st.error("Could not save on this server.")
    else:st.info("This tab is empty. Search for a stock above and click Add stock.")

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
        heat_force_refresh=st.button("↻ Refresh",use_container_width=True,key="heat_stock_refresh")

    move_filter=st.radio("Show",["All","🟢 Gainers","🔴 Losers","⚪ Unchanged"],horizontal=True,key="heat_move_filter")

    nifty50=["ADANIENT","ADANIPORTS","APOLLOHOSP","ASIANPAINT","AXISBANK","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BEL","BHARTIARTL","CIPLA","COALINDIA","DRREDDY","EICHERMOT","ETERNAL","GRASIM","HCLTECH","HDFCBANK","HDFCLIFE","HEROMOTOCO","HINDALCO","HINDUNILVR","ICICIBANK","INDUSINDBK","INFY","ITC","JIOFIN","JSWSTEEL","KOTAKBANK","LT","M&M","MARUTI","NESTLEIND","NTPC","ONGC","POWERGRID","RELIANCE","SBILIFE","SBIN","SHRIRAMFIN","SUNPHARMA","TATACONSUM","TATAMOTORS","TATASTEEL","TCS","TECHM","TITAN","TRENT","ULTRACEMCO","WIPRO"]

    all_syms=list(dict.fromkeys(universe()))
    if universe_name=="ALL NSE":
        syms=all_syms
    else:
        target={"NIFTY 50":50,"NIFTY 100":100,"NIFTY 200":200,"NIFTY 500":500}[universe_name]
        syms=(nifty50+[s for s in all_syms if s not in nifty50])[:target]

    period_column={"1 Day":"1D %","1 Week":"1W %","1 Month":"1M %",
                   "3 Months":"3M %","6 Months":"6M %","1 Year":"1Y %","5 Years":"5Y %"}[heat_period]

    def stock_heat_prices(symbols,period_label,force_refresh=False):
        snapshot=shared_market_snapshot(symbols,force_refresh=force_refresh)
        if snapshot.empty:
            return []
        result=[]
        for row in snapshot.to_dict("records"):
            last=float(row["Latest"]);change_pct=float(row[period_column])
            if not np.isfinite(change_pct):
                change_pct=0.0
            if change_pct<=-100:
                continue
            previous=last/(1+change_pct/100)
            result.append((row["Symbol"],last,last-previous,change_pct))
        return result

    with loading_stopwatch(f"Loading {len(syms):,} {universe_name} stocks · {heat_period}..."):
        rows=stock_heat_prices(syms,heat_period,force_refresh=heat_force_refresh)

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

    with loading_stopwatch(f"Loading complete research for {symbol}..."):
        info,hist,qpl,apl,qbs,abs_,qcf,acf,major,inst=PA_bundle(ticker)

    last=PA_num(PA_val(info,"currentPrice","regularMarketPrice"))
    if last is None and not hist.empty:last=float(hist["Close"].dropna().iloc[-1])
    prev=PA_num(PA_val(info,"previousClose"))
    change=(last-prev) if last is not None and prev else None
    pct=(change/prev*100) if change is not None and prev else None
    name=PA_val(info,"longName","shortName") or symbol

    st.markdown(f"## {name}  ·  NSE: {symbol}")
    st.link_button("📊 Open this stock in Screener", f"https://www.screener.in/company/{symbol}/", use_container_width=False)
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
        with loading_stopwatch("Scanning 500 liquid-listed symbols for technical setups..."):
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
        with loading_stopwatch("Downloading market history in batches..."):snap=bulk_snapshot(tuple(syms),"1y");res=run_screen(snap,name)
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
    with loading_stopwatch("Loading fresh market catalysts..."):
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
        with loading_stopwatch("Searching brokerage calls and comparing market prices..."):
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


elif page=="📈 Charts":
    render_independent_stock_charts()

elif page=="⚡ Fast":
    render_fast_percentage()

elif page=="🌐 All NSE Performance":
    st.markdown("<div class='hero'><div class='eyebrow'>NSE PERFORMANCE</div><h1>🌐 All NSE Performance</h1><p>Start with market statistics, then explore heat maps, then choose Classic Table or Smart Scanner.</p></div>",unsafe_allow_html=True)

    st.markdown("## 📊 Market Statistics")
    if st.button("↻ Refresh market statistics", key="refresh_nse_market_statistics"):
        nse_market_statistics.clear()
    official_stats = nse_market_statistics()
    stale = False
    if official_stats.get("source") == "NSE":
        st.session_state["nse_last_good_statistics"] = dict(official_stats)
    elif st.session_state.get("nse_last_good_statistics"):
        error = official_stats.get("error", "NSE is unavailable.")
        official_stats = dict(st.session_state["nse_last_good_statistics"])
        stale = True
        st.warning(f"{error} Showing the last successful snapshot below; it is not live. Click Refresh to retry.")
    else:
        st.warning(official_stats.get("error", "NSE statistics unavailable.") + " No successful snapshot is available. Click Refresh to retry.")
    if official_stats.get("source") == "NSE":
        st.caption(f"Official NSE Market Statistics · As on {official_stats.get('as_on')} IST" + (" · LAST SUCCESSFUL SNAPSHOT" if stale else ""))
    s1, s2, s3, s4 = st.columns(4)
    for column, label, key in zip([s1, s2, s3, s4], ["Stock Traded", "Advances", "Declines", "Unchanged"], ["stock_traded", "advances", "declines", "unchanged"]):
        column.metric(label, _nse_stat_display(official_stats.get(key)))
    t1, t2, t3, t4 = st.columns(4)
    for column, label, key in zip([t1, t2, t3, t4], ["52 Week High", "52 Week Low", "Upper Circuit", "Lower Circuit"], ["high52", "low52", "upper", "lower"]):
        column.metric(label, _nse_stat_display(official_stats.get(key)))

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
    view=st.radio("Choose view",["📋 Classic Table (Excel Style)","⚡ Smart Scanner","🧩 Sector-wise Stocks","📊 By Percentage","📈 Steady Uptrend"],horizontal=True,key="allnse_view")

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

    if view=="📈 Steady Uptrend":
        render_nse_steady_view(universe_group,use_syms)
    elif view=="📊 By Percentage":
        render_nse_percentage_view(universe_group,use_syms)
    elif view=="🧩 Sector-wise Stocks":
        render_nse_sector_view(universe_group)
    elif view=="📋 Classic Table (Excel Style)":
        st.markdown("### 📋 Classic Performance Table")
        c1,c2,c3=st.columns(3)
        history=c1.selectbox("History",["1y","2y","5y"],index=2,key="classic_history")
        sort_by=c2.selectbox("Sort by",["Symbol","Brokerage Call","Latest","1D %","1W %","1M %","3M %","6M %","1Y %","5Y %","RSI14","SMA20","SMA50","SMA200","52W High","52W Low","% of 52W High","Volume","Volume Ratio","Up Days 20"],index=2,key="classic_sort")
        order_options=["A → Z","Z → A"] if sort_by in ["Symbol","Brokerage Call"] else ["Largest → Smallest","Smallest → Largest"]
        order=c3.selectbox("Order",order_options,key="classic_order")

        if st.button("📊 Build / Refresh Classic Table",type="primary",use_container_width=True,key="classic_build"):
            with loading_stopwatch(f"Loading {len(use_syms):,} stocks..."):
                table,failed=classic_period_snapshot(tuple(use_syms),history)
                st.session_state['classic_df']=table
                st.session_state['classic_failed']=failed
                st.session_state['classic_selection']=(tuple(use_syms),history)

        if st.session_state.get('classic_selection')!=(tuple(use_syms),history):
            st.info('Click Build / Refresh to load the selected universe and history.')
            classic=None
        else:classic=st.session_state.get("classic_df")
        st.caption('Selected history only · saved results reused for 15 minutes · four simultaneous downloads maximum. Sector history is separate.')
        if st.session_state.get('classic_load_notice'):st.warning(st.session_state['classic_load_notice'])
        if classic is not None and st.session_state.get('classic_failed'):
            st.warning(f"{len(st.session_state['classic_failed']):,} stocks have no saved prices yet; shown results may be incomplete.")
        if isinstance(classic,pd.DataFrame) and not classic.empty:
            d=classic.copy()
            if sort_by=="Symbol":
                d=d.sort_values("Symbol",ascending=(order=="A → Z"),na_position="last")
            elif sort_by!="Brokerage Call" and sort_by in d.columns:
                d[sort_by]=pd.to_numeric(d[sort_by],errors="coerce")
                d=d.sort_values(sort_by,ascending=(order=="Smallest → Largest"),na_position="last")

            show_brokerage=st.checkbox("🔵 Check recent public brokerage calls",value=True,key="classic_brokerage")
            if show_brokerage:
                with loading_stopwatch("Checking recent brokerage-call headlines..."):
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
            with loading_stopwatch("Scanning selected universe..."):
                d=bulk_snapshot(tuple(use_syms),history,force_refresh=True)

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
elif page=="⚡ Circuit & Volatility":
    render_circuit_page()
elif page=="🇺🇸 All US Stocks":
    render_us_market()
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
            with loading_stopwatch("Scanning price + volume participation..."):
                snap=bulk_snapshot(tuple(syms),"1y")
                res=run_screen(snap,"High Volume Breakout")
            st.dataframe(clean_display(res),use_container_width=True,height=560,hide_index=True)

else:
    st.markdown("## 💾 Market Data Hub")
    st.markdown("### ✅ Yes — you can stop manually typing closing prices.")
    st.write("Use the All NSE Performance module to calculate 1D, 1W, 1M, 3M, 6M, 1Y and 5Y returns and export them to CSV.")
    st.write("For speed: single-stock analysis is quick; the first full-universe 5-year refresh is a large job and can take longer. Cache makes repeated use faster.")
