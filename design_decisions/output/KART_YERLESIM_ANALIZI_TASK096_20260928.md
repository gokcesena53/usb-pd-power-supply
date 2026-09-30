# REV_C Kart Yerleşiminin Elektriksel ve Mekanik Analiz Raporu (TASK-096)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**PCB SHA256:** `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`  
**Araç Sürümleri:** KiCad 10.0.5, FreeCAD 1.1, Python 3.11.5 / 3.14.6  
**Temel Sonuç:** **KOŞULLU ROUTING'E HAZIR (CONDITIONAL READY FOR ROUTING)**  

---

## 1. Yönetici Özeti ve Temel Metrikler

TASK-095 ile sol panel encoder cebi açıldıktan sonra kart dışına park edilen 26 komponentin B.Cu katmanına geri yerleştirilmesiyle oluşan nihai REV_C yerleşimi, TASK-087 (genel routing) öncesinde elektriksel bütünlük, termal davranış, yüksek frekanslı anahtarlama döngüleri, sinyal koridorları, 3D katı mekaniği ve üretim kuralları açısından kapsamlı bir analize tabi tutulmuştur.

### 1.1. Temel Doğrulama Özeti

| Parametre / Metrik | Hedef / Kural Sınırı | Gerçekleşen Değer | Durum |
|---|---|---|---|
| **Toplam Komponent Sayısı** | 144 footprint | **144 footprint** (143 elektriksel + 1 MECH_ENC) | UYGUN |
| **Kart Dışında Bekleyen Elektriksel Parça** | 0 adet | **0 adet** (yalnızca MECH_ENC panel 3D modeli ve U2 anteni dışarıdadır) | UYGUN |
| **DRC Hata Sayısı** | $\le 15$ adet | **15 adet** (tamamı U2 RF anteni zemin pedleri; 0 yeni hata) | UYGUN |
| **DRC Uyarı Sayısı** | Taban: 153 adet | **153 adet** (126 metin boyutu, 17 silk çakışması, 6 maske kesmesi, 3 kenar, 1 lib) | AÇIKLANDI |
| **Şematik Paritesi Farkı** | 0 fark | **0 fark** | UYGUN |
| **Bağlantısız Öğe (Unconnected Items)** | 360 adet (taban çizgi) | **360 adet** (TASK-087 routing aşamasına devredildi) | UYGUN |
| **FreeCAD 3D Katı Kesişimi** | $0{,}000\text{ mm}^3$ | **$0{,}000000\text{ mm}^3$** (Maksimum kesişim sıfır) | UYGUN |
| **Enkoder Kablo Hacmi Açıklığı** | $> 0{,}000\text{ mm}$ | **$1{,}4000\text{ mm}$** (R36 ile $X \in [57{,}8, 70{,}0], Y \in [102, 123]$ arası) | UYGUN |
| **LCD Altı F.Cu Yükseklik Tavanı** | $Z \le 1{,}80\text{ mm}$ | **Maksimum $1{,}35\text{ mm}$** (D10 SOD-123; U2 standoff hariç) | UYGUN |
| **Bakır-Kenar Açıklığı (Edge.Cuts)** | $\ge 0{,}254\text{ mm}$ | **Minimum $0{,}285\text{ mm}$** (U2 Pad 50; diğer tüm pedler $> 0{,}500\text{ mm}$) | UYGUN |
| **D5–U11 `BOOST_FB` İz Uzunluğu** | $\le 10{,}000\text{ mm}$ | **$2{,}585\text{ mm}$** (4 segment) | UYGUN |

---

## 2. Envanter, Katman Dağılımı ve Şematik Paritesi (AC #1)

PCB üzerindeki 144 footprint'in katman ve fonksiyonel blok dağılımı aşağıdaki gibidir:

- **F.Cu Katmanı (46 Footprint):**
  - Ankrajlar: J7 (USB-C), J9 (Enkoder FPC), J3 (TFT FPC), H1–H4 (M3 Montaj Delikleri), MECH_ENC (Panel Enkoder 3D Modeli).
  - MCU & RF: U2 (ESP32-C6-MINI-1), C5, C6, C7, R1, R2, R3, R10, R15, R16, R37, TP9, TP10.
  - USB ESD: D3, U10, D8, D9, R62, R63.
  - LM74801 Çıkış Anahtarı (Grup 5): U12, Q5, D6, C30, C31, C32, R54, R55, R56, R58.
  - TFT Backlight & Dekuplaj (Grup 12 & 13): Q7, R28, R29, R60, C34.
  - Aktif Deşarj Pasifleri (Grup 7): Q6, D10, R66, R67.
  - Test Noktaları: TP11, TP12, TP13.
