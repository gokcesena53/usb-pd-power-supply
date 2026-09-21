---
name: kicad-schematic
description: Bu depodaki KiCad şemalarını üret, değiştir ve temizle. Şemaya bileşen/blok eklerken, mevcut bir bloğun yerleşimini/çizimini düzeltirken, bir sembolü başka bir parçayla değiştirirken (ör. RTC veya ekran konnektörü değişimi), blokları sayfalar arasında taşıyıp sayfaları birleştirir/kaldırırken, bir handoff dokümanındaki tasarım kararlarını uygularken, komponent alanlarını (property/BOM üstverisi, tedarikçi BOM'undan MPN/SelectionNote aktarımı) düzenleyip görünürlüğünü ayarlarken, proje footprint'i çizip önizlerken veya şemanın okunabilirliğini (üst üste binen metin, tel üstüne basan değer, çerçeveden taşan etiket/not, üst üste binen sembol gövdesi) denetlerken kullan.
---

# KiCad şema çalışması — gopo deposu

Yöntem ve kurallar `references/kistack-schematic-SKILL.md` dosyasına dayanır
(American Embedded, MIT). Aşağıdakiler o kuralların bu depoya uyarlanmış hali
ve bu depoda çalışırken pahalıya mal olan tuzaklardır.

## Temel döngü

Şemayı görmeden temiz çizemezsin. Her değişiklikten sonra:

```
üret → render et → GÖRÜNTÜYE BAK → düzelt → tekrar
         ⌊ her turda ERC + netlist + lint ile deterministik doğrula
```

```bash
SK=../.claude/skills/kicad-schematic/scripts
cd hardware

# sayfaları listele
python $SK/render.py gopo.kicad_sch --list -o <scratch>/r

# bir bölgeye yakınlaş (mm), çıkan PNG'yi Read ile aç
python $SK/render.py gopo.kicad_sch --page 10 --crop 255 26 410 128 -o <scratch>/r
# aynı PDF'ten başka bölge: yeniden export etmeden
python $SK/render.py gopo.kicad_sch --page 12 --crop 170 34 358 122 -o <scratch>/r --reuse

# ERC + netlist; değişiklik ÖNCESİ referansı kaydet, sonra karşılaştır
python $SK/verify.py gopo.kicad_sch --save <scratch>/base.net
python $SK/verify.py gopo.kicad_sch --against <scratch>/base.net
python $SK/verify.py gopo.kicad_sch --show PD_VOUT V_PRE GND

# üst üste binen metin / tel üstüne basan değer / çerçeve taşması /
# gövde-gövde çakışması (render'a bakmadan önce)
python $SK/readability.py usb_pd_controller.kicad_sch mcu.kicad_sch

# yeni/değişen proje footprint'ini önizle (ped, silk, fab, courtyard)
python $SK/render.py --footprint libraries/Connector_FPC_Custom.pretty <AD> -o <scratch>/fp
```

`readability.py` bulgu **vermiyorsa** metin yerleşimi temizdir; bulgu **veriyorsa**
önce o bölgeyi render et, sonra oynat — denetçi kaba gövde kutuları kullandığı için
sahte pozitif üretebilir (bkz. tuzaklar).

Görüntüye bakmadan "tamam" deme. Tek turda olmaz; 3-5 tur normaldir.
Yerleşim/çizim düzenlemesinde hedef: **`netlist farki: YOK`**, ERC sayısı
değişmemiş, `lint()` boş (bilinçli kesişmeler hariç).

Blok başka sayfaya taşındığında net **adları** değişir (`/POWER GENERATION/LX_SW`
-> `/USB_PD_CONTROLLER/LX_SW`); o zaman hedef **`baglanti farki: YOK; N net
yeniden adlandi`**. `KAYIP`/`YENI` satırı çıkarsa bağlantı gerçekten koptu.

Sayfa numaraları **her oturumda `--list` ile doğrulanır**; sayfa eklenince,
silinince veya proje KiCad'de bir kez kaydedilince kayar. REV_C birleştirmesinden
sonra: 1 kök (blok diyagramı), 2 USB_C_INPUT, 3 USB_PD_CONTROLLER (tüm güç
zinciri, A3), 4 MCU, 5 USER INTERFACE, 6 USER (yalnız tasarım notları).

Bilinçli devre düzeltmesinde (kullanıcı onaylı) hedef: netlist farkı **yalnızca**
beklenen netler. Referans netlist'i oturum başında bir kez al, sayfalar arasında
yenileme; toplam fark her adımda aynı beklenen listeyi göstermeli.

### Ortam

- Linux'ta `kicad-cli` PATH'tedir; `python` yok, **`python3`** kullan (bu
  dosyadaki örneklerde `python` = Windows). PyMuPDF yoksa `render.py`
  `pdftoppm`'e düşer (`--crop`/`--dpi` aynı çalışır, çıktı adı
  `<ad>-<sayfa>.png` olur). `--footprint` PNG için PyMuPDF veya `cairosvg`
  ister; ikisi de yoksa yalnız SVG üretir (`pip install cairosvg` bir venv'de).
- KiCad'in kendi sembol kütüphaneleri (`Timer_RTC`, `Device`, `Transistor_FET`,
  `Connector_Generic`...) Linux'ta `/usr/share/kicad/symbols`;
  `kicadtools.kicad_symbol_lib(nick)` bulur, `KICAD10_SYMBOL_DIR` önceliklidir.
- Windows'ta `kicad-cli` PATH'te değil; `kicadtools.kicad_cli()`
  `%LOCALAPPDATA%\Programs\KiCad\*\bin` altında bulur. Başka yerdeyse
  `KICAD_CLI` ortam değişkenini ayarla.
- **KiCad'in `bin` dizinini PATH'in önüne ekleme**: KiCad'le gelen python öne
  geçer, PyMuPDF bulunamaz. Betikleri `python` (C:\Python314) ile çağır.
- `pdftoppm` yok; `render.py` PyMuPDF (`fitz`) ile rasterleştirir.
- `kicad-cli` her çalıştığında `gopo.kicad_pro`'yu (yalnız satır sonları) yeniden
  yazar. `render.py`/`verify.py` dosyayı bayt bayt geri koyar; kendi `kicad-cli`
  çağrında `kicadtools.keep_file` kullan veya `git checkout -- gopo.kicad_pro`.
