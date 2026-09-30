---
id: TASK-058
title: 'PCB: U6 TLV431 pad sırası ve D5 SOD-323 güncellemesi'
status: To Do
assignee: []
created_date: '2026-09-23 12:54'
updated_date: '2026-09-23 15:18'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-057
references:
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
ordinal: 121000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-057 şema değişikliğinin PCB'ye aktarılması. U6'nın SOT-23 kılıfı aynı kalıyor ama pin eşlemesi değişti: pad 1 = REF, pad 2 = K. D5'in footprint'i Diode_SMD:D_SOD-123 yerine D_SOD-323 oldu. R42 kaldırıldı, R43'ün değeri değişti (2512 kalıyor).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PCB 'Update from schematic' sonrası U6 pad1 = Net-(U6-REF), pad2 = EN_CTRL, pad3 = GND
- [x] #2 D5 SOD-323; pad1 (katot) EN_CTRL, pad2 (anot) BOOST_FB
- [ ] #3 R42 PCB'den silindi; DRC 0 hata, bağlanmamış öğe yok
- [x] #4 D5, U11 FB pinine yakın: BOOST_FB yolu ≤10 mm
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026: TASK-006 (commit 1792ccb) ile PCB şemadan güncellendi. AC#1 ve AC#2 pad netleri doğrulandı: U6 1=Net-(U6-REF) 2=EN_CTRL 3=GND; D5 D_SOD-323 1=EN_CTRL 2=BOOST_FB; R42 silindi. D5 yeni footprint olarak kart dışında; AC#3 (DRC 0) ve AC#4 (≤10 mm) yerleşim işi (TASK-008).

24.09.2026: D5 U11'in yanına (60,05; 57,60) taşındı, 180° çevrildi; pad 2 (anot, BOOST_FB) ile U11 pad 9 (FB) arasına 0,20 mm F.Cu iz çekildi. İz uzunluğu KiCad pcbnew ile **2,585 mm** (≤10 mm). Pad 1 (katot) EN_CTRL, U6 padları 1=REF / 2=EN_CTRL / 3=GND, R42 yok; `hardware/docs/reports/task-058-20260924/place_d5.py` ile yeniden üretilebilir. DRC kanıtı aynı klasördeki `before-drc.json` ve `after-drc.json`: öncesi 19 hata + 129 uyarı / 361 bağlantısız, sonrası 19 hata + 129 uyarı / 360 bağlantısız. Yeni DRC ihlali yok. D5 pad 1 ve diğer EN_CTRL/REF bağlantıları hâlâ açık; kart genelindeki yerleşim ve yönlendirme tamamlanmadan AC#3 sağlanmıyor. Devre kararı değişmedi; karar belgesi ve CHANGES.TXT için yeni kayıt gerekmiyor.
<!-- SECTION:NOTES:END -->