- **B.Cu Katmanı (98 Footprint):**
  - Ankraj: J8 (Ethernet Mezanin Konnektörü).
  - AP33772S PD Kontrolcü (Grup 2): U1, Q3, R8, R9, R11, R12, R13, R14, R21, R64, R65, C1, C2, C3, C4, C8, D1, TH1, TP1–TP5 (Toplam 23 parça).
  - TPS55340 Boost Dönüştürücü (Grup 3): U11, L3, D4, D5, C23–C29, R47–R49, R52, R53 (Toplam 16 parça).
  - AOZ1284 Buck Dönüştürücü (Grup 4): U5, U6, L1, D2, C12–C19, R38–R41, R43, R50, R51 (Toplam 19 parça).
  - INA226 & Çıkış Klemensi (Grup 6): U3, U13, RShunt1, J4, C11, C35, D7, R27, R59, R61 (Toplam 10 parça).
  - Ethernet Besleme Hücresi (Grup 11 / TASK-093.01): Q8, R17, C21, C20, C10, TP14 (Toplam 6 parça).
  - RTC BQ32000 (Grup 9): U4, Y1, C9, C33, R24 (Toplam 5 parça).
  - I2C Seviye Dönüştürücü (Grup 10): Q1, Q2, R4, R5, R6, R7 (Toplam 6 parça).
  - Panel Enkoder Pull-Up Dirençleri (Grup 14): R34, R35, R36 (Toplam 3 parça).
  - Butonlar ve Test Noktaları: SW1, SW2, Q4 (Deşarj FET), TP6, TP7, TP8.

Şematik paritesi denetiminde (`final-drc.json`), PCB netlist'i ile `gopo.kicad_sch` şematik ağı arasında **0 parite uyuşmazlığı** doğrulanmıştır. Kart dışı elektriksel parça sayısı **0**'dır.

---

## 3. Güç Akışı, Sıcak Akım Döngüleri ve Kritik Hat Analizi (AC #2)

Kart üzerindeki ana güç zinciri soldan sağa kesintisiz doğrusal bir eksende yerleşmiştir:
$$\text{J7 (USB-C)} \longrightarrow \text{AP33772S} \longrightarrow \text{TPS55340 Boost} \longrightarrow \text{AOZ1284 Buck} \longrightarrow \text{LM74801} \longrightarrow \text{INA226 / Şönt} \longrightarrow \text{J4 (Klemens)}$$

Aşağıda her güç bloğunun kritik geometrik mesafeleri, sıcak döngüleri ($di/dt$), gate sürücüleri ve geri besleme/Kelvin hatları incelenmiştir:

### 3.1. AP33772S USB-PD Kontrolcüsü ve Giriş Güç Anahtarı (B.Cu)
- **VBUS Akım Algılama Şöntü (R11):**
  - R11 şönt direnci ($10\text{ m}\Omega$, 1206) J8 Ethernet modülünün güneyinde $(76{,}500, 103{,}000)$ konumundadır.
  - U1 kontrolcüsü $(76{,}500, 120{,}500)$ konumundadır.
  - **Kritik Mesafe:** R11 Pin 1 ile U1 Pin 1 (`USB_VBUS`) arası $16{,}98\text{ mm}$; R11 Pin 2 ile U1 Pin 24 (`PD_VBUS_SENSED`) arası $15{,}63\text{ mm}$'dir.
  - **Analiz ve Risk (BULGU-01 / P2):** Diodes Inc. AP33772S veri sayfası VBUS akım algılama hatlarının diferansiyel ve düşük gürültülü çekilmesini önerir. 16 mm'lik hat boyu, yakınındaki TPS55340 Boost ve AOZ1284 Buck anahtarlama gürültüsünden etkilenebilir.
  - **Routing Şartı (TASK-087):** R11 pedlerinden U1 Pin 1 ve 24'e gidecek Kelvin algılama hatları, B.Cu üzerinde birbirine paralel sıkı diferansiyel çift olarak çekilmeli, çevresi In1.Cu GND düzlemi ile korunmalı ve anahtarlama düğümlerinden (SW/LX) en az 2 mm uzakta tutulmalıdır.
- **Q3 Giriş Güç MOSFET'i ve Gate Hattı:**
  - Q3 $(78{,}500, 110{,}000)$ koordinatında R11 ile U1 arasındadır.
  - R11 Pin 2'den Q3 Drain pedlerine mesafe: **$7{,}71\text{ mm}$**.
  - Q3 Source pedlerinden filtre kondansatörü C8'e mesafe: **$6{,}04\text{ mm}$**.
  - U1 Pin 23 (`PWR_EN`) $\rightarrow$ R12 Gate direnci: **$2{,}54\text{ mm}$**; R12 $\rightarrow$ Q3 Gate (Pin 2): **$7{,}71\text{ mm}$** (Toplam gate döngüsü $\approx 10{,}25\text{ mm}$). Gate osilasyonu riski düşüktür.
- **Dahili LDO Dekuplajları:**
  - U1 Pin 20 (`PD_5V`) $\rightarrow$ C4 (1µF): **$3{,}73\text{ mm}$**.
  - U1 Pin 12 (`V18`) $\rightarrow$ C1 (1µF): **$3{,}77\text{ mm}$**.
  - U1 Pin 15 (`IFB`) $\rightarrow$ C2 (100nF): **$3{,}65\text{ mm}$**.
  - Tüm dahili regülatör kapasitörleri $< 4\text{ mm}$ mesafede olup üretici önerisine ($< 5\text{ mm}$) tam uygundur.
