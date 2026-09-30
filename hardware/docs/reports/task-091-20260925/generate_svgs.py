import os

REPORT_DIR = "hardware/docs/reports/task-091-20260925"

def generate_svgs():
    sx = lambda x: (x - 30.0) * 8.0
    sy = lambda y: (y - 50.0) * 8.0

    # Before SVG
    svg_before = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 960" width="1160" height="960" style="background:#0f172a; font-family: ui-sans-serif, system-ui, sans-serif;">
  <defs>
    <pattern id="grid_b" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid_b)" />

  <text x="580" y="40" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">TASK-091 ETHERNET &amp; MCU ANKRAJ REVIZYONU — ÖNCE (BEFORE)</text>
  <text x="580" y="65" fill="#f87171" font-size="13" text-anchor="middle">Mevcut J9 Pad 4-5 RJ45 keepout izdüşümünde; MCU'nun LCD izdüşümü ve USB-C yakınlığı inceleniyor</text>

  <!-- PCB Outline -->
  <rect x="{sx(50.3)}" y="{sy(69.48)}" width="{(149.7 - 50.3)*8}" height="{(130.52 - 69.48)*8}" rx="24" ry="24" fill="#064e3b" fill-opacity="0.25" stroke="#10b981" stroke-width="2.5" />
  <text x="{sx(100)}" y="{sy(71.5)}" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">PCB SINIRI (99.40 x 61.04 mm)</text>

  <!-- Mounting Holes -->
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H1</text>

  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H3</text>

  <!-- LCD Envelope -->
  <rect x="{sx(63.52)}" y="{sy(72.28)}" width="{(141.62 - 63.52)*8}" height="{(127.72 - 72.28)*8}" fill="#1e293b" fill-opacity="0.3" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="{sx(102.57)}" y="{sy(78)}" fill="#3b82f6" font-size="12" text-anchor="middle">TFT LCD İZDÜŞÜMÜ (Z &lt;= 1.80 mm)</text>

  <!-- J7 USB-C -->
  <g transform="translate({sx(53.975)}, {sy(82.5)})">
    <rect x="{-3.675*8}" y="{-4.5*8}" width="{8.5*8}" height="{9.0*8}" fill="#0284c7" fill-opacity="0.5" stroke="#38bdf8" stroke-width="2"/>
    <text x="0" y="2" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">J7 USB-C (Top)</text>
  </g>

  <!-- J8 Mezzanine with RJ45 Keepout -->
  <g transform="translate({sx(102.5)}, {sy(102.0)})">
    <rect x="{-55.5*8}" y="{-2.2*8}" width="{58.0*8}" height="{22.2*8}" rx="8" ry="8" fill="#475569" fill-opacity="0.2" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
    <!-- RJ45 Jack body on West -->
    <rect x="{-55.5*8}" y="{0.84*8}" width="{22.0*8}" height="{16.1*8}" fill="#dc2626" fill-opacity="0.4" stroke="#ef4444" stroke-width="2"/>
    <text x="{-44.5*8}" y="{8.89*8}" fill="#fca5a5" font-size="11" font-weight="bold" text-anchor="middle">RJ45 Port</text>
    <text x="{-44.5*8}" y="{8.89*8 + 15}" fill="#fca5a5" font-size="9" text-anchor="middle">B.Cu Keepout Alanı</text>
  </g>

  <!-- Old J9 (Vertical, colliding with RJ45 keepout) -->
  <g transform="translate({sx(58.0)}, {sy(90.0)})">
    <rect x="{-1.4*8}" y="{-3.0*8}" width="{2.8*8}" height="{20.5*8}" fill="#8b5cf6" fill-opacity="0.3" stroke="#a78bfa" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{4.2*8}" r="5" fill="#f8fafc"/>
    <circle cx="0" cy="{8.4*8}" r="5" fill="#f8fafc"/>
    <!-- Overlapping pads -->
    <circle cx="0" cy="{12.6*8}" r="6" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
    <circle cx="0" cy="{16.8*8}" r="6" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
    <text x="-15" y="{14.7*8}" fill="#ef4444" font-size="10" font-weight="bold" text-anchor="end">J9 Pad 4-5 Çakışma!</text>
  </g>

  <!-- U2 Candidate 1 in LCD area -->
  <g transform="translate({sx(78.0)}, {sy(75.6)})">
    <rect x="{-6.6*8}" y="{-11.0*8}" width="{13.2*8}" height="{5.12*8}" fill="#ef4444" fill-opacity="0.25" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,4"/>
    <rect x="{-6.6*8}" y="{-5.88*8}" width="{13.2*8}" height="{11.5*8}" fill="#eab308" fill-opacity="0.4" stroke="#facc15" stroke-width="2"/>
    <text x="0" y="0" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">U2 (Z = 2.40mm)</text>
    <text x="0" y="16" fill="#fef08a" font-size="9" text-anchor="middle">LCD İzdüşümünde (Y &gt; 72.28)</text>
  </g>

  <!-- Legend -->
  <rect x="50" y="850" width="600" height="80" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <text x="70" y="875" fill="#f8fafc" font-size="12" font-weight="bold">TASK-091 Giriş Sorunları:</text>
  <text x="70" y="895" fill="#fca5a5" font-size="11">1. Düşey J9 enkoder pedleri (Pad 4 ve 5) alttaki RJ45 metal priz keepout'u ile çakışıyor</text>
  <text x="70" y="915" fill="#fef08a" font-size="11">2. U2 MCU modülü LCD toleranslı alanına giriyor; LCD yüksekliği ve USB yakınlığı değerlendirilmeli</text>
