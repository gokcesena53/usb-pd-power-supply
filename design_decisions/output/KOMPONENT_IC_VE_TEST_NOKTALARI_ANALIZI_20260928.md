# REV_C Kartı Komponent-IC İlişkileri ve Test Noktaları Doğrulama Raporu

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**PCB SHA256:** `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`  
**İlgili Görevler:** TASK-096, TASK-097, TASK-098, TASK-099  

---

## 1. Yönetici Özeti

REV_C kartı üzerindeki 144 footprintin (10 IC, 52 Direnç, 34 Kapasitör, 10 Diyot, 8 Transistör/FET, 2 Güç Bobini, 1 Kristal, 14 Test Noktası, 5 Konnektör/Arayüz, 2 Buton, 1 Termistör, 4 Montaj Deliği, 1 Mekanik Enkoder) tamamı KiCad 10 Python API (`pcbnew`) kullanılarak taranmış ve iki temel odak alanında denetlenmiştir:
1. **Komponentlerin Bağlı Oldukları IC'lerle Olan İlişkileri (Pin Bazında):** Her bir IC'nin tüm pinlerine bağlı komponentlerin fiziksel konumları, katman uyumu (aynı katman vs zıt katman), doğrusal pin-ped mesafeleri ve elektriksel kurallara (dekuplaj, geribesleme bölücüleri, gate sürüş döngüleri, Kelvin algılama, yüksek frekanslı anahtarlama döngüleri) uyumu.
2. **Test Noktalarının Yerleşimi ve Kapsamı (TP1–TP14):** Test noktalarının fiziksel koordinatları, prob erişilebilirliği, mekanik engeller (özellikle üst kattaki 3.2" LCD ekran ve alt kattaki Ethernet mezanin modülü) ve kart doğrulama için gerekli hayati güç/sinyal hatlarının kapsamı.

---

## 2. Entegre Devreler (IC) ve Bağlı Komponentlerin İlişki Matrisi

### 2.1. U1: AP33772S USB PD Sink Denetleyici (B.Cu, X=76.50, Y=120.50 mm)
- **LDO ve Çekirdek Dekuplajı:**
  - `C1` (100n 0402): Pin 12 (V18 LDO) çıkışında, mesafesi **3.77 mm**. Katman: `B.Cu` (AYNI KATMAN).
  - `C4` (1u0 0603): Pin 20 (PD_5V LDO) çıkışında, mesafesi **3.73 mm**. Katman: `B.Cu` (AYNI KATMAN).
  - `C2` (100n 0402): Pin 15 (IFB akım filtresi), mesafesi **3.65 mm**. Katman: `B.Cu` (AYNI KATMAN).
- **Lokal Kontrol Dirençleri:**
  - `R12` (6k2): Pin 23 (PWR_EN pull-down), mesafesi **2.54 mm**. Katman: `B.Cu`.
  - `R21` (100k): Pin 11 (VSEL pull-down), mesafesi **3.09 mm**. Katman: `B.Cu`.
  - `R8` (10k): Pin 9 (PD_INT_5V pull-up), mesafesi **3.18 mm**. Katman: `B.Cu`.
  - `R14` (2k2): Pin 8 (LED akım sınırlayıcı), mesafesi **3.96 mm**. Katman: `B.Cu`.
- **Güç Anahtarlama ve Akım Algılama:**
  - `Q3` (SQJB60EP Dual N-FET): Pin 24 (VBUS Sensed) mesafesi **5.85 mm**. Katman: `B.Cu`.
  - `R11` (5m0 2512 Şönt): Pin 1 (USB_VBUS, 16.98 mm) ve Pin 24 (PD_VBUS_SENSED, 15.63 mm). B.Cu katmanında yer alır. TASK-087'de sıkı diferansiyel Kelvin iz çifti şarttır.
  - `TH1` (10k NTC): Pin 13 (OTP) mesafesi **11.31 mm**, Q3 güç transistörünün hemen yanında konumlandırılmıştır.
- **USB-C Giriş / ESD Zinciri:**
  - `J7` (USB-C) -> `D8, D9` (SMF30A TVS) -> `R62, R63` (5k1) -> Via -> `U1` (Pin 16/17 CC1/CC2). TVS diyotları konnektör pini ile IC arasında doğru koruma sırasındadır.

### 2.2. U2: ESP32-C6-MINI-1-H4 Ana MCU (F.Cu, X=77.92, Y=75.06 mm)
- **Besleme Dekuplajı:**
  - `C5` (22u 0805) ve `C6` (100n 0402): Pin 3 (+3.3V) girişine mesafesi **10.4 mm**. Katman: `F.Cu` (AYNI KATMAN).
- **Reset ve Boot Arayüzü:**
  - `C7` (1u 0603) ve `R1` (10k 0402): Pin 8 (EN) RC reset devresi, mesafeleri sırasıyla **9.05 mm** ve **11.00 mm**. Katman: `F.Cu`.
  - `SW1` (BOOT) ve `SW2` (RESET): Kartın sol kenarında `B.Cu` katmanında yer alır; kullanıcı buton erişimi için idealdir.
- **Hızlı USB Sinyal Bütünlüğü:**
  - `R2` (22R) ve `R3` (22R): Pin 17/18 (USB D-/D+) sönümleme dirençleri, mesafeleri **8.19 mm** ve **9.28 mm**. Katman: `F.Cu`.
  - `U10` (USBLC6-2SC6): USB D+/D- hattında J7 konnektörüne **3.71 mm** mesafede olup U2'yi harici ESD darbelerinden korur.
- **Anten Keepout:** U2 modülünün dahili anteni PCB sol-üst kenar sınırındadır; altında bakır bulunmamaktadır.

### 2.3. U3: INA226 Çıkış Akım/Gerilim Monitörü (B.Cu, X=136.75, Y=112.10 mm)
- **Dekuplaj ve Çekme Dirençleri:**
  - `C11` (100n 0402): Pin 6 (+3.3V) mesafesi **2.97 mm**. Katman: `B.Cu`.
  - `R27` (10k 0402): Pin 3 (ALERT) mesafesi **2.99 mm**. Katman: `B.Cu`.
- **Kelvin Akım Algılama:**
  - `RShunt1` (5m0 2512): Pin 8/9/10 mesafesi **4.01 mm**. Tam simetrik Kelvin pad yerleşimi.
- **Çıkış TVS:**
  - `D7` (SMBJ30A): OUT_POS barasında, mesafesi **7.32 mm**.

### 2.4. U4: BQ32000 Gerçek Zamanlı Saat (B.Cu, X=143.00, Y=82.00 mm)
- **Osilatör Kristali:**
  - `Y1` (32.768 kHz tuning fork): Pin 1 (OSCI) ve Pin 2 (OSCO) mesafesi **8.98 mm**. Katman: `B.Cu`. Osilatör döngü alanı minimaldir ve güç anahtarlama hatlarından uzaktadır.
- **Dekuplaj ve Yedekleme:**
  - `C9` (1u 0603): Pin 8 (+3.3V) mesafesi **3.33 mm**. Katman: `B.Cu`.
  - `C33` (1F5 Süperkapasitör): Pin 3 (VBACK) mesafesi **31.02 mm**.

### 2.5. U5: AOZ1284PI 3.3V Buck Regülatör (B.Cu, X=126.70, Y=105.31 mm)
- **Sıcak Döngü ve Giriş Filtresi:**
  - `C14` (100n 0603 HF baypas): U5 Exposed Pad (Pin 9 / VIN) mesafesi **5.31 mm**. Katman: `B.Cu`.
  - `C12`, `C13` (4u7 1210 bulk giriş): Exposed Pad mesafesi **6.00 mm** ve **9.65 mm**.
  - `L1` (22uH güç bobini): Pin 1 (LX) mesafesi **6.05 mm**. Katman: `B.Cu`.
  - `D2` (SS2060FL boot diyotu) ve `C17` (100n boot kapasitörü): Pin 1/2 mesafesi **2.20 mm** ve **4.72 mm**.
- **Geribesleme ve Kompanzasyon:**
  - `R39` (10k2) ve `R40` (3k24) FB gerilim bölücüsü: Pin 6 (FB) mesafesi **5.49 mm** ve **7.50 mm**.
  - `R41` (51k) COMP direnci: Pin 5 (COMP) mesafesi **2.57 mm**.
  - `C18` (10n) Soft-start: Pin 7 (SS) mesafesi **4.10 mm**.
  - `R38` (100k) Frekans ayarı: Pin 4 mesafesi **2.45 mm**.

### 2.6. U11: TPS55340 Pre-Boost Regülatör (B.Cu, X=98.00, Y=121.00 mm)
- **Anahtarlama Sıcak Döngüsü:**
  - `D4` (SX36 Schottky diyot): Pin 1/2 (SW) mesafesi **4.39 mm**.
  - `C27`, `C28` (4u7 1210 çıkış filtreleri): D4 katoduna doğrudan bitişik. Sıcak döngü çevresi $\approx 24\text{ mm}$ olup minimal parazitik endüktans sağlar.
  - `L3` (6u8 boost bobini): Pin 1/2 (SW) mesafesi **10.89 mm**.
- **Kontrol ve Geri Besleme:**
  - `D5` (BAS16H clamp diyotu): Pin 9 (FB) mesafesi **2.14 mm**.
  - `R48` (30k1) ve `R49` (9k76) FB bölücüsü: Pin 9 mesafesi **7.84 mm** ve **7.88 mm**.
  - `R52` (2k) COMP direnci: Pin 8 mesafesi **5.01 mm**.
  - `C23` (47n) Soft-start: Pin 5 mesafesi **4.12 mm**.
  - `R47` (78k7) Frekans direnci: Pin 10 mesafesi **3.58 mm**.

### 2.7. U12: LM74801-Q1 İdeal Diyot ve Çıkış Güç Anahtarı Sürücüsü (F.Cu, X=135.50, Y=101.50 mm)
- **Gate Sürüş Döngüsü:**
  - `Q5` (SQJB60EP Dual FET): Pin 1 (DGATE) mesafesi **3.94 mm**, Pin 8 (HGATE) mesafesi **9.09 mm**. Katman: `F.Cu` (AYNI KATMAN).
  - `C31` (220n şarj pompası kapasitörü): Pin 10/11 mesafesi **3.21 mm**.
  - `D6` (BZT52C12 12V Zener gate clamp): Mesafesi **8.49 mm**.
  - `R54` (1k HGATE soft-start direnci): Mesafesi **13.58 mm**.
- **Aşırı Gerilim ve Enable:**
  - `R56` (10k) ve `R55` (237k) OV Sense bölücüsü: Pin 5 mesafesi **6.43 mm** ve **6.94 mm**.
  - `R58` (100k pull-down): Pin 6 (EN) mesafesi **5.30 mm**.

### 2.8. U13: 74LVC1G08 Donanım Koruma VE Kapısı (B.Cu, X=129.00, Y=123.10 mm)
- `C35` (100n dekuplaj): Pin 5 (+3.3V) mesafesi **1.88 mm**.
- `R61` (4k7 pull-down): Pin 1 mesafesi **2.87 mm**.
- `Q4` (BSS138P deşarj kontrol FET'i): Pin 4 mesafesi **11.15 mm**.

---

## 3. Test Noktaları (TP1–TP14) Doğrulama Bulguları

| Ref | Net Adı | Katman | Konum $(X, Y)$ | Doğrulama & Erişim Durumu | Aksiyon / Çözüm |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`TP1`** | `USB_VBUS` | `B.Cu` | $(71.50, 101.30)$ | Giriş VBUS prob noktası. R11'e 2.65 mm mesafede. Açık ve erişilebilir. | Uygun. |
| **`TP2`** | `PD_VBUS_SENSED` | `B.Cu` | $(82.00, 102.50)$ | U1 VBUS algılama gerilimi. R11'e 2.59 mm mesafede. Açık ve erişilebilir. | Uygun. |
| **`TP3`** | `PD_VOUT` | `B.Cu` | $(90.80, 103.60)$ | Pre-boost giriş güç barası. Açık ve erişilebilir. | Uygun. |
| **`TP4`** | `PD_5V` | `B.Cu` | $(70.00, 127.50)$ | AP33772S dahili 5V LDO çıkışı. Açık ve erişilebilir. | Uygun. |
| **`TP5`** | `PD_GATE` | `B.Cu` | $(74.00, 113.50)$ | Q3 gate gerilimi. Açık ve erişilebilir. | Uygun. |
| **`TP6`** | `PD_I2C_SCL_3V3`| `B.Cu` | $(74.00, 72.00)$ | I2C saat hattı. Açık ve erişilebilir. | Bitişiğine osiloskop için GND TP eklenmeli. |
| **`TP7`** | `PD_I2C_SDA_3V3`| `B.Cu` | $(77.00, 72.00)$ | I2C veri hattı. Açık ve erişilebilir. | Bitişiğine osiloskop için GND TP eklenmeli. |
| **`TP8`** | `PD_INT_3V3` | `B.Cu` | $(80.00, 72.00)$ | PD kesme hattı. Açık ve erişilebilir. | Bitişiğine osiloskop için GND TP eklenmeli. |
| **`TP9`** | `/MCU/ETH_CFG0` | `F.Cu` | $(94.50, 83.00)$ | **KRİTİK HATA:** 3.2" LCD ekran modülünün tam altında kalıyor. Montaj sonrası erişilemez! | **Alt kata (`B.Cu`) aktarılmalı.** |
| **`TP10`**| `/MCU/ETH_PWR_EN`| `F.Cu` | $(97.00, 83.00)$ | **KRİTİK HATA:** 3.2" LCD ekran modülünün tam altında kalıyor. Montaj sonrası erişilemez! | **Alt kata (`B.Cu`) aktarılmalı.** |
| **`TP11`**| `/MCU/UART_TX` | `F.Cu` | $(133.00, 72.00)$| Seri port konsol çıkışı. LCD üst sınırına $0.4\text{ mm}$ mesafede (sınırda). | $Y \approx 71.0\text{ mm}$'ye veya B.Cu'ya kaydırılmalı. |
| **`TP12`**| `/MCU/UART_RX` | `F.Cu` | $(135.50, 72.00)$| Seri port konsol girişi. LCD üst sınırına $0.4\text{ mm}$ mesafede (sınırda). | $Y \approx 71.0\text{ mm}$'ye veya B.Cu'ya kaydırılmalı. |
| **`TP13`**| `GND` | `F.Cu` | $(138.00, 72.00)$| UART referans toprağı (TX/RX ile $2.54\text{ mm}$ adımlı). LCD sınırında. | TP11/TP12 ile birlikte kaydırılmalı. |
| **`TP14`**| `/MCU/ETH_RUN` | `B.Cu` | $(107.00, 82.15)$| J8 Ethernet mezanin sınırına $1.1\text{ mm}$ mesafede (dar erişim). | Sağa ($X \approx 110.0\text{ mm}$) kaydırılmalı. |

### 3.1. Eksik Olan Test Noktaları
Kartın ilk çalıştırma (bring-up), hata ayıklama ve doğrulama süreçlerinde doğrudan prob bağlanması gereken aşağıdaki düğümlerde test noktası bulunmamaktadır:
1. `+3.3V` (MCU, RTC, INA226 ve lojik devrelerin ana besleme rayı).
2. `V_PRE` (Boost regülatörü çıkışı / Buck regülatörü girişi, 5V–20V ara barası).
3. `OUT_POS` (Güç kaynağının nihai çıkış gerilimi; kalın J4 kablosu lehimlenmeden önce prob ölçümü için).
4. `SW_EN` (Çıkış güç FET'i ve aktif deşarj devresini kontrol eden güvenlik sinyali).
5. `GND` (TP6–TP8 I2C test grubunun yanında osiloskop yaylı şasi probu takılabilecek bitişik toprak pedi).

---

## 4. Sonuç ve Görev Planı

1. **TASK-098 (Test Noktalarının Düzenlenmesi):** Açıldı. TP9/TP10 alt kata alınacak, UART hücresi emniyetli mesafeye kaydırılacak, eksik güç ve GND test noktaları eklenecek.
2. **TASK-099 (Aktif ve Manyetik Komponentlerin Denetimi):** Açıldı. D, Q, L, Y ve IC-IC sinyal zincirleri denetim kriterleriyle kaydedildi.
3. **TASK-097 (Direnç ve Kapasitör Denetimi):** Güncellenmiş gerçek PCB verisiyle tamamlanacak.
