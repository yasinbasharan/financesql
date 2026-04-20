import streamlit as st
import pyodbc
import pandas as pd

def get_connection():
    conn_str = (
        "Driver={SQL Server};"
        "Server=.;"
        "Database=BorsaDB;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

st.set_page_config(page_title="Borsa Analiz Paneli", layout="wide")
st.title("📈 Havacılık Sektörü Hisse Analizi")

try:
    conn = get_connection()
    sirketler_df = pd.read_sql("SELECT * FROM Sirketler", conn)
    sirket_listesi = sirketler_df['SirketKodu'].tolist()
    
    secilen_sirket = st.sidebar.selectbox("Şirket Seçin:", sirket_listesi)
    
    if secilen_sirket:
        sirket_id = sirketler_df[sirketler_df['SirketKodu'] == secilen_sirket]['SirketID'].values[0]
        query = f"SELECT TOP 100 Tarih, Kapanis, Hacim FROM GunlukFiyatlar WHERE SirketID = {sirket_id} ORDER BY Tarih DESC"
        fiyatlar_df = pd.read_sql(query, conn)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{secilen_sirket} Son 100 Günlük Veri")
            st.dataframe(fiyatlar_df)
        with col2:
            st.subheader("Fiyat Grafiği")
            st.line_chart(fiyatlar_df.set_index('Tarih')['Kapanis'])
    conn.close()
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")