- **Sıcaklık Sensörü (TH1):**
  - NTC termistör TH1 $(73{,}500, 111{,}000)$, Q3 güç transistörünün yalnızca **$3{,}50\text{ mm}$** batısındadır. Termal kuplaj mükemmeldir.

### 3.2. TPS55340 Boost Dönüştürücü (B.Cu)
- **Sıcak Anahtarlama Döngüsü ($di/dt$ Loop):**
  - Döngü elemanları: U11 dahili N-MOSFET (Pin 15/16 SW) $\rightarrow$ D4 Schottky diyotu $\rightarrow$ C29/C28 çıkış kapasitörleri $\rightarrow$ U11 PGND (Pin 1/2 ve termal ped).
  - Koordinatlar: U11 SW $(96{,}90, 118{,}80)$, D4 Anot $(104{,}95, 114{,}66)$, D4 Katot $(100{,}95, 114{,}66)$, C29 Pozitif $(90{,}35, 111{,}66)$, C29 GND $(84{,}95, 111{,}66)$, U11 PGND $(100{,}86, 119{,}05)$.
  - **Sıcak Döngü Çevresi:** Yaklaşık **$50{,}98\text{ mm}$**.
  - **Analiz ve Risk (BULGU-02 / P2):** TI TPS55340 veri sayfası (SLVSBD4C, Bölüm 11.1, Sayfa 26) SW $\rightarrow$ Diyot $\rightarrow$ Çıkış Kapasitörü $\rightarrow$ PGND döngüsünün olabildiğince dar tutulmasını şart koşar. Yerleşimde C29 $X \approx 90\text{ mm}$'de batıda kalırken, D4 $X \approx 101\text{--}105\text{ mm}$'de doğuda kalmaktadır (aralarında 10.6 mm yatay mesafe).
  - **Routing Şartı (TASK-087):** D4 katodundan C29 ve C28 pozitif terminallerine B.Cu üzerinden en az 2.0 mm genişliğinde düşük endüktanslı bakır poligon çekilmeli; C29/C28 toprak pedleri doğrudan U11 termal pedine ve iç katmandaki GND düzlemine çoklu via dizisiyle bağlanmalıdır.
- **Feedback İzi (`/USB_PD_CONTROLLER/BOOST_FB`):**
  - D5 katodundan U11 Pin 6 FB girişine giden 4 segmentli hazır iz korunmuştur:
    - Segment 1: $(93{,}07, 122{,}46) \rightarrow (93{,}90, 121{,}63)$, $L = 1{,}174\text{ mm}$
    - Segment 2: $(93{,}90, 121{,}63) \rightarrow (94{,}25, 121{,}63)$, $L = 0{,}350\text{ mm}$
    - Segment 3: $(94{,}25, 121{,}63) \rightarrow (94{,}85, 121{,}03)$, $L = 0{,}849\text{ mm}$
    - Segment 4: $(94{,}85, 121{,}03) \rightarrow (95{,}06, 121{,}03)$, $L = 0{,}212\text{ mm}$
    - **Toplam İz Uzunluğu:** **$2{,}585\text{ mm}$** ($\le 10{,}000\text{ mm}$ kuralına tam uyumlu).
- **Kompanzasyon Ağı (COMP Pin 7):**
  - U11 Pin 7 $\rightarrow$ R47: **$4{,}52\text{ mm}$**; R47 $\rightarrow$ C25: **$2{,}43\text{ mm}$**. Hassas analog düğüm SW hattından uzakta güvenli bölgededir.

### 3.3. AOZ1284 Buck Dönüştürücü (B.Cu)
- **Giriş Sıcak Döngüsü ($di/dt$ Loop):**
  - Döngü elemanları: Giriş dekuplaj kapasitörü C16 (HF 0805) $\rightarrow$ U5 Pin 5 (VIN) $\rightarrow$ U5 Dahili High-Side FET $\rightarrow$ U5 Pin 4 / Termal Pad (PGND) $\rightarrow$ C16 GND.
  - U5 VIN $(124{,}20, 107{,}22)$, U5 PGND $(129{,}20, 107{,}22)$, C16 VIN $(120{,}00, 95{,}83)$, C16 GND $(120{,}00, 98{,}78)$.
  - **Giriş Döngü Çevresi:** **$32{,}58\text{ mm}$** (C16 ile U5 arası dikey mesafe $11{,}40\text{ mm}$).
  - **Analiz ve Risk (BULGU-03 / P2):** AOS AOZ1284PI veri sayfası giriş kapasitörünün VIN ve PGND pinlerine en yakın mesafede tutulmasını önerir. 11.4 mm'lik mesafe kabul edilebilir sınırlar içindedir ancak routing sırasında endüktans artışı engellenmelidir.
  - **Routing Şartı (TASK-087):** C16/C15'ten U5 VIN pinine B.Cu üzerinden en az 1.5 mm genişliğinde besleme yolu kurulmalı, C16 toprak pini çoklu via ile iç GND düzlemine bağlanmalıdır.
