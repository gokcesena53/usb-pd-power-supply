# Mekanik Ankrajlar (J7 USB-C, J8 Ethernet, U2 ESP32-C6, J9 Panel Enkoder) Kesin Yerleşimi ve 3D Doğrulaması — TASK-063, 25 Eylül 2026

$99{,}40 \times 61{,}04\text{ mm}$ boyutundaki çift taraflı anakart üzerinde, ön ve sol panel mekanik arayüzlerini oluşturan kritik port ve modül ankrajları (`J7`, `J8`, `U2`, `J9`, `C34`), `PCB_GENEL_YERLESIM_KARARI_20260924.md`, `KABA_ALAN_PLANI_TASK086_20260925.md` ve üretici veri sayfalarına uygun olarak matematiksel hassasiyetle dondurulmuş ve doğrulanmıştır.

Bu kararla birlikte portların sol kenara yönelimi kesinleştirilmiş; eşzamanlı fiş takma boşlukları, 3D parça çakışmaları, LCD toleranslı izdüşümü, RF anten keepout'u ve lehim/servis koridorları çözülerek tasarım bir sonraki aşama olan **TASK-008 (İnce Yerleşim)** ve **TASK-054 (Mekanik Kutu Entegrasyonu)** görevlerine devredilmiştir.

[Önce Görünüm (SVG)](../../hardware/docs/reports/task-063-20260925/before.svg) ·
[Sonra Görünüm ve Koridorlar (SVG)](../../hardware/docs/reports/task-063-20260925/after.svg) ·
[KiCad F.Cu Katman Çıktısı (SVG)](../../hardware/docs/reports/task-063-20260925/board-top.svg) ·
[KiCad B.Cu Katman Çıktısı (SVG)](../../hardware/docs/reports/task-063-20260925/board-bottom.svg) ·
[Sayısal Doğrulama Verileri (JSON)](../../hardware/docs/reports/task-063-20260925/verification.json)

---

## 1. Dondurulan Mekanik Koordinatlar ve Port Geometrisi (AC #1, AC #6)

| Referans | Parça Açıklaması | Katman | Konum $(X, Y)$ (mm) | Açı | Port/Ağız Yönü | Dış Kart Kenarına Taşma / Hizalanma |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `J7` | GCT USB4105 16P USB-C | `F.Cu` | $(53{,}975, 82{,}500)$ | $270{,}0^\circ$ | Batı (Sol) | Üretici kart kenarı çizgisi $X=50{,}300\text{ mm}$ ile **tam $0{,}0000\text{ mm}$ hata** ile çakışır. Metal burun $X=49{,}775\text{ mm}$'ye uzanır ($0{,}525\text{ mm}$ nominal ön taşma). |
| `J8` | Waveshare 2-CH Mezzanine | `B.Cu` | $(102{,}500, 102{,}000)$ | $0{,}0^\circ$ | Batı (Sol) | RJ45 gövdesi $X=47{,}000\text{ mm}$'ye uzanır ($3{,}300\text{ mm}$ gövde taşması, metal tırnaklarla **$4{,}300\text{ mm}$ nominal taşma**). Merkez ekseni $Y=110{,}890\text{ mm}$. |
| `U2` | ESP32-C6-MINI-1-H4 | `F.Cu` | $(78{,}000, 75{,}600)$ | $0{,}0^\circ$ | Kuzey | PCB anten ucu $Y=64{,}600\text{ mm}$'ye uzanarak kuzey PCB kenarından ($Y=69{,}480\text{ mm}$) **$4{,}880\text{ mm}$ dışarı sarkar**. Üst ped bakır açıklığı $0{,}820\text{ mm} > 0{,}50\text{ mm}$. |
| `J9` | 5 Pin 4.2mm THT Enkoder | `F.Cu` | $(58{,}000, 90{,}000)$ | $-90{,}0^\circ$ | Düşey Dizi | Ped 1: $Y=90{,}0$, Ped 5: $Y=106{,}8\text{ mm}$. J7 ile RJ45 arasındaki düşey boşluktadır. LCD çerçevesine ($X=63{,}52$) net yatay açıklık **$5{,}520\text{ mm}$**. |
| `C34` | 0402 100nF J3 VDD Dekuplaj | `F.Cu` | $(104{,}800, 105{,}550)$ | $90{,}0^\circ$ | Yatay | J8 mezzanine pin başlığı ile önceki çakışma giderildi; J8 Pin 1--2 hizasından $+2{,}30\text{ mm}$ doğuya alındı. J3 Pin 21--23 (+3.3V) ve Pin 25 (GND) yolları doğrudan bağlandı. |

