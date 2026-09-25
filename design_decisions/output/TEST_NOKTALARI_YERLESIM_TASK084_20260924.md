# Test Noktaları Grubu (TP6–TP8, TP11–TP13) İlişkisel Yerleşimi ve 14 TP Haritası — TASK-084, 24 Eylül 2026

Test noktaları grubunun (`TEST NOKTALARI`) 6 üyesi (`TP6`, `TP7`, `TP8`, `TP11`, `TP12`, `TP13`), IPC-7351B test edilebilirlik kılavuzları, Espressif ESP32-C6 donanım tasarım rehberi, Diodes AP33772S I2C spesifikasyonu, TASK-065 yükseklik kuralları ve TASK-069 üretici kurallarına uygun olarak standart **$2{,}540\text{ mm}$ (100 mil)** prob adımıyla ilişkisel olarak yerleştirildi.

Bu görev kapsamında kart üzerindeki 14 test noktasının (`TP1`–`TP14`) tamamının elektriksel neti, ait olduğu fonksiyonel blok, ölçüm amacı ve prob yaklaşım yüzeyi eksiksiz olarak haritalandırılmış; `TEST NOKTALARI` grubunun 6 üyesi iki bağımsız teşhis hücresine (UART0 programlama portu ve I2C veri yolu sniffing hücresi) ayrılarak gürültülü güç anahtarlama hatlarından izole edilmiştir.

[Önce görünüm](../../hardware/docs/reports/task-084-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-084-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-084-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-084-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-084-20260924/verification.json)

---

## 1. Kart Üzerindeki Tüm 14 Test Noktasının Tam Haritası (AC #1)

Aşağıdaki tablo, `gopo` PCB üzerindeki 14 test noktasının tamamının net adını, devre bloğunu, montaj yüzeyini, koordinatını ve donanım doğrulama/ölçüm işlevini listeler:

| Ref | Net Adı | Devre Bloğu | Katman | Konum $(X, Y)$ (mm) | Açı | Ölçüm ve Hata Ayıklama Amacı |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`TP1`** | `USB_VBUS` | AP33772S PD KONTROLCU | `B.Cu` | $(46{,}500, 140{,}000)$ | $0^\circ$ | USB-C girişinden gelen ham VBUS gerilimi; PD voltaj geçişleri (5V/9V/12V/15V/20V) ve inrush tepe ölçümü (TASK-021). |
| **`TP2`** | `/USB_PD_CONTROLLER/PD_VBUS_SENSED` | AP33772S PD KONTROLCU | `B.Cu` | $(54{,}500, 135{,}500)$ | $0^\circ$ | AP33772S VBUS duyu gerilim bölücü çıkışı; UVLO/OVLO eşik doğrulaması. |
| **`TP3`** | `PD_VOUT` | AP33772S PD KONTROLCU | `B.Cu` | $(69{,}500, 140{,}000)$ | $0^\circ$ | Q3 anahtarlama FET'leri sonrası ana iç güç barası; TPS55340 pre-boost girişi gerilimi. |
| **`TP4`** | `PD_5V` | AP33772S PD KONTROLCU | `B.Cu` | $(52{,}000, 149{,}000)$ | $0^\circ$ | AP33772S dahili 5V LDO çıkışı ve I2C seviye dönüştürücü yüksek taraf besleme doğrulaması. |
| **`TP5`** | `/USB_PD_CONTROLLER/PD_GATE` | AP33772S PD KONTROLCU | `B.Cu` | $(61{,}000, 134{,}500)$ | $0^\circ$ | Q3 dahili güç anahtarı gate sürüş gerilimi; şarj pompası ve yumuşak açılış dinamikleri. |
| **`TP6`** | `PD_I2C_SCL_3V3` | TEST NOKTALARI / I2C | `B.Cu` | $(207{,}500, 126{,}000)$ | $0^\circ$ | 3.3V lojik I2C saat (SCL) hattı; 400 kHz Fast-mode bus dalga şekli ve yükselme zamanı ($t_r$) kontrolü. |
| **`TP7`** | `PD_I2C_SDA_3V3` | TEST NOKTALARI / I2C | `B.Cu` | $(210{,}040, 126{,}000)$ | $0^\circ$ | 3.3V lojik I2C veri (SDA) hattı; AP33772S, INA226 ve BQ32000 haberleşme paketlerini koklama (sniffing). |
| **`TP8`** | `PD_INT_3V3` | TEST NOKTALARI / I2C | `B.Cu` | $(212{,}580, 126{,}000)$ | $0^\circ$ | AP33772S aktif-düşük kesme hattı; PD takılma/çıkarılma ve arıza uyarı zamanlaması (GPIO10). |
| **`TP9`** | `/MCU/ETH_CFG0` | ESP32-C6-MINI-1-H4 | `B.Cu` | $(152{,}000, 84{,}500)$ | $0^\circ$ | CH9121 Ethernet denetleyicisi boot yapılandırma pini 0 (ESP32 GPIO0). |
| **`TP10`**| `/MCU/ETH_PWR_EN` | ESP32-C6-MINI-1-H4 | `B.Cu` | $(152{,}000, 105{,}000)$ | $0^\circ$ | Ethernet modülü güç anahtarı kontrol sinyali (ESP32 GPIO1); Q8 soft-start anahtarlama gecikmesi. |
| **`TP11`**| `/MCU/UART_TX` | TEST NOKTALARI / UART | `F.Cu` | $(207{,}500, 122{,}000)$ | $0^\circ$ | ESP32-C6 birincil seri konsol çıkışı (TXD0 / GPIO16); boot logları, CLI ve hata ayıklama. |
| **`TP12`**| `/MCU/UART_RX` | TEST NOKTALARI / UART | `F.Cu` | $(210{,}040, 122{,}000)$ | $0^\circ$ | ESP32-C6 birincil seri konsol girişi (RXD0 / GPIO17); firmware yükleme ve komut girişi. |
| **`TP13`**| `GND` | TEST NOKTALARI / UART | `F.Cu` | $(212{,}580, 122{,}000)$ | $0^\circ$ | Dijital toprak referansı; osiloskop ve mantık analizörü yaylı şasi klipsi için sıfır döngülü prob noktası. |
| **`TP14`**| `/MCU/ETH_RUN` | ETHERNET MEZANIN | `B.Cu` | $(153{,}000, 155{,}690)$ | $0^\circ$ | CH9121 Ethernet denetleyicisi çalışma durumu ve link göstergesi; mezanin dışından %100 erişilebilir. |