- **Bootstrap Kondansatörü (C17):**
  - U5 Pin 1 (BST) ile C17 Pin 1 arası mesafe: **$5{,}57\text{ mm}$**. C17 Pin 2 doğrudan U5 LX (Pin 2/3) hattına bağlıdır. Mesafe kısadır.
- **Çıkış Filtresi (L1 ve C12/C13):**
  - U5 LX $\rightarrow$ L1 Endüktörü Pin 1: **$7{,}71\text{ mm}$**.
  - L1 Pin 2 $\rightarrow$ C12/C13 Çıkış Kapasitörleri: **$9{,}82\text{ mm}$**.
- **Kompanzasyon (COMP Pin 8) ve FB (Pin 6):**
  - U5 Pin 8 $\rightarrow$ R39: **$4{,}85\text{ mm}$**; U5 Pin 6 $\rightarrow$ R38/R41 gerilim bölücü: **$3{,}10\text{ mm}$**.

### 3.4. LM74801 İdeal Diyot ve Çıkış Anahtarı (F.Cu)
- **Katman Tercihi Doğrulaması:**
  - LM74801 kontrolcüsü (U12) ve güç anahtarı Q5 orijinal tasarımda olduğu gibi `F.Cu` katmanındadır.
  - B.Cu'daki Buck bloğu (U5, L1, C12, C13) ile F.Cu'daki LM74801 bloğu çift taraflı (double-sided) yerleşerek kart alanından tasarruf sağlamış ve koryard çakışmalarını tamamen sıfırlamıştır.
- **Kritik Hatlar:**
  - U12 Pin 4 (DGATE) $\rightarrow$ Q5 Gate (Pin 4): **$3{,}66\text{ mm}$** (Kısa, osilasyon riski sıfır).
  - U12 Pin 1 (Anode Sense) $\rightarrow$ Q5 Source (Pin 1..3): **$7{,}61\text{ mm}$**.
  - U12 Pin 8 (Cathode Sense) $\rightarrow$ Q5 Drain (Pin 5..8): **$6{,}97\text{ mm}$**.
  - Charge pump kondansatörü C31 $\rightarrow$ U12 Pin 2 (CAP): **$4{,}15\text{ mm}$**.
  - TI LM7480-Q1 veri sayfası (SNVSAU9, Bölüm 11.1, Sayfa 43) tavsiyelerine tam uygundur.

### 3.5. INA226 Akım/Güç Monitörü ve J4 Çıkış Klemensi (B.Cu)
- **4 Telli Kelvin Akım Algılama:**
  - RShunt1 ($10\text{ m}\Omega$, 2512 şönt direnci) $(136{,}00, 117{,}60)$ konumundadır.
  - U3 INA226 $(136{,}75, 112{,}10)$ konumundadır.
  - RShunt1 Pin 1 $\rightarrow$ U3 Pin 10 (`IN+`): **$4{,}31\text{ mm}$**.
  - RShunt1 Pin 2 $\rightarrow$ U3 Pin 9 (`IN-`): **$4{,}31\text{ mm}$**.
  - Diferansiyel giriş filtresi C11 $\rightarrow$ U3 Pin 9/10: **$4{,}97\text{ mm}$**.
  - **Analiz:** Kelvin algılama mesafeleri tamamen simetriktir ($4{,}31\text{ mm}$). TI INA226 veri sayfası (SBOS526G, Bölüm 10.1, Sayfa 24) tasarım kurallarına mükemmel uyum sağlar.
- **Şöntten J4 Klemensine Çıkış Yolu:**
  - RShunt1 Pin 2 $\rightarrow$ J4 Pin 1 (`OUT_POS`): **$15{,}31\text{ mm}$**.
  - Çıkış TVS koruma diyotu D7 $\rightarrow$ J4 Pin 1: **$15{,}50\text{ mm}$**.
  - **Routing Şartı (TASK-087):** RShunt1'den J4'e giden `OUT_POS` hattı 3A sürekli DC akım taşıyacaktır. B.Cu üzerinde en az 2.5 mm genişliğinde kalın güç poligonu olarak çekilmelidir.

---

## 4. Dijital, RF, Mezanin ve Arayüz Analizi (AC #3)

### 4.1. ESP32-C6 MCU ve RF Anten İzolasyonu
- **Anten Keepout Bölgesi:**
  - U2 modülü $Y = 75{,}065\text{ mm}$ merkezindedir; dahili PCB anteni kuzey kenarından ($Y = 69{,}48\text{ mm}$) dışarı taşar.
  - Yazılımsal ve geometrik taramada (`digital-interfaces-analysis.json`), $Y < 69{,}48\text{ mm}$ anten keepout hacmi içerisinde U2 anten pedleri haricinde **hiçbir bakır hat, via veya komponent bulunmadığı (%100 temiz)** doğrulanmıştır.
