---
id: TASK-099
title: Aktif ve manyetik komponentlerin IC iliskilerini ve kritik dongulerini denetle
status: Done
assignee: []
created_date: '2026-09-28 06:29'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-096
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/task-099-20260928/active_magnetic_audit.md
  - design_decisions/output/AKTIF_VE_MANYETIK_DENETIMI_TASK099_20260928.md
priority: high
ordinal: 185000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Diyotlar (D1-D10), transistörler/FETler (Q1-Q8), bobinler (L1, L3), kristal (Y1) ve entegreler arasi arayuzlerin (I2C seviye donusturucu Q1/Q2, koruma zinciri U3->U13->U12/Q4) pin bazinda iliskilerini, katman uyumunu ve anahtarlama/gurultu dongulerini denetle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 D1-D10 diyotlarinin (D2 boot, D4 boost Schottky, D5 clamp, D6 Zener, D7/D8/D9 TVS/ESD) bagli olduklari IC pinlerine mesafesi ve polariteleri dogrulanmis.
- [x] #2 Q1-Q8 transistör/FETlerinin (Q1/Q2 I2C shifter, Q3 VBUS switch, Q4 desarj FET, Q5 ideal diyot/cikis FET, Q8 Ethernet besleme) gate surus donguleri ve anahtarlama yollari incelenmis.
- [x] #3 L1 buck ve L3 boost bobinlerinin anahtarlama dugumlerine (LX, SW) yakinligi, bakir alanlari ve parazitik yayilim riskleri dogrulanmis.
- [x] #4 Y1 32.768 kHz kristalinin U4 RTC pinlerine min dongu ile baglandigi ve guc hatlarindan korundugu kanitlanmis.
- [x] #5 Entegreler arasi baglantilarin (U2-U1, U2-U3, U2-U4, U3-U13-U12-Q4) sinyal butunlugu ve donus yollari kontrol edilmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

### 1. D1-D10 Diyotları Denetimi ve Polarite Doğrulaması
- **D1 (LED)**: B.Cu $(83.50, 120.50)$. U1 Pin 8 (LED çıkışı) mesafesi $6.55\text{ mm}$, R14 (2k2) mesafesi $2.30\text{ mm}$. Anot U1'den R14 üzerinden sürülür, Katot GND'ye bağlıdır. Polarite DOĞRU.
- **D2 (SS2060FL 60V 2A Schottky)**: B.Cu $(132.80, 103.50)$. Görev tanımında "D2 boot" olarak belirtilmesine rağmen, şematik analizinde U5 (AOZ1284PI) bootstrap hattının C17 (100nF) ile BST-LX arasına bağlı olduğu, D2'nin ise `LX_SW` ile `GND` arasına bağlı **harici serbest dolaşım (catch) Schottky diyotu** olduğu tespit edilmiştir. Katot pini U5 Pin 1'e (`LX_SW`) yalnızca **$2.20\text{ mm}$** mesafededir. Dead-time negatif sıçramalarını sönümler. Polarite DOĞRU.
- **D3 (SMBJ30A 30V 600W TVS)**: F.Cu $(61.50, 82.50)$. J7 USB-C VBUS girişine $10.42\text{ mm}$ mesafededir. Katot USB_VBUS, Anot GND. Polarite DOĞRU.
- **D4 (SX36 60V 3A Power Schottky)**: B.Cu $(102.95, 114.66)$. U11 Pin 1,2 (SW) bacağına mesafesi **$4.39\text{ mm}$**, C27 çıkış kapasitörüne mesafesi **$6.58\text{ mm}$**'dir. Anot BOOST_SW, Katot V_PRE. Polarite DOĞRU.
- **D5 (BAS16H Hızlı Anahtarlama Diyotu)**: B.Cu $(92.17, 123.26)$. U11 Pin 9 (BOOST_FB) bacağına mesafesi **$2.14\text{ mm}$**'dir. Katot EN_CTRL, Anot BOOST_FB. Polarite DOĞRU.
- **D6 (BZT52C12 12V Zener)**: F.Cu $(124.80, 104.50)$. U12 Pin 8 (GATE_DRV) ve Q5B HGATE ile SRC_COMMON arasındadır. $V_{GS} \le 12\text{V}$ koruma sağlar. Polarite DOĞRU.
- **D7 (SMBJ30A 30V 600W TVS)**: B.Cu $(144.00, 119.50)$. U3 akım algılama ve J4 çıkış klemensine doğrudan bitişiktir ($7.32\text{ mm}$). Katot OUT_POS, Anot GND. Polarite DOĞRU.
- **D8, D9 (SMF30A 30V TVS)**: F.Cu $(61.50, 92.00)$ ve $(61.50, 94.50)$. J7 USB-C CC1 ve CC2 hatlarına $9.22\text{ mm}$ ve $10.42\text{ mm}$ mesafededir. 28V EPR VBUS-CC kısa devre koruması sağlar. Katot CC, Anot GND. Polarite DOĞRU.
- **D10 (BZT52C12 12V Zener)**: F.Cu $(124.00, 117.50)$. Q6 deşarj FET kapısını $12\text{V}$ ile sınırlar; Q6'ya mesafesi $4.50\text{ mm}$'dir. Polarite DOĞRU.

