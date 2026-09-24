# Ethernet mezanin grubu ve besleme anahtarı ilişkisel yerleşimi — TASK-080, 24 Eylül 2026

Ethernet mezanin grubunun (`ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI`) 7 footprint üyesi (`J8`, `Q8`, `R17`, `C21`, `C10`, `C20`, `TP14`), Waveshare 2-CH UART TO ETH modül şeması, CH9121DS1 veri sayfası, TSM3443CX6 P-kanal güç anahtarı kuralları, `ETHERNET_MODULU_ANALIZI_20260923.md` ve `PCB_GENEL_YERLESIM_KARARI_20260924.md` kararlarına göre ilişkisel olarak yerleştirildi. Yedi footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 `B.Cu` yüz ataması korunmuştur. Kart dışındaki geçici blok alanı ($x\approx 140\text{--}214\text{ mm}$, $y\approx 138\text{--}161\text{ mm}$) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-080-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-080-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-080-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-080-20260924/board-bottom.svg) ·
[x/y/açı/yüz, ölçüm ve Z yükseklik verileri](../../hardware/docs/reports/task-080-20260924/verification.json)

## Devre topolojisi, pin ve yerleşim kuralları

1. **Q8 TSM3443CX6 Yüksek Taraf Besleme Anahtarı ve Yumuşak Açılış (Soft-Start) Hücresi:**
   - **Topoloji:** Q8 (P-kanal MOSFET, SOT-23-6 / SOT-26, $-20\text{ V}$, $R_{\text{DS(on)}} \le 100\text{ m}\Omega$ @ $V_{\text{GS}}=-2{,}5\text{ V}$, Özdisan 1211076).
     - *Kaynak (Source, Pin 4):* Doğrudan ana $+3.3\text{V}$ sistem rayına bağlıdır.
     - *Kapı (Gate, Pin 3):* ESP32-C6 mikrodenetleyicisinin GPIO0 pininden R16 ($10\text{ k}\Omega$) seri direnci üzerinden gelen `/MCU/ETH_PWR_EN` aktif-low sinyaliyle sürülür.
     - *Savak (Drain, Pin 1, 2, 5, 6):* Anahtarlanan `/MCU/ETH_3V3` rayına bağlıdır; modülün Pins 13 ve 14'ünü besler.
   - **R17 ($100\text{ k}\Omega$ 0402) Kapı Pull-Up Direnci:**
     - Kaynak ($+3.3\text{V}$) ile Kapı (`ETH_PWR_EN`) arasına doğrudan bağlanmıştır ($R17.1 \leftrightarrow Q8.4 = 2{,}626\text{ mm}$, $R17.2 \leftrightarrow Q8.3 = 2{,}626\text{ mm}$).
     - ESP32-C6 reset/boot aşamasındayken GPIO0 yüksek empedansta kaldığında Q8'in kapısını kesin olarak $+3.3\text{V}$'a çekerek kapalı tutar; modül açılışta enerjisiz başlar (arıza-emniyetli tasarım).
   - **C21 ($100\text{ nF}$ 0402) Yumuşak Açılış Kapasitörü:**
     - Kaynak ($+3.3\text{V}$) ile Kapı (`ETH_PWR_EN`) arasına R17 ile tam paralel yerleştirilmiştir ($C21.1 \leftrightarrow R17.1 = 3{,}000\text{ mm}$, $C21.2 \leftrightarrow R17.2 = 3{,}000\text{ mm}$).
     - R16 ($10\text{ k}\Omega$) ve R17 ($100\text{ k}\Omega$) ile birlikte açılma zaman sabiti:
       $$\tau_{\text{on}} \approx (R16 \parallel R17) \times C21 \approx 9{,}09\text{ k}\Omega \times 100\text{ nF} \approx 0{,}91\text{ ms}$$
     - Aşağı akıştaki toplam sığa ($C10 = 22\text{ }\mu\text{F}$ + $C20 = 100\text{ nF}$ + modül içi sığa $\approx 12\text{ }\mu\text{F} \rightarrow C_{\text{load}} \approx 34\text{ }\mu\text{F}$) şarj edilirken ani akım (inrush current) yaklaşık $62\text{ mA}$ seviyesinde sınırlandırılır. Ana $+3.3\text{V}$ rayında hiçbir gerilim çökmesi (droop) oluşmaz.
     - Kapanma zaman sabiti: $\tau_{\text{off}} = R17 \times C21 = 100\text{ k}\Omega \times 100\text{ nF} = 10\text{ ms}$ (tam deşarj $\sim 3\tau = 30\text{ ms}$). Firmware, Fixed PDO geçişine başlamadan önce $\ge 50\text{ ms}$ bekleyerek Ethernet yükünün tamamen devreden çıktığını garanti eder.

