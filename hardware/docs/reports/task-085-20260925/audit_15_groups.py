import pcbnew
import json
import os

BOARD_PATH = "hardware/gopo.kicad_pcb"
REPORT_DIR = "hardware/docs/reports/task-085-20260925"

board = pcbnew.LoadBoard(BOARD_PATH)

# Authoritative 15 groups mapping from TASK-069 (137 grouped footprints)
GROUP_DEFS = {
    "1_USB_C_GIRIS": {
        "task": "TASK-070",
        "doc": "USB_C_GIRIS_YERLESIM_TASK070_20260924.md",
        "refs": ["J7", "D3", "D8", "D9", "U10", "R62", "R63"],
        "target_face": "F.Cu (J7) / B.Cu (D3, D8, D9, U10, R62, R63 per TASK-063)",
        "role": "USB-C giriş portu, TVS koruma, CC pull-down, USB 2.0 ESD",
        "interfaces": ["USB_VBUS", "USB_CC1", "USB_CC2", "USB_DP", "USB_DM", "GND"]
    },
    "2_AP33772S_PD_KONTROLCU": {
        "task": "TASK-071",
        "doc": "AP33772S_YERLESIM_TASK071_20260924.md",
        "refs": ["U1", "Q3", "R8", "R9", "R11", "R12", "R13", "R14", "R21", "R64", "R65", "C1", "C2", "C3", "C4", "C8", "D1", "TH1", "TP1", "TP2", "TP3", "TP4", "TP5"],
        "target_face": "B.Cu",
        "role": "USB PD Sink Kontrolcü, Kelvin akım şöntü, NTC ve VBUS algılama",
        "interfaces": ["USB_VBUS", "PD_VBUS_SENSED", "I2C_SDA_5V", "I2C_SCL_5V", "PD_INT", "GND"]
    },
    "3_TPS55340_PRE_BOOST": {
        "task": "TASK-072",
        "doc": "TPS55340_YERLESIM_TASK072_20260924.md",
        "refs": ["U11", "L3", "D4", "D5", "C23", "C24", "C25", "C26", "C27", "C28", "C29", "R47", "R48", "R49", "R52", "R53"],
        "target_face": "B.Cu",
        "role": "Pre-boost regülatör (V_PRE üretimi, 4.8V - 21V)",
        "interfaces": ["USB_VBUS", "V_PRE", "BOOST_FB", "EN_CTRL", "GND"]
    },
    "4_AOZ1284_BUCK": {
        "task": "TASK-073",
        "doc": "AOZ1284_YERLESIM_TASK073_20260924.md",
        "refs": ["U5", "U6", "L1", "D2", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "R38", "R39", "R40", "R41", "R43", "R50", "R51"],
        "target_face": "B.Cu",
        "role": "Senkron buck regülatör ve TLV431 referans kelepçesi (0.8V - 20V / 5A)",
        "interfaces": ["V_PRE", "PD_VOUT", "BUCK_FB", "EN_CTRL", "GND"]
    },
    "5_LM74801_CIKIS_ANAHTARI": {
        "task": "TASK-074",
        "doc": "LM74801_YERLESIM_TASK074_20260924.md",
        "refs": ["U12", "Q5", "D6", "C30", "C31", "C32", "R54", "R55", "R56", "R58"],
        "target_face": "B.Cu",
        "role": "İdeal diyot ve ters akım korumalı çıkış güç anahtarı",
        "interfaces": ["PD_VOUT", "OUT_POS", "OUT_EN", "GND"]
    },
    "6_INA226_OLCUM_CIKIS": {
        "task": "TASK-075",
        "doc": "INA226_PANEL_CIKISI_YERLESIM_TASK075_20260924.md",
        "refs": ["U3", "U13", "RShunt1", "J4", "C11", "C35", "D7", "R27", "R59", "R61"],
        "target_face": "B.Cu (U3, U13, RShunt1) / F.Cu (J4 Banana Jak)",
        "role": "Hassas akım/gerilim izleme, şönt direnci ve çıkış klemensi/banana jak",
        "interfaces": ["OUT_POS", "I2C_SDA", "I2C_SCL", "ALERT", "+3.3V", "GND"]
    },
    "7_CIKIS_DESARJI": {
        "task": "TASK-076",
        "doc": "CIKIS_DESARJI_YERLESIM_TASK076_20260924.md",
        "refs": ["Q4", "Q6", "D10", "R66", "R67"],
        "target_face": "B.Cu",
        "role": "Aktif hızlı çıkış kapasitör deşarj hücresi",
        "interfaces": ["OUT_POS", "OUT_DISCHARGE", "GND"]
    },
    "8_ESP32_C6_MCU": {
        "task": "TASK-077",
        "doc": "ESP32_C6_YERLESIM_TASK077_20260924.md",
        "refs": ["U2", "C5", "C6", "C7", "R1", "R2", "R3", "R10", "R15", "R16", "R37", "SW1", "SW2", "TP9", "TP10"],
        "target_face": "F.Cu (Top)",
        "role": "Ana MCU kontrolcü, Wi-Fi 6 / BLE 5, butonlar, RF anten",
        "interfaces": ["+3.3V", "UART", "SPI", "I2C", "GPIO", "GND"]
    },
    "9_RTC_BQ32000": {
        "task": "TASK-078",
        "doc": "RTC_BQ32000_YERLESIM_TASK078_20260924.md",
        "refs": ["U4", "Y1", "C9", "C33", "R24"],
        "target_face": "B.Cu (C33 THT)",
        "role": "Gerçek zamanlı saat (RTC), 32.768 kHz kristal, 1.5F süperkapasitör yedekleme",
        "interfaces": ["+3.3V", "I2C_SDA", "I2C_SCL", "GND"]
    },
    "10_I2C_SEVIYE_DONUSTURUCU": {
        "task": "TASK-079",
        "doc": "I2C_SEVIYE_DONUSTURUCU_YERLESIM_TASK079_20260924.md",
        "refs": ["Q1", "Q2", "R4", "R5", "R6", "R7"],
        "target_face": "B.Cu",
        "role": "Çift yönlü I2C seviye dönüştürücü (MCU 3.3V <-> Periferikler 5V)",
        "interfaces": ["+3.3V", "I2C_SDA_3V3", "I2C_SCL_3V3", "I2C_SDA_5V", "I2C_SCL_5V", "GND"]
    },
    "11_ETHERNET_MEZANIN": {
        "task": "TASK-080",
        "doc": "ETHERNET_MEZANIN_YERLESIM_TASK080_20260924.md",
        "refs": ["J8", "Q8", "R17", "C10", "C20", "C21", "TP14"],
        "target_face": "B.Cu (Bottom)",
        "role": "Waveshare 2-CH UART to ETH mezanin modülü ve P-MOSFET besleme anahtarı",
        "interfaces": ["+3.3V", "ETH_3V3", "ETH_PWR_EN", "UART_TX", "UART_RX", "ETH_RUN", "GND"]
    },
    "12_TFT_BACKLIGHT": {
        "task": "TASK-081",
        "doc": "TFT_BACKLIGHT_YERLESIM_TASK081_20260924.md",
        "refs": ["Q7", "R28", "R29", "R60"],
        "target_face": "F.Cu (Top)",
        "role": "TFT LCD arka aydınlatma akım sınırlayıcı ve PWM anahtarı",
        "interfaces": ["+3.3V", "BL_A", "BL_K", "TFT_BL_PWM", "GND"]
    },
    "13_TFT_J3": {
        "task": "TASK-082",
        "doc": "TFT_J3_YERLESIM_TASK082_20260924.md",
        "refs": ["C34"], # J3 is the mechanical anchor
        "target_face": "F.Cu (Top)",
        "role": "3.2 inç TFT LCD 30-pin FPC konnektörü ve VDD ayrıştırma kapasitörü",
        "interfaces": ["+3.3V", "SPI_MOSI", "SPI_CLK", "SPI_CS", "TFT_DC", "TFT_RST", "BL_A", "BL_K", "GND"]
    },
    "14_PANEL_ENKODER": {
        "task": "TASK-083",
        "doc": "PANEL_ENKODER_J9_YERLESIM_TASK083_20260924.md",
        "refs": ["R34", "R35", "R36"], # J9 is the mechanical anchor
        "target_face": "B.Cu (R34, R35, R36 pull-up)",
        "role": "Panel döner enkoder kablo bağlantısı ve 10k filtre pull-up dirençleri",
        "interfaces": ["+3.3V", "ENC_A", "ENC_B", "ENC_SW", "GND"]
    },
    "15_TEST_NOKTALARI": {
        "task": "TASK-084",
        "doc": "TEST_NOKTALARI_YERLESIM_TASK084_20260924.md",
        "refs": ["TP6", "TP7", "TP8", "TP11", "TP12", "TP13"],
        "target_face": "F.Cu (UART0) / B.Cu (I2C)",
        "role": "UART0 debug hücresi (TP11-13) ve I2C bara teşhis hücresi (TP6-8)",
        "interfaces": ["UART0_TX", "UART0_RX", "I2C_SCL", "I2C_SDA", "GND"]
    }
}