---

## 2. Test Noktaları Grubunun İki Alt Kümeye Ayrılması (AC #1, AC #3)

Grup üyeleri tek bir yapay/estetik sıraya dizilmek yerine elektriksel işlevlerine göre iki fonksiyonel teşhis hücresine ayrılmıştır:

1. **UART0 Programlama ve Seri Konsol Portu (`TP11`, `TP12`, `TP13` — `F.Cu`):**
   - **Konum:** $Y = 122{,}000\text{ mm}$ yatay ekseninde, $X = 207{,}500$, $210{,}040$, $212{,}580\text{ mm}$.
   - **Standart Adım:** Pedler arası merkez mesafesi tam **$2{,}540\text{ mm}$ (100 mil)**; toplam span **$5{,}080\text{ mm}$ (200 mil)**.
   - **İşlev:** Rev B'de kaldırılan 3 pinli J2 UART konnektörünün yerini alan bu 3 test pedi, harici bir USB-UART adaptörünün yaylı pogo-pin klemensiyle veya standart osiloskop problarıyla doğrudan kartın üst yüzeyinden erişilebilmesini sağlar.
   - `TP13` (GND), `TP12` (RX) ve `TP11` (TX) pinlerinin hemen yanında yer alarak ölçümlerde parazitik endüktans döngüsü oluşturmadan temiz sinyal yakalanmasını temin eder.

2. **I2C Veri Yolu ve Kesme Teşhis Portu (`TP6`, `TP7`, `TP8` — `B.Cu`):**
   - **Konum:** $Y = 126{,}000\text{ mm}$ yatay ekseninde, $X = 207{,}500$, $210{,}040$, $212{,}580\text{ mm}$.
   - **Standart Adım:** Pedler arası merkez mesafesi tam **$2{,}540\text{ mm}$ (100 mil)**; toplam span **$5{,}080\text{ mm}$ (200 mil)**.
   - **Düşey Ayrım:** UART hücresi ile I2C hücresi arasında $\Delta Y = 4{,}000\text{ mm}$ net ayrım bırakılmıştır.
   - **İşlev:** AP33772S, INA226 ve BQ32000 çevre birimlerinin tümü alt yüzde (`B.Cu`) yer aldığından, bu test noktalarının `B.Cu` katmanında tutulması gereksiz via geçişlerini önler ve bus sinyallerinin doğrudan yüzeyden prob edilmesine olanak tanır.

