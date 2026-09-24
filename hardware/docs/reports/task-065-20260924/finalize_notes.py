"""Fill TASK-065 measured tables and record the handoff; run once."""
import json
from pathlib import Path
from audit import HERE, ROOT

def read(name):
    return json.loads((HERE/name).read_text(encoding='utf-8'))

rows=read('heights-after.json')
before={f['ref']:f for f in read('inventory-before.json')['footprints']}
after=read('inventory-after.json')['footprints']
applied=read('applied.json')
decision=ROOT/'design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md'
text=decision.read_text(encoding='utf-8')
group_lines=['| Blok | h>2 mm üyeler (mm) | Aynı yüzü paylaşan tüm referanslar | Son yüz |',
             '| --- | --- | --- | --- |']
for name in applied['groups']:
    members=[r for r in rows if r['group']==name]
    tall=', '.join(f"{r['ref']}={r['height_mm']:.2f}" for r in members if r['height_mm']>2.0001) or '—'
    group_lines.append('| '+name+' | '+tall+' | '+', '.join(r['ref'] for r in members)+' | B.Cu |')
group_lines.append('| TFT BACKLIGHT | Yok | Q7, R28, R29, R60; J3 F.Cu ile birlikte | F.Cu |')
height_lines=['| Ref | Model h (mm) | Önce → sonra | Üst çıkıntı (mm) | LCD XY zarfıyla kesişir |',
              '| --- | ---: | --- | ---: | --- |']
for r in rows:
    h=f"{r['height_mm']:.3f}"
    if r['height_mm']>2.0001: h='**'+h+'**'
    if not r['models']: h='0 (düz PCB öğesi)'
    height_lines.append(f"| {r['ref']} | {h} | {before[r['ref']]['side']} → {r['side']} | {r['top_projection_mm']:.3f} | {'Evet' if r['lcd_overlap'] else 'Hayır'} |")
text=text.replace('<!-- GROUP_TABLE -->','\n'.join(group_lines)).replace('<!-- HEIGHT_TABLE -->','\n'.join(height_lines))
decision.write_text(text,encoding='utf-8')

def append_note(number, content):
    path=next((ROOT/'backlog/tasks').glob(f'task-{number:03d} - *.md'))
    raw=path.read_bytes()
    newline='\r\n' if b'\r\n' in raw else '\n'
    s=raw.decode('utf-8').replace('\r\n','\n')
    if content.strip() in s: return
    if '<!-- SECTION:NOTES:END -->' in s:
        s=s.replace('<!-- SECTION:NOTES:END -->',content+'\n<!-- SECTION:NOTES:END -->')
    else:
        s+='\n## Implementation Notes\n\n<!-- SECTION:NOTES:BEGIN -->\n'+content+'\n<!-- SECTION:NOTES:END -->\n'
    path.write_bytes(s.replace('\n',newline).encode('utf-8'))

append_note(15,'''24.09.2026 — TASK-065 dizgi devri:
- Çift taraflı SMT: L1/L3, C15/C29 ve ilişkili buck/boost devreleri B.Cu'da.
  Dizgiciyle önce hafif top SMT, sonra bottom yüz yukarı bakarken ağır bottom
  SMT'nin son reflow'u planlanacak; profil/ikinci çevrimde parça tutunması
  doğrulanacak. Ağır parçaların aşağı bakarak yeniden erimesine güvenilmeyecek;
  farklı sırada fikstür/yapıştırıcı veya sonradan lehimleme değerlendirilecek.
- C33 süperkapasitör, J8 Ethernet modül/header ve J4/J9 teller SMT sonrasında
  uygun THT/elle lehimlenecek. C33/modül için reflow uygunluğu varsayılmayacak;
  mekanik destek ve kablo gerilim alma uygulanacak.
- C33'ün top bacak çıkıntısı modelde 1,9 mm, J8'inki 4,4 mm (kart 1,6 mm).
  LCD altında kalırlarsa üstte metal+lehim zarfı ≤1,5 mm olacak şekilde kesilip
  ölçülecek veya pinler LCD izdüşümünün dışında tutulacak. Kesim artıkları
  temizlenecek; elektriksel bağlantı/lehim kalitesi kontrol edilecek.
- LCD arka yüz–PCB üst yüz hedefi 2,35±0,15 mm (min.2,20); J3 kapalı maks.2,15.
  J3 dışındaki toplam top zarf sınırı 1,80 mm. Önce FPC tak/kilitle, sonra
  LCD'yi mesafe elemanlarına sabitle; J3 üzerine montaj yükü bindirme.
- Ayrıntı ve yükseklik listesi:
  `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
  Bu not dizginin yapıldığını veya fiziksel doğrulamanın tamamlandığını göstermez.''')
