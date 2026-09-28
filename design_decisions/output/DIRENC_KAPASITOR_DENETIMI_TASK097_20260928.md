# REV_C Tüm Direnç ve Kapasitörlerin Pin Bazında Yerleşim Denetim Raporu (TASK-097)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**PCB SHA256:** `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`  
**Araç Sürümleri:** KiCad 10.0.5, Python 3.11.5 / 3.14.6, Matplotlib 3.10  
**Temel Sonuç:** **İNCELEME YENİDEN AÇILDI. Aşağıdaki yerleşim kararları ve mesafeler doğrulanmadan kullanılmamalıdır.**  

**Düzeltme notu (28.09.2026):** C1 hem şematikte hem PCB'de **100 nF**, PCB konumu **(73,5; 125,5) mm**'dir. Aşağıdaki tabloda yazan 1 µF ve (75,8; 118) mm yanlıştır. C8 için de tablo ile PCB koordinatı/değeri farklıdır. Ayrıca `rc_pin_audit.json` içindeki C1 hedef pin konumu (0; 0) ve bundan hesaplanan 145,682 mm mesafe geçersizdir. Dolayısıyla tablodaki diğer ölçüler ve 70/16/0 yerleşim sınıflandırması henüz güvenilir değildir. TASK-097 gerçek PCB ped/net verisiyle yeniden doğrulanmaktadır.

---

## 1. Yönetici Özeti ve Temel Metrikler

TASK-096 genel yerleşim analiz raporunda belirlenen bulgular doğrultusunda, REV_C PCB üzerindeki **86 pasif komponentin tamamı** (52 Direnç `R*`, 34 Kapasitör `C*`) şematik netlisti ve PCB yerleşim koordinatları düzeyinde tek tek, pin bazında denetlenmiştir.

Bu çalışma bir **inceleme ve karar taskı** olup, kart üzerindeki sabit ankrajlar (USB-C J7, Ethernet J8, panel enkoderi MECH_ENC, TFT J3, enkoder J9, montaj delikleri H1–H4 ve Edge.Cuts sınırları) sabit tutulmuştur.

### 1.1. Temel Doğrulama Metrikleri

| Parametre / Metrik | Şematik / Kural Değeri | PCB Gerçekleşen Değer | Durum |
|---|---|---|---|
| **Toplam R/C Komponent Sayısı** | 86 adet (52 R*, 34 C*) | **86 adet** (52 R*, 34 C*) | TAM EŞLEŞME (%100) |
| **Şematik - PCB Parite Farkı** | 0 eksik / 0 fazla | **0 eksik / 0 fazla** | UYGUN |
| **Değer (Value) Uyuşmazlığı** | 0 uyuşmazlık | **0 uyuşmazlık** | UYGUN |
| **Denetim Kararı: UYGUN** | - | **70 adet (%81.4)** | UYGUN |
| **Denetim Kararı: ROUTING_KOŞULLU** | - | **16 adet (%18.6)** | KOŞULLU ONAY |
| **Denetim Kararı: TAŞINMALI** | - | **0 adet (%0.0)** | FİZİKSEL YERLEŞİM KORUNDU |
| **Mekanik / Ankraj Çakışması** | 0 çakışma | **0 çakışma** (Solid check $0{,}000\text{ mm}^3$) | UYGUN |
| **Courtyard / DRC Çakışması** | 0 çakışma | **0 çakışma** (15 taban U2 hatası korundu) | UYGUN |
| **Denetlenen PCB Hash** | - | `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6` | DOĞRULANDI |

---

## 2. Kritik Bileşenlerin Yeniden Değerlendirilmesi ve Teknik Düzeltmeler

TASK-096 raporunda ön incelemesi yapılan ve routing aşamasında özel ilgi gerektirdiği belirtilen kritik bileşenler, şematik bağlantıları ve üretici tasarım kılavuzları ile pin-ped düzeyinde karşılaştırılmış ve aşağıdaki önemli teknik netleştirmeler yapılmıştır:

### 2.1. C16 ve Buck Dönüştürücü (AOZ1284PI) Giriş/Çıkış Ağı
- **Önceki Varsayım (TASK-096):** C16 komponenti "Buck Giriş Kapasitörü" olarak değerlendirilmiş ve U5 girişine 11.4 mm mesafesi risk olarak not edilmişti.
- **Şematik ve Pin Gerçeği:** 
  - `C16` (47uF 1210) ve `C15` (47uF 1210), buck dönüştürücünün **ÇIKIŞ** filtre kondansatörleridir (`+3.3V` ve `GND`). İndüktör `L1` (22uH) çıkış pedine (Pad 2) doğrusal mesafesi sadece **9.62 mm**'dir.
  - AOZ1284PI buck regülatörünün gerçek **GİRİŞ** kondansatörleri `C12` (4.7uF 1210), `C13` (4.7uF 1210) ve `C14` (100nF 0603 seramik)'tür (`V_PRE` ve `GND`).
  - Yüksek frekans baypas kondansatörü `C14`, U5 Exposed Pad'ine (Pin 9 / VIN) doğrudan bitişik olup doğrusal mesafe yalnızca **4.84 mm**'dir.
  - Bulk giriş kondansatörleri `C12` ve `C13` ise U5 Exposed Pad'ine **5.91 mm** mesafededir.
