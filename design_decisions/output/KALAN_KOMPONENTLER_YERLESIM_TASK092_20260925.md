# Kalan Komponentlerin Kart İçi Yerleşimi (TASK-092) — 25 Eylül 2026

## 1. Özet ve Temel Başarı Göstergeleri

TASK-091 (USB-C ve Ethernet port hizalanması) ve TASK-093.01 (Ethernet besleme hücresinin J8 yakınına yerleşimi) sonrasında geçici park alanında (kart dışında) bekleyen tüm komponentler, ana PCB sınırları ($X \in [50{,}300, 149{,}700]\text{ mm}$, $Y \in [69{,}480, 130{,}520]\text{ mm}$) içine başarıyla yerleştirilmiştir.

| Başarı Kriteri | Hedef / Referans | Gerçekleşen | Durum |
|---|---|---|---|
| **Toplam Komponent Sayısı** | 143 footprint | **143 footprint** | **TAMAMLANDI** |
| **Kart Dışında Bekleyen** | 0 adet (yalnızca U2 anteni kuzeye taşar) | **0 adet** | **TAMAMLANDI** |
| **Toplam DRC Hata Sayısı** | 15 adet (yalnızca U2 taban anten hataları) | **15 adet** | **TAMAMLANDI** |
| **Yeni / Açıklanmamış DRC Hatası** | 0 adet (kısa devre, açıklık, koryard çakışması yok) | **0 adet** | **TAMAMLANDI** |
| **Şematik Paritesi Farkı** | 0 fark | **0 fark** | **TAMAMLANDI** |
| **Bağlantısız Öğe (Unconnected)** | 360 adet (taban çizgi korundu) | **360 adet** | **TAMAMLANDI** |
| **D5–U11 `BOOST_FB` İz Uzunluğu** | $\le 10{,}000\text{ mm}$ | **$2{,}585\text{ mm}$** (4 segment) | **TAMAMLANDI** |
| **FreeCAD 3D Katı Kesişimi** | $0{,}000\text{ mm}^3$ (J8 mezanin ve çevre elemanlar) | **$0{,}000\text{ mm}^3$** | **TAMAMLANDI** |
| **LCD Altı Yükseklik Kısıtı ($Z \le 1{,}80\text{ mm}$)** | $X \in [63{,}52, 141{,}62]$, $Y \in [72{,}28, 127{,}72]$ F.Cu | **Maksimum $1{,}35\text{ mm}$** | **TAMAMLANDI** |
| **RJ45 Keepout (B.Cu)** | $X \in [51{,}35, 69{,}85]$, $Y \in [80{,}60, 97{,}00]$ 0 komponent | **0 komponent** | **TAMAMLANDI** |

---

## 2. Mekanik ve Elektriksel Ankrajların Korunması

Aşağıdaki ankraj elemanlarının hiçbir koordinatı değiştirilmemiş, taban durumla birebir ($0{,}000\text{ mm}$ sapma) korunmuştur:
- **H1–H4:** M3 montaj delikleri ($(54{,}30, 73{,}48)$, $(145{,}70, 73{,}48)$, $(54{,}30, 126{,}52)$, $(145{,}70, 126{,}52)$).
- **J7 (USB-C Giriş Portu):** $(53{,}975, 88{,}500)$, Açı: $-90^\circ$, Katman: `F.Cu`.
- **J8 (Ethernet Mezanin Konnektörü):** $(102{,}500, 79{,}610)$, Açı: $0^\circ$, Katman: `B.Cu`.
- **J9 (Panel Enkoder FPC Konnektörü):** $(58{,}000, 104{,}000)$, Açı: $-90^\circ$, Katman: `F.Cu`.
- **J3 (TFT LCD FPC Konnektörü):** $(98{,}000, 109{,}300)$, Açı: $90^\circ$, Katman: `F.Cu`.
- **U2 (ESP32-C6-MINI-1-H4):** $(77{,}925, 75{,}065)$, Açı: $0^\circ$, Katman: `F.Cu`.
- **Ethernet Besleme Hücresi (TASK-093.01):** Q8, R17, C21, C20, C10, TP14 aynen muhafaza edilmiştir.

---

## 3. Güç Akışı ve Blok Bazlı Yerleşim Detayları

