# Sıfırdan yerleşim — ağırlıklı ratsnest (29 Eylül 2026)

Yöntem: `.claude/skills/kicad-placement` (IC'den dışa, blok içi → bloklar arası,
kritik pad çiftleri 10/5/1 ağırlıklı). Kullanıcı kararı: yalnız KiCad'de kilitli
parçalar (H1–H4, J3) sabit; geri kalan 139 parça sıfırdan yerleştirildi.
Rapor/görseller: `hardware/docs/reports/placement-scratch-20260929/`.

## Korunan kısıtlar

- Dış hat, footprint seçimleri, netler, katman sayısı, parça yüzleri (F/B)
  değişmedi. Yüzler LCD altı ≤1,80 mm yükseklik kararı nedeniyle korundu.
- H1–H4, J3: 0,0000 mm sapma (yeniden açılan kartla doğrulandı).
- Kenar/mekanik bağlı parçalar tek eksende serbest bırakıldı: J7 (sol kenar,
  Y 88,2–91,25), J8 J7'ye bağlı (Ethernet USB-C'nin altında, aynı panel),
  U2 (anten kart dışında, X 64,6–98), J4 (sağ kenar, Y 92–120,4). Sonuç:
  J7 Y=88,5, J8 aynı ofsette; MECH_ENC ve J9 sabit dış hat girintisiyle
  belirlendiği için taşınmadı.
- D3, D8, D9, U10, R62, R63, TP11–13 LCD izdüşümü dışında tutuldu.
- Onaylı mimari (TASK-101) bölge kısıtı olarak uygulandı: güneyde soldan sağa
  PD → boost → buck → çıkış; kuzeyde MCU, Ethernet, RTC.
- Courtyard çakışması 0 (KiCad DRC ile de doğrulandı); THT pinleri karşı yüzde
  engel sayıldı. J7 THT gövde pinleri–J8 courtyard'ı istiflenmiş port tasarımı
  gereği muaf.

## Metrik

S = Σ ağırlık × pad merkezleri arası Öklid mesafesi (mm). 88 kritik çift
(ağırlık 10: sıcak döngü/yerel dekuplaj/TVS; 5: Kelvin, FB/COMP/FREQ, kristal),
kalan bağlantılar her nette kritik bileşenler daraltılarak MST ile tamamlandı.
GND sıradan tamamlaması optimizasyonda dışlandı (iç düzlem), raporda dahil.

| | Önce | Sonra |
| --- | ---: | ---: |
| S (ağırlıklı) | 7171,1 | 4025,2 (−%44) |
| S blok içi | 5746,3 | 3196,1 (−%44) |
| S bloklar arası | 1424,8 | 829,1 (−%42) |
| L (ağırlıksız) | 2927,7 | 1960,2 (−%33) |

Kritik döngü toplamları: boost sıcak döngü 33,1 → 17,0 mm; buck giriş döngüsü
79,0 → 43,8; buck bootstrap 9,6 → 4,1; USB-C TVS/ESD 49,2 → 32,6; çıkış TVS D7
39,3 → 10,2; Kelvin (R11, RShunt1) 41,2 → 20,7; dekuplaj (30 kenar)
162,1 → 78,0 mm. Yerel arama sonucudur, global minimum iddia edilmez.

## Ödünleşimler ve belirsizlik

- Boost SW–D4 anodu 4,55 → 7,34 mm uzadı; aynı döngüde D4–C27/C28 ve
  C27/C28–PGND kısaldığı için döngü toplamı %48 azaldı. Routing'de SW bakırı
  kısa tutulmalı.
- D3.1–J7 VBUS 7,52 → 9,15 mm: sol kenar şeridi (X<63,65, LCD dışı) dar.
- C20–J8 3V3 3,48 → 4,20 mm: J8 3V3 pinleri modül altında; J8 altına parça
  konmadı (TASK-080 kanıtı olmadan courtyard istisnası yok).
- D5–U11 FB 2,09 → 2,89 mm (ağırlık 5).
- C16 (buck çıkış) için eklenen iki ağırlık-10 çift AOZ1284 yerleşim metniyle
  teyit edilmedi; belirsiz olarak işaretlidir.
- Ağırlıklı mesafe döngü alanını, dönüş yolu sürekliliğini, termal yeterliliği
  ve yönlendirilebilirliği kanıtlamaz; bunlar routing (TASK-087) ile doğrulanır.