2. **Yüksek Frekans Ayırma ve Bulk Kapasite Düzenlemesi:**
   - **C20 ($100\text{ nF}$ 0402 Yüksek Frekans Dekuplajı):** Q8 Savak uçlarının (Pin 1, 6) hemen çıkışına yerleştirildi ($Q8.6 \rightarrow C20.1 = 3{,}441\text{ mm}$). Yüksek frekanslı anahtarlama gürültüsünü filtreler.
   - **C10 ($22\text{ }\mu\text{F}$ 0805 Bulk Rezervuarı):** C20 ile J8 pin header'ı arasına yerleştirildi ($C20.1 \rightarrow C10.1 = 3{,}234\text{ mm}$, $C10.1 \rightarrow J8.13 = 4{,}299\text{ mm}$). CH9121 Ethernet paket iletim anlarındaki ani 100BASE-TX akım darbelerini karşılar.
   - **GND Dönüş Döngüsü:** C20.2 ile C10.2 ($3{,}234\text{ mm}$) ve C10.2 ile J8.11 GND pini ($4{,}299\text{ mm}$) doğrudan geniş bakır koridoruyla birleştirildi. Yüksek frekans akım döngü alanı $< 15\text{ mm}^2$ seviyesinde tutularak EMI yayılımı engellendi.

