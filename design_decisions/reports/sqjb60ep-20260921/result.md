# Q3/Q4 ve Q5/Q6 → SQJB60EP-T1_GE3

**Tarih:** 2026-09-21
**Kapsam:** `usb_pd_controller` sayfası — dahili kol anahtarı (eski Q3/Q4) ve kullanıcı çıkış anahtarı (eski Q5/Q6)
**Kaynak:** Vishay Siliconix doc 77774, S22-0167 Rev. B (14-Feb-2022) → `hardware/datasheets/sqjb60ep.pdf`
**Sonuç:** Uygulandı. Dahili kolda tam isabet; çıkış kolunda **RDS(on) onaylı spesifikasyonun 3 katı** (§3).

---

## 1. Parça, tasarımın varsaydığından farklı: bu bir **dual**

SQJB60EP tek FET değil, **tek pakette iki bağımsız N-kanal FET**tir
(PowerPAK SO-8L Dual, 6.15 × 5.13 mm). Pin haritası:

| Pin | 1 | 2 | 3 | 4 | 5, 6 | 7, 8 |
|---|---|---|---|---|---|---|
| | S1 | G1 | S2 | G2 | D2 | D1 |

Şemadaki her iki çift de zaten **ortak source, sırt sırta** bağlıydı
(Q4.S–Q3.S ortak + kapılar birleşik; Q5.S–Q6.S ortak + kapılar birleşik).
Bu topoloji bir dual paketin tam olarak karşıladığı şeydir, dolayısıyla her
çift **tek pakete indi**:

| Eskiden | Şimdi |
|---|---|
| Q3 + Q4 (2 × IRF7855TRPBF, 2 × SOIC-8) | **Q3** (1 × SQJB60EP, unit A + B) |
| Q5 + Q6 (2 × "60V 4mR TBD", footprint yok) | **Q5** (1 × SQJB60EP, unit A + B) |

`Q4` ve `Q6` referansları artık yoktur. Dört paket ikiye indi.

## 2. Datasheet özeti

| | Değer |
|---|---|
| VDS | 60 V |
| VGS | ±20 V |
| VGS(th) | 1.5 / 2.0 / 2.5 V |
| **RDS(on) @ VGS = 10 V** | **10 mΩ tip., 12 mΩ maks.** (125 °C'de 19.1 mΩ, 175 °C'de 23.5 mΩ) |
| RDS(on) @ VGS = 4.5 V | 13.1 mΩ tip., 16 mΩ maks. |
| ID (bacak başına) | 30 A @ TC 25 °C, 26 A @ 125 °C; IDM 84 A |
| PD | 48 W @ TC 25 °C |
| RthJA / RthJC | 85 °C/W (1 inç² pad) / 3.1 °C/W |
| Qg | 18 nC tip., 30 nC maks. |
| Gövde diyodu VSD | 0.84 V tip. @ 10 A |
| Avalanş | IAS 23 A, EAS 26.5 mJ, %100 UIS testli |
| Nitelik | AEC-Q101, TJ −55…+175 °C |

## 3. Handoff gereksinimlerine karşı denetim

### 3.1 Dahili kol (eski Q3/Q4) — handoff §3.2 #2: "küçük dual NMOS, 40–60 V, ≥2 A"

| Gereksinim | SQJB60EP | |
|---|---|---|
| Dual | Dual | ✅ tam istenen |
| 40–60 V | 60 V | ✅ |
| ≥2 A | 30 A/bacak | ✅ |
| "küçük" | 2 × SOIC-8 yerine 1 × PowerPAK SO-8L Dual | ✅ kart alanı ~yarıya iner |

Dahili yük ~1.4 A (3.3 V rayı). Sırt sırta 24 mΩ → **34 mV düşüm, 47 mW**.
Önemsiz. Kapı sürüşü AP33772S şarj pompası + R12 (6.2 kΩ) üzerinden; Qg 18 nC
IRF7855 sınıfında, yavaş açılış zaten istenen davranış. **Sorun yok.**

### 3.2 Çıkış kolu (eski Q5/Q6) — handoff §3.4 #2 / §8

