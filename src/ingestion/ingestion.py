import yfinance as yf
import pandas as pd
import os

def download_data(ticker="AAPL", start="2020-01-01", end="2025-01-01"):
    print(f"Descargando datos para {ticker}...")
    data = yf.download(ticker, start=start, end=end)
    
    output_path = "data/raw/market_data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path)
    print(f"Datos guardados en {output_path}")

if __name__ == "__main__":
    download_data()