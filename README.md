# 📈 BIST 2 Büyük Havayolu Şirketi Analizi - Son 5 Yıl(2021-2026)

Bu proje, Borsa İstanbul'un (BIST) iki dev ismi olan **Türk Hava Yolları (THYAO)** ve **Pegasus (PGSUS)** hisselerinin son 5 yıllık verilerini SQL Server üzerinde analiz etmek amacıyla geliştirilmiştir.

-Projenin Amacı
Veritabanı yönetimi ve T-SQL yetkinliklerini kullanarak; ham borsa verilerini anlamlı finansal çıktılara dönüştürmek, sektör bazlı karşılaştırmalar yapmak ve veritabanı normalizasyon süreçlerini uygulamaktır.

-- Kullanılan Teknolojiler
* Veritabanı:** Microsoft SQL Server (SSMS)
* Dil:** T-SQL (Transact-SQL)
* Veri Kaynağı:** Google Finance (CSV Import)
* Versiyon Kontrol: Git & GitHub

-- Veritabanı Mimarisi
Proje kapsamında ilişkisel veritabanı (RDBMS) mantığıyla iki ana tablo oluşturulmuştur:
1.  **Sirketler:** Şirketlerin kimlik bilgilerini (ID, Kod, Ad) tutar.
2.  **GunlukFiyatlar:** 5 yıllık geçmiş fiyat verilerini (Açılış, Kapanış, Hacim vb.) tutar ve `SirketID` üzerinden ilişkilidir.

-- Öne Çıkan Sorgular
-- 1. Şirket Bazlı Performans Özeti
İki şirketin 5 yıllık süreçteki en düşük, en yüksek ve ortalama fiyatlarını karşılaştıran sorgu:

```sql
SELECT 
    S.SirketAdi, 
    MIN(G.Kapanis) AS EnDusukFiyat, 
    MAX(G.Kapanis) AS EnYuksekFiyat, 
    AVG(G.Kapanis) AS OrtalamaFiyat
FROM GunlukFiyatlar G
JOIN Sirketler S ON G.SirketID = S.SirketID
GROUP BY S.SirketAdi;

SELECT TOP 1 Tarih, Kapanis, S.SirketKodu
FROM GunlukFiyatlar G
JOIN Sirketler S ON G.SirketID = S.SirketID
ORDER BY Kapanis DESC;


