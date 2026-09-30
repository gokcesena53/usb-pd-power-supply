---
id: TASK-094.03
title: Encoder montajini tamamla ve sadece sol board shapei duzenle
status: Done
assignee: []
created_date: '2026-09-25 13:23'
updated_date: '2026-09-26 10:52'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-094.02
references:
  - hardware/gopo.kicad_pcb
  - hardware/gopo.kicad_dru
  - design_decisions/output/ENCODER_SOL_PANEL_GOREV_KAPSAMI_20260925.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/docs/reports/task-094-20260925/verification.json
parent_task_id: TASK-094
priority: high
ordinal: 180000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
J9 tarafindaki panel encoder montajini tamamla; ardindan yalniz sol Edge.Cuts geometrisini encoder ve kablo zarflarina gore duzenle. USB J7 ve Ethernet J8 ankrajlari sabit. Encoder elektriksel PCB footprinti olmaz; montaj modelinde panel parcasi olarak temsil edilir. Son kullanici karari: 3 mm DUZ DIS PANEL montaji, saft disari tasabilir; USB giris duzlemiyle saft ucu esitligi aranmaz. Saft yuksekligi iki kablo giris merkezinin ortalamasi, J9 baglantisi kabloludur. Park edilen bloklar kart disinda kalir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Encoder konumu kesinlestikten sonra yalniz sol dis hat degistirilmis; ust/alt/sag kenar ve montaj delikleri korunmus; kapali, kendiyle kesismeyen uretilebilir Edge.Cuts elde edilmis. Sol yerel kose/gecislerin geometrisi ve olculeri raporlanmis.
- [x] #2 Degisen kenardaki tum bakirlar en az 0,254 mm uzakta; mevcut daha siki kurallar gevsetilmemis. 0,250 mm 10 mil sayilmamis; gerekli kural guncellemesi ve gercek en kucuk aciklik raporlanmis.
- [x] #3 Encoder/panel/PCB/LCD/USB/RJ45/J9 ve kablo montaj hacimlerinde amaclanan montaj temaslari haric kesisim yok; en kisa mesafeler ve model sinirlari raporlanmis. Sabit portlar veya 3 mm panel ile cozulmeyen cakisma varsa tasima yapilmadan kullaniciya sunulmus.
- [x] #4 kicad-cli DRC ve schematic parity, ust/alt katman renderleri ve 3D kontrol kayitli; J7/J8 ankraj farki sifir, parite farki sifir, yeni aciklanmamis ihlal sifir. Park edilen bloklar ve eski ihlaller ayri listelenmis; PCB uretime hazir diye raporlanmamis.
- [x] #5 Nihai encoder XYZ/donusum ve J9 kablo guzergahi kayitli; saft Z iki giris merkezi Z ortalamasi, taban acisi 90 derece; 3 mm DUZ DIS PANEL montajinda saftin disari tasmasina izin var (kullanici duzeltmesi). Ust ve sol panel gorunumleri olculu.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kullanici duzeltmesi: aciklamadaki USB giris duzlemindeki saft ucu sarti kaldirildi; duz dis panel montaji ve disari tasan saft esas alinacak.

26.09.2026 kapanis: Sol dik kenar 1 mm pahli girintiyle degisti; ic dik kenar X=59,8. Diger 7 Edge.Cuts ogesi, yaylar, ust/alt/sag kenar ve H1-H4 ayni. J9 bakir-kenar acikligi 0,775 mm; J7 ozel kenar kurali 0,254 mm yapildi. Encoder-PCB 2,008; J7 11,809; J8 5,250; J9 3,496; LCD XY zarfi 5,720 mm nominal mesafe, tumunde kesisim 0. Kablo servis zarfi STEP X57,8..70/Y-123..-102/Z-17..-0,5 mm ayrildi. Son DRC: 15 eski U2 hatasi, 153 uyari, yeni ihlal 0; parite 0, baglantisiz 360. Ust/alt SVG ve 3D gorseller incelendi. Numune/retansiyon ve gercek fis sinirlari raporda.
<!-- SECTION:NOTES:END -->
