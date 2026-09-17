from pathlib import Path
src=Path('reports/output-update/block_reports.py').read_text(encoding='utf8')
src=src.replace("out=Path('output/pdf/bloklar')","out=Path('output/pdf/bloklar-20260911')")
for item in ['after.xml','before.xml','erc.rpt','changes.json','svg']:
 src=src.replace('reports/output-update/'+item,'reports/recheck-20260911/'+item)
src=src.replace("['J4','J5','J6','J7']","['J4','J5','J6']")
src=src.replace('J6/J7 siyah108-0903-001 GND’ye kabloyla bağlanır. Kullanıcının mevcut üçüncü jack’i korundu. Siyah jack’ler','J6 siyah108-0903-001 GND’ye kabloyla bağlanır. Kullanıcı kararıyla yalnız iki jack vardır; J7 yoktur. Siyah jack')
src=src.replace('mevcut J4/J5/J6/J7 üzerinden kırmızı pozitif / iki siyah GND','J4/J5/J6 üzerinden bir kırmızı pozitif / bir siyah GND')
src=src.replace('10.09.2026','11.09.2026').replace('10 Eylül 2026','11 Eylül 2026')
src=src.replace('TASARIM_RAPORLARI.md','TASARIM_RAPORLARI_20260911.md')
src=src.replace('Değişimden sonra açık kalan drain yeniden bağlandı.','Açık kalan drain yeniden bağlandı. Eksik AO3400A footprint kütüphanesi yerine üretici SOT23 paketine uygun standart Package_TO_SOT_SMD:SOT-23 atandı (G1/S2/D3).')
src=src.replace('Hatalar kaynak sürücü tanımları olarak ayrıca listelenmiştir.','Beş hata power_pin_not_driven sınıfındadır. Uyarılar:323 off-grid,6 açık tel ucu,1 kaynaksız BACKLIGHT_3V0,1 encoder kütüphane farkı. Tam konumlar teslim paketindeki ERC raporundadır.')
# Add exact ERC evidence and pin comparison to the documentation, without hiding warnings.
insert="""
st.extend([PageBreak(),para('ERC ve doğrulama kanıtları','h'),para('23 kritik bağlantı grubu netlist üzerinden geçti. Bu sonuç bütün kartın elektriksel performans onayı değildir. Şematik SHA-256 özeti teslim paketinde bulunur.'),para('ERC: 5 power_pin_not_driven hatası; 323 off-grid, 6 açık tel ucu, 1 kaynaksız BACKLIGHT_3V0 ve 1 encoder kütüphane farkı uyarısı. Açık tel ucu uyarılarının tümü giderilmiş kabul edilmedi. PWR_FLAG ile hata gizlenmedi.')])
st.append(para('Güç sürücüsü ERC konumları: U1.24 VCC; #PWR01; #PWR032; U4.6 VBACKUP; U5.9 VIN. Netlist fiziksel besleme yolunu gösterse de ERC kaynak modeli ayrıca tamamlanmalıdır.'))
st.append(para('Açık tel ucu konumları (mm): (71,755;159,385), (86,995;141,605), (118,745;57,150), (143,510;85,725), (143,510;88,265), (258,445;102,235). Ayrıntılar erc.rpt dosyasında.'))
"""
src=src.replace("build('00_DEGISIKLIK_RAPORU',st)",insert+"\nbuild('00_DEGISIKLIK_RAPORU',st)")
Path('reports/recheck-20260911/block_reports.py').write_text(src,encoding='utf8')
exec(compile(src,'block_reports.py','exec'))
