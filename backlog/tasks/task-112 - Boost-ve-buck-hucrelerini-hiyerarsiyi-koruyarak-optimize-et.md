---
id: TASK-112
title: Boost ve buck hücrelerini hiyerarşiyi koruyarak optimize et
status: To Do
assignee: []
created_date: '2026-09-28 13:46'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-111
  - TASK-008
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 198000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Boş alanı aynı fonksiyonel blok içindeki güç hücrelerini iyileştirmek için kullan. Boost ve buck için ayrı önce/sonra kanıt üret; yalnız görsel sıkıştırma veya grup merkezlerine göre sıralama yeterli değildir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Boost L3/U11/D4/C27/C28 akım ve dönüş yolları datasheet pinleriyle gösterilmiş; L3-U11, U11-D4 ve D4-kapasitör mesafeleri, SW alanı ve tasarlanan sıcak döngü değerlendirilmiş.
- [ ] #2 Buck U5/C12/C13/C14/L1/D2 giriş ve GND döngüleri değerlendirilmiş; C16 çıkış tarafında, FB ve COMP hassas yolları SW/LX alanından ayrılmış.
- [ ] #3 Parçalar ilgili fonksiyonel grupta tutulmuş; iki güç kolu ve kontrol hiyerarşisi korunmuş. Kritik mesafe/döngü kötüleşmeleri çözülmüş veya hesap ve kaynakla gerekçelendirilmiş.
- [ ] #4 TASK-110 aralıkları, sabit ankrajlar ve mekanik hacimler sağlanmış; iki yüz görüntüsü, pad/net ölçüleri, DRC/parite ve routing önerisi TASK-087 için hazırlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