- Satır sonu dosyaya göre değişir: şema sayfaları ve `.kicad_sym`'lerin çoğu
  **LF** (KiCad Linux'ta kaydetti), Windows'ta çizilmiş footprint'ler
  (`Molex_541324062`, `Power_Output_Custom/*`, `TPS61023_DRL0006A`) **CRLF**.
  Varsayma, dosyanın kendisine uy: `kicadtools.read_sheet` / `write_sheet`
  mevcut satır sonunu korur; yeni footprint'i aynı kütüphanedeki komşusunun
  satır sonuyla yaz.
- Değerlerde `Ω` geçen sayfalarda (usb_pd_controller, mcu) konsola yazdırmak
  `UnicodeEncodeError: 'charmap'` verir: `PYTHONIOENCODING=utf-8` ile çalıştır.

## Modüller

| dosya | iş |
|---|---|
| `kisch.py` | yeni öğe üretimi: `sym`, `power`, `wire`, `wires`, `label` (global etikette `shape`), `junction`, `no_connect`, `rect`, `text`, `xf`, `lib_pins`, `lib_body`, `text_width`, `text_box`, `boxes_overlap` |
| `kisch_edit.py` | mevcut sayfada düzenleme — envanter: `inventory`, `power_symbol_nets`, `label_shapes`, `dump`; değişiklik: `strip_region`, `place`, `translate_region`, `move_text`, `remove_texts` (`prefixes=`), `Pool`; **alanlar**: `sym_props`, `set_sym_props` (`visible=None`), `field_geometry`, `field_visibility`, `field_boxes`, `sym_body`, `prop_escape`; silme: `remove_items` (koşula göre öğe); denetim: `sym_pin`, `pin_at`, `lint`; kütüphane: **`swap_lib`** (sembolü başka kütüphane sembolüyle değiştir), **`prune_lib_symbols`**, `edit_lib_symbol`, `hide_pin_texts`, `hide_stacked_pins` |
| `kisch_sheet.py` | sayfalar arası: `move_block` (blok + instance yolu + lib_symbols), `remove_sheet` (boş sayfa + sayfa sembolü + .kicad_pro kaydı), `set_paper`, `is_empty` |
| `kicadtools.py` | `kicad_cli()`, `kicad_symbol_lib(nick)`, `read_sheet`/`write_sheet` (satır sonu korunur), `keep_file` |
| `render.py` | PDF export + kırpılmış PNG; `--footprint PRETTY AD` footprint önizlemesi (`render_footprint`) |
| `verify.py` | ERC sayıları + netlist farkı; `--against` net adı değişimini gerçek bağlantı kaybından ayırır (`signature`) |
| `readability.py` | üst üste binen metin, tel/gövde üstüne basan sembol alanı, gövdesinden tel geçen global etiket, **çerçeveden taşan** etiket/not/alan (`frame_overflow`), **üst üste binen sembol gövdeleri** (`body_overlaps`, güç sembolü dahil); CLI çıkış kodu = bulgu sayısı |

### Yeni blok üretmek

```python
import sys; sys.path.insert(0, '../.claude/skills/kicad-schematic/scripts')
import kisch as K
from kicadtools import read_sheet, write_sheet
t, crlf = read_sheet('usb_pd_controller.kicad_sch')
t = K.ensure_lib_symbol(t, 'libraries/Power_Path_Custom.kicad_sym', 'TPS55340PWPR', 'Power_Path_Custom')
pins = K.lib_pins(t, 'Power_Path_Custom:TPS55340PWPR')
vin  = K.xf((320.04, 76.2), 0, pins['3'])     # VIN pininin mutlak konumu
t = K.insert(t, K.wire(vin, (vin[0], 48.26)))
write_sheet('usb_pd_controller.kicad_sch', t, crlf)
```

### Mevcut bloğu yeniden yerleştirmek

Sembolleri **silip yeniden oluşturma**; taşı. uuid, footprint, MPN ve instance
korunur, diff okunur kalır. Akış (tam örnek `kisch_edit.py` başındaki docstring'de):

1. `verify.py --save` ile referans netlist'i al. Temizlemeden önce:
   `print(E.inventory(t, V.parse(net)))` (her pinin adı, konumu ve **neti**),
   `E.power_symbol_nets(t, net)` (PWR_FLAG netlist'te yok; hangi nette olduğunu
   buradan öğren), `shape = E.label_shapes(t)` (global etiket yönleri).
   Envanterdeki `unconnected-(...)` pinlerine bak: eski ERC hatası gerçek bir
   bağlantı hatası olabilir (bkz. tuzaklar).
2. **Önce kâğıt üstünde koordinat planı yap**: her kolonun x'i, her satırın y'si,
   metinlerin kapladığı alan (`K.text_width`). Planı yapmadan betiği yazma.
3. `E.strip_region(t, kutu)` → tel/etiket/junction/no_connect/metin/çerçeve ve
   güç sembolleri gider; `E.Pool(freed, K.next_power_ref())` ile `#PWR`'leri
   geri kullan. `no_connect` işaretleri de silinir, **yeniden ekle**. Tasarım
   notlarını korumak için `kinds`'tan `'text'` çıkar, notları `E.move_text` ile
   taşı ve kendi başlıklarını her çalıştırmada `E.remove_texts` ile sil.
4. `E.place(...)` ile sembolleri taşı; her kullandığın pini `E.pin_at(t, ref, n,
   planlanan)` ile doğrula (ayna/açı/asimetrik pin hatası anında yakalanır).
5. Telleri, etiketleri (`shape=shape[ad]`), güç sembollerini `K.*` ile üret, `K.insert`.
6. `verify.py --against`, `E.lint(t, kutu)`, render, bak. Betiği tekrar
   çalıştırılabilir yaz: strip yeni çizimi de siler, place mutlak konum yazar.

Betiği scratchpad'de tut; depoya yalnız sonuç şema girer.

### Bir sembolü başka parçayla değiştirmek

RV-3028-C7 → BQ32000, `Conn_01x40` → `Conn_01x30` (NHD-2.4 → TFT032B018) gibi
parça değişimlerinde de sembolü silme; **`E.swap_lib`** ile değiştir. Referans,
uuid, instance ve alanlar korunur (PCB'de footprint eşleşmesi kopmaz).

```python
t = E.swap_lib(t, 'U4', 'Timer_RTC:BQ32000')      # KiCad sistem kutuphanesinden
t = E.swap_lib(t, 'J3', 'Connector_Generic:Conn_01x30')
t = E.swap_lib(t, 'U9', 'Power_Path_Custom:X', lib_path='libraries/Power_Path_Custom.kicad_sym')
```

`swap_lib` lib_id'yi değiştirir, yeni tanımı önbelleğe kopyalar, `(pin "N")`
uuid kayıtlarını yeni sembolün pinlerine eşitler (40→30'da 31..40 silinir) ve
kullanılmayan eski tanımı `prune_lib_symbols` ile atar. Sonrası normal akış:
pin konumları değiştiği için bölgeyi strip et, `place` + `pin_at`, yeniden çiz,
alanları `set_sym_props` ile yaz (Value, Footprint, Datasheet, Description,
grup alanları). Beklenen netlist farkını önceden listele; `--against` yalnız o
netleri göstermeli (RTC: `RTC_*` pin numaraları, `Net-(U4-OSCI/OSCO/VBACK)`).

- Kalkan parçaları `E.remove_items(t, lambda k, b: k == 'symbol' and
  E.ref_of(b) in {...})` ile sil, ardından **`E.prune_lib_symbols(t)`**: BT1
  silindiğinde `Device:Battery_Cell` önbellekte kalmıştı, userinterface'te
  kullanılmayan `AO3400A` tanımı vardı (ikisi de prune testiyle bulundu).
- `Device:C` → `Device:C_Polarized` gibi polarite kazanan değişimde önce
  netlist'ten **pin 1'in pozitif rayda** olduğunu doğrula (C15.1 `+3.3V`,
  C29.1 `PD_VOUT`); değilse sembolü çevir.
- Yeni parça için kütüphanede birebir sembol yoksa genel sembol yeterli:
  SOT-23 G-S-D MOSFET'ler (BSS138, IRLML6344) → `Transistor_FET:Q_NMOS_GSD`;
  4 pedli kristal (ABS25: 1–4 kristal, 2–3 NC) → `Device:Crystal_GND23`
  (2 ve 3 gizli istifli GND; `Crystal_GND24` 1–3 kristaldir, uymaz).
  Pin eşlemesini footprint ve datasheet ile karşılaştır.
- Yeni proje footprint'i çizince `render.py --footprint` ile bak: ilk KLS/Korchip
  denemelerinde silk pedlerin üstünden geçiyordu (yay ile böl) ve courtyard
  pedi kapsamıyordu (pedleri de içine alan dikdörtgen).

### Komponent alanlarını (property) düzenlemek

Alan standardı `design_decisions/standards/komponent-field-standardi.csv`; çekirdek
katman `design_decisions/standards/kicad-field-templates.py` ile `.kicad_pro`'nun
Field Name Templates listesine yazılır (yeni sembollerde hazır gelsin diye).

```python
props = E.sym_props(blk)                 # [(ad, deger, gizli_mi, blok_metni)]
want  = [('Reference', ref), ('Value', val), ('Footprint', fp), ('Datasheet', ds),
         ('Description', desc)] + [(f, vals.get(f, 'TBD')) for f in grup_alanlari]
blk   = E.set_sym_props(blk, want, visible=('Reference', 'Value'))
```

`set_sym_props` mevcut alanın **bloğunu korur** (konum, hizalama, font, açı) ve
yalnız ad/değer/gizliliği değiştirir; yeni alanı sembol konumunda gizli üretir.
Bu yüzden elle ayarlanmış Reference/Value yerleşimi bozulmaz.

Kurallar:
- **Görünürlük tek kural**: yalnız `Reference` + `Value`. Depoda `Description`
  119 sembolde açıktı ve sayfaları dolduruyordu.
- Güç sembolleri ayrı: Reference daima gizli, `GND`/`PWR_FLAG` değeri gizli,
  pozitif raylar (`+3.3V`) görünür. TestPoint'in `"TestPoint"` değeri gizli.
- **Value parametrik değerdir**, MPN değil: `L1` = `22u` (MPN alanına
  `SRI0704-220M`), `D2` = `SS2060FL` (MPN'e tam sipariş kodu). Value'dan çıkan
  gerilim/güç/tolerans kendi alanına gider (`10uF 50V` -> `10u` + `VoltageRating`).
- Eski/eş anlamlı alanları standarda birleştir: `Manufacturer Part Number`/
  `DisplayMPN` -> `MPN`, `Voltage` -> `VoltageRating`. `Sim.*` alanları KiCad'in
  simülasyon alanlarıdır, korunur.
- Bilinmeyen zorunlu alana `TBD` yaz — KiCad'in Symbol Fields Table'ında
  filtrelenir ve eksik sayılabilir. **MPN veya datasheet parametresi uydurma**;
  yalnız depodan (footprint, lib_id, BOM, tasarım notu) doğrulanabileni doldur.
- Betiği **yeniden çalıştırılabilir** yaz: `set_sym_props` idempotenttir, tüm
  alan listesini her seferinde baştan verir.
- **Veri aktarımında görünürlüğe dokunma: `visible=None`.** Varsayılan
  `visible=('Reference', 'Value')` görünürlüğü standarda *zorlar*; tedarikçi
  BOM'undan MPN/SelectionNote aktarırken bu, bilinçli gizlenmiş Value'ları
  açtı (13 TestPoint + J7). `visible=None` mevcut görünürlüğü korur, yeni
  alanları gizli üretir.
- Tedarikçi BOM'u aktarımı: MPN/Manufacturer yalnız stoktan **seçilmiş** parçaya
  yazılır; stokta yoksa tasarım MPN'i kalır, durum/öneri `SelectionNote`'a
  (`Özdisan <kod>; stok N (tarih); durum. not`). Parametrik alanları yalnız
  tedarikçi kaydından/datasheet'ten doldur, doğrulanmayanı `TBD` bırak.

Doğrulama, çizim işlerinden farklı: hedef **`netlist farki: YOK`** *ve*
`E.field_geometry()` farkının **boş** olması. İkincisi "hiçbir sembol veya metin
oynamadı"ı kanıtlar; alan işi asla yerleşimi değiştirmemelidir.

```python
before, vis = E.field_geometry(t), E.field_visibility(t)   # islemden ONCE
...                                                          # alanlari duzenle
assert E.field_geometry(t2) == before
assert all(E.field_visibility(t2)[k] == v for k, v in vis.items())  # yeni alanlar haric
```

### Blokları başka sayfaya taşımak / sayfaları birleştirmek

```python
import kisch_sheet as S
S.move_block('kaynak.kicad_sch', 'usb_pd_controller.kicad_sch',
             (17, 33, 166, 122), dx=0, dy=190.5)     # kutu = kaynak sayfadaki çerçeve
S.set_paper('usb_pd_controller.kicad_sch', 'A3')
S.remove_sheet('kaynak.kicad_sch', 'gopo.kicad_sch', 'gopo.kicad_pro')
```

Sıra: **taşı → doğrula → yerine çiz → artıkları temizle → boş sayfayı kaldır.**

1. `move_block` tüm bloğu (sembol + tel + etiket + çerçeve) taşır, sembolün
   `instances/path`'ini hedef sayfanınkiyle değiştirir ve eksik `lib_symbols`'ı
   kopyalar. Hemen `verify.py --against` çalıştır: sonuç
   `baglanti farki: YOK; N net yeniden adlandi` olmalı.
2. Taşınan blok yeniden çizilecekse **hem eski hem yeni bölgeyi** `strip_region`
   ile temizle; yoksa eski konumdaki teller öksüz kalır (ERC
   `unconnected_wire_endpoint` + `endpoint_off_grid` yağar).
3. Bloklar arası eski teller kaynak sayfada değil hedef sayfada kalır ve
   parça parça kayar. `lint` bunları `ust uste yatay tel` / `T baglanti junction
   yok` olarak raporlar; `E.remove_items` ile konumlarını vererek sil.
4. Alt sayfa sembolleri (`sheet`) `items()` kapsamında değildir: taşınmaz,
   silinmez. Taşınan bloğun içinde kalırlarsa ayrıca ele al.
5. Tek sayfada kalan global etiketleri (ör. `PD_VBUS_SENSED`, `SW_OUT`) yerel
   etikete indir; ad aynı kalırsa yalnız kapsam değişir, bağlantı değişmez.
6. Boş kalan sayfayı `remove_sheet` ile kaldır: dosya + üst sayfadaki sembol +
   `.kicad_pro` kaydı birlikte gider (fonksiyon JSON'u doğrular). Sayfa boş
   değilse hata verir.

**Çok adımlı yeniden yapılandırmayı tek "yeniden üretim" betiğinde topla**:
taşımalar, blok çizimleri, temizlik ve sayfa silme sırayla o betikte olsun,
commit edilmiş durumdan çalıştırılabilsin. Ara adımda bir şey bozulursa
`git checkout -- hardware/` + betiği baştan çalıştır yeterli olur.

## Bu depoda geçerli kurallar

**Izgara** 1.27 mm. Her koordinat katı olmalı; değilse KiCad'de sürüklerken kayar.
Metin konumları ızgaraya bağlı değildir.

**Pasifler** IC pinlerine *gerçek tellerle* bağlanır (dekuplaj, pull-up/down,
SS, FREQ, kompanzasyon, kapı sürücü ağı). Etiket yalnızca bloklar/sayfalar arası
ve okunabilirlik düğümlerinde (`BOOST_SW`, `BOOST_FB`, `GATE_DRV` gibi). Aynı
sayfa içinde iki noktayı etiket eşleşmesiyle bağlamak zayıf çizimdir.

**Direnç sembolü** `Device:R_Small_US`. Kondansatör ve bobin standart.

**Value, IEC 60062 kodudur** (`komponent-field-standardi.csv`, satır 3):
`4k7`, `78k7`, `9k76`, `100k`, `22R`, `5m0`, `100n`, `2u2`, `10u`, `6u8`.
Çarpan harfi ondalık noktanın yerine geçer; omega işareti kullanılmaz (`Ω`
geçen sayfalarda konsola yazdırmak `UnicodeEncodeError` veriyordu).
Gerilim/güç/tolerans/dielektrik Value'ya YAZILMAZ, kendi alanına gider.
IC, diyot, konnektör ve modülde Value ürün adıdır (`AP33772SDKZ-13-FA02`),
tam sipariş kodu `MPN` alanındadır.

REV_C'de tüm sayfalar bu biçime çevrildi (`10 kΩ`/`4,7k`/`100K`/`10kR` karışıktı).
Eski `100kR` stili artık kullanılmaz.

**Güç sembolleri**: GND daima aşağı, pozitif raylar daima yukarı bakar.
Referansı (`#PWR###`) **gizle**, değeri **göster**. Tersini yaparsan sayfa
`#PWR232` gibi kalabalıkla dolar ve `+3.3V` etiketi kaybolur. `power()`
yardımcısı bunu doğru yapar.

**PWR_FLAG** kaynağın yanına konur (regülatör/diyot çıkışı), rastgele yere değil.
Başka bir junction'ın 2.54 mm yakınına koyma; iki nokta tek düğüm gibi görünür.

**Bir IC'nin birden çok toprak pini** (AGND/PGND/PowerPAD) tek GND sembolünde
köprülenir: her pinden kısa dikey tel, altta yatay köprü, ortadan tek GND.
Ortadaki tel köprünün **ucunda** bitmeli, içinden geçmemeli.

**Alt devreler** kesikli dikdörtgen içine alınır ve kısa kalın başlık yazılır
(`K.rect`, `K.text`, başlık 2 mm kalın, not 1.4 mm normal). Blok dışındaki
öğeler çerçevenin üstüne düşüyorsa `E.translate_region` ile kenara çek.

**Renk** ilgili netleri ayırmak için: giriş rayı turuncu `(200,120,0)`,
anahtarlama/kapı düğümü mor `(130,0,160)`, regüle çıkış kırmızı `(200,0,0)`.
Kontrol telleri renksiz. Bir bloktaki her teli aynı renge boyamak işe yaramaz.

## Yerleşim kuralları (ölçülü)

Bu değerler REV_C Blok A/B ve usb_pd_controller/mcu düzenlemelerinde render'dan ölçüldü.

**Metin genişliği** 1.27 mm fontta küçük harfli değerlerde ~1.11 mm/karakter,
büyük harf/rakamda ~1.34 mm/karakter (`ESP32-C6-WROOM-1` = 21.4 mm).
`K.text_width` ikisini ayırır. Pasif
metni sembol merkezinden +2.54 mm başlar, kondansatör plakası ±2.03 mm.
→ Yan yana dikey kondansatörler, değer `10uF 50V` ise **15.24 mm** aralık,
en az 13.97 mm. 12.7 mm'de metin komşu sembole değer.

**İki satırlı metin**: ref `(+2.54, -1.27)`, değer `(+2.54, +1.27)`. Sağda yer
yoksa sola yaz: `(-2.54, ∓1.27, 'right')`. Rayın üstündeki yatay bobin/diyot
için ortalı ve üstte: `(0, -6.35, None)` / `(0, -3.81, None)`.

**IC ref/değeri** gövdenin üstünde, sol kenar hizasında: ref `-18.4`, değer
`-16.5` (gövde üst kenarı -15.24 ise). 1.9 mm'den sık satır üst üste biner.

**Yatayda yer yoksa sıkıştırma, iki satıra böl.** Üst satır güç yolu (giriş
etiketi → giriş kondansatörleri → bobin/anahtar → çıkış kondansatörleri → çıkış
etiketi), alt satır IC ve kontrol ağı. IC'nin VIN/SW pinleri doğrudan yukarı,
raya çıkar. Sayfada boş dikey alan varsa kullan.

**Aynı kenardaki pinler iç içe L ile çıkar.** Kural telin döndüğü yöne bağlı:
- **Aşağı inen** hatlarda **üstteki** pin daha dışa gider. Blok A: FREQ (üstte)
  R47'ye x=307 ile dıştan, SS (altta) C23'e x=315 ile içten iner.
- **Yukarı çıkan** hatlarda **alttaki** pin daha dışa gider. Blok B: VCAP içte,
  GATE ortada, SRC en dışta yükselir. INA228 bloğu: şönte inen Vin+ (üstte)
  dıştan, Vin− içten → Kelvin çifti kesişmez.

**Dikey pasif sütunları 12.7 mm aralıkla.** Değer metni ("100kR 1%", "12.7kR 1%")
sütunlar arasına taşar: 7.62 mm'de metinleri sırayla sağa/sola yazsan bile komşu
sembole değer (AOZ1284 buck yeniden çiziminde render'dan ölçüldü). Yer yoksa
metni sembolün **altına** al (`ref_at=(0, 5.08, None)`), sütunu daraltma.

**Global etiket gövdesi** ≈ `K.text_width(ad)` + şekil payı: oklu şekiller
(`input`/`output`/`bidirectional`) **+3 mm**, `passive` dikdörtgen **+1 mm**
(render'dan: V_PRE 6.6 mm). Bloğun kenarına etiket koyarken bunu hesaba kat:
"PD_VOUT" ≈ 12.5 mm, "PD_VBUS_SENSED" ≈ 22 mm. Sol kenardaki `rot=180` etiket
için çıpa x ≥ çerçeve x + gövde + 2.54: TFT_BL_PWM çerçeveden 10.16 mm içeride
başlatıldığında 6 mm taştı. `readability.py` artık bunu `tasma` olarak raporlar.

**Not metinleri çerçeveye sığmalı.** 1.27 mm fontta satır ≈ karakter × 1.1 mm;
~60 karakteri geçen satırı böl (RTC notu 72 karakterle çerçeveden 4.3 mm taştı).
Notu çizmeden önce `K.text_width(satır)` ile ölç.

**Güç sembolünü IC gövdesinin köşesine koyma.** Kondansatörün GND'si IC gövdesinin
hemen yanına düşüyorsa kondansatörü bir kolon (2.54 mm) kaydır: C33'ün GND'si
U4'ün sağ üst köşesine oturmuştu; alan denetimi yakalamadı, `body_overlaps`
yakalar.

**Konnektörde çok sayıda GND / besleme pini** (TFT J3, 30 pin, render ile
doğrulandı): ardışık GND pinlerini pinlerin 5.08 mm solunda tek dikey baraya
topla, GND sembolünü baradan **satırlar arasına** (ör. y=49.53) çıkan kısa kolun
ucuna koy — bara ucuna koyarsan sembol alttaki sinyal satırının teline biner.
Besleme pinlerinin hemen üstünde sinyal satırı varsa `+3.3V` yukarı bakamaz:
barayı son pinin altına kadar indir, sola dön, `+3.3V`'u ve dekuplajı orada
konumla. Boş (NC) pinlerin arasından bara geçebilir, NC pinin teli yoktur.

**2.54 mm aralıklı pin sıraları (MCU, konnektör) için:**
- Yatay seri direncin metni satır arasına sığmaz. Komşu satırlardaki dirençleri
  x'te kaydır ve metni sırayla **üste / alta** yaz (mcu: R2 üstte, R3 altta).
- Yukarı bağlanan eleman (pull-up, +3.3V) ancak üstündeki bütün satırlardan
  **daha uzağa** uzanan satırda konabilir. Pull-up'ı satır sonuna yatay koy, güç
  sembolünü direncin ucuna yerleştir. Uzanamayan satırı IC'nin yanından aşağı
  indir (mcu GPIO9: x=171 ile etiket satırlarının dışından iner, BOOT ağı altta).
- Yerel etiket metni telin **üstüne** basılır ve bir üst satırın global etiket
  gövdesine biner. Yerel etiketleri global etiketlerin bittiği x'in dışına al.
- Test noktası daireyi telin üstüne çizer. Satır ortasına konan TP üst satırla
  çakışır. Yer yoksa test noktalarını ayrı bir "TEST NOKTALARI" bloğunda
  etiketle topla; global/yerel etiket adları aynı kaldığı için netlist değişmez.
  TestPoint'in "TestPoint" değerini `hide_val=True` ile gizle.

**Kesişmeyi planarlıkla çöz.** Yerleştirmeden önce sor: bu tel hangi kapalı
döngünün içinden geçmek zorunda? Örnek (Blok B):
- Rayın üstünden gelen bölücü (OV) ile EN pini aynı kenardaysa, bölücü **en dış
  kolon** olur, EN ağı ortada kalır, OV teli EN ağının GND sembolünün altından
  döner.
- Sırt sırta MOSFET'lerde kapı hattı ortak source düğümünü çevreler; SRC teli
  kapı hattını **kesmek zorundadır**. Bu kabul edilebilir tek kesişmedir:
  junction koyma, `lint` onu `kesisme baglantisiz` olarak raporlar.
- Zener gibi iki dikey hat arasındaki eleman, hatların arasına **yatay** konur;
  metni hatların arasında ortalanır.

**Global etiket yönü**: `rot=0` gövde sağa uzar → telin sağ ucunda (çıkış).
`rot=180` gövde sola uzar → telin sol ucunda (giriş). Yanlış yönde tel etiket
gövdesinin altından geçer; ERC temiz kalır ama çizim bozuktur.

## Pahalıya mal olan tuzaklar

**Gizli `power_in` pinleri ada göre otomatik bağlanır.** TPS55340'ın PGND 13/14
pinlerini `power_in` bırakıp gizlersen KiCad onları `PGND` adlı ayrı bir nete
bağlar, GND'ye değil. ERC `multiple_net_names` ile yakalar. İstiflenmiş
pinlerin numaraları üst üste biniyorsa `E.hide_stacked_pins(blok, {'13','14'})`:
fazlalıklar `passive` + gizli olur, bir tanesi `power_in` ve görünür kalır.

**Property açısı sembole GÖRELİ saklanır.** Ekrandaki açı `(sembol_ang +
prop_rot) % 360`'tır; KiCad 180'i okunur yöne çevirir. `R13` ang=90, Reference
rot=270 -> yatay basılır. Mutlak sanarsan metin kutusu 90 derece döner ve
çarpışma denetimi sahte bulgularla dolar (ilk taramada 34 bulgunun çoğu sahteydi,
düzeltince 9'a indi). `E.field_boxes` bu telafiyi yapar; elle hesaplama.

**Etikette rot ile justify aynı yönü iki kez kodlar.** Global etiket `rot=180`
ise KiCad `(justify right)` yazar; gövde yönünü **yalnız rot'tan** hesapla.
İkisini birden uygularsan kutu ters döner: `PD_5V` (rot 180) raporda Q1/Q2 ile
çakışıyor göründü, render'da 8 mm uzaktaydılar. `readability.label_boxes` bunu
doğru yapar.

**Yerel etiketin metni telin ÜSTÜNE kaydırılarak çizilir**, gövdesi yoktur:
tel üzerinde olması doğrudur, bulgu sayma. Global/hiyerarşik etiketin gövdesi
çıpaya oturur; tel çıpada durmayıp gövde yönünde devam ederse yazıyı çizer
(`PD_VOUT` böyle bulundu, render ile doğrulandı). Denetimi yalnız gövdeli
etiketlere uygula — yerel etiketleri de tararsan 16 bulgunun 14'ü sahte çıkar.

**Property bloklarını elle birleştirirken girinti kaybolur.** Bloklar dosyada
`\n\t\t` girintisiyle durur ama `K.block_at` yalnız `(` ile başlayan gövdeyi
verir; `'\n'.join(parts)` ile birleştirirsen ikinci property **sütun 0**'da
başlar. KiCad dosyayı yine okur (ERC ve netlist etkilenmez, render çalışır) ama
`\n\t\t\(property` arayan her araç — `items()`, `sym_props()` — artık yalnız
ilk alanı görür ve betik idempotent olmaktan çıkar; ikinci çalıştırma sembolü
bozar. Ayırıcı `'\n\t\t'` olmalı. Belirti: `grep -c '^(property' *.kicad_sch`
sıfırdan büyük. `E.set_sym_props` kullan, elle birleştirme.

**Otomatik metin kaydırma sembol gövdesini bilmiyorsa gerileme üretir.**
"Çakışmayı azaltan ilk aday" kuralıyla Q1/Q2'nin değeri transistörün üstüne
taşındı: rapor iyileşti, render'da `BSS138` sembolün içine bindi. Aday konumu
kabul etmeden önce `E.sym_body` ile gövde kutularını da denetle **ve her
otomatik yerleşimi render ile doğrula** — denetçi puanı düşmesi yetmez.

**Etiket telin tam üstünde olmalı.** 0.64 mm kayma `label_dangling` verir, ve
etiket bir pini besliyorsa o pin `pin_not_connected` olur. Etiketi hep bir tel
segmentinin *içine* koy — segmentin dışında, uzantısı üzerinde olması yetmez.
Blok B'nin ilk çiziminde `GATE_DRV` etiketi telin başlangıcından 2.54 mm soldaydı;
U12'nin GATE pini ayrı bir nette kaldı ve yalnızca `verify.py --show` ile
yakalandı.

**Telin serbest ucu bir yere bağlanmalı.** Hiçbir pine, etikete veya başka tele
değmeyen uç `unconnected_wire_endpoint` verir. Rayları son bağlantı noktasında
bitir, "biraz uzun olsun" diye uzatma.

**Her koordinat 1.27'nin katı olmalı.** Yarım adım (0.635) kaymalar el ile
koordinat yazarken kolayca sızar ve `endpoint_off_grid` uyarısı verir.
`E.lint` ızgara dışı tel uçlarını raporlar; tek değer için
`assert abs(v / 1.27 - round(v / 1.27)) < 1e-6`.

**Döndürülmüş/aynalı sembolde metin açısı ve hizalama** (KiCad 10, render ile
doğrulandı: usb_pd_controller D1, R4, Q1–Q4, TH1):

| sembol | alan açısı | left/right |
|---|---|---|
| ang 0 | 0 | olduğu gibi |
| ang 90 | **270** | olduğu gibi |
| ang 270 | **90** | olduğu gibi |
| ang 180 | **0** (180 verirsen metin TERS basılır) | **ters** |
| `mirror y` (herhangi açı) | yukarıdaki | **ters** (180 ile birlikteyse tekrar düz) |

Belirtiler: ang 90'da alan açısı 90 verilirse `'right'` sağa uzar, uzun değer
IC'nin üstüne biner (TH1). ang 180'de alan açısı 180 ise "LED D1" ayna yazı gibi basılır.
`E.place` bu tabloyu uygular; `just` her zaman **görüntüdeki** hizalamadır.
`prop_rot` elle verilirse telafi yapılmaz.

**Pin dönüşümü** (U6/D2 ve Q5/Q6 üzerinden ampirik doğrulandı):

| açı | dönüşüm (ayna yok) |
|---|---|
| 0 | `(x+px, y-py)` |
| 90 | `(x-py, y-px)` |
| 180 | `(x-px, y+py)` |
| 270 | `(x+py, y+px)` |

**Ayna dönüşümden SONRA, şema ekseninde uygulanır.** `(mirror y)` yatay
çevirir (dx → -dx), `(mirror x)` dikey (dy → -dy). Kütüphane koordinatında
çevirip sonra döndürmek 90/270'te yanlış pin konumu verir; netlist'te
`unconnected-(Q6-...)` netleri olarak görünür. `K.xf(..., mirror=)` ve
`E.sym_pin` doğru modeli kullanır.

**Sırt sırta (ortak source) MOSFET çifti.** `Transistor_FET:Q_NMOS_GSD` yatay
hatta: `ang=90` drain sola, source sağa, gate aşağı; `ang=270` source sola,
drain sağa ama gate **yukarı**. İlk Blok B çiziminde Q6 `ang=270` idi, gate'ler
ters yönlere baktığı için `GATE_DRV` etiketiyle bağlanmıştı. Daha iyisi:
Q5 `ang=90`, Q6 `ang=90, mirror='y'` → iki gate de aşağı bakar, tek kapı hattı
teliyle U12 GATE'e bağlanır (REV_C Blok B, 9c3d219).

**Tel kesişmeleri ve junction.** Bir telin *ucu* başka telin ortasına değiyorsa
KiCad bağlar; junction koy. İki tel birbirinin *içinden geçiyorsa* ve orada
junction varsa da bağlanır, ama okunmaz. Teli o noktada böl ki uçlar orada
bitsin. `E.lint` üç durumu da raporlar.

**`E.place` gizli alanı görünür yapardı.** `_set_prop` `(hide yes)`'i siliyor ve
yalnız `hide_val` ile Value'ya geri koyuyordu; güç sembolüne `ref_at` verince
`#PWR###` şemada beliriyordu. Artık `hide=None` (varsayılan) **mevcut gizliliği
korur**: Reference'ın gizliliği her zaman korunur, `hide_val` de `None`
verilirse dokunulmaz. Bir alanı bilerek göstermek/gizlemek için `True`/`False`
geç.

**`no_connect` işaretleri bölge temizliğinde silinir.** Yeniden eklemezsen ERC
`pin_not_connected` sayısı artar.

**Pinler sembol merkezine simetrik değildir.** `Device:Battery_Cell`'de + pini
merkezin −5.08, − pini +2.54 mm uzağında. GND'yi simetri varsayarak koyunca
netlist'te `unconnected-(BT1---Pad2)` çıktı. Kullandığın **her** pini
`E.pin_at` ile doğrula, yalnız birini değil.

**Koordinat karşılaştırmasını `==` ile yapma.** `53.34 - 7.62` sonucu
`45.720000000000006` çıkar ve doğru yerleşim `AssertionError` verir. `E.pin_at`
yuvarlayarak karşılaştırır.

**Metinleri silmeyen betik tekrar çalışınca başlıklar üst üste biner.** Aynı
koordinattaki kopya görünmez, kaydırılmış olan çift basılır ("RTC RV-3028"
başlığı böyle bulundu). `E.remove_texts(t, {başlıklar})` ile önce sil.
İçerik **dosyadaki** haliyle eşleşir: çok satırlı notta satır sonu `\\n` (iki
karakter). Notun metnini betikte değiştirdiysen eski hali tam eşleşmez ve
sayfada kalır (RTC ve J3 notları ikilendi): `E.remove_texts(t, prefixes=('TFT032B018',))`.

**Eski ERC hataları gerçek devre hatası olabilir.** `todo.txt`'de yıllanmış
"R6 pin 2 bağlı değil / Q2 pin 3 bağlı değil / PD_I2C_SDA_5V dangling" üçlüsü
aslında SDA seviye dönüştürücüsünün kopukluğuydu (SCL tarafı R5/Q1 doğruydu).
Envanterde `unconnected-(...)` gördüğünde simetrik/eş devreyle karşılaştır;
düzeltme netlist'i değiştirdiği için **kullanıcıya sor**, onaylanırsa beklenen
fark listesini commit mesajına yaz.

**Tek sayfada kullanılan global etiketi kaldırma.** `PD_INT_5V` gibi yalnız bir
yerde geçen global etiket silinirse net adı `Net-(U1-INT)` olur ve netlist farkı
çıkar. Kaldırmadan önce `grep -l 'label "AD"' *.kicad_sch` ile bak; kalacaksa
telin kısa bir dalına koy.

**Kütüphane sembolünü değiştirdiğinde onu kullanan her sayfanın `lib_symbols`
önbelleğini de aynı şekilde değiştir.** Yoksa ERC `lib_symbol_mismatch`.
`E.edit_lib_symbol(fn, lib, [sayfalar], ad, nick)` hepsine birden uygular.
Örn. SMBJ30A iki sayfada kullanılıyor (D3 `usb_c_input`, D7 `usb_pd_controller`).

**İki pinli özel sembollerde pin adı/numarası gövdeye biner** (SMBJ30A'da A1/A2
triyotun içine yazılıyordu). `E.hide_pin_texts` ile ikisini de gizle.

**Güç rayının adı `+3.3V`**, `+3V3` değil. Yanlış yazarsan beslenmeyen ayrı bir
net oluşur ve `power_pin_not_driven` hatası alırsın.

**`#PWR`/`#FLG` referansları benzersiz olmalı ve aynı sayacı paylaşır.**
Tekrarlarsa netlist dışa aktarımı "annotation errors" uyarısı verir.
`next_power_ref()` ve `E.Pool` kullan.

**Sadece passive pinlerden beslenen yeni ray** (diyot katodu gibi) "driven"
görünmez; o raya `PWR_FLAG` ekle.

**Sembolü `extends` ile türetilmiş halde kopyalama.** KiCad'in `SMAJ30A`
sembolü `SM6T6V8A`'dan türüyor; parent olmadan kütüphane yüklenmez.
`ensure_lib_symbol` bunu yakalar, önce bağımsızlaştır.

**Sembol düzenledikten sonra pin numarası→ad eşlemesini datasheet'le karşılaştır.**
Kutu genişletmek güvenlidir, pin adı değiştirmek değil.

**Yeniden çizim, şüpheli bağlantıyı korumak için bahane değil.** Bir bağlantı
tuhaf görünüyorsa (C31: VCAP–V_PRE) topolojiyi kopyalamadan önce datasheet'e
bak. LM74502: CVCAP, VCAP ile VS arasına bağlanır; VS = V_PRE → doğruydu.
Yanlışsa çizimi düzeltmeden önce kullanıcıya sor.

**Çalışan dosyada `git checkout` yapma.** Bir betiği "temiz durumdan başlat"
diye `git checkout -- <sayfa>` ile geri almak, o oturumda yapılmış ama commit
edilmemiş tüm düzeni siler (bu depoda bir turluk sayfa düzeni böyle kayboldu).
Geri alma yalnız bilinçli reset içindir; yeniden üretim betiği varsa zaten
`git checkout -- hardware/` + betik güvenli yoldur.

**Geçici "park" ötelemesi de 1.27'nin katı olmalı.** Blokları taşırken ara
konuma atmak için 200/300 mm ötelersen tüm blok ızgara dışına kayar; nihai
öteleme farkı katı olsa bile ara adımda ERC `endpoint_off_grid` (61 uyarı)
verir ve KiCad'de sürükleyince oynar. `move_block` bunu assert ile yakalar.

**Etiketi yalnız ada göre seçme.** "İlk eşleşen `PD_5V` etiketini taşı" diyen
döngü, başka bloktaki pull-up etiketini taşıdı; o net koptu ve `verify.py`
`unconnected-(R6-Pad1)` gösterdi. Etiket seçiminde ad **ve** konum kullan
(`E.remove_items` docstring'indeki örnek).

**Teli uzatırken başka netin teline değme.** Etiketi rahat yerleştirmek için
rayı 5 mm uzattığımda uç, kapı hattının dikey teline denk geldi: ERC
`multiple_net_names`, iki net birleşti. Uzatmadan önce hedef noktada ne
olduğuna bak; `verify.py --against` bunu anında gösterir.

**KiCad projeyi kapanırken yeniden kaydeder.** Tüm sayfalar normalize olur,
sayfa sırası/numaraları değişir, diff dev olur ama bağlantı aynıdır. Bunu
`--against` ile doğrula ve **ayrı bir commit** olarak al; kendi değişikliğinle
karıştırma. Proje KiCad'de açıkken dosyayı düzenlersen, KiCad'in kaydı seninkini
ezer (`hardware/~gopo.kicad_sch.lck` varsa açıktır; `pgrep -af kicad` ile de
bak). Açıksa düzenlemeye başlama, kullanıcıdan kaydedip kapatmasını iste;
beklerken yalnız okuma/parça seçimi yap.

KiCad 10'un kaydında ölçülen iki somut etki (REV_C alan çalışmasında yakalandı):
- `Description` alanı olmayan sembollere **`(hide yes)` olmadan** boş bir
  `Description` eklenir. Değer boş olduğu için render'da görünmez ama
  "yalnız Reference + Value görünür" değişmezini bozar: alan işini bitirdikten
  sonra betiği bir kez daha çalıştır (idempotenttir) ve gizlemeyi geri koy.
- Güç sembollerinden `(fields_autoplaced no)` düşer (30 sembol). Zararsızdır,
  ama HEAD ile birebir karşılaştırma yapan testte fark olarak görünür.

**Uzun oturumda dosyaların hâlâ senin bıraktığın halde olduğunu varsayma.**
Doğrulamadan önce `ls -la --time-style=full-iso hardware/*.kicad_sch`: tüm
sayfaların **aynı saniyede** damgalanması KiCad'in kaydettiği anlamına gelir,
kullanıcı arada sembol taşımış olabilir. Oturum başında alınan geometri
referansı o anda bayatlar; `--against` ve `field_geometry` karşılaştırmasını
yenile, kullanıcının düzenlemesini kendi değişikliğin sanıp geri alma.

**`git add -A` kullanma.** Blok A yeniden çizilirken o zamanki `poweroutput.kicad_sch` de
sıfırlanmıştı; `git add -A` onu commit'e aldı ve Blok B sessizce geri alındı
(daeca6d, iki tur sonra dca3fd1 ile telafi). Commit öncesi:

```bash
git status --short          # beklenmeyen dosya var mı
git add hardware/<yalnizca-calistigin-sayfa>.kicad_sch
git diff --cached --stat    # ne gireceğini doğrula
```

**Push öncesi uzak dalı kontrol et.** Skill dosyaları başka oturumlarda da
güncelleniyor; `git fetch` + gerekirse rebase ve içerik birleştirme yap,
force-push yapma.

**Blok A4'e sığmıyorsa sayfayı A3 yap** — sıkıştırmaya çalışma. Birden çok blok
tek sayfaya toplanacaksa önce **alan bütçesi** çıkar: A3'ün çizim alanı ~400x280
= 112.000 mm²; bloklar toplamı bunun %60'ını geçiyorsa blokları yeniden çizmeden
sığmaz. Ölçülen blok boyutları (REV_C): PD kontrolcü + VBUS anahtarı 142x118,
AP74502Q çıkış anahtarı 121x80, INA228 + panel 115x122, TPS55340 ön-boost 145x84,
AOZ1284 buck 156x110, I2C seviye dönüştürücü 84x56. Sığmıyorsa A2'ye çıkmak yerine
önce blokları dar/uzun biçimde yeniden çizmeyi değerlendir; kullanıcı kağıt
boyutunu sınırlıyorsa bu zorunludur.

## Parça seçimi

Bu skill parça *seçmez*. Değeri veya MPN'i belirsiz olan parçayı jenerik
sembolle yerleştir ve değerine `TBD` yaz; gereksinimleri `todo.txt` dosyasına
kaydet. MPN uydurma.

Datasheet gerekiyorsa indir. TI (`ti.com/lit/ds/symlink/<parça>.pdf`) erişilebilir
(`curl -sL -A "Mozilla/5.0"`). Diodes eskiden 403/404 veriyordu; 2026-09'da
`diodes.com/datasheet/download/<PARÇA>.pdf` curl ile indi (AP74502Q, pin tablosu
sembolle karşılaştırıldı). Mouser hâlâ bot korumalı. Datasheet inmezse ve parça
TI'la pin uyumluysa TI datasheet'i geçici kaynak olarak kullan ve bunu
`todo.txt`'ye not et. Tedarikçi indeksinin (Özdisan MCP) verdiği datasheet
bağlantıları (`cdn.ozdisan.com/public/product/assets/...`) da doğrudan iner;
tek sayfalık çizim-datasheet'lerde (Çin panelleri, KLS) metin çıkmaz, sayfayı
`pdftoppm -r 300` ile render edip tabloyu kırparak oku. Pinout'u `pdftotext -layout` ile "Pin Functions"
tablosundan çıkar, PDF'teki referans devre şekillerine görüntü olarak bak.
