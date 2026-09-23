---
name: kicad-footprint
description: Bu depoda proje footprint'i ve 3D modeli üret, doğrula ve şema/PCB'ye bağla. Datasheet land pattern'inden, üretici ölçü çiziminden veya ürün fotoğrafından (alt görünüş pin etiketleri) footprint çizerken; header ile doğrudan lehimlenen modül (Waveshare, breakout kart) footprint'i hazırlarken; mekanik/bağlantısız pin (MP), modül altı lehim çıkıntısı için keepout, courtyard/silk/fab katmanlarını ayarlarken; üretici 3D model yayınlamadığında STEP üretirken; footprint'i sembole atayıp PCB'ye alırken veya kütüphanede değişen footprint'i PCB'de yenilerken; footprint'i 2D/3D render ve STEP dışa aktarımıyla denetlerken kullan.
---

# KiCad footprint ve 3D model — gopo deposu

Şema tarafı (sembol, alan, netlist) `kicad-schematic` skill'indedir; ortam
katmanı (`kicadtools.py`, `kpy`, `view.py`, `update_pcb.py`) oradan paylaşılır.
Bu skill ölçüden footprint'e, footprint'ten PCB'ye kadar olan kısmı kapsar.

## Ortam (Windows + Linux)

Tüm betikler **Bash aracından** (Windows'ta Git Bash) aynı komutla çalışır:

```bash
SK=.claude/skills/kicad-schematic/scripts     # ortak: kpy, kicadtools, view, render, update_pcb
FK=.claude/skills/kicad-footprint/scripts     # bu skill: kifp, step_boxes, fp_check
sh $SK/kpy $FK/fp_check.py hardware/libraries/<Lib>.pretty <Ad> -o <scratch>/fp --3d
```

`kpy` çalışan python'u seçer (Windows'ta `python3` Store kısayoluna düşer,
Linux'ta `python` olmayabilir). kicad-cli, KiCad `share` dizinleri ve `pcbnew`
için yol yazma: `kicadtools.kicad_cli() / kicad_share('footprints'|'3dmodels'|
'template') / ensure_pcbnew()`. Ayrıntı `kicad-schematic` → Ortam.

## Akış

```
kaynak topla → ölç → pin numarası → koordinat planı → kifp ile üret
   → fp_check (2D) → step_boxes (3D) → fp_check --3d → kütüphane kaydı
   → sembole ata (verify: netlist farkı YOK) → update_pcb → DRC parity 0
   → CHANGES.TXT + backlog
```

1. **Kaynak:** datasheet land pattern > üretici ölçü çizimi > fotoğraf.
   Modülün **kendi şeması** varsa pin numaralarının tek otoritesidir (Altium
   PDF'te `view.py --text` netlist'i de verir).
2. **Ölç** (aşağıdaki kurallar), her değeri kaynağıyla betik docstring'ine yaz.
3. **Pin numarası:** şema sembolü + ürün fotoğrafındaki etiketler + pin-1 işareti
   üçü birbirini doğrulamalı.
4. **Koordinat planı:** modül koordinatı (üst görünüş, sol-üst köşe 0,0) →
   footprint koordinatı (orijin pin 1) dönüşümünü tek fonksiyonda (`m(x, y)`) yap.
5. **Üret:** `kifp.Footprint`, 3D için `step_boxes.StepBoxes`. Tek betik ikisini
   de üretsin (örnek: `examples/waveshare_2ch_uart_to_eth.py`); betik
   deterministiktir, tekrar çalıştırmak git farkı üretmez.
6. **Doğrula:** `fp_check.py` (KiCad ayrıştırması + sayılar + PNG); `--3d` ile
   test kartında üst/ön/izometrik render ve STEP katı sayısı. PNG'lere BAK.
7. **Kütüphane:** yeni `.pretty` için `hardware/fp-lib-table`'a satır ekle;
   3D model yanına `<Lib>.3dshapes/`, yol `${KIPRJMOD}/libraries/<Lib>.3dshapes/<Ad>.step`.
8. **Sembole ata:** `E.update_fields(t, 'J8', {'Footprint': 'Lib:Ad', 'Value': ...,
   'Pitch': ..., 'Height': ..., 'AssemblyNote': ...})`; `verify.py --against` →
   `netlist farki: YOK`, `E.field_geometry` değişmemeli (kicad-schematic → alanlar).
9. **PCB:** `sh $SK/kpy $SK/update_pcb.py gopo.kicad_pcb --dry-run` → yalnız
   beklenen `EKLE`; sonra `--keep-tracks`. Kütüphanede footprint/3D model
   değiştiyse FPID aynı kaldığı için güncelleme görmez: `--refresh J8`.
   Doğrulama: `run_cli(['pcb','drc','--schematic-parity',...])` → parity 0.

## Ölçme kuralları

- **Görüntüden ölçerken ölçeği iki bilinen toplamdan çıkar, x ve y için ayrı.**
  Waveshare çiziminde x 14.05, y 13.92 px/mm çıktı; tek ölçek 0.3 mm kaydırır.
  SQJB60EP land pattern'inde 6.75 ve 7.75 toplamlarından ≈78.4 px/mm; her kenarın
  orijine uzaklığını pikselden hesapla, toplamların tuttuğunu kontrol et
  (2 × 3.075 = 6.15).
- **Ölçü etiketi ile toplamlar çelişirse bağımsız ölçümle karar ver.** Çizimde
  RJ45 taşması "4.00" yazıyor ama 57.30 − 53.00 = 4.30 ve mekanik pin konumu
  (RJ45 önünden 8.30) görüntüde 3.85–3.91 mm → 4.30 doğru; courtyard 4.30 ile.
- **Yığın yüksekliğini farktan bul:** header ara parçası = 10.10 − 1.60 (kart)
  − 6.00 (pin) = 2.50 mm.
- **Görüntüden ölçülen konum ±0.3 mm'dir:** delik ve pedi büyüt (mekanik pin
  0.64 kare için 1.4 / 2.2 mm), konumu backlog'daki numune görevine "1:1 çıktı
  üzerine oturt" kriteriyle yaz.
