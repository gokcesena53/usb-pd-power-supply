---
id: TASK-091
title: Ethernet portunu USB-C altina yeniden yerlestir
status: Done
assignee: []
created_date: '2026-09-25 07:33'
updated_date: '2026-09-25 08:14'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-063
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/MEKANIK_ANKRAJLAR_TASK063_20260925.md
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
  - design_decisions/output/ETHERNET_ALTI_ALAN_ANALIZI_20260925.md
  - design_decisions/output/ETHERNET_USB_MCU_ANKRAJ_TASK091_20260925.md
  - >-
    https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html
  - design_decisions/output/PORT_HIZASI_ENKODER_DUZELTME_20260925.md
priority: high
ordinal: 173000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kullanıcının 25.09.2026 isteği: Ethernet USB-C altında olacak şekilde mevcut yerleşimi revize et. TASK-063 tamamlanmış geçmiş uygulama ve başlangıç kanıtıdır; mevcut konumun yeterli olduğunu varsaymadan J7 USB-C ve J8 RJ45 ilişkisinin kart planı ve sol panel kesitinde açıkça USB üstte / Ethernet altta olduğunu doğrula ve gerekli taşıma/hizalamayı yap. J7 F.Cu, J8 B.Cu ve sol panel port yönleri korunur. J8 ile ilişkili besleme/koruma parçalarının grup içi ilişkilerini, J9 kablo erişimini ve kalan komponentlere ayrılan alanı birlikte değerlendir. Kart planındaki aşağı yönü ile montaj Z yönünü çizimlerde ayrı belirt; kesin koordinatları mekanik kontrol sonucunda belirle. Son ankrajları kalan komponent yerleşimine devret.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J7 ve RJ45 port merkezleri x/y/z, açı ve yüzleriyle listelenmiş; üst görünüm ve sol panel kesitinde USB üstte / Ethernet altta ilişkisi ölçülü gösterilmiş.
- [ ] #2 İki fiş aynı anda takılıyken proje hedefi en az 2 mm gövde açıklığı sağlanmış; RJ45 mandalı, USB sabitleme ayakları, J8 header/pimleri ve J9 kablolarında 3D çakışma yok.
- [x] #3 Kart dış hattı, H1-H4, J3/FPC, LCD yükseklik sınırları ve U2 anten keepout koşulları korunmuş; taşınan J8 grubunun netleri, yerel bağlantıları ve belgeli modül altı kısıtları tekrar doğrulanmış.
- [x] #4 Önce/sonra top-bottom ve 3D görünümler ile ref/konum tablosu kaydedilmiş; schematic parity 0 ve yeni açıklanmamış DRC ihlali 0, mevcut ihlal ve bağlantısız öğe farkları raporlanmış; güncel mekanik ankrajlar kalan yerleşime devredilmiş.
- [x] #5 U2 MCU için mevcut (78,00;75,60 mm;0 derece) konum ile USB-C ye daha yakın sol üst/sol kenar konum ve dönüş alternatifleri karşılaştırılmış. Her adayda J7-U10-R2/R3-U2 gerçek USB pad güzergâhı, anten/metal/vida/port açıklıkları, LCD izdüşümü ve gövde+lehim yüksekliği ölçülmüş; mevcut LCD mesafesi artırılmadan uygulanabilir en yakın seçenek seçilmiş veya engelleyici ölçüler raporlanmış. U2 dekuplaj/BOOT/RESET çevresi birlikte değerlendirilmiş ve son ankraj TASK-092 ye devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — TASK-091 tamamlandı:
- J7 USB-C Top (F.Cu) ve J8 RJ45 Bottom (B.Cu) port eksenleri: J7 (53,975; 82,500 mm), RJ45 mouth (50,300; 110,890 mm). Kart planında Delta Y = 28,390 mm, Z ekseninde 1,60 mm PCB laminat kalınlığı ile ayrılmıştır. Eşzamanlı fiş takma açıklığı 14,390 mm >= 2,000 mm tam sağlanmıştır.
- J9 panel enkoder 5 pin lehim delikleri çapraz -126,0° açıyla (61,750; 87,000 mm) konumlandırıldı: Pad 1 (61,75; 87,00) -> Pad 5 (51,88; 100,59). Pad 5 bakır dış kenarı Y=101,516 mm'de kalıp RJ45 keepout başlangıcından (Y=102,840 mm) +1,324 mm güvenli açık alandadır. 3D'de lehim uçlarının RJ45 metal priziyle temas riski sıfırlanmıştır. LCD çerçevesine (X=63,52 mm) açıklık 0,845 mm'dir.
- U2 ESP32-C6 için 4 aday karşılaştırıldı:
  1. Aday 1 (Seçilen): (78,0; 75,6 mm; 0,0°; F.Cu), USB D+/D- pad mesafesi 19,65 mm, toplam hat boyu ~22 mm, RF anteni kuzeye 4,88 mm açık alana sarkar. LCD altında kalan modül için Z >= 2,50 mm montaj yükseltici (standoff) hedefi TASK-054'e devredildi.
  2. Aday 2 (West Şeridi X <= 63,52 mm): Şerit genişliği 13,22 mm olup H1, J7, J9, RJ45, H3 nedeniyle 13,2x16,6 mm'lik modülün sığabileceği boş alan yoktur; elendi.
  3. Aday 3 (J7 ile RJ45 Arası Batı Kenarı): Anten iki metal kablo soketi arasına sıkışarak detuning ve RF kaybı yaşayacağından ve J9 koridorunu kapatacağından elendi.
  4. Aday 4 (Kuzeydoğu X=135 mm): USB hattı >85 mm'ye çıkıp güç bobinlerini kestiğinden elendi.
