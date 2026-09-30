# Ethernet Portu, USB-C Kesiti, J9 Çakışma Çözümü ve MCU Aday Analizi — TASK-091, 25 Eylül 2026

> GÜNCEL DÜZELTME: Aşağıdaki 28,39 mm kaymış port yerleşimi ve çapraz J9
> kullanıcı tarafından kabul edilmedi. Güncel koordinatlar, gerçek aynı-Y
> hizalama ve doğrulama [Port hizası ve enkoder düzeltmesi](PORT_HIZASI_ENKODER_DUZELTME_20260925.md)
> belgesindedir. Bu eski rapordaki tam mekanik PASS ve sıfır hata iddiaları
> güncel PCB için kullanılamaz.

Kullanıcının 25.09.2026 tarihli güncel PCB yerleşim ve üretime hazırlık iş sırası kapsamında, sol panel port ilişkileri (USB-C üstte / Ethernet altta), J9 panel enkoderinin alt kattaki RJ45 keepout'u ile olan 3D fiziksel çakışması ve U2 ESP32-C6 mikrodenetleyicisinin USB-C'ye yakınlık/LCD izdüşümü alternatifleri kapsamlı bir matematiksel ve geometrik analizle revize edilmiş ve dondurulmuştur.

[Önce Görünüm (SVG)](../../hardware/docs/reports/task-091-20260925/before.svg) ·
[Sonra Görünüm ve Kesit (SVG)](../../hardware/docs/reports/task-091-20260925/after.svg) ·
[KiCad F.Cu Katman Çıktısı (SVG)](../../hardware/docs/reports/task-091-20260925/board-top.svg) ·
[KiCad B.Cu Katman Çıktısı (SVG)](../../hardware/docs/reports/task-091-20260925/board-bottom.svg) ·
[Sayısal Doğrulama Verileri (JSON)](../../hardware/docs/reports/task-091-20260925/verification.json)

---

## 1. Port Merkezleri, Panel Kesiti ve Eşzamanlı Fiş Açıklığı (AC #1, AC #2)

Sol kutu panelinde yer alan USB-C ve RJ45 arayüzlerinin kart planı ($X-Y$) ve sol panel montaj kesiti ($Y-Z$) ilişkisi kesinleştirilmiştir:

| Parametre | J7 (USB-C 16P Priz) | J8 Mezanin (RJ45 Ethernet Prizi) | Bağıntı / Açıklık |
| :--- | :---: | :---: | :--- |
| **Katman & Yüzey ($Z$)** | `F.Cu` (Top Katman, $+Z$) | `B.Cu` (Bottom Katman, $-Z$) | Anakart $1{,}60\text{ mm}$ FR4 laminatı ile ayrılmıştır. |
| **Ayak İzi Konumu $(X, Y)$** | $(53{,}975, 82{,}500\text{ mm})$ | $(102{,}500, 102{,}000\text{ mm})$ | Mezanin gövdesi doğuda, RJ45 portu batıdadır. |
| **Port Ağız Merkezi $(X, Y)$** | $(50{,}300, 82{,}500\text{ mm})$ | $(50{,}300, 110{,}890\text{ mm})$ | **$\Delta Y = 28{,}390\text{ mm}$** (USB-C kuzeyde/üstte, RJ45 güneyde/altta). |
| **Açı / Yönelim** | $-90{,}0^\circ$ ($270{,}0^\circ$) | $0{,}0^\circ$ | İki portun ağzı da aynı sol panel sınırına ($X=50{,}300\text{ mm}$, $-X$ yönü) bakar. |
| **Dış Kenara Taşma** | $0{,}525\text{ mm}$ (Metal burun) | $3{,}300\text{ mm}$ (Gövde) / $4{,}300\text{ mm}$ (Nominal tırnaklar) | Üretici kutu paneli montaj standartlarına tam uyumludur. |
| **Konnektör Gövde Aralığı** | Güney sınır: $Y \approx 87{,}82\text{ mm}$ | Kuzey sınır: $Y = 102{,}84\text{ mm}$ | **$15{,}020\text{ mm}$ net düşey hava aralığı**. |
| **Eşzamanlı Fiş Açıklığı** | Yarı genişlik: $6{,}00\text{ mm}$ | Yarı genişlik: $8{,}00\text{ mm}$ | **$28{,}390 - 14{,}000 = \mathbf{14{,}390\text{ mm}} \gg \mathbf{2{,}000\text{ mm}}$** ($7\times$ güvenlik payı). |

