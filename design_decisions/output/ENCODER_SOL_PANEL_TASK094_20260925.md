# TASK-094 — Sol panel encoder ve sol kart kenarı

25.09.2026: Ana PCB'ye uygulandı. TASK-094.01/02/03 kapsamı tamamlandı; kart dışındaki blokların geri yerleşimi TASK-095'tir.

## Son kullanıcı kararı ve koordinatlar

Uygulama sırasında kullanıcı **düz dış panel montajını ve şaftın dışarı taşmasını** seçti. Önceki şaft ucunu USB ağzıyla aynı düzleme getirme şartı kaldırıldı. Encoder tabanı PCB top düzlemine 90°; şaft sol panele dik ve PCB düzlemine paraleldir. Encoder SW3 elektriksel olarak hâlâ panel parçasıdır, J9'a kabloyla bağlanır.

3 mm kalınlığındaki düz panel için iç yüz X=49,800, dış yüz X=46,800 mm seçildi. Bu, mevcut X=50,300 mm kart kenarı ile panel arasında **0,500 mm montaj payı** varsayımıdır; kullanıcı tarafından verilen ayrı bir kutu koordinatı değildir. Kutu tasarımına aktarılacak nominal montaj konumudur.

| Öğe | Nominal koordinat / ölçü |
|---|---|
| J7 USB ankrajı | X=52,975, Y=88,500; −90°; F.Cu — değişmedi |
| J8 Ethernet ankrajı | X=102,500, Y=79,610; 0°; B.Cu — değişmedi |
| USB giriş merkezi | STEP Z=+3,325 mm |
| RJ45 giriş merkezi | STEP Z=−9,585 mm (mevcut yaklaşık port modeli) |
| Encoder şaft yüksekliği | Z=(3,325−9,585)/2=−3,130 mm |
| PCB üstüne göre şaft yüksekliği | −4,725 mm; STEP PCB üstü +1,595 mm |
| Şaftın panel üzerindeki yanal konumu | PCB Y=112,400 mm; eski J9 sırasının ortası |
| Encoder gövde ön / arka yüzü | X=49,800 / 54,300 mm |
| Şaft ucu | X=37,300 mm; dış panelden 9,500 mm çıkıntı |
| J9 pad 1 | X=61,500, Y=104,000 mm; −90°; F.Cu |

USB ve RJ45'in yalnız ankrajları değil model dönüşümleri de başlangıçla aynıdır. J7'nin eski rapordaki X=53,975 konumuna dönülmedi. Düz panelde USB için 12×6 mm, RJ45 için 18×17 mm kaba erişim açıklıkları; encoder için Ø7,3 mm burç deliği mekanik inceleme modeline işlendi. Bunlar bitmiş kutu üretim çizimi değildir.

## Encoder modeli

Üretici PDF'sinin tek sayfalık çizimindeki gövde 12×11,7×4,5 mm, tespit kulaklarıyla 12,5 mm, E burç Ø7×5 mm, F şaft Ø6, L=12,5 mm, düz kısım uzunluğu 4,5 mm ve düz yüz karşılığı 4,5 mm esas alındı. Şaft ucu gövde arkasından 17 mm; bağlantı uçları arkaya 3,5 mm uzanır. Terminal merkezleri 7,5/7,0 mm asimetrik yerleşim ve 2,5/5,0 mm adımlarla modellendi.

Eski STEP basamaklı kutularla silindir yaklaşımı yapıyor ve şaft düzlüğünü içermiyordu. Ayrı panel modeli gerçek silindir ve F düzlüğüyle oluşturuldu:

`hardware/libraries/Mechanical_Custom.3dshapes/Encoder_Panel_EC1121S.step`

Ana PCB'deki **MECH_ENC** yalnız mekanik 3D gösterimdir: elektriksel pad yok, `board_only`, BOM ve pozisyon çıktılarından hariç. Şemaya SW3 footprint'i geri eklenmedi. Eski kütüphane modeli yerinde bırakıldı.

Model sınırları: bacak kalınlığı ve metal kapak ayrıntıları basitleştirilmiştir; PDF'de diş/somun ölçüsü verilmediğinden doğrulanmış dişli bağlantı iddiası yoktur. Burç deliği ve oturma yüzeyi gösterilir; gövdede tutma/retansiyon ayrıntısı kutu/numune kontrolünde netleştirilecektir. Şaft buton hareketi çizimde 1,1±0,2 mm; düğme/panel hareket payı kutu kabulünde korunmalıdır.

## Taşınan bloklar ve J9

Encoder zarfı, J9 ve yeni sol kenar nedeniyle etkilenen iki blok **26 komponent** olarak kart dışına park edildi:

| Blok | Refler | Rijit öteleme (mm) |
|---|---|---|
| AP33772S PD kontrolcü + VBUS şönt/anahtar | U1, Q3, D1, TH1, C1–C4, C8, R8, R9, R11–R14, R21, R64, R65, TP1–TP5 | ΔX=−45, ΔY=+50 |
| ROTARY ENCODER | R34, R35, R36 | ΔX=−30, ΔY=+75 |