- Fotoğraf/çizimi `view.py --crop ... --scale 3` ile büyütüp oku; PDF bölgesini
  `view.py --page N --clip ... --dpi 500`. Read aracı Windows'ta PDF sayfası
  render edemez (pdftoppm yok).

## Pin numarası ve yön

- Footprint **üst görünüşte** çizilir (KiCad, y aşağı). Modül ana kartın üstüne
  bileşen yüzü yukarı oturuyorsa modülün kendi üst görünüşü = footprint.
- **Alt görünüş fotoğrafı soldan sağa aynadır, satırlar aynı kalır.** Etiket
  tablosunun sütunları pin sütunlarıyla konum olarak eşleşir: Waveshare alt
  görünüşte sol sütun (kart kenarı) DIR1/CFG0/RXD1… = tek numaralar → üst
  görünüşte dış sütun. Şema sembolü (P1: 1 DIR1, 2 DIR2 … 15–16 5V) ve üst
  görünüşteki pin-1 silk kutusu (alt sıra) aynı sonucu verdi.
- **Bağlantısız görünen pini şemanın GÖRÜNTÜSÜNDEN doğrula.** Altium PDF metninde
  adsız netlerin sonlandırıcısı yok; grup sınırı metinden okunmaz (P2/P3'ün
  RSETE netinde olduğu sanıldı, `view.py --find P2` + `--clip` render'ı telsiz
  "Header 1" gösterdi). Bağlantısızsa ped numarası **`MP`**: sembolde pini yok,
  net almaz, `update_pcb` hata vermez.
- Sembolde eş pinli drain (SQJB60EP 5-6, 7-8) varsa ikinci numarayı aynı
  gövdenin **yalnız bakır** (`"F.Cu"`) kopyası yap: paste ikilenmez, PCB
  güncellemesinde "pad yok" hatası çıkmaz.

## Footprint içeriği (bu depodaki kurallar)