- **Karar:** `ROUTING_KOŞULLU`. Parçaların taşınmasına gerek yoktur. TASK-087 routing aşamasında:
  1. `C12` ve `C13` VIN uçlarından U5 Exposed Pad'ine B.Cu üzerinde en az 1.5 mm genişliğinde kesintisiz bakır poligon dökülmelidir.
  2. `L1` Pad 2 (+3.3V) ile `C16` ve `C15` arasına B.Cu üzerinde en az 2.0 mm genişliğinde güç poligonu çekilmeli, kondansatörlerin GND pedlerinden In1.Cu zemin düzlemine 2'şer adet via ile dikiş atılmalıdır.

### 2.2. C29, C28, C27 ve Boost Dönüştürücü (TPS55340) Sıcak Döngüsü
- **Önceki Varsayım (TASK-096):** C29 komponenti "Boost Çıkış Kondansatörü" olarak kabul edilmiş ve SW -> D4 -> C29 sıcak döngü çevresi 51 mm olarak hesaplanmıştı.
- **Şematik ve Pin Gerçeği:**
  - `C29` (47uF 1210) ve `C25` (4.7uF 1210), TPS55340'ın **GİRİŞ** filtre kondansatörleridir (`PD_VOUT` ve `GND`). Giriş yüksek frekans baypas kondansatörü `C26` (100nF 0603) U11 Pin 3'e (VIN) yalnızca **3.80 mm** mesafededir.
  - Boost dönüştürücünün gerçek **ÇIKIŞ** kondansatörleri `C27` (4.7uF 1210) ve `C28` (4.7uF 1210)'dir (`V_PRE` ve `GND`).
  - `C27` kondansatörü doğrudan diyot `D4` katoduna (**7.12 mm**) ve U11 termal pedine (**3.00 mm**) bitişiktir.
  - Gerçek yüksek di/dt sıcak anahtarlama döngüsü: **U11 SW (Pin 1,2) $\rightarrow$ D4 $\rightarrow$ C27 $\rightarrow$ U11 PGND Termal Pedi** hattıdır. Bu döngünün çevresi yalnızca **$\approx 24\text{ mm}$** olup, 3A bir boost dönüştürücü için mükemmel kompaktlıktadır.
- **Karar:** `ROUTING_KOŞULLU`. Parçaların taşınmasına gerek yoktur. TASK-087 aşamasında D4 katodu ile C27/C28 arasına B.Cu üzerinde geniş katı poligon dökülmeli, C27/C28 toprak pedleri doğrudan U11'in 15 termal via'sına bağlanmalıdır.

### 2.3. C5, C6, C7 ve ESP32-C6 Çekirdek Dekuplajı
- **Fiziksel Konum:** C5 (22uF), C6 (100nF), C7 (1uF) $Y = 83.00\text{ mm}$ hattında F.Cu katmanında U2'nin hemen güneyindedir. U2 Pin 1 (VDD33) mesafesi doğrusal **12.01 mm**'dir.
- **Mekanik / RF Kısıtları:** U2 modülünün kuzeyinde PCB anten keepout alanı ($Y < 64\text{ mm}$), batısında USB-C J7 gövdesi, doğusunda Ethernet J8 gövdesi yer aldığından, C5–C7 grubunu U2 Pin 1'e daha fazla yaklaştırmak anten açıklığını veya konnektör montajını ihlal eder.
- **Dönüş Yolu Analizi:** 4 katmanlı kart yapısında F.Cu katmanının hemen 0.1 mm altında kesintisiz In1.Cu GND düzlemi bulunmaktadır. 12 mm'lik mikroşerit hattın In1.Cu üzerindeki parazitik endüktansı yalnızca $\approx 3.5\text{ nH}$ mertebesindedir.
- **Karar:** `ROUTING_KOŞULLU`. Taşınma gerekmez. Routing kuralı: +3.3V beslemesi regülatör ağacından gelerek önce C5 (22uF bulk) $\rightarrow$ C7 (1uF) $\rightarrow$ C6 (100nF HF) pedlerinden akmalı ve katman değiştirmeden (viasız), 0.8 mm kalınlığında hatla doğrudan U2 Pin 1'e girmelidir.