# Fixed / staged mechanical anchors
MECHANICAL_REFS = ["H1", "H2", "H3", "H4", "J3", "J9"]

all_fps = board.GetFootprints()
fp_by_ref = {fp.GetReference(): fp for fp in all_fps}
print(f"Total footprints on board: {len(fp_by_ref)}")

# Check coverage
all_defined_refs = set()
for g_name, g_info in GROUP_DEFS.items():
    all_defined_refs.update(g_info["refs"])
all_defined_refs.update(MECHANICAL_REFS)

missing_in_board = all_defined_refs - set(fp_by_ref.keys())
extra_in_board = set(fp_by_ref.keys()) - all_defined_refs

print(f"Defined refs count: {len(all_defined_refs)}")
print(f"Missing in board: {missing_in_board}")
print(f"Extra in board (unassigned): {extra_in_board}")

assert len(missing_in_board) == 0, f"Missing: {missing_in_board}"
assert len(extra_in_board) == 0, f"Extra: {extra_in_board}"
print("PARITY: 100% of board footprints match exactly with the 15 groups and mechanical anchors!")

# Build envelope and detail for each group
group_summaries = {}
for g_name, g_info in GROUP_DEFS.items():
    refs = g_info["refs"]
    fps = [fp_by_ref[r] for r in refs if r in fp_by_ref]
    min_x = min(fp.GetBoundingBox(True, False).GetX() / 1e6 for fp in fps)
    max_x = max((fp.GetBoundingBox(True, False).GetX() + fp.GetBoundingBox(True, False).GetWidth()) / 1e6 for fp in fps)
    min_y = min(fp.GetBoundingBox(True, False).GetY() / 1e6 for fp in fps)
    max_y = max((fp.GetBoundingBox(True, False).GetY() + fp.GetBoundingBox(True, False).GetHeight()) / 1e6 for fp in fps)
    
    width = max_x - min_x
    height = max_y - min_y
    area = width * height
    
    layers = set(fp.GetLayerName() for fp in fps)
    
    member_details = []
    for fp in fps:
        pos = fp.GetPosition()
        member_details.append({
            "ref": fp.GetReference(),
            "value": fp.GetValue(),
            "x": pos.x / 1e6,
            "y": pos.y / 1e6,
            "angle": fp.GetOrientationDegrees(),
            "layer": fp.GetLayerName(),
            "locked": fp.IsLocked()
        })
        
    group_summaries[g_name] = {
        "task": g_info["task"],
        "doc": g_info["doc"],
        "role": g_info["role"],
        "target_face": g_info["target_face"],
        "current_layers": list(layers),
        "ref_count": len(refs),
        "bbox": {
            "min_x": round(min_x, 3),
            "max_x": round(max_x, 3),
            "min_y": round(min_y, 3),
            "max_y": round(max_y, 3),
            "width": round(width, 3),
            "height": round(height, 3),
            "area_mm2": round(area, 2)
        },
        "interfaces": g_info["interfaces"],
        "members": member_details
    }

