# ERC düzeltmeleri — 11 Eylül 2026

Sonuç: **5 hata / 331 uyarı → 0 hata / 1 uyarı**.

## Uygulanan düzeltmeler

- 323 grid uyarısı: sembol, tel, etiket ve bağlantı noktaları 50 mil bağlantı gridine birlikte taşındı. ERC ayarındaki kontrol kapatılmadı.
- 6 açık tel ucu: UART_TX, UART_RX, RTC_SDA ve PD_GATE üzerindeki etiket sonrasına taşan gereksiz tel uzantıları kısaltıldı. Pin ile etiket arasındaki bağlantılar korundu.
- Encoder kütüphane farkı: projede kullanılan SW3 sembolü proje kütüphanesine eşitlendi. Pin numarası/işlevi değişmedi: 1 A, 2 C, 3 B, 4 S1, 5 S2. Bu işlem mekanik footprint doğrulaması anlamına gelmez.
- Beş power_pin_not_driven hatası: mevcut devrede besleme kaynağı izlenebilen aşağıdaki noktalara standart PWR_FLAG eklendi.

| Bayrak | Net | Mevcut besleme yolu |
|---|---|---|
| #FLG01 | PD_VBUS_SENSED | USB VBUS → giriş şöntü R11 → VCC |
| #FLG02 | PD_VOUT | Giriş → Q4/Q3 anahtarları → PD_VOUT |
| #FLG03 | GND | USB girişinin ortak besleme dönüşü |
| #FLG04 | +3.3V | AOZ1284PI → L1 → çıkış kapasitörleri |
| #FLG05 | RTC VBACKUP | CR2032 → R22 → RTC yedek beslemesi |

PWR_FLAG yeni bir gerilim kaynağı oluşturmaz; mevcut besleme yolunu ERC'ye tanıtır. Anahtarların her zaman açık olduğu veya regülatörün çalışmasının ölçülerek doğrulandığı anlamına gelmez.

## Doğrulama

Önceki ve sonraki netlistlerdeki **94 pin bağlantı grubunun tamamı aynı**. Grid düzenlemesi ve tel kısaltmaları hiçbir elemanın hangi pine bağlı olduğunu değiştirmedi. Şematik görünümleri kontrol edildi. Değerler, footprint seçimleri ve iki banana jack kararı korundu.

- [Son ERC raporu](<C:/Users/Slayer/Desktop/masaüstü güç kaynağı/reports/erc-fix-20260911/after.rpt>)
- [Netlist eşdeğerlik kaydı](<C:/Users/Slayer/Desktop/masaüstü güç kaynağı/reports/erc-fix-20260911/net-equivalence.json>)
- [Değişiklik öncesi yedekler](<C:/Users/Slayer/Desktop/masaüstü güç kaynağı/reports/erc-fix-20260911/before>)

## Kalan tek uyarı

**BACKLIGHT_3V0 — isolated_pin_label:** J3 pin 38 arka ışık anodu henüz bir besleme/sürücü devresine bağlı değil. Bu gerçek tasarım eksikliği etiket değiştirilerek, test noktası veya PWR_FLAG eklenerek gizlenmedi. Uyarının elektriksel olarak çözülmesi için ekranın akım ve ileri gerilim gereksinimlerini karşılayan arka ışık sürücüsü tamamlanmalı.

Önceki PDF paketindeki ERC sayıları önceki şematik sürümüne aittir; bu kayıt güncel sonucu verir. Sıfır ERC hatası, boş PCB'nin fiziksel yerleşim/ısıl/RF kontrolünün tamamlandığı veya açık tasarım konularının çözüldüğü anlamına gelmez.
