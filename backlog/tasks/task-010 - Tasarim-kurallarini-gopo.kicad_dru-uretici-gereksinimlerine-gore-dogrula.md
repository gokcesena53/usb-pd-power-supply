---
id: TASK-010
title: Tasarım kurallarını (gopo.kicad_dru) üretici gereksinimlerine göre doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_dru
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: medium
ordinal: 125000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Üretici seçildi ve yetenekleri not edildi
- [ ] #2 gopo.kicad_dru buna göre güncellendi
- [ ] #3 Üretici katman dizilimi, dielektrik/bakır kalınlıkları, min iz/aralık/via/delik/freze ve kenar açıklıkları kayıtlı; USB için empedans hesabı ve bottom güç/sinyal referans dönüş planı hazırlanmış.
- [ ] #4 Her özel DRC kuralının güncel ref/net ile eşleşmesi doğrulanmış; USB-C eski J1 yerine J7 için kontrol edilmiş, U9 gibi diğer eski seçiciler de denetlenmiş. Kuralın çalıştığı kontrollü örnek/raporla kanıtlı; çözüm yalnız limit gevşetme değil.
- [ ] #5 U11 0,2 mm termal via ile min delik kuralı çelişkisi üretici kabiliyeti/footprint seçimiyle çözülmüş; mezanin courtyard istisnası yalnız kanıtlı ref çiftlerine sınırlı tasarlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026 (TASK-006): U11 footprint'i Package_SO:Texas_HTSSOP-14-1EP_..._ThermalVias 0.2 mm termal via delikleri içeriyor; gopo.kicad_dru/board setup min delik 0.3 mm -> 15x drill_out_of_range. Üreticinin min deliği netleşince ya kural ya da footprint (ThermalVias'sız varyant + elle via) seçilmeli.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
