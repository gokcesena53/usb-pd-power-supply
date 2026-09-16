# gopo — Masaüstü Güç Kaynağı

USB-C PD beslemeli, ESP32-C6 tabanlı, TFT ekranlı ve döner enkoderli
masaüstü ayarlanabilir güç kaynağı. Şematik ve PCB tasarımı KiCad ile yapılmıştır.

Depo yapısı [Open Hardware Template](https://github.com/mfhepp/open_hardware_template)
şablonunu izler.

## Klasör yapısı

| Klasör | İçerik |
| --- | --- |
| `hardware/` | KiCad projesi (`gopo.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `.kicad_dru`) ve kütüphane tabloları (`fp-lib-table`, `sym-lib-table`) |
| `hardware/libraries/` | Projeye özel sembol (`.kicad_sym`), footprint (`.pretty`) ve 3D model (`.3dshapes`) kütüphaneleri |
| `hardware/datasheets/` | Kullanılan bileşenlerin veri sayfaları |
| `hardware/docs/` | Ham ERC/DRC raporları, netlist'ler, doğrulama betikleri ve anlık görüntüler |
| `hardware/gerber/` | Üretim çıktıları (Gerber, drill) |
| `hardware/images/` | Şematik/PCB görüntüleri (PNG, SVG) |
| `hardware/pdf/` | Blok blok şematik PDF çıktıları ve inceleme belgeleri |
| `design_decisions/` | Tasarım kararları, hesaplamalar ve inceleme notları (Markdown) |
| `3d_design/` | Kutu/mekanik tasarım dosyaları |
| `software/` | Firmware ve yardımcı betikler |
| `docs/` | GitHub Pages proje sayfası |
| `.claude/skills/` | KiCad şema üretimi için Claude Code skill'i ve araçları |

## Şema araçları

`.claude/skills/kicad-schematic/` altında şema üretimi ve temizliği için
bir Claude Code skill'i ve iki bağımsız betik bulunur:

```bash
SK=.claude/skills/kicad-schematic/scripts
cd hardware
python3 ../$SK/render.py gopo.kicad_sch --list
python3 ../$SK/render.py gopo.kicad_sch --page 10 --crop 255 26 410 128 -o /tmp/r
python3 ../$SK/verify.py gopo.kicad_sch --show PD_VOUT V_PRE
```

`render.py` şemayı PNG'ye çevirir ve mm cinsinden bir bölgeye yakınlaşır;
`verify.py` ERC çalıştırıp netlist'i bir referansla karşılaştırır.
Gereksinimler: `kicad-cli`, `poppler-utils` (pdftoppm, pdftotext), Python 3.

Yöntem [American-Embedded/kistack](https://github.com/American-Embedded/kistack)
schematic skill'ine dayanır (MIT); kopyası ve lisansı skill'in `references/`
klasöründedir.

## Revizyonlar

Aktif revizyon **REV_B**'dir; `hardware/` klasöründeki tasarım budur.
Üretilmiş olan REV_A tasarımı depodan çıkarılmıştır ve yalnızca git geçmişinde
bulunur (`git log --diff-filter=D -- "masaüstü güç kaynağı.kicad_pcb"`).

Değişiklik kaydı için `CHANGES.TXT` dosyasına bakınız.

## Tasarım kuralları ve PCB üretimi

Tasarım kuralları `hardware/gopo.kicad_dru` dosyasındadır. Üretime göndermeden önce
seçtiğiniz üreticinin yeteneklerine uyduğunu doğrulayın.

PCB ipek baskısına ve şematiğe **"Licensed under CERN OHL v.1.2"** metnini
eklemeyi unutmayın.

## Lisans

Donanım tasarımı CERN OHL v.1.2 altında, `software/` klasöründeki yazılım MIT
lisansı altında dağıtılmaktadır. Ayrıntılar için `LICENSE` ve
`cern_ohl_v_1_2.txt` dosyalarına bakınız.

> **Not:** `LICENSE` dosyasındaki `<TELİF HAKKI SAHİBİ>` alanı henüz
> doldurulmamıştır; yayımlamadan önce doldurun veya farklı bir lisans seçin.

## Sorumluluk reddi

BU TASARIM VE YAZILIM, AÇIK VEYA ZIMNİ HİÇBİR GARANTİ OLMAKSIZIN "OLDUĞU GİBİ"
SAĞLANMAKTADIR. YAZARLAR VEYA TELİF HAKKI SAHİPLERİ, TASARIMIN VEYA YAZILIMIN
KULLANIMINDAN DOĞAN HİÇBİR TALEP, ZARAR VEYA SORUMLULUKTAN SORUMLU TUTULAMAZ.
