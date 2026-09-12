from pathlib import Path
import re
import xml.etree.ElementTree as ET
import pcbnew

ROOT = Path(__file__).resolve().parents[2]
NETLIST = ROOT / "reports/final-prelayout-20260911/project.xml"
BOARD_PATH = ROOT / "masaüstü güç kaynağı.kicad_pcb"
SYSTEM_FP = Path(r"C:/Program Files/KiCad/10.0/share/kicad/footprints")
ESP_FP = Path.home() / r"Documents/KiCad/10.0/3rdparty/footprints/com_github_espressif_kicad-libraries/Espressif.pretty"
LOCAL_LIBS = {p.stem: p for p in ROOT.glob("*.pretty")}

BOARD_X0, BOARD_Y0 = 20.0, 20.0
BOARD_X1, BOARD_Y1 = 113.0, 80.0
SKIP_BOARD = {"J5", "J6"}  # Panel-mounted banana jacks; wired through J4.


def load_footprint(fid: str):
    lib, name = fid.split(":", 1)
    candidates = [LOCAL_LIBS.get(lib), SYSTEM_FP / f"{lib}.pretty"]
    if lib == "PCM_Espressif":
        candidates.insert(0, ESP_FP)
    for directory in candidates:
        if directory and directory.exists():
            fp = pcbnew.FootprintLoad(str(directory), name)
            if fp:
                return fp
    raise FileNotFoundError(f"Footprint could not be loaded: {fid}")


def symbol_uuid_map():
    result = {}
    for sch in ROOT.glob("*.kicad_sch"):
        text = sch.read_text(encoding="utf-8")
        i = 0
        while True:
            start = text.find("\n\t(symbol", i)
            if start < 0:
                break
            pos = start + 2
            depth = 0
            in_string = False
            escape = False
            end = None
            for j in range(pos, len(text)):
                ch = text[j]
                if in_string:
                    if escape:
                        escape = False
                    elif ch == "\\":
                        escape = True
                    elif ch == '"':
                        in_string = False
                    continue
                if ch == '"':
                    in_string = True
                elif ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            if not end:
                break
            block = text[pos:end]
            ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
            uid = re.search(r'\(uuid\s+"([0-9a-f-]{36})"\)', block)
            if ref and uid and not ref.group(1).startswith("#"):
                result[(sch.name, ref.group(1))] = uid.group(1)
            i = end
    return result


def box_mm(fp):
    poly = fp.GetCourtyard(pcbnew.F_Cu)
    bb = poly.BBox() if poly.OutlineCount() else fp.GetBoundingBox(False, False)
    return (
        pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY()),
        pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetBottom())
    )


def expanded(box, margin=0.25):
    return (box[0] - margin, box[1] - margin, box[2] + margin, box[3] + margin)


