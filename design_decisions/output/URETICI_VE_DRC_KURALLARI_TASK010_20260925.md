# Üretici Kuralları, Stackup, USB Empedansı ve Özel DRC Doğrulaması — TASK-010, 25 Eylül 2026

`hardware/gopo.kicad_dru`, `hardware/gopo.kicad_pcb` ve `hardware/gopo.kicad_pro` dosyaları üretici kabiliyetleri (JLCPCB 4-katman standart prosesi), katman stackup geometrisi (`JLC04161H-7628`), USB 2.0 diferansiyel empedans hesabı ($90\ \Omega$) ve güncel bileşen referansları (`J7`, `U11`, `U1/U7/U8/U11/U12`, `J8`) doğrultusunda güncellendi ve kontrollü deneylerle kanıtlandı.

## 1. Üretici ve Katman Stackup Seçimi (JLCPCB JLC04161H-7628)

Üretici olarak prototip ve seri üretim için **JLCPCB 4-Katman Standart Prosesi** (`JLC04161H-7628`) seçilmiştir.

| Katman | Katman Adı / Tipi | Kalınlık | Malzeme / Bakır | Dielektrik Sabiti ($\varepsilon_r$) | Fonksiyonu ve Referans Düzlemi |
| --- | --- | --- | --- | --- | --- |
| 1 | `F.SilkS` / `F.Mask` | $0{,}010\text{ mm}$ | Solder Mask (Yeşil/Siyah) | $3{,}8$ | Yüzey maskeleme ve koruma |
| 2 | **`F.Cu` (Top)** | **$0{,}035\text{ mm}$ (1 oz)** | Bakır Folyo | — | USB D+/D-, ESP32 RF/Anten, J7, MCU sinyalleri, LCD backlight/J3 |
| 3 | **Dielectric 1 (Prepreg)** | **$0{,}2104\text{ mm}$** | **7628 Prepreg** | **$4{,}6$** | L1 mikroşerit referans aralığı ($H = 0{,}2104\text{ mm}$) |
| 4 | **`In1.Cu` (Inner 1)** | **$0{,}0175\text{ mm}$ (0.5 oz)** | Bakır | — | **Kesintisiz `GND_PLANE`** (Tüm L1 izlerinin dönüş düzlemi) |
| 5 | **Dielectric 2 (Core)** | **$1{,}065\text{ mm}$** | **FR4 Core** | **$4{,}6$** | İç çekirdek mekanik taşıyıcı |
| 6 | **`In2.Cu` (Inner 2)** | **$0{,}0175\text{ mm}$ (0.5 oz)** | Bakır | — | **`POWER_PLANE` / Bölünmüş Güç ve İkincil GND Düzlemi** (`VBUS`, `V_PRE`, `+3.3V`, `ETH_3V3`) |
| 7 | **Dielectric 3 (Prepreg)** | **$0{,}2104\text{ mm}$** | **7628 Prepreg** | **$4{,}6$** | L4 referans aralığı ($H = 0{,}2104\text{ mm}$) |
| 8 | **`B.Cu` (Bottom)** | **$0{,}035\text{ mm}$ (1 oz)** | Bakır Folyo | — | Güç anahtarlama blokları (TPS55340, AOZ1284, LM74801, J8 Ethernet) |
| 9 | `B.Mask` / `B.SilkS` | $0{,}010\text{ mm}$ | Solder Mask | $3{,}8$ | Yüzey maskeleme |
| — | **Toplam Kart Kalınlığı** | **$1{,}5908\text{ mm} \approx 1{,}60\text{ mm}$** | ENIG Yüzey Kaplama | — | Nominal $1{,}6\text{ mm}$ hedefiyle tam uyumlu |

### Üretim Limitleri (JLCPCB 4-Layer)
- Asgari İz Genişliği / Boşluğu: $0{,}127\text{ mm}$ ($5\text{ mil}$) (Tasarımımızda asgari $0{,}15\text{ mm}$ uygulanmıştır)
- Asgari Via Matkap / Ped Çapı: $0{,}20\text{ mm} / 0{,}45\text{ mm}$ (Standart via $0{,}30\text{ mm} / 0{,}60\text{ mm}$)
- Asgari THT Komponent Deliği: $0{,}30\text{ mm}$
- Asgari Bakır-Kenar Mesafesi: $0{,}30\text{ mm}$ (Global kural $0{,}50\text{ mm}$, J7 için $0{,}25\text{ mm}$)
- Lehim Maskesi Köprüsü: Min $0{,}10\text{ mm}$ ($4\text{ mil}$)

