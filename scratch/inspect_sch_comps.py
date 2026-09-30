import re

schematics = [
    "hardware/gopo.kicad_sch",
    "hardware/mcu.kicad_sch",
    "hardware/usb_c_input.kicad_sch",
    "hardware/usb_pd_controller.kicad_sch",
    "hardware/userinterface.kicad_sch"
]

def analyze_sch():
    components = {}
    for sch_path in schematics:
        with open(sch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match symbols
        # A symbol starts with (symbol (lib_id ...) ... (property "Reference" "XYZ") ... )
        # Let's find all symbols with properties
        sym_blocks = re.findall(r'\(symbol\s+.*?\n\t\)', content, re.DOTALL)
        for sym in sym_blocks:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', sym)
            val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', sym)
            fp_m = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', sym)
            lib_m = re.search(r'\(lib_id\s+"([^"]+)"', sym)
            if ref_m:
                ref = ref_m.group(1)
                val = val_m.group(1) if val_m else ""
                fp = fp_m.group(1) if fp_m else ""
                lib = lib_m.group(1) if lib_m else ""
                if any(ref.startswith(prefix) for prefix in ['D', 'Q', 'L', 'Y', 'U']) and not ref.startswith('#'):
                    components[ref] = {
                        'file': sch_path,
                        'ref': ref,
                        'val': val,
                        'fp': fp,
                        'lib': lib,
                        'raw': sym
                    }

    for ref in sorted(components.keys()):
        c = components[ref]
        print(f"{c['ref']}: {c['val']} ({c['lib']}) in {c['file']}")

analyze_sch()
