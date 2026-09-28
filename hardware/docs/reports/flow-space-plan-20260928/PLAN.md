# PCB hiyerarşi, boş alan ve montaj açıklığı planı

**Tarih:** 28 Eylül 2026  
**Durum:** İnceleme ve uygulanmamış yerleşim planı  
**Kaynak:** `hardware/gopo.kicad_pcb` — KiCad 10.0.5  
**İncelenen PCB SHA-256:** `81e4c9f16e19864cbf0ebd2b2fce5f8ca75153457234904a125ef8e253077e54`

## 1. Sonuç

Fonksiyonel gruplama büyük ölçüde korunmuş; ancak eski TASK-101 raporundaki tek seri güç zinciri güncel bağlantıları doğru göstermiyor. Çıkış güç kolu ile dahili besleme kolu ayrı planlanmalı. Boşlukları değerlendirmede ilk tercih, aynı işlevdeki parçaları yakınlaştırmak ve gerekli güç/sinyal yollarına yer ayırmak olmalı.

Bu incelemede ana PCB değiştirilmedi. Dört parçalık ilk aşama için ayrı bir aday hazırlandı. Adayın bileşenleri, değerleri, footprint kimlikleri ve pad/net eşleşmeleri ana kartla aynı. Mevcut 25 DRC ihlalinin türleri ve ilgili öğeleri de birebir korundu; yeni ihlal yok. Bu, üretime uygunluk onayı değildir.

### İncelemenin kapsamı

- 144 footprint: F.Cu üzerinde 50, B.Cu üzerinde 94; 15 mevcut KiCad grubu.
- Kartta yalnızca dört çizilmiş iz segmenti var. Kart seviyesinde bakır dolgu yok; footprint içindeki iki alan U2 ve J8 keepout'ları.
- DRC: 15 bakır–kart kenarı ihlali, 10 footprint/kütüphane uyuşmazlığı, ayrıca 360 bağlantısız öğe. Şematik parite hatası: 0.
- Dört bakır katmanın SVG çıktısı ve iki yüzün 3D görüntüsü üretildi. 3D görüntüler görsel inceleme içindir; yeni bir katı model çarpışma hesabı veya LCD ile birleşik montaj doğrulaması yapılmadı.
- Aşağıdaki bağlantı ölçüleri pad merkezleri arasındaki düz çizgi mesafesidir; yönlendirilmiş iz uzunluğu veya endüktans hesabı değildir.

## 2. Gerçek güç ve kontrol hiyerarşisi

```text
J7 USB_VBUS → R11 → PD_VBUS_SENSED
                        ├─ Kullanıcı çıkışı: Q5 → SW_OUT → RShunt1 → OUT_POS → J4
                        └─ Dahili besleme: Q3 → PD_VOUT → L3/U11/D4 → V_PRE
                                                                   ├─ U5/L1 → +3.3 V
                                                                   └─ U12 beslemesi

U1: USB-PD anlaşması ve giriş kolu kontrolü
U3 INA_ALERT + MCU OUT_EN → U13 → SW_EN
                                  ├─ U12 → Q5 kapı kontrolü
                                  └─ Q4 → DISCH_G → Q6/R67 aktif deşarj
```

Q5 giriş padleri `PD_VBUS_SENSED`, çıkış padleri `SW_OUT` ağına bağlıdır. U5'in termal/VIN pedi `V_PRE`, L1'in çıkışı `+3.3V` üzerindedir. Dolayısıyla buck, kullanıcı çıkışının seri bir aşaması değildir. Grup merkezlerinin X yönünde artması, gerçek akım yolunun doğru veya kısa olduğunu kanıtlamaz.

### Düzeltilmesi gereken önceki rapor kabulleri

