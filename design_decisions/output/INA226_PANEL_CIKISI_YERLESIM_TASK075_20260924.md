# INA226 ölçüm ve panel çıkışı grubu ilişkisel yerleşimi — TASK-075, 24 Eylül 2026

INA226 akım/güç ölçümü ve panel çıkışı grubunun (`INA226 OLCUM + PANEL CIKISI`) 10 footprint üyesi (U3, U13, RShunt1, J4, D7, C11, C35, R27, R59, R61), TI INA226 Kelvin algılama kuralları, 3 A çıkış güç akışı, TVS koruma kenetlemesi, U13 donanım kapatma mantığı ve ön panel banana kablo lehimleme alanına göre ilişkisel olarak yerleştirildi. On footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 B.Cu yüz ataması korunmuştur. Kart dışındaki geçici blok alanı (x≈146–177, y≈47–65 mm) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-075-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-075-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-075-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-075-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-075-20260924/verification.json)

## Kaynak, pin ve yerleşim kuralı

- **Texas Instruments INA226 (SBOS547C, Rev. Ağustos 2026, s. 31):**
  1. *Kelvin Şönt Bağlantısı (§8.4.1 / Şekil 8-4):*
     - U3 Pin 10 (`IN+`) ve Pin 9 (`IN-`), RShunt1 (5 mΩ 2512) şönt direncinin iç algılama padlerine bağlandı.
     - U3, $-90^\circ$ (270°) oryantasyonunda RShunt1'in doğrudan kuzeyine ($x=157{,}75, y=51{,}0$) yerleştirildi.
     - `U3.10` $\rightarrow$ `RShunt1.1` mesafesi: **4,310 mm**.
     - `U3.9` $\rightarrow$ `RShunt1.2` mesafesi: **4,310 mm**.
     - Her iki algılama hattı mikron düzeyinde **tam eşit uzunlukta**, paralel ve simetrik olarak planlanmıştır. Yüksek akım taşıyan güç bakırından bağımsız olarak ayrılmış, parazitik empedans etkisi sıfırlanmıştır.
  2. *Bus Gerilimi Algılama (VBUS):*
     - U3 Pin 8 (`VBUS`), doğrudan yük tarafı düğümü olan `OUT_POS`'a (RShunt1.2 pad'i hizasına) bağlandı (**4,01 mm**).
  3. *Güç Kaynağı Bypass Kapasitörü (§8.4.1):*
     - C11 (100 nF 0402), U3 Pin 6 (`VS` / `+3.3V`) ve Pin 7 (`GND`) pinlerinin hemen yanına ($x=162{,}2, y=53{,}0$) yerleştirildi (mesafe **2,97 mm**).
  4. *I2C Arayüzü ve Adresleme:*
     - Pin 1 ve 2 (`A1`, `A0`) doğrudan GND'ye bağlıdır (cihaz adresi `0x40` / `1000000b`).
     - Pin 4 (`SDA`) ve Pin 5 (`SCL`) MCU I2C barasına açılmıştır.

- **74LVC1G08 (SOT-23-5) Donanım Koruma Mantığı:**
  1. *Hızlı Kapatma Döngüsü:*
     - U3 Pin 3 (`ALERT` / `INA_ALERT`), açık-drenaj aşırı akım/güç alarm çıkışıdır.
     - R27 (10 kΩ 0402) pull-up direnci ile `+3.3V`'a çekilir (U3.3–R27.2: **4,74 mm**).
     - Alarm hattı doğrudan U13 Pin 2 (AND kapısı girişi B) ile birleştirilir. Aşırı akım durumunda `INA_ALERT` anında LOW'a çekilerek, MCU yazılım gecikmesi beklenmeksizin donanımsal kapatma tetiklenir.
  2. *Çıkış Enable Kontrolü:*
     - U13 Pin 1 (`OUT_EN`), MCU'dan gelen aktif-yüksek çıkış talebidir; R61 (4k7 0402) pull-down direnci ile pin dibinde GND'ye çekilir (**2,87 mm**).
  3. *Besleme Filtresi:*
     - C35 (100 nF 0402), U13 Pin 5 (`+3.3V`) ve Pin 3 (`GND`) hemen bitişiğine yerleştirildi (**1,88 mm**).
  4. *Anahtar Sürme Çıkışı:*
     - U13 Pin 4 (`SW_EN`), hem LM74801 (U12) güç anahtarını hem de aktif deşarj devresindeki Q4 tersleyicisini sürmek üzere $y\approx 62\text{ mm}$ eksenindeki enable barasına açılmıştır.

