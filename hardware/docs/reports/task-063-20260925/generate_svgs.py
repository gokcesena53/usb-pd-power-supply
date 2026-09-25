import os

REPORT_DIR = "hardware/docs/reports/task-063-20260925"

def generate_svgs():
    # Scale: 1 mm = 8 px, offset X=30 -> 0 px, offset Y=50 -> 0 px
    # Total width = (175 - 30) * 8 = 1160 px, height = (170 - 50) * 8 = 960 px
    sx = lambda x: (x - 30.0) * 8.0
    sy = lambda y: (y - 50.0) * 8.0

    # Before SVG
    svg_before = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 960" width="1160" height="960" style="background:#0f172a; font-family: ui-sans-serif, system-ui, sans-serif;">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" />

  <text x="580" y="40" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">TASK-063 MEKANIK ANKRAJLAR — ÖNCE (BEFORE PLACEMENT)</text>
  <text x="580" y="65" fill="#94a3b8" font-size="13" text-anchor="middle">Portlar ve modüller dağınık veya geçici park alanlarında; mekanik sol panel hizalaması yok</text>

  <!-- PCB Outline -->
  <rect x="{sx(50.3)}" y="{sy(69.48)}" width="{(149.7 - 50.3)*8}" height="{(130.52 - 69.48)*8}" rx="24" ry="24" fill="#064e3b" fill-opacity="0.3" stroke="#10b981" stroke-width="2.5" />
  <text x="{sx(100)}" y="{sy(73)}" fill="#10b981" font-size="12" font-weight="bold" text-anchor="middle">ANA PCB SINIRI (99.40 x 61.04 mm)</text>

  <!-- Mounting Holes -->
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H1</text>

  <circle cx="{sx(145.7)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(145.7)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(145.7)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H2</text>

  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H3</text>

  <circle cx="{sx(145.7)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(145.7)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(145.7)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H4</text>

  <!-- LCD Envelope -->
  <rect x="{sx(63.52)}" y="{sy(72.28)}" width="{(141.62 - 63.52)*8}" height="{(127.72 - 72.28)*8}" fill="#1e293b" fill-opacity="0.5" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="{sx(102.57)}" y="{sy(80)}" fill="#3b82f6" font-size="12" text-anchor="middle">TFT LCD İZDÜŞÜMÜ (Z &lt;= 1.80 mm)</text>

  <!-- J3 FPC -->
  <rect x="{sx(98.0 - 1.5)}" y="{sy(109.3 - 8.0)}" width="{3.0*8}" height="{16.0*8}" fill="#f59e0b" fill-opacity="0.4" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="{sx(98.0)}" y="{sy(109.3)+5}" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">J3 (LCD)</text>

  <!-- C34 Collision with J8 header area -->
  <rect x="{sx(101.0 - 0.5)}" y="{sy(105.55 - 0.5)}" width="{1.0*8}" height="{1.0*8}" fill="#ef4444" stroke="#ef4444" stroke-width="1.5"/>
  <text x="{sx(101.0)}" y="{sy(105.55)-8}" fill="#ef4444" font-size="9" text-anchor="middle">C34 (Çakışma)</text>

  <!-- J7 (Old temporary position outside board: 41.05, 77.32 on B.Cu) -->
  <g transform="translate({sx(41.05)}, {sy(77.32)})">
    <rect x="-35" y="-30" width="70" height="60" fill="#dc2626" fill-opacity="0.3" stroke="#ef4444" stroke-width="2" />
    <text x="0" y="5" fill="#fca5a5" font-size="11" font-weight="bold" text-anchor="middle">J7 (B.Cu)</text>
    <text x="0" y="20" fill="#fca5a5" font-size="9" text-anchor="middle">Geçici Dış Park (41.05)</text>
  </g>

  <!-- J8 (Old parked position: 158.29, 158.23) -->
  <g transform="translate({sx(158.29)}, {sy(158.23)})">
    <rect x="-80" y="-40" width="160" height="80" fill="#dc2626" fill-opacity="0.3" stroke="#ef4444" stroke-width="2" />
    <text x="0" y="5" fill="#fca5a5" font-size="11" font-weight="bold" text-anchor="middle">J8 ETH (B.Cu)</text>
    <text x="0" y="20" fill="#fca5a5" font-size="9" text-anchor="middle">Güneydoğu Park Alanı</text>
  </g>

  <!-- U2 (Old parked position: 160.62, 93.60) -->
  <g transform="translate({sx(160.62)}, {sy(93.60)})">
    <rect x="-40" y="-50" width="80" height="100" fill="#dc2626" fill-opacity="0.3" stroke="#ef4444" stroke-width="2" />
    <text x="0" y="5" fill="#fca5a5" font-size="11" font-weight="bold" text-anchor="middle">U2 ESP32 (B.Cu)</text>
    <text x="0" y="20" fill="#fca5a5" font-size="9" text-anchor="middle">Doğu Park Alanı</text>
  </g>

  <!-- J9 (Old position: 58.00, 91.60) -->
  <g transform="translate({sx(58.0)}, {sy(91.6)})">
    <rect x="-10" y="-70" width="20" height="140" fill="#3b82f6" fill-opacity="0.3" stroke="#60a5fa" stroke-width="1.5" />
    <text x="0" y="0" fill="#93c5fd" font-size="10" font-weight="bold" text-anchor="middle" transform="rotate(-90)">J9 (F.Cu) 91.6mm</text>
  </g>

  <!-- Legend -->
  <rect x="50" y="850" width="450" height="80" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <text x="70" y="875" fill="#f8fafc" font-size="12" font-weight="bold">Önceki Durum Sorunları:</text>
  <text x="70" y="895" fill="#94a3b8" font-size="11">• J7 kart dışı B.Cu'da; J8 güneydoğuda; portlar sol kutu paneline hizalı değil</text>
  <text x="70" y="915" fill="#94a3b8" font-size="11">• U2 B.Cu'da doğu parkında; C34 J8 mezzanine başlığı ile çakışma riski taşıyor</text>