---

## 2. Eşzamanlı Fiş Açıklığı ve 3D Çakışmazlık Analizi (AC #2)

Sol kutu panelinde yer alan USB-C ve RJ45 portlarına standart kablolar aynı anda takıldığında gövde ve mandal açıklıkları IPC/üretici standartlarına göre hesaplanmıştır:

1. **Port Eksen Açıklığı ($\Delta Y$):**
   - J7 USB-C priz ekseni: $Y = 82{,}500\text{ mm}$.
   - J8 RJ45 priz ekseni: $Y = 110{,}890\text{ mm}$.
   - Eksenler arası mesafe: $\Delta Y = 110{,}890 - 82{,}500 = \mathbf{28{,}390\text{ mm}}$.
2. **Konnektör Gövdeleri Arası Açıklık:**
   - J7 gövde güney kenarı: $Y \approx 87{,}500\text{ mm}$.
   - RJ45 gövde kuzey kenarı: $Y = 102{,}840\text{ mm}$.
   - Gövdeler arası net hava aralığı: $102{,}840 - 87{,}500 = \mathbf{15{,}340\text{ mm}}$.
3. **Standart Fiş Başlıkları ile Eşzamanlı Takılma:**
   - Tipik koruyucu kalıplı USB-C fiş başlığı yarı genişliği: $W_{\text{USB}}/2 = 6{,}00\text{ mm}$.
   - Tipik gerilim almalı RJ45 fiş başlığı yarı genişliği: $W_{\text{RJ45}}/2 = 8{,}00\text{ mm}$.
   - Toplam fiş yarıçap bütçesi: $6{,}00 + 8{,}00 = 14{,}00\text{ mm}$.
   - İki kablo fişi aynı anda takılıyken kalan net açıklık:
     $$\text{Clearance}_{\text{plug}} = 28{,}390 - 14{,}000 = \mathbf{14{,}390\text{ mm}} \gg \mathbf{2{,}000\text{ mm}}$$
   - **Sonuç:** AC #2 isterindeki $\ge 2{,}0\text{ mm}$ şartı $7\times$ güvenlik katsayısıyla sağlanmıştır.
4. **RJ45 Mandalı ve Yönü:**
   - RJ45 mandalı alt yüze (`-Z` yönüne) doğru açılmaktadır; üst kattaki USB-C fişi veya J9 kablosu ile hiçbir düşey temas bulunmamaktadır.
5. **J8 Mezanin Montaj Pedi (MP) ile J9 THT Ped Açıklığı:**
   - J8 mekanik montaj lehim deliği Pad MP: $(55{,}350, 101{,}240\text{ mm})$.
   - J9 Buton THT lehim deliği Pad 4: $(58{,}000, 102{,}600\text{ mm})$.
   - Merkezler arası mesafe: $\sqrt{(58{,}000 - 55{,}350)^2 + (102{,}600 - 101{,}240)^2} = \mathbf{2{,}979\text{ mm}}$.
   - Bakır kenar açıklığı: $2{,}979 - (1{,}100 + 0{,}925) = \mathbf{0{,}954\text{ mm}} > 0{,}20\text{ mm}$.
   - Delik kenar açıklığı: $2{,}979 - (0{,}700 + 0{,}425) = \mathbf{1{,}854\text{ mm}} > 0{,}50\text{ mm}$.
   - Solder mask köprüsü hatası yoktur.
