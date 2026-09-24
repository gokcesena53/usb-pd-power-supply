# USB-C giriş grubu ilişkisel yerleşimi — TASK-070, 24 Eylül 2026

J7 (41,05;77,32; −90°; B.Cu) yerinde tutuldu. D3, D8, D9, R62, R63 ve
U10 konnektör padlerinin solundaki çıkış tarafına taşındı. Yedi footprint'in
grup üyeliği, UUID, pad/net ve B.Cu yüzü korundu. J7 henüz kart dışındaki
geçici mekanik ankrajdır; sol kart kenarı ve kutu açıklığı TASK-063'te
sonlandırılacaktır.

[Önce görünüm](../../hardware/docs/reports/task-070-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-070-20260924/after.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-070-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-070-20260924/verification.json)

## Kaynak, pin ve yerleşim kuralı

- [ST USBLC6-2 / DS4260, “How to ensure good ESD protection” ve
  Şekil 17](https://www.st.com/content/st_com/en/technical-documents/DS4260.html):
  veri, besleme ve GND yollarının parasitik endüktansını azaltmak için
  korumayı girişe yakın, dönüşü kısa tutmayı önerir. Üretici burada bu
  karta uygulanacak sayısal mm sınırı vermez.
- [THINKING SMF serisi, 2021.03, s. 1 ve 3](https://www.thinking.com.tw/upload/product/files/TVS%20Diode-SMF%20Series.pdf):
  SMF30A tek yönlüdür; gövde bandı katodu gösterir. D8.1 CC1 ve D9.1 CC2
  katot; pad2 GND anot olarak bırakıldı.
- D3 SMBJ30A için katot pad1 `USB_VBUS`, anot pad2 `GND` eşleşmesi
  TASK-009'daki footprint/silkscreen denetimiyle yeniden doğrulandı.
  Eski `USB_ESD_TASARIMI_20260911.md` belgesindeki AQ3130E/D4/D5/U9
  referansları güncel PCB'ye uygulanmadı.
- TASK-069'un tüm grupları kapsayan kaynak tablosu henüz tamamlanmadı.
  USB-C grubunun uygulanmış üretici kuralı ve ref/pin kanıtı burada tutuldu.

| Giriş ve koruma | Pad/net karşılığı ve yön |
| --- | --- |
| VBUS | J7.B4/A9 `USB_VBUS` → D3.1 katot `USB_VBUS`; en yakın pad merkezleri 5,765 mm. D3.2 GND için kısa, geniş B.Cu dönüş ve yakın via alanı ayrıldı. D3 girişe yakın TVS koludur; VBUS güç izi ve C3/Q3 yönü ayrıca çizilecek. |
| CC1 | J7.A5 `USB_CC1` → D8.1 `USB_CC1` 3,620 mm; D8.2 GND. R62.1 CC1, R62.2 GND; D8.1–R62.1 4,89 mm. Koruma J7 tarafında, AP33772S U1.17 yönü koruma sonrasında. |
| CC2 | J7.B5 `USB_CC2` → D9.1 `USB_CC2` 3,489 mm; D9.2 GND. R63.1 CC2, R63.2 GND; D9.1–R63.1 4,89 mm. U1.16 yönü koruma sonrasında. |
| D− | J7.B7/A7 `USB_DM` → U10.1 `USB_DM` 3,539 mm; U10.6 aynı netin devre tarafı. |
| D+ | J7.B6/A6 `USB_DP` → U10.3 `USB_DP` 3,537 mm; U10.4 aynı netin devre tarafı. |
| ESD dönüşü/rail | U10.2 GND ortadaki konnektör tarafı padidir; kısa GND bakırı ve doğrudan via için x≈34–35, y≈77 mm koridoru ayrıldı. U10.5 +3.3V karşı taraftadır; üretici çizimindeki VBUS bağlantısından farklı olan bu mevcut proje neti değiştirilmedi. |

U10 180° yönünde konnektöre bakan 1/3 padleri x=33,837; devreye bakan
6/4 padleri x=31,562 mm'dir. D− ve D+ U10 üstünden aynı netli karşı
padlere devam edecek; girişe uzun paralel stub eklenmemeli. J7'nin A/B
çift veri padleri konnektör footprint'inde ayrı y konumlarına sahiptir;
çifti birleştiren fan-in geometrisi nihai routing'de simetri ve açıklık
bakımından kontrol edilmelidir. [Yakın plan](../../hardware/docs/reports/task-070-20260924/after.svg)
okları **planlanan koridorları** gösterir, bitmiş bakır izi değildir.

## AP33772S ve mekanik devir

C3 mevcut (52,02;153,51) konumunda ve `PD_VBUS_SENSED` netindedir;
D3.1 ise `USB_VBUS` netindedir. Pad merkezleri 69,874 mm uzakta ve
**doğrudan aynı net değildir**. TASK-071 U1/Q3/C3 grubunu J7/D3 giriş
yönüne çevirirken bu iki neti Q3/algılama topolojisine uygun ayrı
tutmalı; C3'ü yalnızca geometrik olarak D3'e yaklaştırıp aynı bakıra
bağlamamalıdır. J7 konumu TASK-063 için sabit tutuldu, fakat bu konum
henüz sol Edge.Cuts üzerinde nihai ağız hizası değildir. TASK-063'te J7
ve koruma grubunun tümü birlikte taşınırsa ESD pad sırası ve GND dönüşü
yeniden incelenmeli.

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`: mevcut ihlaller **146→146**,
  bağlantısız öğeler **360→360**, schematic parity **0→0**. Yeni
  courtyard/clearance/short/edge/mask ihlali yok. Mevcut 146 bulgu:
  63 yazı yüksekliği, 63 yazı kalınlığı, 15 drill aralığı, J7 footprint
  içi 4 hole clearance, D10 silk/mask 1. Bağlantısız 360 öğe kartın
  tamamlanmamış routing'inin ayrı envanteridir.
- J7, J3, J9, H1–H4, D5 ve U11 konum/açı/yüz/UUID ankrajları aynı.
  Dört mevcut track UUID'si değişmedi. Hiçbir net veya şema/BOM elemanı
  değiştirilmedi.
- Kart içine son taşıma veya flip sonrasında J7 ağız hizası, kablo
  zarfı, D3 katot bandı, D8/D9 yönü, U10 veri akışı, GND via dönüşü ve
  J7'nin dört mevcut hole clearance bulgusu yeniden kontrol edilmeli.

Kanıt: [DRC önce](../../hardware/docs/reports/task-070-20260924/drc-before.json),
[DRC sonra](../../hardware/docs/reports/task-070-20260924/drc-after.json),
[doğrulama betiği](../../hardware/docs/reports/task-070-20260924/verify.py).
