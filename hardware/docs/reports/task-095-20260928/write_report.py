from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
v=json.loads((D/'verification.json').read_text());s=json.loads((D/'solid-check.json').read_text());p=json.loads((D/'placement.json').read_text())
lines=['# TASK-095 — Kart dışında bekleyen blokların yeniden yerleşimi','',
'28.09.2026: TASK-094 sonrasında park edilmiş 26 komponent ana PCB içine alındı. AP33772S bloğu 23, encoder pull-up bloğu 3 üyedir. Geçici park alanında elektriksel komponent kalmadı. Panel encoder mekanik modeli kart dışında kalması gereken panel parçasıdır.', '',
'## Yerleşim kararı','',
'AP33772S bloğu B.Cu üzerinde encoder kablo hacmi ile TPS55340 boost bölgesi arasına yerleştirildi. R11 giriş şöntü Ethernet modülünün güneyinde; Q3 onun güneyinde; C3 giriş tarafında, C8 Q3 çıkışı ile boost girişi arasında. U1 ve bypass/filtre elemanları Q3 altında, bölücü ve gösterge elemanları kartın güney kenarındadır. TH1 güç MOSFET yakınında kaldı. R34–R36, J9 altında Y=125,5 mm üzerinde 2,5 mm adımla sıralandı.', '',
'Tüm 26 parça B.Cu yüzünde kaldı; yeni çift yüzlü güç döngüsü oluşturulmadı. C8 0 dereceye, R34–R36 ortak 90 dereceye getirildi. Yeni dar alana uyarlamak için blok içi koordinatlar yeniden düzenlendi; grup üyeliği ve pad-net eşleşmeleri korundu.', '',
'J7 USB, J8 Ethernet, J9, MECH_ENC, J3/FPC, H1–H4 ve diğer footprint konumları/açıları/yüzleri korunmuştur. Edge.Cuts ve tasarım kuralları değişmedi. Yalnız J8 referans yazısı yeni R11 ile çakışmaması için taşındı; Q3/R11/R64/R65 referansları da yeni konumlara uyarlandı.', '',
'## Son koordinatlar','', '| Ref | X (mm) | Y (mm) | Açı | Yüz |','|---|---:|---:|---:|---|']
for r in sorted(p['targets']):
 f=p['after'][r];lines.append(f"| {r} | {f['xy'][0]:.3f} | {f['xy'][1]:.3f} | {f['angle']:.0f}° | {f['layer']} |")
lines+=['','## Elektriksel yerleşim ve routing devri','',
'Aşağıdaki değerler pad merkezleri arasındaki düz mesafedir; bitmiş iz uzunluğu veya elektriksel performans ölçümü değildir.', '',
'| Bağlantı | Mesafe (mm) |','|---|---:|']
for k,d in v['pin_center_distances_mm'].items():lines.append(f'| {k} | {d:.3f} |')
lines+=['',
'TASK-087 için güç akışı J7 → R11 → Q3 → C8 → boost girişidir. R11 iki ucundan U1 algılama pinlerine bağımsız Kelvin bağlantıları çekilmeli; algılama izleri yüksek akım bakırından ayrılmalıdır. U1 CC1/CC2 hatları J7/ESD yönüne sol-kuzey koridorundan götürülmeli. C4/V5V, C1/V18 ve C2/IFB pin bağlantıları en kısa doğrudan rotalarla ve yakın GND dönüşüyle tamamlanmalı. Q3 gate yolu R12 üzerinden, güç/SW bakırından uzak tutulmalı. R34–R36 +3.3V ortak beslemesi ve encoder sinyalleri J9 yönüne çıkarılmalı.', '',
'Mevcut dört D5–U11 FB iz segmentinin UUID, koordinat, genişlik ve netleri değişmedi. Diğer bağlantılar henüz route edilmemiştir; 360 bağlantısız öğe TASK-087 işidir.', '',
'## Mekanik ve DRC doğrulaması','',
'Encoder/J9 alt yüz kablo hacmi PCB X=57,8..70, Y=102..123, STEP Z=−17..−0,5 mm olarak korundu. Taşınan modeller bu hacme, encoder modeline ve sabit tüm komponent modellerine karşı kontrol edildi. Taşınan modellerin kendi aralarındaki katı kesişimleri de denetlendi.', '',
f"- Taşınan 21 modelli parçanın sabit modellerle en büyük kesişim hacmi: **{s['max_stationary_intersection']:.6f} mm³**; kendi aralarında çakışma: **{len(s['pair_intersections'])}**. Beş test noktası düz PCB pedidir, ayrı yükseltilmiş katı modeli yoktur.",
f"- Kablo servis hacmine minimum model mesafesi: **{s['minimum_cable_clearance']:.3f} mm**.",
f"- Encoder modeline minimum mesafe: **{s['minimum_encoder_clearance']:.3f} mm**.",
'- Taşınan 26 footprint’in tüm pad merkezleri kapalı kart poligonunun içinde; DRC pad kenarı/bakır açıklıklarını denetledi. Yalnız pad merkezine bakılarak kenar uygunluğu iddia edilmedi.',
'- Sol kenarda en az 0,254 mm ve mevcut daha sıkı genel 0,500 mm kuralı korundu; J9 ve yeni sol kenar değişmedi.',
f"- DRC hata **{v['baseline_errors']} → {v['final_errors']}**, uyarı **{v['baseline_warnings']} → {v['final_warnings']}**; yeni ihlal **{len(v['new_violations'])}**. Mevcut 15 hata U2 kart kenarı ihlalleridir.",
f"- Şematik parite farkı **{v['schematic_parity']}**; bağlantısız öğe **{v['unconnected_before']} → {v['unconnected_after']}**.",
'- Üst/alt SVG katmanları ve 3D renderleri kontrol edildi.', '',
'Model kontrolü nominal geometriler içindir; gerçek lehim çıkıntıları, Ethernet model toleransı, kablo demeti ve kutu/fiş kabulü önceki numune görevlerinde sürer. Bu yerleşim tamamlanması genel routing veya üretim kabulü değildir.', '',
'## Kanıtlar','',
'- [Son alt yüz 3D](../../hardware/docs/reports/task-095-20260928/bottom.png)',
'- [Son üst yüz 3D](../../hardware/docs/reports/task-095-20260928/top.png)',
'- [Sayısal doğrulama](../../hardware/docs/reports/task-095-20260928/verification.json)',
'- [Katı kontrolü](../../hardware/docs/reports/task-095-20260928/solid-check.json)',
'- [Önce/sonra koordinatlar](../../hardware/docs/reports/task-095-20260928/placement.json)',
'- [Son DRC](../../hardware/docs/reports/task-095-20260928/final-drc.json)', '',
f"Doğrulanan PCB SHA256: `{v['board_sha256']}`. Başlangıç yedekleri ve tekrar üretim betikleri aynı rapor dizinindedir."]
(ROOT/'design_decisions/output/KART_DISI_BLOKLAR_YERLESIM_TASK095_20260928.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