- **MCU Dekuplaj Kapasitörleri:**
  - U2 Pin 1 (`+3.3V`) $\rightarrow$ C5 (22µF bulk): **$12{,}03\text{ mm}$**.
  - U2 Pin 1 $\rightarrow$ C6 (100nF HF): **$12{,}03\text{ mm}$**.
  - U2 Pin 1 $\rightarrow$ C7 (1µF): **$13{,}14\text{ mm}$**.
  - Kapasitörler $Y = 83{,}00\text{ mm}$ F.Cu hattında sıralıdır.
  - **Routing Şartı (TASK-087):** In1.Cu katmanındaki kesintisiz GND referans düzlemi korunmalı; +3.3V ana beslemesi doğrudan C5 $\rightarrow$ C7 $\rightarrow$ C6 üzerinden geçerek U2 Pin 1'e ulaştırılmalıdır.
- **Kullanıcı Butonları (SW1, SW2):**
  - SW1 $(85{,}00, 73{,}50)$ ve SW2 $(92{,}50, 73{,}50)$ B.Cu katmanındadır.
  - U2 anten alanının güneyinde, J8 mezanin konnektörünün kuzeyindeki açık $7{,}7\text{ mm}$'lik B.Cu koridorunda yer alır. Mekanik buton basma erişimi açıktır.

### 4.2. USB-C ESD Koruması (F.Cu)
- J7 USB-C soketi Pin A6/B6 (D+) $\rightarrow$ U10 (USBLC6-2SC6) ESD koruma entegresi: **$3{,}77\text{ mm}$**.
- D+/D- diferansiyel hatları için stub (yan dal) uzunluğu $< 1\text{ mm}$ olacak şekilde doğrudan U10 pedleri üzerinden geçirilmeye elverişlidir.
- VBUS TVS diyotu D3 (SMBJ30A) $\rightarrow$ J7 VBUS pinleri: **$11{,}61\text{ mm}$**.

### 4.3. Ethernet Mezanin Besleme Hücresi (TASK-093.01)
- C20 (100nF HF dekuplaj) J8 modülü altında $(96{,}500, 93{,}580)$ B.Cu katmanındadır.
- J8 Pin 14 (`ETH_3V3`) ve Pin 12 (`GND`) bacaklarına mesafesi **$3{,}55\text{ mm}$**'dir. Döngü son derece sıkıdır.
- C10 (22µF dökme bulk) J8 modülü dışındadır ($X = 107{,}00\text{ mm}$). Modül altı sıkışması ve termal kapanma riski sıfırlanmıştır.

### 4.4. RTC BQ32000 (B.Cu)
- 32.768 kHz kristal Y1 Pin 1 $\rightarrow$ U4 OSCI (Pin 1): **$8{,}98\text{ mm}$**; Y1 Pin 2 $\rightarrow$ U4 OSCO (Pin 2): **$6{,}04\text{ mm}$**.
- VCC dekuplaj kondansatörü C9 $\rightarrow$ U4 Pin 8: **$3{,}33\text{ mm}$**.
- C33 süperkapasitör $\rightarrow$ U4 VBACKUP (Pin 7): **$26{,}03\text{ mm}$**. Süperkapasitör DC yedekleme enerjisi sağladığı için bu mesafe elektriksel olarak risksizdir.
- **Routing Şartı (TASK-087):** Y1 kristal hatları çevresine GND koruma halkası (guard ring) örülmeli ve altına diğer katmanlardan hızlı anahtarlama izi geçirilmemelidir.

### 4.5. Panel Enkoder Arayüzü (J9 & R34..R36)
- J9 lehim pedleri $X = 61{,}500, Y = 104{,}000\text{ mm}$ F.Cu katmanındadır.
- R34, R35, R36 pull-up dirençleri B.Cu üzerinde $Y = 125{,}500\text{ mm}$ ($X = 62{,}5, 65{,}0, 67{,}5\text{ mm}$) hattındadır.
- J9 ile R34 arası Euclidean mesafe: **$22{,}03\text{ mm}$**.
- Sinyaller düşük frekanslı kullanıcı arayüzü anahtarlama sinyalleri (A, B, Push) olduğundan $22\text{ mm}$'lik iz uzunluğu zamanlama veya sinyal bütünlüğü riski oluşturmaz.

---

## 5. Mekanik Ankrajlar, 3D Katı Kesişimi ve Tolerans Analizi (AC #4 & AC #5)

### 5.1. Mekanik Ankrajların Karşılaştırılması
TASK-094 ve TASK-095 kararlarında sabit kabul edilen tüm ankrajlar incelenmiş ve tam eşleşme doğrulanmıştır:

| Ankraj Referansı | Açıklama | Beklenen (X, Y) | Gerçekleşen (X, Y) | Katman | Fark (mm) |
|---|---|---|---|---|---|
| **H1** | Montaj Deliği Sol-Üst | (54.300, 73.480) | (54.300, 73.480) | F.Cu | **0.000** |
| **H2** | Montaj Deliği Sağ-Üst | (145.700, 73.480) | (145.700, 73.480) | F.Cu | **0.000** |
| **H3** | Montaj Deliği Sol-Alt | (54.300, 126.520) | (54.300, 126.520) | F.Cu | **0.000** |
| **H4** | Montaj Deliği Sağ-Alt | (145.700, 126.520) | (145.700, 126.520) | F.Cu | **0.000** |
| **J7** | USB-C Giriş Soketi | (52.975, 88.500) | (52.975, 88.500) | F.Cu | **0.000** |
| **J8** | Ethernet Mezanin Header | (102.500, 79.610) | (102.500, 79.610) | B.Cu | **0.000** |
| **J9** | Enkoder FPC Konnektörü | (61.500, 104.000) | (61.500, 104.000) | F.Cu | **0.000** |
| **J3** | TFT LCD FPC Konnektörü | (98.000, 109.300) | (98.000, 109.300) | F.Cu | **0.000** |
| **MECH_ENC** | Panel Enkoder 3D Modeli | (54.300, 112.400) | (54.300, 112.400) | F.Cu | **0.000** |