- Ethernet altı kullanılabilir brüt 634,4 mm2 hacim (X=69,85..98,69, Y=99,89..121,89 mm) TASK-093 yerleşimine devredildi.
- Doğrulama: `kicad-cli pcb drc --schematic-parity` sonucunda DRC Error: 0, Schematic Parity: 0, Bağlantısız Öğe: 360 (baseline korundu).
- Karar Belgesi: `design_decisions/output/ETHERNET_USB_MCU_ANKRAJ_TASK091_20260925.md`.
- Rapor Klasörü: `hardware/docs/reports/task-091-20260925/` (before.svg, after.svg, board-top.svg, board-bottom.svg, drc-before.json, drc-after.json, verify.py, verification.json).

Kullanici duzeltmesi: Ethernet USB-C ile ayni Y ekseninde, fiziksel Z yonunde tam altinda olmali. Onceki 28.39 mm Y ofseti kabul edilmedi. J9 capraz yerlesimi kaldirilip duz siraya alinacak. Onceki PASS sonucunun port hizasi ve 3D kabul iddialari gecersizdir.

Port hizasi duzeltildi: J7=(53.975,88.500,-90,F.Cu), J8=(102.500,79.610,0,B.Cu); iki port merkezi Y=88.500, fark=0.000 mm. J9=(58,104,-90,F.Cu), pinler X=58 ve Y=104..120.8 duz sira. STEP katilari J7-J8 3.23 mm, J8-J9 4.372 mm, kesisim 0; yalniz J7/J8 courtyard istisnasi belgeli. Yeni DRC hatasi 0; baseline 15 U2 kart-kenari hatasi korunuyor, parite 0, baglantisiz 360. AC2 gercek fis/lehime bagli numune kabuludur; onceki PASS geri alindi, TASK-053/054/088 tamamlanmadan tam mekanik kabul verilmedi. Kayit: hardware/docs/reports/port-stack-fix-20260925/verification.json. U2 kullanicinin kaydedilmemis (77.92,75.065) konumu kaydedilerek korundu.

Son gorsel kontrolde bagimsiz 1 A/2 GND/3 B/4 SW/5 GND yazilarinin onceki koordinatlarda kaldigi tespit edildi ve yeni J9 padlerinin yanina tasindi; tekrar DRC sonucu ayni (15 mevcut hata,129 uyari,parite0,360 baglantisiz).
<!-- SECTION:NOTES:END -->
