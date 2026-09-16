---
name: kicad-schematic
description: Bu depodaki KiCad şemalarını üret, değiştir ve temizle. Şemaya bileşen/blok eklerken, mevcut bir bloğun yerleşimini/çizimini düzeltirken veya bir handoff dokümanındaki tasarım kararlarını uygularken kullan.
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
```

Görüntüye bakmadan "tamam" deme. Tek turda olmaz; 3-5 tur normaldir.
Yerleşim/çizim düzenlemesinde hedef: **`netlist farki: YOK`**, ERC sayısı
değişmemiş, `lint()` boş (bilinçli kesişmeler hariç).

Sayfa numaraları: 10 = POWER GENERATION (Blok A), 12 = POWER OUTPUT (Blok B).
`--list` ile doğrula; sayfa eklenirse kayar.

### Ortam (Windows)

- `kicad-cli` PATH'te değil; `kicadtools.kicad_cli()` `%LOCALAPPDATA%\Programs\KiCad\*\bin`
  altında bulur. Başka yerdeyse `KICAD_CLI` ortam değişkenini ayarla.
- **KiCad'in `bin` dizinini PATH'in önüne ekleme**: KiCad'le gelen python öne
  geçer, PyMuPDF bulunamaz. Betikleri `python` (C:\Python314) ile çağır.
- `pdftoppm` yok; `render.py` PyMuPDF (`fitz`) ile rasterleştirir.
- `kicad-cli` her çalıştığında `gopo.kicad_pro`'yu (yalnız satır sonları) yeniden
  yazar. `render.py`/`verify.py` dosyayı bayt bayt geri koyar; kendi `kicad-cli`
  çağrında `kicadtools.keep_file` kullan veya `git checkout -- gopo.kicad_pro`.
- Şema ve kütüphane dosyaları **CRLF**. `open().read()` + `newline='\n'` yazarsan
  tüm dosya LF olur. `kicadtools.read_sheet` / `write_sheet` satır sonunu korur.

## Modüller

| dosya | iş |
|---|---|
| `kisch.py` | yeni öğe üretimi: `sym`, `power`, `wire`, `wires`, `label`, `junction`, `no_connect`, `rect`, `text`, `xf`, `lib_pins`, `text_width` |
| `kisch_edit.py` | mevcut sayfada düzenleme: `dump`, `strip_region`, `place`, `sym_pin`, `translate_region`, `Pool`, `lint`, `edit_lib_symbol`, `hide_pin_texts`, `hide_stacked_pins` |
| `kicadtools.py` | `kicad_cli()`, `read_sheet`/`write_sheet` (CRLF), `keep_file` |
| `render.py` | PDF export + kırpılmış PNG |
| `verify.py` | ERC sayıları + netlist farkı |

### Yeni blok üretmek

```python
import sys; sys.path.insert(0, '../.claude/skills/kicad-schematic/scripts')
import kisch as K
from kicadtools import read_sheet, write_sheet
t, crlf = read_sheet('powergeneration.kicad_sch')
t = K.ensure_lib_symbol(t, 'libraries/Power_Path_Custom.kicad_sym', 'TPS55340PWPR', 'Power_Path_Custom')
pins = K.lib_pins(t, 'Power_Path_Custom:TPS55340PWPR')
vin  = K.xf((320.04, 76.2), 0, pins['3'])     # VIN pininin mutlak konumu
t = K.insert(t, K.wire(vin, (vin[0], 48.26)))
write_sheet('powergeneration.kicad_sch', t, crlf)
```

### Mevcut bloğu yeniden yerleştirmek

Sembolleri **silip yeniden oluşturma**; taşı. uuid, footprint, MPN ve instance
korunur, diff okunur kalır. Akış (tam örnek `kisch_edit.py` başındaki docstring'de):

1. `verify.py --save` ile referans netlist'i al. `E.dump(t, kutu)` ile envanter çıkar
   (sembol, açı, ayna, tel, etiket). Mevcut netleri `--show` ile yaz.
2. **Önce kâğıt üstünde koordinat planı yap**: her kolonun x'i, her satırın y'si,
   metinlerin kapladığı alan (`K.text_width`). Planı yapmadan betiği yazma.
3. `E.strip_region(t, kutu)` → tel/etiket/junction/no_connect/metin/çerçeve ve
   güç sembolleri gider; `E.Pool(freed, K.next_power_ref())` ile `#PWR`'leri
   geri kullan. `no_connect` işaretleri de silinir, **yeniden ekle**.