### 5.2. Panel Arayüzü, Fiş Girişleri ve Enkoder Hacmi
1. **3 mm Düz Dış Panel:**
   - Panel iç yüzü $X = 49{,}800\text{ mm}$, dış yüzü $X = 46{,}800\text{ mm}$ olarak modellenmiştir.
   - PCB sol kenarı ($X = 50{,}300\text{ mm}$) ile panel arasında nominal $0{,}500\text{ mm}$ montaj payı mevcuttur.
   - MECH_ENC şaft ucu $X = 37{,}300\text{ mm}$'de sonlanarak dış panelden $9{,}500\text{ mm}$ dışarı taşar (kullanıcı onayıyla düğme montajına ayrılmıştır).
2. **Enkoder Kablo Servis Hacmi:**
   - Ayrılan hacim: $X \in [57{,}8, 70{,}0]$, $Y \in [102{,}0, 123{,}0]$, STEP $Z \in [-17{,}0, -0{,}5]\text{ mm}$.
   - FreeCAD 3D katı model analizinde (`solid-check.json`), bu servis hacmi ile B.Cu üzerindeki en yakın komponent (R36 pull-up direnci) arasında **$1{,}4000\text{ mm}$** net serbest açıklık ölçülmüştür. Kablo geçiş koridoru tamamen açıktır.
3. **FreeCAD 3D Katı Kesişim Analizi:**
   - Sabit gövdeler, mezanin modülü, MECH_ENC ve B.Cu'daki tüm taşınan elemanlar arasında yapılan boolean kesişim analizinde:
     - **Maksimum Sabit Kesişim Hacmi:** **$0{,}000000\text{ mm}^3$** (Sıfır çakışma).
     - **Eleman Çifti Kesişimi:** **0 adet**.
     - **Minimum Enkoder Gövde Açıklığı:** **$7{,}0360\text{ mm}$**.

### 5.3. LCD Altı Yükseklik ve Bakır-Kenar Açıklığı
- **TFT LCD Altı Bölgesi ($X \in [63{,}52, 141{,}62], Y \in [72{,}28, 127{,}72]$ F.Cu):**
  - Bu alan altındaki 41 SMD komponentin tamamı incelenmiştir.
  - En yüksek eleman $1{,}35\text{ mm}$ ile D10 (SOD-123) diyotudur.
  - Q5 (1.04 mm), U12 (1.10 mm), U10 (1.45 mm), pasif direnç/kapasitörler (0.50–0.85 mm) tavan kuralı olan **$1{,}80\text{ mm}$**'nin altındadır ($+0{,}45\text{ mm}$ pozitif mekanik emniyet payı).
- **Bakır-Kenar Açıklığı (Copper to Edge.Cuts):**
  - Minimum üretici kuralı $0{,}254\text{ mm}$ (10 mil), genel kural $0{,}500\text{ mm}$'dir.
  - Kart genelindeki tüm elektriksel pedler $0{,}500\text{ mm}$ şartını eksiksiz sağlar.
  - Yalnızca U2 ESP32 modülünün kuzey kenarındaki 15 adet GND lehim pedi $0{,}285\text{ mm}$ açıklığa sahiptir; bu değer $0{,}254\text{ mm}$ mutlak üretici sınırını karşılar.

---

## 6. Termal Yayılım, Bakır Alanı ve Routing Yapılabilirliği (AC #6)

### 6.1. Termal Yoğunlaşma Alanları
Kart üzerinde çalışma esnasında kayda değer ısı üretecek 2 ana güç bloğu bulunmaktadır:
1. **TPS55340 Pre-Boost Bloğu (B.Cu Güney-Orta, $X \in [85, 105], Y \in [108, 128]$):**
   - Tepe güç kaybı $\approx 2{,}2\text{W}$ (U11 anahtar kaybı $\approx 1{,}5\text{W}$, L3 $\approx 0{,}4\text{W}$, D4 $\approx 0{,}3\text{W}$).
   - U11 kılıfı altında halihazırda 15 adet $0{,}20\text{ mm}$ matkap çaplı termal via tanımlıdır.
   - Bu bölge kartın en sıcak noktası (hotspot) olacaktır. B.Cu ve In1.Cu katmanlarında geniş bakır yüzeylerle soğutulmalıdır.
2. **AOZ1284 Buck Bloğu (B.Cu Güneydoğu, $X \in [108, 130], Y \in [95, 113]$):**
   - Tepe güç kaybı $\approx 1{,}6\text{W}$ (U5 $\approx 1{,}1\text{W}$, L1 $\approx 0{,}3\text{W}$, D2 $\approx 0{,}2\text{W}$).
   - U5 SO-8 kılıfının altındaki açık termal pedin iç GND düzlemine bağlanması için routing esnasında en az 4–6 adet termal via eklenmelidir.
