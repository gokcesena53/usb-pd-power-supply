# Firmware gereksinimleri (REV_C)

Donanımın firmware'den beklediği davranışlar. Kaynak: `design_decisions/USB_PD_REV_C_tasarim_kararlari_handoff.md`
Bölüm 4 ve 22.09.2026 şema değişiklikleri. Uygulama işleri `backlog/` altındaki `firmware` etiketli
görevlerde izlenir; bu doküman değiştiğinde ilgili görevin kabul kriterleri de güncellenir.

## 1. Pinler ve bus

- **OUT_EN = GPIO6 (MTCK)**; açılışta low. ESP32 reset/boot boyunca GPIO6 zayıf pull-up'ına karşı
  R61 4k7 U12'yi kapalı tutar.
- **UART0 (GPIO16 TX / GPIO17 RX) Ethernet köprüsüne ayrıldı** (23.09.2026): J8 üzerinden
  CH9121'in kanal 1'ine (RXD1/TXD1) gider. TP11/TP12 aynı netlerde tap olarak kalır.
  Loglar USB-Serial/JTAG üzerinden akmaya devam eder; UART0'a konsol bağlanmaz.
- **I2C tek bus**: GPIO18 SCL / GPIO19 SDA, R4/R7 4k7.

  | Cihaz | Adres |
  | --- | --- |
  | AP33772S | 0x52 |
  | INA226 | 0x40 |
  | BQ32000 | 0x68 |

- INA226 ALERT → GPIO3 (yalnız okuma; EN düğümü değil).
- Ekran: ST7789V2 240x320, 4 telli SPI: SCLK GPIO4, MOSI GPIO5, **CS GPIO14**,
  **DC GPIO7**, RST GPIO15; TFT_BL_PWM (GPIO1) aktif-yüksek PWM.
- **ETH_CFG0 = GPIO8** (strapping, R15 22 Ω seri): CH9121 CFG0 girişi. High = normal mod,
  low = yapılandırma modu. R37 10k pull-up boot boyunca high tutar, yani ESP32 reset'teyken
  modül normal modda kalır. **Firmware GPIO8'i boot tamamlanmadan sürmemeli**; varsayılanı high.
- **ETH_PWR_EN = GPIO0** (R16 10k seri, Q8 gate): Ethernet modülünün 3,3 V beslemesini
  kesen P-kanal yüksek-yan anahtarı. **Aktif-LOW: GPIO0 low = modül açık.** GPIO0 reset/boot
  boyunca yüksek empedans olduğu için R17 100k Q8'i kapalı tutar — modül açılışta kapalıdır.
  Açılma ~3 ms (C21 yumuşak kalkış), kapanma ~30 ms; firmware kapattıktan sonra PDO
  geçişine başlamadan önce ≥50 ms beklemeli.
- **CH9121 RST1 pini bağlı değil.** Reset gerektiğinde ya güç kesilir ya da yapılandırma
  modunda `0x02` (chip reset) / `0x0e` (execute + reset) komutu gönderilir.
- CH9121 RUN çıkışı **hiçbir GPIO'ya bağlı değil**, yalnız TP14 pedinde. Bağlantı durumu
  firmware'de keepalive/zaman aşımı ile izlenir.
- **Modülü kapatmadan önce GPIO16 (UART_TX) ve GPIO8 (CFG0) low yapılmalı.** Bu pinler
  CH9121'e seri dirençsiz/10k üzerinden bağlıdır; modül beslemesizken yüksek sürülürse
  akım ESD klemplerinden modülün 3V3 rayına akar, modül yarı beslenir ve güç kesme
  hiçbir işe yaramaz. Açma sırası: GPIO8 high (normal mod) → GPIO0 low (güç) → link bekle.
- Modül **ESP32-C6-MINI-1-H4** (23.09.2026): IO10/IO11 dışarı verilmiyor, bu yüzden
  CS GPIO10 -> GPIO14 ve DC GPIO11 -> GPIO7 taşındı. Kullanılan GPIO: 0-9 ve 12-23;
  **boş GPIO kalmadı**. Strapping: GPIO4/5/8/9/15.

## 2. RTC (BQ32000)

- Trickle charge: TCHE=0x5, TCH2=1, TCFE=1.
- Her tam güç kaybından sonra VCC ≥1 ms (datasheet 8.2.2.3).

## 3. PD ve çıkış sırası

- VSELMIN boot sonrası ≤3.2 V yapılmalı.
- 5 V altı yalnızca PPS; istek APDO minimumunun altındaysa gönderilmez.
- **Çıkış açma:** OUT_EN high → ≥25 ms bekle → INA226 ile doğrula.
- **Voltaj değiştirme:** OUT_EN low → PDO/APDO isteği → PS_RDY → doğrula → kullanıcı onayı → OUT_EN high.
- **Gerilim düşürürken deşarjı bekle:** OUT_EN low olunca Q6/R67 (1 kΩ) çıkışı donanımla boşaltır;
  firmware kontrol etmez. OUT_EN'i yeni gerilimle açmadan önce INA226 Vbus hedef gerilimin altına
  inmiş olmalı (LM74801 ters akımı engellediği için aksi halde çıkış eski gerilimde kalır).
  Beklenen süre: 1000 µF yükte 28 → 5 V ~1,7 s. Vbus ~2 V altında yavaşlar (Q6 eşiği, R59 100k).
