---
id: TASK-008
title: Kritik yerleşim kurallarını uygula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-25 07:43'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-006
  - TASK-065
  - TASK-063
  - TASK-085
  - TASK-010
  - TASK-092
references:
  - hardware/datasheets/LM7480-Q1.pdf
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 123000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-063 mekanik yerleşimi ve TASK-085 grup devrinden sonra genel kart yerleşimini tamamla. Sıra: portlar → U2/anten → J9/kablo alanı → güç blokları → diğer küçük devreler. J7/U2 top, J8 bottom; anten PCB dışında ve RF şartlarını sağlayan USB-C'ye yakın konumda. AOZ1284 buck ve TPS55340 boost B.Cu üzerinde ESP32/anten bölgesinden uzakta; anahtarlama düğümleri ve bobinler MCU/anten altına getirilmez.

Yüksek akım çıkış yolu J4'e doğrudan ilerlemeli; LM74801/MOSFET, şönt ve INA226 birbirine uygun yönde yerleşmeli. Modül altı alan yalnız TASK-080'in kullanılabilir yükseklik haritasına göre kullanılır. Öncelik mekanik/RF sınırları, kısa kritik akım döngüleri ve kesintisiz dönüş yolları, sonra kritik sinyal koridorları ve ratsnest sadeliğidir. Genel routing'in tamamlanması bu yerleşim görevinin bitiş şartı değildir.

İki turlu akışın ikinci turu: tüm blokları birlikte dikkate alan kaba plan ve TASK-063 mekanik seçimi üzerine ince yerleşim yap. Yerleşim kesinleşmeden kritik hatları gerçek iz/via veya ölçülü güzergâh denemesiyle geçir; mekanik değişiklik gerekiyorsa TASK-063 kabulünü yeniden doğrula. Nihai bütün routing ayrı görevde tamamlanır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 D3 SMBJ30A ve C3 J7 girişine yakın; CC1/CC2 AP33772S yönüne kısa koridorla çıkıyor. J7 top'a geçiş sonrası ESD yerleşimi ve kısa GND dönüşleri yeniden doğrulanmış.
- [ ] #2 U10 D+/D- flow-through (1-6, 3-4); J7–U10–U2 USB çifti için sürekli GND referanslı ve az katman geçişli koridor ayrılmış, R2/R3 MCU tarafında.
- [ ] #3 U12 A/DGATE/C pinleri Q5B S/G/D, HGATE/OUT pinleri Q5A G/S yönüne bakıyor; DGATE kısa. C32 VS/GND'ye yakın, C31 MOSFET ısısından uzak.
- [ ] #4 LM74801/MOSFET, RShunt1, INA226 ve J4 yönleri kısa/doğrudan çıkış güç yolu sağlıyor; şönt Kelvin yolları güç akımından ayrı, SW/LX bölgesinden uzak.
- [ ] #5 OUT_POS/GND için J4'e 3 A güç bakırı ve termal alan ayrılmış; genişlik/katman/bakır kalınlığı varsayımlarıyla ΔT ≤10 °C proje hedefi değerlendirilmiş. Nihai polygon ve akım/ısı doğrulaması routing/fabrikasyon devrine yazılmış.
- [ ] #6 AOZ1284 ve TPS55340 güç grupları B.Cu'da U2/anten bölgesinden ayrı; bobinler ve SW/LX alanları U2/anten altında değil. U2/anten ile en yakın bobin/SW sınırı mesafeleri ölçülü ve yön seçimi gerekçeli; üretici şartı olmayan evrensel bir mm limiti uydurulmamış.
- [ ] #7 U2 bypass/bulk kapasiteleri MCU dibinde; buck uzaklığına rağmen 3,3 V besleme ve GND dönüşü için yeterli bakır/via koridoru mevcut. Cin–anahtarlama–GND güç döngüleri ve FB/COMP/sense sessiz yolları korunmuş.
- [ ] #8 Blok giriş/çıkış yönleri birbirine bakıyor; USB, CC, Kelvin, I2C/UART, güç ve GND dönüş koridorları açıklamalı görünümde. Kritik hatlar için güzergâh denemesi yapılmış; ratsnest azalması kritik döngü veya dönüş yolunu bozarak sağlanmamış.
- [ ] #9 Ethernet altına yalnız TASK-080 yükseklik/keepout haritasına uyan düşük profilli, az ısınan parçalar konmuş; seçilen ref/yükseklik/boşluk listesi ve gerekirse modül dışındaki alternatif alan gösterilmiş.
- [ ] #10 J3/FPC, H1-H4, TASK-063/083 son J9 kablo alanı, test noktaları ve BOOT/RESET erişimi korunmuş; bobin/MOSFET/şönt/güç dirençleri için ısıl bakır ve montaj alanı mevcut.
- [ ] #11 Son top/bottom ve 3D inceleme tamam; grup üyeliği/net/polarite korunmuş, schematic parity 0, yeni açıklanmamış geometrik/elektriksel ihlal yok. 3D kanıtlı J8 courtyard istisnaları ayrı kayıtlı; kısa devre veya eksik bağlantı gizlenmemiş. Mevcut ihlaller ve bağlantısız öğeler ayrı; D5–U11 FB kesintisiz ve ≤10 mm.
- [ ] #12 Yerleşim/routing için 3,3 V yük akımı ve buck–U2 DC düşüm bütçesi, U2 min/max besleme ve transient/ripple hedefi; giriş/çıkış yük/ortam matrisi ve bileşen sıcaklık sınırları sayısal olarak kaynak/marj ayrımıyla kaydedilmiş. Katman/via/bakır boyutlandırması bu bütçeye bağlı; sonuç besleme/termal prototip görevine aktarılmış.
- [ ] #13 USB/CC, Kelvin, kritik güç/GND döngüleri ve MCU beslemesi için güzergâh denemesi başarıyla tamamlanmış; hangi katmanda hangi referans düzleme dönüldüğü, özellikle bottom–In2 güç adaları çevresindeki dönüş sürekliliği gösterilmiş. Genel routing görevine denenmiş koridorlar devredilmiş.
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

25.09.2026 — Yeni kullanıcı isteğinin iş sırası: TASK-091 Ethernet/USB-C mekanik revizyonu → TASK-092 kalan komponentlerin fiziksel yerleşimi → TASK-008 kritik elektriksel yerleşim/güzergâh kabulü → TASK-087 routing. TASK-063 geçmiş başlangıç kanıtıdır; güncel port ankrajları TASK-091 çıktısından alınır. Bu kayıt yalnız iş planı güncellemesidir.

25.09.2026 — Güncel yerleşim sırası TASK-091 → TASK-093 (Ethernet altı aktif komponent yerleşimi) → TASK-092 → TASK-008 → TASK-087. Alt hacimde seçilen reflerin güç/GND dönüşü, hassas sinyal ve termal kabulleri bu görevde nihai güzergâhlarla yeniden kontrol edilir; üretim numune kabulü TASK-053/088 dedir.
<!-- SECTION:NOTES:END -->
