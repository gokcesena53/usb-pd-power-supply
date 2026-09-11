from pathlib import Path
import json,re,xml.etree.ElementTree as E,html,hashlib,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('AB','C:/Windows/Fonts/arialbd.ttf'))
styles={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=lead,spaceAfter=8,textColor=colors.HexColor("#"+col)) for k,font,size,lead,col in [('p','Arial',9.3,13,'253542'),('h','AB',13,17,'164d65'),('t','AB',21,26,'164d65'),('c','Arial',8,10.5,'253542')]}
out=Path('output/pdf/bloklar');out.mkdir(parents=True,exist_ok=True)
root=E.parse('reports/output-update/after.xml').getroot();cs={c.get('ref'):c for c in root.find('components')};nets={};func={}
for n in root.find('nets'):
 for p in n:nets[(p.get('ref'),p.get('pin'))]=n.get('name');func[(p.get('ref'),p.get('pin'))]=p.get('pinfunction','')
blocks=[
 dict(file='01_USB_C_INPUT',title='USB-C giriş',sheet='USB_C_INPUT',refs=['J1'],pins=['J1'],source='datasheets/DX07B024JJ1R1500.pdf',notes=[
 'J1 DX07B024JJ1R1500: VBUS A4/A9/B4/B9 ortak USB_VBUS; GND A1/A12/B1/B12 ve shield GND. CC1 A5 ve CC2 B5 ayrı netlerdir. USB2 D+ A6/B6, D− A7/B7 birleşir.',
 'D+/D− ve CC global etiketleri bidirectional yapıldı. Aynı fiziksel veri hattının iki konektör yüzü birleştirilirken CC1 ve CC2 birleştirilmedi.',
 'Açık: J1 PCB footprint’i seçili değil. Süper hızlı veri/SBU uçları kullanılmıyor. USB veri/CC ESD koruması ve kablo girişindeki transient davranışı ayrıca tasarlanmalı.',
 '5 A için yalnız konektör yeterli değildir: PD sözleşmesi, kablo ve termal yol birlikte doğrulanır. PCB dosyası boş; diferansiyel hat empedansı ve kasa/shield bağlantısı fiziksel olarak denetlenemedi.']),
 dict(file='02_USB_PD_CONTROLLER',title='USB PD kontrolü ve ana anahtar',sheet='USB_PD_CONTROLLER',refs=[c for c in cs if cs[c].find('sheetpath').get('names')=='/USB_PD_CONTROLLER/'],pins=['U1','Q1','Q2','Q3','Q4'],source='datasheets/AP33772S.pdf; https://www.diodes.com/datasheet/download/AP33772S.pdf',notes=[
 'AP33772SDKZ-13-FA02, VSEL=100 kΩ/floating seçimiyle varsayılan 5 V başlangıcını hedefler. DNP R21 durumu korunmuştur. VCC=PD_VBUS_SENSED, VOUT monitörü PD_VOUT’u 100 Ω üzerinden izler; EP GND’dir.',
 'Güncel dosyada tekrar görülen R4/R5/R6/R7 pull-up, R8 INT ve R11 giriş boşlukları kapatıldı. Şematikte görünen yakınlık yeterli sayılmadı; XML netlerindeki birleşmeler doğrulandı.',
 'R8=12 kΩ/R9=20 kΩ: 4,37–5,33 V interrupt yüksek seviyesini ideal olarak 2,731–3,331 V’a indirir. 5 V nominalde 3,125 V. Direnç toleransı ve açılışta MCU enerjisizken enjeksiyon akımı ayrıca dikkate alınır.',
 'R11=5 mΩ: 5 A’da 25 mV düşüm, 0,125 W. 1 W/2512 gereksinimi korundu. R12 gate direnci için 0603 korundu; anahtarlama darbesi nedeniyle körlemesine 0402’ye indirilmedi.',
 'Q3/Q4 gerçek paket eşlemesi G4, S1/2/3, D5/6/7/8 olarak mevcut. Kritik açık: IRF7855 Rds garantisi VGS=10 V için; AP33772S ile garantili sürüş uygunluğu gösterilmemiş. SELECTED_FOR_PROTOTYPE alanı kullanıcı seçimi olarak korundu, uygunluk onayı sayılmadı.',
 'Koruma MOSFET’i kapanınca PD_VOUT ve buradan beslenen MCU kapanabilir. Bazı hata kurtarmalarında yeni PD isteği gerektiğinden kontrol beslemesi/kurtarma stratejisi doğrulanmalı.']),
 dict(file='03_MCU',title='ESP32-C6 kontrol bloğu',sheet='MCU',refs=[c for c in cs if cs[c].find('sheetpath').get('names')=='/MCU/' and c not in ['BT1','U4','C9','C10','R22','R23','R24','R25','R26']],pins=['U2','J2'],source='datasheets/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf',notes=[
 'U2 +3.3V üzerinden beslenir. C5 22 µF/0805 korunur; 0402 pakette nominal ve bias koşulu varsayılmaz. C6 bypass 0402 oldu. Reset RC ve BOOT GPIO9 yapısı korunur; GPIO8 üzerinde 10 kΩ pull-up vardır.',
 'TFT sinyalleri bu sayfada output, encoder ve INA_ALERT input olarak işaretlendi. I²C hatları clock stretching/çift yönlü kullanım nedeniyle bidirectional tutuldu. Etiket şekli elektriksel net adını değiştirmez.',
 'GPIO4/5/15 strapping işlevleriyle TFT paylaşımı başlangıç koşullarına göre kontrol edilmeli. Harici TFT reset/IO durumunun boot örnekleme aralığını bozmadığı henüz ölçülmedi.',
 'J2 yalnız UART_TX/RX/GND; harici dönüştürücü 3,3 V logic olmalı. USB D+/D− için 22 Ω seri dirençler mevcut. RF anten keepout ve modül altında bakır alanları boş PCB nedeniyle incelenemedi.',
 'Wi-Fi yük adımı, CHIP_PU rampası ve düşük girişte yeniden başlatma prototip testidir. Yaklaşık 0,4 A yük tahmini sabit garanti değildir; iç buck 1 A tasarım yüküyle ele alınır.']),
 dict(file='04_RTC_BATTERY',title='RTC ve yedek pil',sheet='MCU',refs=['U4','BT1','R22','R23','R24','R25','R26','C9','C10'],pins=['U4','BT1'],source='datasheets/RV-3028-C7.pdf; datasheets/L-KLS5-CR2032-05.pdf',notes=[
 'RV-3028-C7: CLKOUT1 kullanılmıyor, INT2 RTC_INT, SCL3 RTC_SCL, SDA4 RTC_SDA, VSS5 GND, VBACKUP6 pil ağı, VDD7 +3.3V, EVI8 10 kΩ üzerinden GND. Pin/net tablosu aşağıdadır.',
 'BT1 için L-KLS5-CR2032-05-R1 seçildi. Özdisan ürün 497433, inceleme anında 70 stok gösteriyordu. MPN, üretici, tedarikçi ve footprint şematiğe yazıldı. Pil yuvası CR2032 hücreyi içermez; 3 V birincil hücre ayrıca alınır.',
 'Üretici 31.03.2025 çizimindeki padler 3,60×4,50 mm, merkezler x=±14,55 mm; dış pad açıklığı 32,70 mm. Sol pad 1 pozitif, sağ pad 2 negatif. SMD footprint ve basitleştirilmiş STEP eklendi.',
 'Özdisan R1 alt kodu ile üretici temel -05 çizimi aynı aile kabul edildi; sipariş edilen parçanın revizyonu/kaplama varyantı mekanik çizimle karşılaştırılmalı. Yuvasının gövde ölçüsü 28,50×16,00 mm, yükseklik 5,50 mm.',
 'Birincil CR2032 kullanılacağından RTC trickle charge kapalı tutulmalıdır. Şematikte uyarı eklendi; firmware/EEPROM ayarı değiştirilmedi. R22 1 kΩ yedek besleme serisi ve C10 korunur. VBACKUP güç ERC kaydı gerçek bağlantı eksikliği olarak yorumlanmadı.']),
 dict(file='05_TFT',title='TFT arayüzü ve arka ışık',sheet='USER INTERFACE',refs=['J3','Q5','R28','R29','R30','R31','R32','R33'],pins=['J3','Q5'],source='datasheets/NHD-2.4-240320AF-CSXP.pdf',notes=[
 'Projedeki gerçek ekran NHD-2.4-240320AF-CSXP, 40 pin 0,5 mm FFC; önerilen konektör Molex 54132-4062. J3 MPN konektör, DisplayMPN ekran olarak ayrı alanlara yazıldı. Önceki rapordaki model belirsizliği bu yerel datasheet ile giderildi.',
 '4-wire SPI: IM0/IM1/IM2=0/1/1 (pin31 GND, 32/33 +3.3V). SDA9=MOSI, CS10, SCL11, DC12, RESET30. Datasheet wiring diagram doğrultusunda RDX13 ve DB0–DB15 pin14–29 GND’ye bağlandı. Pin6 SDO ve40 TE kullanılmıyor.',
 'Q5 AO3400A kullanıcı seçimi korundu. G1 PWM/100 Ω ve100 kΩ pull-down; S2 GND; D3 BL_SINK. Değişimden sonra açık kalan drain yeniden bağlandı.',
 'Arka ışık: 160 mA tipik, 200 mA maksimum; 3,0 V tipik Vf, 2,7–3,4 V aralığı. Voltaj değeri akım regülasyonu yerine geçmez. BACKLIGHT_3V0 hâlâ kaynaksız; ayrı LED akım sürücüsü seçimi açık.',
 'Dört 15 Ω kol direncinde eşit dağılımla 40 mA için 24 mW, 50 mA için37,5 mW olur. 0402 seçimi en az62,5 mW ve sıcaklık derating kontrolü ister. 3,0 V anoda seri15 Ω eklenirse 160 mA garanti edilemez; mevcut ağ sabit akım sürücüsü değildir.',
 'Molex footprint kütüphanesi Downloads klasörüne bağımlıydı; proje içine kopyalanarak yol taşınabilir hale getirildi. FFC temas yönü ve mekanik yerleşim gerçek ekran kablosuyla kontrol edilmeli.']),
 dict(file='06_ENCODER',title='Rotary encoder',sheet='USER INTERFACE',refs=['SW3','R34','R35','R36'],pins=['SW3'],source='datasheets/L-KLS4-EC12-012424-W.pdf',notes=[
 'SW3 A1=ENCODER_A→GPIO22, ortak C2=GND, B3=ENCODER_B→GPIO23, switch4=ENCODER_SW→GPIO21, switch5=GND. A/B/switch hatlarında 10 kΩ +3.3V pull-up bulunur.',
 'Aktif kontakta yaklaşık 3,3/10k=0,33 mA akar. A/B yön çözümleme ve buton debounce firmware’de yapılmalıdır. GPIO bağlantıları güncel netlistte doğrulandı.',
 'Etiketler arayüz sayfasında output, MCU tarafında input olarak düzenlendi. Pull-up dirençleri0402 yapıldı; değer değiştirilmedi.',
 'Mevcut özel encoder footprint’i değiştirilmedi. Önceki mekanik yerleşim belirsizliği ve gömülü sembol/kütüphane farkı hâlâ açık; sembol eşitleyerek fiziksel pin sırası körlemesine değiştirilmedi. Datasheet ve gerçek parçayla montaj tırnakları/şaft yönü kontrolü gerekir.']),
 dict(file='07_POWER_GENERATION',title='AOZ1284PI — iç 3,3 V rail',sheet='POWER GENERATION',refs=[c for c in cs if cs[c].find('sheetpath').get('names')=='/POWER GENERATION/'],pins=['U5','U6'],source='reports/buck-20260910/AOZ1284PI.pdf; https://www.aosmd.com/sites/default/files/res/datasheets/AOZ1284PI.pdf',notes=[
 'DATASHEET VALUE: U5 pin1 LX,2 BST,3 GND,4 FSW,5 COMP,6 FB,7 SS,8 EN, exposed-pad VIN (KiCad9). Giriş5–28 V çalışma sınırları içindedir. C17 BST–LX arasında100 nF. EP GND’ye bağlanmaz.',
 'CALCULATED VALUE: R38=100k için denklem476,19kHz, tablo500kHz. İdeal duty5V’ta%66,28V’ta%11,79. L22µH ile ripple0,107/0,278A; L−%20 ile en kötü0,347A, peak1,174A. On-time28V’ta247,5ns, minimum150ns üzerinde.',
 'ENGINEERING CHOICE: L22µH, normal yük için Isat≥2A/Irms≥1,5A; Schottky60V/2A. Diyot ortalama0,882A; VRRM>28V şartı. Bu ratingler kısa devre yeterliliği değildir; kesin MPN/footprint açık.',
 'Cin2×10µF50V +100nF50V; etkili≥10µF. Cout2×47µF10V; etkili≥44µF. MLCC bias/tolerans eğrileri seçilecek parçada doğrulanır. Bu yüksek kapasiteli elemanlar0402’ye küçültülmedi.',
 'FB10k/3,2k ile3,300V nominal. Css10nF ve2,5µA ile3,2ms; kaynak akımının2–3µA aralığında2,67–4ms. COMP12,7k+18nF seriGND. Co44µF veGEA200µA/V ilefc≈10kHz;170µA/V ile8,5kHz.',
 'COMP denklemleri: Rc=fc(Vo/Vfb)2πCo/(GEA·GCS); Cc=1,5CoRL/Rc. Birinci Cc denklemi kullanıldı. Faz marjı ölçülmedi. EN: TL4312,495V şönt, R43 1k/2W veR42 100k. 28V’taR43≈0,651W; doğrudan EN–PD_VOUT bağlantısı yok. Bu harici UVLO değildir.',
 'Ana5A yük buck üzerinden geçmez. Kontrol ağı hesaplanmış olsa da gerçek L/D/MLCC seçimi, yük adımı, başlangıç ve termal testler açık. Ek EN bias kaybı sistem güç bütçesine dahildir.']),
 dict(file='08_POWER_SENSING',title='INA228 ve çıkış şöntü',sheet='POWER SENSING',refs=['U3','R27','RShunt','C11'],pins=['U3'],source='datasheets/ina228.pdf',notes=[
 'U3 Vin+10=PD_VOUT, Vin−9=OUT_POS; VBUS8=OUT_POS. Böylece şönt öncesi/sonrası akım farkı ve terminale giden gerilim izlenir. A1/A0 GND ile adres0x40; VS6 +3.3V, GND7 GND.',
 'RShunt5mΩ:5A’da25mV,0,125W. 1W/2512 gereksinimi korunur. %1 şönt toleransı kalibrasyon öncesi yaklaşık%1 ölçek hatası oluşturur; kesin düşük TCR parça seçilmedi.',
 'SDA4/SCL5 çift yönlü I²C netleri; ALERT3,10k pull-up ile MCU GPIO3. C11 100nF0402 bypass. INA228 ölçüm yapar; kendi başına hızlı sabit akım güç regülatörü değildir.',
 'Şönt Kelvin sense bağlantıları PCB’de güç padinin iç tarafından ayrılmalı; yüksek akım izi üzerinden gerilim alma ölçüm hatası yapar. PCB henüz boş olduğundan bu yerleşim kontrolü yapılmadı.',
 'Kalibrasyon ve ADC aralığı firmware’de seçilecek;25mV ölçümü uygun shunt range içinde tutulur. Çıkış anahtarı eklendiğinde VBUS ve shunt konumu ölçülmek istenen gerçek terminale göre yeniden değerlendirilir.']),
 dict(file='09_POWER_OUTPUT',title='Güç çıkışı ve panel bağlantıları',sheet='POWER OUTPUT',refs=['J4','J5','J6','J7'],pins=['J4','J5','J6','J7'],source='datasheets/pi-CCS-JOHN-108-0904-001.pdf; datasheets/DG142R-5.08-XXP-1Y-00A(H)T0-l.pdf',notes=[
 'J4.1 OUT_POS; J4.2 GND. J5 kırmızı108-0902-001 OUT_POS’a; J6/J7 siyah108-0903-001 GND’ye kabloyla bağlanır. Kullanıcının mevcut üçüncü jack’i korundu. Siyah jack’ler protective earth değil, devreGND’sidir.',
 'Degson2P terminal:5,08mm pitch; aynı kutbun iki bacağı7,62mm aralıklı. Dört delikØ1,35mm; bakır pad2,35mm mühendislik seçimi. Pad1/1 ve2/2 aynı kutuplardır. Body12,70×14,10mm,13,4mm reference yükseklik; önceki gövde geometrisi düzeltildi.',
 'Footprint kökeni ilk pinin birinci bacağıdır. İlk kutup(0,0)/(0,7,62), ikinci(5,08,0)/(5,08,7,62). Gövde sol−2,54; sağ10,16; üst−1,75; alt12,35mm. Aynı kutbun her iki deliği PCB’de aynı neti taşımalı.',
 'Cinch jack’ler panel montajlı lehim terminallidir. MontajØ8,33mm ve flat6,35mm; başlıkØ11,13mm; panel kalınlığı en fazla8,8mm. Panel footprint’lerinde bakır pad yoktur; şematikte on_board=no ile ana PCB’den dışlanır. Çizim yeşil0904 aile üyesidir; kırmızı/siyah ürün kimlikleri Cinch ürün sayfalarıyla doğrulandı.',
 'mm birimli çift düz yüzlü kesimDXF’i ve iki mekanik footprint verildi. Nut/lug ayrıntısı tam ölçülü olmadığından STEP yalnız basitleştirilmiş zarf modelidir. Üretim paneli gerçek parçayla prova edilmelidir.',
 'Bu aşamada PD_VOUT→şönt→OUT_POS geçişi vardır. Ayrı CV/CC, çıkış kapatma/ters akım ve deşarj devresi eklenmiş değildir. 28V×5A=140W terminal garantisi sayılamaz; adaptör/kablo ve iç devre kayıpları bütçeden düşülür.'])]
