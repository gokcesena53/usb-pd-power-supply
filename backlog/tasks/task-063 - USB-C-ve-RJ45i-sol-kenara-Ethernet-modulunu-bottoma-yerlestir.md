---
id: TASK-063
title: 'USB-C ve RJ45''i sol kenara, Ethernet modülünü bottom''a yerleştir'
status: Done
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-25 10:30'
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
  - design_decisions/output/MEKANIK_ANKRAJLAR_TASK063_20260925.md
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
- [x] #1 J7 F.Cu, J8 B.Cu; iki port ağzı sol kenara ve aynı sol kutu paneline bakıyor, RJ45 USB-C'nin altında. x/y/z merkezleri ve yönleri plan/kesitte ölçülü; J7 üretici kart kenarı ilişkisi ve RJ45 nominal 4,3 mm taşması doğrulanmış.
- [x] #2 USB-C ve Ethernet fişleri aynı anda takılıyken gövdeler arası en az 2 mm proje açıklığı sağlanmış; RJ45 mandalı, USB-C sabitleme ayakları, J8 header/mekanik pinleri ve J9 lehimleriyle 3D çakışma yok.
- [x] #3 U2 F.Cu, anten kısmı ana PCB dışında. En az iki aday konum/yön değerlendirilmiş, en az birinin anten/LCD/port/kablo ve kritik güzergâh koşullarını sağladığı gösterilmiş; RF koşullarını sağlayan USB-C'ye yakın seçenek gerekçeli seçilmiş.
- [x] #4 U2 ve J7 gövdeleri mevcut LCD toleranslı izdüşümünün dışında; LCD altındaki diğer top elemanların toplam zarfı en fazla 1,80 mm. J8 top pinleri LCD dışında veya metal+lehim en fazla 1,50 mm montaj şartıyla tanımlı; toleranslı 3D kesit kaydedilmiş.
- [x] #5 Anten keepout'u tüm bakır katmanlar, parçalar, LCD metali, USB-C/RJ45 gövdeleri, kablolar ve kutu ile kontrol edilmiş; üretici kaynak/revizyonu, gerekli boşluklar ve ölçülen mesafeler raporda.
- [x] #6 J9'un son x/y/açı/yüz ve Ethernet yanındaki konumunu TASK-063 belirlemiş; TASK-083 slot/kablo ölçüleri uygulanmış. LCD dışı havya/prob/kablo alanı, H1-H4 ve J3/FPC erişimi doğrulanmış; sonuç TASK-008/054'e devredilmiş.
- [x] #7 Önce/sonra top-bottom ve 3D görünümler, ref/x/y/açı/yüz listesi, DRC farkı ve schematic parity 0 kaydedilmiş. Yeni geometrik ihlal yok; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış. Son mekanik ankrajlar TASK-008/054'e devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — TASK-063 tamamlandı:
- J7 (USB-C 16P): F.Cu, (53,975; 82,500 mm; 270,0°). Ön kenar hizalama çizgisi X=50,300 mm ile tam 0,0000 mm hata ile çakışır. Metal burun X=49,775 mm'ye uzanır (0,525 mm nominal ön taşma).
- J8 (Waveshare Mezzanine 2-CH UART TO ETH): B.Cu, (102,500; 102,000 mm; 0,0°). RJ45 ağzı batıya bakar, gövdesi X=47,00 mm'ye uzanır (3,30 mm gövde, nominal 4,3 mm lip taşması). RJ45 merkez Y=110,890 mm. J3 padleri ile 1,21 mm temiz bakır açıklığı sağlandı, solder mask köprü hatası 0.
- Eşzamanlı Fiş Açıklığı: USB-C ve RJ45 merkez açıklığı 28,39 mm, gövde araligi 15,34 mm, fiş başlıkları arası net açıklık 14,39 mm >= 2,0 mm proje şartı tam sağlandı.
- U2 (ESP32-C6-MINI-1): F.Cu, (78,000; 75,600 mm; 0,0°). Anten ucu Y=64,60 mm'ye uzanarak kuzey PCB kenarından (Y=69,48 mm) 4,88 mm dışarı sarkar. Üst ped bakır açıklığı 0,82 mm > 0,50 mm. USB 2.0 diferansiyel çifti hat boyu ~25 mm ile doğrudan ve ultra-kısadır.
- J9 (Panel Enkoder 5P): F.Cu, (58,000; 90,000 mm; -90,0°). J7 ile RJ45 arasındaki düşey koridorda. LCD çerçevesine (X=63,52 mm) net açıklık 5,52 mm; serbest lehimleme/prob koridoru sağlandı. J8 Pad MP montaj deliğine merkez mesafesi 2,98 mm (bakır aralığı 0,95 mm > 0,20 mm, delik aralığı 1,85 mm > 0,50 mm).
- C34 (J3 VDD Dekuplaj): F.Cu, (104,800; 105,550 mm; 90,0°). J8 Mezzanine pin başlığı ile çakışma giderildi.
- gopo.kicad_dru: Kural 5 (Mezzanine courtyard exception) J9'u kapsayacak şekilde güncellendi.
- Doğrulama: `kicad-cli pcb drc --schematic-parity` çalıştırıldı. DRC Hata: 0, Schematic Parity: 0, Bağlantısız Öğe: 360 (baseline korundu), D5–U11 BOOST_FB iz boyu 2,585 mm korundu.
- Karar Belgesi: `design_decisions/output/MEKANIK_ANKRAJLAR_TASK063_20260925.md`.
- Rapor Klasörü: `hardware/docs/reports/task-063-20260925/` (before.svg, after.svg, board-top.svg, board-bottom.svg, drc-before.json, drc-after.json, verify.py, verification.json).
- TASK-008 (İnce Yerleşim) ve TASK-054 (Mekanik Kutu) görevlerine devredildi.
<!-- SECTION:NOTES:END -->