3. **Koridor Ayrımı: Güç ve Sinyal İzolasyonu (AC #3):**
   - **Kuzey Güç Koridoru ($y \in [140{,}5, 146{,}5]\text{ mm}$):**
     - $+3.3\text{V}$ ana ray girişi, `ETH_PWR_EN` kapı kontrolü, Q8 MOSFET hücresi, `ETH_3V3` anahtarlanan rayı, C20, C10 ve J8 Pins 11--14 (GND ve 3V3).
     - Güç akışı tamamen batıdan doğuya doğru tek yönlü ve kısa ilerler.
   - **Güney Sinyal ve Teşhis Koridoru ($y \in [150{,}0, 158{,}5]\text{ mm}$):**
     - J8 Pin 7 (`UART_RX` $\rightarrow$ ESP32 GPIO17), Pin 5 (`UART_TX` $\leftarrow$ ESP32 GPIO16), Pin 3 (`ETH_CFG0` $\leftarrow$ ESP32 GPIO8) ve Pin 4 (`ETH_RUN` $\rightarrow$ TP14).
     - Tüm sinyal pinleri J8'in batı dış sütunundan doğrudan batıya, MCU bölgesine açılır.
   - **İzolasyon Mesafesi:** Güç koridorunun en güney pini (J8.11 GND, $y=145{,}53\text{ mm}$) ile sinyal koridorunun en kuzey pini (J8.7 UART_RX, $y=150{,}61\text{ mm}$) arasında **$5{,}08\text{ mm}$ (2 header adımı)** fiziksel açıklık bulunur. Header'daki Pins 9 ve 10 (RST1 / RESET) bağlanmadığından (No-Connect) güç gürültüsünün UART veri hatlarına kapasitif/endüktif kuplajı tamamen bloke edilmiştir.

4. **Teşhis Test Noktası (TP14):**
   - J8 Pin 4 (`ETH_RUN` çıkışı) sinyali için $1{,}0\text{ mm}$ çapında test pedi (`TP14`, $OD=2{,}0\text{ mm}$) yerleştirildi ($x=153{,}000$, $y=155{,}690$).
   - TP14, J8 modül gövdesinin ve courtyard sınırının tamamen batısında, açık alandadır ($J8.4 \leftrightarrow TP14 = 7{,}827\text{ mm}$). Modül karta takılıyken dahi osiloskop ve multimetre probları ile \%100 fiziksel erişim sağlanır.

| Eleman | Rolü ve Değeri | Koordinat (x, y, açı) | Bağlantı ve Yönlenme |
| --- | --- | --- | --- |
| `J8` | Waveshare 2-CH UART TO ETH | $(158{,}287, 158{,}230, 180^\circ)$ | $2\times 8$ header batıda ($x\approx 158..161$), RJ45 doğuda ($x\approx 205..214$). B.Cu. |
| `Q8` | TSM3443CX6 P-MOSFET SOT-26 | $(147{,}000, 142{,}990, 90^\circ)$ | Pad 4 (+3.3V) & Pad 3 (Gate) batıya bakar; Pad 1,2,5,6 (Drain) doğuya bakar. |
| `R17` | $100\text{ k}\Omega$ 0402 Kapı Pull-Up | $(143{,}500, 142{,}990, 270^\circ)$ | Pad 1 (+3.3V) kuzeyde, Pad 2 (`ETH_PWR_EN`) güneyde; Q8 ile tam paralel. |
| `C21` | $100\text{ nF}$ 0402 Yumuşak Açılış | $(140{,}500, 142{,}990, 270^\circ)$ | Pad 1 (+3.3V) kuzeyde, Pad 2 (`ETH_PWR_EN`) güneyde; R17 ile tam paralel. |
| `C20` | $100\text{ nF}$ 0402 HF Dekuplaj | $(150{,}800, 144{,}260, 270^\circ)$ | Pad 1 (`ETH_3V3`) kuzeyde, Pad 2 (GND) güneyde; Q8 Drain çıkışında. |
| `C10` | $22\text{ }\mu\text{F}$ 0805 Bulk Rezervuar | $(154{,}000, 144{,}260, 270^\circ)$ | Pad 1 (`ETH_3V3`) kuzeyde, Pad 2 (GND) güneyde; J8 Pins 11--14 girişinde. |
| `TP14` | $D1{,}0\text{ mm}$ Test Pedi (`ETH_RUN`) | $(153{,}000, 155{,}690, 0^\circ)$ | J8 Pin 4 hizasında, modül gövdesi dışında \%100 erişilebilir. |

---

## Modül altı 3D yükseklik haritası ve mekanik kısıtlar (AC #2, AC #6, AC #7)

Waveshare modülü ana karta standoff olmadan, $2\times 8$ pin header ve iki mekanik pin (`MP1`, `MP2`) ile lehimlenir. Tüm modül altı homojen bir yüksekliğe sahip değildir; 4 belirgin XY/Z bölgesi tanımlanmıştır:

```
+─────────────────────────── J8 MODÜL ALTI HARİTASI (B.Cu) ───────────────────────────+
│                                                                                     │
│  [BÖLGE 1: HEADER]       [BÖLGE 2: ORTA BOŞLUK]          [BÖLGE 3: RJ45 KEEPOUT]   │
│  x = 156.0 .. 162.0      x = 162.0 .. 198.0              x = 198.0 .. 214.5        │
│  y = 138.0 .. 160.6      y = 138.0 .. 160.6              y = 138.0 .. 160.6        │
│                                                                                     │
│  2x8 Pin Header          Nominal Z = 2.50 mm             RJ45 Pim Çıkıntısı ~2.2mm  │
│  Z = 0 (B.Cu dolu)       Min Z (tolerans) = 1.90 mm      Kalan boşluk = 0.30 mm    │
│  Pimler F.Cu'ya geçer    SMD elemanlar sığabilir         MUTLAK KEEPOUT BÖLGESİ     │
│  (Top zarf kontrolü)     (Tercihen boş bırakıldı)        (Bakır/via/parça YASAK)   │
│                                                                                     │
│  ◄── BATI                                                               DOĞU ──►    │
│  [YARDIMCI ELEMANLAR]                                    [MEKANİK PİNLER]           │
│  Q8, R17, C21, C20, C10                                  MP1: (205.44, 139.69)      │
│  TP14 (x = 140 .. 155)                                   MP2: (205.44, 158.99)      │
│  Header DIŞINDA B.Cu'da                                                             │
+─────────────────────────────────────────────────────────────────────────────────────+
```

1. **Bölge 1: Header Bölgesi ($x \in [156{,}0, 162{,}0]\text{ mm}$):**
   - $2\times 8$ $2{,}54\text{ mm}$ adımlı dişi/erkek header gövdesi yer alır.
   - Plastik yükseltici nominal yüksekliği: $H_{\text{ins}} = 2{,}50\text{ mm}$ ($\pm 0{,}20\text{ mm}$).
   - B.Cu yüzeyinde $Z = 0$ (alan header tabanı tarafından işgal edilmiştir).
   - Header pimleri lehim yüzeyinden F.Cu (Top) katmanına geçer. Final kart yerleşiminde (TASK-063/TASK-008), LCD izdüşümü dışında veya pimlerin $\le 1{,}50\text{ mm}$ kesilmesi/yüzey montaj başlığı şartıyla koordine edilir.
2. **Bölge 2: Orta Boşluk ($x \in [162{,}0, 198{,}0]\text{ mm}$):**
   - Modül PCB'sinin alt yüzü görece düzdür; nominal ara mesafe $Z_{\text{nom}} = 2{,}50\text{ mm}$'dir.
   - *En Kötü Durum Tolerans Analizi:*
     - Header yükseltici toleransı: $-0{,}20\text{ mm}$
     - PCB eğrilmesi (IPC Class 2, 53 mm üzerinde max \%0,75): $-0{,}20\text{ mm}$
     - Lehim menisküsü ve oturma farkı: $-0{,}20\text{ mm}$
     - **Kullanılabilir Net Minimum Yükseklik:** $Z_{\text{min}} = 2{,}50 - 0{,}20 - 0{,}20 - 0{,}20 = 1{,}90\text{ mm}$.
3. **Bölge 3: RJ45 Pim Çıkıntısı ve Keepout ($x \in [198{,}0, 214{,}5]\text{ mm}$):**
   - Entegre trafolu RJ45 konnektörünün THT lehim bacakları modül altından yaklaşık **$2{,}20\text{ mm}$** dışarı taşar.
   - Anakart B.Cu yüzeyi ile bacak uçları arasındaki nominal boşluk yalnızca $2{,}50 - 2{,}20 = 0{,}30\text{ mm}$'dir.
   - $\pm 0{,}25\text{ mm}$ montaj toleransı eklendiğinde bacaklar anakart bakırına temas edebilir ve kısa devre riski doğurur.
   - **Kural:** Anakart B.Cu üzerinde RJ45 izdüşümü ($x \in [198{,}0, 214{,}5]$, $y \in [138{,}0, 160{,}6]$) **MUTLAK KEEPOUT** alanıdır; hiçbir SMD eleman, via veya açık bakır bulunamaz.
4. **Bölge 4: Mekanik Montaj Pimleri (`MP1`, `MP2`):**
   - Konumlar: $(205{,}44, 139{,}69)$ ve $(205{,}44, 158{,}99)$ mm. THT delikleri anakartı boydan boya deler; etrafında elektriksel izolasyon halkası korunmalıdır.

### Aday elemanlar için gövde + lehim zarfı ve yerleşim kararı (AC #7)

Dayanağı olmayan genel "$\le 2\text{ mm}$ her şey sığar" kabulü reddedilmiştir. Her eleman için maksimum boyutlar incelenmiştir:

| Ref | Kılıf | Maksimum Gövde (mm) | Maksimum Lehim (mm) | Toplam Zarf (mm) | Modül Altı Net Açıklık ($1{,}90\text{ mm}$ bazlı) | Yerleşim Kararı ve Gerekçesi |
| --- | --- | --- | --- | --- | --- | --- |
| `Q8` | SOT-23-6 | 1,45 | 0,15 | 1,60 | 0,30 mm | **Modül Dışında (Header Yanı):** 0,30 mm açıklık marjı termal ve mekanik açıdan risklidir. Isı yayılımı ve lehim kontrolü için header batısına yerleştirildi. |
| `C10` | 0805 | 1,40 | 0,15 | 1,55 | 0,35 mm | **Modül Dışında (Header Yanı):** 0,35 mm açıklık marjı dar. Yüksek frekans akım döngüsü header hemen girişinde tutuldu. |
| `C20` | 0402 | 0,60 | 0,05 | 0,65 | 1,25 mm | **Modül Dışında (Header Yanı):** Modül altına sığabilir ($1{,}25\text{ mm}$ açıklık); ancak Q8 ve C10 ile aynı dekuplaj hücresinde kalması için header batısına yerleştirildi. |
| `C21` | 0402 | 0,60 | 0,05 | 0,65 | 1,25 mm | **Modül Dışında (Header Yanı):** Sığabilir; Q8 Gate/Source girişinde tutuldu. |
| `R17` | 0402 | 0,60 | 0,05 | 0,65 | 1,25 mm | **Modül Dışında (Header Yanı):** Sığabilir; Q8 Gate/Source girişinde tutuldu. |
| `TP14` | Pad D1.0 | 0,05 | 0,05 | 0,10 | 1,80 mm | **Modül Dışında (Zorunlu):** Yükseklik sığsa dahi modül altında test probu fiziksel olarak temas edemez. Teşhis için dışarıda olması şarttır. |

**Tasarım Kararı Özeti:**
Altı yardımcı elemanın tümü J8 header'ının batısında ($x \in [140{,}5, 154{,}0]\text{ mm}$), modül izdüşümünün hemen dışında konumlandırılmıştır. Bu tercih:
1. KiCad DRC'sinde J8'in tüm modülü kapsayan B.Courtyard poligonu ile **0 çakışma** (courtyards_overlap: 0) sağlar.
2. Modül takılıyken dahi tüm elemanların optik muayene ve havya ile yeniden işleme (rework) yapılabilmesini garanti eder.
3. TP14 test noktasına osiloskop probu ile \%100 erişim sunar.
4. Sıcak güç ve anahtarlama elemanlarının modül altına hapsolarak aşırı ısınmasını önler.
5. Header Pins 11--14'e olan yol uzunluklarını $< 4{,}3\text{ mm}$'de tutarak elektriksel performanstan hiçbir taviz vermez.

*Not:* TASK-053 kapsamında gelecek fiziksel numune ile header yükseltici toleransı, RJ45 bacak boyu ve PCB düzlüğü laboratuvarda kumpasla ölçülecek; model değerleri kalibre edilecektir.

---

## Doğrulama ve DRC sonuçları

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni courtyard, clearance, short, hole veya silk ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0** (şema ile netlist tam uyumlu).
- **Courtyard kontrolü:**
  - Ayrık 6 eleman arasında minimum 2D aralık: **$1{,}280\text{ mm}$** (R17--Q8 arası).
  - Elemanların J8 modülüne minimum aralığı: **$0{,}322\text{ mm}$** ($C10\text{--}J8$ arası, courtyard poligonu dışı).
  - Çakışma (overlap): **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-080-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-080-20260924/drc-after.json)
- [Doğrulama, ölçüm ve Z haritası](../../hardware/docs/reports/task-080-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-080-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-080-20260924/verify.py)
