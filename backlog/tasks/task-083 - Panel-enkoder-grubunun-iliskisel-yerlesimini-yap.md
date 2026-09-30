---
id: TASK-083
title: Panel enkoder grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-25 06:20'
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
- [x] #1 J9 1=A,2=GND,3=B,4=S1,5=GND pin haritası ve R34-R36 bağlantıları şemayla doğrulanmış; MCU yönüne giden hatlar ayrılmış.
- [x] #2 J9 için gerekli LCD dışı lehim/prob erişimi ve kablo büküm zarfı ölçülü tanımlanmış; güç/SW ve anten önünden geçmeyen kablo yönü seçenekleri TASK-063'e verilmiş.
- [x] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
- [x] #5 J9/enkoder yerleşim girdisi (minimum alan, kablo çıkış yönü, gerilim alma, Ethernet komşuluğu) TASK-063'e devredilmiş; son koordinat/açı/yüz ve gerçek çakışma kabulü TASK-063 sorumluluğunda.
- [x] #6 Slot tipi netleştirilmiş ve kaydedilmiş. Fiziksel yarık seçilirse genişlik/uzunluk/uç yarıçapı, üretici freze sınırı, bakır açıklığı ve kalan PCB et kalınlığı tanımlı; boş alan seçilirse keepout ve kablo zarfı ölçülü.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — TASK-083 tamamlandı:
- ROTARY ENCODER grubunun 3 üyesi (R34, R35, R36 10k 0402 pull-up dirençleri) B.Cu katmanında 2.0 mm adımla (x=40.700, 42.700, 44.700 mm, y=116.200 mm) tek tip rot 90.0° olarak hizalandı; Pad 1'ler tek +3.3V güç barasında (y=116.710 mm), Pad 2'ler paralel MCU sinyal çıkışında (GPIO21, 22, 23, y=115.690 mm) birleştirildi.
- J9 5-pin THT kablo lehim ankrajının (x=58.000, y=91.600 mm, rot -90.0°, F.Cu) pin haritası (1=ENCODER_A, 2=GND, 3=ENCODER_B, 4=ENCODER_SW, 5=GND) şematikle doğrulandı; sinyaller arası interleaved GND hatları fazlar arası kuplajı sönümler.
- Lehim ve prob erişimi: LCD modül sol kenarına (x=63.72 mm) 5.720 mm (en kötü toleransta 5.520 mm > 4.0 mm) açıklıkla 45-60° havya yaklaşımı ve 4.2 mm adımlı prob erişim koridoru sağlandı.
- Kablo büküm zarfı ve güzergâhı: 26-28 AWG (0.14 mm²) çok telli esnek kablo için R_min >= 4.5 mm (3xOD), Z >= 6.0 mm (önerilen 8.0 mm) derinlik zarfı tanımlandı. Ön panele doğrudan batı çıkışı (Seçenek A, <60 mm, en güvenli ve kısa), kuzey-batı kenar çıkışı (Seçenek B) ve alt yüz geçişi (Seçenek C) belirlendi.
- İzolasyon kuralları ve TASK-063 devri: Kablonun ESP32-C6 (U2) anteninin 15 mm keepout alanından ve buck/boost (L1, D2, L3, D4) anahtarlama hatlarından uzak tutulması şartı ve kutu duvarında J9'a <=15 mm mesafede gerilim alma (strain relief) tutucusu TASK-063'e devredildi. J9'un son koordinat/açı/yüz ve RJ45 ile çakışma kararı TASK-063 yetkisindedir.
- Slot tipi kararı: Edge.Cuts'a fiziksel freze yarığı açmak yerine iç toprak düzlemi sürekliliğini koruyan açık bord 3D keepout koridoru (6.0x24.0 mm, Z>=8.0 mm) onaylandı; fiziksel yarık parametreleri (W=2.5 mm, L=22 mm, R=1.25 mm) TASK-063 için opsiyonel olarak dokümante edildi; Edge.Cuts değiştirilmedi.
- Doğrulama: kicad-cli pcb drc --schematic-parity ile DRC 145->145 (0 yeni ihlal), unconnected 360->360, schematic parity 0; 9 ankraj ve iz UUID'leri korundu.
- Kanıtlar: design_decisions/output/PANEL_ENKODER_J9_YERLESIM_TASK083_20260924.md, hardware/docs/reports/task-083-20260924/verification.json, after.svg, drc-after.json.
<!-- SECTION:NOTES:END -->
