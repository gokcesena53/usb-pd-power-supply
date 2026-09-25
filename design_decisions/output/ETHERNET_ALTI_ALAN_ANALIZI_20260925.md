# Ethernet mezanini altındaki alanı aktif kullanma — 25.09.2026

Kullanıcı, Ethernet modülünün altındaki alana da komponent yerleştirilmesini istedi.
Buradaki alan, B.Cu üzerindeki J8 modülü ile anakart arasındaki hacimdir; kartın
üst görünümünde RJ45'in aşağısındaki boşluk değildir. Bu karar TASK-080'deki
yardımcı parçaları modül dışında tutma tercihini ve genel plandaki alanı başlangıçta
boş bırakma yaklaşımını değiştirir. Elektriksel ve mekanik sınırlar korunarak
uygun alt hacim aktif kullanılacak; gerçek yerleşim ayrı görevde uygulanacaktır.

## Güncel PCB'den okunan geometri

Kaynak: `hardware/gopo.kicad_pcb`; dosya SHA-256, ref/net/konum envanteri ve
J8 geometrisi `hardware/docs/reports/ethernet-underlay-analysis-20260925/geometry.json`
dosyasındadır. Bu çalışma salt okunur ön analizdir; yeni DRC, 3D çakışma kontrolü
veya numune ölçümü yapılmadı. F.Fab/B.Fab çizgileri mekanik nominal zarfı gösterir;
lehim ve üretim toleransı eklenmiş nihai kullanılabilir hacim değildir.

- J8: B.Cu, (102,50; 102,00 mm), 0°. Nominal modül PCB zarfı
  X=51,35..104,35, Y=99,89..121,89 mm (53 × 22 mm).
- RJ45 B.Cu keepout: X=51,35..69,85, Y=102,99..119,39 mm;
  footprint, iz ve via yasakları mevcut. Bu bölge yerleşime açılmayacak.
- Header nominal zarfı: X=98,69..103,77, Y=100,73..121,05 mm.
- Bu iki engelin arasındaki ön inceleme şeridi X=69,85..98,69,
  Y=99,89..121,89 mm: **28,84 × 22 mm, yaklaşık 634 mm² brüt alan**.
  Bu değer kullanılabilir net alan değildir; yerel çıkıntılar, toleranslar,
  erişim, bakır/via koridorları ve diğer parçalar düşülecek.
- TASK-091 J8'i taşıyacağı için bu mutlak koordinatlar geçicidir. Aynı şerit
  mevcut J8 orijinine göre dx=-32,65..-3,81, dy=-2,11..19,89 mm'dir;
  yeni açı/yüz/konumda footprint dönüşümüyle tekrar hesaplanmalıdır.
- J3 üst yüzde, orta şeridin header tarafıyla XY olarak örtüşür. Karşı yüz
  SMD gövdeleri tek başına çakışma sayılmaz; delik, via ve lehim zarfları incelenir.
- J9 pad 5 merkezi (58,00;106,80), mevcut RJ45 keepout izdüşümündedir;
  pad 4 (58,00;102,60) kenarı da bölgeye girer. THT pin/lehimin modüle bakan
  yüzü TASK-091'de yeniden kontrol edilmeli. Courtyard istisnası bu fiziksel
  uygunluğun kanıtı değildir.
- Q8/R17/C10/C20/C21 ve TP14 halen eski kart dışı koordinatlardadır. J8'in
  taşınmış olması bunların son konuma birlikte taşındığı anlamına gelmez.

## Yükseklik ve adaylar

TASK-080 raporundaki 2,50 mm nominal aralık ve 1,90 mm toleranslı boşluk birer
ön varsayımdır; TASK-053 numunesi halen bekleniyor. 1,90 mm tüm modül altı için
garanti sayılamaz. Her ref için seçili MPN maksimum yüksekliği, lehim/oturma,
modül altı yerel çıkıntı, eğrilik ve montaj toleransı ile kalan açıklık hesaplanır.

| Öncelik / ref | Değerlendirme |
|---|---|
| C20, R17, C21 | İlk adaylar, 0402. Eski rapor toplam 0,65 mm zarf varsayıyor; 1,90 mm boşlukta hesap 1,25 mm kalır. MPN ile doğrulanmalı. C20 J8.13/14 ve GND dönüşüne, R17/C21 Q8 gate/source uçlarına yakın tutulmalı. |
| Q8, C10 | Aynı işlevsel hücre içinde koşullu adaylar. Eski rapor sırasıyla 1,60/1,55 mm toplam zarf varsayıyor; kalan pay 0,30/0,35 mm. Gerçek MPN/montaj verisi olmadan onaylanamaz. Q8 sırf MOSFET olduğu için sıcak kabul edilmez; gerçek yükte iletim ve açılış kaybı hesaplanır. Gerekirse Q8/C10 dış kenarda, ilgili küçük pasifler yakın iç kenarda kalır. |
| R34, R35, R36 | 0402 enkoder pull-up grubu, ikinci aday. Güncel J9 ve MCU koridoruna göre beraber taşınabilir; kablo lehimleri ve RJ45 pin alanından uzak kalmalı. |
| Q1/Q2 + R4/R5/R6/R7 | I2C seviye dönüştürücü hücresi, üçüncü aday. SOT-23 yüksekliği MPN ile kontrol edilmeli; yalnız toplam bus güzergâhını/kapasitansını bozmazsa grup olarak kullanılmalı. |
| TP14, diğer test pedleri, butonlar | Modül takılıyken erişim gerekenler açık kenarda tutulmalı. |
| Buck/boost, bobinler, güç şöntü/deşarj direnci, RTC kristali, MCU anteni | Bu hacim için öncelikli aday değiller. Güç/ısı, hassas ölçüm veya RF yerleşimini alan doldurmak amacıyla bozma. MCU dekuplajını MCU'dan ayırma. |

## Uygulama ve kabul

Önce TASK-091 port/MCU/J9 ankrajlarını ve J8 yerel hacim haritasını kesinleştir.
Ardından Ethernet altı görevinde adayları seçip gerçekten yerleştir; yalnız boş
alan çizimi veya tüm adayları gerekçesiz dışarı bırakmak tamamlanma sayılmaz.
Uygun ref bulunamazsa ölçülü engelleri kaydet, görevi tamamlandı yapma.
Seçilen ref sayısı ve kapladıkları alan ile kalan routing/erişim alanını raporla;
bir doluluk yüzdesini tutturmak için gereksiz parça taşıma.

Sadece fiziksel olarak doğrulanan J8–ref çiftleri için courtyard istisnası
tanımlanabilir. Mevcut J8–TP14/J9 kuralı yeni parçalar için genel izin değildir;
short, clearance, delik ve RJ45 keepout kontrolleri etkin kalır. Modül takılmadan
önce dizgi/muayene ve sonrasında yeniden işleme/söküm sırası belgelenir.

Ön yerleşim numune beklemeden açık varsayımlarla ilerleyebilir. TASK-053 gerçek
ara mesafe, alt çıkıntı, pin ve eğrilik ölçülerini sağlar; TASK-088 üretim öncesi
kabulünde yerleştirilmiş her ref bu ölçülerle tekrar karşılaştırılır. Bu ölçüm
kapısı geçilmeden üretime uygunluk iddiasında bulunulmaz. Son yerleşim TASK-092,
kritik güzergâh kabulü TASK-008 ve routing TASK-087 ile devam eder.
