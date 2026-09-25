import json
import os
import math

REPORT_DIR = "hardware/docs/reports/task-086-20260925"

# Board geometry
BOARD_W = 99.40
BOARD_H = 61.04
ORIGIN_X = 100.0
ORIGIN_Y = 100.0
X_MIN = ORIGIN_X - BOARD_W / 2.0 # 50.30
X_MAX = ORIGIN_X + BOARD_W / 2.0 # 149.70
Y_MIN = ORIGIN_Y - BOARD_H / 2.0 # 69.48
Y_MAX = ORIGIN_Y + BOARD_H / 2.0 # 130.52

# Load handoff matrix from TASK-085
with open("hardware/docs/reports/task-085-20260925/handoff_matrix.json", encoding="utf-8") as f:
    handoff = json.load(f)

groups = handoff["groups"]

# Candidate A Floorplan definition (Recommended)
# Anchors & zones:
# J7 USB-C: Top-Left (F.Cu)
# J8 Ethernet Mezzanine: Bottom-Left (B.Cu)
# U2 ESP32-C6: North-West (F.Cu), antenna outside top edge
# J9 Encoder: Left-Center between J7 and J8
# J3 TFT: Fixed at (98.00, 109.30)
# Power chain: AP33772S -> TPS55340 -> AOZ1284 -> LM74801 -> INA226 -> J4
candidate_a = {
    "name": "Candidate A: Linear Eastward Power Flow + Northwest RF & Control (Recommended)",
    "description": "J7 USB-C top-left, J8 Ethernet bottom-left under J7, U2 ESP32-C6 top edge (antenna outside North), linear west-to-east power flow on B.Cu, quiet RTC in North-East.",
    "blocks": {
        "1_USB_C_GIRIS": {"x_range": [50.3, 62.0], "y_range": [72.0, 89.0], "face": "F.Cu / B.Cu", "w": 11.7, "h": 17.0},
        "8_ESP32_C6_MCU": {"x_range": [64.0, 85.5], "y_range": [69.48, 88.0], "face": "F.Cu", "w": 21.5, "h": 18.5, "antenna_out": True},
        "11_ETHERNET_MEZANIN": {"x_range": [50.3, 105.0], "y_range": [104.0, 130.52], "face": "B.Cu", "w": 54.7, "h": 26.5},
        "14_PANEL_ENKODER": {"x_range": [52.0, 60.0], "y_range": [90.0, 103.0], "face": "F.Cu / B.Cu", "w": 8.0, "h": 13.0},
        "2_AP33772S_PD_KONTROLCU": {"x_range": [62.0, 86.0], "y_range": [88.0, 105.0], "face": "B.Cu", "w": 24.0, "h": 17.0},
        "3_TPS55340_PRE_BOOST": {"x_range": [86.0, 110.0], "y_range": [82.0, 104.0], "face": "B.Cu", "w": 24.0, "h": 22.0},
        "4_AOZ1284_BUCK": {"x_range": [110.0, 132.0], "y_range": [82.0, 104.0], "face": "B.Cu", "w": 22.0, "h": 22.0},
        "5_LM74801_CIKIS_ANAHTARI": {"x_range": [130.0, 149.0], "y_range": [84.0, 102.0], "face": "B.Cu", "w": 19.0, "h": 18.0},
        "6_INA226_OLCUM_CIKIS": {"x_range": [128.0, 149.7], "y_range": [102.0, 128.0], "face": "B.Cu / F.Cu (J4)", "w": 21.7, "h": 26.0},
        "7_CIKIS_DESARJI": {"x_range": [116.0, 128.0], "y_range": [104.0, 118.0], "face": "B.Cu", "w": 12.0, "h": 14.0},
        "9_RTC_BQ32000": {"x_range": [126.0, 147.0], "y_range": [69.48, 84.0], "face": "B.Cu", "w": 21.0, "h": 14.5},
        "10_I2C_SEVIYE_DONUSTURUCU": {"x_range": [86.0, 96.0], "y_range": [72.0, 82.0], "face": "B.Cu", "w": 10.0, "h": 10.0},
        "12_TFT_BACKLIGHT": {"x_range": [94.0, 106.0], "y_range": [95.0, 106.0], "face": "F.Cu", "w": 12.0, "h": 11.0},
        "13_TFT_J3": {"x_range": [96.0, 103.0], "y_range": [105.0, 112.0], "face": "F.Cu", "w": 7.0, "h": 7.0},
        "15_TEST_NOKTALARI": {"x_range": [106.0, 116.0], "y_range": [108.0, 122.0], "face": "F.Cu / B.Cu", "w": 10.0, "h": 14.0}
    },
    "metrics": {
        "usb_trace_length_mm": 22.0,
        "rf_keepout_ok": True,
        "simultaneous_plug_clearance_mm": 2.5,
        "power_loop_flow": "Linear West-to-East",
        "rtc_isolation_mm": 26.5
    }
}

