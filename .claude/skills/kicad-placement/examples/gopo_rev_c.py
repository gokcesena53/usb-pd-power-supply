"""gopo REV_C yerlesim config'i (TASK-115, 29.09.2026 sifirdan yerlesim).

place.py --cfg ile okunur. Kilitli parcalar (H1-H4, J3) pcb_dump'tan otomatik
sabittir. Kaynaklar: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md,
HIYERARSIK_YERLESIM_MIMARISI_TASK101_20260928.md, SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md.
TASK-115 (agirlik 10/5/1): S 7171.1 -> 4025.2. TASK-118 (10/5/5 + FPC keepout): S 10771.1 -> 10973.1.
"""

# encoder girintisi: sabit dis hattin sol kenarindan kesilen dikdortgen
CUTOUTS = [(50.275, 102.5, 59.8, 122.3)]
LCD = (63.65, 72.41, 141.5, 127.59)           # LCD modulunun F yuz izdusumu (User.Drawings)
# LCD FPC buküm yolu (LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md): J3 agzi X=102.55 -> apex X=142.42,
# FPC Y=101.55..117.05 (+-0.50 cikis toleransi); FPC LCD ile kart arasinda F yuzeyine yatar.
FPC_PATH = (102.55, 101.05, 142.92, 117.55)
KEEPOUTS = [(LCD, "J7 D3 D8 D9 U10 R62 R63 TP11 TP12 TP13",
             "LCD alti <=1.80 mm; uzun/kenar parcalari LCD golgesi disinda"),
            (FPC_PATH, "@F", "FPC buküm yolunda top layerda komponent yok (B parcalarin THT pinleri dahil)")]

# Kullanici agirliklari (SKILL.md, 29.09.2026): kritik 10, olcum/FB 5, diger 5
W_ORDINARY = 5.0
# Routability terimleri (TASK-119, 29.09.2026; oneri degerleri, kullanici onayi bekler):
W_CROSS = 15.0          # ayni yuzde kesisen kenar cifti ~ via cifti + dolanma; w5 kenarda ~3 mm
W_DECAP_SIDE = 100.0    # dekuplaj IC ile ayni yuzde "mumkun oldugunca": w10 kenarda ~10 mm'ye esdeger
FLIP_DECAPS = True      # yer yoksa karsi yuz (legal once ayni yuzu tarar)
W_GND_LOCAL = 1.0       # GND padi blok icindeki en yakin GND padina (arama GND MST'sini disarida tutar)
FAR_MM = 6.0
# In2 POWER_PLANE: tum guc hatlari bolunmus polygon (kullanici karari 29.09.2026); In1 = GND.
# Anahtarlama dugumleri (BOOST_SW, LX_SW) ve SRC_COMMON yerel dis katman bakiri kalir.
PLANE_NETS = {"+3.3V", "V_PRE", "PD_VOUT", "PD_VBUS_SENSED", "USB_VBUS", "SW_OUT", "OUT_POS",
              "ETH_3V3", "PD_5V"}
W_PLANE = 1.0           # polygon kompaktligi (oneri; ayni netin padlari bir arada kalsin)
AUTO_LOCAL = True       # R2/R3 (USB seri), C23 (U11 SS) gibi IC-yerel parcalar cekme hamlesi alsin
NO_WORSE_W = 5          # Kelvin/FB kenarlari da uzayamaz (TASK-119'da R11 Kelvin 6.7 -> 10.6 mm oldu)

BLOCKS = {
    "USB": "J7 U10 D3 D8 D9 R62 R63",
    "PD": "U1 R11 Q3 C1 C2 C3 C4 C8 R12 R13 R14 D1 R21 TH1 R8 R9 R64 R65 TP1 TP2 TP4 TP5",
    "BOOST": "U11 L3 D4 C23 C24 C25 C26 C27 C28 C29 R47 R48 R49 R52 R53 D5 TP3",
    "BUCK": "U5 L1 D2 C12 C13 C14 C15 C16 C17 C18 C19 R38 R39 R40 R41 U6 R50 R51 R43",
    "OUTSW": "U12 Q5 C30 R54 D6 C31 C32 R55 R56 R58 Q4 Q6 D10 R66 R67 U13 R61 C35",
    "OUTMEAS": "RShunt1 U3 C11 R27 R59 D7 J4",
    "MCU": "U2 C5 C6 C7 R1 SW1 SW2 R10 R37 R15 R16 R2 R3 TP6 TP7 TP8 TP11 TP12 TP13 Q1 Q2 R4 R5 R6 R7",
    "RTC": "U4 Y1 C9 C33 R24",
    "ETH": "J8 Q8 R17 C10 C20 C21 TP9 TP10 TP14",
    "UI": "J3 J9 MECH_ENC R34 R35 R36 Q7 R28 R29 R60 C34",
    "MECH": "H1 H2 H3 H4",
}

