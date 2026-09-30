# TFT J3 Konnektör ve C34 Dekuplaj Grubu İlişkisel Yerleşimi — TASK-082, 24 Eylül 2026

TFT Konnektör grubunun (`TFT CONNECTOR J3`) üyesi `C34` (100nF / 1u0 0402 VDD dekuplaj kapasitörü), sabit mekanik ankraj `J3` (NingBo KLS L-KLS1-242I-2.0-30-R 30 pin 0.5mm FPC konnektörü), Sitronix ST7789V2 denetleyici veri sayfası, Focus LCDs TFT032B018 ekran spesifikasyonu, TASK-064 FPC büküm kararı, TASK-065 LCD yükseklik kuralları ve TASK-069 üretici kılavuzlarına uygun olarak `F.Cu` (Top) katmanında J3'ün güç/toprak pinlerine göre ilişkisel olarak yerleştirildi. J3'ün kilitli ankraj konumu ($x=98{,}000$, $y=109{,}300$, açı $90{,}0^\circ$, `F.Cu`), FPC giriş koridoru, ZIF kapak açıklığı ve şematik netlist bağlantıları bütünüyle korunmuştur.

Bu yerleşim, TASK-067 sonrası kart dışındaki geçici bekleme alanında ($x=28{,}649$, $y=108{,}230$) bulunan C34'ün, sabit ankrajı J3 karta kilitlenmiş olduğu için anakart üzerine taşınması istisnasıdır.

[Önce görünüm](../../hardware/docs/reports/task-082-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-082-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-082-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-082-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-082-20260924/verification.json)

---

## 1. Devre Topolojisi, Dekuplaj İlişkisi ve Pin Eşleşmesi (AC #1)

1. **ST7789V2 Lojik ve Analog Besleme Dekuplajı (C34):**
   - **Eleman Tanımı:** `C34` ($100\text{ nF}$ / $1\mu\text{F}$ 0402 1005Metric seramik kapasitör).
   - **Hedef Konum:** $x = 101{,}000\text{ mm}$, $y = 105{,}550\text{ mm}$, Açı: $90{,}0^\circ$ (`F.Cu`).
   - **Pad 1 ($+3.3\text{V}$ VDD Beslemesi):**
     - Koordinat: $x = 101{,}000\text{ mm}$, $y = 106{,}030\text{ mm}$.
     - J3 Pin 22 ($+3.3\text{V}$) pini $x = 98{,}000\text{ mm}$, $y = 106{,}050\text{ mm}$ koordinatındadır.
     - Dikey sapma: $\Delta Y = |106{,}030 - 106{,}050| = 0{,}020\text{ mm}$ (neredeyse sıfır; mükemmel yatay eksenel hizalama).
     - J3 Pin 21 ($y = 106{,}550$) ve Pin 23 ($y = 105{,}550$) ile birlikte ortak bir $+3.3\text{V}$ güç barası oluşturarak doğrudan, kesintisiz ve düz bir bakır hatla C34 Pad 1'e bağlanır.
     - Merkezler arası doğrudan mesafe: **$3{,}000\text{ mm}$**; bakır kenar-kenar mesafesi: **$1{,}940\text{ mm}$**.
   - **Pad 2 (`GND` Dönüşü):**
     - Koordinat: $x = 101{,}000\text{ mm}$, $y = 105{,}070\text{ mm}$.
     - J3 Pin 25 (`GND`) pini $x = 98{,}000\text{ mm}$, $y = 104{,}550\text{ mm}$ koordinatındadır.
     - C34 Pad 2'den J3 Pin 25'e dikey sapma sadece $0{,}520\text{ mm}$'dir.
     - C34 Pad 2'nin hemen doğusuna ($x \approx 102{,}2\text{ mm}$) yerleştirilecek yerel via ile Katman 2 (`GND_PLANE`) iç düzlemine bağlanır.
     - Dekuplaj döngüsü ($+3.3\text{V} \rightarrow \text{C34} \rightarrow \text{J3} \rightarrow \text{GND}$ düzlemi) minimum döngü alanına ($< 4{,}5\text{ mm}^2$) sahip olup ST7789V2 ekran denetleyicisinin ani akım darbelerinde gerilim dalgalanmasını ve SPI iletişiminde sıçramaları önler.

2. **Sabit Ankraj İstisnası ve Pin 1 Yönü:**
   - J3 FPC konnektörü TASK-064 ve TASK-065 ile belirlenen **$(98{,}000, 109{,}300\text{ mm}, 90{,}0^\circ)$** konumunda ve **Locked (Kilitli)** durumundadır.
   - J3'ün yönü, pin 1 konumu ($y = 116{,}550\text{ mm}$) ve net bağlantıları kesinlikle değiştirilmemiştir.
   - C34'ün kart dışı bekleme alanından alınıp J3'ün yanına yerleştirilmesi, J3'ün anakart üzerinde sabitlenmiş bir mekanik arayüz olmasının zorunlu ve doğal sonucudur.

| Eleman | Değer / Kılıf | Konum (x, y) | Açı | Katman | Netler (Pad 1 / Pad 2) |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `C34` | 100n / 0402 | $(101{,}000, 105{,}550)$ | $90{,}0^\circ$ | `F.Cu` | Pad 1: `+3.3V` / Pad 2: `GND` |
| `J3` (Ankraj) | KLS1-242I 30p | $(98{,}000, 109{,}300)$ | $90{,}0^\circ$ | `F.Cu` | Pin 21-23: `+3.3V`, Pin 25: `GND`, Pin 16-20: SPI |

