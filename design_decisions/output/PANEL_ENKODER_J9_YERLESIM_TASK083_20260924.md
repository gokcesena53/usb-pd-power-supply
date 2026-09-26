# Panel Enkoder Grubu (J9 + R34–R36 Pull-Up) İlişkisel Yerleşimi ve Slot/Kablo Tanımı — TASK-083, 24 Eylül 2026

Panel enkoder grubunun (`ROTARY ENCODER`) 3 SMD üyesi (`R34`, `R35`, `R36` 10k 0402 pull-up dirençleri) ve ilişkili 5 pinli THT kablo lehim ankrajı `J9`, NingBo KLS Electronic L-KLS4-EC1121S döner enkoder veri sayfası, TASK-066 enkoder panel montaj kararı, `PCB_GENEL_YERLESIM_KARARI_20260924.md` ve TASK-069 üretici kılavuzlarına uygun olarak ilişkisel olarak düzenlendi.

Bu görev, TASK-063 mekanik port seçiminden önce J9 kablo lehim bağlantısının yer gereksinimlerini, lehim/prob erişim koridorunu, kablo büküm zarfını, gerilim alma gereksinimlerini ve slot tipi seçeneklerini sayısal olarak tanımlar. R34–R36 pull-up dirençleri ortak bir $+3.3\text{V}$ güç barası ve paralel sinyal çıkışları oluşturacak şekilde `B.Cu` katmanında ilişkisel olarak hizalanmıştır.

J9'un nihai anakart koordinatı, açısı, montaj yüzü ve Ethernet mezanini (`J8`) ile fiziksel çakışma/komşuluk kabulünün tek yetkilisi **TASK-063**'tür. Mevcut J9 koordinatı ($x=58{,}00$, $y=91{,}60\text{ mm}$, rot $-90^\circ$, `F.Cu`) mutlak ankraj değildir; TASK-063'ün mekanik yerleşim kararı beklenirken şemadaki netlist, pin haritası ve elektriksel kurallar doğrulanmış, `Edge.Cuts` sınırına onaylı fiziksel slot kararı olmadan müdahale edilmemiştir.

[Önce görünüm](../../hardware/docs/reports/task-083-20260924/before.svg) ·
[Sonra ve koridorlar](../../hardware/docs/reports/task-083-20260924/after.svg) ·
[KiCad F.Cu katman çıktısı](../../hardware/docs/reports/task-083-20260924/board-top.svg) ·
[KiCad B.Cu katman çıktısı](../../hardware/docs/reports/task-083-20260924/board-bottom.svg) ·
[x/y/açı/yüz ve pad ölçümleri](../../hardware/docs/reports/task-083-20260924/verification.json)

---

## 1. Pin Haritası, Sinyal Ayrımı ve R34–R36 Pull-Up Düzeni (AC #1)

1. **J9 5 Tel Pin Haritası ve Şematik Doğrulaması:**
   - Ön paneldeki SW3 enkoderinden gelen beş telli kablo demeti, anakart üzerinde J9 THT deliklerine lehimlenir:
     - **Pin 1 (`ENCODER_A`):** Faz A sinyali $\leftrightarrow$ R34 Pad 2 pull-up $\leftrightarrow$ MCU U2.28 (GPIO22).
     - **Pin 2 (`GND`):** Enkoder Faz A/B ortak ucu C (toprak dönüşü).
     - **Pin 3 (`ENCODER_B`):** Faz B sinyali $\leftrightarrow$ R35 Pad 2 pull-up $\leftrightarrow$ MCU U2.29 (GPIO23).
     - **Pin 4 (`ENCODER_SW`):** Dahili basma butonu kontağı S1 $\leftrightarrow$ R36 Pad 2 pull-up $\leftrightarrow$ MCU U2.27 (GPIO21).
     - **Pin 5 (`GND`):** Buton dönüş ucu S2 (ayrı toprak dönüşü).
   - **Girişim Önleyici Toprak Dizilimi:** Sinyal telleri (Faz A, Faz B, Buton) arasına yerleştirilen Pin 2 ve Pin 5 GND hatları, kablo demeti boyunca fazlar arası kapasitif kuplajı ve çapraz konuşmayı (cross-talk) sönümler.