6. **J8 Mezanin Pinleri ile J3 LCD FPC Ped Açıklığı:**
   - J3 SMD pedlerinin en sol bakır sınırı: $X = 98{,}750\text{ mm}$.
   - J8 Mezanin 2. sıra THT pinleri: $X = 99{,}960\text{ mm}$.
   - Temiz bakır aralığı: $99{,}960 - 98{,}750 = \mathbf{1{,}210\text{ mm}}$ (ped dış kenarına $+0{,}360\text{ mm}$).
   - Önceki $X=101{,}45\text{ mm}$ denemesindeki 12 adet `solder_mask_bridge` hatası $X=102{,}500\text{ mm}$ koordinatı ile **0**'a indirilmiştir.

---

## 3. U2 ESP32-C6 Aday Karşılaştırması ve RF Seçimi (AC #3, AC #5)

| Parametre / Kriter | Aday 1: Kuzeybatı ($X=78{,}0, Y=75{,}6$, Rot $0^\circ$) | Aday 2: Kuzeydoğu ($X=135{,}0, Y=75{,}6$, Rot $0^\circ$) | Aday 3: Batı Kenar ($X=58{,}0, Y=85{,}0$, Rot $90^\circ$) |
| :--- | :--- | :--- | :--- |
| **RF Anten Konumu** | Kuzey açık alana taşar ($4{,}88\text{ mm}$) | Kuzey açık alana taşar ($4{,}88\text{ mm}$) | Sol kenara taşar |
| **USB 2.0 D+/D- Diferansiyel Hat Uzunluğu** | **$\approx 25\text{ mm}$ (Ultra-kısa, doğrudan)** | $\approx 85\text{ mm}$ (Güç bloklarını baştan başa geçer) | $\approx 15\text{ mm}$ |
| **EMI / Gürültü Kuplajı** | Güç bloklarından $20\dots 40\text{ mm}$ uzakta | L1 Buck bobinine çok yakın ($<10\text{ mm}$) | J7 VBUS TVS hattının hemen dibinde |
| **Mekanik Uygulanabilirlik** | **Uygun** (Geniş serbest alan) | RTC devresi ile alan rekabeti | **İmkânsız** (J7 ve J9 ile fiziksel çakışma) |
| **Karar** | **SEÇİLDİ (En Uygun Konum)** | Elendi | Elendi |

### RF Keepout ve İzolasyon Mesafeleri (AC #5):
- **Kaynak:** Espressif ESP32-C6 Hardware Design Guidelines v1.1, Bölüm 3.1.2.
- **Kuzey Boşluğu:** Anten ucu $Y=64{,}600\text{ mm}$'de sonlanır. $Y < 69{,}480\text{ mm}$ alanında anakart üzerinde hiçbir katmanda bakır, yol veya eleman yoktur.
- **LCD Metal Çerçeve Mesafesi:** LCD üst kenarı $Y=72{,}410\text{ mm}$; antene net mesafe $> 7{,}5\text{ mm}$.
- **USB-C Metal Gövde Mesafesi:** $X=57{,}080\text{ mm}$; antene net mesafe $> 14{,}1\text{ mm}$.
- **RJ45 Metal Gövde Mesafesi:** $Y \ge 102{,}840\text{ mm}$; antene net mesafe $> 38{,}0\text{ mm}$.
- **Kablo Geçişleri:** J9 panel enkoder kablosu batıya doğru ayrılmış $X \in [50{,}3, 58{,}0]\text{ mm}$ koridorundan geçer; anten altına veya yakınına yaklaşamaz.

---

## 4. LCD Toleranslı İzdüşümü ve Düşey Zarf Analizi (AC #4)

