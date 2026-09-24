# Çıkış deşarjı grubu ilişkisel yerleşimi — TASK-076, 24 Eylül 2026

Aktif çıkış deşarjı grubunun (`CIKIS DESARJI (R59 yerine aktif)`) 5 footprint üyesi (Q4, Q6, D10, R66, R67), güncel şemadaki Q4/Q6 sürme, D10 clamp, R67 güç ve akım yolu ile U13 SW_EN kontrol mantığına göre ilişkisel olarak yerleştirildi. Beş footprint'in grup üyeliği, UUID, pad/net bağlantıları ve TASK-065 yüz atamaları (Q4 B.Cu; Q6, D10, R66, R67 F.Cu) korunmuştur. Kart dışındaki geçici blok alanı (x≈180–200, y≈55–65 mm) düzenlenmiştir; nihai kart içine taşıma ve genel routing TASK-085/TASK-008 kapsamındadır.

[Önce görünüm](../../hardware/docs/reports/task-076-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-076-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-076-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-076-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-076-20260924/verification.json)

## Kaynak, pin ve yerleşim kuralı

- **Nexperia BSS138P (Rev. 2 — 11 Aralık 2020, SOT-23 / TO-236AB):**
  1. *Deşarj anahtarı Q6 (F.Cu, rot 180°):*
     - Pin 3 (`Net-(Q6-D)` / Drain) doğrudan batıya, R67.2 pad'ine baktırıldı (y=57,5 mm doğrusal ekseninde, pad aralığı **2,60 mm**).
     - Pin 1 (`DISCH_G` / Gate) güney-doğuya, Pin 2 (`GND` / Source) kuzey-doğuya açıldı.
     - $V_{DS} = 60\text{ V} > 30,4\text{ V}$, $I_D = 360\text{ mA} \gg 30,3\text{ mA}$, $R_{DS(on)} \approx 2\ \Omega \ll 1000\ \Omega$.
  2. *Tersleyici anahtar Q4 (B.Cu, rot 0°):*
     - TASK-065 yüz atamasına uygun olarak B.Cu'da tutuldu (U13 ile aynı yüzey).
     - Pin 1 (`SW_EN`) batıya (U13 yönüne) yönlendirildi; logic 3.3V gate sürüşü ile $V_{GS} = 3,3\text{ V} > V_{GS(th)}$ (maks 1,5 V) güvenli tam iletim sağlar.
     - Pin 2 (`GND`) batı/kuzey-batıya, Pin 3 (`DISCH_G`) doğuya açıldı.
     - Q4.3 ile Q6.1 arasında B.Cu'dan F.Cu'ya geçiş için (x≈192, y≈60,5) konumunda tek bir sinyal viası planlanmıştır (pad mesafesi 4,08 mm).

- **PANJIT BZT52C12 (Rev. 01 — 2014, SOD-123):**
  - Pin 1 (Katot) güneyde `DISCH_G` koridoruna; Pin 2 (Anot) kuzeyde `GND` koridoruna bağlandı (rot 90°).
  - Q6.1–D10.1 (`DISCH_G`) ve Q6.2–D10.2 (`GND`) hatları paralel, kesişimsiz iki doğrusal koridor oluşturur (**3,63 mm**).
  - $V_Z = 12\text{ V}$ kenetleme gerilimi, Q6 BSS138P gate-source sınırını ($\pm 20\text{ V}$) güvenli aralıkta tutar ($P_D = 500\text{ mW} \gg 1,4\text{ mW}$).

- **Vishay CRCW0603100KFKTBBC (100 kΩ 0603):**
  - Pull-up direnci R66, rot -90° (270°) ile konumlandırıldı.
  - Pin 1 (`SW_OUT`) kuzeye açılarak LM74801 / çıkış anahtarı barasından beslenir.
  - Pin 2 (`DISCH_G`) güneye açılarak D10.1 ve Q6.1 düğümüne doğrudan bağlanır (**3,60 mm**).
  - 28 V'ta akım 0,28 mA, kayıp 7,8 mW'tır ($100\text{ mW}$ anma gücünün çok altındadır).

- **UniOhm PS122WF1001T4E (1 kΩ 2512 2 W anti-surge):**
  - R67 güç deşarj direnci rot 0° ile yerleştirildi.
  - Pin 1 (`OUT_POS`) doğrudan batıya, INA226 akım şöntü RShunt1 ve J4 banana çıkış yönüne bakar.
  - Pin 2 (`Net-(Q6-D)`) doğuya, Q6.3 drain pad'ine bakar.

| Alt Devre / Koridor | Elemanlar ve Pad/Net Yönü |
| --- | --- |
| Güç Deşarjı (OUT_POS → GND) | `OUT_POS` batıdan R67.1'e girer, R67.2'den Q6.3'e akar (2,60 mm); Q6.2 üzerinden GND'ye boşalır. |
| Gate Kenetleme (DISCH_G) | Q6.1 ↔ D10.1 ↔ R66.2 ↔ Q4.3 ortak `DISCH_G` düğümü (güney koridoru). |
| Referans / Pull-up (SW_OUT) | R66.1 kuzeyden LM74801 çıkış barasından (`SW_OUT`) beslenir. |
| Mantık Sürüşü (SW_EN) | `SW_EN` batıdan U13.4 çıkışından Q4.1'e girer (B.Cu, 3.3V logic). |
| GND Dönüşü | Q6.2 (F.Cu), D10.2 (F.Cu) ve Q4.2 (B.Cu) toprak koridoruna bağlanır. |