- **Panel Çıkışı J4, TVS D7 ve Pasif Bleed R59:**
  1. *J4 Banana Terminali:*
     - SolderWire 1x02 kılıfı (pitch 7,8 mm), ön panel banana jaklarına giden 1,5 mm² silikon kablolar için ayrılmıştır.
     - Pin 1 (`OUT_POS`) $x=168{,}0$, Pin 2 (`GND`) $x=175{,}8$ konumundadır; 3,9 mm dış çaplı TH pedlerin çevresinde lehimleme havya erişimi tamamen serbesttir.
  2. *D7 TVS Koruması (SMBJ30A SMB 30V):*
     - Doğrudan J4 klemensinin altına ($x=167{,}0, y=57{,}5$) yerleştirildi (D7.1–J4.1: **6,78 mm**; D7.2–J4.2: **8,96 mm**).
     - Katot (Pin 1) `OUT_POS` hattında, Anot (Pin 2) `GND` hattındadır. Harici ESD ve endüktif darbeleri kartın girişinde sönümler.
  3. *R59 Pasif Yedek Bleed (100 kΩ 0603):*
     - D7'nin altına ($x=167{,}0, y=62{,}5$) konumlandırıldı; OUT_POS ile GND arasında sürekli pasif gerilim sıfırlama ve INA226 bus tanımı sağlar.

| Alt Devre / Koridor | Elemanlar ve Pad/Net Yönü |
| --- | --- |
| 3 A Güç Akışı | `SW_OUT` batıdan RShunt1.1'e girer; RShunt1.2'den doğuya J4.1 (`OUT_POS`) ve aktif deşarj grubuna akar. |
| Kelvin Akım Algılama | RShunt1.1 → U3.10 (`IN+`) ve RShunt1.2 → U3.9 (`IN-`); 4,310 mm tam eşit simetrik diferansiyel çift. |
| Bus Gerilim Algılama | RShunt1.2 → U3.8 (`VBUS`); 4,015 mm. |
| Besleme Filtreleri | C11 (100n) U3 dibinde (2,97 mm); C35 (100n) U13 dibinde (1,88 mm). |
| Alarm ve Koruma Mantığı | U3.3 (`INA_ALERT`) → R27 pull-up (4,74 mm) → U13.2; R61 pull-down (2,87 mm) → U13.1 (`OUT_EN`); U13.4 → `SW_EN`. |
| Çıkış Klemensi ve TVS | J4.1 (`OUT_POS`) ve J4.2 (`GND`) terminallerine D7 TVS diyotu (6,78 mm / 8,96 mm) ve R59 bleed direnci paralel bağlanır. |

## 3 A Güç yolu ve termal değerlendirme

1. **RShunt1 Güç Kaybı:**
   - $R_{shunt} = 5\text{ m}\Omega$, nominal maksimum sürekli akım $I_{max} = 3{,}0\text{ A}$.
   - Sürekli güç kaybı:
     $$P = I^2 R = (3{,}0)^2 \times 0{,}005 = \mathbf{0{,}045\text{ W}} \quad (45\text{ mW})$$
   - 2512 kılıfının 1 W – 2 W anma gücünün %5'inden düşüktür; ısınma etkisi ihmal edilebilir düzeydedir.
2. **Güç Bakırı ve İletkenlik:**
   - 3 A akım koridoru için IPC-2152 standardına göre 1 oz (35 µm) bakırda 10°C sıcaklık artışı için minimum 1,5 mm iz genişliği yeterlidir; bu yerleşimde RShunt1–J4 arasında >3 mm genişliğinde poligon dökümü planlanmıştır.
   - Kesin iz genişlikleri ve katman dağılımı TASK-008 routing aşamasında doğrulanacaktır.

## Komşuluk, yüz seçimi ve devir notları

1. **Yüz Seçimi Koordinasyonu (TASK-065 Devri):**
   - 10 elemanın tümü TASK-065 kararına uygun olarak **B.Cu** katmanında yerleştirilmiştir.
   - İki boyutlu (2D) izdüşümde elemanlar arasında çakışma yoktur (minimum aralık **0,390 mm**).
2. **Grup Komşulukları:**
   - Batı: LM74801 grubundan `SW_OUT` güç girişi ve U12 enable hattı.
   - Doğu: Aktif çıkış deşarjı grubuna (`CIKIS DESARJI`) `OUT_POS`, `GND` ve `SW_EN` hatları aktarılır.
   - Güney: ESP32-C6 modülünden `OUT_EN` kontrolü ve I2C veri yolu (`SDA`/`SCL`).

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni courtyard, clearance, short, edge veya mask ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0**.
- **Courtyard kontrolü:** 10 eleman arasında minimum 2D aralık **0,390 mm** (RShunt1–U3 arası); çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-075-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-075-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-075-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-075-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-075-20260924/verify.py)