def para(t,kind='p'):return Paragraph(html.escape(str(t)).replace('\n','<br/>'),styles[kind])
def tab(rows,widths):
 t=Table([[para(v,'c') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1eff5')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c4d0d7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return t
def footer(c,d):c.setFont('Arial',8);c.drawString(43,24,'10.09.2026 • Şematik denetimi • Fiziksel PCB ve prototip doğrulaması yapılmadı');c.drawRightString(550,24,str(d.page))
def build(name,story):SimpleDocTemplate(str(out/(name+'.pdf')),pagesize=(595.28,841.89),leftMargin=43,rightMargin=43,topMargin=40,bottomMargin=42,title=name,author='Codex').build(story,onFirstPage=footer,onLaterPages=footer)
stats=Path('reports/output-update/erc.rpt').read_text(encoding='utf8');errors=stats.count('; error');warnings=stats.count('; warning')
for b in blocks:
 st=[para(b['title'],'t'),para('Tasarım dokümanı / güncel bağlantılar / açık işler','h')]
 for n in b['notes']:st.append(para(n))
 st.extend([PageBreak(),para('Pin ve net kontrol tablosu','h'),para('Gerçek KiCad XML netlisti. NC satırları otomatik olarak doğrulanmış kabul edilmez; kullanım niyeti ilk sayfada açıklanmıştır. Datasheet amacı ile karşılaştırma bulguları ilk bölümde belirtilir.')])
 rows=[['Eleman.pin','Pin işlevi','Güncel net']]
 for ref in b['pins']:
  for (a,p),net in sorted(nets.items(),key=lambda kv:(kv[0][0],len(kv[0][1]),kv[0][1])):
   if a!=ref:continue
   fn=func[(a,p)];fn=re.sub(r'_'+re.escape(p)+'$','',fn)
   if ref=='J3':fn={1:'GND',6:'SDO',7:'VDD',8:'VDDI',9:'SDA',10:'CSX',11:'SCL (SPI)',12:'DCX (SPI)',13:'RDX',30:'RESX',31:'IM0',32:'IM1',33:'IM2',34:'LED-K1',35:'LED-K2',36:'LED-K3',37:'LED-K4',38:'LED-A',39:'GND',40:'TE'}.get(int(p),'NC' if int(p)<6 else 'DB'+str(int(p)-14))
   rows.append([ref+'.'+p,fn,'NC / kullanılmıyor' if net.startswith('unconnected-') else net])
 st.append(tab(rows,[72,115,322]));st.extend([Spacer(1,12),para('Parça ve footprint listesi','h')])
 rows=[['Ref.','Değer','Footprint / seçim durumu']]
 for ref in b['refs']:
  c=cs[ref];rows.append([ref,c.findtext('value'),c.findtext('footprint') or 'SEÇİLMEMİŞ'])
 st.append(tab(rows,[48,140,321]));st.extend([PageBreak(),para('Şematik görünümü ve doğrulama sınırları','h')])
 im=Path('reports/output-update/svg')/('masaüstü güç kaynağı-'+b['sheet']+'.png')
 st.append(Image(str(im),width=509,height=360));st.append(Spacer(1,10))
 st.append(para(f'Tüm projede ERC: {errors} hata, {warnings} uyarı. Hatalar kaynak sürücü tanımları olarak ayrıca listelenmiştir. Off-grid uyarıları telin kopuk olduğu anlamına gelmez. Gerçek bağlantılar netlistten kontrol edildi.'))
 st.append(para('Kaynaklar: '+b['source']))
 if b['file'].startswith('04'):st.append(Paragraph('<link href="https://www.ozdisan.com/p/pil-yuvalari-484/kls-electronic-l-kls5-cr2032-05-r1-497433" color="#16658a">Özdisan L-KLS5-CR2032-05-R1 ürün sayfası</link>',styles['p']))
 if b['file'].startswith('09'):st.append(Paragraph('<link href="https://www.cinch.com/products/rf-microwave/accessories/banana-and-tip-connectors/108-0902-001" color="#16658a">Cinch kırmızı jack ürün sayfası</link>',styles['p']))
 build(b['file'],st)
# Reconstruct the actual value/footprint delta rather than relying only on mutation logs.
before=E.parse('reports/output-update/before.xml').getroot();old={c.get('ref'):c for c in before.find('components')};delta=[]
for ref,c in cs.items():
 for key in ['value','footprint']:
  ov=old[ref].findtext(key) if ref in old else None;nv=c.findtext(key)
  if ov!=nv:delta.append([ref,key,ov or '(boş)',nv or '(boş)'])
st=[para('Değişiklik ve teslim raporu','t'),para('Bu paket dokuz ayrı blok dokümanı, bu değişiklik raporu, netlist/ERC kanıtları ve özel footprint dosyalarını kapsar.'),para('Uygulananlar','h')]
for txt in ['POWER OUTPUT: mevcut J4/J5/J6/J7 üzerinden kırmızı pozitif / iki siyah GND panel bağlantısı yapıldı; banana jack’ler off-board tanımlandı.','Klemens delik dizisi korundu; hatalı gövde sınırları düzeltildi. Pil yuvası ve iki panel footprint’i; DXF ve basitleştirilmiş STEP modelleri eklendi.','RTC: Özdisan stoklu KLS yuvası BT1’e MPN ve footprint ile eklendi. Birincil CR2032 ayrı hücredir; şarj kapalı olmalı.','Küçük R/C footprint’leri0402 yapıldı. Güç/bias gereksinimi nedeniyle istisnalar: R11,RShunt,R43,R12; C3,C4,C5,C7,C8,C12,C13,C15,C16. C7/R12 için0603 tutuldu.','Global label yönleri sinyal üreten/tüketen sayfaya göre düzenlendi; veri ve I²C bidirectional, güç netleri passive. Yeni GND bağlantıları güç sembolleriyle gösterildi.','TFT’nin gerçek datasheet’i bulundu; RDX/DB girişleriGND’ye alındı. Kullanıcının AO3400A Q5 seçimi korundu; drain boşluğu düzeltildi.','Güncel dosyada tekrar görülen PD pull-up/INT/giriş şöntü kopuklukları giderildi. Önceki rapor yalnız önceki dosya anlık görüntüsünü temsil eder.'] :st.append(para(txt))
st.append(para(f'Son ERC: {errors} hata / {warnings} uyarı. PWR_FLAG eklenerek susturulmadı. Ana IRF7855 sürüşü, arka ışık akım kaynağı, kesin L/D/MLCC seçimi ve boş PCB doğrulaması açık.'))
st.extend([PageBreak(),para('Referans bazında gerçek değişiklikler','h'),tab([['Ref.','Alan','Önce','Sonra']]+delta,[42,55,195,217])])
st.extend([PageBreak(),para('Etiket yönleri','h')])
changes=json.loads(Path('reports/output-update/changes.json').read_text(encoding='utf8'));lr=[v for v in changes if v[2]=='Label direction'];st.append(tab([['Sayfa','Net','Önce','Sonra']]+[[v[0],v[1],v[3],v[4]] for v in lr],[156,177,88,88]))
st.extend([PageBreak(),para('Footprint kanıtı','h'),Image('reports/output-update/footprint-svg.png',width=509,height=75),Spacer(1,12),Image('reports/output-update/models.png',width=509,height=152),para('Footprint’ler KiCad pcbnew ile yüklendi. Dört STEP modelinin katı geometri geçerliliği kontrol edildi. Modeller basitleştirilmiş zarf geometrisidir; üretici detay modeli değildir. Panel jack footprint’inde elektriksel pad bulunmaması bilinçli: bunlar ana PCB’ye lehimlenmez.'),para('Gerçek tasarım PCB’si değiştirilmedi. reports/output-update/footprint-review.kicad_pcb yalnız footprint görsel kontrolü için test dosyasıdır.')])
build('00_DEGISIKLIK_RAPORU',st)
index=['# Tasarım dokümanları','', '10 Eylül 2026 — Güncel teslim paketi','']
for f in sorted(out.glob('*.pdf')):index.append(f'- [{f.stem}]({f.resolve().as_posix().replace(" ","%20")})')
index+=['','## Açık tasarım konuları','','- IRF7855 / AP33772S gate sürüş uyumluluğu.','- TFT arka ışığı için regüle akım kaynağı.','- Buck L/D ve bias koşulu doğrulanmış MLCC MPN seçimi.','- PCB boş: bakır, RF, ısıl, yerleşim ve DRC doğrulaması yapılmadı.','- Birincil CR2032: RTC trickle charge kapalı olmalı.']
Path('output/TASARIM_RAPORLARI.md').write_text('\n'.join(index),encoding='utf8')
print('Created',len(list(out.glob('*.pdf'))),'PDFs; actual component changes',len(delta))