1. **TASK-101 güç sıralaması:** Boost → buck → Q5 biçimindeki seri zincir yerine yukarıdaki dallanma kullanılmalı.
2. **TASK-096 kondansatör/pin tanımı:** C16, `+3.3V–GND` çıkış kondansatörüdür. Buck giriş kondansatörleri C12/C13, küçük bypass C14'tür. U5 pin 5 COMP, termal pad 9 VIN'dir. [AOZ1284PI veri sayfası](https://www.aosmd.com/res/data_sheets/AOZ1284PI.pdf)
3. **GND düzlemi:** İç katmanın `GND_PLANE` diye adlandırılmış olması dolgu bulunduğu anlamına gelmez. Güncel dosyada kesintisiz GND bakırı henüz oluşturulmamış. Önceki raporların kalkanlama ve tamamlanmış güzergâh ifadeleri gerçekleşmiş sonuç olarak kullanılamaz.
4. **Bileşen kimlikleri:** Güncel U1 değeri AP33772SDKZ-13-FA02. Bazı eski yerleşim metinlerindeki STUSB4500 adı güncel tasarımla uyuşmuyor.

### Yerleşimde incelenecek bağlantılar

| Bağlantı | Mevcut mesafe, mm | Plan açısından anlamı |
|---|---:|---|
| R11.2 → Q5.7 | 46,94 | Kullanıcı çıkış kolu için ayrı ve yeterli kesitte güç güzergâhı gerekli |
| Q5.5 → RShunt1.1 | 19,98 | F.Cu–B.Cu geçişi, güç bakırı ve Kelvin ayrımı birlikte planlanmalı |
| L3.1 → U11.1 | 10,89 | BOOST_SW alanı için yerleşim önceliği; bobin/IC yönleri birlikte incelenmeli |
| U11.1 → D4.2 | 4,55 | Boost yüksek frekanslı akım döngüsünün bir bölümü |
| D4.1 → C28.1 | 12,34 | İlk aşamada kısaltılabilecek boost çıkış bağlantısı |
| C12.1 → U5.9 VIN | 6,06 | Buck giriş kapasitörü erişimi iyileştirilmeli |
| C12.2 → U5.3 GND | 8,79 | Giriş döngüsünün dönüş kolu uzun; sadece VIN mesafesine bakılmamalı |
| C14.1 → U5.9 VIN | 5,33 | Bypass için daha yakın bir aday yerleşim aranmalı |
| RShunt1 → U3 sense pinleri | 4,31 / 4,31 | Simetrik pad mesafeleri korunmalı; ayrı Kelvin izleri hâlâ gerekli |

TI, boost SW yollarının uzunluğunu/alanını azaltmayı ve bypass kondansatörünü VIN/AGND'ye yaklaştırmayı önerir. AOS da giriş kondansatörü, VIN ve GND bağlantılarını yakın tutmayı, FB/COMP hatlarını LX'ten uzak geçirmeyi ister. Bu yüzden boş alan planının ikinci aşaması güç döngüleridir. [TPS55340 yerleşim bölümü](https://www.ti.com/lit/ds/symlink/tps55340.pdf), [AOZ1284PI yerleşim bölümü](https://www.aosmd.com/res/data_sheets/AOZ1284PI.pdf)

## 3. Boş alanları değerlendirme planı

`placement-plan.png` mevcut avluları ve aday inceleme pencerelerini gösterir. İki yüz de aynı KiCad koordinat sistemiyle çizilmiştir; B.Cu aynalanmamıştır. Pencerelerin tamamı kullanılabilir boş alan sayılmaz.

| Alan / öncelik | Yüz ve yaklaşık pencere, mm | Öneri | Korunacak ilişki |
|---|---|---|---|
| **A / ilk aşama** | B.Cu, X=106–114; Y=109–121 | C28'i D4/C27 yakınına al; gerektiğinde boost döngüsünü bütün olarak düzenle | L3–U11–D4–C27/C28 aynı boost hücresi |
| **B / ilk aşama** | B.Cu, X=124–134; Y=118,5–124,5 | U13, C35 ve R61'i birlikte 3 mm yukarı taşıyan aday | U3 → U13 → U12/Q4 koruma zinciri; C35 dekuplajı korunur |
| **C / bağlantıya ayrılacak** | F.Cu, X=70–100; Y=85–98 | USB/enkoder/LCD bağlantıları için geçiş; yalnız ilgili arayüz pasifleri burada değerlendirilsin | MCU–konnektör akışı; J8 geçiş delikleri ve ekran yüksekliği |
| **D / güç yoluna ayrılacak** | F.Cu, X=105–140; Y=88–96 | Q5 girişine ulaşan kullanıcı güç kolunun doğu bölümünü planla | R11 → Q5; bu pencere tek başına tüm güzergâhın geçtiğini kanıtlamaz |
| **Buck çevresi / ikinci aşama** | B.Cu, U5/C12/C13/C14 ve L1 çevresi | Giriş kondansatörü dönüş yolunu ve LX döngüsünü beraber sıkıştır | Güç hücresi ile FB/COMP bölgesi ayrımı |
| **Çıkış çevresi / routing** | Q5–RShunt1–J4 bölgesi | Boşluğu güç bakırı, katman geçişleri ve Kelvin geçişi için kullan | Şönt üzerinden yük akımı; sense izlerinden yük akımı geçmez |
| **Mekanik/RF alanlar / koru** | U2 anteni, H1–H4, J8 altı, enkoder cebi, LCD altı | Anten ve montaj alanlarını boş tut; kullanılabilir mezanin altı alanı yalnız yükseklik doğrulamasıyla değerlendir | Konektör, vida, kablo ve RF hacimleri |

Önceki mekanik kayıtta LCD altı F.Cu penceresi X=63,52–141,62; Y=72,28–127,72 ve yükseklik sınırı 1,80 mm olarak verilmiş. Bu, planın devraldığı bir kısıttır; yeni taşımalarda güncel montaj modeliyle tekrar doğrulanmalıdır. J8'in büyük B.Cu avlusunun bazı bölümlerinde daha önce kabul edilmiş alt yerleşimler bulunur; avlu içinin tamamı serbest veya tamamı yasak kabul edilmemelidir.

### İlk aşamanın denenmiş adayı

| Parça | Mevcut X/Y, mm | Aday X/Y, mm | Aday açı |
|---|---|---|---:|
| C28 | 110,00 / 125,00 | 107,50 / 118,75 | 270° |
| U13 | 129,00 / 123,10 | 129,00 / 120,10 | 0° |
| C35 | 132,16 / 124,00 | 132,16 / 121,00 | 0° |
| R61 | 125,82 / 124,00 | 125,82 / 121,00 | 180° |

| Ölçü | Mevcut, mm | Aday, mm |
|---|---:|---:|
| D4.1 → C28.1 | 12,34 | 3,74 |
| U3.3 INA_ALERT → U13.2 | 15,87 | 13,49 |
| U13.4 SW_EN → Q4.1 | 8,88 | 8,11 |

Bu adayda ana güç kollarının parçaları birbirine karıştırılmadı. C28 boost grubunda; U13 ile kendi C35/R61 pasifleri aynı göreli düzende kaldı. Q4'ün önceki turda belirlenen konumu korundu. C28 taşıması tüm boost döngüsünün veya termal performansın tamamlandığı anlamına gelmez.

### Uygulama sırası ve kabul koşulları

1. **Kural ve kütüphane temeli:** Footprint ailelerini, maksimum gövde ölçülerini ve avlu paylarını doğrula. 0,20 mm ek avlu açıklığını proje hedefi olarak tanımla; üreticinin daha büyük isteği varsa onu kullan. Elektriksel bakır clearance kuralını bununla karıştırma.
2. **Yerel düzenleme:** Yukarıdaki dört parçalık adayı uygula; kendi blokları içindeki pad bağlantılarını ve iki yüzün montaj açıklığını denetle.
3. **Güç döngüleri:** Boost L3/U11/D4/C27/C28 ve buck U5/C12/C13/C14/L1/D2 hücrelerini ayrı ayrı ele al. Bir pasif taşınırken bağlı olduğu IC pini, GND dönüşü, güç/geri besleme ayrımı ve komşu blok sınırı birlikte değerlendirilsin.
4. **Bağlantı yolları:** Kullanıcı çıkış kolunu, dahili besleme kolunu ve GND dönüşlerini route et. Akım, bakır kalınlığı, izin verilen gerilim düşümü ve sıcaklık artışına göre iz/poligon/via boyutlarını belirle. USB/SPI/I2C ve Kelvin yollarının referans düzlemlerini tamamla.
5. **Montaj doğrulaması:** Fiducial/panel taşıma alanı, pick-and-place merkez/açı/yüz bilgisi, stencil ve maske açıklıkları, nozul erişimi, iki yüzlü dizgi sırası ve rework erişimini seçilen montajcıyla doğrula. İlk numunede lehim/AOI ve elektriksel işlev kontrolünü tamamla.

Yerleşim aşamasında kabul: yeni elektriksel veya mekanik DRC ihlali yok; pad/net eşleşmeleri korunmuş; mekanik ankrajlar sabit; kritik döngüler uzamamış. Üretim kapısı ayrıca 360 açık bağlantının giderilmesini ve mevcut DRC bulgularının çözülmesini veya gerekçeli kabulünü gerektirir.

## 4. IPC Class 2 / Level B mesafe tablosu

**Class 2**, ürünün performans/kabul sınıfıdır; **Level B**, nominal land-pattern yoğunluk seviyesidir. Aynı sınıflandırma değildirler. Lehimli montajın Class 2 kabulü IPC-A-610/J-STD-001 çerçevesinde belirlenir. [IPC-A-610 sınıflandırması](https://www.ipc.org/TOC/IPC-A-610E.pdf)

**Tek bir mesafe, pick-and-place ve lehimlemeyi garanti etmez.** IPC-7351 kapsamı land-pattern geometrisi yanında maskeyi, pastayı ve montaj koşullarını da dikkate alır; montajcının proses sınırları gerekir. [IPC-7351B kapsamı](https://www.ipc.org/TOC/IPC-7351B.pdf)

### Ölçüm tanımları

- **Pad-to-pad:** Bakır kenarından bakır kenarına açıklık. Pad merkezleri arasındaki pitch değildir.
- **Courtyard excess, E:** Gövde/pad zarfının dışına bir bileşen için eklenen avlu payı.
- **Courtyard-to-courtyard, G:** İki footprint'in avlu sınırları arasındaki ek mesafe. Çizgi kalınlığının dış kenarı yerine tanımlı geometrik sınır esas alınmalı.

Karşılıklı kenarlarda avluyu padler belirliyorsa **pad aralığı = E₁ + G + E₂**. Gövde daha büyükse gerekli pad aralığı daha da büyüyebilir. Bu geometrik çıkarım aynı footprint'in içindeki iki IC padine uygulanmaz.

### Farklı bileşenler arasındaki açıklıklar — tüm değerler mm

Sayısal aile payları için doğrulanan referans IPC-7351 **Şubat 2005**, Tablo 3-2/3-3/3-5/3-6/3-13/3-14'tür. Buradaki **Level B, “IPC-7351B” revizyon harfi değildir**. Üretim şartnamesinde kullanılacak revizyon ayrıca belirtilmeli; bu tablo tam footprint uygunluk belgesi sayılmamalıdır. [IPC-7351 aile tabloları](https://kte.fei.tuke.sk/livovsky/ECAD/Literatura/IPC_7351.pdf)

| Komşu paket çifti | Nominal E₁ + E₂ | Avluların çakışmadığı geometrik G alt sınırı | Bu durumda türetilen pad-to-pad alt sınırı | Bu kart için önerilen G | Önerilen G ile pad alt sınırı |
|---|---:|---:|---:|---:|---:|
| 0402–0402 (1005 metrik) | 0,15 + 0,15 | 0,00 | 0,30 | 0,20 | 0,50 |
| 0402–0603 ve üzeri pasif | 0,15 + 0,25 | 0,00 | 0,40 | 0,20 | 0,60 |
| 0402–SOT/SOIC/TSSOP/QFN | 0,15 + 0,25 | 0,00 | 0,40 | 0,20 | 0,60 |
| 0603/0805/1206/1210/2512 direnç/MLCC–benzer R/C | 0,25 + 0,25 | 0,00 | 0,50 | 0,20 | 0,70 |
| 0603 ve üzeri direnç/MLCC–SMD IC | 0,25 + 0,25 | 0,00 | 0,50 | 0,20 | 0,70 |
| SOT/SOIC/TSSOP–SOT/SOIC/TSSOP | 0,25 + 0,25 | 0,00 | 0,50 | 0,20 | 0,70 |
| QFN/WSON–IC, rework erişimi gereken yön | 0,25 + 0,25 | 0,00 | 0,50 | 0,50 hedef | 1,00 |

0,00 mm sütunu yalnızca doğru avluların temas edebildiği geometrik başlangıçtır; üretim garantili aralık değildir. 0,20 ve 0,50 mm hedefleri bu incelemenin proje önerileridir, IPC'nin tüm paketlere koyduğu zorunlu minimumlar değildir. Montaj/nozul/rework gereği daha büyük bir değer gerekebilir. Isınan 2512 dirençler ve bobinler için ayrıca termal alan gerekir.

KiCad kütüphane kuralları genel olarak 0,25 mm; küçük parçalarda 0,15 mm pay kullanır. Metal kutu kapasitör/kristal ve konnektörlerde 0,50 mm; BGA'da 1,00 mm gibi farklı paylar vardır. Bunlar avlunun içindeki paylardır. Konnektör eşleşme hacmi, büyük komponent yüksekliği ve mezanin istisnaları ayrıca değerlendirilir. [KiCad F5.3](https://klc.kicad.org/footprint/f5/f5.3/)

### Aynı IC içindeki komşu padler

Tek bir IPC Class 2 minimumu vermek doğru olmaz. Paket pitch'i, üretici land-pattern'i, pad genişliği ve PCB/maske/pasta prosesi belirleyicidir. Örneğin aynı sıradaki eş genişlikli padlerde açıklık `pitch − pad genişliği` olur.

| Güncel karttaki örnek | Pitch, mm | Pitch yönündeki pad genişliği, mm | Komşu kenar açıklığı, mm |
|---|---:|---:|---:|
| U1 WQFN, pad 1–2 | 0,50 | 0,25 | 0,25 |
| U12 WSON, pad 1–2 | 0,50 | 0,25 | 0,25 |
| U3, pad 1–2 | 0,50 | 0,30 | 0,20 |
| U11 HTSSOP, pad 1–2 | 0,65 | 0,40 | 0,25 |
| U13 SOT-23-5, pad 1–2 | 0,95 | 0,60 | 0,35 |
| U5 SOIC-8, pad 1–2 | 1,27 | 0,60 | 0,67 |

Bunlar mevcut dosyadan ölçülen belirli pad çiftleridir; paketteki termal pad dâhil tüm çiftlerin minimumu veya kabul sınırı değildir. Projedeki genel bakır clearance değeri 0,15 mm'dir; bu bir dizgi avlusu kuralı değildir. Maske büyütmesi `m` ve istenen maske köprüsü `w` için, karşılıklı eş açıklıklarda pad aralığının en az `2m+w` olması gerekir. Örneğin `m=0,05`, `w=0,10` ise geometrik gereksinim 0,20 mm çıkar; gerçek proses değerleri montaj/PCB üreticisinden alınmalıdır.

### Mevcut 0,15 mm iddiasının kontrolü

R56–R58 örneğinde çizgi merkezlerine göre avlu aralığı **0,20 mm**, 0,05 mm kalınlıklı çizgilerin dış kenarları arasında **0,15 mm**, hizalı bakır pad kenarları arasında **0,50 mm** bulunuyor. Önceki raporların 0,15 mm ifadesi ölçüm tanımı olmadan kullanılamaz.

`gopo.kicad_dru` dosyasında genel pozitif avlu aralığı kuralı yok; belirli J8/J7 ilişkileri için istisnalar var. Dolayısıyla sıfır `courtyards_overlap` bulgusu, tüm kartın 0,15 veya 0,20 mm ek avlu aralığına uyduğunu kanıtlamaz. Sonraki uygulamada seçilen açıklık ayrı bir DRC kuralına dönüştürülmeli; var olan mekanik istisnalar kendi kanıtlarıyla korunmalı.

Montajcı gereksinimleri paket çiftine göre değişebilir: örneğin JLCPCB pasif, QFN, QFP ve BGA komşuluklarını ayrı değerlendirir. Bu üreticiye ait komponent aralıkları yukarıdaki IPC avlu paylarıyla aynı ölçü değildir. [Montajcı örneği: SMD aralıkları](https://jlcpcb.com/help/article/minimum-spacing-for-smd-components)

## 5. İnceleme çıktıları

- `placement-plan.png`: Gerçek avlulardan hazırlanmış iki yüzlü alan planı; mavi çizgiler aday yerleşim.
- `top.png`, `bottom.png`: Ana kartın 3D görünümleri.
- `layers/`: Dört bakır katmanın KiCad SVG çıktıları.
- `board-audit.json`: Kaynak hash, koordinatlar, pad/netler, gruplar ve avlular.
- `measurements.json`: Mevcut kart mesafeleri.
- `drc.json`: Ana kartın DRC ve şematik parite kontrolü.
- `candidate/gopo.kicad_pcb`: **Ana karta uygulanmamış** dört parçalık aday. Üretim dosyası değildir.
- `candidate/moves.json`, `candidate-drc.json`, `candidate-check.json`: Aday hareketleri, DRC karşılaştırması, bağlantı kimliği ve ana dosyanın değişmediğinin kontrolü.

Üretim uygunluğu için kalanlar: güç/sinyal routing'i, GND/power dolguları, tam footprint aile/tolerans denetimi, nihai avlu kuralı, seçilen montajcı DFM kabulü ve numune doğrulaması.