append_note(12,'''24.09.2026 — TASK-065 mekanik tolerans girdisi:
KLS çizimindeki J3 kapalı yüksekliği 2,00±0,15 mm. LCD arka yüz–PCB top
montaj hedefi 2,35±0,15 mm (en az2,20 mm), J3 dışında top zarf bütçesi1,80 mm.
TASK-064'ün nominal2,00 mm boşluğu doğrudan mesafe parçası ölçüsü yapılmamalı.
Numunede gerçek boşluk, köpük/boss toleransı, kapağın serbest kapanması,
FPC kıvrımı ve gerilimsiz takılması doğrulanmalı. Kaynak:
`design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.'''.replace('az2','az 2').replace('bütçesi1','bütçesi 1').replace('nominal2','nominal 2'))
append_note(69,'''24.09.2026 — TASK-065 tamamlandı: buck/boost, RTC, USB-C, Ethernet,
INA226/panel çıkışı, AP33772S ve ESP32 blokları B.Cu; backlight/J3 F.Cu.
Bu yüz atamalarını başlangıç olarak koru. D5.2–U11.9 FB izi B.Cu'da
2,584607 mm; sonraki taşımalarda birlikte taşı. C33/J8 karşı yüz pinleri,
J9 proje model ataması ve top 1,80 mm bütçe için
`design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md` esas alınmalı.''')
append_note(85,'''24.09.2026 — TASK-065 devri: nihai konumlandırma sonrası model yükseklik
ve LCD izdüşüm denetimini tekrarla. LCD toleranslı zarfı
x=63,52…141,62; y=72,28…127,72 mm; top J3 dışı toplam zarf≤1,80 mm.
C33/J8 bottom gövdeleri güvenli olsa da top pin çıkıntıları modelde
1,9/4,4 mm: pinleri LCD dışında tut veya montajda metal+lehim≤1,5 mm şartını
uygula. Buck/boost B.Cu, backlight/J3 F.Cu ve D5–U11 FB sürekliliği korunmalı.
Karar: `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
TASK-065'in sıfır LCD çakışması kart dışındaki geçici yerleşime aittir.''')
append_note(65,'''24.09.2026 — Uygulandı ve doğrulandı.
- 58 footprint B.Cu'ya alındı; ilişkili 8 blok alt yüzde tutarlı. Buck/boost
  güç/FB/COMP üyeleri B.Cu, backlight Q7/R28/R29/R60 ve J3 F.Cu.
- 143 footprint tarandı; 125 model / 36 farklı STEP dosyası FreeCAD ile
  ölçüldü. 14 test pedi +4 montaj deliği modelsiz PCB öğesi; eksik model0.
  J9 kırık model yolu proje içi basit tel zarfıyla düzeltildi.
- LCD toleranslı izdüşümünde top h>2,00 mm parça0; J3 harici1,80 mm
  bütçeyi aşan çıkıntı0. SW3 PCB'de yok; J9 tel zarfı LCD'nin dışında.
- D5.2–U11.9 BOOST_FB dört segmentiyle B.Cu'ya taşındı:2,584607 mm,
  graf sürekliliği doğrulandı. Routing'in kalanı tamamlanmış değildir.
- J3/J9/H1–H4 ankrajları, tüm footprint/pad netleri/UUID'ler, grup üyelikleri
  ve Edge.Cuts korundu. C33 flip sonrası Y1 ile çakışmayacak şekilde
  aynı geçici gövde yuvasına geri ötelenip referans yazıları düzeltildi.
- kicad-cli pcb drc --schematic-parity: parity0; DRC148→146,
  unconnected360→360; yeni ihlal0; courtyard/clearance/shorting0.
  Mevcut146 bulgu nihai yerleşim ve üretim görevlerinde devam ediyor.
- Kanıt: `hardware/docs/reports/task-065-20260924/verification.json`,
  `drc-before.json`, `drc-after.json`, `inventory-before/after.json`,
  `heights-before/after.csv/json`; top/bottom SVG ve 3D görüntüler incelendi.
  `audit.py`, `apply_sides.py`, `verify.py` çalışma betikleridir.
- Karar ve tüm143 ref için yükseklik tablosu:
  `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
  J3=2,00±0,15 mm; top bütçe1,80 mm; LCD montaj hedefi2,35±0,15 mm.
- Çift taraflı SMT/ağır parçalar ve C33/J8 pin kesme şartı TASK-015'e,
  fiziksel Z/FPC doğrulaması TASK-012'ye, yerleşim devri TASK-069/085'e yazıldı.
  Blokların kart dışı geçici yerleşimi korundu; son konumlarda tarama tekrarlanır.'''.replace('model0','model 0').replace('parça0','parça 0').replace('harici1','harici 1').replace('çıkıntı0','çıkıntı 0').replace('taşındı:2','taşındı: 2').replace('parity0','parity 0').replace('DRC148','DRC 148').replace('unconnected360','unconnected 360').replace('ihlal0','ihlal 0').replace('shorting0','shorting 0').replace('Mevcut146','Mevcut 146').replace('tüm143','tüm 143').replace('bütçe1','bütçe 1').replace('hedefi2','hedefi 2'))

