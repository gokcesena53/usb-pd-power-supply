# USB-C giriş ESD koruması

Tarih: 2026-09-11

## Uygulanan tasarım

USB-C konnektörü J1'in dışarıya açık VBUS, CC1, CC2, D+ ve D- uçlarına ESD koruması eklendi. USB2 veri hatları düşük kapasitanslı bir diziyle; 28 V USB-PD hattı ve CC hatları ise 28 V sürekli çalışma gerilimli çift yönlü TVS elemanlarıyla korunuyor.

| Ref | Parça | Korunan hat | Temel değerler | Footprint |
|---|---|---|---|---|
| U9 | Texas Instruments TPD4E05U06QDQARQ1 | USB_DP, USB_DM | 5.5 V VRWM, 0.5 pF/kanal, IEC 61000-4-2 ±12 kV temas / ±15 kV hava | `USB_ESD:antmicro_tpd4e05u06qdqarq1` |
| D3 | Littelfuse AQ3130E-01ETG | USB_VBUS | çift yönlü, 28 V VRWM, 0.30 pF tipik, IEC ±30 kV temas/hava | `Diode_SMD:D_SOD-882` |
| D4 | Littelfuse AQ3130E-01ETG | USB_CC1 | çift yönlü, 28 V VRWM, 0.30 pF tipik, IEC ±30 kV temas/hava | `Diode_SMD:D_SOD-882` |
| D5 | Littelfuse AQ3130E-01ETG | USB_CC2 | çift yönlü, 28 V VRWM, 0.30 pF tipik, IEC ±30 kV temas/hava | `Diode_SMD:D_SOD-882` |

TPD4E05U06'nın kalan iki kanalı kullanılmıyor ve KiCad'de açıkça NC işaretli. Bunlar CC hatlarına bağlanmadı. Parçanın 5.5 V VRWM değeri, 28 V VBUS'un CC pinine mekanik kısa devre olasılığıyla uyumlu değildir.

AP33772S datasheet'i CC1/CC2 ile komşu yüksek gerilim pini arasındaki kısa devreler için 34 V'a kadar dahili koruma bildiriyor. D4 ve D5'in 28 V VRWM seçimi bu özelliği bozmaz; normal 28 V girişte TVS iletime geçmez.

## Bağlantı tablosu

| Koruma pini | Bağlantı | Net |
|---|---|---|
| U9 pin 1, D1+ | USB2 veri hattı | USB_DP |
| U9 pin 2, D1- | USB2 veri hattı | USB_DM |
| U9 pin 3 | ESD dönüşü | GND |
| U9 pin 8 | ESD dönüşü | GND |
| U9 pin 4, 5, 6, 7, 9, 10 | Kullanılmıyor | NC |
| D3 pin 2 | USB-C güç girişi | USB_VBUS |
| D3 pin 1 | ESD dönüşü | GND |
| D4 pin 1 | Configuration Channel 1 | USB_CC1 |
| D4 pin 2 | ESD dönüşü | GND |
| D5 pin 1 | Configuration Channel 2 | USB_CC2 |
| D5 pin 2 | ESD dönüşü | GND |

D3, D4 ve D5 çift yönlü TVS olduğundan iki terminal arasında anot/katot yön şartı yoktur; tabloda gösterilen pin numarası şematik ve footprint net eşleşmesini tanımlar.

## PCB yerleşim şartları

Koruma elemanları J1'in hemen arkasına yerleştirilmelidir. Konnektörden koruyucuya giden iz, koruyucudan devam eden sistem izinden önce gelmelidir. GND dönüşleri kısa ve geniş tutulmalı, her koruyucunun yanında doğrudan GND düzlemine via kullanılmalıdır. USB_DP ve USB_DM diferansiyel çiftinin U9 üzerinden geçişinde stub bırakılmamalı ve çift geometrisi korunmalıdır.

## Doğrulama

- KiCad 10.0.5 ERC: **0 hata, 0 uyarı**.
- Önceki şematikte bulunan bütün bileşenlerin pin-net grupları otomatik karşılaştırıldı: değişiklik yok.
- Yeni referanslar yalnızca D3, D4, D5 ve U9.
- U9 sembol pin tablosu ve 1–10 footprint pad kümesi otomatik doğrulandı.
- USB_VBUS, USB_CC1, USB_CC2, USB_DP, USB_DM ve GND net eşleşmeleri netlist üzerinden doğrulandı.

## Kalan mühendislik sınırı

AQ3130E-01ETG'nin datasheet klemp değeri 1 A'da tipik 39 V, maksimum 44 V'tur. AP33772S VCC mutlak maksimumu 34 V, VOUT/ISENP mutlak maksimumu 31 V olduğundan D3, IEC ESD akımını toprağa yönlendirir ancak uzun süreli surge veya kablo kaynaklı aşırı gerilim için tek başına mutlak maksimum garantisi vermez. Seri yol empedansı, parazitik endüktans ve gerçek PCB yerleşimiyle IEC 61000-4-2 sistem testi yapılmalıdır. Daha uzun enerjili surge şartı varsa VBUS'a ayrıca uygun bir surge-stopper/eFuse kademesi gerekir.

## Kaynaklar

- Texas Instruments, TPD4E05U06-Q1 datasheet: https://www.ti.com/lit/ds/symlink/tpd4e05u06-q1.pdf
- Littelfuse, AQ3130E-01ETG datasheet: https://www.littelfuse.com/assetdocs/littelfuse-tvs-diode-array-aq3130e-01etg-datasheet?assetguid=f74c18ee-03bb-4555-9ff2-5486f45a66ee
- Diodes Incorporated, AP33772S datasheet: `datasheets/AP33772S.pdf`

