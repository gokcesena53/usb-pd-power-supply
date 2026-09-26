---
id: TASK-094.02
title: Encoder alanindan etkilenen bloklari kart disina tasi
status: Done
assignee: []
created_date: '2026-09-25 13:22'
updated_date: '2026-09-26 10:52'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-094.01
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/ENCODER_SOL_PANEL_GOREV_KAPSAMI_20260925.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/docs/reports/task-094-20260925/placement.json
parent_task_id: TASK-094
priority: high
ordinal: 179000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-094.01 encoder montaj zarfi ve ongorulen sol kenar geometrisinden etkilenen komponentleri iliskili devre bloklari halinde mevcut ve planlanan board shape disindaki ayrilmis gecici alanlara tasi. Encoder govdesi, lehim uclari, J9 kablolama ve montaj erisimini hesaba kat. Blok ici goreli konumlari/netleri/yerel izleri koru; J7/J8 sabit ankrajlarini hicbir blokla birlikte tasima. J9 tasinmasi gerekiyorsa kablo erisimi ve pin/net eslesmesini koruyarak gerekcesini kaydet. Bu islemden sonra bloklari kart icine geri yerlestirme.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Baslangic PCB yedegi, tum ref x/y/aci/yuz ve grup uyeligi, mevcut iz/via/net envanteri ve baslangic DRC kayitli.
- [x] #2 Etkilenen her blok icin neden, tum uye refler, once/sonra koordinatlar ve kart disi park alani kayitli; park alanlari birbirleriyle, kartla veya diger gecici gruplarla cakismiyor.
- [x] #3 J7/J8 konum/aci/yuzleri ve etkilenmeyen refler ayni; etkilenen bloklarin goreli yerlesimi, pad-net eslesmesi ve grup ici iz/vialari korunmus. Blok siniri baglantilarinda zorunlu degisiklik varsa tek tek raporlanmis; sessiz net kaybi yok.
- [x] #4 Once/sonra gorunum ve DRC farki kayitli; schematic parity 0; gecici kart disi konumdan dogan ihlaller ref bazinda ayrilmis; yeni kisa devre veya aciklanmamis ihlal yok. Geri yerlestirme listesi sonraki goreve devredilmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
26.09.2026 kapanis: AP33772S blogunun 23 uyesi (-45,+50) mm, ROTARY ENCODER grubunun R34/R35/R36 uyeleri (-30,+75) mm rijit otelendi. Grup yazilari birlikte tasindi; netler ve goreli yerlesim korundu. J9 (61,5;104) mm oldu; pin sirasi ve etiketleri korundu. J7/J8 ve diger 116 elektriksel footprint ayni; mevcut 4 iz segmenti UUID/geometri/net ayni. Baslangic yedekleri, once-sonra ref tablosu placement.json, park alani parked-blocks.png icinde. DRC baglantisiz 360->360, yeni ihlal 0. Geri yerlestirme TASK-095.
<!-- SECTION:NOTES:END -->
