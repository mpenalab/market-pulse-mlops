import pandas as pd
import os

def preprocess_data(input_path="data/raw/market_data.csv", output_path="data/processed/cleaned_data.csv"):
    if not os.path.exists(input_path):
        print("Error: No se encontró el archivo raw.")
        return

    # Cargamos el CSV saltando las filas que yfinance a veces agrega
    # y asegurándonos de que las columnas sean numéricas
    df = pd.read_csv(input_path, header=[0, 1], index_col=0)
    
    # Aplanamos el MultiIndex (Ticker/Price) para quedarnos solo con el precio
    # Si yfinance descargó solo un ticker, las columnas se ven como ('Close', 'AAPL')
    df.columns = df.columns.get_level_values(0)
    
    # Forzamos que las columnas sean numéricas por si acaso
    cols_to_fix = ['Close', 'Open', 'High', 'Low', 'Volume']
    for col in cols_to_fix:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Ahora sí, Feature Engineering
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA21'] = df['Close'].rolling(window=21).mean()
    df['Daily_Return'] = df['Close'].pct_change()
    
    df.dropna(inplace=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"Datos procesados exitosamente en {output_path}")

if __name__ == "__main__":
    preprocess_data()