def intersects(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


tree = ET.parse(NETLIST)
components = tree.findall(".//components/comp")
uuid_by_ref = symbol_uuid_map()

board = pcbnew.BOARD()
board.SetCopperLayerCount(4)
board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
board.SetLayerName(pcbnew.In2_Cu, "POWER_PLANE")

def make_netclass(name, clearance, track, via=0.60, drill=0.30, diff_width=0.20, diff_gap=0.15):
    nc = pcbnew.NETCLASS(name)
    nc.SetClearance(pcbnew.FromMM(clearance))
    nc.SetTrackWidth(pcbnew.FromMM(track))
    nc.SetViaDiameter(pcbnew.FromMM(via))
    nc.SetViaDrill(pcbnew.FromMM(drill))
    nc.SetDiffPairWidth(pcbnew.FromMM(diff_width))
    nc.SetDiffPairGap(pcbnew.FromMM(diff_gap))
    board.GetNetClasses()[name] = nc
    return nc

netclasses = {
    "Default": make_netclass("Default", 0.15, 0.20),
    "USB_DIFF": make_netclass("USB_DIFF", 0.15, 0.20, diff_width=0.20, diff_gap=0.15),
    "POWER_3V3": make_netclass("POWER_3V3", 0.20, 0.60, via=0.70, drill=0.35),
    "MAIN_5A": make_netclass("MAIN_5A", 0.25, 2.50, via=1.00, drill=0.50),
}

# Conservative fabrication defaults; differential geometry is finalized against fab stack-up.
ds = board.GetDesignSettings()
ds.m_MinClearance = pcbnew.FromMM(0.15)
ds.m_TrackMinWidth = pcbnew.FromMM(0.15)
ds.m_ViasMinSize = pcbnew.FromMM(0.45)
ds.m_ViasMinAnnularWidth = pcbnew.FromMM(0.10)
ds.m_SolderMaskMinWidth = pcbnew.FromMM(0.05)

nets = {}
for idx, net_xml in enumerate(tree.findall(".//nets/net"), start=1):
    raw_name = net_xml.attrib["name"]
    name = raw_name.replace("/", "{slash}") if raw_name.startswith("Net-(") else raw_name
    net = pcbnew.NETINFO_ITEM(board, name, idx)
    board.Add(net)
    if raw_name in {"PD_VOUT", "OUT_POS", "USB_VBUS", "PD_VBUS_SENSED"}:
        net.SetNetClass(netclasses["MAIN_5A"])
    elif raw_name in {"+3.3V", "BACKLIGHT_4V2"}:
        net.SetNetClass(netclasses["POWER_3V3"])
    elif raw_name in {"USB_DP", "USB_DM"}:
        net.SetNetClass(netclasses["USB_DIFF"])
    else:
        net.SetNetClass(netclasses["Default"])
    nets[raw_name] = net

pin_net = {}
for net_xml in tree.findall(".//nets/net"):
    name = net_xml.attrib["name"]
    for node in net_xml.findall("node"):
        pin_net[(node.attrib["ref"], node.attrib["pin"])] = name

fps = {}
for comp in components:
    ref = comp.attrib["ref"]
    if ref in SKIP_BOARD:
        continue
    fid = comp.findtext("footprint", "")
    if not fid:
        raise RuntimeError(f"Missing footprint: {ref}")
    fp = load_footprint(fid)
    fp.SetReference(ref)
    fp.SetValue(comp.findtext("value", ""))
    fp.SetFPIDAsString(fid)
    sheet_file = next((p.attrib.get("value") for p in comp.findall("property") if p.attrib.get("name") == "Sheetfile"), None)
    uid = uuid_by_ref.get((sheet_file, ref)) if sheet_file else None
    sheet_stamp = comp.find("sheetpath").attrib.get("tstamps", "/").rstrip("/")
    if uid:
        fp.SetPath(pcbnew.KIID_PATH(f"{sheet_stamp}/{uid}"))
    for pad in fp.Pads():
        net_name = pin_net.get((ref, pad.GetNumber()))
        if net_name:
            pad.SetNet(nets[net_name])
    board.Add(fp)
    fps[ref] = fp

# Functional anchors. All parts remain on the top side for the first placement pass.
anchors = {
    "J1": (21.75, 30.0, 270),
    "D3": (30.5, 25.5, 0), "D4": (30.5, 29.0, 0), "D5": (30.5, 32.5, 0), "U9": (34.0, 29.0, 90),
    "U1": (39.0, 30.0, 0), "Q4": (47.0, 27.0, 0), "Q3": (47.0, 34.0, 0), "R11": (58.0, 22.5, 0),
    "RShunt": (58.0, 34.0, 0), "U3": (62.0, 39.0, 0), "J4": (70.0, 22.5, 0),

    # AOZ1284PI power stage: input/boot at the IC, LX parts to the left, feedback/COMP on the quiet side.
    "U5": (60.0, 48.0, 0), "L1": (51.0, 47.0, 180), "D2": (55.0, 53.0, 0),
    "C12": (68.0, 42.8, 0), "C13": (66.5, 49.0, 0), "C14": (57.0, 42.0, 90),
    "C15": (45.0, 54.0, 0), "C16": (48.0, 58.0, 0), "C17": (66.5, 53.0, 90),
    "C18": (61.5, 54.0, 90), "C19": (64.0, 54.0, 90),
    "R38": (70.0, 50.0, 90), "R40": (59.0, 54.0, 90), "R42": (70.0, 46.0, 90),
    "U6": (73.0, 55.0, 0),

    # ESP32 antenna points out through the right board edge; local decoupling sits below the module body.
    "U2": (97.25, 30.0, 270),
    "C5": (84.0, 42.5, 0), "C6": (88.0, 42.5, 0), "C7": (91.0, 42.5, 0),
    "C9": (94.0, 42.5, 0), "C10": (97.0, 42.5, 0),
    "SW1": (84.0, 48.0, 0), "SW2": (92.0, 48.0, 0), "J2": (83.0, 55.0, 90),
    "U4": (56.0, 58.0, 90), "BT1": (36.9, 69.0, 0),

    # TFT/backlight cluster at the bottom edge; encoder is rotated away from the RF keepout.
    "J3": (67.5, 76.0, 0), "L2": (61.0, 65.0, 0), "U7": (67.0, 65.0, 0), "U8": (76.0, 65.0, 0),
    "C20": (61.0, 59.5, 0), "C21": (72.0, 59.5, 0), "C22": (81.0, 61.0, 0),
    "SW3": (93.5, 69.0, 90),
}

occupied = []
for ref, (x, y, angle) in anchors.items():
    fp = fps[ref]
    fp.SetOrientationDegrees(angle)
    fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
    occupied.append((ref, expanded(box_mm(fp), 0.20)))

regions = {
    "/USB_C_INPUT/": (26.0, 23.0, 34.0, 37.0),
    "/USB_PD_CONTROLLER/": (29.0, 21.5, 51.0, 43.5),
    "/POWER SENSING/": (51.0, 23.0, 68.0, 37.0),
    "/POWER GENERATION/": (40.0, 39.0, 74.0, 59.0),
    "/MCU/": (78.0, 41.0, 102.0, 60.0),
    "/USER INTERFACE/": (55.0, 59.0, 82.0, 72.0),
    "/POWER OUTPUT/": (100.0, 22.0, 108.0, 40.0),
}

unplaced = []
for comp in components:
    ref = comp.attrib["ref"]
    if ref in SKIP_BOARD or ref in anchors:
        continue
    fp = fps[ref]
    sheet = comp.find("sheetpath").attrib.get("names", "/")
    x0, y0, x1, y1 = regions[sheet]
    placed = False
    for angle in (0, 90):
        fp.SetOrientationDegrees(angle)
        y = y0
        while y <= y1 and not placed:
            x = x0
            while x <= x1:
                fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
                box = expanded(box_mm(fp), 0.18)
                inside = box[0] >= BOARD_X0 + 0.5 and box[2] <= BOARD_X1 - 0.5 and box[1] >= BOARD_Y0 + 0.5 and box[3] <= BOARD_Y1 - 0.5
                if inside and not any(intersects(box, other) for _, other in occupied):
                    occupied.append((ref, box))
                    placed = True
                    break
                x += 0.75
            y += 0.75
        if placed:
            break
    if not placed:
        unplaced.append(ref)
        fp.SetPosition(pcbnew.VECTOR2I_MM(125 + 3 * len(unplaced), 25))

# Rounded 93 x 60 mm outline with the JAE mid-mount USB-C edge cutout.
def segment(a, b):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pcbnew.VECTOR2I_MM(*a)); s.SetEnd(pcbnew.VECTOR2I_MM(*b))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(pcbnew.FromMM(0.05)); board.Add(s)

