---
id: TASK-064
title: LCD FPC büküm yolunu ve J3 konumunu belirle
status: To Do
assignee: []
created_date: '2026-09-23 20:34'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-062
references:
  - hardware/datasheets/KLS1-242I.pdf
  - hardware/userinterface.kicad_sch
priority: high
ordinal: 104000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TFT032B018'in FPC'si modülün arkasına doğru bükülerek kart üzerindeki J3'e (KLS L-KLS1-242I-2.0-30, 30p 0,5 mm flip ZIF, yatay) girer. J3'ün konumu ve açısı FPC'nin çıkış kenarı, uzunluğu, minimum büküm yarıçapı ve kontak yüzüne göre belirlenmeli; yanlış konumda FPC gerilir, ters yüze kıvrılır veya ZIF kapağı kapanmaz.

Büküm sonrası kontak yüzü J3'ün kontak yüzüyle eşleşmeli (KLS1-242I çift temaslı, ancak pin 1 yönü ters dönmemeli). Numune doğrulaması TASK-012'de.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Datasheet'ten FPC çıkış kenarı, serbest uzunluğu, kalınlığı ve kontak yüzü okunmuş; büküm yarıçapı ≥ üretici minimumu (yoksa ≥ 1 mm) alınmış
- [ ] #2 J3 konumu ve açısı büküm geometrisinden hesaplanmış; FPC'nin J3 içine girme boyu datasheet ekleme derinliği ±0,3 mm içinde
- [ ] #3 Büküm sonrası J3 pin 1 ile LCD FPC pin 1 eşleşiyor; ZIF kapağının açılıp kapanacağı alan (önünde ve üstünde) boş
- [ ] #4 Büküm çizimi (yan kesit) design_decisions/ altında; sonuç TASK-012 numune kontrolüne girdi olarak bağlanmış
- [ ] #5 J3 PCB'de sabitlenmiş (locked) ve LCD modül izdüşümüne göre konumu User katmanında işaretli
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
