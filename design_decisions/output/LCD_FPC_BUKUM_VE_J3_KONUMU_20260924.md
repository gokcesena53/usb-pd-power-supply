# LCD FPC Büküm Yolu ve J3 Konum Belirleme Kararı (24 Eylül 2026)

**Görev:** TASK-064 (Milestone m-1)  
**İlgili Görevler:** TASK-062 (Board shape / LCD görünür alanı), TASK-067 (Başlangıç yerleşimi), TASK-065 (Top yükseklik sınırları), TASK-012 (Numune ile konnektör doğrulama)  
**Kaynak Belgeler:**
- LCD: `hardware/datasheets/TFT032B018.pdf` (Xiamen Precise Display Co., Ltd., Rev A, 2023-02-10)
- Konnektör: `hardware/datasheets/KLS1-242I.pdf` (NingBo KLS Electronic Co., Ltd., Rev 2018-03-10)
- Şematik & Layout: `hardware/userinterface.kicad_sch`, `hardware/gopo.kicad_pcb`

---

## 1. Özet ve Alınan Kararlar

1. **J3 Konumu ve Yönü:**
   - **Footprint Referansı:** `J3` (`Connector_FPC_Custom:KLS_L-KLS1-242I-2.0-30_1x30-2MP_P0.50mm_Horizontal`)
   - **PCB Koordinatı:** `(X = 98.00 mm, Y = 109.30 mm)`, Açı: `90°` (saat yönünde). Durum: **Locked (Kilitli)**.
   - **Kablo Giriş Yönü:** Konnektör ağzı sağa (+X) dönük; FPC LCD'nin sağ kenarından çıkıp arkaya kıvrılarak -X yönünde J3 içine girer.
   - **Sinyal Padleri:** X = 98.00 mm hattında, Y = 102.05 mm (Pin 1) ile Y = 116.55 mm (Pin 30) arasında sıralıdır.
   - **Konnektör Giriş Ağzı (Mouth):** X = 102.55 mm hattındadır.
   - **Dahili Stop (Dip Noktası):** X = 100.45 mm hattındadır.

2. **FPC Büküm Geometrisi:**
   - **Büküm Yarıçapı:** \(R \ge 1.0\text{ mm}\) (statik büküm için IPC-2223 standartlarına ve üretici çizimine uygun; nominal \(R \approx 1.2\dots 1.7\text{ mm}\)).
   - **Büküm Çıkıntısı (Loop Apex):** LCD modül sağ kenarından (X = 141.42 mm) 1.00 mm dışarı taşar; döngü tepesi \(X = 142.42\text{ mm}\)'dedir. Kart kenarı X = 149.70 mm ve montaj delikleri X = 145.70 mm olduğundan hiçbir mekanik çakışma yoktur.
   - **Ekleme Derinliği:** KLS1-242I datasheet ekleme derinliği nominal \(2.10\text{ mm}\)'dir. FPC stiffener ucu \(X = 100.42\text{ mm}\)'ye ulaşır, ekleme boyu \(102.55 - 100.42 = 2.13\text{ mm}\) olur. Sapma \(+0.03\text{ mm}\) olup \(\pm 0.3\text{ mm}\) tolerans bandının tam merkezindedir.

3. **Pin 1 Eşleşmesi ve Kontak Yüzü:**
   - LCD FPC Pin 1 büküm sonrasında üst tarafta (düşük Y, Y = 102.05 mm) kalır. J3 Pin 1 de Y = 102.05 mm'dedir.
   - KLS1-242I çift temaslı (double contact) bir konnektördür. FPC'nin altın kontakları büküm sonrası PCB yüzeyine (aşağı) bakar ve J3'ün alt kontaklarına basar; arka yüzdeki 0.3 mm PI takviye ise ZIF kapağına bakar. Pin sıralaması 1:1 netlist eşleşmesine sahiptir (Schematic Parity = 0).

4. **Kapak Açılma Alanı (Clearance):**
   - J3 flip-lock kapağı yukarı ve arkaya (-X yönüne) doğru açılır. Açık yükseklik 3.1 mm'dir.
   - Montaj sırasında LCD karta sabitlenmeden önce FPC J3'e takılır ve kapak kilitlenir; ardından LCD gövdesi modül köpüğü ve ön panel boss vidalarıyla yerine oturtulur. J3 önünde ve üstünde hiçbir engel yoktur.

---

## 2. Datasheet Parametreleri

### 2.1 TFT032B018 LCD Modülü ve FPC Ölçüleri

