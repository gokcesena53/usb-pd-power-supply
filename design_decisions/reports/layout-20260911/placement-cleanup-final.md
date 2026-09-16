# PCB Yerleşim ve Silkscreen Temizliği

Tarih: 2026-09-12

## Yapılan değişiklikler

- J3/TFT konnektörünün fiziksel alanına giren boost ve backlight parçaları konnektörün üstüne taşındı.
- `L2`, `U7`, `C20`, `C21`, `C22`, `R44`, `R45` ve ilgili kontrol parçaları işlevsel bir küme halinde yeniden yerleştirildi.
- `U8` 90 derece döndürülerek backlight kanalları TFT konnektörü yönüne çevrildi.
- `TP6`–`TP10` test noktaları konnektör ve buton gövdelerinin dışında düzenlendi.
- Küçük 0402 parçaların okunamayacak ve padlerin üstüne taşan referans yazıları F.SilkS katmanından gizlendi. Referanslar PCB verisinde ve F.Fab/assembly çıktısında korunuyor.
- SW3 encoder silkscreen gövde çizgisi üst padlerin üzerinden geçmeyecek şekilde açıldı; aynı değişiklik proje footprint kütüphanesine işlendi.
- J3 Molex footprint’ine pad ve gövde sınırlarını kapsayan `F.CrtYd` eklendi. Aynı courtyard hem karttaki footprint’e hem proje kütüphanesine yazıldı.

## Doğrulama

- KiCad DRC: **0 ihlal**.
- Courtyard kontrolü: **0 footprint çakışması**, 0.2 mm ek yerleşim payıyla.
- Kalan `266 unconnected items`, kart henüz route edilmediği için beklenen bağlantı sayısıdır.
- J1 USB-C, J2 UART ve U2 ESP32 anten modülü kart kenarında mekanik amaçla konumlandığından courtyard sınırları kart dışına çok az taşmaktadır; bunlar birbirleriyle çakışmıyor.

## Sonraki adım

Yerleşim çakışmaları temizlendi. Routing sırası: GND/via planı, 5 A ana güç yolu, AOZ1284PI buck güç döngüsü, 3.3 V dağıtımı, USB diferansiyel hatları ve son olarak düşük hızlı sinyaller.
