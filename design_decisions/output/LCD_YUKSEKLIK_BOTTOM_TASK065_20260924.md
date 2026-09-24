# LCD yüksekliği ve alt yüz seçimi — TASK-065, 24 Eylül 2026

58 footprint F.Cu'dan B.Cu'ya alındı. AOZ1284 ve TPS55340 blokları bütünüyle
alt yüzde; düşük profilli backlight devresi J3 ile üst yüzde kaldı. Şema,
BOM, ped netleri, grup üyelikleri, J3/J9/H1–H4 ankrajları ve kart dış hattı
korundu. Bloklar TASK-067'deki geçici kart dışı yerleşimdedir; bu karar
nihai kart yerleşimini veya tamamlanmış güç routing'ini temsil etmez.

## J3, LCD boşluğu ve tolerans

Kaynak: [KLS1-242I üretici çizimi, sayfa 1, SECTION A-A](../../hardware/datasheets/KLS1-242I.pdf),
2018-03-10; ölçü çizimi görsel olarak kontrol edildi.

- **h_J3 = 2,00 ± 0,15 mm**; kapalı gövde maksimumu 2,15 mm. Açık kapak 3,1 mm.
- TASK-064'ün J3 yüksekliğine dayanan nominal 2,00 mm boşluğu, toleranslı
  montajda konnektörü sıkıştırmamak için tek başına yeterli değildir.
  **Montaj tasarım hedefi 2,35 ± 0,15 mm, LCD'nin en alçak arka yüzü ile
  PCB üst yüzeyi arasında en az 2,20 mm** olarak ayrıldı. Böylece maksimum
  J3 üzerinde en az 0,05 mm açıklık kalır. Bu değer kutu/mesafe parçasına
  uygulanacak şarttır; üretilmiş veya ölçülmüş bir montaj değildir.
- J3 dışındaki parçalar için daha sıkı **1,80 mm üst yüz zarf sınırı**
  korundu: nominal h_J3 − 0,20 mm. Bu bütçe gövde, lehim oturma yüksekliği,
  parça toleransı ve bacak/lehimin toplamını kapsamalıdır. J3 istisnadır.
- J3 mekanik taşıyıcı değildir; LCD mesafe elemanlarıyla taşınır. FPC,
  LCD sabitlenmeden önce takılır ve kapak kapatılır. TASK-012'de gerçek
  boşluk, FPC kıvrımı ve gerilimsiz takılma yeniden ölçülür; z farkı
  TASK-064'teki XY hesabının fiziksel doğrulama gereğini kaldırmaz.
- TASK-064 LCD nominal izdüşümü x=63,72…141,42; y=72,48…127,52 mm.
  Betikte muhafazakâr ±0,20 mm genişletilmiş zarf kullanıldı:
  **x=63,52…141,62; y=72,28…127,72 mm**.

## Yükseklik hesabının kapsamı

KiCad'den 143 footprint'in model yolu, ölçek/ofset, yüz, açı ve koordinatı
çıkarıldı. FreeCAD/OpenCascade ile 36 farklı STEP dosyasının katı sınırları
ölçüldü. 125 footprint'in modeli var; 14 test pedi ve 4 montaj deliği
modelsiz düz PCB öğeleridir. Kırık model yolu kalmadı.

Tablodaki h, montaj yüzeyinden model z_max değeridir; **üretici maksimum
yüksekliği olarak yorumlanmaz**. Özellikle standart 1210 modeli 2,50 mm
genel zarftır; seçilen kapasitörün kesin mekanik ölçüsü değildir. Bununla
birlikte bu parçalar muhafazakâr biçimde alt yüze taşındı. TASK-061'de
datasheet zarfından üretilen L1=5,0 (maks.5,3), C33=6,5 (maks.7,0),
U2=2,4, Y1=2,5 mm gibi basitleştirilmiş modeller ayrıntılı mekanik model
yerine geçmez. Lehim, köpük sıkışması, kart eğilmesi ve kutu toleransları
numune/kutu doğrulamasına dahildir.

J9'un TASK-066 sonrası atanmış standart STEP dosyası kurulumda yoktu.
PCB model yolu `${KIPRJMOD}/libraries/Generic_Custom.3dshapes/` altındaki
basit kablo zarfına düzeltildi: 5 tel, 4,2 mm adım, Ø1,7 mm zarf,
karttan 10 mm düz çıkış; bakır uç z=-1,8 mm. **10 mm, seçilmiş bir parça
yüksekliği veya toplam kablo boyu değildir**; çıkış yönünün görsel zarfıdır.
J9'un footprint/net/konumu değişmedi; standart kütüphaneden model alanı
yenilenirse bu proje model ataması korunmalıdır.