- **Dış kaynak uyarısı:** OUT_EN low sonrası Vbus 100 ms içinde %5'ten az düşerse OUT_POS'a dış
  kaynak bağlıdır; "harici kaynak bağlı" uyarısı göster, çıkışı açma. Deşarj kapatılamaz: R67
  30,4 V'ta sürekli 0,92 W harcar (`design_decisions/output/CIKIS_DESARJI_20260923.md`).
- INA226 akım okumasında çıkış açıkken R59 (100k) kaynaklı ofset: V_OUT / 100 kΩ (28 V'ta 0,28 mA);
  isteğe bağlı olarak firmware'de çıkarılabilir.
- Fixed PDO geçişlerinde Accept–PS_RDY arası tüketim ≤2.5 W. Ethernet modülünün ~0,66 W'ı
  **Q8 ile kesilir**: geçişten önce UART/CFG0 low → GPIO0 high (modül kapalı) → ≥50 ms bekle
  → PDO isteği → PS_RDY → GPIO0 low. Bedeli: modül yeniden açıldığında link ve TCP oturumu
  2–4 s içinde kurulur. Gerilim değişimi PPS/APDO ile yapılabiliyorsa standby kuralı
  bağlamaz ve modül kesilmez — tercih edilen yol budur (TASK-056).
- PDO/APDO isteklerinde çalışma akımı ≤3 A (maksimum çıkış akımı 3 A,
  `design_decisions/output/CIKIS_AKIMI_3A_KARARI_20260922.md`); AP33772S OCP eşiği buna göre.
- Çıkış gerilimi tavanı 28 V (`design_decisions/output/CIKIS_GERILIMI_28V_TAVANI_20260922.md`).
- Hard Reset / detach interrupt → OUT_EN hemen low.
- AP33772S FAULT izlenir; UVP'de yeniden pazarlık. PPS'te 20 mV adımlarla kablo düşümü kompanzasyonu.

## 4. INA226 ve koruma

Register haritası INA228'den tamamen farklı; sürücü yeniden yazılmalı.

| Adres | Register |
| --- | --- |
| 00h | Configuration |
| 01h | Shunt voltage |
| 02h | Bus voltage |
| 03h | Power |
| 04h | Current |
| 05h | Calibration |
| 06h | Mask/Enable |
| 07h | Alert limit |

5 mΩ şönt, 3 A maksimum için ayar (hesap: `design_decisions/output/CIKIS_AKIMI_3A_KARARI_20260922.md`):

- Current_LSB 125 µA, Power_LSB 3.125 mW
- 05h = 0x2000 (CAL 8192)
- 07h = 0x1B58 (SOL 3.5 A)
- 06h = 0x8001 (SOL + LEN, APOL=0, CNVR=0)

Koruma davranışı:

- ALERT mandallıdır (06h LEN=1) ve U13 üzerinden U12 EN'i donanımla keser. Aşırı akımdan sonra
  çıkışı yeniden açmak için: OUT_EN low → 06h oku (ALERT bırakılır) → normal açılış sırası.
- Ters akım donanımda U12 LM74801 DGATE ile kesilir; firmware INA226'nın işaretli akımını izler,
  ters akımda OUT_EN'i low yapar (yedek katman).
- Bus OV donanım yedeği LM74801 OV: R55 237k / R56 10k → 30.4 V (29.5–31.3 V).
- Enerji/şarj sayacı (mAh, Wh) firmware'de integralle tutulur; INA226'da donanım biriktirici ve
  die sıcaklık sensörü yok.

## 5. Ethernet (CH9121, J8)

Waveshare 2-CH UART TO ETH modülü mezanin olarak bağlıdır. **Bir IP arayüzü değildir**:
şeffaf UART↔TCP köprüsüdür, en fazla 2 eşzamanlı soket ve her biri önceden sabitlenmiş
(IP, port, rol) çiftine bağlı. ESP32 kablolu taraftan ping'lenemez, DNS/mDNS göremez,
çalışma anında rastgele bir cihaza bağlantı açamaz.

- Yalnız kanal 1 kullanılır (TXD1/RXD1). TXD2/RXD2/DIR1/DIR2/RST1/RESET ve 5V bağlı değil.
- **Ayarlar kalıcıdır.** Yapılandırma sırası (CH9121 Serial control instruction set v2.0):
  CFG0 low → parametre komutları (`0x57 0xab <kod> <veri>`) → **`0x0d` EEPROM'a kaydet** →
  `0x0e` uygula + reset → CFG0 high. `0x0d` gönderilmezse ayarlar yalnız o oturumda geçerlidir.
  Kaydedildikten sonra güç kesilip verilse bile yeniden yapılandırma gerekmez.
- **CFG0 ile yapılandırma sabit 9600 bps'tedir.** Firmware UART0'ı yapılandırma için 9600'e
  düşürüp sonra çalışma hızına (hedef 921600) geri almalı.
- EEPROM yazma ömürlüdür: her açılışta değil, yalnız ayar değiştiğinde `0x0d` gönderilmeli.
- Baud 300 bps – 921,6 kbps; bant genişliği ~90 kB/s.
- Fabrika varsayılanı: IP 192.168.1.200, baud 9600 — ilk kurulumda değiştirilecek.
- Uygulama görevi: TASK-055. Numune doğrulaması: TASK-053.
