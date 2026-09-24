# RTC BQ32000 ve 1.5F süperkapasitör grubu ilişkisel yerleşimi — TASK-078, 24 Eylül 2026

Gerçek zamanlı saat (RTC) ve süperkapasitör yedekleme grubunun (`RTC BQ32000 + 1F5 süper kapasitör`) 5 footprint üyesi (`U4`, `Y1`, `C9`, `C33`, `R24`), Texas Instruments BQ32000 Datasheet (§8.3 Yerleşim Kılavuzu & Şekil 8-4), Abracon ABS25 kristal kılavuzu ve TASK-065 B.Cu yükseklik koordinasyonuna göre ilişkisel olarak yerleştirildi. Beş footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 `B.Cu` yüz ataması korunmuştur. Kart dışındaki geçici blok alanı ($x\approx 203\text{--}230$, $y\approx 72\text{--}103\text{ mm}$) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-078-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-078-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-078-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-078-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-078-20260924/verification.json)

## Kaynak, pin ve yerleşim kuralları

- **Texas Instruments BQ32000 (SLUS900F, Rev. Ağustos 2026, s. 23–24):**
  1. *Osilatör Yerleşimi ve Simetrisi (§8.3.1 / Şekil 8-4):*
     - 32.768 kHz kristal osilatör, kaçak kapasitansları (stray capacitance) ve parazitik endüktansı en aza indirmek için doğrudan `OSCI` (Pin 1) ve `OSCO` (Pin 2) pinlerinin hemen yanına yerleştirilmelidir.
     - `U4` (SOIC-8) $180^\circ$ oryantasyonunda ($x=214{,}00, y=99{,}00$) konumlandırıldı; bu oryantasyonda Pin 1 (`OSCI`, $y=97{,}09$) ve Pin 2 (`OSCO`, $y=98{,}36$) doğrudan doğuya (sağa) bakar.
     - `Y1` (Abracon ABS25, $x=223{,}50, y=97{,}725$, rot $270^\circ$) doğrudan U4'ün doğusuna yerleştirildi. Pad 1 (`OSCI`, $y=96{,}12$) ve Pad 4 (`OSCO`, $y=99{,}32$) doğrudan batıya (U4'e) bakar.
     - Hat uzunlukları:
       - $U4.1 \rightarrow Y1.1$ (`OSCI`): **4,384 mm**
       - $U4.2 \rightarrow Y1.4$ (`OSCO`): **4,381 mm**
       - Simetri farkı (skew): **0,003 mm** (yalnızca 3 mikron!).
     - İki hat birbirini kesmez (no crossover), paralel ve tam eşleşmiş diferansiyel çift gibi ilerler.
     - Y1'in Pad 2 ve Pad 3 toprak pedleri doğuya bakar; kristal çevresinde koruyucu toprak halkası (guard ring) ve alt katmanda kesintisiz sessiz toprak adacığı oluşturulur.
  2. *VCC Besleme Filtresi (§8.3.1):*
     - `C9` (1 µF 0402 düşük ESR seramik kapasitör), U4 Pin 8 (`+3.3V`) pini hemen dibine ($x=211{,}50, y=94{,}50$, rot $90^\circ$) yerleştirildi ($U4.8\rightarrow C9.1$ mesafesi: **2,115 mm**).
     - GND dönüşü U4 Pin 4 ile iç katman toprak düzlemi üzerinden kısa döngü ile tamamlanır.
  3. *Açık-Drenaj IRQ Pull-Up Direnci:*
     - `R24` (4.7 kΩ 0402), Pin 7 (`RTC_INT`) ile Pin 8 (`+3.3V`) arasına doğrudan U4'ün batısına yerleştirildi ($x=208{,}50, y=97{,}70$, rot $0^\circ$; $U4.7\rightarrow R24.2$ mesafesi: **2,601 mm**; $U4.8\rightarrow R24.1$: **3,586 mm**).
  4. *Süperkapasitör Yedekleme Yolu (VBACK):*
     - `C33` (Korchip DCL H-Tipi 1.5 F 5.5 V yatay madeni para tipi süperkapasitör), $x=207{,}98, y=82{,}50$, rot $180^\circ$ konumundadır.
     - Pad 1 (`VBACK` pozitif terminal) $x=207{,}98$, Pad 2 (`GND` negatif terminal) $x=227{,}98$ konumundadır.
     - U4 Pin 3 (`VBACK`, $x=216{,}48, y=99{,}64$) doğrudan C33.1 padine yönelir; parazitik şarj/deşarj direnci ihmal edilebilir düzeydedir.
  5. *Termal ve Gürültü İzolasyonu:*
     - 32.768 kHz kristal ve süperkapasitör, sıcaklık dalgalanmalarından ve anahtarlama gürültüsünden korunmak amacıyla 2 W çıkış deşarj direnci `R67`'den **>19,7 mm** ve anahtarlamalı güç dönüştürücülerinden (TPS55340, AOZ1284) **>100 mm** uzakta izole edilmiştir.
  6. *Yükseklik ve Mekanik Uyum (TASK-065 Koordinasyonu):*
     - C33 gövde yüksekliği $6{,}5\text{ mm}$ (maks. $7{,}0\text{ mm}$) ve Y1 yüksekliği $2{,}5\text{ mm}$ olup, üst yüzdeki LCD ekran modülünün 1,80 mm yükseklik sınırını aştığı için TASK-065 kararıyla `B.Cu` (kart alt yüzü) katmanında tutulmuştur.

