---
id: TASK-114
title: Otomatik dizgi ve lehimleme için montaj DFM kabulünü tamamla
status: To Do
assignee: []
created_date: '2026-09-28 13:47'
labels:
  - layout
  - fabrication
milestone: m-1
dependencies:
  - TASK-087
  - TASK-110
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 200000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Son route edilmiş kart için dizgiciyle üretim sürecini doğrula ve TASK-088 üretim öncesi kabulüne kanıt sağla. Geometrik aralık tablosu süreç uygunluğunun yalnız bir girdisidir; numune sonuçları gerçekleşmeden garanti veya başarılı test iddia etme.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Montajcıya ait nozzle/komponent açıklıkları, çift yüz montaj sırası, ağır eleman tutunması, yeniden işleme ve test erişimi son kartta doğrulanmış; daha sıkı üretici kuralları uygulanmış.
- [ ] #2 Fiducial ve gerekiyorsa panel rayları, CPL merkez/açı/yüzleri, BOM-footprint eşleşmesi ve polariteler kontrol edilmiş.
- [ ] #3 Stencil kalınlığı/açıklıkları, termal pad paste düzeni, solder-mask büyümesi ve web limitleri seçilen süreçle doğrulanmış; mm tablosu son kabul değerleriyle güncellenmiş.
- [ ] #4 Üretici DFM sonucu, açık konular ve kart hash TASK-088 e bağlı; açık üretim engeli varsa kabul verilmemiş. Numune lehim/AOI/elektriksel kontrol kriterleri ve ilgili prototip görevlerine devir belgelenmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