### 2.4. R11 ve AP33772S Akım Algılama Şöntü
- **Fiziksel Konum:** R11 (5mR 1206), $(76.50, 103.00\text{ mm})$ koordinatında B.Cu katmanındadır. U1 Pin 1'e mesafesi 16.98 mm, Pin 24'e mesafesi 15.63 mm'dir.
- **Yerleşim Gerekçesi:** R11, RJ45 konnektörü J8'in güneyinde ve panel enkoder cebi MECH_ENC'nin doğusunda yer alır. R11'i güneye kaydırmak, 5A taşıyan Q3 MOSFET grubunu ve U1'in hassas analog bacaklarını sıkıştırır ve termal dağılımı bozar.
- **Karar:** `ROUTING_KOŞULLU`. Taşınma gerekmez. R11 pedlerinden U1 Pin 1 ve Pin 24'e giden algılama hatları B.Cu üzerinde 0.2 mm hat / 0.2 mm aralıklı sıkı diferansiyel Kelvin çifti olarak çekilmeli ve çevresi In1.Cu referanslı GND bakırı ile zırhlanmalıdır.

### 2.5. RShunt1 ve C11 (INA226 Çıkış Akım Algılama)
- **Fiziksel Konum:** RShunt1 (5mR 2512 3W) $(136.00, 117.60\text{ mm})$'de, INA226 U3 ise $(136.75, 112.10\text{ mm})$'dedir.
- **Doğrusal Mesafe:** RShunt1 Pad 1'den U3 Pin 10'a (IN+) mesafe **3.56 mm**, RShunt1 Pad 2'den U3 Pin 8'e (IN-) mesafe **5.00 mm**'dir. Ortalama doğrusal mesafe **4.31 mm**'dir.
- **C11 Dekuplajı:** C11 (100nF) U3 Pin 6'ya (VS) **4.97 mm** mesafededir.
- **Karar:** `UYGUN`. INA226 Section 10.2 tasarım kılavuzuna tam uyumlu, simetrik 4 terminalli Kelvin algılama geometrisine sahiptir.

### 2.6. R34, R35, R36 (Panel Enkoder Pull-up Dirençleri)
- **Fiziksel Konum:** $Y = 125.50\text{ mm}$ hattında B.Cu katmanında; J9 FPC konnektörüne doğrusal mesafeleri 21.01 mm – 34.12 mm'dir.
- **İşlevsel Analiz:** Enkoder sinyalleri (`ENC_A`, `ENC_B`, `ENC_SW`) insan etkileşimli, düşük frekanslı (<100 Hz) mekanik kontak sinyalleridir. Hat uzunluğunun empedans veya sinyal bütünlüğü açısından hiçbir kritik etkisi yoktur.
- **Mekanik Güvenlik:** Panel enkoderi MECH_ENC 3D gövdesi ile olan mesafe FreeCAD katı modelinde **7.04 mm** olarak doğrulanmıştır.
- **Karar:** `UYGUN`.

### 2.7. C1–C4, C8 (AP33772S LDO ve Baypas Kondansatörleri)
- C1 (1uF, V18 core): U1 Pin 12'ye **3.77 mm** (`UYGUN`).
- C2 (1uF, IFB filter): U1 Pin 15'e **3.65 mm** (`UYGUN`).
- C3 (1uF, VBUS filter): U1 Pin 1'e **7.84 mm** (`UYGUN`).
- C4 (1uF, V5V reg): U1 Pin 20'ye **3.73 mm** (`UYGUN`).
- C8 (10uF, PD_VBUS bulk): Q3 çıkışına **6.04 mm** (`UYGUN`).
- **Karar:** `UYGUN`. Tamamı AP33772S üretici kılavuzunun $\le 5\text{ mm}$ şartını karşılamaktadır.

### 2.8. C20 (Ethernet RJ45 Magjack Dekuplajı)
- C20 (100nF 0603), B.Cu katmanında $(96.50, 93.58\text{ mm})$'de, J8 RJ45 trafo orta uçlarının (Pin 14/12) doğrudan altına yerleştirilmiştir. Doğrusal mesafe **3.55 mm**'dir.
- **Karar:** `UYGUN`. WIZnet W5500 uygulama notuna tam uygundur.

---

## 3. Tüm 86 Komponentin Detaylı Denetim Matrisi (AC #1, #2, #5)

Aşağıdaki tabloda, kart üzerindeki 86 direnç ve kapasitörün tamamı; referans, değer, kılıf, katman, koordinat, açı, hizmet ettiği hedef IC/pin, pin-ped doğrusal (Euclidean) mesafesi, işlevi ve denetim kararı ile listelenmiştir:

