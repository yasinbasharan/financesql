-- 1. Şirket Bilgileri Tablosu
---- 1. Company Information Table
CREATE TABLE Sirketler (
    SirketID INT PRIMARY KEY IDENTITY(1,1),
    SirketKodu NVARCHAR(10) NOT NULL,
    SirketAdi NVARCHAR(100),
    Sektor NVARCHAR(50)
);

-- 2. Günlük Fiyatlar Tablosu (OHLC)
---- 2. Daily Price Chart (OHLC)
CREATE TABLE GunlukFiyatlar (
    VeriID INT PRIMARY KEY IDENTITY(1,1),
    SirketID INT FOREIGN KEY REFERENCES Sirketler(SirketID),
    Tarih DATE NOT NULL,
    Acilis DECIMAL(18, 2),
    Yuksek DECIMAL(18, 2),
    Dusuk DECIMAL(18, 2),
    Kapanis DECIMAL(18, 2),
    Hacim BIGINT
);

INSERT INTO Sirketler (SirketKodu, SirketAdi, Sektor)
VALUES ('THYAO', 'Turk Hava Yollari', 'Ulasim');

USE BorsaDB;
GO

-- THYAO_5Y tablosundaki verileri asıl yerlerine gönderiyoruz
---- We are sending the data from the THYAO_5Y table to its original locations.
INSERT INTO GunlukFiyatlar (SirketID, Tarih, Acilis, Yuksek, Dusuk, Kapanis, Hacim)
SELECT 
    1, -- THY'nin ID'si
    [Date], 
    [Open], 
    [High], 
    [Low], 
    [Close], 
    [Volume]
FROM [THYAO_5Y];

SELECT TOP 10 * FROM GunlukFiyatlar;

--Veritabanına göre THY son 5 yılda en yüksek hangi fiyattan kapanış yapmış?
--According to the database, what was the highest closing price of Turkish Airlines in the last 5 years?

SELECT TOP 1 Tarih, Kapanis, Hacim 
FROM GunlukFiyatlar 
WHERE SirketID = 1 
ORDER BY Kapanis DESC;

DROP TABLE THYAO_5Y;

USE BorsaDB;
GO

SELECT TOP 1 Tarih, Kapanis, Hacim 
FROM GunlukFiyatlar 
WHERE SirketID = 1  -- THY'nin ID'si 1 olduğu için bunu ekliyoruz
ORDER BY Kapanis DESC;

USE BorsaDB;
GO

-- En güncel veriyi en üstte görmek için
---- To see the most up-to-date data at the top
SELECT * FROM GunlukFiyatlar
ORDER BY Tarih DESC; 


USE BorsaDB;
GO

INSERT INTO Sirketler (SirketKodu, SirketAdi, Sektor)
VALUES ('PGSUS', 'Pegasus Hava Tasimaciligi', 'Ulasim');

-- Bakalım 2 numara olmuş mu?
SELECT * FROM Sirketler;

--We created Pegasus's identity card.
USE BorsaDB;
GO
INSERT INTO Sirketler (SirketKodu, SirketAdi, Sektor)
VALUES ('PGSUS', 'Pegasus Hava Tasimaciligi', 'Ulasim');


USE BorsaDB;
GO

-- PGSUS_5Y tablosundaki verileri GunlukFiyatlar'a taşıyoruz
---- We are transferring the data from the PGSUS_5Y table to GunlukFiyatlar.
INSERT INTO GunlukFiyatlar (SirketID, Tarih, Acilis, Yuksek, Dusuk, Kapanis, Hacim)
SELECT 
    2, -- Pegasus'un Sirketler tablosundaki ID'si
    ---- Pegasus' ID in the Companies table
    [Date], 
    [Open], 
    [High], 
    [Low], 
    [Close], 
    [Volume]
FROM [PGSUS_5Y];

SELECT SirketID, COUNT(*) AS ToplamGunSayisi
FROM GunlukFiyatlar
GROUP BY SirketID;




--We are entering a stock market comparison analysis query.
SELECT 
    S.SirketAdi, 
    MIN(G.Kapanis) AS EnDusukFiyat, 
    MAX(G.Kapanis) AS EnYuksekFiyat, 
    AVG(G.Kapanis) AS OrtalamaFiyat
FROM GunlukFiyatlar G
JOIN Sirketler S ON G.SirketID = S.SirketID
GROUP BY S.SirketAdi;