| öğe | kural |
|---|---|
| orijin | header'lı modülde pin 1 (KiCad PinHeader gibi); IC'de gövde merkezi |
| THT header pedi | `kifp.PINHEADER_PAD/DRILL` = 1.7 / 1.0 (KiCad PinHeader ile aynı), pin 1 `rect` |
| F.SilkS | gövde sınırı 0.12 mm dışarıda, 0.12 kalınlık; pin-1 üçgeni sınırın dışında |
| F.Fab | gövde, taşan parça (RJ45), header gövdesi + pin-1 pahı, pin adları 0.6 mm, `${REFERENCE}` |
| F.CrtYd | 0.25 mm pay, **taşan parçayı da** kapsayan poligon, 0.05 çizgi |
| Cmts.User | montaj notu (ara parça yüksekliği, keepout nedeni) |
| keepout | modül altından çıkan lehim ucu ile ara parça arasındaki boşluk < ~0.5 mm ise F.Cu'da iz/via/döküm/parça yasak (RJ45: 2.2 mm çıkıntı / 2.5 mm ara) |
| satır sonu | yeni kütüphane LF; mevcut kütüphanede komşu dosyaya uy (`write(crlf=True)`) |

Yeni footprint'e ilk bakışta en sık iki hata (KLS/Korchip): silk pedin üstünden
geçiyor (yayla böl / dışarı al) ve courtyard pedleri kapsamıyor.

## 3D model