## Yüz kararı ve ilişkili devreler

Tüm uzun parçalar ve aynı bloktaki ilişkili referanslar aşağıdaki tablolarda
yer alır. Önceden B.Cu'da olan üyeler de blok bütünlüğü kontrolüne dahildir.

| Blok | h>2 mm üyeler (mm) | Aynı yüzü paylaşan tüm referanslar | Son yüz |
| --- | --- | --- | --- |
| TPS55340 PRE-BOOST | C25=2.50, C27=2.50, C28=2.50, C29=5.80, D4=2.22, L3=4.50 | C23, C24, C25, C26, C27, C28, C29, D4, D5, L3, R47, R48, R49, R52, R53, U11 | B.Cu |
| AOZ1284 3.3V BUCK | C12=2.50, C13=2.50, C15=5.80, C16=2.50, L1=5.00 | C12, C13, C14, C15, C16, C17, C18, C19, D2, L1, R38, R39, R40, R41, R43, R50, R51, U5, U6 | B.Cu |
| USB-C GIRIS | D3=2.15, J7=3.31 | D3, D8, D9, J7, R62, R63, U10 | B.Cu |
| RTC BQ32000 + 1F5 süper kapasitör | C33=6.50, Y1=2.50 | C33, C9, R24, U4, Y1 | B.Cu |
| ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI | J8=17.50 | C10, C20, C21, J8, Q8, R17, TP14 | B.Cu |
| INA226 OLCUM + PANEL CIKISI | D7=2.15, J4=10.00 | C11, C35, D7, J4, R27, R59, R61, RShunt1, U13, U3 | B.Cu |
| AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR | C8=2.50 | C1, C2, C3, C4, C8, D1, Q3, R11, R12, R13, R14, R21, R64, R65, R8, R9, TH1, TP1, TP2, TP3, TP4, TP5, U1 | B.Cu |
| ESP32-C6-MINI-1-H4 | SW1=2.50, SW2=2.50, U2=2.40 | C5, C6, C7, R1, R10, R15, R16, R2, R3, R37, SW1, SW2, TP10, TP9, U2 | B.Cu |
| TFT BACKLIGHT | Yok | Q7, R28, R29, R60; J3 F.Cu ile birlikte | F.Cu |

Backlight artık bir DC-DC değildir: U7/L2/U8 önceki revizyonda kaldırılmıştır.
Güncel yol +3.3V → R60 → J3.2/BL_A → LCD LED'leri → J3.1/BL_K → Q7 → GND;
R28/R29 PWM kapı ağıdır. Q7/R28/R29/R60 ve J3 **F.Cu**'da kalır.

TPS55340: U11/L3/D4/C23–C29/R47–R49/R52/R53 ve FB clamp D5 B.Cu'da.
AOZ1284: U5/L1/D2/C12–C19/R38–R41/R43 ile ortak EN/V_X referansı
U6/R50/R51 B.Cu'da. Cin/Cout, SW yolu, FB/COMP aynı yüzde tutuldu.
Bu güç döngülerinin izleri henüz tamamlanmamıştır; TASK-072/073'te ve
nihai routing'de yerel güç döngüleri katman değiştirmeden bağlanmalıdır.
Rails'in diğer bloklara dağıtımı ayrı bir bağlantı konusudur.

Mevcut D5.2 → U11.9 BOOST_FB izi dört segmentiyle blokla birlikte
aynalandı; **2,584607 mm**, B.Cu, via yok. Pad merkezleri (65,069998;
57,600000) ve (66,987498; 56,640000) mm. Net/iz genişliği ve segment UUID'leri
korundu; kaydedilmiş karttan graf bağlantısı doğrulandı.

Tamamı üstteki buck/boost/USB blokları ortak eksende aynalandı; yerel
geometrileri korundu. Karışık yüzlü diğer bloklarda mevcut alt yüz üyeleri
korundu. C33'ün ankrajı gövde merkezi değil bacaktır: flip sonrası gövdesi
aynı geçici yuvada kalsın ve Y1 ile çakışmasın diye x yönünde −20 mm
ötelendi. R43 ve D7 referans yazıları bakırdan uzaklaştırıldı. D7 yazısı
geçici olarak grubun üstünde y=44 mm'dedir; nihai yerleşimde yakına alınır.