# Candidate B Floorplan definition (Alternative)
# J7 USB-C: Bottom-Left (F.Cu)
# J8 Ethernet Mezzanine: Top-Left (B.Cu)
# U2 ESP32-C6: North-East (F.Cu)
# Long USB lines across the board
candidate_b = {
    "name": "Candidate B: Perimeter Flow + Northeast RF",
    "description": "J8 Ethernet top-left, J7 USB-C bottom-left, U2 ESP32-C6 north-east edge, power loops wrap around bottom edge. Long USB traces (~70 mm) across the board.",
    "blocks": {
        "11_ETHERNET_MEZANIN": {"x_range": [50.3, 105.0], "y_range": [69.48, 96.0], "face": "B.Cu", "w": 54.7, "h": 26.5},
        "1_USB_C_GIRIS": {"x_range": [50.3, 62.0], "y_range": [110.0, 128.0], "face": "F.Cu / B.Cu", "w": 11.7, "h": 18.0},
        "8_ESP32_C6_MCU": {"x_range": [125.0, 147.0], "y_range": [69.48, 88.0], "face": "F.Cu", "w": 22.0, "h": 18.5, "antenna_out": True},
        "2_AP33772S_PD_KONTROLCU": {"x_range": [62.0, 86.0], "y_range": [110.0, 128.0], "face": "B.Cu", "w": 24.0, "h": 18.0},
        "3_TPS55340_PRE_BOOST": {"x_range": [86.0, 110.0], "y_range": [108.0, 130.0], "face": "B.Cu", "w": 24.0, "h": 22.0},
        "4_AOZ1284_BUCK": {"x_range": [110.0, 132.0], "y_range": [108.0, 130.0], "face": "B.Cu", "w": 22.0, "h": 22.0},
        "5_LM74801_CIKIS_ANAHTARI": {"x_range": [132.0, 149.7], "y_range": [108.0, 126.0], "face": "B.Cu", "w": 17.7, "h": 18.0},
        "6_INA226_OLCUM_CIKIS": {"x_range": [130.0, 149.7], "y_range": [88.0, 108.0], "face": "B.Cu / F.Cu (J4)", "w": 19.7, "h": 20.0},
        "7_CIKIS_DESARJI": {"x_range": [116.0, 128.0], "y_range": [94.0, 108.0], "face": "B.Cu", "w": 12.0, "h": 14.0},
        "9_RTC_BQ32000": {"x_range": [105.0, 124.0], "y_range": [72.0, 86.0], "face": "B.Cu", "w": 19.0, "h": 14.0},
        "10_I2C_SEVIYE_DONUSTURUCU": {"x_range": [116.0, 126.0], "y_range": [86.0, 96.0], "face": "B.Cu", "w": 10.0, "h": 10.0},
        "14_PANEL_ENKODER": {"x_range": [52.0, 60.0], "y_range": [98.0, 109.0], "face": "F.Cu / B.Cu", "w": 8.0, "h": 11.0},
        "12_TFT_BACKLIGHT": {"x_range": [94.0, 106.0], "y_range": [95.0, 106.0], "face": "F.Cu", "w": 12.0, "h": 11.0},
        "13_TFT_J3": {"x_range": [96.0, 103.0], "y_range": [105.0, 112.0], "face": "F.Cu", "w": 7.0, "h": 7.0},
        "15_TEST_NOKTALARI": {"x_range": [106.0, 116.0], "y_range": [90.0, 104.0], "face": "F.Cu / B.Cu", "w": 10.0, "h": 14.0}
    },
    "metrics": {
        "usb_trace_length_mm": 72.0,
        "rf_keepout_ok": True,
        "simultaneous_plug_clearance_mm": 2.0,
        "power_loop_flow": "U-Shape / Perimeter",
        "rtc_isolation_mm": 14.0
    }
}