2. **R34–R36 Pull-Up Grubu İlişkisel Yerleşimi:**
   - Üç adet $10\text{ k}\Omega$ 0402 pull-up direnci (`B.Cu` katmanında, $x=40{,}70\dots 44{,}70\text{ mm}$, $y=116{,}20\text{ mm}$), daha önceki dağınık/ters yönelimli halinden (R36'nın $-90^\circ$ ters açısı) kurtarılarak **tek tip $90{,}0^\circ$** açıyla hizalandı:
     - **R34:** $(40{,}700, 116{,}200\text{ mm}, 90{,}0^\circ)$, Pad 1: $+3.3\text{V}$ ($y=116{,}710$), Pad 2: `ENCODER_A` ($y=115{,}690$).
     - **R35:** $(42{,}700, 116{,}200\text{ mm}, 90{,}0^\circ)$, Pad 1: $+3.3\text{V}$ ($y=116{,}710$), Pad 2: `ENCODER_B` ($y=115{,}690$).
     - **R36:** $(44{,}700, 116{,}200\text{ mm}, 90{,}0^\circ)$, Pad 1: $+3.3\text{V}$ ($y=116{,}710$), Pad 2: `ENCODER_SW` ($y=115{,}690$).
   - **Güç ve Sinyal Çıkış Baraları:**
     - Pad 1'ler $y = 116{,}710\text{ mm}$ hattında tek bir düz $+3.3\text{V}$ güç barası oluşturur ($\Delta Y = 0{,}000\text{ mm}$).
     - Pad 2'ler $y = 115{,}690\text{ mm}$ hattında kuzeye, MCU'ya (GPIO21, 22, 23) doğru paralel 3 hatlı sinyal koridoru olarak çıkar.
     - Elemanlar arası adım tam **$2{,}000\text{ mm}$** olup avlu boşluğu $1{,}030\text{ mm} \ge 0{,}50\text{ mm}$ şartını eksiksiz sağlar.

| Eleman | Değer / Kılıf | Konum (x, y) | Açı | Katman | Netler (Pad 1 / Pad 2) | İşlev |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `R34` | 10k / 0402 | $(40{,}700, 116{,}200)$ | $90{,}0^\circ$ | `B.Cu` | Pad 1: `+3.3V` / Pad 2: `ENCODER_A` | Faz A pull-up (GPIO22) |
| `R35` | 10k / 0402 | $(42{,}700, 116{,}200)$ | $90{,}0^\circ$ | `B.Cu` | Pad 1: `+3.3V` / Pad 2: `ENCODER_B` | Faz B pull-up (GPIO23) |
| `R36` | 10k / 0402 | $(44{,}700, 116{,}200)$ | $90{,}0^\circ$ | `B.Cu` | Pad 1: `+3.3V` / Pad 2: `ENCODER_SW` | Buton pull-up (GPIO21) |
| `J9` (Ankraj) | Conn_01x05 THT | $(58{,}000, 91{,}600)$ | $-90{,}0^\circ$ | `F.Cu` | 1: A, 2: GND, 3: B, 4: SW, 5: GND | Panel kablo lehim pedleri |

---

## 2. Lehim/Prob Erişimi ve Kablo Büküm Zarfı (AC #2)

1. **LCD Dışı Lehimleme ve Havya Açısı Erişimi:**
   - J9 lehim pedleri $X = 58{,}000\text{ mm}$ eksenindedir.
   - TFT032B018 ekran modülü gövdesi $X \ge 63{,}720\text{ mm}$ (toleranslı en kötü durum $X \ge 63{,}520\text{ mm}$) bölgesindedir.
   - J9 ile LCD sol çerçevesi arasındaki net yatay açıklık **$5{,}720\text{ mm}$** (en kötü durumda **$5{,}520\text{ mm}$**)'dir.
   - $4{,}200\text{ mm}$ ped adımı sayesinde lehimleme havyası $45^\circ\dots 60^\circ$ serbest yaklaşımla LCD camına ve polarizörüne temas riski olmaksızın telleri güvenle lehimleyebilir.
   - Multimetre ve osiloskop probları için test/servis sırasında yeterli temas alanı mevcuttur.

2. **Kablo Özellikleri ve Büküm Zarfı:**
   - **Tel Tipi:** 5 adet esnek çok telli (stranded) izole bakır tel, 26 AWG – 28 AWG ($0{,}14\text{ mm}^2$), maksimum tel dış çapı $OD \le 1{,}50\text{ mm}$, maksimum boy $150\text{ mm}$.
   - **Minimum Büküm Yarıçapı:** IPC-2221 uyarınca statik montaj büküm yarıçapı $R_{\text{min}} \ge 3 \times OD \approx \mathbf{4{,}50\text{ mm}}$ (montaj esneme payı için tavsiye $7{,}5\text{ mm}$).
   - **Kablo Derinlik Bütçesi:** Kablo demetinin karta lehimlendikten sonra bükülerek yönlenmesi için $Z \ge 6{,}0\text{ mm}$ (tavsiye $\ge 8{,}0\text{ mm}$) dikey montaj hacmi ayrılmalıdır.

---

## 3. Kablo Çıkış Güzergâhı Seçenekleri ve İzolasyon Kuralları (AC #2, AC #5)

Anakart yerleşimi TASK-063 tarafından kesinleştirilirken, enkoder kablosunun parazit toplamaması ve hassas devreleri etkilememesi için 3 farklı çıkış güzergâhı tanımlanmıştır:

1. **Seçenek A: Ön Panele Doğrudan Batı Çıkışı (Önerilen):**
   - Teller J9'un üst yüzeyinden (F.Cu) lehimlenir ve derhal batıya ($-X$ yönüne) bükülerek kart kenarı ($X=50{,}28\text{ mm}$) ile kutu ön duvarı arasındaki boşluktan enkoder miline ulaşır.
   - **Toplam Kablo Boyu:** $< 60\text{ mm}$.
   - **Avantajı:** En kısa güzergâh; LCD ekranın, alt kattaki güç indüktörlerinin (L1, L3) ve anahtarlama diyotlarının tamamen uzağında kalır.
2. **Seçenek B: Kuzey-Batı Kenar Güzergâhı:**
   - Teller J9'dan çıkarak $X \approx 52\dots 55\text{ mm}$ koridorundan kuzeye (düşük Y) yönlenir, RJ45 modülünün üzerinden geçmeden kutu tavanından panele kıvrılır.
   - **Toplam Kablo Boyu:** $< 80\text{ mm}$.
3. **Seçenek C: Alt Yüzden Lehimleme ve Slot/Kenar Çıkışı:**
   - Teller karta `B.Cu` yüzeyinden lehimlenir, alt yüzdeki Ethernet mezanini boşluğundan veya bir kenar yarığından panele aktarılır.

### Zorunlu İzolasyon ve Gerilim Alma Kuralları (TASK-063 için Şartlar):
- **Anten Yasaklı Alanı:** Kablo demeti ESP32-C6 (U2) PCB anteninin $15\text{ mm}$ çevresindeki RF keepout bölgesinden KESİNLİKLE GEÇİRİLEMEZ.
- **Güç Anahtarlama Düğümleri:** Kablo demeti AOZ1284 buck (L1, D2, LX) ve TPS55340 boost (L3, D4, SW) anahtarlama hatlarının üzerinden geçirilemez.
- **Mekanik Gerilim Alma (Strain Relief):** Kablonun lehim noktalarından doğrudan çekilmesini önlemek amacıyla, J9'un en fazla $15\text{ mm}$ uzağında kutu ön paneline entegre bir kablo tutucu boss veya cırt kelepçe (zip-tie) köprüsü bulunmalıdır.

---

## 4. Slot Tipi Seçimi ve Freze Parametreleri (AC #6)

Kablo geçişi için fiziksel PCB yarığı (milled slot) ile serbest kart kenarı koridoru değerlendirilmiş ve aşağıdaki ölçülü parametreler belirlenmiştir:

1. **Seçenek 1: Fiziksel Frezelenmiş Yarık (Milled Slot in Edge.Cuts):**
   - *Uygulanabilirlik:* Eğer TASK-063 kabloların kartın alt yüzünden üst panele PCB gövdesi içinden geçmesini gerektirirse kullanılır.
   - **Yarık Genişliği ($W_{\text{slot}}$):** $2{,}50\text{ mm}$ (5 adet $1{,}5\text{ mm}$ telin rahat geçişi için).
   - **Yarık Uzunluğu ($L_{\text{slot}}$):** $22{,}00\text{ mm}$ (J9 pad dizisinin $16{,}8\text{ mm}$ açıklığını kapsar).
   - **Uç Radyüsü ($R$):** $1{,}25\text{ mm}$ (tam yuvarlatılmış freze ucu).
   - **Üretici Freze Çapı:** Standart CNC router ucu $\varnothing 2{,}00\text{ mm}$ (üretici ek maliyetsiz minimum $\varnothing 1{,}00\text{ mm}$).
   - **Bakır Açıklığı:** Yarık kenarından bakır yollara ve GND düzlemine en az $\ge 0{,}50\text{ mm}$ izolasyon mesafesi.
   - **Kalan PCB Et Kalınlığı:** Yarık ile dış kart kenarı arasında en az $\ge 3{,}00\text{ mm}$ rijit taşıyıcı laminat payı.
2. **Seçenek 2: Açık Kart Boşluğu / 3D Keepout Koridoru (ÖNERİLEN VE SEÇİLEN):**
   - J9 pedleri $X=58{,}00\text{ mm}$ konumunda olup kart kenarına ($X=50{,}28\text{ mm}$) $7{,}72\text{ mm}$ mesafededir.
   - Teller doğrudan üstten veya kenardan lehimlenip kutu boşluğundan panele yönlendirilebilir; kartta fiziksel bir yarık açılmasına gerek yoktur.
   - **Tanımlanan Koridor:** $X \in [52{,}00, 58{,}00]\text{ mm}$, $Y \in [88{,}00, 112{,}00]\text{ mm}$ ($6{,}00 \times 24{,}00\text{ mm}$), $Z \ge 8{,}00\text{ mm}$.
   - **Gerekçe:** PCB laminat bütünlüğünü bozmaz, iç katman toprak düzleminin sürekliliğini korur, freze maliyeti getirmez ve TASK-063 öncesinde Edge.Cuts katmanını gereksiz yere değiştirmez.

---

## 5. Doğrulama ve DRC Sonuçları (AC #4)

- `kicad-cli pcb drc --schematic-parity`:
  - **DRC İhlalleri:** **145 → 145** (yeni courtyard, clearance, short, hole veya silk ihlali: **0**).
  - **Bağlantısız Öğeler:** **360 → 360** (temel rota envanteri korundu).
  - **Schematic Parity:** **0 → 0** (şema ile netlist tam uyumlu).
- **Courtyard ve Açıklık Kontrolü:**
  - R34, R35, R36 arasında 2D avlu boşluğu: **$1{,}030\text{ mm}$** ($\ge 0{,}50\text{ mm}$, çakışma: **0**).
- **Sabit Ankrajlar ve İzler:** `J7`, `J3` (kilitli), `J9`, `H1–H4`, `D5`, `U11` konum/açı/yüz ankrajları ve TASK-058 D5.2--U11.9 FB izi UUID'leri tamamen korundu.

Kanıt dosyaları:
- [DRC önce](../../hardware/docs/reports/task-083-20260924/drc-before.json)
- [DRC sonra](../../hardware/docs/reports/task-083-20260924/drc-after.json)
- [Doğrulama ve pad ölçüm verileri](../../hardware/docs/reports/task-083-20260924/verification.json)
- [Yerleşim betiği](../../hardware/docs/reports/task-083-20260924/place.py)
- [Doğrulama betiği](../../hardware/docs/reports/task-083-20260924/verify.py)
