# Ethernet eklentisi: Waveshare 2-CH UART TO ETH (CH9121) analizi

23.09.2026. İstek: deterministik, kablolu laboratuvar ağı bağlantısı; gopo'nun lab
cihazlarıyla ETH üzerinden konuşması ve istenen parametrelerin ekrana basılması.
İncelenen modül: [Waveshare 2-CH UART TO ETH](https://www.waveshare.com/2-CH-UART-TO-ETH.htm),
CH9121, 53,0 × 22,0 mm, 3,3 V/5 V, 140 mA, 300 bps–921,6 kbps, TCP/UDP client/server.

Bu belge **karar değil**, uygulanabilirlik incelemesidir. Karar verildikten sonra
`design_decisions/output/` altında ayrı bir karar belgesi açılmalı, `CHANGES.TXT`
güncellenmeli ve `backlog/` görevleri buna bağlanmalıdır.

## Özet

Modül, gopo'ya **elektriksel ve pin olarak sığıyor** — hatta beklenenden ucuza,
çünkü UART0 (GPIO16/17) hâlihazırda yalnız TP11/TP12 test noktalarına gidiyor ve
loglar USB-Serial/JTAG üzerinden akıyor (`software/FIRMWARE_GEREKSINIMLERI.md` §1).
Yeni GPIO harcamadan TXD1/RXD1 bağlanabilir.

Buna karşılık üç gerçek engel var: (1) CH9121 bir **şeffaf seri tünel**dir, ESP32'ye
IP arayüzü vermez — "lab cihazlarına bağlanma" senaryosu bundan büyük ihtimalle daha
fazlasını istiyor; (2) modülün sürekli çektiği ~0,5 W, Fixed PDO geçişlerindeki
**2,5 W pSnkStdby bütçesini** zaten dar olan tasarımda taşırıyor; (3) 53 × 22 mm'lik
modül + RJ45, 65,9 × 40,6 mm'lik ana karta **yerleşmiyor**, mezanin/panel çözümü şart.

Zamanlama iyi: PCB'de yalnız 7 segment var (TASK-006/TASK-008 hâlâ To Do), yani
yerleşim başlamadı. Ethernet kararı verilecekse **şimdi** verilmeli.

## Karar (23.09.2026)

**Seçenek B uygulanacak:** modül ana karta mezanin olarak bağlanacak, RJ45 arka
panelden çıkacak. I²C genişletici kullanılmayacak; kontrol pinleri bugün yalnız test
noktalarına giden **IO0 ve IO8**'den alınacak.

| Sinyal | MCU pini | Yön | Neden |
| --- | --- | --- | --- |
| `UART_TX` | GPIO16 (U0TXD) | MCU → modül RXD1 | UART0 boşta; loglar USB-Serial/JTAG'de |
| `UART_RX` | GPIO17 (U0RXD) | modül TXD1 → MCU | aynı |
| `ETH_CFG0` | GPIO8, R15 22 Ω üzerinden | MCU → modül CFG0 | **strapping pini**, download boot'ta (GPIO9 = 0) high olmak zorunda, SPI boot'ta okunmaz; mevcut R37 10 k pull-up bunu sağlıyor ve CH9121'de CFG0 high = normal mod → ESP32 reset'teyken modül kendiliğinden normal modda kalıyor |
| `ETH_PWR_EN` | GPIO0, R16 10 k üzerinden | MCU → Q8 gate | **aktif-low** besleme anahtarı (aşağıdaki revizyon). RST1 bağlanmadı: `0x02`/`0x0e` yazılım reset'i var |
| RUN | — | modül → (test pedi) | GPIO'ya bağlanmıyor |

Bağlanmama gerekçeleri:

- **RUN, IO8'e bağlanamaz.** IO8 strapping pinidir; oraya modülün bir *çıkışı*
  gelirse ve modül boot anında low sürerse ESP32 açılmaz. IO8'e yalnız modül
  *girişi* bağlanabilir, bu yüzden CFG0 oraya gitti.
- **RST1 atlanmadı.** Waveshare'in kendi Pico-ETH-CH9121 kartı da MCU'ya tam olarak
  CFG0 + RST1 ikilisini veriyor; kütüphanesindeki `CH9121_Eed()` ayarları EEPROM'a
  yazıp modülü reset'liyor. Yani config'i uygulamak için reset gerekiyor, RST1
  RUN'dan önceliklidir. Link durumu firmware'de keepalive/zaman aşımıyla izlenecek.

~~Taşınan risk: CH9121'in CFG0 girişinde dahili bir pull-down varsa, R37 10 k ile
bölücü oluşup GPIO8'in boot gerilimini VIH altına düşürebilir ve ESP32 açılmaz.~~
CH9121 veri sayfasıyla kapandı: CFG girişinde **dahili pull-up** var (bkz. "Revizyon 2").
Yerine geçen, daha küçük risk modül **kapalıyken** boot'tur; aynı bölümde.

Görevler: TASK-051 (şema, **tamamlandı**), TASK-052 (numune), TASK-053 (doğrulama),
TASK-054 (yerleşim/kutu), TASK-055 (firmware sürücüsü), TASK-056 (PDO bütçesi).

Şema 23.09.2026'da `hardware/mcu.kicad_sch` sayfasına işlendi: J8 (Conn_01x07, pin
sırası ve footprint TBD), R17 10 k pull-up, C10 22 µ + C20 100 n ayırma, TP14 (RUN).
ERC 0/0, netlist farkı yalnız beklenen yedi net. UART0 netleri `UART_TX`/`UART_RX`
adında bırakıldı (sinyal gerçekten UART0'dır ve TP11/TP12 zaten bu adla etiketli);
yalnız adsız iki net `ETH_CFG0` ve `ETH_RST1` adını aldı.

## Revizyon — üretici şeması okundu (23.09.2026, akşam)

Waveshare'in modül şeması depoya eklendi (`hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf`,
Altium çıktısı, 07.08.2021). Aşağıdaki maddeler artık **ölçüm değil, belge** ile
kesinleşmiştir; bölüm 1–5'teki bazı varsayımlar bununla güncellendi.

