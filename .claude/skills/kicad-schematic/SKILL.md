---
name: kicad-schematic
description: Bu depodaki KiCad şemalarını üret, değiştir ve temizle. Şemaya bileşen/blok eklerken, yerleşimi düzeltirken veya bir handoff dokümanındaki tasarım kararlarını uygularken kullan.
---

# KiCad şema çalışması — gopo deposu

Yöntem ve kurallar `references/kistack-schematic-SKILL.md` dosyasına dayanır
(American Embedded, MIT). Aşağıdakiler o kuralların bu depoya uyarlanmış hali
ve bu depoda çalışırken pahalıya mal olan tuzaklardır.

## Temel döngü

Şemayı görmeden temiz çizemezsin. Her değişiklikten sonra:

```
üret → render et → GÖRÜNTÜYE BAK → düzelt → tekrar
         ⌊ her turda ERC + netlist ile deterministik doğrula
```

```bash
SK=.claude/skills/kicad-schematic/scripts
cd hardware

# sayfaları listele
python3 ../$SK/render.py gopo.kicad_sch --list

# bir bölgeye yakınlaş (mm cinsinden), sonra çıkan PNG'yi Read ile aç
python3 ../$SK/render.py gopo.kicad_sch --page 10 --crop 255 26 410 128 -o /tmp/r

# ERC + netlist; değişiklik öncesi referansı kaydet, sonra karşılaştır
python3 ../$SK/verify.py gopo.kicad_sch --save /tmp/base.net
python3 ../$SK/verify.py gopo.kicad_sch --against /tmp/base.net
python3 ../$SK/verify.py gopo.kicad_sch --show PD_VOUT V_PRE GND
```

Görüntüye bakmadan "tamam" deme. Tek turda olmaz; 3-5 tur normaldir.

## Üretim modülü

`scripts/kisch.py` sembol yerleştirme, tel, etiket, junction, dikdörtgen ve
metin üretir. Pin koordinatı için `xf(konum, açı, lib_pin)` kullan.

```python
import sys; sys.path.insert(0, '.claude/skills/kicad-schematic/scripts')
import kisch as K
t = open('powergeneration.kicad_sch', encoding='utf-8').read()
t = K.ensure_lib_symbol(t, 'libraries/Power_Path_Custom.kicad_sym', 'TPS55340PWPR', 'Power_Path_Custom')
pins = K.lib_pins(t, 'Power_Path_Custom:TPS55340PWPR')
vin  = K.xf((320.04, 76.2), 0, pins['3'])     # VIN pininin mutlak konumu
t = K.insert(t, K.wire(vin, (vin[0], 48.26)))
```

## Bu depoda geçerli kurallar

**Izgara** 1.27 mm. Her koordinat katı olmalı; değilse KiCad'de sürüklerken kayar.

**Pasifler** IC pinlerine *gerçek tellerle* bağlanır (dekuplaj, pull-up/down,
SS, FREQ, kompanzasyon). Etiket yalnızca bloklar/sayfalar arası ve
okunabilirlik düğümlerinde (`BOOST_SW`, `BOOST_FB` gibi).

**Direnç sembolü** `Device:R_Small_US`. Kondansatör ve bobin standart.

**Değerlerde birim var**: `100kR`, `78.7kR`, `9.76kR`, `47nF`, `10uF 50V`, `6.8uH`.
Ohm için `R`, omega işareti değil. Depodaki mevcut stil budur.

**Güç sembolleri**: GND daima aşağı, pozitif raylar daima yukarı bakar.
Referansı (`#PWR###`) **gizle**, değeri **göster**. Tersini yaparsan sayfa
`#PWR232` gibi kalabalıkla dolar ve `+3.3V` etiketi kaybolur. `power()`
yardımcısı bunu doğru yapar.

**PWR_FLAG** kaynağın yanına konur (regülatör/diyot çıkışı), rastgele yere değil.

**Bir IC'nin birden çok toprak pini** (AGND/PGND/PowerPAD) tek GND sembolünde
köprülenir, her pine ayrı sembol konmaz.

**Alt devreler** kesikli dikdörtgen içine alınır ve kısa kalın başlık yazılır.

**Renk** ilgili netleri ayırmak için: güç rayları ayrı, anahtarlama düğümü ayrı.
Bir bloktaki her teli aynı renge boyamak işe yaramaz.

## Pahalıya mal olan tuzaklar

**Gizli `power_in` pinleri ada göre otomatik bağlanır.** TPS55340'ın PGND 13/14
pinlerini istiflenmiş ve gizli yaparsan KiCad onları `PGND` adlı ayrı bir nete
bağlar, GND'ye değil. ERC `multiple_net_names` ile yakalar. Güç pinlerini asla
gizleme; `passive` pinleri gizleyebilirsin.

**Etiket telin tam üstünde olmalı.** 0.64 mm kayma `label_dangling` verir.
Etiketi hep bir tel segmentinin koordinatına koy.

**Döndürülmüş sembolde metin de döner.** `prop_rot` ile geri al: 270 derece
döndürülmüş sembolde metni yatay tutmak için `prop_rot=90`.

**Pin dönüşümü** (bu depoda U6/D2 üzerinden ampirik doğrulandı):

| açı | dönüşüm |
|---|---|
| 0 | `(x+px, y-py)` |
| 90 | `(x-py, y-px)` |
| 180 | `(x-px, y+py)` |
| 270 | `(x+py, y+px)` |

**Güç rayının adı `+3.3V`**, `+3V3` değil. Yanlış yazarsan beslenmeyen ayrı bir
net oluşur ve `power_pin_not_driven` hatası alırsın.

**`#PWR` referansları benzersiz olmalı.** Tekrarlarsa netlist dışa aktarımı
"annotation errors" uyarısı verir. `next_power_ref()` kullan.

**Sadece passive pinlerden beslenen yeni ray** (diyot katodu gibi) "driven"
görünmez; o raya `PWR_FLAG` ekle.

**Sembolü `extends` ile türetilmiş halde kopyalama.** KiCad'in `SMAJ30A`
sembolü `SM6T6V8A`'dan türüyor; parent olmadan kütüphane yüklenmez.
`ensure_lib_symbol` bunu yakalar, önce bağımsızlaştır.

**Sembol düzenledikten sonra pin numarası→ad eşlemesini datasheet'le karşılaştır.**
Kutu genişletmek güvenlidir, pin adı değiştirmek değil.

**Blok A4'e sığmıyorsa sayfayı A3 yap** — sıkıştırmaya çalışma.

## Parça seçimi

Bu skill parça *seçmez*. Değeri veya MPN'i belirsiz olan parçayı jenerik
sembolle yerleştir ve değerine `TBD` yaz; gereksinimleri `todo.txt` dosyasına
kaydet. MPN uydurma.

Datasheet gerekiyorsa indir. TI (`ti.com/lit/ds/symlink/<parça>.pdf`) erişilebilir;
Diodes ve Mouser bot korumasıyla 403/404 verir. Pinout'u `pdftotext -layout` ile
"Pin Functions" tablosundan çıkar, PDF'teki referans devre şekillerine görüntü
olarak bak.