---

## 3. Prob Yaklaşım Kuralları, GND Referansı ve Kapalı Alan İzolasyonu (AC #2)

1. **Prob Ucu Boyutları ve Fiziksel Açıklıklar:**
   - **Test Pedi Geometrisi:** `TestPoint:TestPoint_Pad_D1.0mm` (çapı $\varnothing 1{,}00\text{ mm}$ dairesel SMD bakır ped).
   - **Prob İğnesi Uyumu:** $\varnothing 0{,}50\text{ mm}\dots \varnothing 0{,}80\text{ mm}$ sivri uçlu (needle-point) osiloskop probları, kancalı problar ve fikstür pogo-pinleri için tam uygundur.
   - **Avlu Açıklığı (Courtyard Clearance):** $2{,}540\text{ mm}$ adımda iki ped arasındaki net bakır kenar mesafesi $2{,}540 - 1{,}000 = \mathbf{1{,}540\text{ mm}}$'dir. İki komşu ped avlusu arasındaki boşluk **$1{,}515\text{ mm}$** olup IPC $\ge 0{,}50\text{ mm}$ kuralını fazlasıyla sağlar.
   - **Dikey Prob Hacmi:** Her test pedi etrafında en az $Z \ge 8{,}0\text{ mm}$ dikey açıklık bırakılarak prob kafalarının rahatça oturması sağlanır.

2. **Osiloskop GND Referans Klipsi:**
   - Yüksek hızlı dijital sinyallerde (özellikle 115200+ baud UART kenarlarında ve I2C yükselme sürelerinde) uzun timsah krokodil toprak kablosu endüktif osilasyona (ringing) sebep olur.
   - `TP13` (GND), `TP11` ve `TP12`'ye tam $2{,}54\text{ mm}$ mesafede yerleştirildiğinden, osiloskop problarının minyatür yaylı şasi klipsi (ground spring) doğrudan TP13'e basarak **sıfır endüktanslı** temiz dalga şekli yakalar.

3. **Yasaklı Alanlar ve Gürültülü Güç Koridorlarının İzolasyonu:**
   - **LCD Altı İzolasyonu:** Ekran modülü monte edildiğinde üst yüzey (`F.Cu`) LCD arkasında kalır. Bu nedenle nihai kart yerleşiminde çalışırken prob edilmesi gereken seri konsol/debug hatlarının erişilebilir kenarlarda kalması esastır.
   - **RJ45 Keepout İzolasyonu:** Modül altındaki RJ45 THT bacak çıkıntıları ($Y \ge 138{,}0\text{ mm}$) bölgesine hiçbir test noktası konulmamıştır; en yakın test noktası ($Y = 126{,}0\text{ mm}$) RJ45 yasaklı alanından **$> 12\text{ mm}$** uzaktadır.
   - **Anahtarlama Düğümleri (SW Nodes):** Test noktaları AOZ1284 LX ve TPS55340 SW gibi yüksek frekanslı ($\sim 1\text{ MHz}$), yüksek $dv/dt$ anahtarlama düğümlerine **KESİNLİKLE EKLENMEMİŞTİR**. Bu tür hatlara eklenecek test pedleri parazitik anten görevi görerek EMI yayılımına neden olur.

---

## 4. Doğrulama ve DRC Sonuçları (AC #4)

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC İhlalleri:** **145 → 145** (yeni courtyard, clearance, short, hole veya silk ihlali: **0**).
  - **Bağlantısız Öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic Parity:** **0 → 0** (şema ile netlist tam uyumlu).
- **Courtyard ve Açıklık Kontrolü:**
  - Grup üyeleri arasında minimum 2D avlu aralığı: **$1{,}515\text{ mm}$** ($\ge 0{,}45\text{ mm}$, çakışma: **0**).
- **Sabit Ankrajlar ve İzler:** `J7`, `J3` (kilitli), `J9`, `H1–H4`, `D5`, `U11` konum/açı/yüz ankrajları ve TASK-058 D5.2--U11.9 FB izi UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-084-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-084-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-084-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-084-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-084-20260924/verify.py)