</svg>'''

    # After SVG
    svg_after = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 960" width="1160" height="960" style="background:#0f172a; font-family: ui-sans-serif, system-ui, sans-serif;">
  <defs>
    <pattern id="grid2" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#4ade80" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid2)" />

  <text x="580" y="40" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">TASK-063 MEKANIK ANKRAJLAR — SONRA (FINAL APPROVED ANCHORS)</text>
  <text x="580" y="65" fill="#4ade80" font-size="13" text-anchor="middle">J7 USB-C Top, J8 ETH Bottom, U2 Kuzeybatı Anten Dışarı, J9 Kablo Koridoru, 0 DRC Hatası</text>

  <!-- PCB Outline -->
  <rect x="{sx(50.3)}" y="{sy(69.48)}" width="{(149.7 - 50.3)*8}" height="{(130.52 - 69.48)*8}" rx="24" ry="24" fill="#064e3b" fill-opacity="0.3" stroke="#10b981" stroke-width="2.5" />
  <text x="{sx(100)}" y="{sy(71.5)}" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">KUZEY KENAR (Y = 69.48 mm)</text>
  <text x="{sx(49.0)}" y="{sy(100)}" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle" transform="rotate(-90 {sx(49.0)} {sy(100)})">SOL KENAR (X = 50.30 mm)</text>

  <!-- Mounting Holes -->
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H1</text>

  <circle cx="{sx(145.7)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(145.7)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(145.7)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H2</text>

  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H3</text>

  <circle cx="{sx(145.7)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(145.7)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(145.7)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H4</text>

  <!-- LCD Envelope -->
  <rect x="{sx(63.52)}" y="{sy(72.28)}" width="{(141.62 - 63.52)*8}" height="{(127.72 - 72.28)*8}" fill="#1e293b" fill-opacity="0.3" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="{sx(102.57)}" y="{sy(78)}" fill="#3b82f6" font-size="12" text-anchor="middle">TFT LCD İZDÜŞÜMÜ (Z &lt;= 1.80 mm)</text>

  <!-- J3 FPC -->
  <rect x="{sx(98.0 - 1.5)}" y="{sy(109.3 - 8.0)}" width="{3.0*8}" height="{16.0*8}" fill="#f59e0b" fill-opacity="0.3" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="{sx(98.0)}" y="{sy(109.3)+5}" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">J3 (LCD)</text>

  <!-- C34 Relocated -->
  <rect x="{sx(104.8 - 0.5)}" y="{sy(105.55 - 0.5)}" width="{1.0*8}" height="{1.0*8}" fill="#10b981" stroke="#10b981" stroke-width="1.5"/>
  <text x="{sx(104.8)}" y="{sy(105.55)-8}" fill="#10b981" font-size="9" text-anchor="middle">C34 (104.8, 105.55)</text>

  <!-- U2 ESP32-C6 (78.0, 75.6 on F.Cu, rot 0) -->
  <g transform="translate({sx(78.0)}, {sy(75.6)})">
    <!-- Antenna Keepout outside board -->
    <rect x="{-6.6*8}" y="{-11.0*8}" width="{13.2*8}" height="{5.12*8}" fill="#ef4444" fill-opacity="0.25" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,4"/>
    <text x="0" y="{-8.0*8}" fill="#fca5a5" font-size="9" font-weight="bold" text-anchor="middle">RF ANTEN (Dışarıda: 4.88mm)</text>
    <!-- Module Body -->
    <rect x="{-6.6*8}" y="{-5.88*8}" width="{13.2*8}" height="{11.5*8}" fill="#0284c7" fill-opacity="0.5" stroke="#38bdf8" stroke-width="2"/>
    <text x="0" y="0" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">U2 ESP32-C6</text>
    <text x="0" y="16" fill="#e0f2fe" font-size="9" text-anchor="middle">F.Cu (78.0, 75.6)</text>
  </g>

  <!-- J7 USB-C (53.975, 82.5 on F.Cu, rot 270) -->
  <g transform="translate({sx(53.975)}, {sy(82.5)})">
    <!-- Front nose overhang past X=50.30 -->
    <rect x="{-4.2*8}" y="{-4.5*8}" width="{0.53*8}" height="{9.0*8}" fill="#f59e0b" fill-opacity="0.6" stroke="#f59e0b" stroke-width="1"/>
    <!-- Body -->
    <rect x="{-3.675*8}" y="{-4.5*8}" width="{8.5*8}" height="{9.0*8}" fill="#0284c7" fill-opacity="0.5" stroke="#38bdf8" stroke-width="2"/>
    <text x="{0}" y="2" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">J7 USB-C</text>
    <text x="{0}" y="15" fill="#e0f2fe" font-size="9" text-anchor="middle">F.Cu (53.98, 82.5)</text>
  </g>

  <!-- J9 Encoder (58.0, 90.0 on F.Cu, rot -90) -->
  <g transform="translate({sx(58.0)}, {sy(90.0)})">
    <rect x="{-1.4*8}" y="{-3.0*8}" width="{2.8*8}" height="{20.5*8}" fill="#8b5cf6" fill-opacity="0.5" stroke="#a78bfa" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{4.2*8}" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{8.4*8}" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{12.6*8}" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{16.8*8}" r="5" fill="#f8fafc"/>
    <text x="25" y="{8.4*8}" fill="#c4b5fd" font-size="10" font-weight="bold" text-anchor="start">J9 (5P Enkoder)</text>
  </g>

  <!-- J8 Mezzanine (102.5, 102.0 on B.Cu, rot 0) -->
  <g transform="translate({sx(102.5)}, {sy(102.0)})">
    <!-- Mezzanine PCB body outline -->
    <rect x="{-55.5*8}" y="{-2.2*8}" width="{58.0*8}" height="{22.2*8}" rx="8" ry="8" fill="#475569" fill-opacity="0.3" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
    <!-- RJ45 Jack body on West -->
    <rect x="{-55.5*8}" y="{0.84*8}" width="{22.0*8}" height="{16.1*8}" fill="#0d9488" fill-opacity="0.6" stroke="#2dd4bf" stroke-width="2"/>
    <text x="{-44.5*8}" y="{8.89*8}" fill="#ccfbf1" font-size="11" font-weight="bold" text-anchor="middle">RJ45 Port</text>
    <text x="{-44.5*8}" y="{8.89*8 + 15}" fill="#ccfbf1" font-size="9" text-anchor="middle">3.3mm Taşma</text>
    <!-- Header pins on East -->
    <rect x="{-2.54*8 - 6}" y="-6" width="{2.54*8 + 12}" height="{17.78*8 + 12}" fill="#334155" stroke="#cbd5e1" stroke-width="1"/>
    <text x="{-10}" y="{9.0*8}" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="end">J8 Mezzanine</text>
  </g>

  <!-- Plug Clearance Annotation -->
  <line x1="{sx(46.0)}" y1="{sy(82.5)}" x2="{sx(46.0)}" y2="{sy(110.89)}" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <rect x="{sx(34.0)}" y="{sy(93.0)}" width="115" height="35" rx="4" fill="#0369a1" stroke="#38bdf8" stroke-width="1"/>
  <text x="{sx(34.0)+57}" y="{sy(93.0)+15}" fill="#f0f9ff" font-size="10" font-weight="bold" text-anchor="middle">Fiş Açıklığı</text>
  <text x="{sx(34.0)+57}" y="{sy(93.0)+28}" fill="#f0f9ff" font-size="9" text-anchor="middle">14.39 mm &gt;&gt; 2mm</text>

  <!-- USB D+/D- route annotation -->
  <path d="M {sx(57.65)} {sy(82.5)} Q {sx(68)} {sy(80)} {sx(78.0)} {sy(78.0)}" fill="none" stroke="#4ade80" stroke-width="2" stroke-dasharray="4,2" marker-end="url(#arrow-green)"/>
  <text x="{sx(68)}" y="{sy(84)}" fill="#4ade80" font-size="9" font-weight="bold">USB 2.0 (~25mm)</text>

  <!-- J9 to Front Panel Cable Exit Corridor -->
  <path d="M {sx(58.0)} {sy(98.0)} L {sx(48.0)} {sy(98.0)}" stroke="#a78bfa" stroke-width="2" stroke-dasharray="3,3"/>
  <text x="{sx(48.0)}" y="{sy(96.0)}" fill="#c4b5fd" font-size="9" text-anchor="end">Enkoder Kablo Çıkışı</text>

  <!-- Legend -->
  <rect x="50" y="850" width="700" height="85" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <text x="70" y="873" fill="#f8fafc" font-size="12" font-weight="bold">TASK-063 Doğrulama Kanıtları:</text>
  <text x="70" y="892" fill="#94a3b8" font-size="11">• J7 F.Cu (53.98, 82.50) sol kenar 0.00mm hata ile hizalı; J8 B.Cu (102.50, 102.00) RJ45 ağzı West</text>
  <text x="70" y="908" fill="#94a3b8" font-size="11">• Fiş açıklığı 14.39 mm &gt;= 2.0 mm; U2 F.Cu (78.0, 75.6) anteni 4.88mm kuzeye açık alana uzanır</text>
  <text x="70" y="924" fill="#94a3b8" font-size="11">• J9 F.Cu (58.0, 90.0) LCD mesafesi 5.52mm; C34 (104.8, 105.55) taşındı; DRC Error 0, Parity 0</text>
</svg>'''

    with open(os.path.join(REPORT_DIR, "before.svg"), "w", encoding="utf-8") as f:
        f.write(svg_before)

    with open(os.path.join(REPORT_DIR, "after.svg"), "w", encoding="utf-8") as f:
        f.write(svg_after)

    print("Generated before.svg and after.svg successfully.")

if __name__ == "__main__":
    generate_svgs()