| Gereksinim | SQJB60EP | |
|---|---|---|
| 60 V | 60 V | ✅ |
| Vgs ±20 V | ±20 V | ✅ (D6 BZT52C12 12 V'a kırpıyor) |
| 5×6 DFN | PowerPAK SO-8L Dual 6.15 × 5.13 mm | ✅ üstelik iki FET'i tek pakete alıyor |
| **≤4 mΩ @ 10 V** | **12 mΩ maks.** | ❌ **3 kat** |
| 28 V × 1–5 A × ~10 ms SOA | görünüşte marjlı, ölçülmeli | ⚠️ |

## 4. RDS(on) sapmasının sayısal sonucu

Sırt sırta iki FET seri olduğu için yol direnci **2 × RDS(on)**:

| | hedef (≤4 mΩ) | SQJB60EP 25 °C | SQJB60EP 125 °C |
|---|---|---|---|
| Kol direnci | 8 mΩ | 24 mΩ | 38.2 mΩ |
| 5 A'de düşüm | 40 mV | **120 mV** | **191 mV** |
| 5 A'de kayıp | 0.20 W | **0.60 W** | **0.96 W** |

### 4.1 Isıl — sorun değil

İki die'ın ayrı drain pad'i var, güç paylaşılıyor: die başına 0.30 W
(125 °C'de 0.48 W). RthJA 85 °C/W ile die başına ~26–41 °C artış. TJ,
175 °C sınırından çok uzak. **Isıl risk yok.**

### 4.2 Verim — 28 V'ta önemsiz, 3.3 V'ta değil

- 28 V / 5 A (140 W): 0.6–0.96 W = **%0.4–0.7**. Önemsiz.
- 3.3 V / 5 A (16.5 W): 120–191 mV = **%3.6–5.8**.

### 4.3 Asıl sonuç: 3.3 V tam yükte adaptör başlığı

`USB_VBUS` → `OUT_POS` arasındaki toplam seri direnç:

```
R11      (AP33772S sonti)  5 mΩ  ->  25 mV @ 5 A
Q5A+Q5B                   24 mΩ  -> 120 mV @ 5 A   (125 °C'de 191 mV)
RShunt1  (INA226 sonti)    5 mΩ  ->  25 mV @ 5 A
                          -----      ------
toplam                    34 mΩ      170 mV   (125 °C'de 241 mV)
```

≤4 mΩ FET'lerle bu toplam 90 mV olurdu. Yani **FET'ler yol düşümünü iki-üç
katına çıkarıyor.**

3.3 V / 5 A çıkış için adaptörün **3.47–3.54 V** (artı kablo düşümü) vermesi
gerekir. Adaptörün APDO minimumu 3.3 V ise **3.3 V çıkış tam akımda
ulaşılamaz**. Düşük akımda sorun yok (1 A'de ~3.34 V yeter).

Düşüm INA226'nın ölçüm halkasının **içinde** (Vbus, FET'lerin ve şöntün
arkasındaki `OUT_POS`'tan okunuyor), dolayısıyla **gösterilen değer doğru
kalır**; firmware PPS 20 mV adımlarıyla telafi eder. Kaybedilen şey doğruluk
değil, **3.3 V tabanındaki başlık**.

### 4.4 SOA (inrush)

AP74502Q yumuşak açılışı: CdVdT 22 nF + RG 1 kΩ → ~2.7 V/ms. 1000 µF
kapasitif yükte I = 1000 µF × 2700 V/s = **2.7 A**, süre 28/2.7 ≈ **10.4 ms**.
t=0'da paket gücü 28 V × 2.7 A = 75 W (die başına ~37 W), lineer düşerek 0.

Datasheet SOA eğrisinde (s. 5) 10 ms eğrisi VDS ≈ 14 V'ta kabaca 4–5 A
gösteriyor; gereken 2.7 A. Marj var gibi, üstelik gerçek olayda VDS düşüyor
(sabit-VDS SOA testinden daha hafif). Ancak eğri TC = 25 °C içindir.
**Prototipte doğrulanmalı** (handoff §10.5 zaten bunu istiyor).

## 5. Uygulanan değişiklik

**`hardware/libraries/Power_Supply_Custom.kicad_sym`** — yeni `SQJB60EP`
sembolü (2 unit). Pin geometrisi kasten `IRF7855_SO8` / `Q_NMOS_GSD` ile
**birebir aynı** tutuldu (G −5.08,0,0; S 2.54,−5.08,90; D 2.54,5.08,270), bu
sayede yerleşim ve teller hiç oynamadı. Fazla drain pinleri (8 ve 6) üst üste
yığılıp gizlendi — `IRF7855_SO8`'in kendi S2/S3, D6/D7/D8 için yaptığının aynısı.

- unit A: S=1, G=2, D=7 (+8 gizli)
- unit B: S=3, G=4, D=5 (+6 gizli)

**`hardware/usb_pd_controller.kicad_sch`** — dört sembol iki parçaya indirildi
(Q3A/Q3B, Q5A/Q5B), alanlar datasheet'ten dolduruldu, artık kullanılmayan
`Transistor_FET:Q_NMOS_GSD` ve `Power_Supply_Custom:IRF7855_SO8` önbellek
girdileri kaldırıldı.

Doğrulama:

```
ERC: 2 ihlal (0 hata, 2 uyari)   <- değişim öncesiyle aynı
netlist: 105 net                 <- aynı
baglanti farki: 7 kayip, 7 yeni  <- tamamı pin yeniden numaralaması
readability: 9 bulgu             <- aynı, Q3/Q5 ile ilgisiz
```

Değişen 7 netin **Q dışı üyeleri birebir korundu**:

| Net | Q dışı üyeler (değişmedi) | Q pinleri: eski → yeni |
|---|---|---|
| PD_GATE | R12.2, TP5.1 | Q3.4+Q4.4 → Q3.2+Q3.4 |
| PD_VBUS_SENSED | C3.1, R11.2, R55.1, TP2.1, U1.24 | Q4.5-8, Q5.3 → Q3.7-8, Q5.7-8 |
| PD_VOUT | C8.1, C25.1, C26.1, C29.1, L3.2, R13.2, R53.1, TP3.1, U11.3 | Q3.5-8 → Q3.5-6 |
| GATE_DRV | D6.1, R54.1, U12.6 | Q5.1+Q6.1 → Q5.2+Q5.4 |
| SRC_COMMON | D6.2, U12.8 | Q5.2+Q6.2 → Q5.1+Q5.3 |
| SW_OUT | RShunt1.1, U3.10 | Q6.3 → Q5.5-6 |
| Net-(Q3A-S) | — | Q3/Q4 ortak source |

## 6. Yapılmadı / açık

### 6.1 Footprint yok — **bloke edici**

PowerPAK **SO-8L Dual** land pattern'i KiCad'de yok.
`Package_SO:PowerPAK_SO-8_Dual` kullanılamaz: hem L-dışı varyant, hem de
drain'leri **5/6** diye numaralandırıyor (bu parçada 5-6 = D2, 7-8 = D1).

Datasheet s. 9'dan (Vishay doc 63817) **okunabilen** ölçüler:

```
keep-out            6.75 x 7.75 mm
drain pad govdesi   1.73 x 3.99 mm, ic kenarlar +-0.25, dis kenarlar +-1.98 (merkeze gore)
drain "L" kulakcigi 0.585 genislik, dis kenar +-2.565
S/G pad'leri        0.41 x 0.72 mm, 1.27 mm adim, 4 adet
```

**Çözülemeyen:** kulakçıkların dikey konumları ve yükseklikleri
(0.9150 / 0.2550 / 0.4100 / 0.5100) ve S/G sırasının drain pad'lerine göre
dikey ofseti (3.0750 / 2.1100). Bu değerler çizimden ±%15 hatayla okunduğu
için **footprint uydurulmadı**; şemada Footprint alanı boş bırakıldı.

### 6.2 PCB güncellenmedi

`gopo.kicad_pcb` hâlâ Q3 ve Q4'ü ayrı `SOIC-8_3.9x4.9mm_P1.27mm` /
IRF7855TRPBF olarak taşıyor. Footprint çizilmeden "Update PCB from Schematic"
anlamlı sonuç vermez. Kart zaten erken yerleşim aşamasında (7 segment, 0 via,
0 zone), dolayısıyla maliyeti düşük.

### 6.3 LCSC/JLCPCB stok doğrulanmadı

Çevrimdışı. JLCPCB parça numarası aramada C727685 olarak göründü, sipariş
öncesi doğrulanmalı (handoff §0.5).
