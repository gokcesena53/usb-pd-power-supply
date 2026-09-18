---
name: kicad-layout
description: Bu depodaki KiCad PCB yerleşimini ve yönlendirmesini incele, düzenle ve doğrula. Footprint, mekanik erişim, güç döngüleri, dönüş yolları, bakır alanları, DRC ve 3D kontrolü için kullan.
---

# KiCad layout çalışması — gopo deposu

Bu skill, [American Embedded kistack layout skill'inin sabit sürümündeki](https://github.com/American-Embedded/kistack/blob/ecf16c119c7ed610f5f251c479b03884b8d98b09/skills/layout/SKILL.md) ilkeleri bu projeye uyarlar. Kaynak MIT lisanslıdır; telif ve lisans metni `../kicad-schematic/references/LICENSE-kistack` dosyasındadır.

## Temel döngü

```
mevcut kartı ve şematik netlist'i oku → mekanik ve elektriksel plan yap
→ kanonik kartı düzenle → katmanları/3D'yi görüntüle → DRC ve bağlantıları denetle
→ gerekiyorsa düzelt ve tekrarla
```

- Aktif kart `hardware/gopo.kicad_pcb` dosyasıdır. Anlamlı her aşamada aynı dosyaya kaydet. Ara çıktıları `hardware/docs/` altında tut; alternatif PCB adını sessizce aktif kart yerine geçirme.
- Düzenleme öncesi `git status --short`, kartın kopyası, DRC ve bağlantı sayısını kaydet. Düzenleme sonrası karşılaştır; beklenmeyen dosyaları değiştirme.
- Kartı tek yazıcı düzenlesin. Başka süreçler aynı anda yalnız okuyabilir.
- Her aşamanın sonunda ilgili bakır katmanlarını, ipek baskıyı ve gerekirse 3D görünümü **gözle** incele. DRC'nin temiz olması yerleşimin üretilebilir ve kullanılabilir olduğunu tek başına kanıtlamaz.
- `kicad-cli` ve kurulu KiCad sürümünün PCB API'si uygunsa bunları kullan. KiCad IPC/kiPy erişilebiliyorsa canlı kart düzenlemesinde tercih et. Araç seçiminde kartı açıp kaydedebilme ve sonuçları tekrar okuyabilme koşuldur.
- KiCad 10 `pcbnew` Python arayüzünde aynı süreçte art arda kart yükleyip footprint eklemek/kaldırmak, sonraki `Pads()`/`GetFootprints()` çağrılarını `SwigPyObject` olarak döndürebiliyor. Bu depoda REV_C eşitlemesinde görüldü. Toplu değişiklikleri geçici kartta, gerekirse her ekleme/kaldırma için ayrı Python sürecinde yap; yeniden yükleyip pad/net eşleşmesini doğruladıktan sonra aktif karta aktar.
- Otomatik yönlendirmeyi varsayılan yapma. Kritik yolları elle planla ve çiz; karmaşıklık bunu gerektirirse ayrı bir değerlendirme yap.

## Bu oturumun sınırları

- **Şematik dosyaları ve şematik kütüphaneleri değiştirme.** Layout sırasında bulunan şematik hata, gerekli pin değişimi veya önerilen devre düzeltmesini `todo.txt` içine referans, pin/net, gerekçe ve beklenen etkiyle yaz. PCB'de şematikle çelişen geçici bir bağlantı üretme.
- Mevcut klasör düzenini koru. Projeye özgü footprint veya düşük ayrıntılı 3D model gerekiyorsa mevcut `hardware/libraries/` yapısını kullan.
- `design_decisions/output/PCB_LAYOUT_YOL_HARITASI_20260912.md` eski REV_B topolojisini anlatır. Yerleşim kararlarını mevcut REV_C şeması, PCB ve `design_decisions/USB_PD_REV_C_tasarim_kararlari_handoff.md` ile doğrula; eski güç yolu sırasını doğrudan kopyalama.

## Yerleşim sırası

1. Kart sınırını, USB-C oyuntusunu, panel kablolarını, TFT FPC yönünü, enkoder milini, butonları ve pil değiştirme alanını ölç. Konnektörlerin takma yönünü ve çevresindeki erişim hacmini 3D'de kontrol et. Kasa ölçüsü kesinleşmemişse varsayımı açıkça kaydet.
2. Her footprint için pad numarası, yön, courtyard, üretici land pattern'i ve mümkünse 3D modeli denetle. Kötü veya eksik modeli mevcut proje kütüphanesinde düzelt; mekanik inceleme için gerekirse basit 3D model oluştur.
3. USB-C, koruma, PD kontrolcü, iki güç kolu, şönt/INA228, TPS55340, AOZ1284, ESP32 anteni ve kullanıcı arayüzünü işlevsel kümeler halinde yerleştir. Kritik akım döngüleri ve bağlantı sırası üzerinden gerekirse üst düzey yerleşimi yeniden kur.
4. Önce güç yolu ve anahtarlamalı dönüştürücülerin sıcak döngülerini, sonra Kelvin ölçümünü, USB D+/D− çiftini ve düşük hızlı sinyalleri yönlendir. En kısa iz tek hedef değildir; dönüş akımının kesintisiz yolu, ısı, EMI ve mekanik erişim birlikte değerlendirilir.
5. GND ve güç alanlarını doldur, sonra izole bakır adalarını, dar boğazları, via dizilerini ve dönüş yolu kopmalarını denetle. Uygun yerlerde GND stitching via kullan; yüksek frekanslı düğümler yanında gereksiz bakır veya kuplaj oluşturma.

## Bu kartın kritik kuralları

- Dört katmanlı hedef: F.Cu kritik döngüler ve bileşenler; In1.Cu mümkün olduğunca kesintisiz GND; In2.Cu güç dağıtımı; B.Cu ikincil sinyaller ve GND. Gerçek üretici stack-up'ı gelmeden USB empedansı veya 5 A sıcaklık artışı için kesin geometri ilan etme.
- ESP32-C6 anten keepout'unu tüm katmanlarda ve 3D mekanikte doğrula. Metal kasa ve kabloların anten önünü kapatmadığını kontrol et.
- USB D+/D− çiftini ESD korumadan ESP32'ye kısa ve benzer uzunlukta, sürekli GND referansı üzerinde götür. Coplanar GND eklemek empedansı değiştirir; üretici stack-up hesabına kat.
- Şöntün iki Kelvin izi doğrudan ilgili şönt padlerinden alınır; yük akımı bu izlerden geçmez. INA228'i şönte yakın tut ve anahtarlama düğümlerinden uzaklaştır.
- TPS55340 ve AOZ1284 giriş/anahtarlama/çıkış akım döngülerini küçük tut. SW/LX bakırını gerektiğinden fazla büyütme; FB/COMP izlerini sessiz bölgede tut. Termal via'nın bağlandığı neti pad/netlist ile doğrula.
- Kullanıcı çıkışındaki M1/M2, AP74502Q, zener ve şönt bağlantılarını mevcut REV_C netleriyle karşılaştır. Q3/Q4 dahili besleme kolunda kalır; iki kol PCB'de yanlışlıkla birleşmemeli.
- 5 A yolunda pad çıkışları, konnektörler, FET'ler, şönt, katman geçişleri ve polygon boyunları tek tek incelenir. Via sayısı ve bakır kesiti akım/ısı hesabıyla doğrulanır.
- GND stitching via'ları dönüş yolunu iyileştirdiği yerde kullan; anten keepout'una, hassas ölçüm aralığına veya farklı potansiyeldeki güç polygonuna rastgele yerleştirme.

## Doğrulama ve kayıt

- Her anlamlı aşamada footprint/net envanteri, kart sınırı, açık bağlantı sayısı ve DRC sonucunu kaydet. DRC bulgularını gerçek kısa devre, clearance, courtyard, silk ve kasıtlı/harici engeller olarak incele; sayıyı tek başına başarı ölçütü yapma.
- Katman görüntülerinde güç yollarını ve GND dönüşünü, 3D'de konektör yönlerini ve kasa temasını kontrol et. Şematik kaynaklı sorunları `todo.txt` dosyasına yaz; şematikleri değiştirme.
- Son kontrolde PCB ile şematik netlist eşleşmesini, sıfır açık bağlantıyı, DRC'yi, üretici stack-up'ını, 5 A ısıl marjını ve mekanik erişimi raporla. Prototip doğrulama gerektiren noktaları açık bırak.
- Yalnız ilgili dosyaları stage et; `git add -A` kullanma. Kullanıcı istemedikçe commit veya push yapma.
