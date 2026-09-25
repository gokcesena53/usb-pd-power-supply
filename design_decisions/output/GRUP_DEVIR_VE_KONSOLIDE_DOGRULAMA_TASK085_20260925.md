# 15 Fonksiyonel Grubun Konsolide Doğrulaması ve Kart Yerleşimine Devir Raporu — TASK-085, 25 Eylül 2026

Bu belge, `gopo` PCB üzerindeki **15 fonksiyonel bloğun** (137 footprint) ve **6 mekanik ankrajın** (toplam 143 footprint) bireysel göreli yerleşimlerini (TASK-070 ... TASK-084) doğrular; blok zarflarını, nihai katman hedeflerini, arayüz koridorlarını ve iki turlu yerleşimin 1. turu olan Kaba Alan Planına (TASK-086) ve İnce Yerleşime (TASK-008) devir matrisini sunar.

[Konsolide Devir Matrisi Verisi (JSON)](../../hardware/docs/reports/task-085-20260925/handoff_matrix.json) ·
[Top Katman Çıktısı (SVG)](../../hardware/docs/reports/task-085-20260925/board-top.svg) ·
[Bottom Katman Çıktısı (SVG)](../../hardware/docs/reports/task-085-20260925/board-bottom.svg) ·
[DRC Doğrulama Raporu](../../hardware/docs/reports/task-010-20260925/final-drc.json)

---

## 1. 15 Blok ve Mekanik Ankraj Konsolide Devir Matrisi (AC #1, AC #3, AC #6)

Kart üzerindeki 143 footprint'in tamamı eksiksiz taranmış, 137'si 15 fonksiyonel gruba, 6'sı ise kilitli/staged mekanik ankrajlara (`H1--H4`, `J3`, `J9`) atanmıştır (%100 parite).

