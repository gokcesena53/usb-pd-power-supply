# TASK-042 — PCM_Espressif temizliği

24.09.2026. U2, aktif şemada ve PCB'de `RF_Module:ESP32-C6-MINI-1`
kullanıyor; eski WROOM kütüphanesine ihtiyaç kalmadı.

Kaldırılan dosyalar:

- `hardware/libraries/PCM_Espressif.kicad_sym`
- `hardware/libraries/PCM_Espressif.pretty/ESP32-C6-WROOM-1.kicad_mod`

`hardware/sym-lib-table` ve `hardware/fp-lib-table` içindeki PCM_Espressif
kayıtları da kaldırıldı. Güncel şema, PCB, proje, lib-table ve yerel
sembol/footprint dosyalarından oluşan 25 dosyada referans sayısı sıfırdır.
Tarihsel rapor ve yedeklerdeki eski devre kayıtları arşiv niteliğindedir.

| Kontrol | Önce | Sonra |
| --- | --- | --- |
| ERC hata / uyarı | 0 / 0 | 0 / 0 |
| DRC schematic parity | 0 | 0 |
| DRC yerleşim/üretim ihlali | 148 | 148 |
| Bağlantısız öğe | 361 | 361 |
| Net sayısı | 120 | 120 |

Netlist, tüm netlerin pin kümeleri üzerinden birebir karşılaştırıldı.
Beş şema dosyası, PCB ve proje dosyasının SHA-256 değerleri de değişmedi.
Görsel tasarım dosyalarına dokunulmadığından bu temizlik için yeni render
üretilmedi.

148 DRC ihlalinin içerikleri aynı kaldı; bağlantısız öğelerin net başına
sayıları da değişmedi. Aynı konumdaki veya aynı pad numarasını paylaşan
pedlerde KiCad ratsnest uç çifti seçimi çalıştırmalar arasında değişebilir;
raporlardaki bu fark PCB bağlantısının değiştiği anlamına gelmez. Kütüphane
temizliği açısından ERC/DRC kontrolü geçti; genel yerleşim/routing DRC'si
henüz sıfır değildir.

Kanıtlar: `before-summary.json`, `after-summary.json`, `before-erc.rpt`,
`after-erc.rpt`, `before-drc.json`, `after-drc.json`.

Boş `PCM_Espressif.pretty` klasörünün silinmesi otomatik onay denetimi
tarafından yalnız “blocked by policy” gerekçesiyle engellendi. Klasör boş
bırakıldı; içinde footprint yoktur ve kütüphane tablolarında kaydı yoktur.
Git boş klasörleri takip etmez.