Doğrusal güç akışı soldan sağa kesintisiz olarak tesis edilmiştir:
$$\text{J7 (USB-C Giriş)} \longrightarrow \text{AP33772S} \longrightarrow \text{TPS55340 Boost} \longrightarrow \text{AOZ1284 Buck} \longrightarrow \text{LM74801} \longrightarrow \text{INA226 / Şönt} \longrightarrow \text{J4 (Çıkış Klemensi)}$$

### 3.1. Grup 1: USB-C ESD Koruması (F.Cu)
- **Komponentler:** `D3, U10, D8, D9, R62, R63`.
- **Konum:** $X = 61{,}500\text{ mm}$, $Y \in [82{,}500, 98{,}500]\text{ mm}$ F.Cu katmanında, J7 soketinin pin çıkışlarına doğrudan komşu.
- **Kısıt Uyumu:** J7 koryardından tamamen açıkta, LCD sınırının ($X = 63{,}52\text{ mm}$) solunda kalır ($D3$ gövde sağı $X = 63{,}30\text{ mm}$).

### 3.2. Grup 2: AP33772S USB-PD Kontrolcüsü (B.Cu)
- **Komponentler:** `U1, Q3, R8, R9, R11-R14, R21, R64, R65, C1-C4, C8, D1, TH1, TP1-TP5`.
- **Öteleme:** $\Delta X = +12{,}00\text{ mm}, \Delta Y = -30{,}00\text{ mm}$.
- **Konum:** $X \in [58{,}50, 81{,}50]\text{ mm}$, $Y \in [104{,}50, 126{,}00]\text{ mm}$ B.Cu katmanında.
- **Kısıt Uyumu:** J9 enkoder konnektörünün F.Cu'daki pinlerine B.Cu'dan temas etmez, RJ45 keepout alanının güneyinde yer alır.

### 3.3. Grup 3: TPS55340 Boost Dönüştürücü (B.Cu)
- **Komponentler:** `U11, L3, D4, D5, C23-C29, R47-R49, R52, R53`.
- **Öteleme:** $\Delta X = +28{,}15\text{ mm}, \Delta Y = +100{,}66\text{ mm}$.
- **Konum:** $X \in [87{,}65, 110{,}15]\text{ mm}$, $Y \in [108{,}00, 128{,}00]\text{ mm}$ B.Cu katmanında.
- **İnce Ayar:** `C28` kart alt kenarından ($Y = 130{,}52\text{ mm}$) 0.5 mm açıklığı korumak için $Y = 125{,}00\text{ mm}$'ye çekilmiştir.
- **Feedback İzi:** D5 ile U11 arasındaki kritik 4 parça `/USB_PD_CONTROLLER/BOOST_FB` yolu aynı vektörle taşınmış ve $2{,}585\text{ mm} \le 10\text{ mm}$ sınırında kalmıştır.
- **J3 ile Ayrım:** F.Cu'daki J3 FPC konnektörünün pinleri $Y = 117{,}30\text{ mm}$'de biter; B.Cu'daki U11 $Y = 121{,}00\text{ mm}$ merkezindedir. Katmanlar arası SMD izolasyonu tamdır.

### 3.4. Grup 4: AOZ1284 Buck Dönüştürücü (B.Cu)
- **Komponentler:** `U5, U6, L1, D2, C12-C19, R38-R41, R43, R50, R51`.
- **Öteleme:** $\Delta X = +28{,}50\text{ mm}, \Delta Y = +84{,}00\text{ mm}$.
- **Konum:** $X \in [108{,}00, 133{,}00]\text{ mm}$, $Y \in [96{,}70, 113{,}00]\text{ mm}$ B.Cu katmanında.
- **Kısıt Uyumu:** Kuzeyde C33 süperkapasitöründen ($Y \le 91{,}53\text{ mm}$) $\ge 5\text{ mm}$, batıda Ethernet besleme hücresinden ($C10, C21$) $\ge 1\text{ mm}$ uzaktadır.