## LCD ve karşı yüze geçen bacaklar

- Şimdiki kayıtlı kartta LCD zarfında h>2 mm üst yüz gövdesi **0**;
  J3 dışındaki 1,8 mm sınırını aşan üst çıkıntı da **0**.
- J9 üstte kalan tek h>2 mm zarfıdır. Tel zarfı x=57,15…58,85 mm;
  toleranslı LCD sol sınırına en az **4,67 mm** vardır. Tel bükümü ve
  lehimler TASK-066'ya göre x=63,52 mm'nin solunda tutulmalıdır.
- SW3 PCB'de yoktur; panel parçasıdır (TASK-066). CR2032/BT1 kaldırılmıştır.
  Task metnindeki USB-C “J1” referansının güncel karşılığı **J7**'dir.
- Alt yüze alınan **C33**'ün model bacağı −3,5 mm: 1,6 mm karttan sonra
  üstte **1,9 mm** çıkar. **J8** header bacağı −6,0 mm: üstte **4,4 mm**
  çıkar. Şu an ikisi de LCD izdüşümü dışında; gelecekte taşındıklarında
  yalnız gövde yüzüne bakmak yeterli değildir.
- Nihai yerleşim/dizgi şartı: C33 ve J8 bacakları LCD zarfının dışında
  tutulmalı **veya** üstte kalan metal+lehim zarfı **≤1,5 mm** olacak
  şekilde kesilip ölçülmelidir. Böylece 1,8 mm bütçede 0,3 mm pay kalır.
  Fiziksel kesim henüz yapılmadı; modellerdeki gerçek uzun pinler gizlenmedi.
  TASK-063/078/080/085 ve TASK-015 bu koşulu devralır.
- Sayısal kontrol STEP XY sınırlarını PCB konumu/açısı/yüzüne dönüştürür;
  bottom modelin top çıkıntısını `max(0, -z_min - kart_kalınlığı)` ile
  hesaplar. XY dikdörtgen testi muhafazakârdır; eğimli kabloyu veya
  nihai kutu/montaj geometrisini simüle etmez.

## Dizgi etkisi ve sonraki yerleşim

Çift taraflı SMT gereklidir. Ağır SMT parçalar L1/L3 ve C15/C29 alt yüzde
toplandı. Dizgiciyle proses planı: önce hafif üst yüz SMT, ardından alt yüz
SMT **alt yüz yukarı bakarken** son reflow. İlk yüzdeki parçaların ikinci
ısıl çevrimde tutulması ve her parçanın sıcaklık profili dizgici tarafından
onaylanmalıdır. Proses sırası değişirse ağır parçalar için fikstür/yapıştırıcı
veya sonradan lehimleme değerlendirilir; ağırlıkları ölçülmeden lehim
yüzey geriliminin yeterli olduğu varsayılmaz.

C33 süperkapasitör, J8 modül/header ve J4/J9 kablolar SMT sonrasında
uygun THT/elle lehim prosesinde takılır. Süperkapasitör ve Ethernet
modülü için reflow uygunluğu varsayılmaz. C33/modül/kablo mekanik olarak
desteklenir; kesilen uçlar temizlenir ve LCD boşluğu ölçülür. Alt yüz
kutu mesafesi ayrıca C33 maks.7,0 mm, L1 maks.5,3 mm ve J8 model17,5 mm
zarflarıyla TASK-054/063'te kontrol edilmelidir.

TASK-069 ve grup yerleşimleri bu yüzleri başlangıç kabul eder. TASK-063
USB/RJ45 nihai sol kenar yönünü/yerini belirler; flip ile port konumu
tamamlanmış sayılmaz. Her nihai taşıma sonrası yükseklik/bacak denetimi
tekrarlanır; TASK-085/008 bunu kart yerleşimine devreder.

## Doğrulama ve kanıt

Raporlar: [task-065-20260924](../../hardware/docs/reports/task-065-20260924/).

| Kontrol | Önce | Sonra |
| --- | ---: | ---: |
| Footprint | 143 | 143 |
| Şema–PCB parity bulgusu | 0 | 0 |
| DRC ihlal toplamı | 148 | 146 |
| Courtyard / clearance / shorting | 0 / 0 / 0 | 0 / 0 / 0 |
| Bağlantısız öğe | 360 | 360 |
| Yeni DRC ihlali (tür + öğe UUID karşılaştırması) | — | 0 |
| Kırık model yolu | 1 (J9) | 0 |