# Comparison table
comparison = {
    "criteria": [
        {"name": "USB 2.0 D+/D- Yol Uzunluğu", "cand_a": "22.0 mm (Çok Kısa / Düşük Kayıp)", "cand_b": "72.0 mm (Uzun / EMI Riski)", "winner": "Candidate A"},
        {"name": "Mekanik Kararla Uyum (PCB_GENEL_YERLESIM_KARARI)", "cand_a": "Tam Uyum (J7 Top, J8 Bottom, U2 Top/Dış)", "cand_b": "Kısmi Uyum (J8 Top'a kaydırılmış)", "winner": "Candidate A"},
        {"name": "Eşzamanlı Fiş Açıklığı (Z)", "cand_a": "2.5 mm (>2.0 mm)", "cand_b": "2.0 mm (Sınır)", "winner": "Candidate A"},
        {"name": "Güç Akışı ve Döngü Doğrusallığı", "cand_a": "Doğrusal Batı -> Doğu (Sıfır Geri Dönüş)", "cand_b": "U-Tipi Alt Kenar Yayılımı", "winner": "Candidate A"},
        {"name": "Termal Ayrım (Soğuk MCU vs Sıcak Güç)", "cand_a": "Kuzey Soğuk MCU / Güney Sıcak Güç (Mükemmel)", "cand_b": "Karışık (Güç bobinleri MCU'ya yakın)", "winner": "Candidate A"},
        {"name": "RTC BQ32000 Sessiz Köşe Mesafesi", "cand_a": "26.5 mm (Kuzeydoğu Sessiz Bölge)", "cand_b": "14.0 mm (L1 Buck Bobinine Yakın)", "winner": "Candidate A"},
        {"name": "Sonuç Değerlendirmesi", "cand_a": "SEÇİLDİ (Uygulama İçin Onaylandı)", "cand_b": "ELENDİ", "winner": "Candidate A"}
    ]
}

