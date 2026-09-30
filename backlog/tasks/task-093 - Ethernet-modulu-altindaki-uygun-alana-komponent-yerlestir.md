---
id: TASK-093
title: Ethernet modulu altindaki uygun alana komponent yerlestir
status: To Do
assignee: []
created_date: '2026-09-25 07:42'
updated_date: '2026-09-25 08:10'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-091
  - TASK-080
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/ethernet-underlay-analysis-20260925/geometry.json
  - design_decisions/output/PORT_HIZASI_ENKODER_DUZELTME_20260925.md
documentation:
  - design_decisions/output/ETHERNET_ALTI_ALAN_ANALIZI_20260925.md
priority: high
ordinal: 175000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kullanıcının 25.09.2026 isteği: B.Cu üzerindeki Ethernet mezanini J8 ile anakart arasındaki uygun hacmi aktif komponent yerleşiminde kullan. Ethernet altı alan analizini uygula; önceki TASK-080 tüm yardımcı parçaları dışarıda tutma tercihi bu görevle revize edilir. TASK-091 son J8/USB/MCU/J9 ankrajları girdidir. Öncelik C20/R17/C21 ve yükseklik/termal uygunlukla Q8/C10 Ethernet hücresi; sonra R34/R35/R36 enkoder dirençleri ve güzergâh uygunsa Q1/Q2/R4/R5/R6/R7 I2C hücresidir. Yerleşimi sadece modül dışına yapmak bu isteği karşılamaz. RJ45 bacak keepout ve header gövdesini boş tut; test erişimini ve kritik döngüleri koru. 1,90 mm yükseklik eski rapor varsayımıdır; numune garantisi değildir. Şema/BOM/modül değişikliği ve genel routing kapsam dışıdır. Model/MPN verileriyle ön yerleşim yapılabilir; numune ölçüsü TASK-053, üretim öncesi yeniden kabul TASK-088 kapsamındadır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Son J8 konum/açı/yüzüne göre yerel ve kart koordinatlarında XY/Z haritası hazırlanmış; RJ45 lehim/pin keepout, header, MP delikleri, J9 THT uçları, J3 karşı yüz ve routing/erişim alanları ayrılmış. Brüt ve net kullanılabilir alan mm² cinsinden ayrı kayıtlı.
- [ ] #2 Her aday ref için kesin MPN, veri sayfası/model kaynağı, maksimum montaj yüksekliği, modül yerel alt çıkıntısı, minimum ara mesafe, tolerans bütçesi ve kalan açıklık listelenmiş; pozitif tasarım marjı gerekçeli. 1,90 mm veya paket kodu tek başına uygunluk kanıtı sayılmamış.
- [ ] #3 Uygun reflerden oluşan en az bir işlevsel hücrenin tamamı veya elektriksel ilişkisi korunmuş alt kümesi modülün kullanılabilir orta hacmine gerçekten yerleştirilmiş; ref/x/y/açı/yüz, parça sayısı ve kaplanan alan kayıtlı. Hiçbir aday uygun değilse ölçülü engeller raporlanmış ve görev Done yapılmamış.
- [ ] #4 C20 ve C10 için J8 ETH_3V3/GND dönüşü, R17/C21 için Q8 gate/source yakınlığı doğrulanmış; Q8 iletim/açılış kaybı hesaplanmış. Ek grup seçimi I2C bus ve enkoder/MCU güzergâhlarını bozmadığı gösterilerek yapılmış; MCU dekuplajı MCU yanında kalmış.
- [ ] #5 TP14 ve servis/test noktalarına modül takılıyken erişim korunmuş; RJ45 mutlak keepout ile pin/delik açıklıkları ihlal edilmemiş. Modül öncesi dizgi/muayene ve sonrasında söküm/yeniden işleme sırası belgelenmiş.
- [ ] #6 Son top-bottom ve 3D kesitlerde seçili refler ile tüm modül altı çıkıntılar incelenmiş; yalnız kanıtlı J8-ref çiftleri courtyard istisnasına alınmış. Genel DRC bastırılmamış; schematic parity 0, yeni açıklanmamış geometrik/elektriksel ihlal 0, bağlantısız öğe ve mevcut ihlal farkları ayrı raporlanmış.
- [ ] #7 Varsayıma dayalı yükseklikler açıkça işaretlenip TASK-053 numune kontrol listesine devredilmiş; TASK-088 üretim kabulü için her yerleştirilen ref ile gerçek ölçü karşılaştırması zorunlu kılınmış. Son alan haritası TASK-092 ve kritik güzergâhlar TASK-008 e devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Son ankraj duzeltmesi: J7=(53.975,88.5,-90,F.Cu), J8=(102.5,79.61,0,B.Cu), J9=(58,104,-90,F.Cu). Portlar ayni Y=88.5 merkezinde. Ethernet orta brut seridi X=69.85..98.69 Y=77.5..99.5; eski Y=99.89..121.89 haritasi gecersiz. Son karar PORT_HIZASI_ENKODER_DUZELTME_20260925.md; USB delik/ayak izdususunu da dikkate al.
<!-- SECTION:NOTES:END -->
