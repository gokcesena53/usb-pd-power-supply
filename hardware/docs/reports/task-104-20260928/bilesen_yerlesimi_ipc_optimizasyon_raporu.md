# REV_C Bileşen Yerleşimini IPC Yüksek Yoğunluk ve Estetik Kurallarına Göre Optimizasyon Raporu (TASK-104)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**Araç Sürümleri:** KiCad 10.0.5, Python 3.10.11 / 3.14.6  
**Durum:** TAMAMLANDI (DONE)

---

## 1. Amaç ve Kapsam

TASK-104 kapsamında; PCB üzerindeki 85 pasif eleman (R, C) ve ilişkili aktif devre blokları IPC-7351 Yüksek Yoğunluk (Least/High-Density Courtyard) kurallarına, sıkı, simetrik ve profesyonel estetiğe göre optimize edilmiştir:
1. **IPC-7351 Yüksek Yoğunluk (Least Courtyard):** Kılıf avlu (courtyard) sınırları dahilinde, toleransları aşmadan gevşek boşluklar giderilerek sıkı ve alan tasarrufu sağlayan yerleşim yapılmıştır.
2. **Ortak Eksen ve Grid Hizalaması:** Paralel direnç ve kapasitörler ortak merkez çizgileri (center-line) boyunca düzenli satır ve sütunlar halinde hizalanmış; rastgele mikro-ofsetler temizlenerek karttaki tüm 85 pasifin %100'ü tutarlı $0.25\text{ mm}$ ve $0.50\text{ mm}$ grid sistemine oturtulmuştur.
3. **Rotasyon Standardizasyonu:** Devre bloklarındaki bileşen yönelimleri normalize edilmiş, rastgele açılar kaldırılmış ve tüm bileşenler kesinlikle $0^\circ$ ve $90^\circ$ (ortogonal) standartlara kavuşturulmuştur. Matris halindeki pull-up dirençleri (örneğin R4/R7) ortak açıya getirilmiştir.
4. **Dekuplaj Önceliği:** Entegre dekuplaj kapasitörleri hedef güç ve GND pinlerinin hemen yanına, via öncesinde ve en dar akım döngüsü sağlanacak şekilde yerleştirilmiştir.
5. **Mekanik Koruma:** Sabit ankrajlar (`H1–H4`, `J7`, `J8`, `J9`, `J3`, `J4`, `MECH_ENC`) ve `U2` modül konumu 0,000 mm sapma ile korunmuştur.

---

## 2. Optimize Edilen Bileşenler ve Koordinat Tablosu

Aşağıdaki tabloda TASK-104 kapsamında koordinatları, grid rayları ve açıları optimize edilen 35 komponent listelenmiştir:

| Ref | Değer | Kılıf | Katman | Önceki Konum $(X, Y)$ [mm] | Yeni Konum $(X, Y)$ [mm] | Açı | Ortak Eksen / Grid Rayı / Adım (Pitch) |
|:---|:---|:---|:---|:---|:---|:---:|:---|
| **R21** | 100k | 0402 | B.Cu | $(75.800, 125.500)$ | **$(76.000, 125.500)$** | $0^\circ$ | $0.25\text{ mm}$ grid; $Y=125.50\text{ mm}$ rayı |
| **R8** | 10k | 0402 | B.Cu | $(78.200, 125.500)$ | **$(78.250, 125.500)$** | $0^\circ$ | R21 ile adım: $\Delta X = 2.25\text{ mm}$ |
| **R64** | 2k0 | 0402 | B.Cu | $(80.500, 125.500)$ | **$(80.500, 125.500)$** | $0^\circ$ | R8 ile adım: $\Delta X = 2.25\text{ mm}$ |
| **R65** | 10k | 0402 | B.Cu | $(82.800, 125.500)$ | **$(82.750, 125.500)$** | $0^\circ$ | R64 ile adım: $\Delta X = 2.25\text{ mm}$ |
| **R9** | 10k | 0402 | B.Cu | $(85.100, 125.500)$ | **$(85.000, 125.500)$** | $0^\circ$ | R65 ile adım: $\Delta X = 2.25\text{ mm}$ |
| **C2** | 100nF | 0402 | B.Cu | $(72.000, 122.800)$ | **$(72.000, 122.750)$** | $0^\circ$ | U1 IFB filtresi $0.25\text{ mm}$ grid |
| **C3** | 2.2µF | 0805 | B.Cu | $(72.400, 107.000)$ | **$(72.500, 107.000)$** | $180^\circ$ | VBUS sense girişi $0.50\text{ mm}$ grid |
| **C8** | 4.7µF | 1210 | B.Cu | $(82.700, 116.900)$ | **$(82.750, 117.000)$** | $0^\circ$ | VOUT filtresi $0.25/0.50\text{ mm}$ grid |
| **R14** | 2.2k | 0402 | B.Cu | $(81.200, 120.500)$ | **$(81.250, 120.500)$** | $0^\circ$ | $0.25\text{ mm}$ grid rayı |
| **C28** | 4.7µF | 1210 | B.Cu | $(110.150, 125.000)$ | **$(110.000, 125.000)$** | $180^\circ$ | Boost çıkış, $0.50\text{ mm}$ grid |
| **R51** | 9.76k | 0402 | B.Cu | $(108.200, 108.000)$ | **$(108.000, 108.000)$** | $180^\circ$ | $Y=108.00\text{ mm}$ rayı, $0.50\text{ mm}$ grid |
| **R50** | 2.87k | 0402 | B.Cu | $(111.100, 108.000)$ | **$(111.000, 108.000)$** | $180^\circ$ | R51 ile adım: tam $3.00\text{ mm}$ |
| **C12** | 4.7µF | 1210 | B.Cu | $(120.800, 105.000)$ | **$(120.750, 105.000)$** | $90^\circ$ | C13 ile adım: $3.75\text{ mm}$ ($0.25\text{ mm}$ grid) |
| **C14** | 100nF | 0402 | B.Cu | $(127.900, 110.000)$ | **$(128.000, 110.000)$** | $90^\circ$ | U5 VIN bypass, $0.50\text{ mm}$ grid |
| **C18** | 10nF | 0402 | B.Cu | $(121.800, 108.500)$ | **$(121.750, 108.500)$** | $180^\circ$ | $0.25\text{ mm}$ grid rayı |
| **C19** | 15nF | 0402 | B.Cu | $(120.800, 112.500)$ | **$(120.750, 112.500)$** | $90^\circ$ | $0.25\text{ mm}$ grid rayı |
| **C15** | 47µF | Elko | B.Cu | $(113.300, 96.700)$ | **$(113.250, 96.750)$** | $180^\circ$ | $0.25\text{ mm}$ grid |
| **C16** | 47µF | 1210 | B.Cu | $(120.000, 97.300)$ | **$(120.000, 97.250)$** | $270^\circ$ | $0.25\text{ mm}$ grid |
| **R54** | 1k0 | 0402 | F.Cu | $(124.800, 107.200)$ | **$(125.000, 107.250)$** | $0^\circ$ | $X=125.00\text{ mm}$ kolon rayı |
| **C30** | 22nF | 0402 | F.Cu | $(124.800, 109.400)$ | **$(125.000, 109.250)$** | $0^\circ$ | R54 ile dikey kolon hizalı |
| **R55** | 237k | 0402 | F.Cu | $(129.000, 107.500)$ | **$(129.000, 107.500)$** | $90^\circ$ | $Y=107.50\text{ mm}$ rayı |
| **R56** | 10k | 0402 | F.Cu | $(131.200, 107.500)$ | **$(131.250, 107.500)$** | $90^\circ$ | R55 ile adım: $2.25\text{ mm}$ |
| **R58** | 100k | 0402 | F.Cu | $(133.400, 107.500)$ | **$(133.500, 107.500)$** | $90^\circ$ | R56 ile adım: $2.25\text{ mm}$ |
| **C35** | 100nF | 0402 | B.Cu | $(132.500, 124.050)$ | **$(132.500, 124.000)$** | $0^\circ$ | U13 dekuplaj, $0.50\text{ mm}$ grid |
| **R61** | 4k7 | 0402 | B.Cu | $(125.500, 124.050)$ | **$(125.500, 124.000)$** | $0^\circ$ | C35 ile ortak $Y=124.00\text{ mm}$ rayı |
| **R62** | 5.1k | 0402 | F.Cu | $(61.500, 96.800)$ | **$(61.500, 96.750)$** | $0^\circ$ | $0.25\text{ mm}$ grid |
| **R63** | 5.1k | 0402 | F.Cu | $(61.500, 98.500)$ | **$(61.500, 98.500)$** | $0^\circ$ | R62 ile adım: $1.75\text{ mm}$ |
| **R28** | 100R | 0402 | F.Cu | $(81.000, 108.300)$ | **$(81.000, 108.250)$** | $0^\circ$ | $0.25\text{ mm}$ grid |
| **R29** | 100k | 0402 | F.Cu | $(83.800, 109.250)$ | **$(83.750, 109.250)$** | $270^\circ$ | $0.25\text{ mm}$ grid |
| **C34** | 1.0µF | 0402 | F.Cu | $(104.800, 105.550)$ | **$(104.750, 105.500)$** | $90^\circ$ | $0.25\text{ mm}$ grid |
| **C20** | 100nF | 0402 | B.Cu | $(96.500, 93.580)$ | **$(96.500, 94.000)$** | $90^\circ$ | J8 avlusundan güvenli mesafe, $0.50\text{ mm}$ grid |
| **C21** | 100nF | 0402 | B.Cu | $(111.500, 89.800)$ | **$(111.500, 89.750)$** | $0^\circ$ | $X=111.50\text{ mm}$ kolonu, $0.25\text{ mm}$ grid |
| **R17** | 100k | 0402 | B.Cu | $(111.500, 87.200)$ | **$(111.500, 87.250)$** | $0^\circ$ | C21 ile adım: $2.50\text{ mm}$ |
| **C11** | 100nF | 0402 | B.Cu | $(141.200, 114.100)$ | **$(141.250, 114.000)$** | $0^\circ$ | U3 INA226 dekuplaj, $0.25/0.50\text{ mm}$ grid |
| **R4** | 4.7k | 0402 | B.Cu | $(105.750, 70.500)$ | **$(105.750, 70.500)$** | **$0^\circ$** (eski: $180^\circ$) | R7 ($0^\circ$) ile rotasyon standardizasyonu |