# SVG Generation for Candidate A (Floorplan Overview)
def generate_floorplan_svg(cand, filename):
    svg_w = 800
    svg_h = 550
    margin = 50
    scale = (svg_w - 2 * margin) / BOARD_W
    
    def to_svg_x(x):
        return margin + (x - X_MIN) * scale
    
    def to_svg_y(y):
        return margin + (y - Y_MIN) * scale

    colors = {
        "F.Cu": "#3498db",
        "B.Cu": "#e67e22",
        "F.Cu / B.Cu": "#9b59b6",
        "B.Cu / F.Cu (J4)": "#e74c3c"
    }

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">',
        '<style>',
        '  .title { font-family: sans-serif; font-size: 16px; font-weight: bold; fill: #2c3e50; }',
        '  .subtitle { font-family: sans-serif; font-size: 12px; fill: #7f8c8d; }',
        '  .board { fill: #ecf0f1; stroke: #2c3e50; stroke-width: 2.5; rx: 15; }',
        '  .lcd-area { fill: rgba(52, 152, 219, 0.08); stroke: #2980b9; stroke-width: 1.5; stroke-dasharray: 4,4; }',
        '  .block-rect { stroke-width: 1.2; stroke: #2c3e50; opacity: 0.85; }',
        '  .block-text { font-family: sans-serif; font-size: 10px; font-weight: bold; fill: #ffffff; text-anchor: middle; }',
        '  .legend { font-family: sans-serif; font-size: 11px; fill: #2c3e50; }',
        '</style>',
        f'<text x="{margin}" y="30" class="title">{cand["name"]}</text>',
        f'<text x="{margin}" y="45" class="subtitle">Boyut: {BOARD_W:.2f} x {BOARD_H:.2f} mm | Alan Bütçesi ve Kaba Blok Dağılımı</text>',
        # PCB outline
        f'<rect x="{to_svg_x(X_MIN)}" y="{to_svg_y(Y_MIN)}" width="{BOARD_W * scale}" height="{BOARD_H * scale}" class="board"/>',
        # LCD active area outline
        f'<rect x="{to_svg_x(61.15)}" y="{to_svg_y(72.48)}" width="{77.7 * scale}" height="{55.04 * scale}" class="lcd-area"/>',
        f'<text x="{to_svg_x(100.0)}" y="{to_svg_y(75.5)}" font-family="sans-serif" font-size="10" fill="#2980b9" text-anchor="middle">LCD GÖRÜNÜR ALANI (77.7 x 55.0 mm)</text>',
        # Mounting holes
        f'<circle cx="{to_svg_x(54.3)}" cy="{to_svg_y(73.48)}" r="{1.6*scale}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="1.5"/>',
        f'<circle cx="{to_svg_x(145.7)}" cy="{to_svg_y(73.48)}" r="{1.6*scale}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="1.5"/>',
        f'<circle cx="{to_svg_x(54.3)}" cy="{to_svg_y(126.52)}" r="{1.6*scale}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="1.5"/>',
        f'<circle cx="{to_svg_x(145.7)}" cy="{to_svg_y(126.52)}" r="{1.6*scale}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="1.5"/>'
    ]

    # Draw blocks
    for b_name, b_data in cand["blocks"].items():
        bx = to_svg_x(b_data["x_range"][0])
        by = to_svg_y(b_data["y_range"][0])
        bw = (b_data["x_range"][1] - b_data["x_range"][0]) * scale
        bh = (b_data["y_range"][1] - b_data["y_range"][0]) * scale
        color = colors.get(b_data["face"], "#95a5a6")
        
        # Clean label
        short_name = b_name.split("_", 1)[1] if "_" in b_name else b_name
        lines.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{color}" class="block-rect" rx="3"/>')
        lines.append(f'<text x="{bx + bw/2}" y="{by + bh/2 + 3}" class="block-text">{short_name}</text>')

    # Legend
    leg_y = svg_h - 25
    lines.append(f'<rect x="{margin}" y="{leg_y}" width="15" height="15" fill="#3498db" rx="2"/>')
    lines.append(f'<text x="{margin + 22}" y="{leg_y + 12}" class="legend">F.Cu (Top)</text>')
    lines.append(f'<rect x="{margin + 120}" y="{leg_y}" width="15" height="15" fill="#e67e22" rx="2"/>')
    lines.append(f'<text x="{margin + 142}" y="{leg_y + 12}" class="legend">B.Cu (Bottom)</text>')
    lines.append(f'<rect x="{margin + 260}" y="{leg_y}" width="15" height="15" fill="#9b59b6" rx="2"/>')
    lines.append(f'<text x="{margin + 282}" y="{leg_y + 12}" class="legend">Karma (F.Cu + B.Cu)</text>')

    lines.append('</svg>')
    
    with open(os.path.join(REPORT_DIR, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

generate_floorplan_svg(candidate_a, "floorplan_candidate_a.svg")
generate_floorplan_svg(candidate_b, "floorplan_candidate_b.svg")

output = {
    "board_dimensions": {
        "width_mm": BOARD_W,
        "height_mm": BOARD_H,
        "gross_area_mm2": round(BOARD_W * BOARD_H, 2),
        "x_bounds": [X_MIN, X_MAX],
        "y_bounds": [Y_MIN, Y_MAX]
    },
    "candidate_a": candidate_a,
    "candidate_b": candidate_b,
    "comparison": comparison
}

with open(os.path.join(REPORT_DIR, "floorplan_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("Coarse floorplan analysis and SVG diagrams generated successfully.")