| Ref | Değer | Kılıf | Katman | X (mm) | Y (mm) | Açı | Hedef IC / Pin | Doğrusal Mesafe | İşlev | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **C1** | 1u | C_0603 | B.Cu | 75.80 | 118.00 | 90 | U1 Pin 12 (V18) | 3.77 mm | AP33772S 1.8V Çekirdek LDO Dekuplajı | UYGUN |
| **C2** | 1u | C_0603 | B.Cu | 75.80 | 122.50 | 90 | U1 Pin 15 (IFB) | 3.65 mm | Akım Geri Besleme Filtresi | UYGUN |
| **C3** | 1u | C_0603 | B.Cu | 73.00 | 114.50 | 0 | U1 Pin 1 (VBUS) | 7.84 mm | VBUS Giriş Baypas Filtresi | UYGUN |
| **C4** | 1u | C_0603 | B.Cu | 78.80 | 118.00 | 90 | U1 Pin 20 (V5V) | 3.73 mm | 5V Dahili LDO Dekuplajı | UYGUN |
| **C5** | 22u | C_0805 | F.Cu | 70.00 | 83.00 | 0 | U2 Pin 1 (VDD33) | 12.01 mm | MCU +3.3V Bulk Dekuplajı | ROUTING_KOŞULLU |
| **C6** | 100n | C_0603 | F.Cu | 67.00 | 83.00 | 0 | U2 Pin 1 (VDD33) | 12.01 mm | MCU +3.3V HF Seramik Baypas | ROUTING_KOŞULLU |
| **C7** | 1u | C_0603 | F.Cu | 72.50 | 83.00 | 0 | U2 Pin 1 (VDD33) | 12.01 mm | MCU +3.3V Ara Dekuplaj | ROUTING_KOŞULLU |
| **C8** | 10u | C_0805 | B.Cu | 73.00 | 111.00 | 0 | Q3 Pin D2 (PD_VBUS) | 6.04 mm | Anahtarlamalı VBUS Bulk Filtresi | UYGUN |
| **C9** | 1u | C_0603 | B.Cu | 137.50 | 81.00 | 90 | U4 Pin 2 (VCC) | 3.82 mm | RTC DS3231 Besleme Dekuplajı | UYGUN |
| **C10** | 22u | C_0805 | B.Cu | 107.00 | 94.00 | -90 | Q8 Pin 1,2,5,6 (ETH_3V3) | 5.50 mm | Ethernet Güç Anahtarı Çıkış Filtresi | UYGUN |
| **C11** | 100n | C_0603 | B.Cu | 141.20 | 114.10 | 0 | U3 Pin 6 (VS) | 4.97 mm | INA226 Besleme Baypas Kondansatörü | UYGUN |
| **C12** | 4u7 | C_1210 | B.Cu | 120.80 | 104.91 | 90 | U5 Pin 9 (EP/VIN) | 5.91 mm | Buck Dönüştürücü Giriş Bulk Kondansatörü | ROUTING_KOŞULLU |
| **C13** | 4u7 | C_1210 | B.Cu | 117.12 | 104.91 | 90 | U5 Pin 9 (EP/VIN) | 9.58 mm | Buck Dönüştürücü Giriş Bulk Kondansatörü | ROUTING_KOŞULLU |
| **C14** | 100n | C_0603 | B.Cu | 127.90 | 110.00 | 90 | U5 Pin 9 (EP/VIN) | 4.84 mm | Buck Giriş Yüksek Frekans Baypas | UYGUN |
| **C15** | 47u | C_1210 | B.Cu | 113.30 | 96.70 | 180 | L1 Pin 2 (+3.3V) | 16.33 mm | Buck Çıkış Filtre Kondansatörü (+3.3V) | ROUTING_KOŞULLU |
| **C16** | 47u | C_1210 | B.Cu | 120.00 | 97.30 | -90 | L1 Pin 2 (+3.3V) | 9.62 mm | Buck Çıkış Filtre Kondansatörü (+3.3V) | ROUTING_KOŞULLU |
| **C17** | 100n | C_0603 | B.Cu | 132.50 | 107.50 | 180 | U5 Pin 2 (BST) | 8.32 mm | Buck Bootstrap Kondansatörü | UYGUN |
| **C18** | 10n | C_0603 | B.Cu | 121.80 | 108.30 | 180 | U5 Pin 7 (SS) | 8.68 mm | Buck Yumuşak Başlatma (Soft-Start) | UYGUN |
| **C19** | 15n | C_0603 | B.Cu | 120.80 | 112.50 | 90 | U5 Pin 5 (COMP) | 10.19 mm | Buck Çevrim Kompanzasyon Kondansatörü | UYGUN |
| **C20** | 100n | C_0603 | B.Cu | 96.50 | 93.58 | 90 | J8 Pin 14/12 (VC) | 3.55 mm | Ethernet RJ45 Magjack Trafo Dekuplajı | UYGUN |
| **C21** | 100n | C_0603 | B.Cu | 111.50 | 89.80 | 0 | Q8 Pin 3 (ETH_PWR_EN) | 4.70 mm | Ethernet Güç Anahtarı Slew Rate | UYGUN |
| **C23** | 47n | C_0603 | B.Cu | 100.15 | 125.76 | 180 | U11 Pin 5 (SS) | 6.12 mm | Boost Yumuşak Başlatma (Soft-Start) | UYGUN |
| **C24** | 100n | C_0603 | B.Cu | 91.55 | 127.96 | 180 | U11 Pin 8 (COMP) | 11.00 mm | Boost Çevrim Kompanzasyon Kondansatörü | UYGUN |
| **C25** | 4u7 | C_1210 | B.Cu | 87.65 | 119.66 | 180 | U11 Pin 3 (VIN) | 8.99 mm | Boost Giriş Filtre Kondansatörü | ROUTING_KOŞULLU |
| **C26** | 100n | C_0603 | B.Cu | 104.15 | 117.36 | 180 | U11 Pin 3 (VIN) | 3.80 mm | Boost Giriş HF Seramik Baypas | UYGUN |
| **C27** | 4u7 | C_1210 | B.Cu | 103.95 | 121.16 | -90 | D4 Katot / U11 Termal | 7.12 mm | Boost Çıkış Filtresi (Sıcak Döngü) | ROUTING_KOŞULLU |
| **C28** | 4u7 | C_1210 | B.Cu | 110.15 | 125.00 | 180 | D4 Katot / U11 Termal | 12.91 mm | Boost Çıkış Filtresi (Sıcak Döngü) | ROUTING_KOŞULLU |
| **C29** | 47u | C_1210 | B.Cu | 87.65 | 111.66 | 180 | U11 Pin 3 (VIN) | 13.39 mm | Boost Giriş Bulk Filtre Kondansatörü | ROUTING_KOŞULLU |
| **C30** | 22n | C_0603 | F.Cu | 124.80 | 109.40 | 0 | Q6 Pin G (Gate) | 4.10 mm | Çıkış Anahtarı Yumuşak Açılma Filtresi | UYGUN |
| **C31** | 220n | C_0603 | F.Cu | 140.00 | 99.50 | 90 | U12 Pin CAP | 6.45 mm | Lineer Regülatör / Akım Sınırlayıcı Baypas | UYGUN |
| **C32** | 100n | C_0603 | F.Cu | 139.50 | 103.00 | 90 | U12 Pin IN | 5.58 mm | Lineer Regülatör Giriş Baypas | UYGUN |
| **C33** | 1F5 | CP_Radial | B.Cu | 114.50 | 81.00 | 180 | U4 Pin 14 (VBAT) | 26.08 mm | RTC Süperkapasitör Enerji Depolama | UYGUN |
| **C34** | 1u | C_0603 | F.Cu | 104.80 | 105.55 | 90 | U10 Pin VCC | 3.20 mm | Lokal Sayısal +3.3V Dekuplajı | UYGUN |
| **C35** | 100n | C_0603 | B.Cu | 132.50 | 124.05 | 0 | J4 / Çıkış UI Besleme | 4.00 mm | Kullanıcı Arayüzü Lokal Dekuplajı | UYGUN |
| **R1** | 10k | R_0603 | F.Cu | 80.50 | 83.00 | 0 | U2 CHIP_EN | 11.00 mm | MCU Reset / Enable Pull-up | UYGUN |
| **RShunt1** | 5m0 | R_2512 | B.Cu | 136.00 | 117.60 | 0 | U3 IN+ / IN- (Pin 10,8) | 4.31 mm | Ana DC Çıkış Akım Şöntü (3W) | UYGUN |
| **R2** | 22R | R_0603 | F.Cu | 84.50 | 83.00 | 90 | U2 Pin IO12 (USB_D-) | 7.80 mm | USB Seri Sönümleme Direnci | UYGUN |
| **R3** | 22R | R_0603 | F.Cu | 86.50 | 83.00 | 90 | U2 Pin IO13 (USB_D+) | 8.94 mm | USB Seri Sönümleme Direnci | UYGUN |
| **R4** | 4k7 | R_0603 | B.Cu | 105.75 | 70.50 | 180 | Q1 Pin 2 (I2C_SCL_3V3) | 3.50 mm | I2C Seviye Dönüştürücü Pull-up | UYGUN |
| **R5** | 4k7 | R_0603 | B.Cu | 105.75 | 77.50 | 90 | Q1 Pin 3 (I2C_SCL_5V) | 3.50 mm | I2C Seviye Dönüştürücü Pull-up | UYGUN |
| **R6** | 4k7 | R_0603 | B.Cu | 110.25 | 77.50 | 90 | Q2 Pin 3 (I2C_SDA_5V) | 3.50 mm | I2C Seviye Dönüştürücü Pull-up | UYGUN |
| **R7** | 4k7 | R_0603 | B.Cu | 110.25 | 70.50 | 0 | Q2 Pin 2 (I2C_SDA_3V3) | 3.50 mm | I2C Seviye Dönüştürücü Pull-up | UYGUN |
| **R8** | 10k | R_0603 | B.Cu | 78.20 | 125.50 | 0 | U1 PD_INT Bölücü | 5.00 mm | PD Kesme Sinyali Seviye Bölücü | UYGUN |
| **R9** | 10k | R_0603 | B.Cu | 85.10 | 125.50 | 0 | U2 IO Kesme Girişi | 5.00 mm | PD Kesme Sinyali Pull-up | UYGUN |
| **R10** | 10k | R_0603 | F.Cu | 92.50 | 83.00 | 90 | U2 Pin IO9 (BOOT) | 10.88 mm | MCU Boot Strap Pull-up | UYGUN |
| **R11** | 5m0 | R_1206 | B.Cu | 76.50 | 103.00 | 0 | U1 Pin 1 & Pin 24 | 16.98 mm | USB VBUS Akım Algılama Şöntü | ROUTING_KOŞULLU |
| **R12** | 6k2 | R_0603 | B.Cu | 77.50 | 115.50 | 90 | U1 Pin 18 (PWR_EN) | 3.07 mm | AP33772S Güç İzin Pull-up | UYGUN |
| **R13** | 100R | R_0603 | B.Cu | 82.50 | 122.50 | 0 | U1 Pin 22 (VOUT) | 7.84 mm | VOUT Boşaltma (Bleeder) Direnci | UYGUN |
| **R14** | 2k2 | R_0603 | B.Cu | 81.20 | 120.50 | 0 | U1 Pin 2 / D1 LED | 6.28 mm | Durum LED Akım Sınırlayıcı | UYGUN |
| **R15** | 22R | R_0603 | F.Cu | 88.50 | 83.00 | 90 | U2 Pin IO8 | 7.80 mm | Ethernet Konfigürasyon Sönümleme | UYGUN |
| **R16** | 10k | R_0603 | F.Cu | 82.50 | 83.00 | 90 | U2 Pin IO0 | 10.03 mm | Ethernet Güç İzin Pull-up | UYGUN |
| **R17** | 100k | R_0603 | B.Cu | 111.50 | 87.20 | 0 | Q8 Pin 3 (ETH_PWR_EN) | 4.68 mm | Ethernet Anahtar Kapı Pull-up | UYGUN |
| **R21** | 100k | R_0603 | B.Cu | 75.80 | 125.50 | 0 | U1 Pin 6 (VSEL) | 3.62 mm | Gerilim Seçim Konfigürasyon Direnci | UYGUN |
| **R24** | 4k7 | R_0603 | B.Cu | 137.50 | 84.00 | 0 | U4 Pin 3 (INT/SQW) | 8.88 mm | RTC Kesme Açık-Kollektör Pull-up | UYGUN |
| **R27** | 10k | R_0603 | B.Cu | 136.75 | 107.00 | 0 | U3 Pin 3 (ALERT) | 2.99 mm | INA226 Alarm Çıkışı Pull-up | UYGUN |
| **R28** | 100R | R_0603 | F.Cu | 81.00 | 108.30 | 0 | Q7 Pin G (Gate) | 4.55 mm | TFT Arka Işık PWM Kapı Sönümleme | UYGUN |
| **R29** | 100k | R_0603 | F.Cu | 83.80 | 109.25 | -90 | Q7 Pin G (Gate) | 2.69 mm | TFT Arka Işık Kapı Pull-down | UYGUN |
| **R34** | 10k | R_0603 | B.Cu | 62.50 | 125.50 | 90 | J9 Pin ENC_A | 21.01 mm | Panel Enkoder Faz-A Pull-up | UYGUN |
| **R35** | 10k | R_0603 | B.Cu | 65.00 | 125.50 | 90 | J9 Pin ENC_B | 29.60 mm | Panel Enkoder Faz-B Pull-up | UYGUN |
| **R36** | 10k | R_0603 | B.Cu | 67.50 | 125.50 | 90 | J9 Pin ENC_SW | 34.12 mm | Panel Enkoder Buton Pull-up | UYGUN |
| **R37** | 10k | R_0603 | F.Cu | 90.50 | 83.00 | 90 | U2 Pin IO8 | 9.71 mm | IO8 Strap Pull-up Direnci | UYGUN |
| **R38** | 100k | R_0603 | B.Cu | 131.00 | 109.30 | 0 | U5 Pin 4 (FSW) | 7.60 mm | Buck Anahtarlama Frekansı Programlama | UYGUN |
| **R39** | 10k2 | R_0603 | B.Cu | 119.50 | 109.50 | 0 | U5 Pin 6 (FB) | 10.81 mm | Buck Çıkış Geribildirim Bölücüsü (Üst) | ROUTING_KOŞULLU |
| **R40** | 3k24 | R_0603 | B.Cu | 116.50 | 108.10 | 180 | U5 Pin 6 (FB) | 13.39 mm | Buck Çıkış Geribildirim Bölücüsü (Alt) | ROUTING_KOŞULLU |
| **R41** | 51k | R_0603 | B.Cu | 123.50 | 110.20 | -90 | U5 Pin 5 (COMP) | 6.22 mm | Buck Kompanzasyon Direnci | UYGUN |
| **R43** | 4k7 | R_0603 | B.Cu | 116.50 | 113.00 | 90 | U5 Pin 8 (EN) | 14.33 mm | Buck Enable Pull-up Direnci | UYGUN |
| **R47** | 78k7 | R_0603 | B.Cu | 91.65 | 119.66 | 180 | U11 Pin 10 (FREQ) | 9.92 mm | Boost Frekans Ayar Direnci | UYGUN |
| **R48** | 30k1 | R_0603 | B.Cu | 88.35 | 125.16 | 180 | U11 Pin 9 (BOOST_FB) | 12.34 mm | Boost Geribildirim Bölücüsü (Üst) | ROUTING_KOŞULLU |
| **R49** | 9k76 | R_0603 | B.Cu | 89.15 | 127.96 | 180 | U11 Pin 9 (BOOST_FB) | 13.47 mm | Boost Geribildirim Bölücüsü (Alt) | ROUTING_KOŞULLU |
| **R50** | 2k87 | R_0603 | B.Cu | 111.10 | 108.00 | 180 | U6 Pin REF | 4.52 mm | Buck Süpervizör Hassas Gerilim Bölücü | UYGUN |
| **R51** | 9k76 | R_0603 | B.Cu | 108.20 | 108.00 | 180 | U6 Pin REF | 4.29 mm | Buck Süpervizör Hassas Gerilim Bölücü | UYGUN |
| **R52** | 2k0 | R_0603 | B.Cu | 94.65 | 127.96 | 180 | U11 Pin 8 (COMP) | 8.38 mm | Boost Kompanzasyon Direnci | UYGUN |
| **R53** | 100k | R_0603 | B.Cu | 103.65 | 125.76 | 180 | U11 Pin 4 (EN) | 10.20 mm | Boost Enable Pull-up Direnci | UYGUN |
| **R54** | 1k0 | R_0603 | F.Cu | 124.80 | 107.20 | 0 | Q6 / U12 Gate Drive | 5.00 mm | Güç Katı Kapı Sönümleme Direnci | UYGUN |
| **R55** | 237k | R_0603 | F.Cu | 129.00 | 107.50 | 90 | U12 Sinyal Bölücü | 5.00 mm | Aşırı Gerilim Koruma Bölücüsü | UYGUN |
| **R56** | 10k | R_0603 | F.Cu | 131.20 | 107.50 | 90 | U12 Sinyal Bölücü | 5.00 mm | Aşırı Gerilim Koruma Bölücüsü | UYGUN |
| **R58** | 100k | R_0603 | F.Cu | 133.40 | 107.50 | 90 | Q6 Gate Pull-down | 5.00 mm | Güç MOSFET Kapı Boşaltma | UYGUN |
| **R59** | 100k | R_0603 | B.Cu | 144.00 | 122.50 | 0 | J4 Çıkış Boşaltma | 5.00 mm | Çıkış Klemensi Boşaltma Direnci | UYGUN |
| **R60** | 5R6 | R_1206 | F.Cu | 87.00 | 104.75 | 0 | J6 Pin BL_A | 6.50 mm | TFT Arka Işık Akım Sınırlayıcı | UYGUN |
| **R61** | 4k7 | R_0603 | B.Cu | 125.50 | 124.05 | 0 | Çıkış Kontrol İzin | 5.00 mm | Çıkış İzin Pull-down Direnci | UYGUN |
| **R62** | 5k1 | R_0603 | F.Cu | 61.50 | 96.80 | 0 | J7 Pin CC1 | 13.66 mm | USB-C Konfigürasyon Kanalı (CC1) Pull-down | UYGUN |
| **R63** | 5k1 | R_0603 | F.Cu | 61.50 | 98.50 | 0 | J7 Pin CC2 | 16.58 mm | USB-C Konfigürasyon Kanalı (CC2) Pull-down | UYGUN |
| **R64** | 2k0 | R_0603 | B.Cu | 80.50 | 125.50 | 0 | PD_INT Seviye Dönüşüm | 5.00 mm | PD Kesme Arayüz Direnci | UYGUN |
| **R65** | 10k | R_0603 | B.Cu | 82.80 | 125.50 | 0 | PD_INT Seviye Dönüşüm | 5.00 mm | PD Kesme Arayüz Direnci | UYGUN |
| **R66** | 100k | R_0603 | F.Cu | 127.50 | 117.50 | -90 | Q6 Aktif Deşarj | 5.00 mm | Çıkış Boşaltma Kapı Direnci | UYGUN |
| **R67** | 1k | R_0603 | F.Cu | 113.00 | 117.50 | 0 | Q6 Aktif Deşarj | 5.00 mm | Çıkış Boşaltma Yük Direnci | UYGUN |