### Kesinleşenler

| Konu | Şemadan çıkan sonuç |
| --- | --- |
| Header | **P1, "Header 8X2"**, 16 pin. 1 DIR1 / 2 DIR2 / 3 CFG0 / 4 RUN / 5 RXD1 / 6 RXD2 / 7 TXD1 / 8 TXD2 / 9 RST1 / 10 RESET / 11–12 GND / 13–14 3V3 / 15–16 5V. Pin sırası artık TBD değil; yalnız **adım ve footprint** numune işi. |
| Besleme | 5V → **AMS1117** → 3V3 → **RT9193-18** → 1V8. Header'da 5V ve 3V3 **ayrı** pinler. 3V3'ü doğrudan beslemek AMS1117'yi atlar; 5V pinleri boş bırakılır. LDO dropout sorunu yok. |
| CFG0 | CH9121 pin 60'a **doğrudan**, hat üzerinde hiçbir eleman yok. Modül kartında harici pull yok; çip içinde 30–55 kΩ pull-up var (Revizyon 2). |
| RST1 | CH9121 pin 36 (RSTI); modülde **C25 1 µF** ile GND'ye bağlı. Çip içi pull-up ile birlikte RC reset gecikmesi oluşturur (Revizyon 2). |
| RJ45 | J1'de **CTTD/CTRD orta uçları var → entegre trafo**, sinyal çiftleri izole (1,5 kVrms). Sonlandırma 4 × 49,9 R + 2 × 100 nF, orta uçlar 3V3'e. |
| RJ45 kabuğu | Pin 13/14 **doğrudan GND'ye** bağlı. Bob Smith yok, kapasitif bağ yok. |
| LED'ler | L1 güç, L2/L3 TCPCS1/TCPCS2 (TCP oturum durumu), her biri 2 k ile. RUN ayrı bir pin. |

### Sonuç 1 — ayarlar kalıcı, güç kesilebilir

CH9121 komut seti (WCH, *Serial control instruction set* v2.0):

| Komut | İş |
| --- | --- |
| `0x0d` | Parametreleri **EEPROM'a kaydet** |
| `0x0e` | Yapılandırmayı uygula + CH9121'i reset'le |
| `0x02` | Çipi reset'le |