---

## 2. USB 2.0 Diferansiyel Empedans Hesabı ($90\ \Omega \pm 10\%$)

JLC7628 katman diziliminde L1 (`F.Cu`) üzerindeki USB 2.0 sinyalleri (`USB_DP`, `USB_DM`), doğrudan altındaki L2 (`In1.Cu` GND_PLANE) referans alınarak IPC-2141 kenar-kuplajlı mikroşerit modeliyle hesaplanmıştır:

- Referans yüksekliği ($H$): $0{,}2104\text{ mm}$
- Dielektrik sabiti ($\varepsilon_r$): $4{,}6$
- Bakır kalınlığı ($T$): $0{,}035\text{ mm}$ ($1\text{ oz}$)
- **İz Genişliği ($W$): $0{,}25\text{ mm}$ ($9{,}84\text{ mil}$)**
- **Diferansiyel Aralık ($S$): $0{,}20\text{ mm}$ ($7{,}87\text{ mil}$)**

### Hesaplama Sonuçları:
- Tek Uçlu Empedans ($Z_0$): **$55{,}1\ \Omega$**
- **Diferansiyel Empedans ($Z_{\text{diff}}$): $89{,}0\ \Omega$** ($90\ \Omega \pm 10\%$ hedef toleransı: $[81{,}0\ \Omega, 99{,}0\ \Omega]$ aralığında, hata $<\%1{,}2$)

`hardware/gopo.kicad_pro` içine `USB_DIFF_90` netclass'ı eklenmiş; `USB_DP` ve `USB_DM` ağları bu sınıfa bağlanmıştır.

---

## 3. Alt Katman (B.Cu) Güç ve Sinyal Referans Dönüş Planı

1. **Yüksek $di/dt$ Anahtarlama Döngüleri (Boost U11 & Buck U5):**
   - TPS55340 boost döngüsü (`U11` $\rightarrow$ `L3` $\rightarrow$ `D4` $\rightarrow$ `C27`/`C28`) ve AOZ1284 buck döngüsü (`C13`/`C14` $\rightarrow$ `U5` $\rightarrow$ `D2` $\rightarrow$ `L1`), tamamen B.Cu yüzeyinde lokal seramik kapasitörlerle kapatılmıştır.
   - Anahtarlama akımları iç katmanlara geçmez; EMI yayılımı engellenmiştir.
2. **B.Cu Sinyal Hatları Dönüş Yolu:**
   - B.Cu üzerinde ilerleyen sinyal hatları (Ethernet UART, I2C, OUT_EN vb.), hemen bitişiğindeki L3 (`In2.Cu` POWER/GND) poligonunu referans alır.
   - Güç düzlemi yarıkları üzerinden geçen hatların yakınına L2 GND ile L3 GND'yi bağlayan dikiş (stitching) viaları eklenerek geri dönüş endüktansı asgari seviyede tutulur.

---

## 4. Özel DRC Kurallarının (`gopo.kicad_dru`) Güncellenmesi ve Denetimi

Eski `.dru` dosyasındaki geçersiz ve eski referanslar (`U9`, `J1`) ayıklanmış, güncel devre referanslarıyla revize edilmiştir:

```lisp
(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U1' || A.Reference == 'U7' || A.Reference == 'U8' || A.Reference == 'U11' || A.Reference == 'U12'")
	(constraint clearance (min 0.15mm))
)

(rule "USB-C J7 copper to edge"
	(condition "A.Reference == 'J7'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "USB-C J7 NPTH to pad hole clearance"
	(condition "A.Reference == 'J7' && B.Reference == 'J7'")
	(constraint hole_clearance (min 0.18mm))
)

(rule "U11 Thermal Via hole size"
	(condition "A.Reference == 'U11'")
	(constraint hole (min 0.20mm))
)

(rule "Mezzanine courtyard exception for proven components"
	(condition "(A.Reference == 'J8' && B.Reference == 'TP14') || (B.Reference == 'J8' && A.Reference == 'TP14')")
	(constraint courtyard_clearance (min -100mm))
)
```