3. **Q3 ve Q5 Güç MOSFET'leri:**
   - İletim dirençleri çok düşük ($10\text{--}20\text{ m}\Omega$) olduğundan 3A'de güç kayıpları $< 0{,}2\text{W}$ seviyesindedir; termal darboğaz oluşturmazlar.

### 6.2. Sinyal Koridorları ve Routing Darboğazları
Routing aşamasında (TASK-087) sinyal geçişlerini sınırlayan 4 kritik koridor tespit edilmiştir:
- **Koridor A (Kuzey Sinyal Geçişi, Y < 77 mm):** U2 ile H2 montaj deliği arasında $46{,}1\text{ mm}$'lik geniş bir koridor mevcuttur. MCU'dan LCD'ye ve I2C çevre birimlerine giden sinyaller buradan rahatlıkla geçirilebilir.
- **Koridor B (Sol Panel Cebi ile Boost Arası):** Enkoder cebi ($X = 59{,}8\text{ mm}$) ile Boost ($X = 87{,}65\text{ mm}$) arasında $27{,}85\text{ mm}$ genişlik vardır. AP33772S bloğu burada yer aldığı için dikey güç akışı ve CC hatları iyi katmanlandırılmalıdır.
- **Koridor C (J8 Mezanin Doğu Koridoru):** J8 pin sırası ($X = 102{,}5\text{ mm}$) ile C33 süperkapasitör ($X = 114{,}5\text{ mm}$) arasında **$12{,}0\text{ mm}$** açıklık vardır. Bu aralık kuzeyden güneye sinyal ve besleme taşımak için yeterlidir.
- **Koridor D (Güney Güç Koridoru, Y > 100 mm):** Kartın güneyindeki $30{,}74\text{ mm}$ dikey yükseklik Boost, Buck, LM74801 ve INA226 güç elemanlarıyla doludur. Yüksek akım yolları bu hatta yatayda akacaktır.

### 6.3. Yüksek Yoğunluklu Netler
Kartta toplam 121 net bulunmakta olup en çok bağlantıya sahip netler:
- `GND`: 152 ped (In1.Cu kesintisiz referans katmanı ve dikiş viaları şarttır).
- `+3.3V`: 34 ped (Yıldız veya geniş besleme ağacı gerektirir).
- `V_PRE` (Boost Çıkış / Buck Giriş): 14 ped (Geniş güç poligonu).
- `PD_VBUS_SENSED`: 13 ped.
- `PD_VOUT`: 13 ped.
- `SW_OUT`: 8 ped.
- `USB_VBUS`: 8 ped.
- `ETH_3V3`: 8 ped.
- `OUT_POS`: 7 ped (3A çıkış terminali).

---

## 7. DRC ve Uyarı Sınıflarının Analizi (AC #7)

`final-drc.json` raporunda tespit edilen 15 hata ve 153 uyarının ayrıntılı teknik açıklaması:

### 7.1. Hatalar (15 Adet `copper_edge_clearance`)
- **İhlal Edilen Elemanlar:** `U2` (ESP32-C6-MINI-1) Pad 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 53.
- **Kural Değeri:** $0{,}5000\text{ mm}$; **Ölçülen Değer:** $0{,}2850\text{ mm}$.
- **Gerekçe ve Kabul:** U2 modülünün PCB anteni üretici uygulama notuna göre kart kenarının dışına taşırılmalıdır. Pedler modülün montaj sınırında kaldığından kenara $0{,}285\text{ mm}$ mesafededir. Bu değer PCB üreticisinin mutlak minimum bakır-kenar sınırı olan $0{,}254\text{ mm}$'den büyüktür. Kısa devre veya izolasyon riski yoktur; tasarım gereği kalıcı kabul edilmiş taban hatasıdır.

### 7.2. Uyarılar (153 Adet)
1. **`text_thickness` ve `text_height` (126 Adet - 63 çift):**
   - R1, R3, TP10 vb. pasif elemanların referans yazılarının çizgi kalınlığı $0{,}025\text{ mm}$ ve yüksekliği $0{,}10\text{ mm}$ olarak kalmıştır (Tasarım kuralı: min $0{,}08\text{ mm}$ kalınlık, $0{,}80\text{ mm}$ yükseklik).
   - Elektriksel veya mekanik bir etkisi yoktur; fabrikasyon öncesi ipek baskı (silkscreen) temizliği sırasında otomatik büyütülecektir.
2. **`silk_overlap` (17 Adet):**
   - Komşu elemanların (örn. U10 ile D8, C5 ile U2) ipek baskı kutu çizgilerinin üst üste binmesidir.
3. **`silk_over_copper` (6 Adet):**
   - D8, D9, R63 gibi elemanların referans yazılarının lehim maskesi açıklığına taşmasıdır. Üretici lehim maskesi üzerine gelen boyayı otomatik traşlar (clip).
