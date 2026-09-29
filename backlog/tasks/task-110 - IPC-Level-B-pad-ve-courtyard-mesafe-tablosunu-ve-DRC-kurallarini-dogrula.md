---
id: TASK-110
title: IPC Level B pad ve courtyard mesafe tablosunu ve DRC kurallarını doğrula
status: To Do
assignee: []
created_date: '2026-09-28 13:46'
labels:
  - layout
  - fabrication
  - docs
milestone: m-1
dependencies:
  - TASK-109
  - TASK-010
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 196000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PLAN.md bölümlerindeki aralık tablosunu footprint ailesi, standart baskısı ve seçilen dizgicinin yetenekleriyle doğrula. Class 2 kabul sınıfı ile Level B nominal land-pattern yoğunluğunu ayır. Tek bir mesafenin otomatik dizgi veya lehimlemeyi garanti ettiği iddia edilmemeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 SMD pasifler, SOT/SOIC/TSSOP, QFN/WSON ve özel gövdeler için bileşenler arası minimum pad-to-pad ve courtyard-to-courtyard değerleri mm tablosunda; kaynak, baskı, varsayım ve üretici limitiyle verilmiş. Aynı IC içindeki pad aralıkları ayrı tutulmuş.
- [ ] #2 Pad/gövde maksimum toleransları ve courtyard excess doğrulanmış. E1+G+E2 hesabı yalnız uygun pad-tanımlı zarf için kullanılmış; 0402 ve diğer aile farkları açıklanmış.
- [ ] #3 Ek courtyard açıklığı G=0.20 mm proje hedefi ve QFN/WSON servis yönünde G=0.50 mm hedefi üreticiyle değerlendirilmiş; bunlar evrensel IPC minimumu olarak sunulmamış.
- [ ] #4 KiCad kurallarında pozitif courtyard açıklığı uygulanmış veya eşdeğer ölçüm denetimi hazırlanmış. Bakır clearance, mask web, paste ve courtyard kuralları ayrı doğrulanmış; J7/J8 istisnaları gerekçeli ve sınırlı.
- [ ] #5 R56-R58 çizgi merkezi 0.20 mm ile çizgi kenarı 0.15 mm ayrımı açıklanmış. Değişiklik sonrası DRC ve tüm footprint aralıkları raporlanmış; yeni kuralla ortaya çıkan eksikler saklanmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