## R67 kayıp hesabı, ısı yayılımı ve hassas bloklara etki

1. **R67 Güç / Kayıp Hesabı:**
   - Normal çalışma (Çıkış açık, `SW_EN = HIGH`): Q4 iletimde, `DISCH_G` $\approx 0\text{ V}$, Q6 kesimdedir. Deşarj akımı ve kaybı **0 W**'tır. R66 üzerinden geçen 0,28 mA akım şönt öncesinden (`SW_OUT`) çekildiği için INA226 ölçümünü etkilemez.
   - Çıkış kapatıldığında / hata durumunda (`SW_EN = LOW` veya kart enerjisiz): Q4 kesime gider, R66 üzerinden Q6 gate dolar ($V_{GS} \le 12\text{ V}$), Q6 iletime geçer.
     - $V_{OUT} = 28\text{ V}$'ta sürekli deşarj:
       $$I_{disch} = \frac{28\text{ V}}{1000\ \Omega + 2\ \Omega} \approx 27,9\text{ mA} \implies P_{R67} = (0,0279)^2 \times 1000 = \mathbf{0,781\text{ W}} \quad (\%39\text{ yük})$$
     - $V_{OUT} = 30,4\text{ V}$'ta sürekli aşırı gerilim kenetleme tavanı:
       $$I_{disch} = \frac{30,4\text{ V}}{1002\ \Omega} \approx 30,3\text{ mA} \implies P_{R67} = (0,0303)^2 \times 1000 = \mathbf{0,920\text{ W}} \quad (\%46\text{ yük})$$
     - $1000\ \mu\text{F}$ yük kondansatörü darbe deşarj enerjisi (28 V → 5 V):
       $$E = \frac{1}{2} C (V_1^2 - V_2^2) = \frac{1}{2} (10^{-3}) (28^2 - 5^2) = \mathbf{0,380\text{ J}}$$
       Zaman sabiti $\tau = R \times C = 1000 \times 1000\times 10^{-6} = 1,0\text{ s}$; 2,6 saniyede gerilim 2 V altına iner.
2. **Isı Yayılımı ve Koruma Kısıtları:**
   - 2512 kılıflı R67 için 0,92 W sürekli kayıpta gövde sıcaklığı ortamın 40–55°C üzerine çıkabilir.
   - **INA226 Ölçüm Grubuna Etki:** R67, batı yönündeki INA226 şönt direnci (RShunt1) ve ölçüm entegresinden (U3) >7 mm uzaktadır. Şönt üzerinde termal gradyan veya Seebeck gerilimi ofseti oluşturmaz.
   - **RTC Grubuna Etki:** R67, güney-doğu yönündeki BQ32000 RTC entegresi ve Korchip 1F5 süperkapasitöründen (C33) >20 mm mesafededir. Kristal osilatörün sıcaklık frekans kaymasını ve süperkapasitörün ömür kısalmasını engeller.
   - **Grup İçi Termal:** Q4 (B.Cu'da ve R67 merkezine 8,6 mm uzakta) doğrudan ısıl akıdan korunmuştur. Q6 (2,6 mm mesafede) $I^2 R_{DS(on)} = (0,03)^2 \times 2 = 1,8\text{ mW}$ önemsiz güç harcar.

## Komşuluk, yüz seçimi ve devir notları

1. **Yüz Seçimi Koordinasyonu (TASK-065 Devri):**
   - Q4 `B.Cu` katmanında (U13 logic çıkışıyla doğrudan aynı yüzde), Q6, D10, R66 ve R67 `F.Cu` katmanında tutulmuştur.
   - Elemanların 2D izdüşümleri birbirine basmamaktadır (min 2D aralık **0,690 mm**). Bu sayede TASK-085 veya TASK-008'de kart içine taşınırken grubun tamamı arzu edilirse B.Cu'ya veya F.Cu'ya tek blok olarak flip edilebilir.
2. **Bağlantı Yönleri:**
   - Batı: `OUT_POS` ve `GND` (INA226 ve J4 çıkış klemensine bakar), `SW_EN` (U13'e bakar).
   - Kuzey: `SW_OUT` (LM74801 çıkış barasına bakar).

## Doğrulama

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **146 → 145** (D10 referans silk kırpılması çözüldü; yeni courtyard, clearance, short veya mask ihlali: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic parity:** **0 → 0**.
- **Courtyard kontrolü:** 5 eleman arasında minimum 2D aralık **0,690 mm** (R67–Q6 arası); çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 konum/açı/yüz ankrajları ve mevcut iz UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-076-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-076-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-076-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-076-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-076-20260924/verify.py)
