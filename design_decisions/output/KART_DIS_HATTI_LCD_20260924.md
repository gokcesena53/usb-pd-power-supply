# Kart dış hattı: TFT032B018 görünür alanına göre (24 Eylül 2026)

Görev: TASK-062. Eski 93 × 60 mm varsayımı (`PCB_LAYOUT_YOL_HARITASI_20260912.md`)
ve 65,9 × 40,6 mm başlangıç dış hattı geçersiz.

## LCD mekanik çizimi

Kaynak: `hardware/datasheets/TFT032B018.pdf` (Xiamen Precise Display, LCM
çizimi rev A, 2023-02-10). Belirtilmeyen tolerans ±0,20 mm.

| Ölçü | Değer |
| --- | --- |
| Modül dış ölçüsü | 77,70 ± 0,2 × 55,04 ± 0,2 mm, kalınlık 2,40 ± 0,15 mm |
| TFT cam | 71,00 × 51,60 mm |
| CF | 68,10 × 51,60 mm |
| Polarizör (POL) | 67,50 × 51,20 mm |
| Görünür alan (AA) | 64,80 × 48,60 mm (240RGB × 320, IPS) |
| Arka yüz | 2 × 76,5 × 4 × 0,5 mm çift taraflı köpük bant (uzun kenarlarda) |

Çizimin ön görünüşünde FPC sol kısa kenardan çıkıyor. AA'nın modül
kenarlarına ofsetleri:

| Kenar | AA ofseti | Kaynak |
| --- | --- | --- |
| FPC'nin karşı kenarı | 3,88 mm | çizimde ölçülü |
| FPC kenarı | 9,02 mm | 77,70 − 64,80 − 3,88 (FPC tarafında sürücü IC'li cam basamağı var) |
| Uzun kenarlar (iki taraf) | 3,22 mm | çizimde ölçülü; 55,04 − 48,60 = 2 × 3,22, simetrik |

POL ofsetleri de aynı şekilde: FPC'nin karşısı 2,43, FPC tarafı 7,77, uzun
kenarlar 1,92 mm. Çizim notları: köpük penceresi AA'dan her kenarda 0,3 mm,
TP/ön panel görünür penceresi AA'dan her kenarda 0,4 mm büyük olmalı.
**Ön panel penceresi önerisi 65,60 × 49,40 mm**, AA merkezinde.

FPC ile ilgili, TASK-064'e girdi olan ölçüler: FPC, modül kenarından
10,47 ± 0,5 mm içeride başlıyor. Açık (düz) sevk ediliyor ve modül
kenarından 44,67 ± 0,5 mm dışarı uzanıyor. Arkaya bükülünce kıvrım modül
kenarından 1,00 mm dışarıda kalıyor, takviye ucu modül kenarından 41,00 mm
içeride. Konnektör ucunun genişliği 15,5 ± 0,1 mm (30 pin, 0,5 mm aralık,
W = 0,35). Takviye toplam kalınlığı 0,3 ± 0,03 mm, kontak boyu 2,5 ± 0,3 mm.

Ön görünüşte FPC'nin karşı alt köşesinde, modül dış hattından yaklaşık 6,6 mm
taşan ve yaklaşık 7,4 mm genişliğinde ölçüsüz, dolu bir dil çizili. Büyük
olasılıkla koruyucu film çekme dili; numunede kontrol edilecek (TASK-012).
Kart ölçüsüne katılmadı.

## Karar

- **Yön:** LCD yatay (landscape), kartın üst (F) yüzünde. FPC **sağ** kısa
  kenardan çıkıp kartın altına doğru arkaya bükülür (kullanıcı kararı,
  24.09). Ön görünüş, çizime göre 180° döndürülmüş hâlidir. AA sağ
  kenardan 9,02 mm, sol kenardan 3,88 mm içeride. ST7789V2 görüntü dönüşü
  firmware'de (MADCTL) bu yöne göre ayarlanır.
- **Enkoder** (SW3) karta monte edilmiyor. Kutuya panel montajla sabitlenip
  kablolarla karta bağlanacak (kullanıcı kararı, 24.09). Kart ölçüsü
  enkoderi hesaba katmıyor. SW3 footprint'i şema değişikliğine kadar geçici
  olarak kartın sol üst köşesinde duruyor (ayrı görev).
- **Orijin:** Aux ve grid orijini AA merkezinde, sayfa koordinatında
  (100, 100) mm. Kutu (`3d_design/`) aynı referansı kullanır. Aşağıdaki
  koordinatlar AA merkezine göredir (x sağa, y aşağı, üstten görünüş).

| Öğe | x (mm) | y (mm) |
| --- | --- | --- |
| AA | −32,40 … +32,40 | −24,30 … +24,30 |
| LCD modül | −36,28 … +41,42 | −27,52 … +27,52 |
| Ön panel penceresi (AA + 0,4) | −32,80 … +32,80 | −24,70 … +24,70 |
| **Kart (Edge.Cuts)** | **−44,50 … +62,50** | **−30,50 … +30,50** |

**Kart ölçüsü 107,0 × 61,0 mm, köşe yarıçapı 3 mm.** Kart her kenarda hem
AA'yı hem LCD modülünü kapsıyor. Kenar payları ve gerekçeleri:

- **Üst ve alt kenar: 2,98 mm.** Modül ±0,2 mm toleransla bile tamamen
  kartın üstünde kalıyor. Bu kenarlarda konnektör ya da delik yok; payı
  büyütmek yalnızca kutuyu büyütürdü.
- **Sol kenar: 8,22 mm.** Bu şerit H1/H3 M3 deliklerini LCD izdüşümünün
  dışında tutuyor (aşağıda). USB-C (J7) ve RJ45 (J8) bu kenara, alt (B)
  yüze gelecek (TASK-063). Alt yüzde oldukları için LCD'nin sol kısmıyla
  çakışmıyorlar.
- **Sağ kenar: 21,08 mm.** ESP32-C6-MINI-1 anteni için ayrıldı.
  Espressif, anten alanının ve çevresindeki 15 mm'nin metalden boş
  kalmasını istiyor. KiCad footprint'inin anten keepout'u da anten alanı
  + 15 mm. U2 alt yüzde, AA ekseninde (y = 0). Modül ucu x = +62,0'da
  (kenardan 0,5 mm içeride, silkscreen kenar açıklığı için). Anten alanı
  x = +56,6'da başlıyor, yani LCD modül kenarından **15,18 mm**, FPC
  kıvrımından yaklaşık 14,2 mm uzakta. Kıvrımın konumu 1,00 mm'lik çizim
  ölçüsüne göre. U2 gövdesi (x = +45,4 … +62,0) LCD izdüşümünün dışında.
  Kart 106 mm olsaydı bu mesafe 14,2 mm olurdu; 1 mm fazla genişlik bu
  yüzden seçildi.
- **Köşe yarıçapı: 3 mm.** Deliklerin kenar mesafesinden (4 mm) küçük;
  köşe yayı ile delik arasında 1 mm'den fazla et kalıyor. Kutu iç
  köşesine uyuyor.

## Montaj delikleri

4 × M3, `MountingHole:MountingHole_3.2mm_M3`: Ø3,2 mm NPTH, halkasız,
board-only (şemada yok), kilitli.

| Ref | x | y | Not |
| --- | --- | --- | --- |
| H1 | −40,5 | −26,5 | LCD sol kenarına merkezden 4,22 mm; M3 baş dairesi (r 3,2) ile 1,02 mm, courtyard (r 3,45) ile 0,77 mm boşluk |
| H2 | +58,5 | −26,5 | LCD kenarından 17,08 mm; anten alanından (y ±6,6) 16,7 mm |
| H3 | −40,5 | +26,5 | H1 gibi |
| H4 | +58,5 | +26,5 | H2 gibi |

- Her delik kart kenarlarından 4 mm içeride. Delikler 99,0 × 53,0 mm
  dikdörtgen oluşturuyor; kutu boss'ları bu ölçüye göre yapılır.
- **NPTH (GND'ye bağlı değil):** Çıkış 28 V'a kadar yüzüyor ve RJ45
  kabuğu GND'ye bağlı (TASK-054). Metal vida ya da boss üzerinden şasiye
  ikinci bir toprak yolu açılmasın diye delikler bakırsız. Kutu plastik
  (3D baskı) varsayılıyor.
- LCD modülü ön panele bantla oturur. Kart, panelden inen boss'lara bu
  dört delikle vidalanır. LCD izdüşümü içinde delik yok.

## PCB'deki uygulama

- Edge.Cuts: 4 çizgi + 4 yay, tek kapalı kontur. Eski dış hattın
  (8 segment) `invalid_outline` hatası giderildi.
- Dwgs.User (User.Drawings) katmanında: AA, LCD modül dış hattı, ön panel
  penceresi (AA + 0,4), AA merkez artısı, "FPC çıkışı" işareti ve
  "LCD + 15 mm" anten sınırı çizgisi.
- Başlangıç yerleşimi (iz ve zone yok) göreli dizilim korunarak
  (+61, −3) mm kaydırıldı ve yeni kartın içine alındı. U2 yukarıdaki
  konuma taşındı. Kenara değen C23, C33, D10, J8 ve R55, kartın büyük
  ölçüde dışında oldukları için 1,06 mm sağa, kartın tamamen dışına
  itildi. Yerleşimleri TASK-063/065'te yapılacak.

DRC (`kicad-cli pcb drc --schematic-parity`):

| | Önce | Sonra |
| --- | --- | --- |
| invalid_outline | 1 | 0 |
| copper_edge_clearance | 3 | 0 |
| silk_edge_clearance | 0 | 0 |
| H1–H4'ü içeren ihlal | — | 0 |
| schematic parity | 0 | 0 |

Kalan hole_clearance (4) J7 footprint'inin kendi GND pedi ile NPTH
pimi arasında; kenarla ilgisi yok. Diğer ihlaller yerleşimden kaynaklanıyor
(courtyard, silk).