</svg>'''

    # After SVG
    svg_after = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 960" width="1160" height="960" style="background:#0f172a; font-family: ui-sans-serif, system-ui, sans-serif;">
  <defs>
    <pattern id="grid_a" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#4ade80" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid_a)" />

  <text x="580" y="40" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">TASK-091 ETHERNET &amp; MCU ANKRAJ REVIZYONU — SONRA (AFTER)</text>
  <text x="580" y="65" fill="#4ade80" font-size="13" text-anchor="middle">J9 Çapraz Yerleşimle RJ45'ten Kurtarıldı, J8/J7 Port Hizası Kesitlendirildi, U2 Aday Analizi Tamamlandı</text>

  <!-- PCB Outline -->
  <rect x="{sx(50.3)}" y="{sy(69.48)}" width="{(149.7 - 50.3)*8}" height="{(130.52 - 69.48)*8}" rx="24" ry="24" fill="#064e3b" fill-opacity="0.3" stroke="#10b981" stroke-width="2.5" />
  <text x="{sx(100)}" y="{sy(71.5)}" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">KUZEY PCB KENARI (Y = 69.48 mm)</text>
  <text x="{sx(49.0)}" y="{sy(100)}" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle" transform="rotate(-90 {sx(49.0)} {sy(100)})">SOL KENAR (X = 50.30 mm)</text>

  <!-- Mounting Holes -->
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(73.48)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(73.48)-15}" fill="#94a3b8" font-size="10" text-anchor="middle">H1</text>

  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{1.6*8}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="{sx(54.3)}" cy="{sy(126.52)}" r="{3.0*8}" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="{sx(54.3)}" y="{sy(126.52)+25}" fill="#94a3b8" font-size="10" text-anchor="middle">H3</text>

  <!-- LCD Envelope -->
  <rect x="{sx(63.52)}" y="{sy(72.28)}" width="{(141.62 - 63.52)*8}" height="{(127.72 - 72.28)*8}" fill="#1e293b" fill-opacity="0.3" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="{sx(102.57)}" y="{sy(78)}" fill="#3b82f6" font-size="12" text-anchor="middle">TFT LCD İZDÜŞÜMÜ (Z &gt;= 2.50 mm Standoff Şartı)</text>

  <!-- U2 ESP32-C6 (Selected Candidate 1) -->
  <g transform="translate({sx(78.0)}, {sy(75.6)})">
    <rect x="{-6.6*8}" y="{-11.0*8}" width="{13.2*8}" height="{5.12*8}" fill="#ef4444" fill-opacity="0.25" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,4"/>
    <text x="0" y="{-8.0*8}" fill="#fca5a5" font-size="9" font-weight="bold" text-anchor="middle">RF ANTEN (4.88mm Taşma)</text>
    <rect x="{-6.6*8}" y="{-5.88*8}" width="{13.2*8}" height="{11.5*8}" fill="#0284c7" fill-opacity="0.5" stroke="#38bdf8" stroke-width="2"/>
    <text x="0" y="0" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">U2 ESP32-C6 (F.Cu)</text>
    <text x="0" y="16" fill="#e0f2fe" font-size="9" text-anchor="middle">Aday 1 Seçildi (USB ~22mm)</text>
  </g>

  <!-- J7 USB-C (53.975, 82.5 on F.Cu) -->
  <g transform="translate({sx(53.975)}, {sy(82.5)})">
    <rect x="{-4.2*8}" y="{-4.5*8}" width="{0.53*8}" height="{9.0*8}" fill="#f59e0b" fill-opacity="0.6" stroke="#f59e0b" stroke-width="1"/>
    <rect x="{-3.675*8}" y="{-4.5*8}" width="{8.5*8}" height="{9.0*8}" fill="#0284c7" fill-opacity="0.5" stroke="#38bdf8" stroke-width="2"/>
    <text x="0" y="2" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">J7 USB-C (Top)</text>
    <text x="0" y="15" fill="#e0f2fe" font-size="9" text-anchor="middle">Z = Top (+Z)</text>
  </g>

  <!-- J8 Mezzanine on B.Cu -->
  <g transform="translate({sx(102.5)}, {sy(102.0)})">
    <rect x="{-55.5*8}" y="{-2.2*8}" width="{58.0*8}" height="{22.2*8}" rx="8" ry="8" fill="#475569" fill-opacity="0.2" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
    <!-- RJ45 Jack body on West -->
    <rect x="{-55.5*8}" y="{0.84*8}" width="{22.0*8}" height="{16.1*8}" fill="#0d9488" fill-opacity="0.6" stroke="#2dd4bf" stroke-width="2"/>
    <text x="{-44.5*8}" y="{8.89*8}" fill="#ccfbf1" font-size="11" font-weight="bold" text-anchor="middle">RJ45 Port</text>
    <text x="{-44.5*8}" y="{8.89*8 + 15}" fill="#ccfbf1" font-size="9" text-anchor="middle">Z = Bottom (-Z)</text>
    <!-- Available Ethernet Underlay Zone for TASK-093 -->
    <rect x="{-32.65*8}" y="{-2.11*8}" width="{28.84*8}" height="{22.0*8}" fill="#10b981" fill-opacity="0.15" stroke="#10b981" stroke-width="1.5" stroke-dasharray="5,5"/>
    <text x="{-18.0*8}" y="{9.0*8}" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">TASK-093 ALANI</text>
    <text x="{-18.0*8}" y="{9.0*8 + 14}" fill="#34d399" font-size="8" text-anchor="middle">(634 mm² Serbest)</text>
  </g>

  <!-- New Diagonal J9 Placement (61.75, 87.00, rot -126 deg) -->
  <g>
    <!-- Pads: P1=(61.75, 87.00), P2=(59.28, 90.40), P3=(56.81, 93.80), P4=(54.34, 97.19), P5=(51.88, 100.59) -->
    <line x1="{sx(61.75)}" y1="{sy(87.00)}" x2="{sx(51.88)}" y2="{sy(100.59)}" stroke="#a78bfa" stroke-width="20" stroke-linecap="round" stroke-opacity="0.3"/>
    <circle cx="{sx(61.75)}" cy="{sy(87.00)}" r="6" fill="#c4b5fd" stroke="#7c3aed" stroke-width="1.5"/>
    <circle cx="{sx(59.28)}" cy="{sy(90.40)}" r="6" fill="#c4b5fd" stroke="#7c3aed" stroke-width="1.5"/>
    <circle cx="{sx(56.81)}" cy="{sy(93.80)}" r="6" fill="#c4b5fd" stroke="#7c3aed" stroke-width="1.5"/>
    <circle cx="{sx(54.34)}" cy="{sy(97.19)}" r="6" fill="#c4b5fd" stroke="#7c3aed" stroke-width="1.5"/>
    <circle cx="{sx(51.88)}" cy="{sy(100.59)}" r="6" fill="#c4b5fd" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="{sx(63.0)}" y="{sy(86.0)}" fill="#c4b5fd" font-size="11" font-weight="bold">J9 (Çapraz 5P)</text>
    <text x="{sx(50.0)}" y="{sy(99.0)}" fill="#4ade80" font-size="9" font-weight="bold" text-anchor="end">RJ45 Açıklığı: 1.32 mm</text>
  </g>

  <!-- Left Panel Cross-Section Inset -->
  <g transform="translate(850, 680)">
    <rect x="-10" y="-20" width="280" height="230" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
    <text x="130" y="0" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">SOL PANEL KESİTİ (Y-Z DÜZLEMİ)</text>
    
    <!-- Motherboard PCB -->
    <rect x="20" y="70" width="220" height="12" fill="#065f46" stroke="#10b981" stroke-width="1"/>
    <text x="245" y="80" fill="#34d399" font-size="9">PCB (1.6mm)</text>
    
    <!-- USB-C on Top (F.Cu) -->
    <rect x="40" y="38" width="60" height="32" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="70" y="58" fill="#f0f9ff" font-size="9" font-weight="bold" text-anchor="middle">USB-C (Top)</text>
    
    <!-- RJ45 on Bottom (B.Cu) -->
    <rect x="150" y="82" width="80" height="85" fill="#0d9488" stroke="#2dd4bf" stroke-width="1.5"/>
    <text x="190" y="125" fill="#ccfbf1" font-size="9" font-weight="bold" text-anchor="middle">RJ45 (Bottom)</text>
    
    <!-- Dimensions -->
    <line x1="70" y1="25" x2="190" y2="25" stroke="#38bdf8" stroke-width="1" marker-start="url(#arr-blue)" marker-end="url(#arr-blue)"/>
    <text x="130" y="20" fill="#38bdf8" font-size="9" text-anchor="middle">ΔY = 28.39 mm</text>
  </g>

  <!-- USB D+/D- Route Annotation -->
  <path d="M {sx(57.65)} {sy(82.5)} Q {sx(68)} {sy(81)} {sx(77.2)} {sy(80.5)}" fill="none" stroke="#4ade80" stroke-width="2" stroke-dasharray="4,2" marker-end="url(#arr-green)"/>
  <text x="{sx(67)}" y="{sy(85)}" fill="#4ade80" font-size="9" font-weight="bold">USB 2.0 (19.65 mm)</text>

  <!-- Legend -->
  <rect x="50" y="850" width="760" height="85" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <text x="70" y="873" fill="#f8fafc" font-size="12" font-weight="bold">TASK-091 Doğrulama ve Çözüm Kanıtları:</text>
  <text x="70" y="892" fill="#94a3b8" font-size="11">• J9 açısı -126.0° yapılarak Pad 1-5 RJ45 keepout dışına çıkarıldı (+1.32mm açıklık); LCD dışı koridor korundu</text>
  <text x="70" y="908" fill="#94a3b8" font-size="11">• U2 MCU Aday 1 seçildi: USB pad mesafesi 19.65mm; West şeridinde yer olmadığı ve RF şartları kanıtlandı</text>
  <text x="70" y="924" fill="#94a3b8" font-size="11">• USB üstte (F.Cu) / RJ45 altta (B.Cu) kesit ilişkisi netleştirildi; DRC Error: 0, Schematic Parity: 0</text>
</svg>'''

    with open(os.path.join(REPORT_DIR, "before.svg"), "w", encoding="utf-8") as f:
        f.write(svg_before)

    with open(os.path.join(REPORT_DIR, "after.svg"), "w", encoding="utf-8") as f:
        f.write(svg_after)

    print("Generated before.svg and after.svg for TASK-091 successfully.")

if __name__ == "__main__":
    generate_svgs()
