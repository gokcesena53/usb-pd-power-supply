# Kullanıcı çıkışı: J4 klemens → kablo lehim pedi, Motorobit 4 mm banana (23 Eylül 2026)

Görev: TASK-044. Maksimum çıkış 3 A, 28 V
(`CIKIS_AKIMI_3A_KARARI_20260922.md`).

## Değişiklik

- **J4**: DEGSON DG142R-5.08-02P-14-00AH (2 poz. açılı klemens) kalktı.
  Yerine 2 pozisyonlu kablo lehim pedi: sembol
  `Connector_Generic:Conn_01x02`, footprint
  `Connector_Wire:SolderWire-1.5sqmm_1x02_P7.8mm_D1.7mm_OD3.9mm`
  (delik 1.7 mm, halka Ø3.9 mm, aralık 7.8 mm). Pin 1 = OUT_POS,
  pin 2 = GND; referans ve pin netleri korundu, netlist değişmedi.
- **J5** (OUT_POS): Cinch 108-0902-001 → Motorobit 4 mm metal dişi banana,
  kırmızı, `KOM.KNN.06.000021`.
- **J6** (GND): Cinch 108-0903-001 → Motorobit 4 mm metal dişi banana,
  siyah, `KOM.KNN.06.000022`.
- J5/J6 PCB'de değil; panele mekanik olarak sabitlenir, kabloları J4
  pedlerine lehimlenir.

## Boyutlandırma

- Kablo: 1.5 mm² (AWG16) silikon. 1.5 mm² kablo 3 A'yi rahat taşır;
  footprint bu kesit için tasarlanmış (1.7 mm delik), 5 A'e kadar da yeterli.
- Pedler THT; OUT_POS ve GND bakırı pedlere polygon ile bağlanmalı
  (yol genişliği/ΔT kontrolü yerleşimde, TASK-008).

## Açık kalan

Motorobit ürün sayfaları akım/gerilim anma değeri, panel deliği ve
gövde ölçüsü vermiyor (23.09.2026 kontrol edildi; yalnız stok kodu ve
"stokta 100+"). J5/J6 footprint'i şimdilik Cinch double-D panel kesimi
olarak kaldı. Numune alınıp ölçülecek: TASK-046.
