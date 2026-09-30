# I2C seviye dönüştürücü grubu ilişkisel yerleşimi — TASK-079, 24 Eylül 2026

I2C seviye dönüştürücü grubunun (`I2C SEVIYE DONUSTURUCU 5V <-> 3.3V`) 6 footprint üyesi (`Q1`, `Q2`, `R4`, `R5`, `R6`, `R7`), NXP AN10441 çift yönlü seviye dönüştürücü topolojisi, BSS138P üretici kuralları ve TASK-065 B.Cu yüz atamasına göre ilişkisel olarak yerleştirildi. Altı footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 `B.Cu` yüz ataması korunmuştur. Kart dışındaki geçici blok alanı ($x\approx 207\text{--}215$, $y\approx 106\text{--}116\text{ mm}$) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-079-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-079-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-079-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-079-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-079-20260924/verification.json)

## Devre topolojisi, pin ve yerleşim kuralları

- **NXP AN10441 Çift Yönlü I2C Seviye Dönüştürücü Mimarisi:**
  1. *Çift Kanal Simetrik Kolon Yapısı:*
     - Devre, iki bağımsız sinyal hattı (`SCL` ve `SDA`) için **tamamen paralel ve simetrik iki dikey kolon** halinde kurgulandı:
       - **Sol Kolon (SCL Kanalı, $x=209{,}000\text{ mm}$):**
         - Kuzey: `R4` (4.7 kΩ 0402 3.3V pull-up, $y=107{,}500$, rot $180^\circ$).
         - Merkez: `Q1` (BSS138P N-MOSFET SOT-23, $y=111{,}000$, rot $270^\circ$).
         - Güney: `R5` (4.7 kΩ 0402 5V pull-up, $y=114{,}500$, rot $90^\circ$).
       - **Sağ Kolon (SDA Kanalı, $x=213{,}500\text{ mm}$):**
         - Kuzey: `R7` (4.7 kΩ 0402 3.3V pull-up, $y=107{,}500$, rot $0^\circ$).
         - Merkez: `Q2` (BSS138P N-MOSFET SOT-23, $y=111{,}000$, rot $270^\circ$).
         - Güney: `R6` (4.7 kΩ 0402 5V pull-up, $y=114{,}500$, rot $90^\circ$).
  2. *Gerilim Alanları ve Yönlenme (Voltage Domains):*
     - **3.3 V Düşük Gerilim Alanı (KUZEY):**
       - MOSFET kaynak (Source, Pin 2) uçları ve 3.3 V pull-up dirençleri kuzeye bakar.
       - Hatlar doğrudan kuzeydeki BQ32000 RTC modülüne (`U4.5` SDA, `U4.6` SCL) ve batıdaki ESP32-C6 mikrodenetleyicisi ile INA226 akım sensörüne kesişimsiz olarak açılır.
     - **5.0 V Yüksek Gerilim Alanı (GÜNEY):**
       - MOSFET savak (Drain, Pin 3) uçları ve 5 V pull-up dirençleri güneye bakar.
       - Hatlar doğrudan güneydeki AP33772S USB-PD kontrolcüsüne (`U1.11` SDA, `U1.12` SCL) yönelir.
  3. *Mikron Düzeyinde Kanal Simetrisi:*
     - Kaynak $\rightarrow$ Pull-up mesafesi:
       - $Q1.2 \rightarrow R4.1$ (`SCL_3V3`): **2,600 mm**
       - $Q2.2 \rightarrow R7.2$ (`SDA_3V3`): **2,600 mm**
       - Simetri farkı: **0,000 mm**.
     - Savak $\rightarrow$ Pull-up mesafesi:
       - $Q1.3 \rightarrow R5.2$ (`SCL_5V`): **2,052 mm**
       - $Q2.3 \rightarrow R6.2` (`SDA_5V`): **2,052 mm**
       - Simetri farkı: **0,000 mm**.
     - Hatlar arasında karşılıklı dolaşma (crossover) kesinlikle yoktur. İki kanal mikron hassasiyetinde tam eşit gecikme ve yükselme zamanı (rise time) karakteristiğine sahiptir.
  4. *Yatay Ortak Besleme Baraları:*
     - **Gate Barası (+3.3V):** $Q1.1 \leftrightarrow Q2.1$ arası $4{,}500\text{ mm}$ doğrudan yatay iz ile birleştirildi.
     - **3.3V Pull-Up Barası:** $R4.2 \leftrightarrow R7.1$ arası $4{,}500\text{ mm}$ doğrudan yatay iz ile birleştirildi.
     - **5V Pull-Up Barası (PD_5V):** $R5.1 \leftrightarrow R6.1$ arası $4{,}500\text{ mm}$ doğrudan yatay iz ile birleştirildi.

| Alt Devre / Kolon | Elemanlar ve Pad/Net Yönü |
| --- | --- |
| SCL Kanalı (x=209.0 mm) | `R4` (3.3V pull-up) $\rightarrow$ `Q1` (BSS138P) $\rightarrow$ `R5` (5V pull-up). Kuzey: `SCL_3V3`, Güney: `SCL_5V`. |
| SDA Kanalı (x=213.5 mm) | `R7` (3.3V pull-up) $\rightarrow$ `Q2` (BSS138P) $\rightarrow$ `R6` (5V pull-up). Kuzey: `SDA_3V3`, Güney: `SDA_5V`. |
| +3.3V Gate & Pull-up Barası | $Q1.1 \leftrightarrow Q2.1$ (4,50 mm) ve $R4.2 \leftrightarrow R7.1$ (4,50 mm) yatay hatları. |
| PD_5V Pull-up Barası | $R5.1 \leftrightarrow R6.1$ (4,50 mm) yatay hattı. |

## Komşuluk, yüz seçimi ve devir notları

1. **Yüz Seçimi Koordinasyonu (TASK-065 Devri):**
   - 6 elemanın tümü TASK-065 kararına uygun olarak **B.Cu** katmanındadır.
   - İki boyutlu (2D) izdüşümde elemanlar arasında çakışma yoktur (minimum aralık **0,590 mm** Q1–R5 ve Q2–R6 arası).
2. **Grup Komşulukları:**
   - Kuzey: RTC BQ32000 grubu ($y\approx 94\text{--}101\text{ mm}$) ile 3.3 V I2C veri yolu paylaşılır (aralık $\sim 5{,}5\text{ mm}$).
   - Güney: AP33772S grubu ($y\approx 135\text{--}155\text{ mm}$) ve Test Noktaları grubu ($y\approx 122\text{--}126\text{ mm}$) ile 5 V I2C veri yolu bağlanır.
   - Batı: ESP32-C6 mikrodenetleyici grubu ($x\approx 152\text{--}163\text{ mm}$) ile I2C kontrolü sağlanır.

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni courtyard, clearance, short, edge veya mask ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0**.
- **Kanal Simetrisi:** SCL ve SDA kanallarında pull-up hat uzunlukları tam eşit (**2,600 mm** ve **2,052 mm**); simetri farkı **0,000 mm**.
- **Courtyard kontrolü:** 6 eleman arasında minimum 2D aralık **0,590 mm**; çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-079-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-079-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-079-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-079-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-079-20260924/verify.py)