## DRC / parite

Önce: 25 ihlal (15 copper_edge_clearance, 10 lib_footprint_mismatch),
360 bağlantısız, parite 0. Sonra: 54 ihlal = aynı 25 + 15 silk_overlap +
14 silk_over_copper (referans yazıları parçalarla taşındı), 361 bağlantısız
(D5–U11 BOOST_FB 4 segmentlik deneme yolu, iki ucu taşındığı için silindi),
parite 0.

## Güncelleme: FPC büküm yolu ve ağırlık 10/5/5 (29 Eylül 2026, TASK-118)

**Kural:** LCD FPC büküm yolu içinde top layerda komponent bulunmaz. Yol,
`LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md`'den alındı: X = 102,55 (J3 ağzı) … 142,92 mm
(büküm tepesi 142,42 + 0,5), Y = 101,05 … 117,55 mm (FPC 101,55…117,05 ± 0,50 çıkış
toleransı). Config'te `KEEPOUTS` içinde `@F` olarak tanımlı: top'taki tüm kilitsiz
parçalar ve bottom parçaların top'a çıkan THT pinleri yasak; SMD padiyle aynı
numaralı termal via padları (U11 EP) gövde pini sayılmaz.

**Ağırlık:** Kullanıcı "diğer güç/sinyal" ağırlığını 1 → 5 yaptı (`W_ORDINARY = 5`).
Bu ağırlıkla önceki yerleşimin skoru S = 10771,1.

**Uygulama:** Önceki yerleşimde 14 OUTSW top parçası ve R60 yolun içindeydi.
Sıfırdan pipeline (4 tohum) legalize edilemedi. Artımlı legal+refine ise OUTSW'yi
dağıttı (C31–U12 CAP 1,6 → 18 mm) ve reddedildi. Seçilen yöntem: OUTSW top kümesi
iç düzeni korunarak rijit (+7,0; −15,5) mm taşındı (tarama: 4 yön, 0,5 mm adım,
ceza 0 ve en düşük tel maliyeti). Ardından R60 legal, OUTSW/UI refine
(`--no-worse`) ve align uygulandı.

| | Önce | Sonra |
| --- | ---: | ---: |
| S (10/5/5) | 10771,1 | 10973,1 (+%2) |
| S blok içi / arası | 6625,5 / 4145,5 | 6814,5 / 4158,5 |
| OUTSW blok içi | 501,8 | 628,8 |
| BUCK blok içi | 966,6 | 1064,5 |
| Uzayan kritik kenar (>0,5 mm) | — | yok |
| Döngü toplamları | — | değişim ≤ %4 (buck bootstrap 4,1 → 4,3 mm) |

Artış FPC kısıtının bedeli. OUTSW, BUCK çıkışından (V_PRE) ~15 mm uzaklaştı;
BUCK iç MST'si bu yüzden büyüdü. Kilitli H1–H4/J3 yerinde, pad-net/yüz/footprint
farkı yok, parite 0, açık bağlantı 361 → 361. Serigrafi ihlali 29 → 37 (TASK-116).
Rapor: `hardware/docs/reports/placement-fpc-20260929/`.

## Güncelleme: routability terimleri (29 Eylül 2026, TASK-119)

**Sorun:** Ağırlıklı uzunluk kesişmeyi görmüyor. Örneğin bir direnci 180° çevirmek
uzunluğu değiştirmez ama via gerektirip gerektirmediğini belirler. Tek pinli IC
netlerindeki destek parçaları (R2/R3 USB seri, C23 SS) çekme hamlesi almadığı için
uzakta kalıyordu. Ölçüm (FPC sonrası yerleşim): aynı yüzde 113 kesişme, 28 via
kenarı, 10 kopuk parça (en yakın bağlı pad > 6 mm).

**Kural (kullanıcı):** Dekuplaj kondansatörü mümkün olduğunca IC ile aynı yüzde
kalır; yer yoksa karşı yüze geçebilir. Kural SMD IC pinleri için geçerli; THT
modül pini iki yüzden de erişilebilir. `legal` önce aynı yüzü tarıyor.

**Eklenen terimler (config; öneri değerleri, kullanıcı onayı bekliyor):**

