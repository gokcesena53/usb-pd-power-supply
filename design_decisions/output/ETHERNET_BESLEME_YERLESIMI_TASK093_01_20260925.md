# Ethernet Besleme Grubunun Kart İçi Yerleşimi (TASK-093.01) — 25 Eylül 2026

Kullanıcının isteği doğrultusunda, hazırlık aşamasında PCB dışında tutulan Ethernet besleme grubu (**Q8, R17, C21, C20, C10, TP14**), B.Cu katmanındaki J8 Ethernet modülünün yanına ve doğrulanmış modül altı (underlay) hacmine taşınmıştır.

Bu yerleşim, son USB-C/Ethernet dikey hizasını ($Y = 88{,}500\text{ mm}$), düz J9 enkoder pad dizilimini ($X = 58{,}000\text{ mm}$), montaj deliklerini ($H1\text{--}H4$), J3 LCD FPC koridorunu ve U2 RF keepout alanını eksiksiz korur.

---

## 1. Uygulanan Yerleşim ve Koordinat Değişimi

Tüm bileşenler `B.Cu` katmanındadır:

| Referans | Değer | Kılıf | Önce X/Y (mm) | Son X/Y (mm) | Açı | Konum & İşlev |
|---|---|---|---|---|---|---|
| **C20** | 100n | C_0402 | 150,800 / 144,260 | **96,500 / 93,580** | $90^\circ$ | **Modül Altı:** J8 Pin 14 (ETH_3V3) & Pin 12 (GND) iç kolonuna bitişik yüksek frekans dekuplajı. |
| **C10** | 22u | C_0805 | 154,000 / 144,260 | **107,000 / 94,000** | $-90^\circ$ | **Modül Dışı:** J8 Pin 13 (ETH_3V3) & Pin 11 (GND) dış kolonuna komşu dökme (bulk) kapasitör. |
| **Q8** | TSM3443CX6 | SOT-23-6 | 147,000 / 142,990 | **107,000 / 88,500** | $90^\circ$ | **Modül Dışı:** C10'un kuzeyinde; Drain pinleri ETH_3V3'e, Gate/Source doğuya bakar. |
| **R17** | 100k | R_0402 | 143,500 / 142,990 | **111,500 / 87,200** | $0^\circ$ | Q8 Pin 3 (Gate) ve Pin 4 (Source) hemen doğusunda pull-up direnci. |
| **C21** | 100n | C_0402 | 140,500 / 142,990 | **111,500 / 89,800** | $0^\circ$ | R17'nin hemen altında, Q8 kapı-kaynak yumuşak kalkış kapasitörü. |
| **TP14** | TestPoint | Pad D1.0mm | 153,000 / 155,690 | **107,000 / 82,150** | $0^\circ$ | J8 Pin 4 (`/MCU/ETH_RUN`) doğrudan karşısında, modül takılıyken test probu erişimine açık. |

---

## 2. Elektriksel Döngüler ve Net Bütünlüğü

