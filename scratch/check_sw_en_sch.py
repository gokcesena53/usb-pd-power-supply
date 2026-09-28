import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for sf in ['hardware/usb_pd_controller.kicad_sch', 'hardware/mcu.kicad_sch', 'hardware/power_output.kicad_sch', 'hardware/usb_c_input.kicad_sch', 'hardware/userinterface.kicad_sch', 'hardware/gopo.kicad_sch']:
    try:
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'SW_EN' in content:
            print(f"=== SW_EN in {sf} ===")
            for line in content.splitlines():
                if 'SW_EN' in line:
                    print(" ", line.strip())
    except Exception as e:
        pass
