---
id: TASK-080
title: Ethernet mezanin grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 13:22'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf
  - hardware/datasheets/TSM3443CX6.pdf
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
  - design_decisions/output/ETHERNET_MEZANIN_YERLESIM_TASK080_20260924.md
  - hardware/docs/reports/task-080-20260924/verification.json
  - hardware/docs/reports/task-080-20260924/after.svg
  - hardware/docs/reports/task-080-20260924/drc-after.json
priority: medium
ordinal: 162000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI. Güncel kapsam: J8, Q8, R17, C10, C20, C21, TP14. J8 modül ankrajı etrafında Q8 besleme anahtarı ve kapasiteleri düzenle. Modül iç devresini yeniden yerleştirme; anakart elemanlarını düzenle. TASK-063 bottom ve sol RJ45 kenar kararını esas al.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.

TASK-063 mekanik yerleşim girdileriyle Ethernet altını ek alan olarak değerlendir. Nominal 2,5 mm ara mesafe ve yaklaşık 2,2 mm RJ45 lehim çıkıntısı tüm modül altında eşit kullanılabilir yükseklik değildir. Önce Q8/R17/C10/C20/C21 gibi kendi kontrol/besleme parçalarını, sonra bağlantısı uygun düşük profilli az ısınan parçaları değerlendir; sıcak güç devrelerini buraya sıkıştırma. Modül altını kullanmak genel yerleşimin zorunlu koşulu değildir.

Bu grup görevi TASK-063 son konumunu beklemez: yerel J8 koordinatlarında hacim/keepout haritası ve aday parça zarfları üretir, TASK-063'e girdi verir. Yüksekliği doğrulanmış aynı yüz mezanin altı yerleşimleri için yalnız belirli ref çiftlerine belgeli courtyard istisnası uygulanabilir; elektriksel açıklık/short kontrolleri ve RJ45 keepout'u gevşetilmez.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Q8 source/drain/gate, R17 ve yumuşak açılış kapasitelerinin işlevleri netlerden doğrulanmış; besleme akım döngüsü ve bypass yolları kısa tutulmuş.
- [x] #2 J8 modül altı, RJ45, header çıkıntısı ve LCD çakışma alanları gösterilmiş; TP14 ve UART hatlarının erişimi korunmuş.
- [x] #3 Anahtarlanan ETH_3V3 koridoru ve MCU kontrol/UART bağlantı yönleri ayrılmış.
- [x] #4 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #5 Grup üyeliği/net/polarite ve yerel ankrajlar korunmuş; yeni açıklanmamış courtyard veya elektriksel clearance ihlali yok, schematic parity 0. İzinli J8–alt parça courtyard çiftleri ref/XY/Z/tolerans/3D kanıtı ile kayıtlı; diğer parça çiftlerinde DRC denetimi etkin. Önce/sonra kanıtı ve bağlantısız öğeler ayrı raporlanmış.
- [x] #6 Modül altı için XY bazında kullanılabilir Z yüksekliği, RJ45 pim keepout'u, header/mekanik pin ve lehim erişim bölgeleri ölçülü haritada; bottom flip sonrası keepout yüzü doğrulanmış. Nominal değerler ve TASK-053 numune doğrulaması ayrı belirtilmiş.
- [x] #7 Her aday ref için maksimum gövde+lehim zarfı, modül altı çıkıntı/toleranslar ve kalan açıklık listelenmiş; dayanağı olmayan genel ≤2 mm kabulü yok. Uygun olmayan parçaların modül dışı alternatifi var; TP14 erişilebilir.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.

24.09.2026 — TASK-080 tamamlandı:
- ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI grubunun 7 üyesi (J8, Q8, R17, C21, C10, C20, TP14) B.Cu katmanında ilişkisel olarak yerleştirildi.
- Q8 TSM3443CX6 P-MOSFET yüksek taraf anahtarı (SOT-26, rot 90°), R17 (100k 0402) gate pull-up ve C21 (100n 0402) yumuşak açılış kapasitesi batıda giriş/kontrol koridorunda (y=140.5..144.5 mm) konumlandırıldı (tau_on ≈ 0.91 ms, inrush ~62 mA; tau_off ≈ 10 ms).
- C20 (100n 0402) ve C10 (22uF 0805) dekuplaj/bulk kapasiteleri Q8 Drain ile J8 Pins 11--14 arasında doğrudan (<4.3 mm) güç ve GND dönüş koridoru oluşturdu; döngü alanı <15 mm² ile sınırlandı.
- TP14 (D1.0mm) teşhis pedi J8 Pin 4 (ETH_RUN) çıkışında modül gövdesi dışında açık alana yerleştirildi; osiloskop/multimetre probları için %100 fiziksel erişim sağlandı.
- Kuzey güç koridoru (y=140.5..146.5 mm) ile güney UART/sinyal koridoru (y=150.0..158.5 mm) arasında 5.08 mm (2 header pini) fiziksel izolasyon sağlandı.
- Modül altı 3D yükseklik haritası ve zarf analizi yapıldı: Header bölgesi (Z=0 B.Cu), orta boşluk (nominal Z=2.50 mm, min tolerans Z=1.90 mm), RJ45 pim lehim çıkıntısı (~2.20 mm çıkıntı, 0.30 mm nominal açıklık -> anakartta MUTLAK KEEPOUT). 6 yardımcı eleman modül gövdesi dışında header batısına yerleştirilerek 0 courtyard çakışması, %100 optik kontrol/rework ve TP14 prob erişimi sağlandı.
- Doğrulama: kicad-cli pcb drc --schematic-parity ile DRC 145->145 (yeni ihlal: 0), unconnected 360->360, schematic parity 0; 9 ankraj ve iz UUID'leri korundu.
- Kanıtlar: design_decisions/output/ETHERNET_MEZANIN_YERLESIM_TASK080_20260924.md, hardware/docs/reports/task-080-20260924/verification.json, after.svg, drc-after.json.
<!-- SECTION:NOTES:END -->
