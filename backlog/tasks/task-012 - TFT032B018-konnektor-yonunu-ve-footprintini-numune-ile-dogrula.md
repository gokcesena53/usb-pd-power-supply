---
id: TASK-012
title: TFT032B018 konnektör yönünü ve footprint'ini numune ile doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - sample-eval
milestone: m-1
dependencies:
  - TASK-064
references:
  - design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md
  - hardware/datasheets/KLS1-242I.pdf
  - hardware/datasheets/TFT032B018.pdf
priority: high
ordinal: 119000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TFT032B018 LCD ve KLS L-KLS1-242I-2.0-30 FPC konnektörü (J3) numuneleri temin edildiğinde, TASK-064'te belirlenen büküm geometrisi, J3 konumu (X=98.00, Y=109.30 rot 90) ve pin 1 yönü fiziksel numunelerle doğrulanacak:
1. FPC arkaya katlandığında Pin 1'in J3 Pin 1 (Y=102.05 mm, yukarı) ile eşleştiği ve BL_A / GND hatlarının doğruluğu
2. FPC'nin J3 stop noktasına 2.1 mm ekleme boyu ile tam oturduğu, büküm döngüsünün modül kenarından ~1.0 mm taştığı ve gerilme olmadığı
3. Stiffener kalınlığının (0.3 mm) KLS1-242I kapağını zorlamadan kilitlediği
4. J3 gövde yüksekliğinin (2.0 mm) LCD arka yüzü ile kart arasındaki boşluğa uygunluğu
Ön panel/kutu ölçüleri 3,2" modüle (77,7 x 55,04 mm) göre güncellenmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J3 pin 1 yönü ve FPC temas yüzü numuneyle doğrulandı (TASK-064 kararı ile uyumlu)
- [ ] #2 KLS footprint'i (Connector_FPC_Custom) numuneye uyuyor; ekleme boyu ve ZIF kilitleme doğrulandı
- [ ] #3 Kutu/ön panel ölçüleri güncellendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — TASK-065 mekanik tolerans girdisi:
KLS çizimindeki J3 kapalı yüksekliği 2,00±0,15 mm. LCD arka yüz–PCB top
montaj hedefi 2,35±0,15 mm (en az 2,20 mm), J3 dışında top zarf bütçesi 1,80 mm.
TASK-064'ün nominal 2,00 mm boşluğu doğrudan mesafe parçası ölçüsü yapılmamalı.
Numunede gerçek boşluk, köpük/boss toleransı, kapağın serbest kapanması,
FPC kıvrımı ve gerilimsiz takılması doğrulanmalı. Kaynak:
`design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
<!-- SECTION:NOTES:END -->
