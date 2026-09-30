# Bileşen Yerleşiminin IPC Yüksek Yoğunluk ve Estetik Kurallarına Göre Optimizasyonu — TASK-104, 28 Eylül 2026

## 1. Karar Özeti

REV_C PCB tasarımı üzerindeki 85 adet pasif komponentin (direnç ve kapasitör) yerleşimi; IPC-7351 Yüksek Yoğunluk (Least/High-Density Courtyard) standartlarına, ortak eksen çizgilerine, tutarlı grid raylarına ve dekuplaj akım döngüsü önceliğine göre optimize edilmiştir.

## 2. Temel İlkeler ve Kararlar

1. **IPC-7351 Yüksek Yoğunluk (Least Courtyard):**
   - Komponentler arasındaki gereksiz gevşek mesafeler giderilerek lehimlenebilirlik ve avlu sınırları dahilinde en sıkı yerleşim sağlanmıştır.
   - Paralel pasif dizilerinde (örneğin AP33772S B.Cu $Y=125.50\text{ mm}$ rayı) adım (pitch) $2.25\text{ mm}$ olarak standartlaştırılmıştır.
   - F.Cu $Y=107.50\text{ mm}$ hattındaki deşarj direnç dizisi ($R55, R56, R58$) $2.25\text{ mm}$ adımla hizalanmıştır.
2. **Grid Raylarına Oturtma (%100 Grid Kilidi):**
   - Öncesinde 31 pasifte bulunan rastgele mikro-ofsetler (`.15`, `.35`, `.55`, `.58`, `.70`, `.80` mm) temizlenmiştir.
   - 85 pasif elemanın 59 adedi $0.50\text{ mm}$, 26 adedi $0.25\text{ mm}$ gridine tam kilitlenmiştir. Kartta grid dışı kalan (off-grid) pasif sayısı **0 adettir**.
3. **Yönelim (Rotasyon) Standartlaştırması:**
   - Kart üzerindeki 144 komponentin tamamı kesinlikle ortogonal ($0^\circ, 90^\circ, 180^\circ, 270^\circ$) standartlara getirilmiştir.
   - I2C pull-up matrisinde R4 ($180^\circ$) açısı R7 ($0^\circ$) ile aynı hizaya getirilerek tekdüzelik sağlanmıştır.
4. **Dekuplaj Döngüleri:**
   - Entegre dekuplaj kapasitörleri (C1, C4, C9, C11, C14, C26, C27, C32, C35) hedef güç pinlerine $<5.5\text{ mm}$ (çoğunlukla $<3.5\text{ mm}$) mesafede tutulmuştur.
5. **Mekanik Bütünlük:**
   - Mekanik montaj delikleri (`H1–H4`), panel konnektörleri (`J7`, `J8`, `J9`, `J3`, `J4`, `MECH_ENC`) ve `U2` modül konumları korunmuştur.

## 3. Doğrulama

- **KiCad 10 DRC:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
  - DRC Hataları/İhlalleri: **165 ihlal** (Taban 167 korunmuş, 2 adet `silk_overlap` giderilmiş, **0 YENİ İHLAL**).
  - Şematik Paritesi: **0 schematic parity issue** (%100 tam uyum).
  - Bağlantısız Öğeler: **360 unconnected items** (Taban korunmuş, TASK-087 routing'e devredildi).
- **Ratsnest Testi:** 127 sinyal hattında 161 kesişim ve $1342.15\text{ mm}$ tel uzunluğu doğrulanmıştır.
