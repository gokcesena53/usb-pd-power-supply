---
id: TASK-113
title: Boş alanların güç sinyal ve mekanik kullanım planını kesinleştir
status: To Do
assignee: []
created_date: '2026-09-28 13:46'
labels:
  - layout
  - docs
milestone: m-1
dependencies:
  - TASK-112
  - TASK-063
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 199000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PLAN.md A/B/C/D haritasını güncel yerleşimde doğrula. Kullanılabilir alanları fonksiyonel aidiyetiyle değerlendir; güç, dönüş, arayüz ve servis alanlarını koru. Routing uygulamasını mevcut TASK-087 üzerinden yürüt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 C bölgesi F.Cu X70-100/Y85-98 arayüz koridoru; D bölgesi F.Cu X105-140/Y88-96 kullanıcı güç kolunun doğu kesimi olarak değerlendirilmiş. Bu pencerelerin tüm güzergâhı garanti etmediği belirtilmiş.
- [ ] #2 R11-Q5-shunt-J4 ve Q3-boost-buck kolları için geçiş alanı, dönüş yolu ve Kelvin ayrımı çizilmiş; güç bakırı/via boyutlandırma girdileri TASK-087 ye aktarılmış.
- [ ] #3 U2 anten, H1-H4, USB/RJ45/encoder ankrajları, kablo/servis hacmi, J8 pinleri ve LCD/mezanin yüksekliği korunmuş. Tarihsel LCD 1.80 mm varsayımı güncel mekanik veriyle doğrulanmış; tüm J8 altı otomatik olarak boş kabul edilmemiş.
- [ ] #4 Son alan haritasında doldurulacak ve işlevi nedeniyle boş kalacak bölgeler gerekçeli; her taşınan ref ait olduğu hiyerarşik blokla kayıtlı. Kart sınırı değiştirilmemiş.
- [ ] #5 TASK-087 için son yerleşim hash, net/grup haritası, kritik ölçüler ve çözülmesi gereken DRC listesi devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
