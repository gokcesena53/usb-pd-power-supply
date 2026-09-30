---
id: TASK-111
title: C28 ve U13 grubunun incelenmiş boş alan yerleşimini uygula
status: To Do
assignee: []
created_date: '2026-09-28 13:46'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-109
  - TASK-110
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 197000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A ve B bölgeleri için ayrı candidate PCB içindeki dört parçalık düzenlemeyi güncel ana kartla karşılaştırarak uygula. Ana kart dosyasını eski adayla topluca değiştirme; yalnız doğrulanan konumları aktar. Fonksiyonel hiyerarşi ve Q4 mevcut konumu korunmalı.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Güncel kart hash/topoloji başlangıcı kaydedilmiş; kaynak değişmişse aday yeniden değerlendirilmiş. C28=(107.5,118.75,270°); U13=(129,120.1,0°); C35=(132.16,121,0°); R61=(125.82,121,180°), B.Cu yerleşimi doğrulanmış veya gerekçeli revizyon belgelenmiş.
- [ ] #2 U13/C35/R61 göreli grup düzeni, boost C28 ilişkisi ve U3-U13-U12/Q4 kontrol akışı korunmuş; net, değer, footprint kimliği ve sabit mekanik ankrajlar değişmemiş.
- [ ] #3 D4.1-C28.1, U3.3-U13.2 ve U13.4-Q4.1 önce/sonra ölçülmüş; aday referansları sırasıyla 3.735, 13.491 ve 8.105 mm. Ölçüler routing uzunluğu olarak sunulmamış.
- [ ] #4 Her iki yüz, courtyard, mekanik yükseklik ve DRC/parite incelenmiş. Yeni elektriksel/mekanik ihlal yok; eski 25 ihlal/360 açık bağlantı üretim kabulü sayılmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
