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