# Check anchors
anchors_summary = {}
for r in MECHANICAL_REFS:
    fp = fp_by_ref[r]
    pos = fp.GetPosition()
    anchors_summary[r] = {
        "ref": r,
        "value": fp.GetValue(),
        "x": pos.x / 1e6,
        "y": pos.y / 1e6,
        "angle": fp.GetOrientationDegrees(),
        "layer": fp.GetLayerName(),
        "locked": fp.IsLocked()
    }

# Check critical D5 - U11 track
tracks = board.GetTracks()
d5_u11_track_len = 0.0
for t in tracks:
    if t.GetNetname() == "BOOST_FB":
        d5_u11_track_len += t.GetLength() / 1e6

print(f"BOOST_FB track length: {d5_u11_track_len:.3f} mm")

output_data = {
    "total_footprints": len(fp_by_ref),
    "group_count": len(GROUP_DEFS),
    "grouped_footprints_count": sum(g["ref_count"] for g in group_summaries.values()),
    "mechanical_anchors": anchors_summary,
    "missing_refs": list(missing_in_board),
    "unassigned_refs": list(extra_in_board),
    "boost_fb_track_mm": round(d5_u11_track_len, 3),
    "groups": group_summaries
}

with open(os.path.join(REPORT_DIR, "handoff_matrix.json"), "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print("Saved handoff_matrix.json successfully.")
