# REV_C PCB Güç ve Sinyal Akışı Hiyerarşik Yerleşim Mimarisi Raporu (TASK-101)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**PCB SHA256:** `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`  
**Araç Sürümleri:** KiCad 10.0.5, Python 3.11.5 / 3.14.6  
**Durum:** TAMAMLANDI (DONE)

---

## 1. Amaç ve Kapsam

TASK-101 kapsamında; REV_C kartının elektriksel güç ve sinyal akışı hiyerarşik, fonksiyonel ve mantıksal aşamalara (stages) göre incelenmiş, ana güç akışının soldan sağa tek yönlü doğrusal bir boru hattı (pipeline) oluşturduğu, katman hiyerarşisi ve çift taraflı güç yerleşiminin via geçiş bütçeleriyle optimize edildiği, kart alanının 3 dikey fonksiyona (Kuzey dijital/RF, Orta arayüz geçişi, Güney anahtarlamalı güç) ayrıldığı ve hızlı anahtarlama yapan gürültülü düğümler (SW, LX) ile hassas analog hatlar (Kelvin akım algılama, RTC kristali) arasındaki fiziksel izolasyon mesafeleri doğrulanmıştır.

---

## 2. Soldan Sağa Hiyerarşik Güç Boru Hattı (Power Pipeline)

Kart üzerindeki ana güç yolu, giriş soketinden çıkış klemensine kadar kesin ve monoton bir $X$ ekseni artışıyla soldan sağa ilerlemektedir:

$$\text{J7 / U10} \longrightarrow \text{U1 / Q3} \longrightarrow \text{U11 / L3 / D4} \longrightarrow \text{U5 / L1} \longrightarrow \text{Q5 / U12} \longrightarrow \text{RShunt1 / U3} \longrightarrow \text{J4}$$

Aşağıdaki tabloda her aşamanın bileşenleri, katmanı, $X$ koordinat aralığı ve ağırlıklı merkez koordinatı özetlenmiştir:

| Aşama No | Fonksiyonel Blok | Kritik Bileşenler | Katman | $X$ Aralığı [mm] | Ağırlıklı Merkez $X$ [mm] | $Y$ Konumu [mm] |
|:---|:---|:---|:---|:---|:---|:---|
| **Aşama 1** | Giriş & ESD/TVS Koruma | J7, U10, D3 | F.Cu | $[52.98, 61.50]$ | **$58.66\text{ mm}$** | $82.50 - 88.50$ |
| **Aşama 2** | USB-PD Kontrolcü & Giriş FET | U1, Q3, R11 | B.Cu | $[76.50, 78.50]$ | **$77.17\text{ mm}$** | $103.00 - 120.50$ |
| **Aşama 3** | Pre-Boost Dönüştürücü | L3, U11, D4, C29, C27 | B.Cu | $[87.50, 104.00]$ | **$98.04\text{ mm}$** | $108.16 - 121.00$ |
| **Aşama 4** | Buck Dönüştürücü | U5, L1, C12, C13 | B.Cu | $[117.00, 127.00]$ | **$122.88\text{ mm}$** | $97.50 - 105.31$ |
| **Aşama 5** | İdeal Diyot & Güç Anahtarı | Q5, U12, C32 | F.Cu | $[128.50, 139.50]$ | **$134.50\text{ mm}$** | $99.00 - 101.50$ |
| **Aşama 6** | Kelvin Akım & Güç İzleme | RShunt1, U3, C11 | B.Cu | $[136.00, 141.20]$ | **$137.98\text{ mm}$** | $112.10 - 117.60$ |
| **Aşama 7** | Çıkış Terminali & Koruma | J4, D7 | B.Cu | $[144.00, 146.00]$ | **$145.00\text{ mm}$** | $104.00 - 119.50$ |