### 3.5. Grup 5: LM74801 İdeal Diyot ve Çıkış Anahtarı (F.Cu)
- **Komponentler:** `U12, Q5, D6, C30, C31, C32, R54, R55, R56, R58`.
- **Katman:** Şematik ve taban tasarımda olduğu gibi `F.Cu` katmanında tutulmuştur.
- **Öteleme:** $\Delta X = +18{,}00\text{ mm}, \Delta Y = +80{,}00\text{ mm}$.
- **Konum:** $X \in [124{,}80, 140{,}00]\text{ mm}$, $Y \in [99{,}00, 109{,}40]\text{ mm}$ F.Cu katmanında.
- **LCD Yükseklik Uyumu:** Bu alanda F.Cu üzerinde LCD paneli yer alır. Grubun tüm elemanları SMD'dir:
  - U12 (VSSOP-10): $H = 1{,}10\text{ mm} \le 1{,}80\text{ mm}$.
  - Q5 (PowerPAK SO-8 / DFN5x6): $H = 1{,}04\text{ mm} \le 1{,}80\text{ mm}$.
  - D6 (SOD-123): $H = 1{,}35\text{ mm} \le 1{,}80\text{ mm}$.
  - Direnç ve Kapasitörler (0603): $H = 0{,}80\text{ mm} \le 1{,}80\text{ mm}$.
  Hiçbir eleman $1{,}80\text{ mm}$ tavanını aşmaz.
- **Katman Bağımsızlığı:** Buck grubu B.Cu katmanında olduğu için iki güç bloğu arasında sıfır mekanik ve koryard çakışması sağlanmıştır.

### 3.6. Grup 6: INA226 Akım/Gerilim Ölçüm ve Çıkış Klemensi (B.Cu)
- **Komponentler:** `U3, U13, RShunt1, J4, C11, C35, D7, R27, R59, R61`.
- **Öteleme:** $\Delta X = -21{,}00\text{ mm}, \Delta Y = +96{,}10\text{ mm}$.
- **J4 Çıkış Klemensi:**
  - Konum: $X = 146{,}000\text{ mm}, Y = 104{,}000\text{ mm}$, Açı: $90^\circ$ (Dikey oryantasyon).
  - Pin 1 (`OUT_POS`): $(146{,}00, 104{,}00)$, Pin 2 (`GND`): $(146{,}00, 111{,}80)$.
  - 3.9 mm çaplı PTH pad kenarları $X = 147{,}95\text{ mm}$'de kalarak doğu kart kenarından ($149{,}70\text{ mm}$) $1{,}75\text{ mm} > 0{,}50\text{ mm}$ açıklık marjı sağlar.
- **D7 TVS Diyotu:** $(144{,}00, 119{,}50)$, Açı: $0^\circ$. Kart kenarından ve şöntten tamamen izoledir.
- **R27 Alert Direnci:** $(136{,}75, 107{,}00)$, Açı: $0^\circ$. U3 Pin 3'ün hemen kuzeyinde temiz alandadır.
- **R59 Çıkış LED Direnci:** $(144{,}00, 122{,}50)$.

### 3.7. Grup 7: Çıkış Aktif Deşarj Hücresi
- **Komponentler:** `Q4` (B.Cu), `Q6, D10, R66, R67` (F.Cu).
- **Öteleme:** $\Delta X = -71{,}00\text{ mm}, \Delta Y = +95{,}00\text{ mm}$.
- **Konum:** $X \in [113{,}00, 128{,}00]\text{ mm}$, $Y \in [117{,}00, 123{,}00]\text{ mm}$.

### 3.8. Grup 8: MCU Çevresi ve Butonlar
- **F.Cu Pasifleri:** `C5, C6, C7, R1, R2, R3, R10, R15, R16, R37, TP9, TP10` elemanları U2 ESP32 modülünün hemen güneyinde $Y = 83{,}000\text{ mm}$ düz hattında sıralanmıştır.
- **Butonlar (SW1, SW2):**
  - Konum: SW1 $(85{,}00, 73{,}50)$, SW2 $(92{,}50, 73{,}50)$, Açı: $0^\circ$, Katman: `B.Cu`.
  - U2 RF keepout alanının güneyinde ($Y = 73{,}50 > 69{,}48\text{ mm}$), J8 mezanin konnektörünün kuzeyinde ($Y = 73{,}50 < 77{,}22\text{ mm}$) $7{,}7\text{ mm}$'lik açık B.Cu koridorundadır.

### 3.9. Grup 9: RTC BQ32000 ve Süperkapasitör
- **C33 Süperkapasitör:** $(114{,}500, 81{,}000)$, Açı: $180^\circ$, Katman: `B.Cu`.
  - 20 mm bacak aralığıyla Pin 1 $(114{,}50, 81{,}00)$, Pin 2 $(134{,}50, 81{,}00)$.
  - Ethernet besleme hücresinin doğusunda, J8 modül gövdesinden $> 10\text{ mm}$ uzaktadır.