| Parametre | Değer | Gerekçe |
| --- | ---: | --- |
| `W_CROSS` | 15 / kesişme | ≈ via çifti + dolanma; w5 kenarda ~3 mm |
| `W_DECAP_SIDE` | 100 / ihlal | w10 kenarda ~10 mm'ye eşdeğer |
| `W_GND_LOCAL` | 1 / mm | GND MST aramada dışarıda; bulk C ve test noktası çekimi |
| `AUTO_LOCAL` | açık | IC pini–tek pasif netleri kritik listeye `W_ORDINARY` ile girer (17 kenar, S değişmez) |
| `NO_WORSE_W` | 5 | ilk denemede R11 Kelvin 6,7 → 10,6 mm uzadı; w5 kenarlar da korunur |

**Sonuç:** Adımlar: untangle, refine (2 tohum × 200k), untangle, align. R2/R3 elle
U2 pinlerine alındı (1,5 mm).

| | Önce | Sonra |
| --- | ---: | ---: |
| S (10/5/5) | 10973,1 | 10982,7 |
| Aynı yüz kesişme | 113 | 75 |
| Via kenarı | 28 | 27 |
| Kopuk parça | 10 | 7 |
| Uzayan kritik kenar | — | yok |
| Dekuplaj yüz ihlali / flip | 0 / — | 0 / yok |

R2/R3'ün U2'ye alınması kesişmeyi 69'dan 75'e çıkardı. Bu ödünleşim, seri
direncin sürücü yanında durması için bilerek kabul edildi. Kalan kopuk parçalar:
C23 (U11 çevresinde daha yakın yasal slot yok; en yakın 7,17 mm), C33 (19 mm
süperkap), C15, R43, TP1, TP8, TP13 (yalnız GND). Rapor:
`hardware/docs/reports/placement-routability-20260929/`.

## Karar: In2 POWER_PLANE kullanımı (29 Eylül 2026)

Kullanıcı kararı: In2 (POWER_PLANE) tek bir nete ayrılmaz. Tüm güç hatları bu
katmanda bölünmüş polygonlar olarak taşınır: MAIN_5A sınıfı (USB_VBUS,
PD_VBUS_SENSED, PD_VOUT, OUT_POS), POWER_3V3 sınıfı (+3.3V, BACKLIGHT_4V2),
V_PRE ve benzerleri. In1 kesintisiz GND olarak kalır. Polygon sınırları blok
bölgelerine göre çizilecek. TASK-120'deki Freerouting denemesi In2'yi tek +3.3V
düzlemi varsaymıştı; TASK-121 bu kararla tekrarlanacak.

## Güncelleme: düzlem netleri metriği (29 Eylül 2026, TASK-122)

In2 kararı metriğe yansıtıldı. Aşağıdaki netlerin sıradan (MST) bağlantıları
iz değil, polygon/düzlem erişimi sayılıyor:
- `PLANE_NETS` = +3.3V, V_PRE, PD_VOUT, PD_VBUS_SENSED, USB_VBUS, SW_OUT, OUT_POS, ETH_3V3, PD_5V
- GND

Bu kenarlar `W_PLANE = 1` (polygon kompaktlığı; öneri değeri) ile sayılıyor ve
kesişmeye girmiyor. Aynı netlerdeki kritik kenarlar (dekuplaj, Kelvin, sıcak döngü)
gerçek iz olarak kalıyor. BOOST_SW, LX_SW ve SRC_COMMON yerel dış katman bakırı
olarak sinyal gibi sayılıyor.

| | Önce (kart) | Sonra (seed 51) |
| --- | ---: | ---: |
| S (yeni taban) | 8237,1 | 8170,0 |
| Sinyal kesişmesi | 57 | 51 |
| Via kenarı | 19 | 20 |
| Kelvin R11/RShunt1 | 20,7 mm | 20,1 mm |
| Uzayan kritik kenar | — | yok |

Metrik değişikliği tek başına, hiçbir parça taşınmadan kesişmeyi 75'ten 57'ye
indirdi (güç netleri). Kalan kesişmelerin çoğu TFT SPI (TFT_MOSI, TFT_SCLK,
TFT_DC, TFT_CS) ve ENCODER_A/B/SW netlerinde: ESP32 pin sırası J3/J9 sırasına
uymuyor. Bu, pin atamasıyla çözülecek (kullanıcı olumlu, ayrı görev).

