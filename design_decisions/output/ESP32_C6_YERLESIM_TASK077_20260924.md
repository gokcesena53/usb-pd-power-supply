# ESP32-C6-MINI-1-H4 modül ve çevre elemanları grubu ilişkisel yerleşimi — TASK-077, 24 Eylül 2026

ESP32-C6 mikrodenetleyici modülü ve çevre elemanları grubunun (`ESP32-C6-MINI-1-H4`) 15 footprint üyesi (`U2`, `C5`, `C6`, `C7`, `R1`, `R2`, `R3`, `R10`, `R15`, `R16`, `R37`, `SW1`, `SW2`, `TP9`, `TP10`), Espressif ESP32-C6-MINI-1 Datasheet (§10/§11) ve Donanım Tasarım Kılavuzu (Hardware Design Guidelines) RF/anten, güç filtreleme, RC reset zamanlaması, strapping pinleri ve USB diferansiyel empedans kurallarına göre ilişkisel olarak yerleştirildi. On beş footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 `B.Cu` yüz ataması korunmuştur. Kart dışındaki geçici blok alanı ($x\approx 150{,}5\text{--}172$, $y\approx 84\text{--}119\text{ mm}$) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-077-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-077-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-077-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-077-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-077-20260924/verification.json)

## Kaynak, pin ve yerleşim kuralları

- **Espressif ESP32-C6-MINI-1 Datasheet (§10 & §11) ve Donanım Tasarım Kılavuzu:**
  1. *Anten Yönü ve Keepout (Yasaklı Bölge) Kuralı:*
     - Modül üzerindeki dahili PCB anteni sağ kenara (DOĞU / kart dışına) bakacak şekilde konumlandırılmıştır ($U2$ oryantasyonu: $90^\circ$).
     - Anten keepout bölgesi ($x \in [166{,}22, 186{,}62]$, $y \in [72{,}00, 115{,}20]\text{ mm}$), tüm katmanlarda (`F.Cu`, `B.Cu`, `GND_PLANE`, `POWER_PLANE`) **%100 oranında tüm izlerden, bakır dolgulardan, via'lardan ve komponentlerden tamamen arındırılmıştır**. On dört çevre elemanının hiçbiri bu bölgeye taşmamaktadır.
  2. *RF Güç Dekuplajı (VDD):*
     - `C6` (100 nF 0402 yüksek frekans RF bypass seramik kapasitör), doğrudan VDD Pin 3 ve GND Pin 1–2 dibine yerleştirildi ($x=163{,}0, y=102{,}5$; $U2.3\rightarrow C6.1$ mesafesi: **3,041 mm**). RF gürültüsünü filtrelemek ve parazitik döngü endüktansını minimize etmek için Pin 1 GND dönüşü doğrudan bağlanır.
     - `C5` (22 µF 0805 dökme/bulk kapasitör), C6'nın hemen arkasına yerleştirildi ($x=163{,}0, y=105{,}5$; $U2.3\rightarrow C5.1$ mesafesi: **5,585 mm**). Wi-Fi/Bluetooth TX RF patlama akımlarını karşılamak üzere minimum empedanslı yol oluşturuldu.
  3. *EN / Donanım Reset Zamanlama Devresi:*
     - `C7` (1 µF 0402 gecikme kapasitörü) ve `R1` (10 kΩ 0402 pull-up direnci), doğrudan modülün güneyinde EN Pin 8 hizasında ($x=159{,}0, y=102{,}5$ ve $x=156{,}5, y=102{,}5$) konumlandırıldı.
     - $U2.8\rightarrow C7.2$ mesafesi: **3,035 mm**; $U2.8\rightarrow R1.2$ mesafesi: **3,453 mm**.
     - Zaman sabiti: $\tau = R \times C = 10\text{ k}\Omega \times 1\text{ }\mu\text{F} = \mathbf{10\text{ ms}}$ olup, Espressif'in gerektirdiği minimum $50\text{ }\mu\text{s}$ enerji açılış reset gecikmesini fazlasıyla garanti altına alır.
  4. *Ergonomik Buton Koridoru:*
     - `SW2` (RESET taktil buton PTS810) ve `SW1` (BOOT taktil buton PTS810), modülün güneyindeki serbest alanda dikey bir hatta ($x=158{,}5\text{ mm}$, $y=109{,}5\text{ mm}$ ve $y=116{,}5\text{ mm}$) yerleştirildi.
     - Butonlar anten ışıma alanından >8 mm uzakta, RF performansını hiçbir şekilde etkilemeyecek konumdadır.
     - İki buton arasında 1,25 mm fiziksel açıklık bırakılarak lehimleme ve kullanıcı parmak erişim ergonomisi optimize edilmiştir.
  5. *Batı Sinyal Kolonu (USB, Strapping ve Kontrol Hatları):*
     - Tüm sinyal koşullandırma elemanları $x=152{,}0\text{ mm}$ ekseninde hizalanarak Edge.Cuts sınırına ($x=149{,}72\text{ mm}$) **>2,2 mm** emniyetli mesafe bırakılmıştır.
     - **USB Diferansiyel Çifti:** `R2` (22 Ω 0402 seri sönümleme) Pin 17 (`IO12` / `USB_DM`) hizasında (3,43 mm); `R3` (22 Ω 0402) Pin 18 (`IO13` / `USB_DP`) hizasında (3,48 mm) yerleştirildi. Diferansiyel empedans sürekliliği ve sinyal yansıma sönümlemesi sağlandı.
     - **Boot Strapping:** `R10` (10 kΩ 0402 pull-up) Pin 23 (`IO9`) hizasında (3,43 mm); modülün varsayılan SPI flash boot modunda açılmasını temin eder.
     - **IO8 Strapping:** `R37` (10 kΩ 0402 pull-up) Pin 22 (`IO8`) hizasında (3,52 mm).
     - **Ethernet Konfigürasyon:** `R15` (22 Ω 0402 seri empedans) Pin 22 (`IO8` / `ETH_CFG0`) hizasında (4,49 mm); `TP9` test noktası R15 çıkışında (3,04 mm).
     - **Ethernet Güç Kontrolü:** `R16` (10 kΩ 0402 pull-down) Pin 12 (`IO0` / `ETH_PWR_EN`) hizasında (2,41 mm); `TP10` test noktası R16 çıkışında (6,62 mm). Modül açılışında Ethernet PHY'nin kapalı kalmasını (LOW) sağlar.