- **U4, Y1, C9, R24:** C33'ün doğusundaki boş alana yerleştirilmiştir ($X \in [137{,}5, 143{,}0]\text{ mm}$, $Y \in [81{,}0, 89{,}0]\text{ mm}$). H2 montaj deliğinden $\ge 5\text{ mm}$ uzaktadır.

### 3.10. Grup 10: I2C Seviye Dönüştürücü (B.Cu)
- **Komponentler:** `Q1, Q2, R4, R5, R6, R7`.
- **Öteleme:** $\Delta X = -103{,}25\text{ mm}, \Delta Y = -37{,}00\text{ mm}$.
- **Konum:** $X \in [104{,}0, 112{,}0]\text{ mm}$, $Y \in [70{,}0, 78{,}5]\text{ mm}$ B.Cu katmanında. J8 modülünün kuzeyindedir.

### 3.11. Grup 12 & 13: TFT Backlight ve J3 Dekuplajı (F.Cu)
- **Backlight (Grup 12):** `Q7, R28, R29, R60` $X \in [80{,}0, 89{,}0]\text{ mm}$, $Y \in [103{,}5, 111{,}0]\text{ mm}$ F.Cu katmanında, J3'ün hemen batısındadır.
- **J3 Dekuplajı (Grup 13):** `C34` $X = 104{,}800\text{ mm}, Y = 105{,}550\text{ mm}$ F.Cu katmanında J3 Pin 1 yakınına yerleştirilmiştir.

### 3.12. Grup 14: Panel Enkoder Pull-Up Dirençleri (B.Cu)
- **Komponentler:** `R34, R35, R36`.
- **Konum:** $X = 54{,}500\text{ mm}$, $Y = 106{,}00, 109{,}00, 112{,}00\text{ mm}$ B.Cu katmanında. J9 konnektörünün batısında yer alır.

### 3.13. Grup 15: Test Noktaları
- **B.Cu Test Noktaları:** `TP6, TP7, TP8` $Y = 72{,}000\text{ mm}$ hattında $X = 74{,}0, 77{,}0, 80{,}0\text{ mm}$ koordinatlarındadır.
- **F.Cu Test Noktaları:** `TP11, TP12, TP13` $Y = 72{,}000\text{ mm}$ hattında $X = 133{,}0, 135{,}5, 138{,}0\text{ mm}$ koordinatlarındadır.

---

## 4. FreeCAD 3D Katı Kesişim Doğrulaması (`solid-check.json`)

FreeCAD 1.1 Python motoru (`Part.read` ve `distToShape`/`common`) ile J8 Waveshare Ethernet mezanini ve komşu tüm 3D katı STEP modelleri üzerinden hacimsel kesişim analizi yapılmıştır:

```json
{
  "anchor": "J8 (Waveshare_2-CH_UART_TO_ETH)",
  "total_intersection_volume_mm3": 0.0,
  "solid_collision_check_passed": true,
  "pairs": {
    "C20-J8": { "distance_mm": 1.9400, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "C10-J8": { "distance_mm": 2.3948, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "Q8-J8":  { "distance_mm": 1.6234, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "R17-J8": { "distance_mm": 6.9980, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "C21-J8": { "distance_mm": 6.9442, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "SW1-J8": { "distance_mm": 2.2125, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "SW2-J8": { "distance_mm": 2.2125, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "Q1-J8":  { "distance_mm": 2.6024, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "Q2-J8":  { "distance_mm": 5.7155, "intersection_volume_mm3": 0.0, "status": "PASSED" },
    "C33-J8": { "distance_mm": 10.2099, "intersection_volume_mm3": 0.0, "status": "PASSED" }
  }
}
```

Tüm komşu çiftlerde kesişim hacmi **$0{,}000000\text{ mm}^3$**'tür. Mekanik montaj riski sıfırdır.

---

## 5. Üretim ve Takip Notları

1. **TASK-008'e Devir:**
   - 143 elemanın tamamı elektriksel olarak gruplu ve yerleşiktir.
   - 360 adet bağlantısız öğe (unconnected item) genel routing adımı (TASK-087) kapsamında işlenecektir.
   - D5–U11 `BOOST_FB` neti hazır bağlanmış ve doğrulanmıştır.
2. **Kabul:** TASK-092 tüm kabul kriterlerini (AC #1–#6) ve DoD maddelerini eksiksiz sağlamış olup `Done` statüsüne alınmıştır.