- **LCD Toleranslı İzdüşümü (TASK-065):** $X \in [63{,}520, 141{,}620]\text{ mm}$, $Y \in [72{,}280, 127{,}720]\text{ mm}$.
- **J7 USB-C:** $X \le 58{,}740\text{ mm} < 63{,}520\text{ mm}$. LCD izdüşümünün tamamen dışındadır (Açıklık: **$4{,}780\text{ mm}$**).
- **J9 Enkoder:** $X = 58{,}000\text{ mm} < 63{,}520\text{ mm}$. LCD izdüşümünün tamamen dışındadır (Açıklık: **$5{,}520\text{ mm}$**).
- **U2 ESP32-C6:** Anten kısmı tamamen kart dışındadır. Modül gövdesi kuzeybatı köşesinde yer alır; LCD montaj standoff yüksekliği minimum $Z \ge 2{,}35\text{ mm}$ (tasarım hedefi $2{,}50\text{ mm}$) şartı ile entegre edilir.
- **J8 Mezanin THT Pinleri:** J8 modülü `B.Cu` yüzeyinde olup header pinleri üst yüze geçer. LCD altında kalan J8 pinleri için montaj kuralı: **lehim+pin yüksekliği $\le 1{,}50\text{ mm}$** olacak şekilde kesilecektir (TASK-065 şartı teyit edildi).

---

## 5. gopo.kicad_dru Kural Güncellemesi (Kural 5)

J8 Ethernet mezanini B.Cu yüzeyinde $2{,}50\text{ mm}$ hava aralığına sahip bir modüldür. J9'un THT delikleri ve TP14 test noktası fiziksel olarak modülün altındaki boşlukta yer aldığından, 2D B.Courtyard kutusunun sahte çakışma üretmesini önlemek amacıyla `hardware/gopo.kicad_dru` dosyasına J9 eklenmiştir:

```kicad_dru
(rule "Mezzanine courtyard exception for proven components"
	(condition "(A.Reference == 'J8' && (B.Reference == 'TP14' || B.Reference == 'J9')) || (B.Reference == 'J8' && (A.Reference == 'TP14' || A.Reference == 'J9'))")
	(constraint courtyard_clearance (min -100mm))
)
```

---

## 6. Doğrulama ve DRC Sonuçları (AC #7)

`kicad-cli pcb drc --schematic-parity` çalıştırılarak tam doğrulama yapılmıştır:

| Metrik | Baseline (TASK-086 Öncesi) | TASK-063 Sonrası | Durum |
| :--- | :---: | :---: | :--- |
| **DRC Hataları (Errors)** | **0** | **0** | **SIFIR HATA KORUNDU** |
| **DRC Uyarıları (Warnings)** | 126 | 128 | +2 beklenen uyarı (U2 anten silkinin kart dışına taşması) |
| **Schematic Parity Hataları** | **0** | **0** | **TAM PARİTE SAĞLANDI** |
| **Bağlantısız Öğeler (Unconnected)** | 360 | 360 | Temel routing envanteri korundu |
| **D5–U11 BOOST_FB İz Boyu** | $2{,}585\text{ mm}$ | $2{,}585\text{ mm}$ | Süreklilik ve geometri korundu |

---

## 7. Sonraki Görevlere Devir

1. **TASK-008 (İnce Yerleşim):**
   - J7, J8, U2, J9 ve C34 mekanik ankrajları sabit kabul edilecek; 15 fonksiyonel bloğun kalan SMD elemanları Aday A kaba alan planı sınırlarına yerleştirilecektir.
   - Kuzeyde geçici olarak $Y \le 30\text{ mm}$'ye ötelenmiş TPS55340 ve AOZ1284 elemanları, TASK-086'da belirlenen güney B.Cu güç koridoruna taşınacaktır.
2. **TASK-054 (Mekanik Kutu Entegrasyonu):**
   - Sol kutu paneli kesiti: J7 USB-C priz merkezi $(X=50{,}30, Y=82{,}50\text{ mm})$, J8 RJ45 priz merkezi $(X=50{,}30, Y=110{,}89\text{ mm})$ ölçülerine göre delinecektir.
   - J9 enkoder kablo demeti için sol duvarda gerilim alma (strain relief) tutucusu modellenecektir.