146 kalan bulgu: yazı kalınlığı 63, yazı yüksekliği 63, delik aralığı 15,
J7 delikler arası açıklık 4, D10 silk/mask 1. Bu kart üretime hazır değildir.
ERC bu görevde yeniden koşturulmadı; şema değişmedi ve `pcb drc
--schematic-parity` sonucu sıfır. Top/bottom SVG'ler ve iki 3D görünüm
incelendi; bloklar halen kart dışındadır. Boy kontrolünün esas kanıtı
görsel izlenim değil STEP sınırları ve `verification.json` kontrolleridir.

- `audit.py`: KiCad envanteri ve FreeCAD STEP yüksekliği/izdüşüm denetimi.
- `inventory-before/after.json`, `heights-before/after.csv/json`: bütün parçalar;
  model yolları, konum/açı/yüz, netler ve grup bilgileri.
- `apply_sides.py`: SHA-256 ile girdiyi doğrulayan tek seferlik uygulama.
- `verify.py`, `verification.json`: net/UUID/grup/ankraj/dış hat korunumu,
  mevcut FB izi sürekliliği, yüz bütünlüğü, LCD sınırları ve DRC farkı.
- `drc-before/after.json`: KiCad 10.0 DRC raporları.
- `top.svg`, `bottom.svg`, `top-layers.png`, `bottom-layers.png`,
  `top-3d.png`, `bottom-3d.png`: kayıtlı karttan inceleme çıktıları.
- Yerel geri dönüş kopyası `before.kicad_pcb.bak` git tarafından hariç tutulur;
  önceki durumun envanteri ve hash'i raporlarda saklanır.

## Bütün parçaların model yüksekliği

“Üst çıkıntı” kartın F yüzeyinden hesaplanır. Düz ped/delik için sıfır,
takılmış bir parçanın doğrulanmış fiziksel yüksekliği anlamına gelmez.
J9/J4 kablo zarflarıdır. Yüksekliği 2 mm'yi aşanlar **kalın** yazılmıştır.