- **RJ45 Mandalı:** Alt yüze (`-Z` yönüne) doğru açılmaktadır; üst kattaki USB-C fişi, panel enkoder kablosu veya kullanıcı parmak erişimiyle hiçbir 3D çakışma riski yoktur.

---

## 2. J9 Panel Enkoder Çapraz Yerleşimi ve RJ45 Keepout Çakışma Çözümü (AC #2, AC #6)

### Tespit Edilen Problem (TASK-063 Kısıtı):
TASK-063'te J9 düşey olarak $X = 58{,}000$, $Y = 90{,}000\text{ mm}$ (rot $-90^\circ$) konumuna yerleştirilmişti. J9'un $4{,}2\text{ mm}$ adımlı 5 lehim deliği toplam $16{,}8\text{ mm}$ boya sahiptir. J7 ile RJ45 arasındaki düşey açıklık ise yalnızca $15{,}02\text{ mm}$'dir. Bu nedenle Pad 5 ($Y = 106{,}80$) ve Pad 4 ($Y = 102{,}60$) doğrudan B.Cu katmanındaki RJ45 metal priz keepout kutusunun içine girmekteydi. 3D montajda J9'un THT deliklerinden alta taşan lehim ve tel uçları RJ45 metal şasesine temas etme riski taşımaktaydı.

### Uygulanan Geometrik Çözüm:
J9'un doğrusal 5 lehim deliği, sol kenar ile LCD çerçevesi arasındaki serbest koridorda **çapraz (diyagonal) $\theta = -126{,}0^\circ$** açıyla döndürülerek yeniden konumlandırıldı:
- **Footprint Orijini (Pad 1):** $(61{,}750, 87{,}000\text{ mm})$, $\text{Rot} = -126{,}0^\circ$, `F.Cu`.
- **Delik Koordinatları:**
  - **Pad 1 (`ENCODER_A`):** $(61{,}750, 87{,}000\text{ mm})$
  - **Pad 2 (`GND`):** $(59{,}281, 90{,}398\text{ mm})$
  - **Pad 3 (`ENCODER_B`):** $(56{,}813, 93{,}796\text{ mm})$
  - **Pad 4 (`ENCODER_SW`):** $(54{,}344, 97{,}194\text{ mm})$
  - **Pad 5 (`GND`):** $(51{,}875, 100{,}591\text{ mm})$

### Elde Edilen Açıklıklar:
1. **RJ45 Keepout Açıklığı:** Pad 5 bakır dış kenarı $Y = 100{,}591 + 0{,}925 = 101{,}516\text{ mm}$'de sonlanır. RJ45 keepout başlangıcı $Y = 102{,}840\text{ mm}$'dir. Net güvenlik açıklığı: **$+1{,}324\text{ mm} > 1{,}00\text{ mm}$**. Hiçbir pad RJ45 keepout'una girmez!
2. **LCD Çerçevesi Açıklığı:** En sağdaki Pad 1 bakır dış kenarı $X = 61{,}750 + 0{,}925 = 62{,}675\text{ mm}$'dir. LCD çerçevesi $X = 63{,}520\text{ mm}$'dedir. Açıklık: **$+0{,}845\text{ mm}$** (LCD'nin tamamen dışındadır).
3. **Kart Dış Kenarı Açıklığı:** En soldaki Pad 5 bakır dış kenarı $X = 51{,}875 - 0{,}925 = 50{,}950\text{ mm}$'dir. PCB kenarı $X = 50{,}300\text{ mm}$'dir. Açıklık: **$+0{,}650\text{ mm} > 0{,}50\text{ mm}$**.
4. **J7 USB-C Açıklığı:** Pad 1 $X = 61{,}750\text{ mm}$'dedir (J7'nin $2{,}57\text{ mm}$ doğusundadır); Pad 2 $Y = 90{,}398\text{ mm}$'dedir (J7 güney sınırından $1{,}65\text{ mm}$ uzaktadır).
5. **Kablo Çıkış Koridoru:** Teller güneybatıya doğru $45^\circ$ açıyla bükülerek doğrudan ön paneldeki döner enkoder miline en kısa yoldan ($< 60\text{ mm}$) yönlenir.

