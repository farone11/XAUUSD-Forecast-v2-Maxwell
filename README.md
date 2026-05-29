# XAUUSD-Forecast-v2-Maxwell
Quantitative trading system for XAUUSD combining XGBoost and proprietary Maxwell Polarization indicator. Achieves +120.39% return with 53.71% accuracy on 2024-2026 out-of-sample data. Features live Gradio dashboard and systematic backtesting. Developed by FarOneCapital.

<div align="center">

# XAUUSD-Forecast-v2 + Maxwell Polarization

**Quantitative Trading System for Gold (XAUUSD) Powered by ML + Proprietary Indicator** 

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/farone11/XAUUSD-Forecast-v2)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-FarOneCapital-0077B5?logo=linkedin)](https://linkedin.com/company/faronecapital)
[![X.com](https://img.shields.io/badge/X-@FarOneCapital-000000?logo=x)](https://x.com/FarOne11)

**Developed by FarOneCapital | 12+ Years Trading Gold**

</div>

---

### 🚀 Live Demo
**[Try the interactive dashboard here →](https://huggingface.co/spaces/farone11/XAUUSD-Forecast-v2)**

Get real-time BUY/SELL signals for XAUUSD using XGBoost + Maxwell Polarization.

### 📊 Out-of-Sample Performance: Jan 2024 - May 2026

| Metric | **Strategy** | Buy & Hold | Edge |
| --- | :---: | :---: | :---: |
| **Total Return** | **+120.39%** | +119.61% | **+0.78%** |
| **Max Drawdown** | **-25.66%** | ~-35% | **-9.34%** |
| **Profit Factor** | **1.38** | - | ✅ Profitable |
| **Win Rate** | 45.56% | - | 134 Trades |
| **Accuracy** | **53.71%** | 50% | **+3.71%** |

> The strategy outperforms buy-and-hold while reducing drawdown by 9.34%. Achieved through systematic exit timing during corrections.

### 🧠 The Edge: Proprietary Maxwell Polarization Indicator

This model combines machine learning with a custom MT5 indicator developed by FarOneCapital.

**Maxwell Polarization** measures real-time bullish vs bearish market pressure. 
- **Ranked #9** out of 30+ features in XGBoost importance
- **Zero-cross signals** triggered major tops/bottoms in 2025-2026 backtest
- **Reduces whipsaws** by filtering false breakouts

```mql5
// Core logic from MaxwellPolarization.mq5
double mp_value = SMA(Bull_Pressure) - SMA(Bear_Pressure);