`0x0d` gönderildikten sonra ayarlar kalıcıdır: **güç kesilip verildiğinde yeniden
yapılandırma gerekmez.** `0x0d` gönderilmezse ayar yalnız o oturumda geçerlidir.
Yapılandırma CFG0 low ile ve **sabit 9600 bps**'te yapılır (firmware UART0'ı geçici
olarak 9600'e düşürmeli). EEPROM ömürlü olduğundan `0x0d` yalnız ayar değiştiğinde
gönderilmelidir.

Ayrıca `0x02`/`0x0e` yazılım reset'i olduğu için **RST1 hattı gereksizdir** — bu,
GPIO0'ı serbest bırakır.

### Sonuç 2 — besleme anahtarı (bölüm 3'ün "asıl sorun"unu kapatır)

Modülün 3,3 V beslemesi **Q8 TSM3443CX6** (P-kanal, −20 V, RDS(on) ≤100 mΩ @ Vgs −2,5 V,
SOT-26, Özdisan 1211076, stok 2950) ile kesiliyor. 0,2 A'de düşüm 20 mV.

```
+3.3V ──┬──── Q8 S(4)          Q8 D(1,2,5,6) ── ETH_3V3 ── J8.13/14 + C10 + C20
        ├─ R17 100k ─┐
        └─ C21 100n ─┴── Q8 G(3) ── R16 10k ── GPIO0 (ETH_PWR_EN)
```

- **Aktif-low**: GPIO0 low = modül açık. GPIO0 reset/boot boyunca yüksek empedans
  olduğundan R17 Q8'i kapalı tutar → modül açılışta kapalı, arıza-emniyetli.
- Açıkken gate 3,3 × 10/110 = 0,30 V → Vgs = −3,0 V.
- C21 ile açılma zaman sabiti ≈ 0,9 ms → ~35 µF yüke giriş akımı ~60 mA (raya zararsız).
  Kapanma R17 × C21 = 10 ms, pratikte ~30 ms: firmware kapattıktan sonra PDO geçişine
  başlamadan **≥50 ms** beklemeli.
- Bütçe: 3,3 V rayı geçiş anında 0,70 A (2,31 W çıkış / ~2,8 W giriş) idi; Ethernet'in
  ~0,66 W'ı kesildiğinde ve arka ışık kısıldığında (~0,26 W) **2,5 W sınırının altına
  inilir**. Ethernet'siz tasarımın zaten sınırda olduğu gerçeği değişmiyor; eklenen
  yükün bedeli sıfırlanıyor.
- Bedeli: modül yeniden açıldığında link ve TCP oturumu **2–4 s** içinde kurulur. Bu
  yüzden gerilim değişimi PPS/APDO ile yapılabiliyorsa modül hiç kesilmemeli — PPS
  rampalarında standby kuralı bağlamıyor.

**Kritik firmware kuralı:** kapatmadan önce **GPIO16 (UART_TX) ve GPIO8 (CFG0) low
yapılmalı.** Bu pinler CH9121'e (biri doğrudan, biri 10 k üzerinden) bağlıdır; modül
beslemesizken yüksek sürülürse akım ESD klemplerinden modülün 3V3 rayına akar, modül
yarı beslenir ve **güç kesme hiçbir işe yaramaz**. Seri direnç eklemek bunu çözmez
(1 k ile bile ~2 mA sızar ve ray yüzer); çözüm pinleri low sürmektir.

### Sonuç 3 — izolasyon kısmi

Sinyal çiftleri trafo ile izole, bu iyi. **Ama RJ45 kabuk pedleri (13/14) doğrudan modül
GND'sine bağlı.** Ekranlı (STP) kablo, gopo toprağını karşı taraftaki cihazlar üzerinden
bina toprağına bağlar — çıkışı 28 V'a kadar yüzen bir tezgâh kaynağında istenmeyen bir
toprak yolu. **UTP kablo kullanılmalı**, ya da kabuk pedleri montajda ayrılmalı.
Bölüm 4'teki "kapasitif bağ olduğunu doğrulayın" maddesi böylece cevaplandı: değil.

### Şemaya işlenenler

J8 `Conn_02x08_Odd_Even` gerçek pinout ile; Q8 + R17 100k + C21 100n besleme anahtarı;
R16 22R → 10k (gate seri direnci); R17'nin eski rolü (RST1 pull-up) kalktı; RST1/RESET/
DIR1/DIR2/RXD2/TXD2/5V `no_connect`. Yeni proje sembolü
`Power_Supply_Custom:TSM3443CX6` (G=3, S=4, D=1/2/5/6 istifli). ERC 0/0.