## Karar: ESP32-C6 pin ataması (29 Eylül 2026, TASK-123)

Kalan sinyal kesişmelerinin çoğu TFT ve encoder netlerindeydi. ESP32 pin sırası J3
(TFT) ve J9 (encoder) sırasına uymuyordu. GPIO matrisiyle yeniden atandı
(kullanıcı onayı; deep-sleep uyanması yok; pull dirençleri aynen kaldı).

- **Sabit kalan pinler:** EN, GPIO0 ETH_PWR_EN, GPIO6 OUT_EN, GPIO8/9, GPIO12/13 USB,
  GPIO16/17 UART0. Açılış davranışı veya işlev nedeniyle bilinçli seçilmişlerdi.
- **Strapping padları** (GPIO4/5/15) yalnız TFT SCLK/MOSI/DC/CS/RST alabildi. Datasheet:
  "not connected or connected to high-impedance circuit". TFT tarafı yüksek empedanslı,
  kartta pull yok. GPIO15 yalnız `EFUSE_JTAG_SEL_ENABLE=1` ise etkili (varsayılan 0).
  MTDI (GPIO5) SDIO örnekleme kenarını seçer, SDIO kullanılmıyor.
- **SPI hızı:** IOMUX FSPICLK = GPIO6 (OUT_EN), bu yüzden TFT SPI zaten GPIO matrisi
  üzerindeydi. Hız sınırı değişmedi.
- **Arama:** pinswap. Yerleşim sabitken Engine.total en aza indirildi (40 rastgele
  başlangıç + açgözlü ikili değişim), sonra yeniden yerleşim yapıldı. İkinci pinswap
  turu değişiklik bulmadı.

Sonuç: sinyal kesişmesi 51 → 42 (yalnız pin değişimi) → 38 (yeniden yerleşimle),
S 8170 → 7841. Uzayan kritik kenar yok, kilitli parçalar yerinde, parite 0. Tablo:
`software/FIRMWARE_GEREKSINIMLERI.md` §1. Script: `hardware/docs/reports/placement-pinswap-20260929/pinswap.py`.

## Güncelleme: blok bazlı yeniden yerleşim (29 Eylül 2026, TASK-124)

Yöntem (LNS): `place.py anneal --inp <kart> --blocks B` yalnız seçili bloğu söker ve
bloğun mevcut ağırlık merkezinde yeniden kurar; diğer her şey sabit engeldir. Ardından
`legal --blocks`, `refine --blocks --no-worse`, `untangle`, `align` çalışır. Sıcak döngü
parçaları geçici config'te `FIXED_EXTRA` ile sabitlenir.

- **BOOST, tüm blok:** seed 71'de C23 düzeldi ama boost sıcak döngüsü 17,0 → 20,8 mm
  uzadı ve FB/COMP/FREQ kenarları uzadı → reddedildi. Seed 72'de L3 için yasal slot yok.
  Sonuç: bütün bloğu sökmek sıcak döngü için fazla yıkıcı.
- **BOOST, sıcak döngü sabit** (U11, L3, D4, C25–C28): seed 74 kabul edildi.

  | Kenar | Önce | Sonra |
  | --- | ---: | ---: |
  | C23–U11 SS | 7,01 mm | 2,68 mm |
  | R53–U11 EN | 6,72 mm | 5,25 mm |
  | R49–GND | 1,77 mm | 1,11 mm |
  | R52–COMP | 2,99 mm | 2,65 mm |
  | C24–GND | 1,58 mm | 2,64 mm |
  | D5–FB | 2,89 mm | 3,14 mm |

  C24'ün GND ucu In1 düzlemine yerel via ile iner, bu yüzden +1,1 mm kabul edildi.
  Sıcak döngü 17,0 mm aynı, kesişme 38 aynı, S 7841 → 7840.
- **PD, U1/R11/Q3 sabit:** 4 tohum denendi. Seed 82 C1/C3/C4'ü yer varken karşı yüze
  çevirdi: `W_DECAP_SIDE = 100` cezası kullanıcı kuralını ("yalnız yer yoksa") garanti
  etmiyordu. Flip artık yalnız `legal`'de, aynı yüzde yasal slot yokken denenir; refine
  ve untangle flip yapmaz. Kalan tohumlar dekuplajı %2–8 uzattı. Mevcut PD yerleşimi
  korundu.
