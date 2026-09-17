# USB-C Güç Yolu Yerleşim Güncellemesi

Tarih: 2026-09-12

## Uygulanan yerleşim

5 A ana güç yolu, kartın üst kenarında soldan sağa aşağıdaki sıraya alındı:

`J1 USB-C -> R11 -> Q4 -> Q3 -> RShunt -> J4`

| Parça | Merkez (mm) | Dönüş | Yerleşim amacı |
|---|---:|---:|---|
| R11 | 34.0, 26.0 | 0° | USB_VBUS giriş akım algılama direnci |
| Q4 | 42.1, 26.0 | 180° | PD_VBUS_SENSED padleri R11'e bakacak şekilde |
| Q3 | 50.0, 26.0 | 0° | Ortak kaynak padleri Q4'e, PD_VOUT padleri çıkışa bakacak şekilde |
| RShunt | 58.2, 26.0 | 0° | PD_VOUT ile OUT_POS arasında |
| U3 | 63.0, 35.0 | 180° | Kelvin ölçüm pinleri RShunt tarafına bakacak şekilde |

USB ESD parçaları J1 yanında tutuldu. U1 ve çevre dirençleri ana 5 A koridorunun altına yerleştirildi. Test noktaları tek sıra halinde y=41.5 mm hattına taşındı.

## Elektriksel yön kontrolü

- R11 pad 1: `USB_VBUS`; pad 2: `PD_VBUS_SENSED`
- Q4 pad 5-8: `PD_VBUS_SENSED`; pad 1-3: ortak MOSFET kaynak düğümü
- Q3 pad 1-3: ortak MOSFET kaynak düğümü; pad 5-8: `PD_VOUT`
- RShunt pad 1: `PD_VOUT`; pad 2: `OUT_POS`
- U3 pin 10: `PD_VOUT`; pin 8-9: `OUT_POS`

## Kontroller

- Taşınan 26 parçanın courtyard alanlarında 0.2 mm ek yerleşim payı ile yeni çakışma yok.
- KiCad DRC: 0 error, 94 warning.
- Kalan uyarılar yalnızca silkscreen yazı/çizgi çakışmaları ve iki yazı yüksekliği uyarısıdır; bakır kısa devresi veya clearance hatası raporlanmadı.
- Kartın alt bölümündeki J3 çevresi daha önce var olan yerleşim çakışmalarını koruyor ve ayrı bir yerleşim adımında düzeltilmelidir.

Bu güncellemede iz çizilmedi. 5 A yolunda 3 mm iz kuralı başlangıç değeridir; geniş bakır alanlar ve gerekli yerel daralmalar DRC ile denetlenerek uygulanmalıdır.