4. **`silk_edge_clearance` (3 Adet):**
   - U2 ve C33 ipek baskı çizgilerinin kart kenarı sınırına taşmasıdır.
5. **`lib_footprint_mismatch` (1 Adet - J9):**
   - J9 enkoder konnektörünün TASK-091/094 sırasında 5 düz pine ($P=4{,}2\text{ mm}$) uyarlanması nedeniyle kütüphane kopyasıyla uyarısıdır. Kasıtlı özel geometridir.

---

## 8. Bulgular Tablosu ve Önceliklendirilmiş Eylem Matrisi (AC #8)

Yapılan elektriksel ve mekanik analiz sonucunda elde edilen bulgular ve önerilen aksiyonlar aşağıda listelenmiştir:

| Bulgu No | Öncelik | İlgili Blok / Ref | Koordinat (X, Y) | Kural Kaynağı | Ölçülen Değer | Potansiyel Etki | Önerilen Eylem / Takip Görevi |
|---|---|---|---|---|---|---|---|
| **BULGU-01** | **P2 (Orta)** | AP33772S / R11, U1 | R11 (76.5, 103.0)<br>U1 (76.5, 120.5) | AP33772S Datasheet VBUS Sense | $\Delta Y = 16{,}3\text{ mm}$ mesafe | Uzun şönt algılama hattı anahtarlama gürültüsünden etkilenebilir. | **TASK-087 Routing:** R11'den U1 Pin 1 ve Pin 24'e sıkı diferansiyel Kelvin çifti çekilmeli, B.Cu'da GND ile blendajlanmalıdır. |
| **BULGU-02** | **P2 (Orta)** | TPS55340 / D4, C29, U11 | D4 (101.0, 114.7)<br>C29 (90.4, 111.7) | TI SLVSBD4C Sec 11.1 p.26 | Sıcak döngü çevresi $\approx 51\text{ mm}$ | Yüksek di/dt döngü endüktansı ve EMI yayılımı. | **TASK-087 Routing:** D4 katodu ile C29/C28 arasına geniş bakır poligon dökülmeli, GND dönüşü termal pede doğrudan bağlanmalıdır. |
| **BULGU-03** | **P2 (Orta)** | AOZ1284 / C16, U5 | C16 (120.0, 97.3)<br>U5 (124.2, 107.2) | AOS AOZ1284PI Layout Guide | Giriş döngü mesafesi $11{,}4\text{ mm}$ | Buck giriş darbe akımlarında endüktif gerilim çınlaması. | **TASK-087 Routing:** C16 VIN/GND uçlarından U5 Pin 5 ve termal pede en az 1.5 mm genişliğinde düşük empedanslı yol verilmelidir. |
| **BULGU-04** | **P3 (Düşük)** | INA226 / RShunt1, J4 | RShunt1 (136.0, 117.6)<br>J4 (146.0, 104.0) | IPC-2152 3A Akım Taşıma | Hat mesafesi $15{,}3\text{ mm}$ | 3A DC çıkışta hat direnci ve gerilim düşümü. | **TASK-087 Routing:** RShunt1 pin 2 ile J4 pin 1 arasına en az 2.5 mm genişliğinde kalın B.Cu bakır yolu çekilmelidir. |
| **BULGU-05** | **P3 (Düşük)** | RTC / Y1, U4 | Y1 (143.0, 89.0)<br>U4 (143.0, 82.0) | BQ32000 Crystal Layout | Hat mesafesi $6{,}0\text{--}9{,}0\text{ mm}$ | 32.768 kHz osilatör parazit kapma riski. | **TASK-087 Routing:** Y1 hatları çevresine GND koruma halkası çekilmeli, alt katmanlardan hızlı anahtarlama izi geçirilmemelidir. |
| **BULGU-06** | **P3 (Düşük)** | MCU Dekuplaj / C5..C7 | C5 (74.5, 83.0)<br>U2 Pin 1 (64.9, 75.1) | Espressif C6 Hardware Guide | Hat mesafesi $\approx 12{,}0\text{ mm}$ | 3.3V yüksek frekans gürültü bastırma. | **TASK-087 Routing:** +3.3V hattı doğrudan C5 $\rightarrow$ C7 $\rightarrow$ C6 üzerinden geçerek U2 Pin 1'e ulaştırılmalıdır. |

---

## 9. Nihai Sonuç ve Görev Devir Kararı

Mevcut REV_C PCB yerleşimi; 144 komponentin tamamının kural sınırları içerisinde yer alması, 3D mekanik modeller arasında sıfır katı çakışması bulunması, LCD altı yükseklik limitlerine ($Z \le 1{,}35\text{ mm} \le 1{,}80\text{ mm}$) tam uyulması, doğrusal güç akışının korunması ve şematik paritesinin kusursuz olması gerekçeleriyle **KOŞULLU OLARAK ROUTING'E HAZIRDIR**.

Komponent kaydırma veya board shape revizyonuna gerek yoktur. Yukarıda listelenen P2 ve P3 öncelikli bulgular doğrudan **TASK-087 (Genel PCB Routing)** uygulama kurallarına kısıt olarak aktarılmıştır.