- Üretici model yayınlamıyorsa (Waveshare wiki'sinde yalnız şema/datasheet/kod)
  **`step_boxes.py` ile kutulardan STEP üret**: kart, konnektör zarfı, büyük
  entegreler, header gövdesi ve pinler, ara parçalar. cadquery/FreeCAD gerekmez.
- **Koordinat sözleşmesi** (render ile doğrulandı): kutular footprint
  koordinatında (y aşağı) verilir, STEP'e `Y = −y` yazılır; z = 0 ana kart üst
  yüzeyi, kart altına inen pinler negatif z. Böylece footprint'teki `(model ...)`
  offset/rotate **0** kalır.
- KiCad'in hazır modelini (`kicad_share('3dmodels')`, ör. `PinHeader_2x08...step`)
  döndürerek kullanmak yerine parçayı kendi STEP'ine göm: offset/rotate işaret
  kuralı tahmine kalır, render olmadan doğrulanamaz.
- `fp_check.py --3d`: test kartında model gerçekten yüklendi mi (render'da
  görünür), `pcb export step` kaç katı verdi (kutu sayısı + 1 kart).
- Model yolu `${KIPRJMOD}` ile başlar; test kartı başka dizinde olduğu için
  `fp_check` `.3dshapes`'i yanına kopyalar. Model bulunamazsa KiCad **sessizce**
  modelsiz render eder.
- **Silindir** (coin süperkap, enkoder mili): `StepBoxes.cyl(...)` kapsayan
  şeritlerle yaklaşır; yükseklik/çakışma kontrolü için güvenli taraf.
- **Kartın tamamını tara:** `model_scan.py hardware/gopo.kicad_pcb` modelsiz
  footprint'i ve dosyası olmayan model yolunu listeler (çıkış kodu 1).
- **KiCad 10 standart footprint'lerinin bir kısmı kurulumda olmayan modele
  işaret eder** (L_7.3x7.3_H4.5, WSON-12 3x3, ESP32-C6-MINI-1, ABS25,
  SolderWire, SOIC-8-1EP EP2.71x3.7). İkame STEP
  `libraries/Generic_Custom.3dshapes/`'e, PCB'deki yol metin olarak
  değiştirilir (`examples/gopo_basic_models.py --pcb`); gövdesi aynı KiCad
  modeli varsa ona yönlendir. Standart footprint `--refresh` edilirse yol
  geri döner, taramayı tekrarla.
- Mevcut (elle yazılmış) footprint'e model eklerken dosyayı yeniden üretme,
  yalnız `(model ...)` bloğunu son `)`'den önce ekle, satır sonunu koru
  (`gopo_basic_models.add_model`).

## Tuzaklar

- **`kicad-cli fp upgrade` `--force` olmadan** "Footprint library was not
  updated" der, çıktı dizini oluşmaz. `fp_check` `--force` kullanır.
- **`render.py --footprint` zone/keepout çizmez.** Keepout'un KiCad'e geçtiğini
  `fp_check` sayacından (`keepout 1`) doğrula.
- **`update_pcb.py` aynı FPID'li footprint'i yenilemez**: kütüphanede model/ped
  değiştirdikten sonra PCB'deki kopya eski kalır → `--refresh REF`.
- **pcbnew kaydı tüm kartı normalize eder** (KiCad 10: ~2500 satır
  `(thickness ...)` eklendi). İlk `update_pcb` çalıştırmasını ayrı commit'e al.
- **KiCad oturum ortasında yeniden açılır.** Yalnız `~gopo.kicad_pro.lck` =
  proje yöneticisi (şema/PCB'ye yazmak güvenli); `~gopo.kicad_pcb.lck` = PCB
  editörü açık, kaydederse değişiklik ezilir. `kicad_open('.', editors_only=True)`;
  `update_pcb.py` PCB kilidi varken yazmayı reddeder.
- **Git Bash yolu python kodunun içine gömülünce çevrilmez**: `-c "...'/d/GitHub/...'"`
  Windows python'unda `ModuleNotFoundError`. Argüman olarak verilen yollar
  çevrilir; koda göreli yol ver veya `$(pwd -W)` kullan.

## Dosyalar

| dosya | iş |
|---|---|
| `scripts/kifp.py` | `Footprint`: `pad_tht` (`MP`), `pad_smd`, `line`, `rect`, `poly`, `text`, `keepout`, `model`, `prop_ref/value`, `write(crlf=)`; deterministik uuid (uuid5) |
| `scripts/step_boxes.py` | `StepBoxes`: `box`, `pin`, `cyl`, `write(stamp=)`; renkler `BLUE SILVER BLACK GOLD GREEN WHITE` |
| `scripts/fp_check.py` | KiCad ayrıştırma + sayılar + model yolu; 2D PNG; `--3d` render + STEP (KIPRJMOD = `.pretty`'nin üst dizini: test kütüphanesinde `.3dshapes`'i `<üst>/libraries/` altına koy) |
| `scripts/model_scan.py` | PCB genelinde modelsiz / kırık model yolu taraması |
| `examples/waveshare_2ch_uart_to_eth.py` | J8 footprint + STEP'in tam kaynağı; ölçü çözümü docstring'de |
| `examples/gopo_basic_models.py` | J3, L1, Q3/Q5, C33, SW3 STEP'leri + standart footprint ikameleri (L3, U12, U2, Y1, J4); `--pcb` kırık yolları düzeltir |
| `../kicad-schematic/scripts/view.py` | PDF metni/arama/bölge render, görüntü kırp-büyüt |
| `../kicad-schematic/scripts/update_pcb.py` | şemadan PCB (`--refresh`, `--keep-tracks`, `--dry-run`) |

## Doğrulanmış footprint gerçekleri

- **Waveshare 2-CH UART TO ETH** (`Module_Custom:Waveshare_2-CH_UART_TO_ETH`):
  53 × 22 × 1.6 mm, RJ45 16 geniş / modül altından 15.0 yüksek / kenardan 4.3
  taşar, 2x8 header dış sütun kenardan 1.85, sıra kenardan 2.11, ara parça 2.5,
  pin ara parçadan 6.0 iner (ana kart altından ~4.4 çıkar), mekanik pinler
  RJ45 tarafında kenardan 4.00 / 1.35 (± 0.3, numuneyle doğrulanacak: TASK-053).
- **Gövde yükseklikleri (kart üstünden, nominal / maks):** J3 KLS1-242I-2.0
  2.00 ± 0.15 (flip kapak açıkken 3.1), L1 FPI0705 5.0 ± 0.3, L3 SRI0704
  4.5 maks, Q3/Q5 PowerPAK SO-8L 1.07 / 1.14, U12 WSON 0.8 maks, U2
  ESP32-C6-MINI-1 2.4, Y1 ABS25 2.5, C33 Korchip DCL H 6.5 ± 0.5, SW3 gövde
  4.5 / bushing üstü 9.5 / mil ucu 17.0 (E bushing D=5, F mil L=12.5).