| Parametre | Değer / Tolerans | Not / Kaynak |
| :--- | :--- | :--- |
| Modül Dış Ölçüleri | 77.70 ± 0.20 × 55.04 ± 0.20 mm | Kalınlık: 2.40 ± 0.15 mm |
| Görünür Alan (AA) | 64.80 × 48.60 mm | 3.2" IPS 240RGB × 320, ST7789V2 |
| AA Merkez Referansı | (X = 100.00, Y = 100.00) mm | PCB ve Kutu Orijini |
| LCD Modül Sınırları | X: [63.72, 141.42] mm, Y: [72.48, 127.52] mm | Yatay (landscape) montaj |
| FPC Çıkış Kenarı | X = 141.42 mm (Sağ kısa kenar) | Modülün 55.04 mm'lik kenarı |
| FPC Çıkış Başlangıcı | Modül alt kenarından 10.47 ± 0.50 mm yukarıda | PCB Y = 117.05 mm |
| FPC Serbest Açık Boyu | 44.67 ± 0.50 mm | Modül kenarından uca kadar |
| FPC Büküm Çıkıntısı | 1.00 mm (nominal) | Büküm döngüsünün dışa taşması |
| Büküm Sonrası Uç Mesafesi | Modül kenarından 41.00 mm içeride | FPC弯折示意图 (x = 100.42 mm) |
| FPC Uç Genişliği | 15.50 ± 0.10 mm | 30 pin, 0.5 mm pitch |
| Kontak Parmak Boyu | 2.50 ± 0.30 mm | Altın kaplama yüzey |
| Takviye (PI Stiffener) Boyu | 5.00 ± 0.30 mm | Uçtan itibaren takviyeli bölge |
| Takviyeli Bölge Kalınlığı | 0.30 ± 0.03 mm (Bantla maks 0.40 mm) | KLS1-242I kablo kalınlık şartı (0.30±0.03 mm) ile uyumlu |
| İletken Genişliği | W = 0.35 mm | 30 pin × 0.5 mm aralık |

### 2.2 KLS L-KLS1-242I-2.0-30-R ZIF Konnektör Ölçüleri

| Parametre | Değer / Tolerans | Not / Kaynak |
| :--- | :--- | :--- |
| Kontak Sayısı | 30 pin | 0.50 mm pitch |
| Montaj Tipi | SMD Yatay (Right angle) | Flip-lock ZIF |
| Kontak Yapısı | Çift Kontak (Double Contact) | Üst ve alt kontak pencereleri |
| Gövde Yüksekliği | 2.00 ± 0.15 mm | Kapalı durum |
| Açık Kapak Yüksekliği | 3.10 mm (nominal) | Flip kilit açıkken |
| Gövde Boyu (X yönü) | 5.30 ± 0.15 mm | Ön girişten arka gövdeye |
| Toplam Derinlik | 5.90 mm | Ön girişten lehim pini ucuna |
| Ekleme Derinliği (Stop) | 2.10 mm | Giriş ağzından dahili dayanağa |
| Kontak Noktası Derinliği | 1.30 mm | Giriş ağzından temas yaylarına |
| Uygun Kablo Kalınlığı | 0.30 ± 0.03 mm | TFT032B018 stiffener kalınlığı ile birebir |

---

## 3. Yan Kesit Büküm Çizimi (Side Cross-Section)

Aşağıdaki yan kesit diyagramı, LCD modülünün ön yüzeyinden çıkan FPC'nin kartın üst (F.Cu) yüzeyindeki J3 konnektörüne büküm yolunu ve Z eksenindeki yığılmayı (stack-up) göstermektedir:

```text
       +-----------------------------------------------------------+ 
       |                  ÖN PANEL / CAM PENCERESİ                 | 
       +-----------------------------------------------------------+ 
                                    || Çift taraflı köpük bant (0.5 mm)
       +=============================================+             |
       |             TFT032B018 LCD MODÜLÜ           |             |
       |             Kalınlık: 2.40 ± 0.15 mm        |             |
       |  (Arka Yüz: Yansıtıcı sac & köpük bant)     |             |
       +---------------------------------------+-----+             |
                                               |     | Basamak     |
                                               | FPC | Çıkışı      |
                      Boşluk (Z ~ 2.0 mm)      +--+--+             |
                                                  |                |
  +--------------------------------+              |   R >= 1.0 mm  |
  |  J3: KLS1-242I-2.0-30          |              |  Büküm döngüsü |
  |  Yükseklik: 2.0 mm             |              |  (Apex: +1.0mm)|
  |                                |              |                |
  |  [Flip Kapağı]                 |              |         +------+
  |      \                         |              |        /
  |       \ Açık: 3.1mm            |              |       |
  |        v                       |              |       |
  |  +----+---------+  Giriş       |              |       |
  |  |Stop| Kontaklar| Ağzı        |   FPC Şeridi |       |
  |  |2.1m| 1.3mm   |<=============+==============+=======+
  |  +----+---------+ (X=102.55)   |  (Kalınlık 0.12 mm)   (X=142.42)
  |  | Sinyal Padi  |              |  Altta Stiffener: 0.3mm
  +--+--------------+--------------+
  ==================================================================
                 PCB TOP YÜZEYİ (F.Cu) - Z = 0.00 mm
  ==================================================================
     ^              ^              ^                      ^
     |              |              |                      |
  X=97.22        X=98.00        X=102.55               X=141.42
  (Lehim        (Signal Pad    (J3 Kablo              (LCD Modül
   Pini)          Merkezi)      Girişi)                Sağ Kenarı)
```