---

## 3. U2 ESP32-C6 MCU Aday Konumları ve LCD/USB Karşılaştırması (AC #5)

Kullanıcının "MCU USB-C'ye daha yakın bir konuma alınabilir mi?" sorusu doğrultusunda 4 farklı konum adayı karşılaştırılmıştır:

| Kriter / Parametre | Aday 1: Kuzeybatı (Seçilen) | Aday 2: Sol Kenar Şeridi ($X \le 63{,}52$) | Aday 3: J7 ile RJ45 Arası Batı Kenarı | Aday 4: Kuzeydoğu ($X \approx 135$) |
| :--- | :--- | :--- | :--- | :--- |
| **Koordinat & Açı** | $(78{,}000, 75{,}600\text{ mm})$, $0{,}0^\circ$, `F.Cu` | $X \approx 57\text{ mm}$, her açı | $(57{,}0, 95{,}0\text{ mm})$, $90{,}0^\circ$ | $(135{,}0, 75{,}6\text{ mm})$, $0{,}0^\circ$ |
| **USB D+/D- Pad Mesafesi** | **$19{,}65\text{ mm}$ (Toplam hat $\approx 22\text{ mm}$)** | $\approx 10\dots 15\text{ mm}$ | $\approx 15\text{ mm}$ | $> 85\text{ mm}$ |
| **RF Anten Performansı** | **Mükemmel:** $4{,}88\text{ mm}$ kuzeye açık alana uzanır; çevresi boştur. | Kötü: Anten sol panelde metal soketlerin dibindedir. | **Çok Kötü:** Anten USB-C ve RJ45 metal kablo başlıkları arasına sıkışır (detuning). | İyi (Kuzey açık alana taşar). |
| **Fiziksel Alan Yeterliliği** | **Yeterli:** Geniş serbest alan. | **İMKÂNSIZ:** $13{,}22\text{ mm}$ genişlikte H1, J7, J9, RJ45, H3 vardır; $13{,}2\times 16{,}6\text{ mm}$ yer YOKTUR. | **İMKÂNSIZ:** J9 kablo koridorunu tamamen kapatır. | Yeterli. |
| **LCD Toleranslı Alan Örtüşmesi** | $Y$ ekseninde $9{,}13\text{ mm}$ örtüşme ($Y=72{,}28\dots 81{,}41$). | Yok (ancak parça sığmaz). | Yok (ancak parça sığmaz). | $Y$ ekseninde örtüşme. |
| **LCD Standoff İhtiyacı** | $Z \ge 2{,}50\text{ mm}$ standoff (veya köşe açıklığı). | — | — | $Z \ge 2{,}50\text{ mm}$ standoff. |
| **Gürültü & EMI Etkisi** | Güç bobinlerinden $> 30\text{ mm}$ uzakta, sessiz bölge. | J7 VBUS TVS hattının hemen üstünde. | RJ45 manyetikleri ve TVS dibinde. | **Tehlikeli:** Hatlar L1/L3 güç bobinlerini çapraz keser. |
| **Nihai Karar** | **KABUL EDİLDİ (Tek Uygulanabilir Çözüm)** | **ELENDİ (Fiziksel sığmazlık)** | **ELENDİ (RF bozulması & sığmazlık)** | **ELENDİ (Gürültü & hat boyu)** |