OUTLINE_BOUND = {"MECH_ENC", "J9"}             # konumlari sabit encoder girintisiyle belirli
SLIDE = {"J7": ("y", 88.2, 91.25),             # sol kenar USB-C; J8 ust/alt sinirlari H1 ve girintiyle
         "U2": ("x", 64.6, 98.0),              # anten ust kenardan disarida; X H1..MCU bolgesi
         "J4": ("y", 92.0, 120.4)}             # sag kenar cikis kablo pedleri, H2/H4 arasi
TIED = {"J8": ("J7", "y")}                     # Ethernet USB-C'nin tam altinda, ayni panel
NO_EDGE_CHECK = {"J7", "J8", "U2", "MECH_ENC", "J9"}
ALLOW_OVERLAP = [("J7", "J8")]                 # USB-C THT govde pinleri RJ45 mezanin courtyard'inda (tasarim geregi)

# TASK-101 mimarisi: guneyde soldan saga PD -> boost -> buck -> cikis; kuzeyde MCU/ETH/RTC.
# Bolgesiz aramada U1/R11 kuzeye (U2 altina), C15/C29 kendi donusturuculerinden uzaga gitti.
REGION = {
    ("USB", "F"): (50.3, 77.0, 63.6, 102.0),
    ("MCU", "F"): (56.0, 69.5, 105.0, 96.0),
    ("MCU", "B"): (57.0, 69.5, 112.0, 77.3),
    ("ETH", "B"): (103.0, 76.0, 120.0, 101.0),
    ("RTC", "B"): (112.0, 69.5, 149.7, 95.0),
    ("PD", "B"): (59.8, 99.5, 84.0, 130.5),
    ("BOOST", "B"): (80.0, 99.5, 103.0, 130.5),
    ("BUCK", "B"): (100.0, 99.5, 124.0, 130.5),
    ("OUTSW", "F"): (104.0, 84.0, 148.5, 128.0),   # FPC yolu KEEPOUTS ile disarida
    ("OUTSW", "B"): (118.0, 96.0, 142.0, 130.5),
    ("OUTMEAS", "B"): (124.0, 92.0, 149.7, 130.5),
    ("UI", "F"): (60.0, 86.0, 106.0, 130.5),
}
ANCHOR = {"USB": (58, 90), "PD": (72, 115), "BOOST": (91, 115), "BUCK": (112, 115), "OUTSW": (128, 108),
          "OUTMEAS": (137, 112), "MCU": (80, 74), "RTC": (130, 82), "ETH": (110, 88), "UI": (84, 108)}

PULL = [("TP13", "TP12", 1.0, "yalniz GND'li prob noktasi UART test noktalarinin yaninda (TASK-098)")]


def D(c, ic, why, w=10):
    return ("DECAP", c, ic, w, why)