---

## 4. Matematiksel Koordinat ve Tolerans Hesabı

### 4.1 X Ekseni Konum Hesabı
1. **LCD Sağ Kenarı:** \(X_{\text{mod}} = 141.42\text{ mm}\).
2. **Nominal Büküm Dönüşü:** Üretici çiziminde büküm çıkıntısı 1.00 mm verilmiştir (\(X_{\text{apex}} = 142.42\text{ mm}\)).
3. **FPC Büküm Boyu Tüketimi:**
   - 180° büküm yay boyu: \(L_{\text{arc}} \approx \pi \times R \approx 3.14 \times 1.20 \approx 3.77\text{ mm}\).
   - Düz FPC boyu: \(44.67\text{ mm}\).
   - Büküm sonrası kalan serbest uzunluk: \(44.67 - 3.77 + 1.00 \approx 41.90\text{ mm}\) (Üretici nominal 41.00 mm uç mesafesi belirtmiştir).
4. **FPC Uç Noktası (Stiffener Tip):**
   \[
   X_{\text{tip}} = 141.42 - 41.00 = 100.42\text{ mm}
   \]
5. **J3 Konnektör Konumu:**
   - KLS1-242I ekleme derinliği: Dahili stop noktası kablo giriş ağzından 2.10 mm içeridedir.
   - Footprint yapısında sinyal padleri merkezdedir (\(y_f = 0.00\)); gövde giriş ağzı \(y_f = -4.55\text{ mm}\)'dedir.
   - 90° dönüş uygulandığında: Giriş ağzı \(X_{\text{mouth}} = X_0 + 4.55\text{ mm}\), dahili stop \(X_{\text{stop}} = X_0 + (4.55 - 2.10) = X_0 + 2.45\text{ mm}\).
   - FPC ucunun stop noktasına tam oturması şartı: \(X_0 + 2.45 = 100.42 \implies X_0 = 97.97\text{ mm}\).
   - Temiz ızgara (grid) yerleşimi için **\(X_0 = 98.00\text{ mm}\)** seçilmiştir.
   - Bu durumda:
     \[
     X_{\text{mouth}} = 98.00 + 4.55 = 102.55\text{ mm}
     \]
     \[
     X_{\text{stop}} = 98.00 + 2.45 = 100.45\text{ mm}
     \]
     \[
     \text{Ekleme Boyu} = X_{\text{mouth}} - X_{\text{tip}} = 102.55 - 100.42 = 2.13\text{ mm}
     \]
     Datasheet nominal değeri: \(2.10\text{ mm}\). Fark: \(+0.03\text{ mm}\) (\(\pm 0.3\text{ mm}\) kriteri fazlasıyla sağlanır).

### 4.2 Y Ekseni Konum Hesabı
1. **LCD Modül Alt Kenarı:** \(Y_{\text{mod\_bot}} = 127.52\text{ mm}\).
2. **FPC Çıkış Ofseti:** Datasheet ön görünüşünde FPC dış kenarı modül kenarından \(10.47 \pm 0.50\text{ mm}\) içeridedir.
   \[
   Y_{\text{fpc\_outer}} = 127.52 - 10.47 = 117.05\text{ mm}
   \]
3. **FPC Uç Genişliği:** \(15.50\text{ mm}\).
   \[
   Y_{\text{fpc\_inner}} = 117.05 - 15.50 = 101.55\text{ mm}
   \]
4. **FPC Kontak Merkez Hattı:**
   - 30 pin, 0.50 mm aralık ile \(29 \times 0.50 = 14.50\text{ mm}\) hat genişliği.
   - Her iki yanda \(0.50\text{ mm}\) simetrik kenar payı vardır.
   - Kontakların orta ekseni:
     \[
     Y_{\text{center}} = \frac{117.05 + 101.55}{2} = 109.30\text{ mm}
     \]
