# AOZ1284PI uygulama sonucu

Yalnız powergeneration.kicad_sch değiştirildi; diğer şemaların SHA-256 değerleri korundu. Hesaplar [calculations.md](calculations.md), şema görüntüsü [powergeneration.svg](svg/powergeneration.svg), ERC [erc.rpt](erc.rpt).

| AOZ1284PI pin | Bileşen / bağlantı | Net |
|---|---|---|
| EP / KiCad 9 VIN | C12/C13 10 µF + C14 100 nF üst uçları | PD_VOUT |
| 1 LX | L1 22 µH giriş; D2 katot; C17 ikinci uç | LX_SW (yerel) |
| 1 LX | L1 çıkışı → C15/C16 üst uçları | +3.3V |
| 2 BST | C17 100 nF → pin 1 | BST–LX_SW |
| 3 GND | Diyot anot ve kondansatör/direnç dönüşleri | GND |
| 4 FSW | R38 100 kΩ → GND | FSW_SET (yerel) |
| 5 COMP | R41 UNRESOLVED → C19 UNRESOLVED → GND | COMP_NODE (yerel) |
| 6 FB | R39 10 kΩ üst → +3.3V; R40 3.20 kΩ alt → GND | FB_3V3 (yerel) |
| 7 SS | C18 10 nF → GND | SS_RAMP (yerel) |
| 8 EN | R42 100 kΩ → GND; bağımsız 1.2–5 V kaynak gerekli | EN_CTRL (yerel, kaynak UNRESOLVED) |

11 net grubu otomatik doğrulandı. Merkez pad 9 GND ağına bağlı değil; PD_VOUT üzerinde. Bootstrap iki ucu BST ve LX'te; diyot katodu LX'te. Yeni eleman numaraları L1, D2, C12–C19, R38–R42.

Proje ERC: 15 hata, 277 uyarı (292 kayıt). POWER GENERATION altında bir hata var: U5 VIN için power_pin_not_driven. PD_VOUT'un upstream güç kaynağı ERC açısından sürücü olarak tanınmıyor. Bu sayfada pin kopukluğu kalmadı. Upstream sayfa/PWR_FLAG değiştirilmedi. ERC'nin başarılı elektriksel bağları görmesi, COMP değerlerini veya EN kaynak yeterliliğini doğrulamaz.

Çalıştırmadan önce çözülmesi gerekenler: EN bias kaynağı, COMP R/C değerleri ve gerçek Cout/ESR, frekans denklemi/tablo farkı, L/D MPN ve footprint'leri, bobinin hata akımı dayanımı, termal doğrulama ve üretim land-pattern onayı. Hesap raporunda her biri ayrıldı. Mevcut EN pulldown nedeniyle devre kapalı kalır; bu şema tamamlanmış çalışan güç kaynağı olarak sunulmaz.
