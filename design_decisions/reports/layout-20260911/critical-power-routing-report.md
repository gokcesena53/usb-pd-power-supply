# Kritik güç yönlendirme raporu

## Kapsam

Bu adımda AOZ1284PI buck yerleşimi, USB-C'den güç çıkışına uzanan ana güç yolu ve INA228 akım ölçümünün Kelvin bağlantıları düzenlendi. Diğer dijital ve kullanıcı arayüzü sinyalleri bu aşamanın kapsamında yönlendirilmedi.

## AOZ1284PI yerleşim düzenlemesi

- U5 çevresindeki L1, D2, C17, C13, C14, C15, C16, R38-R43, C18 ve C19 yeniden konumlandırıldı.
- U5 pin 1 (LX), D2 pin 1, L1 pin 1 ve C17 pin 2 kısa bir LX_SW kümesi oluşturacak şekilde toplandı.
- C17 bootstrap kondansatörü U5 pin 2 (BST) ile U5 pin 1 (LX) arasına bağlandı.
- Catch diyot dönüşü D2 pin 2 -> GND olarak kısa tutuldu ve GND düzlemine via ile indirildi.
- U5 exposed pad pin 9, PD_VOUT üzerinde bırakıldı; GND'ye bağlanmadı.
- Giriş kapasitörleri C12/C13/C14, çıkış kapasitörleri C15/C16 bağlandı.
- FSW, SS, EN, FB ve COMP ağları U5 çevresinde yönlendirildi.
- FB üst direnci R39, +3.3 V'u buck çıkış kapasitörü tarafındaki algı noktasından alıyor.

## Ana güç yolu

| Bölüm | Uygulama |
|---|---|
| USB-C VBUS çıkışı | Dört VBUS padinden 0.15 mm kısa boyunlar, ardından 0.4-0.8 mm birleşen hat |
| R11 -> Q4 | 2.0 mm F.Cu |
| Q4 -> Q3 ortak source | Paralel 1.0 mm yollar ve 0.8 mm pad birleştirmeleri |
| Q3 -> RShunt | 2.0 mm F.Cu |
| RShunt -> J4 iki pozitif terminal | 3.0 mm ana gövde, 2.0 mm dallar |

USB-C üzerindeki 0.15 mm bölümler yalnızca sık aralıklı konnektör padlerinden güvenli biçimde çıkmak için kullanıldı; akım yolu hemen genişletildi.

## Kelvin algılama

- RShunt pin 1 (PD_VOUT) -> U3 pin 10 ayrı 0.25 mm Kelvin hattıyla bağlandı.
- RShunt pin 2 (OUT_POS) -> U3 pin 8/9 ayrı 0.25 mm Kelvin hattıyla bağlandı.
- Bu yollar B.Cu üzerinden taşındı ve yüksek akım bakırından ayrı tutuldu.
- R11 pin 1 -> U1 pin 1 ve R11 pin 2 -> U1 pin 24 ayrı ince algılama yollarıyla bağlandı.

## Katman kullanımı

- F.Cu: ana güç akışı, buck sıcak döngüsü ve kısa yerel kontrol bağlantıları.
- GND_PLANE: kesintisiz ana referans/dönüş düzlemi.
- POWER_PLANE: PD_VOUT yardımcı dağıtımı.
- B.Cu: INA228 Kelvin algılama ve +3.3 V feedback algı hattı.

## Kontrol sonucu

- Courtyard çakışması: 0
- DRC hata: 0
- DRC uyarı: 0
- Zone dolguları yenilendi.
- Son DRC raporu: drc-critical-power-and-buck-final.txt

## Kalan yönlendirme

Kartın tamamı henüz bitmiş değildir. Sonraki aşamalar:

1. USB D+ / D- çiftinin U9 üzerinden R2/R3 ve ESP32-C6'ya yönlendirilmesi.
2. +3.3 V ana dağıtımı ve yerel bypass bağlantıları.
3. I2C, SPI/TFT, UART, encoder ve buton hatları.
4. Backlight boost ve TFT çıkışlarının tamamlanması.
5. Son GND stitching via turu, tüm zone'ların yeniden doldurulması ve final DRC.

