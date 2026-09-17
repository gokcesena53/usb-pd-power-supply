# PCB yerleşim başlangıç kararı ve BOM durumu

Tarih: 11 Eylül 2026

## Son şematik durumu

- Küçük sinyal dirençleri ve küçük kapasitörler 0402 sınıfına getirildi. Bu son turda R12, C4 ve C7 0402 yapıldı; D1 için 0402 LED footprinti atandı.
- TH1, Özdisan stoklu TSM0B103F3381RZ 10 kΩ 0402 NTC olarak seçildi.
- J1 için JAE DX07B024JJ1R1500 üretici çizimine dayalı proje-yerel mid-mount USB-C footprinti oluşturuldu. Kontaklar A1–A12 ve B1–B12, 0,5 mm adım ve 0,27 mm pad genişliği ile tanımlandı; SH mekanik kalkan padleri şematikte GND'ye bağlıdır. Footprint kart kenarı oyuğunu Edge.Cuts üzerinde taşır ve ana kart sınırı bu geometriye bağlanmalıdır.
- D2, 60 V / 2 A PANJIT SS2060FL Schottky ve SOD-123F footprinti olarak düzeltildi. 01005 footprinti kaldırıldı.
- L1, 22 µH / 1,95 A Core Master SRI0704-220M ve 7,3 × 7,3 × 4,5 mm footprint olarak seçildi.
- SW1 ve SW2, PTS810 SJS 250 SMTR LFS ve KiCad PTS810 footprinti olarak seçildi.
- TP1–TP10, 1,0 mm PCB test padidir; satın alınan BOM parçası değildir.

## Neden bütün R/C parçaları 0402 değildir

Aşağıdaki parçaların daha büyük kalması elektriksel gereksinimdir:

| Referans | Footprint | Gerekçe |
|---|---|---|
| C3 | 0805 | 1 µF / 50 V giriş bypass; 28 V altında gerilim ve DC-bias payı |
| C5 | 0805 | ESP32 yerel 22 µF bulk kapasitesi ve DC-bias |
| C8, C12, C13 | 1210 | 10 µF / 50 V giriş bulk; 28 V altında etkili kapasite |
| C15, C16 | 1210 | 47 µF / 10 V buck çıkış bankı; etkili kapasite hedefi |
| C20, C21 | 1206 | 22 µF / 16 V boost giriş/çıkış bulk ve DC-bias |
| R11, RShunt | 2512 | 5 mΩ / 1 W akım şöntü; güç, sıcaklık ve Kelvin ölçümü |
| R43 | 2512 | 28 V köşesinde yaklaşık 0,65 W kayıp; 2 W sınıfı |

Bu elemanları 0402 yapmak arıza, gerilim delinmesi, aşırı ısınma veya nominalden çok düşük etkili kapasite riski doğurur.

## Katman sayısı kararı

Bu kart için öneri **4 katmandır**:

| Katman | Kullanım |
|---|---|
| L1 Top | Bileşenler, USB D+/D−, buck/boost kritik akım döngüleri, kısa hassas sinyaller |
| L2 Inner 1 | Kesintisiz GND düzlemi; sinyal geçirilmemeli |
| L3 Inner 2 | PD_VOUT, OUT_POS, +3.3V, BACKLIGHT_4V2 güç dağıtımı ve az sayıda yavaş sinyal |
| L4 Bottom | Kalan yavaş sinyaller ve GND dolgu; mümkün olduğunca az bileşen |

Espressif ESP32-C6 donanım kılavuzu 4 katmanlı kartı önerir; ikinci katmanın kesintisiz GND olmasını ve RF bölgesinin altında sağlam referans düzlemi bulunmasını ister. 2 katman uygulanabilir, ancak alt yüzün neredeyse tamamen GND kalması gerekir. Bu projedeki USB 2.0, RF, iki anahtarlamalı dönüştürücü ve 5 A çıkış yolu nedeniyle 2 katman kartı küçültmek yerine çoğunlukla büyütür ve dönüş akımlarını zorlaştırır.

Kaynak: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html

6 katman ancak mekanik zarfın 4 katmanda yönlendirmeyi imkânsız kılması, EMI ölçümünün başarısız olması veya güç/şase bölünmesinin yerleşimden dolayı kapanmaması halinde değerlendirilmelidir.

## En küçük kart için yerleşim sırası

