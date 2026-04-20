-- 1. Şirket Bilgileri Tablosu
CREATE TABLE Sirketler (
    SirketID INT PRIMARY KEY IDENTITY(1,1),
    SirketKodu NVARCHAR(10) NOT NULL,
    SirketAdi NVARCHAR(100),
    Sektor NVARCHAR(50)
);

-- 2. Günlük Fiyatlar Tablosu (OHLC)
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