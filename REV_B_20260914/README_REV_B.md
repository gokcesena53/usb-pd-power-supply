# REV_B PCB çalışma alanı

Bu klasör, mevcut üretim kartından bağımsız yeni PCB yerleşim çalışmasıdır.

## Hazır taban

- Geometrik dış ölçü: **60,00 × 40,00 mm**
- Bakır katman sayısı: **4**
- Köşe bağlantısı: kapalı montaj deliği yoktur.
- Dört köşe, M3 vida gövdesi için **3,40 mm çap eşdeğerinde (R = 1,70 mm) kenara açık çeyrek daire** olarak yontulmuştur.
- Edge.Cuts çizgi genişliği: **0,05 mm**
- Footprint: **0**
- Track: **0**
- Via: **0**
- Copper zone: **0**
- Taban DRC: **0 ihlal / 0 bağlantısız öğe**

Şematik komponentleri bilerek henüz PCB'ye aktarılmadı. Sonraki işlem, KiCad'de **Tools → Update PCB from Schematic (F8)** adımını kullanıcıyla birlikte yürütmektir.

## Enkoder revizyonu

- SW3: **L-KLS4-EC1121S-E5A-F12.5**
- A → ENCODER_A, C → GND, B → ENCODER_B
- D → ENCODER_SW, E → GND
- Projeye özel footprint: `L-KLS4-EC1121S-E5A-F12.5.pretty`
- Elektrik pin delikleri: 5 × Ø1,00 mm
- Elektrik pin sıraları arası: 14,50 mm
- Mekanik slotlar: 2,10 × 1,50 mm, merkezler arası 11,50 mm
- Datasheet: `datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf`
- Revizyon sonrası ERC: **0 ihlal**

Ana `masaüstü güç kaynağı.kicad_pcb` dosyası değiştirilmemiştir. REV_A arşivi `revisions/archive/REV_A_PRODUCTION_20260914` altındadır.