def arc(start, mid, end):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_ARC)
    s.SetArcGeometry(pcbnew.VECTOR2I_MM(*start), pcbnew.VECTOR2I_MM(*mid), pcbnew.VECTOR2I_MM(*end))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(pcbnew.FromMM(0.05)); board.Add(s)

segment((22, 20), (111, 20)); arc((111, 20), (112.414, 20.586), (113, 22))
segment((113, 22), (113, 78)); arc((113, 78), (112.414, 79.414), (111, 80))
segment((111, 80), (22, 80)); arc((22, 80), (20.586, 79.414), (20, 78))
segment((20, 78), (20, 34.7)); segment((20, 34.7), (24.25, 34.7))
arc((24.25, 34.7), (24.75, 34.2), (25.25, 34.7))
segment((25.25, 34.7), (25.25, 25.3))
arc((25.25, 25.3), (24.75, 25.8), (24.25, 25.3))
segment((24.25, 25.3), (20, 25.3)); segment((20, 25.3), (20, 22))
arc((20, 22), (20.586, 20.586), (22, 20))

# Layer 2 is reserved as an uninterrupted GND reference plane.
gnd_zone = pcbnew.ZONE(board)
gnd_zone.SetLayer(pcbnew.In1_Cu)
gnd_zone.SetNet(nets["GND"])
gnd_zone.SetLocalClearance(pcbnew.FromMM(0.20))
outline = gnd_zone.Outline()
outline.NewOutline()
for point in ((20.2, 20.2), (112.8, 20.2), (112.8, 79.8), (20.2, 79.8)):
    outline.Append(pcbnew.VECTOR2I_MM(*point))
board.Add(gnd_zone)

board.BuildListOfNets()
pcbnew.SaveBoard(str(BOARD_PATH), board)

# Placement diagnostics.
anchor_overlaps = []
for i, (ra, a) in enumerate(occupied):
    for rb, b in occupied[i + 1:]:
        if intersects(a, b):
            anchor_overlaps.append((ra, rb))

print(f"Saved: {BOARD_PATH}")
print(f"Board footprints: {len(fps)} (panel-only skipped: {sorted(SKIP_BOARD)})")
print(f"Nets: {len(nets)}")
print(f"Unplaced outside board: {unplaced}")
print(f"Placement overlaps detected by script: {anchor_overlaps}")