4. `E.place(...)` ile sembolleri taşı, `E.sym_pin(...)` ile pin konumunu oku ve
   `assert` ile planla karşılaştır (ayna/açı hatası anında yakalanır).
5. Telleri, etiketleri, güç sembollerini `K.*` ile üret, `K.insert`.
6. `verify.py --against`, `E.lint(t, kutu)`, render, bak. Betiği tekrar
   çalıştırılabilir yaz: strip yeni çizimi de siler, place mutlak konum yazar.

Betiği scratchpad'de tut; depoya yalnız sonuç şema girer.

## Bu depoda geçerli kurallar

**Izgara** 1.27 mm. Her koordinat katı olmalı; değilse KiCad'de sürüklerken kayar.
Metin konumları ızgaraya bağlı değildir.

**Pasifler** IC pinlerine *gerçek tellerle* bağlanır (dekuplaj, pull-up/down,
SS, FREQ, kompanzasyon, kapı sürücü ağı). Etiket yalnızca bloklar/sayfalar arası
ve okunabilirlik düğümlerinde (`BOOST_SW`, `BOOST_FB`, `GATE_DRV` gibi). Aynı
sayfa içinde iki noktayı etiket eşleşmesiyle bağlamak zayıf çizimdir.

**Direnç sembolü** `Device:R_Small_US`. Kondansatör ve bobin standart.

**Değerlerde birim var**: `100kR`, `78.7kR`, `9.76kR`, `47nF`, `10uF 50V`, `6.8uH`.
Ohm için `R`, omega işareti değil. Depodaki mevcut stil budur.

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

Bu değerler REV_C Blok A/B düzenlemesinde render'dan ölçüldü.

**Metin genişliği** 1.27 mm fontta ~1.11 mm/karakter (`K.text_width`). Pasif
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

**Aynı kenardaki pinler iç içe L ile çıkar.** Sol kenarda yukarıdan aşağı
EN, SYNC, FREQ, SS varsa: alttaki pin daha dışa (daha sola) gider, üstteki
içte kalır → hiçbir tel kesişmez. Sağ kenarda yukarı çıkan hatlar için tersi:
en alttaki pin en dıştan yükselir (VCAP içte, GATE ortada, SRC en dışta).

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

**Döndürülmüş sembolde metin de döner.** `prop_rot` ile geri al: 90 ve 270
derecede `prop_rot=90` veya `270` metni yatay tutar (KiCad 180°'yi 0° gibi
okunur basar). `E.place` varsayılan olarak 90 kullanır. Unutursan değer metni
dikey basılır ve komşusunun üstüne biner.

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

**`no_connect` işaretleri bölge temizliğinde silinir.** Yeniden eklemezsen ERC
`pin_not_connected` sayısı artar.

**Kütüphane sembolünü değiştirdiğinde onu kullanan her sayfanın `lib_symbols`
önbelleğini de aynı şekilde değiştir.** Yoksa ERC `lib_symbol_mismatch`.
`E.edit_lib_symbol(fn, lib, [sayfalar], ad, nick)` hepsine birden uygular.
Örn. SMBJ30A iki sayfada kullanılıyor (D3 `usb_c_input`, D7 `poweroutput`).

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

**`git add -A` kullanma.** Blok A yeniden çizilirken `poweroutput.kicad_sch` de
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

**Blok A4'e sığmıyorsa sayfayı A3 yap** — sıkıştırmaya çalışma.

## Parça seçimi

Bu skill parça *seçmez*. Değeri veya MPN'i belirsiz olan parçayı jenerik
sembolle yerleştir ve değerine `TBD` yaz; gereksinimleri `todo.txt` dosyasına
kaydet. MPN uydurma.

Datasheet gerekiyorsa indir. TI (`ti.com/lit/ds/symlink/<parça>.pdf`) erişilebilir
(`curl -sL -A "Mozilla/5.0"`); Diodes ve Mouser bot korumasıyla 403/404 verir.
Diodes parçası TI'la pin uyumluysa TI datasheet'i geçici kaynak olarak kullan ve
bunu `todo.txt`'ye not et. Pinout'u `pdftotext -layout` ile "Pin Functions"
tablosundan çıkar, PDF'teki referans devre şekillerine görüntü olarak bak.