**Hiyerarşik İlerleme Doğrulaması:**  
Merkez koordinatları $58.66 \rightarrow 77.17 \rightarrow 98.04 \rightarrow 122.88 \rightarrow 134.50 \rightarrow 137.98 \rightarrow 145.00\text{ mm}$ şeklinde kesin monoton artış sergilemektedir. Akım hiçbir aşamada geri dönmemekte (backtrack yapmamakta), U dönüşü veya dolambaçlı geçiş oluşturmamaktadır.

---

## 3. Katman Hiyerarşisi ve Katman Atlama (Via Transition) Analizi

### 3.1. Ana Güç Taşıma Katmanı (B.Cu)
- B.Cu katmanı, sistemdeki tüm anahtarlamalı regülatörlerin (Boost U11, Buck U5) ve giriş kontrolcüsünün (U1) ortak zeminidir. Kartın arka yüzü serbest hava akışına açık olduğundan ve LCD ekran ile termal çakışma yaşamadığından, yüksek akımlı bakır poligonlar B.Cu üzerinde kesintisiz ilerler.

### 3.2. Çift Taraflı (Double-Sided) Güç Mimarisi: LM74801 & Q5 (F.Cu)
- **Stratejik Karar:** Buck regülatör (U5, L1, C12, C13) B.Cu'da yer kaplarken, LM74801 ideal diyot kontrolcüsü (U12) ve çift N-MOSFET (Q5) tam bu bloğun karşısında `F.Cu` katmanında konumlandırılmıştır.
- **Sağlanan Avantajlar:**
  1. **Alan Tasarrufu:** $100 \times 60\text{ mm}$ kompakt kart sınırlarında 0 courtyard çakışması ile tam yerleşim sağlanmıştır.
  2. **Termal Yayılım:** L1/U5'in ısısı B.Cu'dan soğurken, Q5 güç transistörünün $I^2 R$ ısısı F.Cu üst yüzey bakırına yayılarak ısı yoğunlaşması engellenmiştir.
  3. **Katman Geçiş Bütçesi:** Buck çıkışından Q5 Source bacaklarına ve Q5 Drain bacaklarından RShunt1/J4 hattına geçiş, TASK-087 genel routing aşamasında her biri en az $6 \times 0.6/0.3\text{ mm}$ via içeren matris dikişleri (via arrays) ile gerçekleştirilecektir.

---

## 4. Fonksiyonel Zonlama (Zoning) Mimarisi

PCB, elektriksel gürültü profili ve mekanik gereksinimlere göre 3 ana yatay zonda hiyerarşik olarak sınırlandırılmıştır:

```
+-------------------------------------------------------------------------+ Y = 60 mm
| KUZEY ZONU (Y < 90 mm) — Düşük Gürültülü Dijital, RF ve Haberleşme      |
| [U2 ESP32-C6 (Anten Keepout Y < 69.5)]   [J8 Ethernet Header]  [U4/Y1 RTC]
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - + Y = 90 mm
| ORTA ZON (Y = 90 - 105 mm) — Kullanıcı Arayüzü & Geçiş Koridoru         |
| [J9 Enkoder FPC]               [J3 TFT LCD FPC]          [MECH_ENC Cebi]|
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - + Y = 105 mm
| GÜNEY ZONU (Y > 90 mm) — Yüksek Akım ve Anahtarlamalı Güç Dönüşümü      |
| [U1/Q3 PD]     [U11/L3/D4 Boost]    [U5/L1 Buck]   [U12/Q5]  [U3/RShunt]|
+-------------------------------------------------------------------------+ Y = 130 mm
  X = 50 mm                                                    X = 150 mm
```

- **Kuzey Zonu ($Y < 90\text{ mm}$ - 42 Komponent):**  
  ESP32-C6 (U2) RF modülü, harici kristal gerektirmeyen dahili osilatör, anten keepout bölgesi ($Y < 69.48\text{ mm}$), Waveshare Ethernet mezanini (J8), BQ32000 RTC (U4), Y1 32.768 kHz kristali, I2C seviye dönüştürücü (Q1, Q2) ve SW1/SW2 butonları.