CRIT = [
    ("D3.1", "J7@USB_VBUS", 10, "VBUS TVS clamp loop at USB-C"),
    ("D3.2", "J7@GND", 10, "VBUS TVS clamp return at USB-C"),
    ("U10.1", "J7@USB_DM", 10, "USBLC6 ESD clamp at USB-C (D-)"),
    ("U10.3", "J7@USB_DP", 10, "USBLC6 ESD clamp at USB-C (D+)"),
    ("U10.2", "J7@GND", 10, "USBLC6 ESD clamp return"),
    ("D8.1", "J7@USB_CC1", 10, "CC1 ESD clamp at USB-C"),
    ("D9.1", "J7@USB_CC2", 10, "CC2 ESD clamp at USB-C"),
    ("D8.2", "J7@GND", 10, "CC1 ESD clamp return"),
    ("D9.2", "J7@GND", 10, "CC2 ESD clamp return"),
    # AP33772S
    D("C1", "U1", "AP33772S V18 LDO decoupling"),
    D("C4", "U1", "AP33772S 5V (PD_5V) decoupling"),
    D("C3", "U1", "AP33772S VIN (PD_VBUS_SENSED) decoupling"),
    ("C2.1", "U1.15", 5, "AP33772S IFB current-sense filter"),
    ("C2.2", "U1@GND", 5, "AP33772S IFB filter return"),
    ("R11.1", "U1@USB_VBUS", 5, "R11 5 mOhm Kelvin sense (VBUS side)"),
    ("R11.2", "U1@PD_VBUS_SENSED", 5, "R11 5 mOhm Kelvin sense (load side)"),
    # TPS55340 boost: SW-diyot-Cout dongusu, VIN bypass, FB/COMP/FREQ IC'de
    ("D4.2", "U11@BOOST_SW", 10, "boost hot loop: SW -> diode"),
    ("D4.1", "C27.1", 10, "boost hot loop: diode -> Cout"),
    ("D4.1", "C28.1", 10, "boost hot loop: diode -> Cout"),
    ("C27.2", "U11@GND", 10, "boost hot loop: Cout -> PGND"),
    ("C28.2", "U11@GND", 10, "boost hot loop: Cout -> PGND"),
    D("C26", "U11", "TPS55340 VIN bypass (100n)"),
    D("C25", "U11", "TPS55340 VIN bypass (4u7)"),
    ("R48.2", "U11.9", 5, "boost FB divider at FB pin"),
    ("R49.1", "U11.9", 5, "boost FB divider at FB pin"),
    ("R49.2", "U11@GND", 5, "boost FB divider ground at IC"),
    ("D5.2", "U11.9", 5, "EN_CTRL diode into boost FB node"),
    ("R52.1", "U11.8", 5, "boost COMP network at COMP pin"),
    ("C24.1", "R52.2", 5, "boost COMP network series RC"),
    ("C24.2", "U11@GND", 5, "boost COMP network ground"),
    ("R47.1", "U11.10", 5, "boost FREQ resistor at pin"),
    ("R47.2", "U11@GND", 5, "boost FREQ resistor ground"),
    # AOZ1284 buck (senkron degil: Cin - VIN(EP) - LX - D2 - GND)
    D("C12", "U5", "AOZ1284 VIN input capacitor (hot loop)"),
    D("C13", "U5", "AOZ1284 VIN input capacitor (hot loop)"),
    D("C14", "U5", "AOZ1284 VIN input capacitor (hot loop)"),
    ("D2.1", "U5.1", 10, "buck hot loop: LX -> catch diode"),
    ("D2.2", "C12.2", 10, "buck hot loop: diode anode -> Cin GND"),
    ("D2.2", "C13.2", 10, "buck hot loop: diode anode -> Cin GND"),
    ("C16.1", "L1.2", 10, "buck output ripple loop: Cout at inductor [uncertain: TASK-117]"),
    ("C16.2", "D2.2", 10, "buck output ripple loop: Cout GND to diode/Cin GND [uncertain: TASK-117]"),
    ("C17.1", "U5.2", 10, "buck bootstrap loop"),
    ("C17.2", "U5.1", 10, "buck bootstrap loop"),
    ("R39.2", "U5.6", 5, "buck FB divider at FB pin"),
    ("R40.1", "U5.6", 5, "buck FB divider at FB pin"),
    ("R40.2", "U5@GND", 5, "buck FB divider ground"),
    ("R41.1", "U5.5", 5, "buck COMP network"),
    ("C19.1", "R41.2", 5, "buck COMP series RC"),
    ("C19.2", "U5@GND", 5, "buck COMP ground"),
    ("R38.1", "U5.4", 5, "buck FSW resistor at pin"),
    ("R38.2", "U5@GND", 5, "buck FSW resistor ground"),
    ("R50.2", "U6.1", 5, "TLV431 REF divider"),
    ("R51.1", "U6.1", 5, "TLV431 REF divider"),
    # LM74801 cikis anahtari
    ("C31.2", "U12.11", 10, "LM74801 CAP charge-pump capacitor"),
    ("C31.1", "U12@V_PRE", 10, "LM74801 CAP charge-pump capacitor"),
    D("C32", "U12", "LM74801 VS bypass"),
    ("U12.2", "Q5@SRC_COMMON", 5, "LM74801 source sense at MOSFET"),
    ("U12.12", "Q5@SW_OUT", 5, "LM74801 output sense at MOSFET"),
    D("C35", "U13", "74LVC1G08 bypass"),
    # INA226 ve cikis
    ("RShunt1.1", "U3.10", 5, "INA226 Kelvin IN+"),
    ("RShunt1.2", "U3.9", 5, "INA226 Kelvin IN-"),
    D("C11", "U3", "INA226 VS bypass"),
    ("D7.1", "J4.1", 10, "output TVS clamp at connector"),
    ("D7.2", "J4.2", 10, "output TVS clamp return"),
    # MCU / RTC / ETH / UI
    D("C5", "U2", "ESP32-C6 3V3 bulk bypass"),
    D("C6", "U2", "ESP32-C6 3V3 HF bypass"),
    D("C9", "U4", "BQ32000 VCC bypass"),
    ("Y1.1", "U4.1", 5, "32 kHz crystal OSCI"),
    ("Y1.4", "U4.2", 5, "32 kHz crystal OSCO"),
    D("C10", "J8", "Ethernet module 3V3 bulk"),
    D("C20", "J8", "Ethernet module 3V3 bypass"),
    D("C34", "J3", "LCD 3V3 bypass at FPC connector"),
]

LOOP_GROUPS = {
    "boost sicak dongu (SW-D4, D4-Cout, Cout-PGND)": ["D4.", "C27.2", "C28.2"],
    "buck giris dongusu (Cin, D2)": ["C12.", "C13.", "C14.", "D2."],
    "buck bootstrap": ["C17."],
    "USB-C TVS/ESD": ["D3.", "U10.", "D8.", "D9."],
    "cikis TVS D7": ["D7."],
    "Kelvin R11 / RShunt1": ["R11.", "RShunt1."],
    "dekuplaj": ["C5.", "C6.", "C9.", "C10.", "C20.", "C34.", "C11.", "C35.", "C1.", "C3.", "C4.", "C25.", "C26.", "C31.", "C32."],
}
