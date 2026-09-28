import re

def check_sch_pins():
    for fn in ["hardware/usb_c_input.kicad_sch", "hardware/usb_pd_controller.kicad_sch"]:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # find symbols
        for sym_m in re.finditer(r'\(symbol\s*\n.*?\n\t\)', content, re.DOTALL):
            sym = sym_m.group(0)
            ref_m = re.search(r'\(property\s+"Reference"\s+"(D\d+)"', sym)
            if ref_m:
                ref = ref_m.group(1)
                val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', sym)
                lib_m = re.search(r'\(lib_id\s+"([^"]+)"', sym)
                print(f"SCH SYMBOL: {ref}, Val: {val_m.group(1) if val_m else '?'}, Lib: {lib_m.group(1) if lib_m else '?'}")
                # find pin instances
                for pin in re.finditer(r'\(pin\s+"([^"]+)"', sym):
                    print(f"  pin: {pin.group(1)}")

check_sch_pins()
