# TFT Backlight (3.3V + PWM) Grubu İlişkisel Yerleşimi — TASK-081, 24 Eylül 2026

TFT Backlight grubunun (`TFT BACKLIGHT (3.3V + PWM)`) 4 footprint üyesi (`Q7`, `R28`, `R29`, `R60`), Infineon IRLML6344TRPBF N-kanal MOSFET veri sayfası, Focus LCDs TFT032B018 ekran spesifikasyonu, `BACKLIGHT_TASARIMI_20260911.md`, TASK-065 LCD yükseklik kuralları ve TASK-069 üretici kılavuzlarına uygun olarak `F.Cu` (Top) katmanında ilişkisel olarak yerleştirildi. Dört footprint'in grup üyeliği, UUID, pad/net bağlantıları ve `F.Cu` yüz ataması korunmuştur. Kart dışındaki geçici blok alanı ($x\approx 15\text{--}24\text{ mm}$, $y\approx 94\text{--}100\text{ mm}$) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-081-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-081-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-081-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-081-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-081-20260924/verification.json)

---

## 1. Devre Topolojisi, Akım Döngüleri ve Pin İlişkileri (AC #1)

1. **Düşük Taraf (Low-Side) PWM Anahtarlama Hücresi:**
   - **Q7 (`IRLML6344TRPBF`, N-MOSFET, SOT-23, rot $0^\circ$, $x=22{,}000$, $y=99{,}000$):**
     - *Kapı (Gate, Pin 1):* Batıya yönlendirilerek ($x=21{,}062$, $y=98{,}050$) gate sürüş ağına bağlanır.
     - *Kaynak (Source, Pin 2):* Batıya yönlendirilerek ($x=21{,}062$, $y=99{,}950$) doğrudan yerel GND düzlemine bağlanır.
     - *Savak (Drain, Pin 3):* Doğuya yönlendirilerek ($x=22{,}938$, $y=99{,}000$) ekran konnektörünün katot dönüş hattına (`/USER INTERFACE/BL_K`) doğrudan bağlanır.
   - **R28 ($100\Omega$ 0402) PWM Seri Sönümleme Direnci:**
     - ESP32-C6 GPIO7 (LEDC PWM) hattı ile Q7 Kapısı arasına seri yerleştirilmiştir ($x=16{,}000$, $y=98{,}050$, rot $0^\circ$).
     - Pad 1 (`TFT_BL_PWM`) batıdan gelen MCU hattını karşılar; Pad 2 (`Net-(Q7-G)`) doğuya, R29 ve Q7 Kapısına doğru kesişimsiz akar ($R28.2 \leftrightarrow Q7.1 = 4{,}552\text{ mm}$ doğrudan eksenel hat).
     - Hızlı PWM anahtarlama kenarlarındaki (ringing/EMI) parazitik osilasyonları bastırır.
   - **R29 ($100\text{ k}\Omega$ 0402) Kapı Pull-Down Direnci:**
     - Q7 Kapısı ile Kaynağı (GND) arasına dikey bir köprü olarak yerleştirilmiştir ($x=18{,}800$, $y=99{,}000$, rot $270^\circ$).
     - Pad 1 (`Net-(Q7-G)`) kuzeyde $y=98{,}490$ hizasında Q7 Kapısı ve R28.2 ile buluşur ($R29.1 \leftrightarrow Q7.1 = 2{,}305\text{ mm}$).
     - Pad 2 (`GND`) güneyde $y=99{,}510$ hizasında Q7 Kaynağı ile buluşur ($R29.2 \leftrightarrow Q7.2 = 2{,}305\text{ mm}$).
     - ESP32-C6 boot ve reset aşamasında GPIO7 yüksek empedanstayken Q7'nin kapısını kesin olarak toprağa çekerek arka ışığın parlamasını ve kontrolsüz açılmasını engeller.

2. **Anot Akım Sınırlama ve LED Beslemesi:**
   - **R60 ($5{,}6\Omega$ 0805, $x=22{,}000$, $y=94{,}500$, rot $0^\circ$):**
     - Pad 1 ($+3.3\text{V}$): Batıya yönlendirilerek ana 3.3V güç rayını alır ($x=21{,}087$, $y=94{,}500$).
     - Pad 2 (`/USER INTERFACE/BL_A`): Doğuya yönlendirilerek ($x=22{,}913$, $y=94{,}500$) J3 FPC konnektörünün Pin 2 anot girişine doğru akar.
   - **Doğrusal ve Paralel Çıkış Arayüzü:**
     - R60 Pad 2 (`BL_A`, $y=94{,}500$) ve Q7 Pad 3 (`BL_K`, $y=99{,}000$) aynı $x\approx 22{,}9\text{ mm}$ ekseninde doğuya, J3 FPC konnektörüne bakar.
     - Ekran konnektörüne giden anot ve katot hatları birbirine paralel ve kesişimsiz ilerler ($4{,}500\text{ mm}$ aralık).