**Montaj kararı (23.09.2026):** standoff yok; modül 2x8 header ve RJ45 tarafındaki iki
mekanik pinle (modül şemasında P2/P3, bağlantısız) ana karta doğrudan lehimlenir.
Footprint `Module_Custom:Waveshare_2-CH_UART_TO_ETH` (Waveshare ölçü çizimi): orijin
pin 1 (DIR1, dış sütun, RJ45'ten uzak köşe), RJ45 modül kenarından 4,3 mm taşar.
Header ara parçası modülü 2,5 mm yükseltir, RJ45 lehim çıkıntısı ~2,2 mm olduğu için
RJ45 pim alanında F.Cu keepout var. Mekanik pin konumu ve çıkıntı TASK-053'te
numuneyle doğrulanacak.

## Revizyon 2 — CH9121 veri sayfası: dahili dirençler (23.09.2026)

Kaynak: `hardware/datasheets/CH9121DS1.PDF` (WCH, V2.5). Pin tablosu CH9121A (LQFP64)
içindir; modüldeki çip ekin harfsiz eski **CH9121**'dir ve veri sayfasına göre pinleri
"büyük ölçüde uyumlu"dur. Pin numaraları modül şemasıyla birebir örtüşüyor
(CFG=60, RSTI=36, RESET=59, RXD1=57, RXD2=55, RUN=31).

| Pin | Tip | gopo'daki durum | Sonuç |
| --- | --- | --- | --- |
| 60 CFG | I, **PU** | `ETH_CFG0`, R37 10 k pull-up + GPIO8 | Modül açıkken iki pull-up paralel → hat yüksek. **Pull-down riski yok.** |
| 36 RSTI | I, **PU** | `no_connect` | Boş bırakmak güvenli. PU ile C25 1 µF bir RC oluşturur (aşağıda). |
| 59 RESET (fabrika ayarı) | I, **PU** | `no_connect` | Boş bırakmak güvenli; kazara fabrika ayarına dönme riski yok. |
| 57 RXD1 | I, **PU** | `UART_TX` (GPIO16) | Modül kapalıyken GPIO16 high → PU/ESD üzerinden modül rayını besler (mevcut kural doğrulandı). |
| 55 RXD2 | I, **PU** | `no_connect` | Güvenli. |
| 31 RUN, 30/33 TCPCS, 51/46 DIR, 58 TXD1 | O | TP14 / `no_connect` / GPIO17 | Çıkış; pull gerekmiyor. |

Dahili direnç RPU = RPD = **30 / 40 / 55 kΩ** (min/tip/maks). Giriş eşikleri VIH ≥ 2,0 V,
VIL ≤ 0,8 V (VCCIO = 3,3 V).

**Reset zamanlaması.** Güç verilince RSTI, 30–55 kΩ PU ile C25 1 µF üzerinden yükselir.
VIH = 2,0 V'a varış t = RC·ln(3,3/1,3) ≈ 0,93·RC = **28–51 ms**. Üstüne RSTI high →
çalışır durum tRSTTEMP1 = 11–19 ms eklenir; iç POR (tRSTTEMP3 = 25–34 ms) paralel koşar.
Yani çip ETH_3V3 yükseldikten **~40–70 ms** sonra UART komutu kabul eder. Firmware
GPIO0 low'dan sonra CFG0'ı çekip yapılandırmaya başlamadan önce **≥100 ms** beklemeli.
Yazılım reset'i (`0x02`/`0x0e`) sonrası çalışır duruma dönüş tRSTTEMP2 = 10–18 ms.

**Yeni risk — modül kapalıyken boot.** Q8 boot boyunca kapalıdır (R17). Bu sırada R37,
GPIO8 hattını CFG pininin PU'su ve ESD diyotu üzerinden **beslemesiz** ETH_3V3 rayına
bağlar: ≤0,33 mA ile ray, yükü (C25, C10, L1 güç LED'i) izin verdiği kadar yükselir ve
GPIO8 ≈ ray + bir diyot düşümünde kalır. L1 LED'i rayı ~1,8 V civarına sabitlerse
GPIO8 ≈ 2,0–2,4 V olur, ESP32-C6 VIH'inin (0,75 × 3,3 = 2,475 V) altında. Etkisi
sınırlıdır: ESP32-C6'da GPIO8 **yalnız GPIO9 = 0 iken** (Joint Download Boot) okunur;
normal SPI boot'ta "Any value". Yani ürün açılışı etkilenmez, yalnız BOOT tuşuyla
download'a girişte GPIO8 = 0 + GPIO9 = 0 geçersiz kombinasyona düşebilir. Ayrıca ROM
varsayılan olarak boot mesajlarını UART0'a da basar (EFUSE_UART_PRINT_CONTROL = 0);
bu, her açılışta GPIO16'nın RXD1 üzerinden kapalı modülü kısa süre beslemesi demektir.
Her ikisi de TASK-053'te ölçülecek.

**Güç.** Veri sayfasına göre CH9121A 100BASE-TX link + trafik 76 mA, link yokken 55 mA
(trafo dahil). Modüldeki LED'ler (RJ45 G/Y 330 Ω, L1–L3 2 kΩ) ~10 mA ekler: ≈ 0,09 A /
0,28 W. Waveshare'in 140 mA'i ve eski CH9121'in farklı olabileceği için bölüm 3'teki
0,20 A kötü durum varsayımı korunuyor; ölçüm TASK-053'te.

**Seçenek D için not.** CH9121A/T 25 MHz kristal ister, kristal kapasitörleri ve 50 Ω
Ethernet sonlandırması **çip içindedir** ("harici 49,9 Ω bağlamayın"). Waveshare
modülündeki harici 4 × 49,9 Ω ve 30 MHz osilatör eski harfsiz CH9121'e aittir; D yolu
seçilirse bu devre kopyalanmamalı.

## 1. İşlevsel uygunluk — asıl soru burada

CH9121, UART ile TCP/UDP arasında bayt köprüsüdür. Somut sonuçları:

- **En fazla 2 eşzamanlı soket**, her biri önceden yapılandırılmış sabit bir
  (IP, port, rol) çiftine bağlı. Üçüncü bir cihaza konuşmak için modülün yeniden
  yapılandırılması gerekir: CFG0 low → UART komut dizisi → reset. Bu, işlem başına
  yapılabilecek bir şey değil (dahili config belleğine yazıyor).
- **ESP32'de IP yığını yok.** Kablolu taraftan gopo ping'lenemez, DHCP/DNS/mDNS
  göremez, üzerinde web arayüzü veya LXI keşfi çalıştıramaz, kendi isteğiyle rastgele
  bir cihaza bağlantı açamaz.
- **Çerçeveleme yok.** SCPI satır sonlandırmalı olduğu için tolere edilebilir, ama
  TCP bağlantısının düştüğü yalnızca RUN pini veya keepalive zaman aşımıyla anlaşılır.
- **Bant genişliği** 921,6 kbps ≈ 90 kB/s ve her bayt bir ESP32 UART kesmesi.
  SCPI metni için fazlasıyla yeter; ekran görüntüsü/dalga formu çekmek için yetmez.
- **Determinizm**: Wi-Fi'ye göre kazanç gerçek, ama jitter kaynağı artık ağ değil,
  CH9121'in paket toplama gecikmesidir (birkaç ms, yapılandırılabilir).

Yani modül şu senaryoya uyar: *sabit IP'li bir (veya iki) cihazla, ya da bir PC/
broker ile, kalıcı bir TCP oturumu üzerinden metin alışverişi*. Şu senaryoya uymaz:
*ağdaki herhangi bir enstrümana, adresi çalışma anında seçilerek bağlanmak*.

İkinci senaryo isteniyorsa doğru parça **SPI Ethernet kontrolcüsüdür**: W5500
(donanım TCP/IP, 8 soket, ESP-IDF `esp_eth` sürücüsü) veya DM9051. Dikkat:
**ESP32-C6'da dahili EMAC yoktur**, bu yüzden LAN8720 + RMII seçeneği masada değil.
Maliyeti bölüm 2'de.

## 2. Pin bütçesi

Mevcut durum: ESP32-C6-MINI-1-H4, GPIO 0–9 ve 12–23 kullanımda, **boşta GPIO yok**
(`PARCA_TEDARIK_KARARLARI_20260922.md` §U2).

| Bağlantı | Gereken | Karşılığı |
| --- | --- | --- |
| 3V3, GND, TXD1, RXD1 | 2 GPIO | **GPIO16/17 (UART0)** — bugün yalnız TP11/TP12'de, bedava |
| CFG0 (çalışma anında yapılandırma) | 1 GPIO | yok |
| RST1 (modül reset) | 1 GPIO | yok |
| RUN (link/çalışma durumu) | 1 GPIO | yok |

Asgari bağlantı (yalnız TX/RX) **yeni GPIO istemiyor**. TP11/TP12 korunup yeni
`ETH_TX`/`ETH_RX` netlerine tap olarak bırakılmalı; köprü hata ayıklamasında gerekir.

CFG0/RST1/RUN da isteniyorsa üç seçenek:

1. **PCF8574 / TCA9534 I²C genişletici** (önerilen). I²C hattı mevcut (GPIO18/19),
   0x52/0x40/0x68 dolu, 0x20 boş. Tek ek parça, MCU değişmiyor. PCF8574'ün yüksek
   sürüşü zayıf olduğundan CFG0'a 10 k pull-up eklenip genişletici yalnız low çeker.
2. **ESP32-C6-WROOM-1'e dönmek** — IO10/IO11 geri gelir (+2 GPIO), ama TASK-041
   tersine döner ve gövde 18 × 25,5 mm'ye büyür.
3. **TFT_RST'i (GPIO15) serbest bırakmak** — ST7789V2 yazılım reset'i (0x01) var,
   RST bir RC/POR'a bağlanabilir. GPIO15 boşta idle-high olduğu için CFG0 için
   elverişli (CFG0 normal çalışmada high olmalı).

W5500 yolu seçilirse tablo değişir: SCLK/MOSI TFT ile paylaşılır ama **MISO + CS +
INT = 3 yeni GPIO** gerekir (TFT tek yönlü sürüldüğü için MISO hattı yok). MINI-1'de
mümkün değil; WROOM-1 (+2) ve TFT_RST'in serbest bırakılması (+1) ile tam tamına
çıkar. Yani W5500 kararı **aynı zamanda bir modül kararıdır**.

## 3. Güç bütçesi

Modülün 140 mA'i hangi gerilimde ölçüldüğü belirtilmemiş. Kart 3,3 V'tan beslenecek
(tasarımda regüle 5 V rayı yok: `PD_5V` AP33772S'in dahili LDO'su, `V_PRE`
pass-through'da PD_VOUT'u izleyip 28 V'a çıkıyor). Kötü durum olarak 3,3 V'ta
**0,20 A / 0,66 W** alındı; iyimser durum 0,14 A / 0,46 W.

Referans: 3,3 V rayının ölçülen tepe talebi 0,70 A (`PARCA_TEDARIK_KARARLARI_20260922.md` §L1).

| Kalem | Ethernet'siz | Ethernet'li (0,20 A) | Sınır | Sonuç |
| --- | --- | --- | --- | --- |
| 3,3 V rayı | 0,70 A | 0,90 A | — | — |
| L1 tepe akımı (FPI0705-220K) | 0,83 A | 1,03 A | IDC 2,3 A | marj 2,8 → **2,2 kat**, yeterli |
| V_PRE yükü | 0,60 A | 0,75 A | — | — |
| L3 tepe akımı (SRI0704-6R8M, 3,3 V PPS) | 1,24 A (geçici 1,5) | 1,50 A (geçici ~1,8) | IDC 3,5 A | marj 2,8 → **2,3 kat**, yeterli |
| AOZ1284 kaybı (V_PRE 27,5 V → 3,3 V, η≈0,80) | ~0,58 W | ~0,74 W | VIN 3–36 V | +0,16 W, ısıl kontrol gerekir |

**Bobinler ve buck yetiyor; hiçbir manyetik parça değişmiyor.** Tek ısıl etki
AOZ1284'te ~0,16 W artış — yerleşimde bakır alanı zaten bu yüzden planlanmalı.

### Asıl sorun: pSnkStdby

`FIRMWARE_GEREKSINIMLERI.md` §3: *"Fixed PDO geçişlerinde Accept–PS_RDY arası
tüketim ≤2,5 W."* 3,3 V rayı 0,70 A'de zaten 2,31 W çıkış / ~2,8 W giriş demek;
tasarım bu sınırı ancak Wi-Fi TX'i erteleyip arka ışığı kısarak tutturuyor.
CH9121'in ~0,66 W'ı firmware'in **kısamayacağı** bir yük: modülü kesmek için
load switch gerekir, ama kesildiğinde link düşer ve auto-negotiation ~2–3 s sürer —
"deterministik bağlantı" gerekçesiyle çelişir.

Sayısal açık ≈ 0,5–0,7 W. Arka ışığın tamamı (~80 mA @ 3,3 V = 0,26 W) atılsa bile
kapanmıyor. Üç çıkış yolu:

1. **Gerilim değişimlerini PPS/APDO ile yapmak.** PPS geçişlerinde kaynak gerilimi
   rampalar ve standby güç indirimi zorunlu değildir; kural yalnız Fixed PDO
   geçişlerini bağlar. Bir tezgâh güç kaynağı için zaten tercih edilen yol.
   Adaptör PPS desteklemiyorsa geriye Fixed kalır.
2. **Sapmayı belgeleyip ölçmek.** TASK-020 (*PD voltaj geçişlerinde 3,3 V rail ve
   UVP davranışını test et*) bu ölçümün doğal yeri; kabul kriterine hedef
   adaptörlerle Ethernet takılıyken geçiş testi eklenmeli.
3. **Ethernet'i kullanıcı seçimine bağlamak** — ETH aktifken firmware gerilim
   değişimini yalnız PPS'te sunar, Fixed'e düşmek gerekiyorsa kullanıcıyı uyarır.

Bu, Ethernet eklemenin **tek gerçek elektriksel bedeli**dir ve firmware'e yansır.

## 4. Mekanik ve RF

- Ana kart **65,9 × 40,6 mm** (Edge.Cuts). Modül **53 × 22 mm** + RJ45 gövdesi.
  Kart üstüne yerleşmez; mezanin (2,54 mm header + standoff) veya arka panele
  montaj gerekir. `3d_design/` boş olduğundan kutu henüz kısıtlı değil — karar
  kutu tasarımından önce verilmeli.
- **Anten çakışması.** MINI-1'in PCB anteni keep-out ister. Metal gövdeli RJ45 ve
  1–2 m'lik Ethernet kablosu antenin yakınında Wi-Fi menzilini düşürür. Kullanıcı
  hem Wi-Fi hem ETH istiyor. Çözüm: RJ45'i karşı kenara koyup ≥15–20 mm ayırmak,
  ya da **ESP32-C6-MINI-1U-H4**'e geçip harici anteni kutuya taşımak (aynı
  datasheet, U.FL konnektörlü varyant; footprint doğrulanmalı).
- **Toprak ve izolasyon.** Ethernet manyetikleri (1,5 kVrms) lab ağıyla gopo
  toprağı arasında galvanik ayrım sağlar — çıkışı 28 V'a kadar yüzen bir kaynak
  için bu istenen davranıştır. Waveshare sayfası RJ45'in entegre trafolu olup
  olmadığını yazmıyordu; üretici şeması J1'de CTTD/CTRD orta uçlarını gösteriyor,
  yani **trafo var** (bkz. Revizyon, "Sonuç 3" — kabuk ise doğrudan GND'de).
- **Kablo ekranı.** STP kablo + gövdesi modül GND'sine doğrudan bağlı RJ45, gopo
  toprağını bina toprağına bağlar. Kabuk bağlantısının kapasitif (1 nF/2 kV Bob
  Smith) olduğu doğrulanmalı, değilse UTP kullanılmalı.
- **ESD/yüzey akımı.** Kutudan çıkan yeni bir kablo demek; TASK-029'daki USB ESD
  testinin muadili Ethernet portu için de gerekir.

## 5. Tedarik

Özdisan indeksinde **hiçbir Ethernet parçası yok**: CH9121, W5500, RJ45 magjack
aramaları boş döndü; yalnız iki PoE PD kontrolcüsü (SI3402/SI3404) var. Yani
Ethernet hangi yoldan eklenirse eklensin ikinci kaynaktan (Mouser/DigiKey/Waveshare)
alınacak. Bu bir engel değil — ESP32-C6 ve AP33772S için emsal mevcut
(`PARCA_TEDARIK_KARARLARI_20260922.md`) — ama BOM'a ikinci bir tedarikçi ekliyor.

Modül fiyatı 12,99 $ (3+ adette 11,79 $).

**Karar (23.09.2026, TASK-052):** Modül **SAMM Market**'ten alınacak —
[ürün sayfası](https://market.samm.com/2-ch-uarttan-ethernete-donusturucu-seri-port-seffaf-iletim-modulu),
Waveshare, SAMM kodu **MP02965**, 634,89 ₺ + KDV (761,87 ₺ KDV dahil), 23.09.2026
itibarıyla stokta 19 adet. Yurt içi kaynak olduğu için Mouser/DigiKey gümrük ve kargo
yükü yok; ikinci tedarikçi yine de BOM'a ekleniyor (Özdisan'da karşılığı yok).

## 6. Seçenekler

| # | Yol | GPIO | REV_C etkisi | Ne kazandırır |
| --- | --- | --- | --- | --- |
| A | Modül **kutu dışında**, TP11/TP12 UART pedlerinden beslenip bağlanır | 0 | **yok** | Kavramı bugün doğrular, PCB'ye dokunmaz |
| B | Modül **mezanin**, header + 3,3 V + UART0 | 0 (CFG0 için +1) | header, 3,3 V bütçesi, kutu, anten | 2 soketli şeffaf tünel |
| C | **W5500** SPI kontrolcü, karta entegre | +3 | MCU değişimi (WROOM-1), TFT_RST serbest bırakma, yeni blok | Gerçek IP arayüzü, 8 soket, web/SCPI istemci |
| D | **CH9121 çipi** karta entegre (modül yerine) | 0 (+1) | yeni blok: çip + magjack + 25 MHz xtal + pasifler | B ile aynı işlev, daha derli toplu, daha çok iş |

İnceleme sırasındaki öneri "önce A, sonra B/C" yönündeydi; kullanıcı doğrudan
**B**'yi seçti (bkz. yukarıdaki Karar bölümü). A'nın doğrulama değeri kaybolmuyor:
TASK-053 numuneyi zaten kart dışında, TP9/TP10/TP11/TP12 pedlerinden sürerek
ölçecek — yalnız bu ölçüm artık B/C kararının önkoşulu değil, B'nin girdisi.

## 7. Doğrulanacaklar (numune gerektirir)

1. ~~Modül gerçekten 3,3 V'tan çalışıyor mu?~~ Şemadan: AMS1117 yalnız 5V pinlerinden
   besleniyor, 3V3 pinleri (13/14) doğrudan CH9121 rayı. Numunede yalnız çalıştırma
   testi kalıyor (TASK-053 KK#1).
2. 3,3 V'ta çekilen akım (link yokken / link varken / TX sırasında) — bölüm 3'ün girdisi.
3. ~~RJ45 entegre trafolu mu? Kabuk nasıl bağlı?~~ Şemadan: trafolu; kabuk doğrudan GND.
4. ~~CFG0/RST1/RUN pinlerinin çip içi pull yönleri~~ Veri sayfasından: CFG, RSTI, RESET,
   RXD1/2 dahili pull-up (Revizyon 2). Kalan: modül kapalıyken boot'ta GPIO8 gerilimi
   ve ETH_3V3'ün ne kadar yükseldiği.
5. Uçtan uca gecikme ve jitter (SCPI sorgu → yanıt), 921600 baud'da.
6. Kart + RJ45 + kablo, MINI-1 anteninden kaç mm uzakta Wi-Fi menzilini bozmuyor?

## Kaynaklar

- Waveshare ürün ve wiki sayfaları: <https://www.waveshare.com/2-CH-UART-TO-ETH.htm>,
  <https://www.waveshare.com/wiki/2-CH_UART_TO_ETH>
- `software/FIRMWARE_GEREKSINIMLERI.md` §1, §3
- `design_decisions/output/PARCA_TEDARIK_KARARLARI_20260922.md` (§L1, §L3, §U2)
- `hardware/datasheets/` — FPI0705-220K, SRI0704-6R8M, AOZ1284, esp32-c6-mini-1
- Özdisan indeksi (23.09.2026): CH9121/W5500/RJ45 sonuç yok