---

## 2. Mekanik Sınırlar, ZIF Kapağı, FPC Koridoru ve LCD Altı Yükseklik Uyumu (AC #2)

1. **FPC Giriş Alanı ve ZIF Flip-Lock Kapağı Açıklığı:**
   - J3 konnektörünün kablo giriş ağzı batı ($-X$) yönündedir; LCD FPC kablosu batıdan girer ($x \le 98{,}000\text{ mm}$).
   - J3 ZIF flip-lock kapağı gövde üzerinde ($x = 93{,}45\text{--}98{,}00\text{ mm}$) yukarı ve arkaya doğru açılarak FPC'yi kilitler (açık yükseklik $3{,}10\text{ mm}$).
   - C34 kapasitörü sinyal padlerinin doğusunda ($+X$ yönünde, $x = 101{,}000\text{ mm}$) konumlandırılmıştır.
   - C34, FPC giriş koridorundan ve ZIF kapağının hareket ekseninden **$> 3{,}0\text{ mm}$** uzakta olup montaj ve kilitleme işlemlerine hiçbir engel oluşturmaz.

2. **TASK-065 LCD Altı Yükseklik Uyumu:**
   - Ekran modülü LCD arka yüzeyi ile PCB üst yüzeyi (`F.Cu`) arasındaki tavan sınırı **$\le 1{,}80\text{ mm}$**'dir.
   - `C34` 0402 kılıfında olup maksimum parça yüksekliği **$0{,}55\text{ mm}$**'dir.
   - Kalan dikey güvenlik payı: $1{,}80 - 0{,}55 = \mathbf{1{,}25\text{ mm}}$'dir. LCD modülünün oturmasına karşı tam mekanik uyum sağlanmıştır.

3. **Sinyal ve Gürültü Koridorlarının İzolasyonu:**
   - **SPI Koridoru (Pin 16--20, $y = 107{,}05\text{--}109{,}05\text{ mm}$):**
     - `TFT_DC`, `TFT_SCLK`, `TFT_CS`, `TFT_MOSI`, `TFT_RST` yüksek hızlı SPI hatları C34'ün kuzeyinde yer alır.
     - C34'ün en kuzey courtyard kenarı $y = 104{,}615\text{ mm}$'dir; en yakın SPI hattı (Pin 20 `TFT_RST`, $y = 107{,}050\text{ mm}$) ile C34 arasında **$> 0{,}56\text{ mm}$** avlu boşluğu ve **$> 1{,}02\text{ mm}$** pad merkez mesafesi bulunmaktadır.
     - SPI hatları doğuya veya Katman 4 (`B.Cu`) üzerinden MCU'ya doğru engelsiz bir koridorda ilerler.
   - **Backlight Koridoru (Pin 2 `BL_A`, Pin 4 `BL_K`, $y = 115{,}05\text{--}116{,}05\text{ mm}$):**
     - Arka ışık PWM anahtarlama ve akım hatları C34'ten **$> 8{,}5\text{ mm}$** kuzeydedir.
     - Arka ışık PWM anahtarlama gürültüsünün ST7789V2 lojik beslemesine kapasitif veya endüktif kuplajı tamamen engellenmiştir.

---

## 3. TASK-069 Üretici Kuralları ve Ankraj Denetimi (AC #3)

- **Sitronix ST7789V2 Kuralları:** VDD/IOVCC ve VCI besleme pinlerine mümkün olan en kısa mesafede düşük ESR seramik dekuplaj kapasitörü yerleştirilmelidir. $3{,}0\text{ mm}$ pad mesafesi bu kuralı eksiksiz karşılar.
- **KLS1-242I Konnektör Kuralları:** Sinyal lehim padleri üzerinde lehim maskesi köprüsü korunmuş, courtyard çakışması engellenmiştir. C34 ile J3 avluları arasındaki mesafe **$1{,}240\text{ mm}$** olup minimum $0{,}50\text{ mm}$ sınırını fazlasıyla sağlar.
- **Toprak Dönüşü:** C34 Pad 2'nin yerel via ile iç katman toprak düzlemine bağlanması sayesinde dönüş akımları ekran denetleyicisi altında kapalı ve küçük bir döngüde tamamlanır.

---

## 4. Doğrulama ve DRC Sonuçları (AC #4)

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC İhlalleri:** **145 → 145** (yeni courtyard, clearance, short, hole veya silk ihlali: **0**).
  - **Bağlantısız Öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic Parity:** **0 → 0** (şema ile netlist tam uyumlu).
- **Avlu ve Açıklık Kontrolü:**
  - C34 ile J3 arasındaki 2D avlu boşluğu: **$1{,}240\text{ mm}$** ($\ge 0{,}50\text{ mm}$, çakışma: **0**).
- **Sabit Ankrajlar ve İzler:** `J7`, `J3` (kilitli), `J9`, `H1–H4`, `D5`, `U11` konum/açı/yüz ankrajları ve TASK-058 D5.2--U11.9 FB izi UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-082-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-082-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-082-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-082-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-082-20260924/verify.py)