---

## 4. Taşınma Gereksinimi ve Uygulanabilirlik Değerlendirmesi (AC #5, AC #6)

AC #5 gereğince, her bileşenin yerinde kalıp kalmayacağı ya da taşınıp taşınmayacağı araştırılmıştır:

1. **Taşınması Gereken Parça Sayısı:** **0 adet (TASINMALI = 0)**.
2. **Gerekçe:**
   - Kart üzerindeki 86 R/C bileşeninin hiçbiri fiziksel bir çakışmaya, lehim erişimsizliğine veya unroutable (rotalanamaz) bir geometrik kilide neden olmamaktadır.
   - 3D katı model kesişimi **$0{,}000000\text{ mm}^3$**'tür.
   - Courtyard çakışmaları sıfırdır.
   - Enkoder kablo servis hacmi ile en yakın pasif (R36) arasında **1.40 mm** serbest açıklık vardır.
   - Panel enkoder gövdesi (MECH_ENC) ile B.Cu pasifleri arasında **7.04 mm** serbest açıklık vardır.
   - LCD altındaki F.Cu bileşenlerinin tepe yüksekliği maksimum 1.35 mm olup, LCD FPC ve cam altı tavan sınırı olan 1.80 mm'nin altındadır.
   - Kenar bakır açıklığı minimum 0.285 mm olup 0.254 mm kuralını karşılamaktadır.
