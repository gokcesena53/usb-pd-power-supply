---
id: TASK-063
title: 'USB-C ve RJ45''i sol kenara, Ethernet modülünü bottom''a yerleştir'
status: To Do
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-062
  - TASK-064
  - TASK-065
  - TASK-070
  - TASK-077
  - TASK-086
  - TASK-080
  - TASK-083
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 109000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
99,40 × 61,04 mm mevcut kartta önce mekanik yerleşimi çöz: J7 USB-C F.Cu üzerinde sol kenarda, J8 Ethernet B.Cu üzerinde USB-C'nin altında olacak. U2 ESP32-C6-MINI-1 F.Cu üzerinde, anten kısmı ana PCB dışında ve anten/mekanik şartları sağlayan USB-C'ye en yakın uygulanabilir konumda olacak. Eski sağ kenar zorunluluğu kaldırıldı. Portlar, U2/anten, LCD/FPC, H1-H4 ve J9 kablo alanını birlikte değerlendir; güç blokları bundan sonra TASK-008'de yerleştirilecek.

J9 pedleri Ethernet yanında, lehim ve kablo erişimi olan alanda konumlandırılabilir; eski koordinatı mutlak ankraj değildir. Slotun fiziksel freze yarığı mı yoksa ayrılmış kablo boşluğu mu olduğu TASK-083'te netleştirilir; netleşmeden Edge.Cuts'a yarık eklenmez. J3/FPC ve H1-H4 ankrajları korunur. Mevcut grup içi ilişkileri başlangıç kabul et, flip/taşıma sonrası kritik yerel bağlantıları yeniden denetle.

İki turlu akışta tüm blokların kaba alan planı girdidir; güç/ölçüm bloklarının zarfları ve koridorları bu mekanik seçim sırasında da kartta gösterilir. Son mekanik koordinatların tek karar sahibi bu görevdir. TASK-083 girdi sağlar; son konumu beklemez. İnce yerleşim/routing sığmazsa gerekçeli mekanik iterasyon yapılır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J7 F.Cu, J8 B.Cu; iki port ağzı sol kenara ve aynı sol kutu paneline bakıyor, RJ45 USB-C'nin altında. x/y/z merkezleri ve yönleri plan/kesitte ölçülü; J7 üretici kart kenarı ilişkisi ve RJ45 nominal 4,3 mm taşması doğrulanmış.
- [ ] #2 USB-C ve Ethernet fişleri aynı anda takılıyken gövdeler arası en az 2 mm proje açıklığı sağlanmış; RJ45 mandalı, USB-C sabitleme ayakları, J8 header/mekanik pinleri ve J9 lehimleriyle 3D çakışma yok.
- [ ] #3 U2 F.Cu, anten kısmı ana PCB dışında. En az iki aday konum/yön değerlendirilmiş, en az birinin anten/LCD/port/kablo ve kritik güzergâh koşullarını sağladığı gösterilmiş; RF koşullarını sağlayan USB-C'ye yakın seçenek gerekçeli seçilmiş.
- [ ] #4 U2 ve J7 gövdeleri mevcut LCD toleranslı izdüşümünün dışında; LCD altındaki diğer top elemanların toplam zarfı en fazla 1,80 mm. J8 top pinleri LCD dışında veya metal+lehim en fazla 1,50 mm montaj şartıyla tanımlı; toleranslı 3D kesit kaydedilmiş.
- [ ] #5 Anten keepout'u tüm bakır katmanlar, parçalar, LCD metali, USB-C/RJ45 gövdeleri, kablolar ve kutu ile kontrol edilmiş; üretici kaynak/revizyonu, gerekli boşluklar ve ölçülen mesafeler raporda.
- [ ] #6 J9'un son x/y/açı/yüz ve Ethernet yanındaki konumunu TASK-063 belirlemiş; TASK-083 slot/kablo ölçüleri uygulanmış. LCD dışı havya/prob/kablo alanı, H1-H4 ve J3/FPC erişimi doğrulanmış; sonuç TASK-008/054'e devredilmiş.
- [ ] #7 Önce/sonra top-bottom ve 3D görünümler, ref/x/y/açı/yüz listesi, DRC farkı ve schematic parity 0 kaydedilmiş. Yeni geometrik ihlal yok; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış. Son mekanik ankrajlar TASK-008/054'e devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
TASK-070 devri (24.09.2026): güncel USB-C ref J7'dir; geçici grup
ankrajı (41,05;77,32), −90°, B.Cu. D3/D8/D9/R62/R63/U10 konnektörün
pad çıkış tarafına ilişkisel yerleştirildi. Sol Edge.Cuts ağız hizası
bu konumda henüz sağlanmadığından J7 ile yedi üyeli USB-C grubunu son
kenar konumuna birlikte taşı. Taşıma sonrası D3 VBUS, D8/D9 CC,
U10 D+/D− akışı ve kısa ESD GND dönüşünü tekrar ölç; J7 footprint içi
4 mevcut hole clearance bulgusunu ayrıca çöz.
`design_decisions/output/USB_C_GIRIS_YERLESIM_TASK070_20260924.md`.

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
