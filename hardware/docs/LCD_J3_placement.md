# Sol kenar USB-C, ESP32 anteni ve LCD/J3 yerleşimi — 2026-09-17

Aktif kart: `../gopo.kicad_pcb`. Koordinatlar KiCad mm cinsindedir. Bu belge önceki LCD/J3 konumlarının yerine geçer. Şematik ve Edge.Cuts değiştirilmedi.

| Öğe | Güncel durum |
|---|---|
| Kartın düz kenar referansları | X=24.504–90.415509; Y=88.397–129.031999, yaklaşık 66 × 41 mm |
| J7 USB-C | (28.179, 120.278667), B.Cu, 90°; ağız sol dışarı |
| U2 ESP32-C6 | (39.209754, 101.665333), B.Cu, −90° |
| U2 anten keepout'u | X=23.459754–29.459754; Y=92.665333–110.665333 |
| LCD gövde sınırı | X=29.9597545–89.8697545; Y=87.314499–130.114499, 59.91 × 42.80 |
| LCD aktif alan | X=32.9797545–81.9397545; Y=90.354499–127.074499, 48.96 × 36.72 |
| Aktif alan ve PCB merkezi | X=57.4597545; Y=108.714499 (PCB merkezi Y=108.7144995) |
| J3 | (63.454754, 108.714499), F.Cu, 90° |
| Anten keepout'u–LCD gövdesi | 0.5000005 mm yatay açıklık; izdüşümde çakışma yok |

## Kenar ve montaj geometrisi

J7'nin footprint içindeki `PCB Edge` çizgisi, kartın X=24.504 sol düz kenarıyla çakışır. Ağız ve kablo takma yönü sola doğrudur. Land pattern, delik ve konnektör gövde ölçüleri değiştirilmedi. U2'nin anten alanı kart kenarından **1.044246 mm dışarı taşar**; montaj padleri kart içinde kalır. Bu, [Espressif'in modül antenini base board dışına taşıma önerisiyle](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html) uyumludur. U2 footprint'inin dışarıdaki üç anten ipek baskısı çizgisi yerel kütüphanede ve karttaki kopyasında fab çizimine çevrildi; anten keepout, boyutlar ve padler aynı kaldı.

U2 ve J7'nin tam footprint zarfları üzerinden ölçülen **üst kenar–U2, U2–J7 ve J7–alt kenar mesafelerinin her biri 3.408 mm** (yuvarlatılmış) olur. Son istekte bu çift için “J7 ve U7” yazıyor; U7 arka ışık güç entegresi olduğu ve aynı istekte J7'nin komşusu olarak U2 tarif edildiği için eşit aralık koşulu J7–U2 üzerinde uygulandı. U7 yerinde bırakıldı.

Aktif ekran merkezi PCB geometrik merkeziyle çakışır. LCD gövdesi sağ kart kenarının **0.546 mm** içinde, üst ve alt sınırdan yaklaşık **1.083 mm** taşar. Anten ile LCD gövdesi arasında 0.500 mm nominal yanal pay bulunur. Anten keepout'unda başka footprint, pad veya bakır yoktur. LCD'nin sağındaki katlı flex çıkışının 0.8 mm azami çıkıntısı dikkate alınırsa sağ kenarda yaklaşık **0.254 mm** kasa dışı yer gerekebilir; FPC'nin gerçek bükümü ve kasa duvarı numuneyle kontrol edilmeli.

J3 LCD ile aynı X hareketini (+2.4547545 mm) izler. LCD'nin sağından çıkan flex alt yüzeye katlanıp J3'e sağdan girer; pin 1 alt, pin 40 üst taraftadır. Ön PCB yüzeyi Z=0 kabul edildiğinde J3 üstü nominal Z=2.00 mm, LCD arkası Z=3.00 mm ve aradaki açıklık **1.00 mm** olur. XY çizimi bu yüksekliği fiziksel olarak sabitlemez; ekran desteği ve kasa sağlamalıdır. J3 STEP modeli mevcut dosya yolunda bulunmadığı için mandal, takviye bölgesi ve FPC büküm yarıçapı gerçek numuneyle doğrulanmalı.

## Çakışmaları gideren yakın yerleşim değişiklikleri

J7/U2 için gerekli alanı açmak amacıyla J4 (80,101), BT1 (51.197,119.926), Q4 (58,92.5), R2 (51.5,92.5), R3 (53.5,92.5) ve TP10 (52.75,95.4) taşındı. U10, J7/U2 arasına (30,113.2) ve D3, J7'nin iç tarafına (39,116) alındı. U1, R11, diğer güç elemanları ve U7 yerinde kaldı. Bu bileşenlerin bazıları önceki PCB'de U2 anten keepout'u veya birbirlerinin pad/courtyard alanıyla çakışıyordu; yeni konumda U2 anten keepout ihlali ve J7–U2 fiziksel çakışması yok.

CC1/CC2'nin J7–U10 düz hat pad uzaklıkları yaklaşık 8.44/5.13 mm'dir. J7–U1 CC1/CC2 yaklaşık 30.32/27.98 mm, J7 VBUS–R11 ise yaklaşık 23.44 mm kaldı. Bunlar yönlendirilmiş iz uzunlukları değildir. Özellikle PD kontrolcü, şönt ve güç yolu tekrar gruplanmadan **5 A VBUS/CC yerleşimi elektriksel olarak bitmiş sayılmaz**. Kullanılabilir kısa/geniş bakır alanı ve kesintisiz GND dönüşü routing sırasında çözülmeli; körlemesine autoroute yapılmadı.

## Doğrulama ve açık işler

- Kanonik PCB üzerinde `kicad-cli pcb drc --schematic-parity`: **307 → 266 ihlal**, **332 açık bağlantı**, **8 şema–PCB uyumsuzluğu**. Tür, açıklama ve nesne UUID'siyle karşılaştırmada sıfır yeni ihlal; 41 eski ihlal kalktı. Kart hâlâ yönlendirilmemiştir.
- Yalnız J7, U2, J3, J4, BT1, Q4, R2, R3, TP10, U10 ve D3 konumu/açısı değişti; LCD'nin 25 kullanıcı çizimi ve dört notu sağa 2.4547545 mm taşındı. Net/pad kimlikleri ve Edge.Cuts korundu. B.Cu plot ve alt 3D görünüm görsel olarak kontrol edildi.
- Üretici, son ürün kasasında antenin her yönde **15 mm** açıklığını önerir; mevcut LCD ile 0.5 mm nominal boşluk bu öneriyi karşılamıyor. Ekran arka metali, FPC, kasa ve kablo konumu ile Wi-Fi/BLE menzil ve throughput testi şarttır.
- J4'ün yeni çıkış erişimi, BT1 pil takıp çıkarma hacmi, J7 kablo overmould'u ve LCD'nin 0.5 mm toleransı kasa/prototip üzerinde doğrulanmalı. Bazı özel 3D modeller eksik; 3D render tam mekanik onay değildir.
- Şematik kaynaklı footprint uyuşmazlıkları ve Q5/Q6 eksikliği `../../todo.txt` içindedir; şematikte işlem yapılmadı.

Kaynaklar: [LCD mekanik PDF](../datasheets/NHD-2.4-240320AF-CSXP.pdf) sayfa 4; [ESP32-C6 modül veri sayfası](../datasheets/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf); [Espressif PCB kılavuzu](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html); J7 footprint'inin `PCB Edge` referansı ve [GCT USB4105 çizimi](https://gct.co/files/drawings/usb4105.pdf).

