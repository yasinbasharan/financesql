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

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Borsa Analiz Portalı", layout="wide")
st.title("✈️ Havacılık Sektörü Veri Paneli")

try:
    conn = get_connection()
    
    # 1. Şirketleri çek ve formatla
    sirketler_df = pd.read_sql("SELECT SirketID, SirketKodu, SirketAdi FROM Sirketler", conn)
    sirketler_df['Gosterim'] = sirketler_df['SirketKodu'] + " - " + sirketler_df['SirketAdi']
    
    secilen_gosterim = st.sidebar.selectbox("Analiz Edilecek Şirket:", sirketler_df['Gosterim'].tolist())
    
    if secilen_gosterim:
        secilen_kod = secilen_gosterim.split(" - ")[0]
        secilen_tam_ad = secilen_gosterim.split(" - ")[1]
        sirket_id = sirketler_df[sirketler_df['SirketKodu'] == secilen_kod]['SirketID'].values[0]
        
        # 2. BÜTÜN VERİYİ ÇEK (Sıralı ve FİLTRESİZ - Saf SQL Verisi)
        query = f"""
            SELECT Tarih, Kapanis, Hacim 
            FROM GunlukFiyatlar 
            WHERE SirketID = {sirket_id}
            ORDER BY Tarih ASC
        """
        df = pd.read_sql(query, conn)
        df['Tarih'] = pd.to_datetime(df['Tarih'])

        # 📊 ÜST METRİKLER (KPI)
        if not df.empty:
            son_fiyat = df['Kapanis'].iloc[-1]
            onceki_fiyat = df['Kapanis'].iloc[-2] if len(df) > 1 else son_fiyat
            
            # Sıfıra bölünme hatası olmasın diye ufak bir güvenlik önlemi
            if onceki_fiyat != 0:
                degisim = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
            else:
                degisim = 0

            st.subheader(f"📊 {secilen_tam_ad} Performans Özeti")
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Son Kapanış", f"{son_fiyat:,.2f} ₺", f"{degisim:.2f}%")
            col_m2.metric("Zirve Fiyat (5Y)", f"{df['Kapanis'].max():,.2f} ₺")
            col_m3.metric("Son İşlem Hacmi", f"{df['Hacim'].iloc[-1]:,.0f}")

            st.markdown("---")

            # 📈 GRAFİK VE TABLO
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Fiyat Trend Analizi")
                st.line_chart(df.set_index('Tarih')['Kapanis'])
                
            with col2:
                st.subheader("Geçmiş Veriler (SQL'deki Ham Hal)")
                st.dataframe(df.sort_values(by='Tarih', ascending=False).head(50), use_container_width=True)
        else:
            st.warning("Bu şirkete ait veri bulunamadı.")

    conn.close()
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")