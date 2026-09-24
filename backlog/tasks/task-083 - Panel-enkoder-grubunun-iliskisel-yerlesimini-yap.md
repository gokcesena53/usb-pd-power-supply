---
id: TASK-083
title: Panel enkoder grubunun iliskisel yerlesimini yap
status: To Do
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf
  - design_decisions/output/ENCODER_PANEL_TASK066_20260924.md
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: medium
ordinal: 165000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-063'ün mekanik seçiminden önce J9 enkoder bağlantısının yer ihtiyacını tanımla: beş tel pin haritası, lehim/havya/prob erişimi, minimum kablo büküm zarfı, gerilim alma ve slot tipi/ölçüleri. R34–R36 pull-up grubunun göreli ilişkisel yerleşimini hazırla; şemada olmayan RC/ESD parçaları ekleme. J9'un son x/y/açı/yüz kararının sahibi TASK-063'tür; bu görev o son kararı beklemeden ölçülü girdisini verir. Eski J9 koordinatı mutlak ankraj değildir. Fiziksel slot kararı olmadan Edge.Cuts değiştirilmez.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J9 1=A,2=GND,3=B,4=S1,5=GND pin haritası ve R34-R36 bağlantıları şemayla doğrulanmış; MCU yönüne giden hatlar ayrılmış.
- [ ] #2 J9 için gerekli LCD dışı lehim/prob erişimi ve kablo büküm zarfı ölçülü tanımlanmış; güç/SW ve anten önünden geçmeyen kablo yönü seçenekleri TASK-063'e verilmiş.
- [ ] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [ ] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
- [ ] #5 J9/enkoder yerleşim girdisi (minimum alan, kablo çıkış yönü, gerilim alma, Ethernet komşuluğu) TASK-063'e devredilmiş; son koordinat/açı/yüz ve gerçek çakışma kabulü TASK-063 sorumluluğunda.
- [ ] #6 Slot tipi netleştirilmiş ve kaydedilmiş. Fiziksel yarık seçilirse genişlik/uzunluk/uç yarıçapı, üretici freze sınırı, bakır açıklığı ve kalan PCB et kalınlığı tanımlı; boş alan seçilirse keepout ve kablo zarfı ölçülü.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