1. **ETH_3V3 – GND Dekuplaj Döngüsü (AC #2):**
   - J8 modülünün besleme pinleri 13 ve 14 (`/MCU/ETH_3V3`), toprak pinleri 11 ve 12'dir (`GND`).
   - `C20` (100nF, 0402), modülün iç tarafında header'ın hemen batısında yer alır. Pin 14'e merkez mesafesi **$3{,}64\text{ mm}$**, Pin 12'ye **$3{,}76\text{ mm}$**'dir. Yüksek frekanslı anahtarlama akımları için döngü endüktansı asgari seviyededir.
   - `C10` (22µF, 0805), header'ın hemen doğu tarafında dış kolon pinlerine (Pin 13 & Pin 11) **$4{,}57\text{ mm}$** mesafededir.
2. **Q8 Kapı-Kaynak Yumuşak Kalkış Hücresi:**
   - `Q8` SOT-23-6 p-kanal güç anahtarıdır. Drain uçları (Pin 1, 2, 5, 6) `/MCU/ETH_3V3` hattına, Source (Pin 4) `+3.3V` rayına, Gate (Pin 3) `/MCU/ETH_PWR_EN` kontrol hattına bağlıdır.
   - `R17` (100k pull-up) ve `C21` (100nF yumuşak kalkış), Q8'in kapı ve kaynak bacaklarına yalnızca **$2{,}59\text{ mm}$** mesafede paralel konumlandırılmıştır.
3. **Netlist Doğrulaması:**
   - 6 elemanın 15 bacağının tüm net isimleri ve pin tipleri önceki durumla %100 eşleşmektedir; şema paritesi hatası $0$'dır.

---

## 3. Mekanik Sınırlar, Yükseklik Bütçesi ve 3D Katı Analizi (AC #3)

Mezanin modülü altındaki boşluk $Z = 2{,}50\text{ mm}$ nominaldir. Konservatif en kötü durum payı $Z = 1{,}90\text{ mm}$ kabul edilmiştir.

1. **Modül Altı Yerleşim (C20):**
   - C20 montaj yüksekliği: **$0{,}50\text{ mm}$**.
   - Kalan dikey açıklık payı: $2{,}50 - 0{,}50 = \mathbf{+2{,}00\text{ mm}}$ (Konservatif $1{,}90\text{ mm}$ payda $+1{,}40\text{ mm}$ pozitif marj).
   - RJ45 keepout bölgesi ($X \in [51{,}35, 69{,}85\text{ mm}]$) ile C20 arasında **$26{,}65\text{ mm}$** yatay mesafe vardır; keepout kesinlikle ihlal edilmemiştir.
2. **Modül Dışı Kenar Yerleşimi (Q8, C10, R17, C21, TP14):**
   - J8 mezanin modülü $X = 104{,}35\text{ mm}$ hattında sona erer.
   - Q8 ($H = 1{,}55\text{ mm}$) ve C10 ($H = 1{,}25\text{ mm}$) bileşenleri $X = 107{,}00\text{ mm}$ koordinatına konularak modül izdüşümünün dışına çıkarılmıştır. Bu sayede modül altı yükseklik sıkışması riski sıfırlanmış, lehim muayenesi (AOI/mikroskop) ve modülü sökmeden tamir imkanı sağlanmıştır.
   - Q8'in iletim kaybı nominal 200 mA yükte $P \approx (0{,}2)^2 \times 0{,}05 = 2\text{ mW}$ seviyesinde olup açık kenarda hava sirkülasyonu serbesttir.
3. **TP14 Test Erişimi:**
   - TP14 ($X = 107{,}000, Y = 82{,}150\text{ mm}$), modül kartının dışındadır. Modül anakarta lehimli/takılı durumdayken osiloskop veya multimetre probu ile `/MCU/ETH_RUN` hattına doğrudan erişilebilir.
4. **FreeCAD 3D Katı Karşılaştırma Sonuçları (`solid-check.json`):**
   - `C20–J8`: En kısa mesafe **$1{,}940\text{ mm}$**, Kesişim Hacmi **$0{,}000\text{ mm}^3$** (Çakışma YOK)
   - `C10–J8`: En kısa mesafe **$2{,}395\text{ mm}$**, Kesişim Hacmi **$0{,}000\text{ mm}^3$** (Çakışma YOK)
   - `Q8–J8`: En kısa mesafe **$1{,}623\text{ mm}$**, Kesişim Hacmi **$0{,}000\text{ mm}^3$** (Çakışma YOK)
   - `R17–J8`: En kısa mesafe **$6{,}998\text{ mm}$**, Kesişim Hacmi **$0{,}000\text{ mm}^3$** (Çakışma YOK)
   - `C21–J8`: En kısa mesafe **$6{,}944\text{ mm}$**, Kesişim Hacmi **$0{,}000\text{ mm}^3$** (Çakışma YOK)
   - Bileşenler arası tüm mesafeler $> 2{,}10\text{ mm}$, tüm kesişim hacimleri **$0{,}000\text{ mm}^3$**'tür.

---

## 4. Tasarım Kuralları (DRC) ve İstisna Tanımı

C20 modül altında J8'in 2D courtyard sınırları içine girdiğinden, `hardware/gopo.kicad_dru` dosyasındaki kurala C20 eklenmiştir:

```lisp
(rule "Mezzanine courtyard exception for proven components"
	(condition "(A.Reference == 'J8' && (B.Reference == 'TP14' || B.Reference == 'J9' || B.Reference == 'C20')) || (B.Reference == 'J8' && (A.Reference == 'TP14' || A.Reference == 'J9' || A.Reference == 'C20'))")
	(constraint courtyard_clearance (min -100mm))
)
```

### DRC Özeti:
- **Hata Sayısı:** $15$ (Başlangıçtaki U2 kart-kenarı açıklığı hataları korunmuştur, **yeni hata: 0**).
- **Uyarı Sayısı:** $129 \rightarrow 129$ (**yeni açıklanmamış uyarı: 0**).
- **Şema Paritesi:** **0** (Tam uyum).
- **Bağlantısız Öğeler:** $360 \rightarrow 360$ (Değişmedi).

---

## 5. Çıktılar ve Rapor Belgeleri

- Rapor Dizini: `hardware/docs/reports/task-093-01-20260925/`
  - `apply_and_verify.py`: Uygulama ve doğrulama betiği
  - `verification.json`: Sayısal doğrulama ve metrik kayıtları
  - `solid-check.json`: FreeCAD 3D katı kesişim ve mesafe analizi
  - `before-inventory.json` / `after-inventory.json`: 143 footprint'in tam durum kaydı
  - `baseline-drc.json` / `final-drc.json`: DRC raporları
  - `final-top.svg` / `final-bottom.svg`: Katman görselleri