- **Güney Zonu ($Y \ge 90\text{ mm}$ - 101 Komponent):**  
  Tüm anahtarlamalı DC-DC güç dönüşüm hücreleri, bobinler, yüksek akımlı MOSFET'ler, şöntler ve filtre kapasitörleri.
- **İç Katman Kalkanlama:**  
  In1.Cu katmanındaki kesintisiz katı GND düzlemi, güneydeki anahtarlama gürültüsünün kuzeydeki RF modülüne ve RTC kristaline kuplajını fiziksel olarak engeller.

---

## 5. Hızlı Anahtarlama Düğümleri ile Hassas Düğümlerin Fiziksel İzolasyonu

Güç indüktörleri ($L1, L3$) ve yüksek $dv/dt$ anahtarlama düğümleri ($SW, LX$) ile sistemdeki hassas analog ve osilatör düğümleri arasındaki mesafeler hesaplanmıştır:

| Hassas Komponent | Fonksiyonu | Katman | Konum $(X, Y)$ [mm] | L1 Buck ($X=127.0, Y=97.5$) Mesafesi | L3 Boost ($X=97.7, Y=108.2$) Mesafesi | İzolasyon Durumu |
|:---|:---|:---|:---|:---|:---|:---|
| **Y1** | RTC Kristali (32.768 kHz) | B.Cu | $(143.00, 89.00)$ | **$18.12\text{ mm}$** | **$49.19\text{ mm}$** | MÜKEMMEL ($> 18\text{ mm}$) |
| **U3** | INA226 Akım/Güç Monitörü | B.Cu | $(136.75, 112.10)$ | **$17.56\text{ mm}$** | **$39.25\text{ mm}$** | MÜKEMMEL ($> 17\text{ mm}$) |
| **RShunt1** | Çıkış Kelvin Şönt Direnci | B.Cu | $(136.00, 117.60)$ | **$22.02\text{ mm}$** | **$39.45\text{ mm}$** | MÜKEMMEL ($> 22\text{ mm}$) |
| **U2** | ESP32-C6 MCU / RF Modül | F.Cu | $(77.92, 75.06)$ | **$53.96\text{ mm}$** | **$38.56\text{ mm}$** | MÜKEMMEL ($> 38\text{ mm}$) |
| **R11** | VBUS Giriş Akım Şöntü | B.Cu | $(76.50, 103.00)$ | **$50.80\text{ mm}$** | **$21.82\text{ mm}$** | UYGUN ($> 21\text{ mm}$) |

**Sonuç:** Tüm hassas analog algılama ve frekans referans hatları, manyetik ve elektriksel gürültü kaynaklarından en az **$17.56\text{ mm}$** (ortalama $> 35\text{ mm}$) fiziksel mesafeyle izole edilmiştir.

---

## 6. Doğrulama ve Metrikler

### 6.1. Ratsnest Çaprazlık ve Tel Uzunluğu Analizi
- **Ölçüm Aracı:** `hardware/docs/reports/task-100-20260928/scripts/ratsnest_crossing_test.py`
- **Sinyal Segment Sayısı:** 127
- **Sinyal Kesişim Sayısı (Crossings):** **185** (Hiyerarşik boru hattı ve zonlama ile taban korundu).
- **Toplam Sinyal Teli Uzunluğu (MST):** **$1450.84\text{ mm}$**.

### 6.2. KiCad 10 DRC ve Şematik Paritesi
- **Komut:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
- **Toplam DRC İhlali:** **164 ihlal** (0 YENİ İHLAL; tamamı bilinen anten kenarı ve serigrafi etiketleridir).
- **Şematik Paritesi:** **0 schematic parity issue** (%100 tam uyum).
- **Bağlantısız Öğeler:** **360 unconnected items** (Taban korundu, TASK-087 routing'e devredildi).