AP grubunun TP1/TP4'ü yeni boşluğa giriyordu; yalnız test noktaları yerine kullanıcının isteğiyle tüm ilişkili blok taşındı. Grup yazıları da birlikte taşındı. Blokların göreli yerleşimi, açı/yüz, pad-net eşleşmeleri korunmuştur. Mevcut dört iz segmenti bu bloklara ait değildir ve aynı UUID/geometri/netlerle korundu. Ayrıntılı önce/sonra envanter `placement.json` içindedir.

J9 yeni kenarın içinde X=61,5'e 3,5 mm kaydırıldı. Beş pad ve pin yazıları birlikte taşındı; sıra **1=A, 2=GND, 3=B, 4=SW, 5=GND**. Encoder–J9 kabloları alt yüzden gider. X=57,8..70, Y=102..123, STEP Z=−17..−0,5 mm servis hacmi ayrılmıştır; TASK-095 bu hacmi korumalıdır. 26–28 AWG esnek kablo ve en az 4,5 mm büküm yarıçapı önceki kablo kararıyla sürdürülür. Bu hacim bir kablo demeti üretim modeli değildir; lehim uçları, izolasyon, gerilim alma ve gerçek büküm numuneyle kabul edilir.

## Sol Edge.Cuts

Sadece eski sol dik çizgi değiştirildi. Diğer **7 Edge.Cuts öğesi**, köşe yayları, üst/alt/sağ kenarlar ve H1–H4 korunmuştur. Yeni boşluğun en iç kenarı X=59,800 mm'dir; ana yatay sınırlar Y=102,500 ve 122,300 mm, geçişler 1×1 mm pahlarla yapılmıştır. Sol kenara dönüş Y=101,500 ve 123,300 mm'dedir. Yeni koordinat zinciri `placement.json` içindedir; kapalı dış hat KiCad STEP ve DRC ile doğrulanmıştır.

J9 pad bakırının en sol noktası X=60,575; yeni dik kenara açıklık **0,775 mm**, hem 0,254 mm kullanıcı sınırını hem 0,500 mm mevcut genel kuralı sağlar. J7'nin eski 0,250 mm özel kuralı **0,254 mm** olarak sıkılaştırıldı. Genel kurallar gevşetilmedi; yeni ihlal istisnası eklenmedi. Kartta bakır dolgu alanı sayısı 0'dır.

## Doğrulama

KiCad'den dışa aktarılan gerçek MECH_ENC modelinin montaj koordinatları hedef STEP ile karşılaştırıldı: tüm sınırlar eşleşir. Encoderın dünya zarfı X=37,3..57,8, PCB Y=104,75..119,55, STEP Z=−9,38..3,12 mm.

| Encoder ile karşılaştırılan katı | En kısa mesafe (mm) | Kesişim (mm³) |
|---|---:|---:|
| PCB | 2,008 | 0 |
| USB J7 | 11,809 | 0 |
| Ethernet J8 | 5,250 | 0 |
| J9 | 3,496 | 0 |
| J3 | 35,694 | 0 |
| LCD'nin toleranslı XY prizması | 5,720 | 0 |
| 3 mm panel | 0 — amaçlanan oturma | 0 |

Alt yüz kablo servis hacmi PCB/J7/J8/J3/panel ile kesişmez. LCD için yükseklik varsayımına ihtiyaç bırakmayan tam yükseklikli XY prizması kullanıldı. Ethernet modeli yaklaşık olduğundan gerçek RJ45 giriş merkezi, lehim çıkıntıları ve fiş/mandal erişimi TASK-053/054/088 numune kabulünde sürer.

Son `kicad-cli pcb drc --refill-zones --schematic-parity`:

- Hata **15 → 15**: başlangıçtaki U2 kart kenarı hataları.
- Uyarı **155 → 153**; yeni ihlal **0**.
- Şema paritesi **0**; bağlantısız öğe **360 → 360**.
- J7/J8, H1–H4 ve etkilenmeyen tüm elektriksel footprint'ler korunmuştur.
- Üst/alt SVG katmanları ve 3D görseller incelendi.

Bu görev yerleşim değişikliğidir; 26 parça bilinçli olarak kart dışındadır. Kart üretime hazır değildir. TASK-095 yeniden yerleşim, TASK-087 genel routing, mevcut numune görevleri fiziksel kabul içindir.

## Kanıtlar

- [Ölçülü montaj görünümü](../../hardware/docs/reports/task-094-20260925/mounting-review.png)
- [Son üst 3D görünüm](../../hardware/docs/reports/task-094-20260925/final-top.png)
- [Park edilen bloklar](../../hardware/docs/reports/task-094-20260925/parked-blocks.png)
- [Sayısal doğrulama](../../hardware/docs/reports/task-094-20260925/verification.json)
- [Katı kesişim kontrolü](../../hardware/docs/reports/task-094-20260925/solid-check.json)
- [Önce/sonra envanter](../../hardware/docs/reports/task-094-20260925/placement.json)
- [Son DRC](../../hardware/docs/reports/task-094-20260925/final-drc.json)
- [Mekanik inceleme STEP](../../hardware/docs/reports/task-094-20260925/mechanical-review.step)

Aynı rapor dizininde başlangıç PCB/proje/kural yedekleri, üretim ve doğrulama betikleri vardır. `axial-mounting.png` ve `mechanical-analysis.json` içindeki `axial_constraints` ilk hizalama şartının inceleme geçmişidir; güncel karar `current_mount` ve bu rapordur.
