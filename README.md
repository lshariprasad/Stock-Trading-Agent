# 🤖 DEV_14 — AI-Powered NSE Stock Analyst

<div align="center">

![DEV_14 Banner](https://img.shields.io/badge/DEV__14-NSE%20Stock%20Analyst-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![NSE India](https://img.shields.io/badge/Market-NSE%20India-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/lshariprasad/Stock-Trading-Agent?style=for-the-badge)

**A complete AI-powered stock analysis system for NSE India — 11-step technical analysis, paper trading, and real-time buy/sell/hold decisions.**

[📖 How It Works](#how-it-works) • [🚀 Quick Start](#quick-start) • [💡 Features](#features) • [🗺️ Roadmap](#roadmap) • [🤝 Contributing](#contributing)

</div>

---

## ✨ What is DEV_14?

**DEV_14** is an expert-level NSE India stock analysis system powered by AI. It analyzes any NSE stock across **20+ technical indicators** in 11 structured steps — giving you a clear **BUY / SELL / HOLD / WAIT** decision with exact entry, stop-loss, and target prices.

> Built by a retail investor, for retail investors. No paid data feeds. No black boxes. 100% transparent logic.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📊 **11-Step Analysis** | Trend → Support/Resistance → Momentum → Volatility → Volume → Advanced → Sector → Consensus → Decision → Reasoning → Action Plan |
| 🇮🇳 **NSE India Focused** | Designed specifically for Indian markets — NIFTY, Supertrend, NSE symbols |
| 🤖 **AI-Powered Decisions** | Claude/GPT analyzes all 20 indicators and gives one clear verdict |
| 📈 **Paper Trading** | Test strategies risk-free before putting real money |
| 🛡️ **Risk Management** | ATR-based stop losses, 1:2 minimum risk-reward enforced |
| 🔄 **Multi-Version** | v1 → v4 iterations with increasing accuracy |
| 💰 **Capital Protection** | Never recommends selling deep-loss stocks in bear markets |

---

## 🧠 Indicators Covered (20+)

```
Trend          →  EMA (9/21/50/200), SMA (20/50/200), ADX, Parabolic SAR
Momentum       →  RSI, MACD, Stochastic, CCI, Williams %R
Volatility     →  Bollinger Bands, ATR, Keltner Channel, Supertrend
Volume         →  OBV, VWAP, Volume SMA
Advanced       →  Ichimoku Cloud, Fibonacci, Smart Money Concepts, Candlestick Patterns
Levels         →  Pivot Points (R1/R2/S1/S2), Support & Resistance zones
```

---

## 🚀 Quick Start

### Step 1 — Clone the repo
```bash
git clone https://github.com/lshariprasad/Stock-Trading-Agent.git
cd Stock-Trading-Agent
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run your first analysis

Open the **DEV_14 prompt** and fill in your stock details:

```
Stock name       : NHPC
NSE Symbol       : NHPC
Current price    : ₹78.50
My avg buy price : ₹76.20
My quantity      : 16 shares
My P&L today     : +₹9.92
My capital total : ₹4022
Timeframe        : Swing 5-15 days
Market today     : BULL
NIFTY today      : +0.5%
My question      : Should I hold or sell?
```

Paste the filled prompt into Claude or GPT → Get your full 11-step analysis instantly.

---

## 📋 How It Works

```
┌─────────────────────────────────────────────────────┐
│                    DEV_14 SYSTEM                    │
├──────────────┬──────────────────────────────────────┤
│  YOU INPUT   │  Stock symbol + price + your position│
├──────────────┴──────────────────────────────────────┤
│  STEP 1   →  Trend Analysis (EMA, SMA, ADX, SAR)    │
│  STEP 2   →  Support & Resistance + Fibonacci       │
│  STEP 3   →  Momentum (RSI, MACD, Stochastic)       │
│  STEP 4   →  Volatility (BB, ATR, Supertrend)       │
│  STEP 5   →  Volume (OBV, VWAP, Volume SMA)         │
│  STEP 6   →  Advanced (Ichimoku, Smart Money)       │
│  STEP 7   →  Sector & Market Context                │
│  STEP 8   →  Full Indicator Consensus (20 signals)  │
│  STEP 9   →  Trade Decision                         │
│  STEP 10  →  Full Reasoning Paragraph               │
│  STEP 11  →  YOUR Personal Action Plan              │
├─────────────────────────────────────────────────────┤
│  OUTPUT   →  BUY / SELL / HOLD / WAIT               │
│              Entry ₹___ | SL ₹___ | Target ₹___     │
│              Confidence: ___/100                    │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Example Output

```
📌 ANALYSIS: NHPC (NSE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TREND       : UPTREND ✅
RSI (14)    : 52 — Neutral
MACD        : Bullish crossover forming
Supertrend  : GREEN — HOLD/BUY
OBV         : Rising (confirmed uptrend)
VWAP        : Price ABOVE VWAP ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUY signals   : 13 / 20
SELL signals  : 3  / 20
NEUTRAL       : 4  / 20
Composite     : 72 / 100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIGNAL     : HOLD ✅
Entry      : ₹78.50
Stop Loss  : ₹75.00  (2×ATR)
Target 1   : ₹84.00
Target 2   : ₹89.50
R:R Ratio  : 1 : 2.4
Confidence : 72 / 100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📁 Repo Structure

```
Stock-Trading-Agent/
│
├── 📄 DEV_14_PROMPT.txt        ← The main analysis prompt (copy & use)
├── 📄 README.md                ← You are here
│
├── 📂 versions/
│   ├── DEV_14_v1.zip           ← Experiment No. 1 (basic)
│   ├── DEV_14_v2.zip           ← Experiment No. 2
│   ├── DEV_14_v3.zip           ← Advanced Level v1.3
│   └── DEV_14_v4_FINAL.zip     ← ⭐ Latest — use this
│
├── 📂 examples/
│   └── sample_analysis.md      ← Example full analysis output
│
└── 📄 requirements.txt         ← Python dependencies
```

---

## 🛡️ Core Rules (Built-in)

DEV_14 follows strict rules to **protect your capital**:

- ❌ Never recommends selling a stock at **-20% or more loss** in a bear market
- ✅ Always checks if **entire sector is weak** before any sell call
- ✅ Minimum **1:2 Risk-Reward** required for any new trade
- ✅ Always gives an **exact stop-loss price**
- ✅ If signals are mixed → says **WAIT**, not BUY or SELL
- ❌ Never recommends averaging down on a losing position

---

## 🗺️ Roadmap

- [x] v1 — Basic NSE stock analysis prompt
- [x] v2 — Added momentum indicators
- [x] v3 — Advanced tools (Ichimoku, Smart Money, Fibonacci)
- [x] v4 — Full 11-step system with consensus scoring
- [x] v5 — Telegram bot for live alerts
- [ ] v6 — Python script to auto-fetch live NSE data (`yfinance`)
- [ ] v7 — CLI tool: `python analyze.py NHPC`
- [ ] v8 — Backtesting engine
- [ ] v9 — Web dashboard

---

## 🤝 Contributing

Contributions are very welcome! Here's how:

1. **Fork** the repo
2. **Create** your feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

Ideas to contribute:
- Add more Indian market indicators (NSE-specific)
- Improve the prompt for options trading
- Build the Python automation script
- Add example analyses for popular NSE stocks
- Translate README to regional Indian languages

---

## ⚠️ Disclaimer

> **This project is for educational and research purposes only.**
> DEV_14 does not provide financial advice. Stock markets are subject to risk.
> Always consult a SEBI-registered financial advisor before investing.
> Past performance of any analysis does not guarantee future results.
> The author is not responsible for any financial losses.

---

## 👨‍💻 Author

**Hari Prasad L S**
- GitHub: [@lshariprasad](https://github.com/lshariprasad)
- Repo: [Stock-Trading-Agent](https://github.com/lshariprasad/Stock-Trading-Agent)

---

## ⭐ Support

If this project helped you, please **give it a star** ⭐ — it helps others find it and motivates continued development!

---

<div align="center">

**Made with ❤️ for Indian retail investors**

*"Capital preservation is more important than profit."*

</div>