5. **J3 Y Konumu:** Footprint merkezinde signal padleri simetriktir (\(x_f = 0\)).
   - 90° dönüşte \(Y_{\text{center}} = Y_0\).
   - Dolayısıyla **\(Y_0 = 109.30\text{ mm}\)**.

---

## 5. Pin Eşleşme ve Netlist Doğrulaması

J3 konnektörü `hardware/userinterface.kicad_sch` şemasına ve ST7789V2 4 telli SPI arayüzüne bağlıdır:

| J3 Pin | Şematik Net Adı | LCD FPC Fonksiyonu | Eşleşme Durumu |
| :---: | :--- | :--- | :---: |
| 1 | `NC` | NC | Doğru |
| 2 | `/USER INTERFACE/BL_A` | BL_A (LED Anot) | Doğru |
| 3 | `NC` | NC | Doğru |
| 4 | `/USER INTERFACE/BL_K` | BL_K (LED Katot, Q7 anahtarlı) | Doğru |
| 5 | `GND` | GND | Doğru |
| 6 | `NC` | TE (Tearing Effect, kullanılmıyor) | Doğru |
| 7..14 | `GND` | DB7..DB0 (SPI modunda GND) | Doğru |
| 15 | `GND` | RDX (SPI modunda GND) | Doğru |
| 16 | `TFT_DC` | WRX/spi_rs (Data/Command) | Doğru |
| 17 | `TFT_SCLK` | DCX/spi_scl (SPI Clock) | Doğru |
| 18 | `TFT_CS` | CSX/spi_cs (Chip Select) | Doğru |
| 19 | `TFT_MOSI` | spi_sda (MOSI Data) | Doğru |
| 20 | `TFT_RST` | RESX (Reset) | Doğru |
| 21 | `+3.3V` | IM1/IM2 (High = 4-wire SPI) | Doğru |
| 22 | `+3.3V` | IOVCC (1.8V / 2.8V / 3.3V lojik) | Doğru |
| 23 | `+3.3V` | VCI (Analog besleme 2.8V / 3.3V) | Doğru |
| 24 | `NC` | TP_VCI (Dokunmatik, kullanılmıyor) | Doğru |
| 25 | `GND` | GND | Doğru |
| 26..29| `NC` | TP_INT, TP_SDA, TP_SCL, TP_RESET | Doğru |
| 30 | `GND` | GND | Doğru |

Schematic Parity testi: **0 hata**.

---

## 6. TASK-012 Numune Doğrulama Girdileri

Bu karardaki teorik hesaplamaların fiziksel prototip üzerinde doğrulanması için `TASK-012` görevine aşağıdaki kontrol maddeleri bağlanmıştır:

1. **Pin 1 ve Polarite Doğrulaması:**
   - Numune LCD'nin FPC'si arkaya büküldüğünde Pin 1'in kartın üst kenarına (düşük Y) denk geldiği bir multimetre/ommetre ile buzzer modunda doğrulanmalı (J3 Pin 2 BL_A ile LCD LED anodunun eşleştiği teyit edilmeli).
2. **FPC Büküm Boyu ve Dayanak Kontrolü:**
   - FPC J3 içine sokulduğunda serbest büküm kavisinin modül kenarından 1.0 mm civarında taştığı, konnektör stop noktasına zorlanmadan oturduğu ve gerilme olmadığı görülmeli.
3. **ZIF Kilit Mekanizması ve Takviye Kalınlığı:**
   - KLS1-242I kapağının FPC takıldıktan sonra rahatça kapanıp kilitlendiği, 0.3 mm'lik stiffener kalınlığının konnektör yaylarını tam kavradığı test edilmeli.
4. **Z Ekseni Boşluğu:**
   - J3 kapalı gövde yüksekliğinin (2.0 mm), LCD arka yüzü ile kart arasındaki köpük/montaj boşluğuna sığdığı ve LCD'nin karta mekanik baskı yapmadığı doğrulanmalı.

## TASK-065 Z toleransı eki (24.09.2026)

Yukarıdaki 2,00 mm nominal J3 yüksekliği, toleranslı LCD mesafe parçası
ölçüsü olarak doğrudan kullanılmaz: J3 kapalı 2,00±0,15 mm, maks.2,15 mm.
TASK-065 LCD arka yüz–PCB top hedefini 2,35±0,15 mm (min.2,20 mm), J3
harici top zarf bütçesini 1,80 mm olarak ayırdı. Kutu/numune doğrulamasında
FPC kıvrımı ve gerilimsiz takılma bu gerçek Z boşluğunda kontrol edilir.
J3 XY konumu, yönü, pin eşleşmesi ve kilidi değişmedi. Ayrıntı:
[TASK-065 kararı](LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md).
