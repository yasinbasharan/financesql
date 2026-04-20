import pandas as pd

files = {
    'RYAAY': 'RYAAY_5Y.csv',
    'PGSUS': 'PGSUS_5Y.csv',
    'THYAO': 'THYAO_5Y.csv',
}

for ticker, filename in files.items():
    df = pd.read_csv(filename)

    # Ondalık virgülü noktaya çevir, float'a dönüştür
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = df[col].str.replace(',', '.').astype(float)

    # Tarihi SQL Server'ın anlayacağı formata çevir (YYYY-MM-DD)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')

    # Ticker sütunu ekle
    df.insert(0, 'Ticker', ticker)

    # Temiz CSV olarak kaydet (noktalı virgül yok, başlık yok)
    df.to_csv(f'{ticker}_clean.csv', index=False, sep=',', header=False)

print("Hazır!")