### Kural Gerekçeleri ve Denetim Sonuçları:
1. **`U9` $\rightarrow$ `U1|U7|U8|U11|U12`:** Eski TPD4E05U06 ESD entegresi (`U9`) şemadan kaldırılmıştı. Yerine gerçek ince adımlı ($0{,}50\text{--}0{,}65\text{ mm}$ pitch) QFN-24 (`U1`), VSSOP-10 (`U7`), WSON-10 (`U8`), HTSSOP-14 (`U11`) ve VSSOP-8 (`U12`) kılıfları tanımlandı.
2. **`J1` $\rightarrow$ `J7` (Bakır-Kenar):** Eski mid-mount J1 yerine güncel TYPE-C-31-M-12 konnektörü `J7` tanımlandı. Kart kenarı kesimine $0{,}25\text{ mm}$ izin verildi (global kural $0{,}50\text{ mm}$).
3. **`J7` NPTH Delik Boşluğu ($0{,}18\text{ mm}$):** J7'nin üretici kılıfındaki plastik kılavuz pimleri (NPTH) ile A1/B12 ve A12/B1 GND pedleri arasındaki mesafe $0{,}1944\text{ mm}$'dir. Global $0{,}25\text{ mm}$ kuralı nedeniyle oluşan 4 adet sahte `hole_clearance` hatası bu kural ile üretici geometrisine uygun şekilde çözüldü.
4. **`U11` Termal Via Delik Çapı ($0{,}20\text{ mm}$):** Texas Instruments HTSSOP-14-1EP kılıfı, lehimin aşağı akmasını önlemek için $0{,}20\text{ mm}$ matkap çaplı 15 adet termal via içerir. Global THT asgari delik kuralı ($0{,}30\text{ mm}$) bozulmadan, U11 termal vias'ı JLCPCB 4-katman çoklu via kabiliyetiyle ($0{,}20\text{ mm}$) onaylandı; 15 adet `drill_out_of_range` hatası çözüldü.
5. **`J8` Mezzanine Courtyard İstisnası:** Sınırsız bir joker kullanılmamış; sadece 3D analizi yapılmış ve Bölge 2 içinde yer alabilecek test noktası (`TP14`) çiftiyle sınırlandırılmıştır. Bölge 3 (RJ45 lehim bacakları) mutlak keepout olarak korunmaktadır.

---

## 5. Kontrollü DRC Karşılaştırma Matrisi

`hardware/docs/reports/task-010-20260925/verify_rules.py` test scripti ile 4 farklı kural konfigürasyonunda DRC çalıştırılmış ve sonuçlar `rule_verification_summary.json` dosyasına kaydedilmiştir:

| Senaryo | Toplam İhlal | `drill_out_of_range` (U11) | `hole_clearance` (J7) | `text_height` / `thickness` (Uyarı) | Açıklama |
| --- | --- | --- | --- | --- | --- |
| **Eski Kurallar (Baseline)** | **145** | 15 (HATA) | 4 (HATA) | 126 (Uyarı) | U11 ve J7 hataları aktif |
| **U11 Kuralı Olmadan** | **141** | 15 (HATA) | 0 | 126 (Uyarı) | U11 kuralının gerekliliği kanıtlandı |
| **J7 Kuralı Olmadan** | **130** | 0 | 4 (HATA) | 126 (Uyarı) | J7 kuralının gerekliliği kanıtlandı |
| **Yeni Kurallar (TASK-010)** | **126** | **0 (ÇÖZÜLDÜ)** | **0 (ÇÖZÜLDÜ)** | **126 (Uyarı)** | **Tüm DRC Hataları SIFIRLANDI** |

- **Şematik Parite:** 0 parite hatası, 0 ERC hatası.
- **Bağlantısız Hat:** 360 (fiziksel routing öncesi beklenen başlangıç seviyesi).
