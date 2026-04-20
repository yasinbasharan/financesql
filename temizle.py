import pandas as pd
import os

# Senin klasör yapına göre
HAM_KLASOR   = r'C:\Users\yasin\Documents\GitHub\financesql\ham'
TEMIZ_KLASOR = r'C:\Users\yasin\Documents\GitHub\financesql\temiz'

os.makedirs(TEMIZ_KLASOR, exist_ok=True)

files = {
    'RYAAY': 'RYAAY_5Y.csv',
    'PGSUS': 'PGSUS_5Y.csv',
    'THYAO': 'THYAO_5Y.csv',
}

for ticker, filename in files.items():
    df = pd.read_csv(os.path.join(HAM_KLASOR, filename))

    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = df[col].str.replace(',', '.').astype(float)

    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')
    df.insert(0, 'Ticker', ticker)

    temiz_path = os.path.join(TEMIZ_KLASOR, f'{ticker}_clean.csv')
    df.to_csv(temiz_path, index=False, sep=',', header=False)
    print(f'{ticker} tamam → {temiz_path}')

print("\nTüm dosyalar hazır!")