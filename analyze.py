"""
╔══════════════════════════════════════════════════════════════╗
║           DEV_14 — NSE Stock Analyzer CLI Tool               ║
║     Built by: Hari Prasad L S (@lshariprasad)                ║
║     GitHub: github.com/lshariprasad/Stock-Trading-Agent      ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python analyze.py NHPC
    python analyze.py IDFCFIRSTB --capital 5000 --qty 20 --avg 76.50
    python analyze.py SUZLON --timeframe swing
"""

import sys
import argparse
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────
#  COLORS FOR TERMINAL OUTPUT
# ─────────────────────────────────────────
class C:
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"
    WHITE  = "\033[97m"

def green(t):  return f"{C.GREEN}{t}{C.RESET}"
def red(t):    return f"{C.RED}{t}{C.RESET}"
def yellow(t): return f"{C.YELLOW}{t}{C.RESET}"
def bold(t):   return f"{C.BOLD}{t}{C.RESET}"
def cyan(t):   return f"{C.CYAN}{t}{C.RESET}"

# ─────────────────────────────────────────
#  FETCH LIVE DATA FROM NSE via yfinance
# ─────────────────────────────────────────
def fetch_data(symbol: str) -> pd.DataFrame:
    nse_symbol = symbol.upper() + ".NS"
    print(f"\n{cyan('⟳')} Fetching live NSE data for {bold(symbol.upper())}...")
    df = yf.download(nse_symbol, period="6mo", interval="1d", progress=False)
    if df.empty:
        print(red(f"✗ Could not fetch data for {symbol}. Check the NSE symbol and try again."))
        sys.exit(1)
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    print(green(f"✓ Data loaded — {len(df)} trading days"))
    return df

# ─────────────────────────────────────────
#  INDICATOR CALCULATIONS
# ─────────────────────────────────────────
def calc_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(series):
    ema12 = calc_ema(series, 12)
    ema26 = calc_ema(series, 26)
    macd  = ema12 - ema26
    signal= calc_ema(macd, 9)
    hist  = macd - signal
    return macd, signal, hist

def calc_bollinger(series, period=20):
    mid  = series.rolling(period).mean()
    std  = series.rolling(period).std()
    upper= mid + 2 * std
    lower= mid - 2 * std
    return upper, mid, lower

def calc_atr(df, period=14):
    hl  = df["High"] - df["Low"]
    hc  = (df["High"] - df["Close"].shift()).abs()
    lc  = (df["Low"]  - df["Close"].shift()).abs()
    tr  = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calc_supertrend(df, period=10, multiplier=3):
    atr  = calc_atr(df, period)
    mid  = (df["High"] + df["Low"]) / 2
    upper= mid + multiplier * atr
    lower= mid - multiplier * atr
    supertrend = pd.Series(index=df.index, dtype=float)
    direction  = pd.Series(index=df.index, dtype=int)
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > upper.iloc[i-1]:
            direction.iloc[i] = 1
        elif df["Close"].iloc[i] < lower.iloc[i-1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]
        supertrend.iloc[i] = lower.iloc[i] if direction.iloc[i] == 1 else upper.iloc[i]
    return supertrend, direction

def calc_stochastic(df, period=14):
    low_min  = df["Low"].rolling(period).min()
    high_max = df["High"].rolling(period).max()
    k = 100 * (df["Close"] - low_min) / (high_max - low_min)
    d = k.rolling(3).mean()
    return k, d

def calc_adx(df, period=14):
    up   = df["High"].diff()
    down = -df["Low"].diff()
    plus_dm  = up.where((up > down) & (up > 0), 0)
    minus_dm = down.where((down > up) & (down > 0), 0)
    atr  = calc_atr(df, period)
    plus_di  = 100 * calc_ema(plus_dm, period) / atr
    minus_di = 100 * calc_ema(minus_dm, period) / atr
    dx   = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.rolling(period).mean(), plus_di, minus_di

def calc_vwap(df):
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    return (tp * df["Volume"]).cumsum() / df["Volume"].cumsum()