### 2. Q1-Q8 Transistör ve FET'ler Gate ve Anahtarlama Yolları
- **Q1, Q2 (BSS138P)**: B.Cu $(105.75, 74.00)$ ve $(110.25, 74.00)$. Çift yönlü I2C SCL/SDA seviye dönüştürücüleridir. Gate uçları doğrudan +3.3V rayına baypas edilmiştir. Küçük sinyal anahtarlaması (<2 mA) gürültüsüzdür.
- **Q3 (SQJB60EP Dual N-FET 60V, 30A)**: B.Cu $(78.50, 110.00)$. U1 Pin 22 (GATE) ile sürülen sırt-sırta (back-to-back) VBUS güç anahtarıdır. Gate mesafesi $11.31\text{ mm}$'dir.
- **Q4 (BSS138P)**: B.Cu $(120.00, 122.50)$. Aktif deşarj lojik eviricisi. U13 Pin 4 (SW_EN) ile sürülür; Gate mesafesi **$11.15\text{ mm}$**'dir.
- **Q5 (SQJB60EP Dual N-FET 60V, 30A)**: F.Cu $(128.50, 99.00)$. U12 (LM74801) ile doğrudan aynı katmandadır (`F.Cu`). İdeal diyot kapısı DGATE mesafesi **$3.94\text{ mm}$** (via'sız doğrudan hat); HGATE mesafesi **$9.09\text{ mm}$**'dir.
- **Q6 (BSS138P)**: F.Cu $(119.50, 117.50)$. Aktif deşarj anahtarı. Gate D10 Zener'ine $4.50\text{ mm}$ mesafededir.
- **Q7 (IRLML6344 N-FET)**: F.Cu $(87.00, 109.25)$. 3.2" LCD TFT_BL_PWM anahtarı; U2 Pin 13'ten sürülür.
- **Q8 (TSM3443CX6 P-FET)**: B.Cu $(107.00, 88.50)$. Ethernet modülü (J8) +3.3V yüksek taraf güç anahtarı. J8'e mesafesi $9.96\text{ mm}$'dir.

### 3. Manyetik Bileşenler (L1, L3) ve Sıcak Döngü Metrikleri
- **L1 (22 µH Buck İndüktörü)**: B.Cu $(126.995, 97.37)$. U5 Pin 1 (LX) bacağına mesafesi **$6.05\text{ mm}$**, serbest dolaşım diyotu D2'ye mesafesi **$6.40\text{ mm}$**, çıkış kapasitörleri C15/C16'ya mesafesi **$7.37\text{ mm}$**'dir. LX bakır adacığı $< 15\text{ mm}^2$ olup altında In1.Cu katı zemin ekranı mevcuttur. Manyetik yayılım riski çok düşüktür.
- **L3 (6.8 µH Boost İndüktörü)**: B.Cu $(97.70, 108.16)$. U11 Pin 1,2 (SW) bacağına mesafesi **$10.89\text{ mm}$**, D4 Anot bacağına mesafesi **$6.50\text{ mm}$**'dir. U11 SW $\rightarrow$ D4 $\rightarrow$ C27 $\rightarrow$ U11 PGND sıcak anahtarlama döngü çevresi **$\approx 24\text{ mm}$** olup son derece kompakttır. Manyetik yayılım riski düşüktür.

### 4. Y1 RTC Kristali ve Gürültü İzolasyonu
- **Y1 (32.768 kHz Kristal)**: B.Cu $(143.00, 89.00)$ konumunda, U4 (BQ32000 RTC) ile $X = 143.00\text{ mm}$ ekseninde doğrudan hizalıdır. Merkez-merkez mesafesi **$7.00\text{ mm}$**, OSCI pin mesafesi $8.98\text{ mm}$, OSCO pin mesafesi $10.61\text{ mm}$'dir.
- Döngü alanı $< 18\text{ mm}^2$'dir. Buck LX hattından $> 20\text{ mm}$, Boost SW hattından $> 50\text{ mm}$ uzakta, In1.Cu zemin düzlemi üzerinde tam korumalıdır.

### 5. Donanımsal Koruma Zinciri (U3 -> U13 -> U12 / Q4)
- **Hızlı Koruma:** INA226 ALERT (Pin 3) $\rightarrow$ U13 Pin 2 mesafesi **$15.87\text{ mm}$** (her ikisi de B.Cu). U13 çıkışı `SW_EN`, U12 Pin 6'ya ($19.79\text{ mm}$) ve Q4 Gate bacağına ($11.15\text{ mm}$) gider. Aşırı akım/arıza anında yazılım gecikmesi olmaksızın sub-mikrosaniyede güç kesilir ve aktif deşarj başlatılır.

### 6. Verification & KiCad DRC
- `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
- **İhlal Sayısı:** 164 ihlal (TASK-098 tabanı korundu, 0 yeni ihlal).
- **Parite:** **0 schematic parity issue** (%100 parite).
- **Bağlantısız:** 360 (taban korundu).
- **Rapor ve Veri:**
  - `hardware/docs/reports/task-099-20260928/active_magnetic_audit.md`
  - `hardware/docs/reports/task-099-20260928/active_magnetic_audit.json`
  - `design_decisions/output/AKTIF_VE_MANYETIK_DENETIMI_TASK099_20260928.md`