path=next((ROOT/'backlog/tasks').glob('task-065 - *.md'))
raw=path.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'
s=raw.decode('utf-8').replace('\r\n','\n')
s=s.replace('status: To Do','status: Done').replace('- [ ]','- [x]')
if 'updated_date:' not in s:
    s=s.replace("created_date: '2026-09-23 20:34'", "created_date: '2026-09-23 20:34'\nupdated_date: '2026-09-24 10:56'")
path.write_bytes(s.replace('\n',nl).encode('utf-8'))

changes=ROOT/'CHANGES.TXT'
raw=changes.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'
s=raw.decode('utf-8').replace('\r\n','\n')
entry='''24.09.2026 - TASK-065:
- J3 kapali yuksekligi 2.00+-0.15 mm; top zarf butcesi 1.80 mm,
  LCD montaj hedefi 2.35+-0.15 mm (min.2.20) olarak belgelendi.
- 58 footprint ve BOOST_FB izi bottom'a alindi; buck/boost bloklari
  B.Cu, backlight/J3 F.Cu. C33 flip sonrasi govde yuvasi korundu.
- 143 footprint icin STEP yukseklik tablosu ve LCD izdusum denetimi;
  J9 eksik modeline proje ici kablo zarfi. LCD ust cakisma 0.
- D5-U11 FB 2.584607 mm, kesintisiz; net/UUID/grup/ankrajlar korundu.
  Parity 0, DRC 148->146, yeni ihlal 0, unconnected 360 degismedi.
- Cift tarafli SMT/ag ir parca proses notlari TASK-015'e; C33/J8 top
  pinleri LCD disinda veya kesim sonrasi metal+lehim <=1.5 mm sarti.
  Karar: LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md. Gecici kart disi
  gruplar nihai konumlandirilinca yukseklik taramasi tekrarlanacak.

'''.replace('ag ir','agir')
if '24.09.2026 - TASK-065:' not in s:
    s=s.replace('24.09.2026 - TASK-042:',entry+'24.09.2026 - TASK-042:',1)
changes.write_bytes(s.replace('\n',nl).encode('utf-8'))

fpc=ROOT/'design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md'
s=fpc.read_text(encoding='utf-8')
add='''
## TASK-065 Z toleransı eki (24.09.2026)

Yukarıdaki 2,00 mm nominal J3 yüksekliği, toleranslı LCD mesafe parçası
ölçüsü olarak doğrudan kullanılmaz: J3 kapalı 2,00±0,15 mm, maks.2,15 mm.
TASK-065 LCD arka yüz–PCB top hedefini 2,35±0,15 mm (min.2,20 mm), J3
harici top zarf bütçesini1,80 mm olarak ayırdı. Kutu/numune doğrulamasında
FPC kıvrımı ve gerilimsiz takılma bu gerçek Z boşluğunda kontrol edilir.
J3 XY konumu, yönü, pin eşleşmesi ve kilidi değişmedi. Ayrıntı:
[TASK-065 kararı](LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md).
'''.replace('bütçesini1','bütçesini 1')
if '## TASK-065 Z toleransı eki' not in s: fpc.write_text(s+add,encoding='utf-8')
print('Decision tables, TASK-065 completion, assembly and placement handoff saved.')
