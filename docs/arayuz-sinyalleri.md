# Kullanıcı arayüzü sinyalleri

Ekran ve enkoder ile MCU arasındaki sinyaller. Bu liste daha önce
`hardware/USER_İNTERFACE.kicad_sch` sayfasında bir not olarak duruyordu; sayfada
şematik içerik olmadığı için sayfa kaldırıldı (TASK-005) ve liste buraya taşındı.

Pin atamaları 23.09.2026'da ESP32-C6-MINI-1-H4 geçişiyle güncellendi
(`design_decisions/output/PARCA_TEDARIK_KARARLARI_20260922.md`).

## Ekran — TFT032B018 (ST7789V2, 4 telli SPI)

| Sinyal | Yön (MCU'dan) | MCU pini | Karşı uç |
| --- | --- | --- | --- |
| TFT_SCLK | çıkış | GPIO4 | J3 pin 17 |
| TFT_MOSI | çıkış | GPIO5 | J3 pin 19 |
| TFT_CS | çıkış | GPIO14 | J3 pin 18 |
| TFT_DC | çıkış | GPIO7 | J3 pin 16 |
| TFT_RST | çıkış | GPIO15 | J3 pin 20 |
| TFT_BL_PWM | çıkış (PWM) | GPIO1 | Q7 üzerinden arka ışık |

## Enkoder — L-KLS4-EC1121S-E5A-F12.5

| Sinyal | Yön (MCU'ya) | MCU pini | Not |
| --- | --- | --- | --- |
| ENCODER_A | giriş | GPIO22 | 3,3 V pull-up; kontak GND'ye kapanır |
| ENCODER_B | giriş | GPIO23 | 3,3 V pull-up |
| ENCODER_SW | giriş | GPIO21 | 3,3 V pull-up |

Firmware tarafında kuadratür çözme ve anahtar sıçrama bastırma gerekir
(`software/FIRMWARE_GEREKSINIMLERI.md`).

## Ethernet mezanin — Waveshare 2-CH UART TO ETH (CH9121), J8

Modül 53 × 22 mm'dir ve ana karta sığmaz; 2×8 header + standoff ile mezanin olarak
bağlanır, RJ45 arka panelden çıkar. Pin sırası üreticinin şemasından alındı
(`hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf`, P1 "Header 8X2"); adım (2,54 mm
varsayımı) ve footprint numune ile kesinleşecek (TASK-053).

| J8 pini | Modül sinyali | Yön (MCU'dan) | MCU pini | Seri | Not |
| --- | --- | --- | --- | --- | --- |
| 3 | CFG0 | çıkış | GPIO8 | R15 22R | high = normal, low = yapılandırma (+ TP9) |
| 4 | RUN | — | yok | — | TP14 pedi |
| 5 | RXD1 | çıkış | GPIO16 (U0TXD) | — | UART_TX (+ TP11) |
| 7 | TXD1 | giriş | GPIO17 (U0RXD) | — | UART_RX (+ TP12) |
| 11, 12 | GND | — | — | — | |
| 13, 14 | 3V3 | — | — | Q8 | ETH_3V3, anahtarlanmış 3,3 V |
| 1,2,6,8,9,10,15,16 | DIR1/2, RXD2/TXD2, RST1, RESET, 5V | — | — | — | bağlı değil |

Modül 5V pininden AMS1117 ile kendi 3V3'ünü üretir. 3V3 pinleri doğrudan beslendiği
için bu LDO atlanır ve 5V pinleri boş bırakılır.

### Besleme anahtarı

| Sinyal | Yön (MCU'dan) | MCU pini | Eleman |
| --- | --- | --- | --- |
| ETH_PWR_EN | çıkış, **aktif-low** | GPIO0 | R16 10k → Q8 (TSM3443CX6) gate, R17 100k pull-up, C21 100n yumuşak kalkış (+ TP10) |

Q8 modülün 3,3 V beslemesini keser; PD Fixed PDO geçişinde 2,5 W standby bütçesini
tutturmak için gerekli. GPIO0 reset/boot boyunca yüksek empedans olduğundan R17 Q8'i
kapalı tutar: **modül açılışta kapalıdır**. Açılma ~3 ms, kapanma ~30 ms.

GPIO8 bir strapping pinidir: boot'ta high olmak zorundadır, bu yüzden oraya modülün bir
**çıkışı** bağlanamaz. CH9121'de CFG0 high = normal mod olduğu ve mevcut R37 10k pull-up
boot boyunca high tuttuğu için CFG0 oraya bağlandı. Modülün CFG0 hattında hiçbir eleman
yoktur (doğrudan CH9121 pin 60), yani hattı belirleyen tek direnç R37'dir.

RST1 bağlanmadı: CH9121 yapılandırma modunda `0x02` / `0x0e` komutlarıyla yazılımdan
reset'lenebiliyor ve güç anahtarı zaten tam bir reset sağlıyor.

**RJ45 kabuğu modül üzerinde doğrudan GND'ye bağlıdır** (J1 pin 13/14). Sinyal çiftleri
entegre trafo ile izoledir, ama STP kablo gopo toprağını bina toprağına bağlar —
**UTP kablo kullanın**.

Besleme ayırma: C10 22u + C20 100n, ETH_3V3 üzerinde. Gerekçe ve güç bütçesi:
`design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md`.
