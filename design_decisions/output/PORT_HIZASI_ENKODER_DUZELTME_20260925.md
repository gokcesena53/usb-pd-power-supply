# USB-C altında Ethernet ve düz enkoder sırası — 25 Eylül 2026

Kullanıcının “tam altına gelmeli” düzeltmesi uygulanmıştır. Altında olma şartı
sol panel görünümünde aynı Y merkezi, USB-C için üst yüz (+Z), Ethernet için
alt yüz (-Z) demektir. Önceki TASK-091 raporundaki 28,39 mm Y farkı bu şartı
karşılamıyordu; o raporun port hizası ve tamamlanma iddiası geçersizdir.

## Uygulanan yerleşim

| Referans | Önce X/Y (mm) | Son X/Y (mm) | Açı | Yüz |
|---|---|---|---|---|
| J7 USB-C | 53,975 / 82,500 | 53,975 / 88,500 | -90° | F.Cu |
| J8 Ethernet header orijini | 102,500 / 102,000 | 102,500 / 79,610 | 0° | B.Cu |
| J9 enkoder pad 1 | 61,750 / 87,000 | 58,000 / 104,000 | -90° (önce -126°) | F.Cu |

RJ45 ağzının yerel Y ofseti +8,890 mm: **79,610 + 8,890 = 88,500 mm**.
USB-C merkezi de **88,500 mm**. Hizalama hatası **0,000 mm**.
İki ağız aynı sol panele bakar; farklı burun uzunlukları değiştirilmemiştir.

USB'nin eski Y=82,500 mm merkezi korunsaydı J8'in üst mekanik pini
(55,350;72,850) H1'in (54,300;73,480) montaj bölgesine giriyordu.
USB ve Ethernet ortak merkezi bu yüzden 6,000 mm güneye alınmıştır.
Son üst MP merkezi (55,350;78,850), H1'e merkez uzaklığı yaklaşık 5,472 mm'dir.
H1–H4 ve dış hat değişmemiştir.

J9 önce RJ45'in eski konumundan kaçınmak için çapraz döndürülmüştü.
Ethernet'in yeni konumunda bu dönüş gereksizdir. Beş pad **X=58,000 mm**
üzerinde, Y=104,000 / 108,200 / 112,400 / 116,600 / 120,800 mm'dir.
Pin sırası **ENCODER_A, GND, ENCODER_B, ENCODER_SW, GND** ve 4,200 mm adım korunur.
Bakırın LCD sınırına yatay açıklığı 63,520 − (58,000 + 0,925) = **4,595 mm**.
Modül kartının güney kenarı Y=99,500; J9 ilk padinin bakır başlangıcı
Y=103,075 olduğundan plan açıklığı **3,575 mm**'dir.

## Doğrulama ve sınırlar

KiCad STEP dışa aktarımıyla aynı orijin altında oluşturulan J7/J8/J9
katıları FreeCAD/OpenCASCADE ile karşılaştırılmıştır:

| Çift | En kısa nominal model mesafesi | Kesişim hacmi |
|---|---|---|
| J7–J8 | 3,230 mm | 0 mm³ |
| J7–J9 | 10,183 mm | 0 mm³ |
| J8–J9 | 4,372 mm | 0 mm³ |

Kanıt: `hardware/docs/reports/port-stack-fix-20260925/solid-check.json`.
Waveshare modeli projede bulunan yaklaşık mekanik modeldir; gerçek lehim
çıkıntıları ve takılı kablo fişleri bu modelde tam temsil edilmez. **3D
model çakışmasızlığı, numune ve iki gerçek fişle ≥2 mm kabulün yerine geçmez.**
RJ45 pim/lehimi ile USB sabitleme ayağı/lehimi arasındaki gerçek boşluk,
mandal erişimi ve J8 header uçlarının LCD altında ≤1,50 mm kesim şartı
TASK-053/054/088 kapsamında doğrulanmalıdır. LCD yükseltilmemiştir.

Tam üst üste iki yüzlü montaj J7'nin 4 PTH ve 2 NPTH öğesini J8'in
iki boyutlu courtyard izdüşümüne sokar. Yalnız **J7/J8 çifti** için,
yukarıdaki nominal model mesafesi belgelenerek `courtyard_clearance`
istisnası eklenmiştir. Bakır, delik ve kenar açıklığı kontrolleri korunmuştur.
Gerçek lehim zarfı numune kontrolü açık kalır; genel ihlal seviyesi bastırılmamıştır.

Son DRC: **15 hata / 129 uyarı; yeni hata 0; şema paritesi 0**.
15 hata başlangıçta da vardır: U2 üst padlerinin 0,500 mm kart-kenarı
şartına karşı 0,285 mm açıklığı. Açık düzenleyicideki kaydedilmemiş U2
konumu (77,920;75,065) önce kaydedilip korunmuştur; eski rapordaki
(78;75,6) konumuna geri alınmamıştır. Bağlantısız öğeler **360 → 360**.
Bu çıktı üretime hazır, tamamen DRC temiz kart iddiası değildir.

J7/J8/J9 konum/açıları ve J9'un beş bağımsız pin yazısı güncellenmiştir.
Eski yerde kalan 1 A / 2 GND / 3 B / 4 SW / 5 GND yazıları ilgili padlerin
yanına taşınmıştır. Tüm footprint pad/net
eşlemeleri, diğer footprint konumları, şema ve dört mevcut iz korunmuştur.
USB/Ethernet yardımcı hücreleri hâlâ önceki hazırlık konumlarındadır;
yerel besleme ve ESD son yerleşimi TASK-092/093/008 kapsamındadır.

## Güncel Ethernet altı alanı ve devir

J8 kart izdüşümü X=51,350..104,350, Y=77,500..99,500 mm.
Mevcut footprint RJ45 keepout'u X=51,350..69,850,
Y=80,600..97,000 mm'ye taşınmıştır. Modül orta kısmının önceki brüt
şeridi X=69,850..98,690, **Y=77,500..99,500 mm**, yaklaşık 634,48 mm².
Bu brüt alan net kullanılabilir alan değildir; TASK-093 son geometriyi
esas almalı ve USB THT/NPTH izdüşümünü de kontrol etmelidir.

## Çıktılar

- [Sol panel 3D görünümü](../../hardware/docs/reports/port-stack-fix-20260925/final-left.png)
- [Alt yüz 3D görünümü](../../hardware/docs/reports/port-stack-fix-20260925/final-bottom.png)
- [Sayısal doğrulama](../../hardware/docs/reports/port-stack-fix-20260925/verification.json)
- [Son DRC](../../hardware/docs/reports/port-stack-fix-20260925/final-drc.json)
- Önceki PCB ve projeye ait yedekler aynı rapor dizinindedir.