| No | Grup Adı & Görev | Üye Sayısı | Ana Bileşenler | Mevcut Yüz | Nihai Hedef Yüz | Boyut Zarfı ($G \times Y$, mm) | Alan ($\text{mm}^2$) | Kritik Döngü / Koridor |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **USB-C GIRIS** (TASK-070) | 7 | `J7`, `D3`, `D8`, `D9`, `U10`, `R62`, `R63` | B.Cu | **F.Cu (J7) / B.Cu** | $17{,}2 \times 18{,}7$ | $321{,}6$ | TVS/ESD doğrudan girişte, RJ45 ile $\ge 2{,}0\text{ mm}$ 3D fiş açıklığı. |
| **2** | **AP33772S PD KONTROLCU** (TASK-071) | 23 | `U1`, `Q3`, `R13` (Şönt), `TH1`, `TP1--TP5` | B.Cu | **B.Cu** | $27{,}5 \times 17{,}0$ | $467{,}5$ | R13 Kelvin diferansiyel çifti, TH1 termal temas, VBUS algılama. |
| **3** | **TPS55340 PRE-BOOST** (TASK-072) | 16 | `U11`, `L3`, `D4`, `D5`, `C27`, `C28`, `R43` | B.Cu | **B.Cu** | $27{,}0 \times 24{,}5$ | $661{,}5$ | U11 $\rightarrow$ L3 $\rightarrow$ D4 $\rightarrow$ C27 yüksek $di/dt$ döngüsü, D5--U11 FB izi $2{,}585\text{ mm}$. |
| **4** | **AOZ1284 BUCK** (TASK-073) | 19 | `U5`, `U6`, `L1`, `D2`, `C13`, `C14`, `R41` | B.Cu | **B.Cu** | $24{,}8 \times 24{,}0$ | $595{,}2$ | U5 $\rightarrow$ D2 $\rightarrow$ L1 $\rightarrow$ C13 buck döngüsü, U6 TLV431 referansı. |
| **5** | **LM74801 CIKIS ANAHTARI** (TASK-074) | 10 | `U12`, `Q5`, `D6`, `C30--C32`, `R54--R58` | B.Cu | **B.Cu** | $20{,}5 \times 14{,}5$ | $297{,}3$ | Q5 dual FET gate sürüşü, A/C Kelvin gerilim algılama, VCAP bypass. |
| **6** | **INA226 OLCUM + CIKIS** (TASK-075) | 10 | `U7`, `U13`, `RShunt1`, `J4`, `C11`, `C35` | B.Cu/F.Cu | **B.Cu (Devre) / F.Cu (J4)** | $24{,}0 \times 21{,}0$ | $504{,}0$ | 4 telli Kelvin akım algılama, J4 Banana klemens barası, ALERT pini. |
| **7** | **CIKIS DESARJI** (TASK-076) | 5 | `Q4`, `Q6`, `D10`, `R66`, `R67` (2W) | B.Cu | **B.Cu** | $14{,}5 \times 12{,}0$ | $174{,}0$ | R67 deşarj darbesi termal izolasyonu ($\ge 15\text{ mm}$ RTC ve INA226'dan). |
| **8** | **ESP32-C6 MCU** (TASK-077) | 15 | `U2`, `C5--C7`, `R1--R3`, `SW1`, `SW2` | B.Cu | **F.Cu (Top)** | $21{,}5 \times 20{,}0$ | $430{,}0$ | Anten PCB kenarından dışarı, $15\text{ mm}$ bakırsız alan, dekuplaj pinde. |
| **9** | **RTC BQ32000** (TASK-078) | 5 | `U4`, `Y1`, `C9`, `C33` (1.5F), `R24` | B.Cu | **B.Cu** | $18{,}5 \times 15{,}0$ | $277{,}5$ | Y1 32.768kHz kristal ultra kısa/simetrik ($\Delta \le 0{,}01\text{ mm}$), C33 süperkap. |
| **10** | **I2C SEVIYE DONUSTURUCU** (TASK-079) | 6 | `Q1`, `Q2`, `R4--R7` (4x 4.7k) | B.Cu | **B.Cu** | $11{,}0 \times 13{,}5$ | $148{,}5$ | İki paralel dikey sütun (SCL/SDA), sıfır kesişim, 3.3V $\leftrightarrow$ 5V köprüsü. |
| **11** | **ETHERNET MEZANIN** (TASK-080) | 7 | `J8`, `Q8`, `R17`, `C10`, `C20`, `C21`, `TP14` | B.Cu | **B.Cu** | $61{,}6 \times 26{,}4$ | $1626{,}2$ | Q8 soft-start hücresi, RJ45 altı MUTLAK KEEPOUT, TP14 \%100 erişim. |
| **12** | **TFT BACKLIGHT** (TASK-081) | 4 | `Q7`, `R28`, `R29`, `R60` | F.Cu | **F.Cu (Top)** | $12{,}0 \times 10{,}0$ | $120{,}0$ | Q7 PWM anahtarı, R60 akım sınırlama, LCD altı $Z \le 1{,}80\text{ mm}$. |
| **13** | **TFT J3** (TASK-082) | 1 | `C34` (İlişkili: Sabit Kilitli `J3`) | F.Cu | **F.Cu (Top)** | $23{,}5 \times 7{,}5$ | $176{,}3$ | J3 Pin 21-23 VDD pini dibinde C34 ($1{,}94\text{ mm}$ aralık), ZIF kapağı serbest. |
| **14** | **PANEL ENKODER** (TASK-083) | 3 | `R34`, `R35`, `R36` (İlişkili: `J9`) | B.Cu | **B.Cu (R) / F.Cu (J9)** | $7{,}5 \times 3{,}5$ | $26{,}3$ | $2{,}0\text{ mm}$ adımlı pull-up dizisi, $6 \times 24\text{ mm}$ kablo açıklığı, LCD payı $>4\text{ mm}$. |
| **15** | **TEST NOKTALARI** (TASK-084) | 6 | `TP6--TP8` (I2C), `TP11--TP13` (UART0) | F.Cu/B.Cu | **F.Cu (UART) / B.Cu (I2C)** | $7{,}6 \times 9{,}0$ | $68{,}4$ | 100-mil standart prob adımı, TP13 yerel GND klipsi, 4.0 mm düşey ayrım. |
| — | **MEKANİK ANKRAJLAR** | 6 | `H1, H2, H3, H4, J3, J9` | F.Cu | **F.Cu** | — | — | Sabit kilitli montaj delikleri, ekran FPC ve panel enkoder ankrajları. |

---

## 2. Gruplar Arası Arayüz Koridorları ve Akış Uyumu (AC #2)

Gruplar arasındaki fiziksel ve elektriksel sınır koridorları incelenmiş ve tam uyum sağlanmıştır:
1. **Giriş Güç Akışı ($X \approx 30 \rightarrow 80\text{ mm}$):**
   - `J7 USB-C` $\rightarrow$ `AP33772S` (VBUS/GND) $\rightarrow$ `TPS55340 Boost` (VBUS_SW).
   - Akış tek yönlü, doğrusal ve minimum yol uzunluğundadır.
2. **Orta Güç Akışı ($X \approx 80 \rightarrow 130\text{ mm}$):**
   - `TPS55340 Boost` $\rightarrow$ `AOZ1284 Buck` (`V_PRE` 4.8V-21V rayı ve `BOOST_FB` kenetleme koridoru).
   - C28 boost rezervuarı ile C13 buck girişi karşı karşıya bakmaktadır ($8{,}38\text{ mm}$ pad mesafesi).
   - D5--U11 BOOST_FB hattı $2{,}585\text{ mm}$ ile $\le 10\text{ mm}$ kriterini tam sağlar.
3. **Çıkış Güç Akışı ($X \approx 130 \rightarrow 160\text{ mm}$):**
   - `Buck / Boost Çıkışı` $\rightarrow$ `LM74801 Çıkış Anahtarı` $\rightarrow$ `INA226 Şöntü` $\rightarrow$ `J4 Banana Jak`.
   - Çıkış katında `Aktif Deşarj` hücresi doğrudan paralel bağlıdır; R67 güç direnci ısı kaynağı olarak RTC ve analog INA226'dan $>15\text{ mm}$ uzaktadır.
4. **Sinyal ve Teşhis Koridorları:**
   - I2C hattı: `ESP32-C6` $\rightarrow$ `Q1/Q2 Seviye Dönüştürücü` $\rightarrow$ Kuzeyde `RTC/INA226`, Güneyde `AP33772S`.
   - UART hattı: `ESP32-C6` $\rightarrow$ `J8 Ethernet` (Güney koridoru, $y=150..158\text{ mm}$).
   - SPI ve Ekran: `ESP32-C6` $\rightarrow$ `J3 FPC` (Ekran arkasından F.Cu üzerinde doğrudan kısa hatlar).

---

## 3. TASK-008 İnce Yerleşim İçin Yeniden Kontrol Listesi (AC #3, AC #5)

Tüm bloklar kart içine taşınırken (TASK-008) mutlaka uygulanacak ve doğrulanacak kontroller:

1. **J7 USB-C ve U2 MCU Top Katman Taşıması:**
   - J7 konnektörü F.Cu sol kenara oturtulurken, B.Cu'daki ESD/TVS elemanları (D3, D8, D9, U10) pcb altındaki pad çıkışlarına en yakın konumda tutulmalıdır.
   - U2 ESP32-C6 modülünün anten ucu PCB sınırından dışarı taşacak şekilde yerleştirilmeli; anten çevresindeki $15\text{ mm}$ keepout alanında hiçbir katmanda bakır veya metal olmamalıdır.
2. **J8 Ethernet Mezzanine Modülü Altı Kısıtları:**
   - Bölge 3 ($x \in [198{,}0, 214{,}5]\text{ mm}$): RJ45 THT bacak çıkıntıları nedeniyle MUTLAK KEEPOUT korunmalıdır.
   - Bölge 2 ($x \in [162{,}0, 198{,}0]\text{ mm}$): Yalnızca $Z \le 1{,}90\text{ mm}$ düşük profilli elemanlar yer alabilir.
   - TP14 test noktası modül takılıyken dışarıdan \%100 prob erişimine açık kalmalıdır.
3. **D5 -- U11 Geri Besleme İzi:**
   - D5 katodu ile U11 Pin 9 (FB) arasındaki iz uzunluğu daima $\le 10\text{ mm}$ kalmalıdır (mevcut: $2{,}585\text{ mm}$).
4. **LCD Altı Yükseklik Limiti (TASK-065):**
   - $x \in [63{,}52, 141{,}62]$, $y \in [72{,}28, 127{,}72]$ alanında F.Cu (Top) elemanlarının toplam montaj yüksekliği $\le 1{,}80\text{ mm}$ olmalıdır (L1, L3, C33, J8 bottom'dadır).
5. **J9 Panel Enkoder Kablo Koridoru:**
   - J9 etrafında lehimleme ve havya yaklaşımı için $\ge 4{,}0\text{ mm}$ açık alan korunmalı; R34--R36 pull-up dirençleri B.Cu'da tutulmalıdır.

---

## 4. Elektriksel ve Mekanik Kabul Durumu (AC #4)

- **DRC Hataları:** **0 HATA** (15x `drill_out_of_range` ve 4x `hole_clearance` TASK-010 ile tamamen çözüldü; kalan 126 ihlal silkscreen metin uyarılarıdır).
- **Bağlantısız Hat:** 360 (fiziksel routing öncesi beklenen başlangıç netlist durumu).
- **Şematik Parite:** 0 fark (143 footprint'in tamamı netlist ile birebir örtüşmektedir).
- **Sonuç:** 15 fonksiyonel grup kaba alan planı (TASK-086) ve ana ankraj dondurma (TASK-063) aşamalarına eksiksiz devredilmiştir.