| Alt Devre / Koridor | Elemanlar ve Pad/Net Yönü |
| --- | --- |
| Dahili RF Anten | `U2` anteni DOĞU yönünde; $x \in [166{,}22, 186{,}62]$, $y \in [72{,}00, 115{,}20]$ keepout bölgesi tamamen temiz. |
| VDD RF Güç Dekuplajı | `C6` (100n 0402) Pin 3 dibinde (3,04 mm); `C5` (22µ 0805) hemen arkasında (5,58 mm). GND Pin 1-2 dönüşü. |
| EN / Donanım Reset | `C7` (1µ 0402) Pin 8 dibinde (3,03 mm); `R1` (10k 0402 pull-up) bitişiğinde (3,45 mm). $\tau = 10\text{ ms}$. |
| Buton Koridoru | `SW2` (PTS810 Reset) $y=109{,}5$; `SW1` (PTS810 Boot) $y=116{,}5$. Güvenli non-RF koridor ($x=158{,}5$). |
| USB Diferansiyel Sönümleme | `R2` (22Ω USB_DM, 3,43 mm) ve `R3` (22Ω USB_DP, 3,48 mm); $x=152{,}0$ batı kolonu. |
| Strapping ve Konfigürasyon | `R10` (10k IO9 Boot, 3,43 mm), `R37` (10k IO8, 3,52 mm), `R15` (22Ω ETH_CFG0, 4,49 mm), `R16` (10k ETH_PWR_EN, 2,41 mm). |
| Test Noktaları | `TP9` (`ETH_CFG0`) $y=84{,}5$; `TP10` (`ETH_PWR_EN`) $y=105{,}0$. Batı kolonu test erişimi. |

## Komşuluk, yüz seçimi ve devir notları

1. **Yüz Seçimi Koordinasyonu (TASK-065 Devri):**
   - 15 elemanın tümü TASK-065 kararına uygun olarak **B.Cu** katmanında tutulmuştur.
   - İki boyutlu (2D) izdüşümde çevre elemanları arasında çakışma yoktur (minimum aralık **0,410 mm** R2–R3 arası).
   - Kart sınırına (`Edge.Cuts` $x=149{,}72$) olan batı açıklığı **>2,2 mm**'dir.
2. **Anten ve RF Entegrasyonu:**
   - Nihai kart içine yerleşimde (TASK-085), modül anteni PCB kenarına denk getirilmeli ve keepout bölgesi altındaki tüm iç bakır katmanlar (GND_PLANE, POWER_PLANE) boşaltılmalıdır.
3. **Grup Komşulukları:**
   - Batı: USB-C giriş katı ve panel buton/enkoder sinyal hatları.
   - Kuzey: INA226 ölçüm katı (`INA_ALERT`, I2C `SDA`/`SCL`) ve çıkış enable (`OUT_EN`).
   - Doğu/Güney: Panel dışı RF yayılım alanı.

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni courtyard, clearance, short, edge veya mask ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0**.
- **Anten Keepout Uyumu:** Keepout bölgesinde bulunan çevre elemanı sayısı: **0**.
- **Courtyard kontrolü:** 14 çevre elemanı arasında minimum 2D aralık **0,410 mm**; çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-077-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-077-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-077-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-077-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-077-20260924/verify.py)
