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
  enkoderi hesaba katmıyor. TASK-066 ile SW3 PCB'den kaldırıldı; yerine
  LCD'nin solunda J9 beşli kablo lehim pedi kondu. Pin 1=(58,00; 91,60) mm,
  açı −90°; ayrıntılar `ENCODER_PANEL_TASK066_20260924.md` dosyasında.
- **Orijin:** Aux ve grid orijini AA merkezinde, sayfa koordinatında
  (100, 100) mm. Kutu (`3d_design/`) aynı referansı kullanır. Aşağıdaki
  koordinatlar AA merkezine göredir (x sağa, y aşağı, üstten görünüş).

| Öğe | x (mm) | y (mm) |
| --- | --- | --- |
| AA | −32,40 … +32,40 | −24,30 … +24,30 |
| LCD modül | −36,28 … +41,42 | −27,52 … +27,52 |
| Ön panel penceresi (AA + 0,4) | −32,80 … +32,80 | −24,70 … +24,70 |
| **Kart (Edge.Cuts)** | **−49,70 … +49,70** | **−30,52 … +30,52** |

**Kart ölçüsü 99,40 × 61,04 mm, köşe yarıçapı 3 mm.** Kart AA'ya göre iki
eksende de simetrik; hem AA'yı hem LCD modülünü her kenarda kapsıyor.

- **Sağ ve sol kenar: AA kenarından 17,30 mm** (kullanıcı kararı, 24.09:
  sağ ve sol pay eşit). LCD modülü AA'ya göre FPC tarafına kaymış olduğu
  için modül kenarına göre paylar farklı: sağ (FPC) 8,28 mm, sol 13,42 mm.
  17,30 mm, sağ deliklerin LCD izdüşümü dışında kalmasını sağlayan en
  küçük değer (yuvarlatılmış): 9,02 (AA → modül) + 1,08 (M3 başı ile
  modül arası boşluk) + 3,2 (M3 baş yarıçapı) + 4,0 (delik → kart kenarı).
- **Üst ve alt kenar: LCD modülünden 3,00 mm** (kullanıcı kararı, 24.09).
  AA kenarından 6,22 mm. Modül ±0,2 mm toleransla da tamamen kartın
  üstünde kalıyor.
- **Köşe yarıçapı: 3 mm.** Deliklerin kenar mesafesinden (4 mm) küçük;
  köşe yayı ile delik arasında 1 mm'den fazla et kalıyor.
- **ESP32 anteni kart ölçüsünü belirlemiyor.** U2'nin konumu henüz
  sabit değil (TASK-063/054). Sağ şerit modülden yalnızca 8,28 mm dışarı
  taşıyor. MINI-1'in PCB anteni için Espressif, anten alanı ve çevresinde
  15 mm metal boşluk istiyor; bu şerit tek başına buna yetmez. Anten
  kararında seçenekler: modül ucunu kart kenarından dışarı taşırmak,
  anteni LCD izdüşümü dışında kalan bir kenara/köşeye almak veya harici
  antenli MINI-1U'ya geçmek.
- USB-C (J7) ve RJ45 (J8) sol kenara, alt (B) yüze gelecek (TASK-063).
  Sol şerit 13,42 mm; alt yüzde oldukları için LCD ile çakışmıyorlar.

## Montaj delikleri

4 × M3, `MountingHole:MountingHole_3.2mm_M3`: Ø3,2 mm NPTH, halkasız,
board-only (şemada yok), kilitli.

| Ref | x | y | Not |
| --- | --- | --- | --- |
| H1 | −45,70 | −26,52 | LCD sol kenarına merkezden 9,42 mm (M3 başı ile 6,22 mm boşluk) |
| H2 | +45,70 | −26,52 | LCD sağ kenarına merkezden 4,28 mm: M3 baş dairesi (r 3,2) ile 1,08 mm, courtyard (r 3,45) ile 0,83 mm boşluk |
| H3 | −45,70 | +26,52 | H1 gibi |
| H4 | +45,70 | +26,52 | H2 gibi |

- Her delik kart kenarlarından 4 mm içeride. Delikler 91,40 × 53,04 mm
  dikdörtgen oluşturuyor; kutu boss'ları bu ölçüye göre yapılır.
- H2/H4 ile FPC: FPC kıvrımı modül kenarından 1,00 mm dışarıda
  (x = +42,42) ve M3 başının iç kenarı x = +42,50'de. Ama FPC bandı
  deliklerin y aralığına girmiyor. Bant, modülün alt kenarından 10,47 mm
  yukarıda başlıyor (y = +17,05). Üst sınırı çizimden ölçekle yaklaşık
  y = −21,4 (38,5 mm genişlik; ölçü yazılmamış). M3 başları |y| ≥ 23,32'de,
  bandın dışında. Bant genişliği numunede doğrulanacak (TASK-064/012).
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
  penceresi (AA + 0,4), AA merkez artısı ve "FPC çıkışı" işareti.
- Başlangıç yerleşimi (iz ve zone yok) göreli dizilim korunarak
  (+55, −9) mm kaydırıldı. Bu kaydırmada her parça ya tamamen kartın
  içinde ya tamamen dışında kalıyor; itilen parça yok. U2'nin kenarı aşan
  kısmı yalnızca anten keepout alanı. Bu başlangıç durumundaki SW3,
  TASK-066 ile kaldırılıp panel parçasına dönüştürüldü.
  Yerleşim TASK-063/065'te yapılacak.

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

## Revizyon

- 24.09 (ilk): 107,0 × 61,0 mm. Sağda U2 anteni için 21,08 mm şerit
  vardı (anten LCD'den 15,18 mm). Kullanıcı itirazıyla geri alındı: U2
  konumu sabit değildi. Yerine sağ/sol eşit pay ve üst/alt 3 mm geldi.