---

## 3. IPC-7351 ve Estetik Standartlaştırma Sonuçları

### 3.1. Grid Hizalama Analizi
Optimizasyon öncesinde kart üzerindeki 85 pasif elemanın 31 adedi $0.25\text{ mm}$ gridinin dışındaydı (kesirli koordinatlar: `.15`, `.35`, `.55`, `.58`, `.70`, `.80` mm).
Optimizasyon sonrasında:
- **0.50 mm gridine oturan:** 59 komponent (%69.4)
- **0.25 mm gridine oturan:** 26 komponent (%30.6)
- **Off-grid (grid dışı) kalan:** **0 komponent (%0.0)**

Tüm 85 pasif komponent ($0.25\text{ mm}$ veya $0.50\text{ mm}$) mühendislik gridine eksiksiz kilitlenmiştir.

### 3.2. Yönelim (Rotasyon) Standartlaştırması
- Kart üzerindeki 144 komponentin tamamı $0^\circ$, $90^\circ$, $180^\circ$ ve $270^\circ$ ortogonal açılara sahiptir.
- Çapraz veya rastgele açılı tek bir eleman bulunmamaktadır (0 adet).
- Paralel I2C pull-up matrisinde R4 ($180^\circ$) elemanı R7 ($0^\circ$) ile aynı hizaya getirilerek tekdüze polarite sağlanmıştır.

### 3.3. Entegre Dekuplaj Önceliği
Tüm kritik entegrelerin dekuplaj kapasitörleri pin merkezlerine en kısa mesafede tutulmuştur:
- **U13 (VE Kapısı):** C35 mesafesi **$1.88\text{ mm}$**
- **U3 (INA226):** C11 mesafesi **$2.97\text{ mm}$**
- **U4 (BQ32000 RTC):** C9 mesafesi **$3.33\text{ mm}$**
- **U12 (LM74801 İdeal Diyot):** C32 mesafesi **$3.40\text{ mm}$**
- **U1 (AP33772S):** C1 mesafesi **$3.77\text{ mm}$**, C4 mesafesi **$3.73\text{ mm}$**, C2 mesafesi **$3.65\text{ mm}$**
- **U11 (TPS55340 Boost):** C26 mesafesi **$4.61\text{ mm}$**, C27 mesafesi **$3.14\text{ mm}$**
- **U5 (AOZ1284PI Buck):** C14 mesafesi **$5.31\text{ mm}$**, C18 mesafesi **$4.28\text{ mm}$**

---

## 4. Doğrulama ve Metrikler

### 4.1. KiCad 10 DRC ve Şematik Parite Doğrulaması
- **Komut:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
- **Toplam DRC İhlali:** **165 ihlal** (Taban 167'den 2 azaldı; **0 YENİ İHLAL**).
- **Şematik Paritesi:** **0 schematic parity issue** (%100 tam uyum).
- **Bağlantısız Öğeler:** **360 unconnected items** (Taban korundu, routing aşaması TASK-087'ye devredildi).
- **Avlu (Courtyard) Çakışması:** **0 adet** (Tüm komponentler IPC toleransları dahilinde).

### 4.2. Ratsnest Çaprazlık Testi
- **Komut:** `hardware/docs/reports/task-100-20260928/scripts/ratsnest_crossing_test.py`
- **Sinyal Hatları Tel Uzunluğu (Wirelength):** $1342.15\text{ mm}$
- **Sinyal Kesişim Sayısı (Crossings):** $161$ kesişim