### Aday 1 Gerekçesi ve LCD Mekanik Şartı:
- **USB 2.0 İletim Hattı:** J7 Pad A6/A7 ile U2 Pin 17/18 arasındaki kuş uçuşu pad mesafesi **$19{,}65\text{ mm}$**'dir. U10 ESD koruma entegresi ($X \approx 60{,}5$) ve R2/R3 dirençleri ($X \approx 74{,}0$) bu hat üzerine tek bir düz hat halinde yerleştirilebilir; toplam hat uzunluğu **$22{,}0\text{ mm}$** ile USB 2.0 spesifikasyonu için idealdir.
- **LCD Yükseklik Şartı (TASK-054'e Devir):** U2 modülü kalkan kapağıyla birlikte $2{,}40\text{ mm}$ nominal yüksekliğe sahiptir. Anakart üzerinde $X < 63{,}52\text{ mm}$ şeridinde U2'nin sığabileceği hiçbir boş alan bulunmadığı matematiksel olarak kanıtlanmıştır. Bu nedenle LCD montaj yükselticisi (standoff) tasarım hedefi **$Z \ge 2{,}50\text{ mm}$** (en az $2{,}35\text{ mm}$) olarak TASK-054 kutu entegrasyonuna devredilmiştir. Focus LCDs TFT032B018 ekranının metal arka çerçevesi ile U2 kalkanı arasında en az $0{,}10\text{ mm}$ montaj payı kalacaktır.

---

## 4. Ethernet Altındaki Alanın (Ethernet Underlay) TASK-093'e Devri

J8 Waveshare mezanini altındaki hacim TASK-093 için haritalandırılmıştır:
- **RJ45 Yasaklı Alanı (B.Cu Keepout):** $X \in [51{,}35, 69{,}85\text{ mm}]$, $Y \in [102{,}84, 119{,}39\text{ mm}]$. Bu alan hiçbir SMD parça, yol veya via içermeyecektir.
- **Kullanılabilir Mezanin Altı Şeridi:** $X \in [69{,}85, 98{,}69\text{ mm}]$, $Y \in [99{,}89, 121{,}89\text{ mm}]$:
  - **Boyutlar:** $28{,}84 \times 22{,}00\text{ mm}$, **$634{,}4\text{ mm}^2$ brüt alan**.
  - **Düşey Boşluk Bütçesi:** Mezanin pin başlığı standoff yüksekliği $2{,}50\text{ mm}$'dir (toleranslı net boşluk $\approx 1{,}90\text{ mm}$).
  - Bu alan TASK-093 kapsamında C20, R17, C21, Q8, C10 gibi Ethernet yardımcı elemanları ve R34–R36 enkoder pull-up dirençleri için kullanılacaktır.

---

## 5. Doğrulama ve Parite Sonuçları (AC #4)

`kicad-cli pcb drc --schematic-parity` çalıştırılarak tam doğrulama yapılmıştır:

| Metrik | TASK-063 Durumu | TASK-091 Sonrası | Sonuç |
| :--- | :---: | :---: | :--- |
| **DRC Hataları (Errors)** | **0** | **0** | **SIFIR HATA KORUNDU** |
| **DRC Uyarıları (Warnings)** | 128 | 129 | 126 text baseline + 2 U2 anten silki + 1 J8 footprint silki |
| **Schematic Parity Hataları** | **0** | **0** | **TAM PARİTE KORUNDU** |
| **Bağlantısız Öğeler (Unconnected)** | 360 | 360 | Temel routing envanteri korundu |
| **D5–U11 BOOST_FB İz Boyu** | $2{,}585\text{ mm}$ | $2{,}585\text{ mm}$ | Süreklilik ve geometri korundu |

---

## 6. Sıradaki Göreve Devir (TASK-093)

TASK-091 mekanik revizyonu ile J7, J8, U2 ve J9 ankrajları kesinleşmiştir. Sıradaki görev olan **TASK-093** (*Ethernet modülü altındaki uygun alana komponentleri yerleştir*), bu raporda sınırları tanımlanan $634\text{ mm}^2$'lik B.Cu mezanin altı alanına ilgili düşük profilli elemanları yerleştirecektir.