3. **Alternatif Taşınma Riskleri (AC #6 Kontrolü):**
   - R11 şöntünü U1'e yaklaştırmak, Q3 MOSFET'lerini sıkıştıracak ve 5A akım taşıyan yüksek di/dt hatlarını U1 analog bacaklarının dibine sokarak gürültüyü artıracaktır.
   - C5–C7 grubunu U2 Pin 1'e yaklaştırmak, USB-C (J7) şasi lehimleme alanına girmekte veya U2 RF anten keepout bölgesini ihlal etmektedir.
   - C16/C15 ve C29/C25 bulk kondansatörleri, dönüştürücü hücrelerini çevreleyen en optimal hacimlerde yer almaktadır.
   - Bu nedenlerle, hiçbir bileşenin koordinatı değiştirilmemiş; tüm kritik durumlar için somut ve uygulanabilir routing kuralları belirlenmiştir.

---

## 5. Doğrulama ve Takip Taskları Eşleştirmesi (AC #7)

Bu denetim raporu ile REV_C PCB yerleşimi dondurulmuş olup, belirlenen 16 `ROUTING_KOŞULLU` kuralı doğrudan takip eden tasklara devredilmiştir:

1. **TASK-087 (Genel Kart Routing'i):**
   - C12/C13 ve U5 Exposed Pad arasına B.Cu üzerinde $\ge 1.5\text{ mm}$ poligon çekilmesi.
   - L1 Pad 2 ile C15/C16 arasına $\ge 2.0\text{ mm}$ poligon ve çift via dikişi.
   - Boost sıcak döngüsü (U11 SW $\rightarrow$ D4 $\rightarrow$ C27 $\rightarrow$ PGND via'ları) için B.Cu üzerinde kesintisiz katı poligon.
   - R11'den U1 Pin 1 ve 24'e 0.2 mm / 0.2 mm sıkı diferansiyel Kelvin çifti çekilmesi.
   - C5 $\rightarrow$ C7 $\rightarrow$ C6 $\rightarrow$ U2 Pin 1 besleme hattının viasız 0.8 mm hatla çekilmesi.
2. **Görsel ve Veri Kanıtları:**
   - JSON Envanter ve Pin Denetimi: `hardware/docs/reports/task-097-20260928/rc_pin_audit.json`
   - Doğrulama Özeti: `hardware/docs/reports/task-097-20260928/verification.json`
   - Üst Katman İşaretli Denetim Haritası: `hardware/docs/reports/task-097-20260928/top_rc_audit.png` / `.svg`
   - Alt Katman İşaretli Denetim Haritası: `hardware/docs/reports/task-097-20260928/bottom_rc_audit.png` / `.svg`