| Ref | Model h (mm) | Önce → sonra | Üst çıkıntı (mm) | LCD XY zarfıyla kesişir |
| --- | ---: | --- | ---: | --- |
| C1 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C10 | 1.250 | B.Cu → B.Cu | 0.000 | Hayır |
| C11 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C12 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C13 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C14 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C15 | **5.800** | F.Cu → B.Cu | 0.000 | Hayır |
| C16 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C17 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C18 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C19 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C2 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C20 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C21 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C23 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C24 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C25 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C26 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C27 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C28 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C29 | **5.800** | F.Cu → B.Cu | 0.000 | Hayır |
| C3 | 1.250 | B.Cu → B.Cu | 0.000 | Hayır |
| C30 | 0.500 | F.Cu → F.Cu | 0.500 | Hayır |
| C31 | 0.800 | F.Cu → F.Cu | 0.800 | Hayır |
| C32 | 0.500 | F.Cu → F.Cu | 0.500 | Hayır |
| C33 | **6.500** | F.Cu → B.Cu | 1.900 | Hayır |
| C34 | 0.500 | F.Cu → F.Cu | 0.500 | Hayır |
| C35 | 0.500 | F.Cu → B.Cu | 0.000 | Hayır |
| C4 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C5 | 1.250 | B.Cu → B.Cu | 0.000 | Hayır |
| C6 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C7 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| C8 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
| C9 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| D1 | 0.500 | B.Cu → B.Cu | 0.000 | Hayır |
| D10 | 1.260 | F.Cu → F.Cu | 1.260 | Hayır |
| D2 | 1.100 | F.Cu → B.Cu | 0.000 | Hayır |
| D3 | **2.150** | F.Cu → B.Cu | 0.000 | Hayır |
| D4 | **2.220** | F.Cu → B.Cu | 0.000 | Hayır |
| D5 | 1.110 | F.Cu → B.Cu | 0.000 | Hayır |
| D6 | 1.260 | F.Cu → F.Cu | 1.260 | Hayır |
| D7 | **2.150** | F.Cu → B.Cu | 0.000 | Hayır |
| D8 | 1.100 | F.Cu → B.Cu | 0.000 | Hayır |
| D9 | 1.100 | F.Cu → B.Cu | 0.000 | Hayır |
| H1 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| H2 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| H3 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| H4 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| J3 | 2.000 | F.Cu → F.Cu | 2.000 | Evet |
| J4 | **10.000** | B.Cu → B.Cu | 0.200 | Hayır |
| J7 | **3.310** | F.Cu → B.Cu | 0.000 | Hayır |
| J8 | **17.500** | F.Cu → B.Cu | 4.400 | Hayır |
| J9 | **10.000** | F.Cu → F.Cu | 10.000 | Hayır |
| L1 | **5.000** | F.Cu → B.Cu | 0.000 | Hayır |
| L3 | **4.500** | F.Cu → B.Cu | 0.000 | Hayır |
| Q1 | 1.200 | B.Cu → B.Cu | 0.000 | Hayır |
| Q2 | 1.200 | B.Cu → B.Cu | 0.000 | Hayır |
| Q3 | 1.080 | B.Cu → B.Cu | 0.000 | Hayır |
| Q4 | 1.200 | B.Cu → B.Cu | 0.000 | Hayır |
| Q5 | 1.080 | F.Cu → F.Cu | 1.080 | Hayır |
| Q6 | 1.200 | F.Cu → F.Cu | 1.200 | Hayır |
| Q7 | 1.200 | F.Cu → F.Cu | 1.200 | Hayır |
| Q8 | 1.550 | F.Cu → B.Cu | 0.000 | Hayır |
| R1 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R10 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R11 | 0.600 | B.Cu → B.Cu | 0.000 | Hayır |
| R12 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R13 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R14 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R15 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R16 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R17 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R2 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R21 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R24 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R27 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R28 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R29 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R3 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R34 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R35 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R36 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R37 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R38 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R39 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R4 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R40 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R41 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R43 | 0.600 | F.Cu → B.Cu | 0.000 | Hayır |
| R47 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R48 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R49 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R5 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R50 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R51 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R52 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R53 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R54 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R55 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R56 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R58 | 0.350 | F.Cu → F.Cu | 0.350 | Hayır |
| R59 | 0.450 | F.Cu → B.Cu | 0.000 | Hayır |
| R6 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R60 | 0.450 | F.Cu → F.Cu | 0.450 | Hayır |
| R61 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R62 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R63 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R64 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R65 | 0.350 | F.Cu → B.Cu | 0.000 | Hayır |
| R66 | 0.450 | F.Cu → F.Cu | 0.450 | Hayır |
| R67 | 0.600 | F.Cu → F.Cu | 0.600 | Hayır |
| R7 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R8 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| R9 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| RShunt1 | 0.600 | B.Cu → B.Cu | 0.000 | Hayır |
| SW1 | **2.500** | B.Cu → B.Cu | 0.000 | Hayır |
| SW2 | **2.500** | B.Cu → B.Cu | 0.000 | Hayır |
| TH1 | 0.350 | B.Cu → B.Cu | 0.000 | Hayır |
| TP1 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP10 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP11 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| TP12 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| TP13 | 0 (düz PCB öğesi) | F.Cu → F.Cu | 0.000 | Hayır |
| TP14 | 0 (düz PCB öğesi) | F.Cu → B.Cu | 0.000 | Hayır |
| TP2 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP3 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP4 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP5 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP6 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP7 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP8 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| TP9 | 0 (düz PCB öğesi) | B.Cu → B.Cu | 0.000 | Hayır |
| U1 | 0.760 | B.Cu → B.Cu | 0.000 | Hayır |
| U10 | 1.550 | F.Cu → B.Cu | 0.000 | Hayır |
| U11 | 1.200 | F.Cu → B.Cu | 0.000 | Hayır |
| U12 | 0.760 | F.Cu → F.Cu | 0.760 | Hayır |
| U13 | 1.550 | F.Cu → B.Cu | 0.000 | Hayır |
| U2 | **2.400** | B.Cu → B.Cu | 0.000 | Hayır |
| U3 | 1.100 | B.Cu → B.Cu | 0.000 | Hayır |
| U4 | 1.750 | B.Cu → B.Cu | 0.000 | Hayır |
| U5 | 1.550 | F.Cu → B.Cu | 0.000 | Hayır |
| U6 | 1.200 | F.Cu → B.Cu | 0.000 | Hayır |
| Y1 | **2.500** | F.Cu → B.Cu | 0.000 | Hayır |
