# Tasarım Kararı: Küresel Ölü Alan Giderme ve Yüksek Yoğunluklu Sıkılaştırma (TASK-108)

**Tarih:** 28 Eylül 2026  
**Karar ID:** DEC-TASK108-20260928  
**İlgili Görev:** TASK-108  
**Durum:** ONAYLANDI (APPROVED)  
**Etkilenen Dosyalar:** `hardware/gopo.kicad_pcb`, `audit_compliance.json`, `CHANGES.TXT`

---

## 1. Bağlam ve Sorun Tanımı
TASK-107 kapsamında gerçekleştirilen nihai yerleşim denetiminin ardından, kart üzerindeki çeşitli alt devrelerde pasif bileşenler (dirençler, kapasitörler) ile ilişkili entegre (IC) bacakları arasında hala gereksiz ölü alanlar (dead space), geniş koridorlar ve veri yolu oluşturan çoklu direnç grupları arasında lüzumsuz aralıklar bulunduğu tespit edilmiştir. 

Özellikle:
1. **U12 eFuse bloğu (F.Cu):** R58, R56, R55 dirençlerinin $Y=107.50\text{ mm}$ hattında U12 entegresinden $4.2\text{ mm}$ uzakta beklemesi ve dirençler arasında $1.26\text{ mm}$ boşluk olması.
2. **U1 STUSB4500 bloğu (B.Cu):** $Y=125.50\text{ mm}$ hattındaki pasif diziliminin (C1, R21, R8, R64, R65, R9) entegre alt avlusuna $1.85\text{ mm}$ uzaklıkta durması.
3. **Enkoder ve USB-C pull-up/pull-down hatları (F.Cu):** R34, R35, R36 ve R62, R63 aralıklarının $0.59-0.76\text{ mm}$ ile gevşek kalması.
4. **U2 MCU strap grubu (F.Cu):** R15, R37, R10 dirençleri arasında $1.01\text{ mm}$ boşluk bulunması.
5. **U11 Boost bloğu alt sınırı (B.Cu):** R52, C24, R49 ve TP4 bileşenlerinin $Y=128.0-128.5\text{ mm}$ bandına kadar inerek kartın bileşen çevreleme kutusunu (bounding box) gereksiz yere aşağı zorlaması.

---

## 2. Alınan Kararlar ve Geometrik Kısıtlar

1. **Katı Minimum Avlu Sınırı (Clearance = 0.15 mm):**
   Ayrık pasif bileşenler (0402 ve 0603) bağlı oldukları IC avlularına ve birbirlerine doğru, IPC-7351 Least Courtyard kurallarını ihlal etmeksizin net $0.15\text{ mm}$ avlu-avlu açıklığı kalacak şekilde çekilmiştir.

2. **Yoğun Doğrusal Paketleme (Dense Linear Packing):**
   Veri yollarında ve pull-up gruplarında yer alan yan yana elemanlar (U12 R58-R56-R55, U1 C1-R21-R8-R64-R65-R9, Enkoder R34-R35-R36, U2 R15-R37-R10) sıfır gereksiz boşlukla ($0.150\text{ mm}$ avlu açıklığı) birbirine kilitlenmiştir.

3. **Mekanik ve RF Ankrajların Korunması:**
   Donmuş mekanik ankrajlar (`H1–H4`, `J3`, `J4`, `J7`, `J8`, `J9`, `MECH_ENC`, `U2`) nominal konumlarında $0.0000\text{ mm}$ sapma ile korunmuş; hiçbir ankrajın yeri değiştirilmemiştir.

4. **Kesişimlerin Giderilmesi (Ratsnest Uncrossing):**
   Sıkıştırma sırasında R54 direnci $180^\circ$ çevrilerek sinyal hava hatları düzeltilmiş, 4 kesişim anında ortadan kaldırılmıştır.

---

## 3. Sayısal Sonuçlar ve Doğrulama

* **Sinyal Tel Uzunluğu:** $1319.04\text{ mm} \rightarrow 1304.25\text{ mm}$ (**$-14.79\text{ mm}$ kazanç**)
* **Sinyal Kesişim Sayısı:** $141 \rightarrow 137$ (**$-4$ adet kesişim çözüldü**)
* **Ankraj Harici Bileşen Bounding Box:** $88.45 \times 58.85\text{ mm} \rightarrow 88.45 \times 57.32\text{ mm}$
  * Yükseklik kazanımı: **$1.530\text{ mm}$**
  * Alan kazanımı: **$135.33\text{ mm}^2$ (%2.60 daralma)**
* **KiCad 10 DRC:** 25 ihlal (taban korundu, 0 yeni ihlal), **0 avlu çakışması**, **0 şematik parite hatası**.
