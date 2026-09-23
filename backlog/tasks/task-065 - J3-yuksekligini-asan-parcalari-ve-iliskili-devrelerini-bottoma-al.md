---
id: TASK-065
title: J3 yüksekliğini aşan parçaları ve ilişkili devrelerini bottom'a al
status: To Do
assignee: []
created_date: '2026-09-23 20:34'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-061
  - TASK-064
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/KLS1-242I.pdf
priority: high
ordinal: 105000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
LCD modülü kartın top yüzüne J3 yüksekliği kadar yakın oturur. Bu yüzden gövde yüksekliği J3'ü (KLS1-242I-2.0, ~2,0 mm; kesin değer TASK-061 modelinden/datasheet'ten) aşan her parça LCD izdüşümü içinde top'ta kalamaz ve bottom'a alınır.

Bir parça bottom'a giderse onunla aynı akım döngüsünü veya kısa bağlantı gerektiren devreyi paylaşan parçalar da aynı tarafa gider. Örnek: DC-DC bobini (L1 FPI0705 5,0 mm, L3) J3'ten yüksekse bottom'a iner, dolayısıyla ilgili regülatör (U5 AOZ1284 / U11 TPS55340), giriş/çıkış kapasiteleri, diyot ve FB/COMP ağı da bottom'a iner; döngü katman değiştirmemeli.

Aday uzun parçalar (TASK-061 sonrası kesinleşir): L1, L3, C33 süperkapasitör, SW3 enkoder (panel parçası, ayrı değerlendirilir), J1 USB-C, CR2032 tutucu, elektrolitik/polimer kapasiteler.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J3 gövde yüksekliği (h_J3) datasheet'ten mm cinsinden yazılmış; LCD alt yüzü ile kart arasındaki boşluk ve kullanılan pay (ör. h_J3 − 0,2 mm) karar dosyasında
- [ ] #2 3D modellerden tüm parçaların yükseklik listesi çıkarılmış; h > h_J3 olan her parça ve yanına gelen ilişkili parçalar (ref listesi) design_decisions/ altında tablo
- [ ] #3 LCD izdüşümü içinde top tarafta h > h_J3 olan parça 0 (3D görünüm veya betikle doğrulanmış); SW3 gibi panel parçaları izdüşüm dışında
- [ ] #4 Her DC-DC bloğunun (U5, U11, backlight) güç döngüsü parçaları (IC, bobin, Cin, Cout, diyot/FET, FB/COMP) tek tarafta; döngü katman değiştirmiyor
- [ ] #5 Bottom'a alınan parçalar için dizgi etkisi (çift taraflı SMT, ağır parçaların reflow yönü) TASK-015'e not düşülmüş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
