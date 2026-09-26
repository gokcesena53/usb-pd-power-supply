---
id: TASK-095
title: Encoder sonrasi park edilen bloklari yeniden kart icine yerlestir
status: To Do
assignee: []
created_date: '2026-09-25 13:23'
updated_date: '2026-09-26 10:52'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-094
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/ENCODER_SOL_PANEL_GOREV_KAPSAMI_20260925.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/docs/reports/task-094-20260925/placement.json
priority: high
ordinal: 181000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sonraki ayri calisma: TASK-094 tamamlandiktan sonra TASK-094.02 park envanterindeki bloklari yeni sol dis hat ve encoder montaj/kablo keepout alanlarini koruyarak yeniden kart icine yerlestir. Kullanici bu yerlestirmeyi daha sonra yapacagini belirtti; TASK-094 kapsaminda otomatik baslatilmaz. J7/J8 sabit konumlari ve encoder nihai mekanik ankrajlari korunur. Yeni PCB sekli icin kritik elektriksel yerlesim, yerel izler ve blok siniri baglantilari yeniden degerlendirilir; genel routing TASK-087 kapsamindadir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 TASK-094.02 park listesindeki her ref yeni x/y/aci/yuz/grup bilgisiyle kart icine alinmis; unutulan veya gerekcesiz disarida kalan blok yok.
- [ ] #2 USB/RJ45 ve encoder nihai ankrajlari degismemis; encoder/J9 kablo, 3 mm panel, LCD/FPC, anten, mezanin ve montaj erisim zarflari korunmus.
- [ ] #3 Blok ici kritik dongu/dekuplaj/FB/COMP/Kelvin iliskileri ve mevcut yerel baglantilar kontrol edilmis; pad-net eslesmeleri korunmus, yeni sol kenarda en az 0,254 mm ve daha siki mevcut kurallar saglanmis.
- [ ] #4 Once/sonra DRC, schematic parity ve 3D aciklik kanitlari kayitli; yeni aciklanmamis ihlal 0, parite farki 0; baglantisiz oge degisimi ve routing devri belgelenmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
TASK-094 devri: AP33772S grubunun 23 uyesi ve R34/R35/R36 kart disinda; once/sonra koordinatlari placement.json. J7/J8 ve encoder ankrajlarini koru. Alt yuz kablo servis hacmi PCB X=57,8..70, Y=102..123, STEP Z=-17..-0,5 mm; buraya komponent yerlestirme. J9=(61,5;104), aci=-90. Yeni dik sol kenar X=59,8 ve bakir acikligi>=0,254 mm/daha siki mevcut kural. Bu gorev henuz uygulanmadi.
<!-- SECTION:NOTES:END -->
