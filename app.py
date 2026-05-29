# app.py - XAUUSD-Forecast-v2 Powered by Maxwell Polarization
import gradio as gr
import pandas as pd
import joblib
import yfinance as yf
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

model = joblib.load('xauusd_v2_maxwell.pkl')
features = joblib.load('xauusd_v2_features.pkl')

def maxwell_polarization(df, period=1, smooth=25):
    close = df['Close'].values
    bull_pressure = np.zeros(len(close))
    bear_pressure = np.zeros(len(close))
    for i in range(period, len(close)):
        bull_sum = 0.0
        bear_sum = 0.0
        for j in range(period):
            idx = i - j
            if idx < 1: break
            diff = close[idx] - close[idx - 1]
            if diff > 0: bull_sum += diff
            else: bear_sum += -diff
        bull_pressure[i] = bull_sum
        bear_pressure[i] = bear_sum
    bull_sma = pd.Series(bull_pressure).rolling(window=smooth).mean().values
    bear_sma = pd.Series(bear_pressure).rolling(window=smooth).mean().values
    return bull_sma - bear_sma

def predict_xauusd():
    df = yf.download("GC=F", period="2y", interval="1d", progress=False)
    df.reset_index(inplace=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.bbands(append=True)
    df.ta.sma(length=50, append=True)
    df.ta.sma(length=200, append=True)
    df.ta.ema(length=21, append=True)
    df.ta.atr(append=True)
    df.ta.stoch(append=True)
    df.ta.adx(append=True)
    df['Maxwell_MP'] = maxwell_polarization(df)
    df['Maxwell_ZeroCrossUp'] = ((df['Maxwell_MP'] > 0) & (df['Maxwell_MP'].shift(1) <= 0)).astype(int)
    df['Maxwell_ZeroCrossDown'] = ((df['Maxwell_MP'] < 0) & (df['Maxwell_MP'].shift(1) >= 0)).astype(int)
    df['Golden_Cross'] = (df['SMA_50'] > df['SMA_200']).astype(int)
    df['RSI_Oversold'] = (df['RSI_14'] < 30).astype(int)
    df['RSI_Overbought'] = (df['RSI_14'] > 70).astype(int)
    df['MACD_Bullish'] = (df['MACD_12_26_9'] > df['MACDs_12_26_9']).astype(int)
    df['Above_SMA200'] = (df['Close'] > df['SMA_200']).astype(int)
    df['Maxwell_Bull'] = df['Maxwell_MP'].clip(lower=0)
    df['Maxwell_Bear'] = -df['Maxwell_MP'].clip(upper=0)
    df['Maxwell_Color'] = np.where(df['Maxwell_MP'] > 0, 1, np.where(df['Maxwell_MP'] < 0, -1, 0))

    df = df.dropna()
    X_live = df[features].iloc[[-1]]
    proba_up = model.predict_proba(X_live)[0][1]

    if proba_up > 0.52: prediction, color = "BUY", "lime"
    elif proba_up < 0.48: prediction, color = "SELL", "red"
    else: prediction, color = "HOLD", "gray"

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['Date'].tail(90), open=df['Open'].tail(90), high=df['High'].tail(90), low=df['Low'].tail(90), close=df['Close'].tail(90), name='XAUUSD'))
    fig.add_trace(go.Scatter(x=df['Date'].tail(90), y=df['Maxwell_MP'].tail(90), name='Maxwell MP', yaxis='y2', line=dict(color='orange')))
    fig.update_layout(title=f"XAUUSD Forecast: {prediction} | Confidence: {proba_up:.1%}", yaxis2=dict(overlaying='y', side='right', title='Maxwell MP'), template='plotly_dark', xaxis_rangeslider_visible=False)

    return fig, f"<h1 style='color:{color};text-align:center;'>{prediction}</h1>", f"Probability Up: {proba_up:.2%}", f"Maxwell MP: {df['Maxwell_MP'].iloc[-1]:.2f} | Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')} WIB"

demo = gr.Interface(
    fn=predict_xauusd,
    inputs=[],
    outputs=[gr.Plot(label="XAUUSD + Maxwell Polarization"), gr.HTML(label="Signal"), gr.Textbox(label="Model Confidence"), gr.Textbox(label="Indicator Status")],
    title="XAUUSD-Forecast-v2 + Maxwell Polarization",
    description="Quantitative Trading System by FarOneCapital. Accuracy: 53.71% | Backtest Return: +120.39%. Not financial advice.",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