1. Kutu iç ölçüsü, ekran penceresi, USB-C kart kenarı, encoder ekseni, klemens ve montaj delikleri sabitlenir. Kart sınırı bu mekaniklerden çıkarılır.
2. ESP32-C6-WROOM-1 anteni kart kenarına, mümkünse kart dışına taşacak biçimde yerleştirilir. Anten altında ve keepout alanında hiçbir katmanda bakır, iz veya bileşen bırakılmaz. Metal kasa ve kablolar anten alanından uzak tutulur.
3. J1 USB-C kart kenarına konur. U9 ve D3/D4/D5 ESD elemanları konnektörün hemen arkasında yerleştirilir; ESD deşarj yolu kısa ve doğrudan GND düzlemine çoklu via ile bağlanır.
4. USB D+/D− aynı katmanda, sürekli L2 GND referansı üzerinde, kısa, paralel ve eşlenmiş yönlendirilir. Üretici PCB stack-up'ı belli olduktan sonra 90 Ω diferansiyel empedans için genişlik/aralık hesaplanır.
5. USB-PD ve 5 A ana güç yolu J1 → koruma/anahtarlar → RShunt → OUT_POS → çıkış konektörleri sırasıyla yerleştirilir. Bu yol iz yerine geniş polygonlar ve gerekirse birden fazla bakır katmanı/via dizileri kullanır.
6. INA228 şöntün hemen yanında yerleştirilir; IN+ ve IN− Kelvin izleri RShunt padlerinden ayrı ve simetrik alınır, yük akımı ölçüm izlerinden geçirilmez.
7. AOZ1284PI buck bölgesinde Cin–VIN/EP–LX–D2–L1 döngüsü çok küçük tutulur. FB ve COMP elemanları LX_SW'den uzak, temiz GND bölgesinde tutulur.
8. TPS61023/CAT4104 backlight bölgesinde giriş kapasitörü–L2–SW ve çıkış kapasitörü döngüleri küçük tutulur; SW bakır alanı yalnız gereken kadar büyütülür.
9. RTC ve kristal/zamanlama bölgesi anahtarlamalı düğümlerden uzak tutulur. CR2032 holder'ın mekanik hacmi ve pil değiştirme yönü kasaya göre kontrol edilir.
10. Yerleşimden sonra üretici stack-up'ı ile USB empedansı, 5 A bakır sıcaklık artışı, via akımı, DRC, 3D mekanik çakışma ve termal inceleme yapılır.

## Boyutu belirleyen gerçek sınırlar

Kartın minimum alanını 0402 pasiflerden çok TFT konnektörü, CR2032 holder, AOZ1284PI indüktörü, USB-C kart kenarı geometrisi, encoder, klemens ve ESP32 anten keepout alanı belirler. Banana jack'ler panel tipi olduğundan kasaya monte edilip J4 üzerinden kablolanırsa PCB alanını büyütmez.

Başlangıç için 4 katman, 1,2 veya 1,6 mm toplam kalınlık ve dış katmanda 2 oz bakır adaydır. Nihai kalınlık JAE mid-mount USB-C çizimi ve seçilecek PCB üreticisinin stack-up'ıyla; bakır kalınlığı ise 5 A yolunun izin verilen sıcaklık artışıyla kesinleştirilmelidir.

## BOM durumu

`BOM_PRELIMINARY_20260911.xlsx` ve CSV dosyası, tüm fiziksel bileşenleri ve 0402 istisnalarını içerir. Footprint ataması tamamlanmıştır. Sarı satırlar üretim siparişinden önce kesin üretici parça numarası veya varyant doğrulaması gerektirir. Özellikle Q3/Q4 MOSFET gate sürüşü/SOA doğrulaması, ESP32 modül varyantı, INA228 suffix'i ve MLCC DC-bias eğrileri kapatılmadan BOM “production release” sayılmamalıdır.

Seçilmiş stoklu parçalar:

- PANJIT SS2060FL_R1_00001: https://www.ozdisan.com/p/schottky-diyotlar-385/panjit-ss2060fl-r1-00001-574723
- Core Master SRI0704-220M: https://www.ozdisan.com/p/Fixed-Inductors-468/core-master-sri0704-220m-587799
- Thinking TSM0B103F3381RZ: https://www.ozdisan.com/p/ntc-termistorler-852/thinking-tsm0b103f3381rz-509291
- PTS810 SJS 250 SMTR LFS: https://www.ozdisan.com/en/p/tactile-switches-485/littelfuse-ck-pts810-sjs-250-smtr-lfs-994927