| Eleman | Rolü ve Değeri | Koordinat (x, y, açı) | Katman | Yönlenme ve Bağlantı |
| --- | --- | --- | --- | --- |
| `Q7` | IRLML6344TRPBF N-MOSFET | $(22{,}000, 99{,}000, 0^\circ)$ | `F.Cu` | Pad 1 (G) ve Pad 2 (S) batıya; Pad 3 (D, BL_K) doğuya bakar. |
| `R28` | $100\Omega$ 0402 PWM Seri Direnç | $(16{,}000, 98{,}050, 0^\circ)$ | `F.Cu` | Pad 1 (TFT_BL_PWM) batıya; Pad 2 (G) doğuya Q7'ye bakar. |
| `R29` | $100\text{ k}\Omega$ 0402 Pull-Down | $(18{,}800, 99{,}000, 270^\circ)$ | `F.Cu` | Pad 1 (G) kuzeyde; Pad 2 (GND) güneyde; dikey gate-source köprüsü. |
| `R60` | $5{,}6\Omega$ 0805 Akım Sınırlayıcı | $(22{,}000, 94{,}500, 0^\circ)$ | `F.Cu` | Pad 1 (+3.3V) batıya; Pad 2 (BL_A) doğuya J3.2'ye bakar. |

---

## 2. R60 Güç Kaybı, Termal Zarf ve PWM Dönüş Yolu İzolasyonu (AC #2)

1. **R60 Güç Kaybı ve Termal Dayanım Analizi:**
   - Focus LCDs TFT032B018 ekran modülünde 4 adet beyaz LED paralel bağlıdır.
   - LED nominal ileri gerilimi: $V_f \approx 3{,}0\text{--}3{,}1\text{ V}$.
   - Nominal LED akımı: $I_{BL} \approx 45\text{--}60\text{ mA}$ (maksimum $70\text{ mA}$).
   - R60 üzerindeki gerilim düşümü: $V_{R60} = 3{,}3\text{ V} - 3{,}05\text{ V} \approx 0{,}25\text{ V}$ (kötü durumda $0{,}39\text{ V}$).
   - **R60 Güç Tüketimi:**
     $$P_{R60\_nom} = I^2 \times R = (0{,}045\text{ A})^2 \times 5{,}6\Omega \approx 11{,}3\text{ mW}$$
     $$P_{R60\_max} = I^2 \times R = (0{,}070\text{ A})^2 \times 5{,}6\Omega \approx 27{,}4\text{ mW}$$
   - Standart 0805 kılıfın nominal güç dayanımı **$125\text{ mW}$** (bazı üreticilerde $250\text{ mW}$)'dır.
   - Maksimum güç kaybı ($27{,}4\text{ mW}$), kılıf sınırının **<\%22**'sidir; direnç üzerinde hiçbir termal yığılma veya aşırı ısınma meydana gelmez. Ped etrafında yeterli bakır soğutma alanı mevcuttur.

2. **PWM Dönüş Akımı ve Gürültü İzolasyonu:**
   - Arka ışık PWM anahtarlama frekansı tipik olarak $1\text{ kHz}$ ile $10\text{ kHz}$ arasındadır.
   - Anahtarlanan $45\text{--}70\text{ mA}$ genlikli kare dalga akımları Q7 Kaynak (Source, Pin 2) pini üzerinden doğrudan yerel GND düzlemine akar.
   - Bu PWM anahtarlama hücresi kartın sol-batı bölgesinde ($x\approx 16\text{--}22\text{ mm}$) konumlanmıştır:
     - INA226 hassas akım ölçüm şöntünden ($x\approx 146\text{--}168\text{ mm}$) **$> 120\text{ mm}$**,
     - BQ32000 RTC kristali ve osilatöründen ($x\approx 208\text{--}224\text{ mm}$) **$> 180\text{ mm}$**
     fiziksel uzaklıktadır.
   - PWM dönüş akımlarının analog ölçüm hatlarına veya saat osilatörüne kuplajı fiziksel mesafe ve kesintisiz toprak düzlemiyle tamamen engellenmiştir.

3. **TASK-065 LCD Altı Yükseklik Uyumu:**
   - Dört elemanın tümü `F.Cu` katmanındadır:
     - `Q7` (SOT-23): maks gövde $1{,}10\text{ mm}$
     - `R60` (0805): maks gövde $0{,}60\text{ mm}$
     - `R28, R29` (0402): maks gövde $0{,}50\text{ mm}$
   - Tüm elemanların montaj yüksekliği, TASK-065 ile belirlenen **$\le 1{,}80\text{ mm}$** LCD altı tavan sınırının çok altındadır; ekran modülünün montajına mekanik hiçbir engel oluşturmaz.

---

## 3. Doğrulama ve DRC Sonuçları (AC #4)

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC İhlalleri:** **145 → 145** (yeni courtyard, clearance, short, hole veya silk ihlali: **0**).
  - **Bağlantısız Öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic Parity:** **0 → 0** (şema ile netlist tam uyumlu).
- **Courtyard ve Açıklık Kontrolü:**
  - 4 eleman arasında minimum 2D aralık: **$0{,}750\text{ mm}$** (Q7--R29 arası).
  - En yakın komşu F.Cu elemanına (C34) minimum aralık: **$7{,}020\text{ mm}$**.
  - Çakışma (overlap): **0**.
- **Ankrajlar ve İzler:** `J7`, `J3` (kilitli), `J9`, `H1–H4`, `D5`, `U11` konum/açı/yüz ankrajları ve TASK-058 D5.2--U11.9 FB izi UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-081-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-081-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-081-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-081-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-081-20260924/verify.py)