def calc_obv(df):
    direction = df["Close"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    return (direction * df["Volume"]).cumsum()

def calc_cci(df, period=20):
    tp  = (df["High"] + df["Low"] + df["Close"]) / 3
    sma = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
    return (tp - sma) / (0.015 * mad)

def calc_williams_r(df, period=14):
    high_max = df["High"].rolling(period).max()
    low_min  = df["Low"].rolling(period).min()
    return -100 * (high_max - df["Close"]) / (high_max - low_min)

def calc_fibonacci(df):
    recent_high = df["High"].tail(60).max()
    recent_low  = df["Low"].tail(60).min()
    diff = recent_high - recent_low
    levels = {
        "0%":    recent_high,
        "23.6%": recent_high - 0.236 * diff,
        "38.2%": recent_high - 0.382 * diff,
        "50.0%": recent_high - 0.500 * diff,
        "61.8%": recent_high - 0.618 * diff,
        "78.6%": recent_high - 0.786 * diff,
        "100%":  recent_low,
    }
    return levels

def calc_pivot(df):
    prev = df.iloc[-2]
    H, L, C = float(prev["High"]), float(prev["Low"]), float(prev["Close"])
    P  = (H + L + C) / 3
    R1 = 2 * P - L
    R2 = P + (H - L)
    S1 = 2 * P - H
    S2 = P - (H - L)
    return P, R1, R2, S1, S2

# ─────────────────────────────────────────
#  SIGNAL HELPERS
# ─────────────────────────────────────────
def sig(condition_buy, condition_sell, neutral_label="NEUTRAL"):
    if condition_buy:  return green("BUY ✅")
    if condition_sell: return red("SELL ❌")
    return yellow(neutral_label)

def val(x): return round(float(x), 2)

# ─────────────────────────────────────────
#  MAIN ANALYSIS ENGINE
# ─────────────────────────────────────────
def run_analysis(symbol, capital=None, qty=None, avg_price=None, timeframe="swing"):
    df = fetch_data(symbol)
    price = val(df["Close"].iloc[-1])

    # ── Calculate all indicators ──
    close = df["Close"]

    ema9   = val(calc_ema(close, 9).iloc[-1])
    ema21  = val(calc_ema(close, 21).iloc[-1])
    ema50  = val(calc_ema(close, 50).iloc[-1])
    ema200 = val(calc_ema(close, 200).iloc[-1])
    sma20  = val(close.rolling(20).mean().iloc[-1])
    sma50  = val(close.rolling(50).mean().iloc[-1])
    sma200 = val(close.rolling(200).mean().iloc[-1])

    rsi = val(calc_rsi(close).iloc[-1])
    macd_line, macd_signal, macd_hist = calc_macd(close)
    macd_v = val(macd_line.iloc[-1])
    macd_s = val(macd_signal.iloc[-1])
    macd_h = val(macd_hist.iloc[-1])

    bb_upper, bb_mid, bb_lower = calc_bollinger(close)
    bb_u = val(bb_upper.iloc[-1])
    bb_m = val(bb_mid.iloc[-1])
    bb_l = val(bb_lower.iloc[-1])
    bb_pos = round(((price - bb_l) / (bb_u - bb_l)) * 100, 1) if (bb_u - bb_l) != 0 else 50

    atr = val(calc_atr(df).iloc[-1])
    st_vals, st_dir = calc_supertrend(df)
    st_val = val(st_vals.iloc[-1])
    st_bull = int(st_dir.iloc[-1]) == 1

    k, d = calc_stochastic(df)
    stoch_k = val(k.iloc[-1])
    stoch_d = val(d.iloc[-1])

    adx_val, plus_di, minus_di = calc_adx(df)
    adx = val(adx_val.iloc[-1])

    vwap = val(calc_vwap(df).iloc[-1])
    obv_now  = calc_obv(df).iloc[-1]
    obv_prev = calc_obv(df).iloc[-6]
    obv_rising = obv_now > obv_prev

    cci = val(calc_cci(df).iloc[-1])
    wr  = val(calc_williams_r(df).iloc[-1])

    vol_now = val(df["Volume"].iloc[-1])
    vol_avg = val(df["Volume"].rolling(20).mean().iloc[-1])
    vol_ratio = round(vol_now / vol_avg, 2) if vol_avg > 0 else 1.0

    fib = calc_fibonacci(df)
    pivot, r1, r2, s1, s2 = calc_pivot(df)

    # ── Support & Resistance ──
    recent_lows  = df["Low"].tail(30)
    recent_highs = df["High"].tail(30)
    support      = val(recent_lows.min())
    resistance   = val(recent_highs.max())

    # Nearest fib level
    nearest_fib  = min(fib.items(), key=lambda x: abs(x[1] - price))

    # ── Trend ──
    if ema9 > ema21 > ema50:  trend = "UPTREND"
    elif ema9 < ema21 < ema50: trend = "DOWNTREND"
    else:                      trend = "SIDEWAYS"

    # ── Consensus Scoring ──
    buy_signals = 0
    sell_signals = 0

    def score(buy_cond, sell_cond):
        nonlocal buy_signals, sell_signals
        if buy_cond:   buy_signals  += 1
        elif sell_cond: sell_signals += 1

    score(ema9 > ema21 > ema50,      ema9 < ema21 < ema50)
    score(price > sma50,             price < sma50)
    score(price > sma200,            price < sma200)
    score(macd_v > macd_s,           macd_v < macd_s)
    score(rsi < 50 and rsi > 30,     rsi > 70)
    score(rsi < 30,                  rsi > 70)
    score(stoch_k < 20,              stoch_k > 80)
    score(cci < -100,                cci > 100)
    score(wr < -80,                  wr > -20)
    score(price < bb_l,              price > bb_u)
    score(st_bull,                   not st_bull)
    score(obv_rising and trend == "UPTREND", not obv_rising and trend == "DOWNTREND")
    score(price > vwap,              price < vwap)
    score(vol_ratio > 1.5,           False)
    score(price > pivot,             price < pivot)
    score(adx > 25 and plus_di > minus_di, adx > 25 and minus_di > plus_di)

    total_scored = buy_signals + sell_signals
    neutral_sigs = 16 - total_scored
    composite    = round((buy_signals / 16) * 100) if total_scored > 0 else 50
    pct_bullish  = round((buy_signals / 16) * 100, 1)

    # ── Final Signal ──
    if composite >= 65 and trend != "SIDEWAYS" and vol_ratio > 1.0:
        final_signal = "BUY"
        signal_color = green
    elif composite <= 35 and trend != "SIDEWAYS":
        final_signal = "SELL"
        signal_color = red
    elif composite >= 55:
        final_signal = "HOLD"
        signal_color = green
    else:
        final_signal = "WAIT"
        signal_color = yellow

    entry    = price
    sl_1atr  = round(price - atr, 2)
    sl_2atr  = round(price - 2 * atr, 2)
    target1  = round(price + 2 * atr, 2)
    target2  = round(price + 3 * atr, 2)
    rr_ratio = round((target1 - entry) / (entry - sl_2atr), 2) if (entry - sl_2atr) > 0 else 0
    confidence = composite

    # ── Personal P&L ──
    pnl_str = ""
    if qty and avg_price:
        invested = round(qty * avg_price, 2)
        current_val = round(qty * price, 2)
        pnl = round(current_val - invested, 2)
        pnl_pct = round((pnl / invested) * 100, 2)
        pnl_col = green if pnl >= 0 else red
        pnl_str = f"""
{bold('━' * 60)}
{bold('💼  YOUR POSITION')}
{bold('━' * 60)}
  Qty         : {qty} shares @ avg ₹{avg_price}
  Invested    : ₹{invested:,.2f}
  Current Val : ₹{current_val:,.2f}
  P&L         : {pnl_col(f'₹{pnl:+,.2f} ({pnl_pct:+.2f}%)')}"""
        if capital:
            pnl_str += f"\n  Capital     : ₹{capital:,.2f}  |  Position: {round((invested/capital)*100,1)}%"

    # ─────────────────────────────────────────
    #  PRINT FULL REPORT
    # ─────────────────────────────────────────
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    print(f"""
{bold('═' * 60)}
{bold(f'  📌 DEV_14 ANALYSIS — {symbol.upper()} (NSE)')}
{bold(f'  {now}')}
{bold('═' * 60)}

{bold('━' * 60)}
{bold('STEP 1 — TREND')}
{bold('━' * 60)}
  EMA  9  : ₹{ema9}
  EMA 21  : ₹{ema21}
  EMA 50  : ₹{ema50}
  EMA 200 : ₹{ema200}
  SMA 50  : ₹{sma50}
  SMA 200 : ₹{sma200}
  ADX     : {adx} {'(Strong trend)' if adx > 25 else '(Weak/ranging)'}
  TREND   : {green(trend) if trend == 'UPTREND' else red(trend) if trend == 'DOWNTREND' else yellow(trend)}

{bold('━' * 60)}
{bold('STEP 2 — SUPPORT & RESISTANCE')}
{bold('━' * 60)}
  Support    : ₹{support}
  Resistance : ₹{resistance}
  Pivot      : ₹{round(pivot,2)}   R1: ₹{round(r1,2)}   R2: ₹{round(r2,2)}
               S1: ₹{round(s1,2)}   S2: ₹{round(s2,2)}
  Fibonacci  : {nearest_fib[0]} = ₹{round(nearest_fib[1],2)} (nearest to price)

{bold('━' * 60)}
{bold('STEP 3 — MOMENTUM')}
{bold('━' * 60)}
  RSI (14)   : {rsi}  →  {sig(rsi < 30, rsi > 70, 'NEUTRAL')}
  MACD       : {macd_v}  Signal: {macd_s}  Hist: {macd_h}  →  {sig(macd_v > macd_s, macd_v < macd_s)}
  Stochastic : %K={stoch_k}  %D={stoch_d}  →  {sig(stoch_k < 20, stoch_k > 80)}
  CCI        : {cci}  →  {sig(cci < -100, cci > 100)}
  Williams%R : {wr}   →  {sig(wr < -80, wr > -20)}

{bold('━' * 60)}
{bold('STEP 4 — VOLATILITY')}
{bold('━' * 60)}
  Bollinger  : Upper ₹{bb_u}  Mid ₹{bb_m}  Lower ₹{bb_l}
               Position: {bb_pos}%  →  {sig(bb_pos < 20, bb_pos > 80)}
               {'⚡ SQUEEZE DETECTED — Big move coming!' if abs(bb_u - bb_l) / bb_m < 0.05 else ''}
  ATR (14)   : ₹{atr}
  Stop 1×ATR : ₹{sl_1atr}
  Stop 2×ATR : ₹{sl_2atr}  ← professional standard
  Supertrend : {green('GREEN ✅ — BULLISH') if st_bull else red('RED ❌ — BEARISH')}  @ ₹{st_val}

{bold('━' * 60)}
{bold('STEP 5 — VOLUME')}
{bold('━' * 60)}
  Today Vol  : {int(vol_now):,}
  Avg 20-day : {int(vol_avg):,}
  Ratio      : {vol_ratio}×  →  {green('HIGH VOLUME ✅') if vol_ratio > 1.5 else yellow('Normal')}
  OBV        : {green('Rising ✅') if obv_rising else red('Falling ❌')}
  VWAP       : ₹{vwap}  →  Price is {green('ABOVE VWAP ✅') if price > vwap else red('BELOW VWAP ❌')}

{bold('━' * 60)}
{bold('STEP 8 — INDICATOR CONSENSUS')}
{bold('━' * 60)}
  BUY signals    : {buy_signals} / 16
  SELL signals   : {sell_signals} / 16
  NEUTRAL        : {neutral_sigs} / 16
  % Bullish      : {pct_bullish}%
  Composite Score: {composite} / 100
{pnl_str}
{bold('═' * 60)}
{bold('  ⚡ FINAL SIGNAL')}
{bold('═' * 60)}
  SIGNAL     :  {signal_color(bold(final_signal))}
  Price Now  :  ₹{price}
  Entry      :  ₹{entry}
  Stop Loss  :  ₹{sl_2atr}  (2×ATR — professional)
  Target 1   :  ₹{target1}
  Target 2   :  ₹{target2}
  R:R Ratio  :  1 : {rr_ratio}
  Confidence :  {confidence} / 100
{bold('═' * 60)}

{bold('⚠️  DISCLAIMER:')} For educational use only. Not financial advice.
    Always use your own judgement and consult a SEBI-registered advisor.
{bold('─' * 60)}
{cyan('⭐ If this helped you → star the repo!')}
{cyan('   github.com/lshariprasad/Stock-Trading-Agent')}
{bold('─' * 60)}
""")

# ─────────────────────────────────────────
#  CLI ENTRY POINT
# ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="DEV_14 — AI-Powered NSE Stock Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze.py NHPC
  python analyze.py IDFCFIRSTB --capital 5000 --qty 20 --avg 76.50
  python analyze.py SUZLON --timeframe intraday
  python analyze.py TATAMOTORS --qty 10 --avg 900 --capital 10000
        """
    )
    parser.add_argument("symbol",     help="NSE stock symbol (e.g. NHPC, SUZLON, TATAMOTORS)")
    parser.add_argument("--capital",  type=float, help="Your total capital in ₹")
    parser.add_argument("--qty",      type=int,   help="Number of shares you hold")
    parser.add_argument("--avg",      type=float, help="Your average buy price in ₹")
    parser.add_argument("--timeframe",default="swing", choices=["intraday","swing","longterm"], help="Trading timeframe")

    args = parser.parse_args()

    print(f"""
{bold(cyan('╔══════════════════════════════════════════════════════╗'))}
{bold(cyan('║        DEV_14 — NSE AI Stock Analyzer v4             ║'))}
{bold(cyan('║  github.com/lshariprasad/Stock-Trading-Agent         ║'))}
{bold(cyan('╚══════════════════════════════════════════════════════╝'))}""")

    run_analysis(
        symbol    = args.symbol,
        capital   = args.capital,
        qty       = args.qty,
        avg_price = args.avg,
        timeframe = args.timeframe,
    )

if __name__ == "__main__":
    main()
