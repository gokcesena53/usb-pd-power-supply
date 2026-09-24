---
id: TASK-085
title: Grup ici yerlesimleri topluca dogrula ve kart yerlesimine devret
status: To Do
assignee: []
created_date: '2026-09-24 07:39'
updated_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-070
  - TASK-071
  - TASK-072
  - TASK-073
  - TASK-074
  - TASK-075
  - TASK-076
  - TASK-077
  - TASK-078
  - TASK-079
  - TASK-080
  - TASK-081
  - TASK-082
  - TASK-083
  - TASK-084
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 167000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
15 grup içi yerleşimin kaynak kurallarına uygunluğunu ve birbirine bağlanabilirliğini birlikte incele. Grupların kart dışındaki göreli yerleşimleri bu aşamada kabul edilebilir; nihai mekanik ankrajlar TASK-063, genel kart yerleşimi TASK-008 ile tamamlanır. TASK-065 yükseklik kısıtları geçerli; eski USB-C/ESP32 bottom yüzleri güncel karar ile değiştirilmiştir. Her grubun zarfını, tercih edilen yüzünü, yönünü, ankrajını ve giriş/çıkış taraflarını devir tablosuna yaz. Nihai yüz/konum değişikliğinden sonra tekrar yapılacak kontrolleri TASK-008'e aktar. Bu görev genel routing veya üretime hazır DRC onayı değildir.

Güncel devir: J7/U2 top, J8 bottom; U2 anteni dışarı ve USB-C'ye RF koşullu yakın. J9 son koordinatı TASK-063/083'te seçilir. Buck/boost B.Cu'da MCU'dan uzak; LM74801/şönt/INA226 J4 yönünde. TASK-080 modül altı hacim haritası ve TASK-083 slot/kablo kararı TASK-008 girdisidir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 15 grubun her biri kaynak kuralı–uygulanan ref/pin–kanıt eşleşmesiyle kontrol edilmiş; eksik veya üyeliği yanlış footprint yok, J3/J9/H1-H4 ankraj istisnaları açık.
- [ ] #2 USB-C/PD, boost/buck ortak V_X, çıkış anahtarı/INA226/J4, TFT/backlight ve MCU çevresi grup sınırları birlikte değerlendirilmiş; karşı karşıya gelmesi gereken bağlantı yönleri ve iz koridorları uyumlu.
- [ ] #3 Her grubun x/y zarfı, parça yüksekliği/yüz kısıtı, ankrajı, kritik döngü ve hassas bağlantıları devir tablosunda; TASK-065 sonrası flip/taşımanın gerektirdiği yeniden kontrol listesi hazırlanmış.
- [ ] #4 Tüm gruplar için top/bottom yakın plan ve genel görünüm alınmış; yeni açıklanmamış courtyard/clearance/short ihlali yok, schematic parity 0. TASK-080'in 3D kanıtlı mezanin courtyard istisnaları ayrı listelenmiş; bağlantısız öğeler ve mevcut ihlaller kayıtlı.
- [ ] #5 D5–U11 FB izi kesintisiz ve ≤10 mm; J3 kilidi/FPC alanı ve J9 kablo alanı korunmuş. TASK-008'e nihai kart konumu/yüzü sonrası kritik bağlantı, anten ve mekanik kontrol girdileri aktarılmış.
- [ ] #6 Devir tablosu son hedef yüzleri ve mekanik önce/güç sonra sırasını içeriyor; USB-C/MCU flip sonrası ESD, dekuplaj, USB yönü, anten ve LCD kontrolleri açık. J9 tarihsel koordinatı değişmez ankraj sayılmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — TASK-065 devri: nihai konumlandırma sonrası model yükseklik
ve LCD izdüşüm denetimini tekrarla. LCD toleranslı zarfı
x=63,52…141,62; y=72,28…127,72 mm; top J3 dışı toplam zarf≤1,80 mm.
C33/J8 bottom gövdeleri güvenli olsa da top pin çıkıntıları modelde
1,9/4,4 mm: pinleri LCD dışında tut veya montajda metal+lehim≤1,5 mm şartını
uygula. Buck/boost B.Cu, backlight/J3 F.Cu ve D5–U11 FB sürekliliği korunmalı.
Karar: `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
TASK-065'in sıfır LCD çakışması kart dışındaki geçici yerleşime aittir.

TASK-072/073 devri: D4–C27 yakın V_PRE yolu ve U5–D2/L1 buck döngüsü
B.Cu'da göreli yerleştirildi. C28 (82,00;64,00) boost'un ikinci V_PRE
deposu olarak buck girişine bakıyor; C28–R43.1 5,41 mm, C28–C13.1
8,38 mm pad mesafesi. Son kart konumu/routing sırasında V_PRE ve GND
bakır genişliği, termal via alanı, ortak EN_CTRL/V_X sessiz koridoru ve
D5–U11 BOOST_FB 2,584607 mm sürekliliğini birlikte denetle.
`design_decisions/output/AOZ1284_YERLESIM_TASK073_20260924.md`.

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