| Alt Devre / Koridor | Elemanlar ve Pad/Net Yönü |
| --- | --- |
| 32.768 kHz Osilatör | `U4.1`–`Y1.1` (`OSCI`, 4,384 mm) ve `U4.2`–`Y1.4` (`OSCO`, 4,381 mm); simetri farkı 0,003 mm; kesisimsiz. |
| VCC Bypass | `C9` (1µF 0402) Pin 8 dibinde (2,115 mm). |
| IRQ Pull-Up | `R24` (4k7 0402) Pin 7 ve Pin 8 arasında (2,601 mm). |
| VBACK Süperkapasitör | `C33` (1.5F 5.5V H-tipi) $x=207{,}98, y=82{,}50$; `U4.3` (`VBACK`) bağlantısı. |
| I2C Arayüzü | `U4.5` (`SDA`) ve `U4.6` (`SCL`) batı/güney yönünde I2C seviye dönüştürücü ve MCU barasına açılır. |

## Komşuluk, yüz seçimi ve devir notları

1. **Yüz Seçimi Koordinasyonu (TASK-065 Devri):**
   - Grubun 5 üyesinin tamamı TASK-065 kararına uygun olarak **B.Cu** katmanındadır.
   - İki boyutlu (2D) izdüşümde elemanlar arasında çakışma yoktur (minimum aralık **0,540 mm** C33–C9 arası).
2. **Grup Komşulukları:**
   - Güney: `I2C SEVIYE DONUSTURUCU 5V <-> 3.3V` grubu ($y\approx 109\text{--}114\text{ mm}$) ile SDA/SCL hatları paylaşılır.
   - Batı: ESP32-C6 mikrodenetleyici grubu ($x\approx 152\text{--}163\text{ mm}$) ile I2C ve RTC_INT hatları bağlanır.
   - Kuzeybatı: Aktif çıkış deşarjı grubu ($x\le 198{,}5\text{ mm}$) ile >19,7 mm termal mesafe korunur.

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni courtyard, clearance, short, edge veya mask ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0**.
- **Osilatör Simetrisi:** $d_1 = 4{,}384\text{ mm}$, $d_2 = 4{,}381\text{ mm}$, fark: **0,003 mm** (kabul kriteri $< 0{,}05\text{ mm}$).
- **Courtyard kontrolü:** 5 eleman arasında minimum 2D aralık **0,540 mm**; çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-078-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-078-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-078-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-078-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-078-20260924/verify.py)
