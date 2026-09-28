import re
import math

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
comps = {}
pads = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        j = i
        depth = 0
        block_lines = []
        while j < len(lines):
            l = lines[j]
            block_lines.append(l)
            depth += l.count('(') - l.count(')')
            if depth == 0:
                break
            j += 1
        block_text = "\n".join(block_lines)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block_text)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_text)
        layer_m = re.search(r'\(layer "([^"]+)"\)', block_text)
        fp_m = re.search(r'\(footprint "([^"]+)"', block_text)
        if ref_m and at_m:
            ref = ref_m.group(1)
            fx = float(at_m.group(1))
            fy = float(at_m.group(2))
            frot = float(at_m.group(3)) if at_m.group(3) else 0.0
            flayer = layer_m.group(1) if layer_m else "F.Cu"
            comps[ref] = {
                'ref': ref, 'fp': fp_m.group(1) if fp_m else "",
                'layer': flayer, 'x': fx, 'y': fy, 'rot': frot, 'block': block_text
            }
            # pads
            for pm in re.finditer(r'\(pad "([^"]+)"\s+(?:smd|thru_hole|np_thru_hole|connect)\s+[^\s]+\s+\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\).*?\(net (?:[0-9]+ )?"([^"]+)"\)', block_text, re.DOTALL):
                pnum = pm.group(1)
                px = float(pm.group(2))
                py = float(pm.group(3))
                prot = float(pm.group(4)) if pm.group(4) else 0.0
                net = pm.group(5)
                rad = math.radians(frot)
                rx = px * math.cos(rad) - py * math.sin(rad)
                ry = px * math.sin(rad) + py * math.cos(rad)
                pads.append({
                    'ref': ref, 'pad': pnum, 'x': fx + rx, 'y': fy + ry, 'net': net, 'layer': flayer
                })
        i = j + 1
    else:
        i += 1

print(f"Total footprints: {len(comps)}")

# Check items for AC #1: J9, R34, R35, R36, and U2
print("\n--- AC #1: Encoder Path (J9 -> R34-R36 -> U2) ---")
for r in ['J9', 'R34', 'R35', 'R36', 'R2', 'R3', 'U10', 'J7', 'U2', 'U3']:
    if r in comps:
        c = comps[r]
        ref_nets = set(re.findall(r'\(net (?:[0-9]+ )?"([^"]+)"\)', c['block']))
        print(f"{r:6}: {c['layer']:4} at ({c['x']:6.2f}, {c['y']:6.2f}) rot={c['rot']:5.1f} | nets={ref_nets}")

encoder_nets = ['ENCODER_A', 'ENCODER_B', 'ENCODER_SW']
for net in encoder_nets:
    net_pads = [p for p in pads if p['net'] == net]
    print(f"\nNet {net}:")
    for p in net_pads:
        print(f"  {p['ref']:6} pin {p['pad']:2} ({p['layer']:4}) at ({p['x']:6.2f}, {p['y']:6.2f})")

# Check items for AC #2: J7 -> U10 -> R2, R3 -> U2
print("\n--- AC #2: USB D+/D- Path (J7 -> U10 -> R2/R3 -> U2) ---")
for r in ['J7', 'U10', 'R2', 'R3', 'U2']:
    if r in comps:
        c = comps[r]
        print(f"{r:6}: {c['layer']:4} at ({c['x']:6.2f}, {c['y']:6.2f}) rot={c['rot']:5.1f}")

usb_nets = ['USB_DP', 'USB_DM', 'Net-(R2-Pad1)', 'Net-(R3-Pad1)', 'Net-(U10-IO1_2)', 'Net-(U10-IO2_2)']
# find pads for these nets or related
for net in set(p['net'] for p in pads if 'USB' in p['net'] or p['ref'] in ['R2', 'R3', 'U10']):
    print(f"\nNet {net}:")
    for p in [p for p in pads if p['net'] == net]:
        print(f"  {p['ref']:6} pin {p['pad']:2} ({p['layer']:4}) at ({p['x']:6.2f}, {p['y']:6.2f})")

# Check items for AC #3: J3 -> U2 (TFT SPI)
print("\n--- AC #3: TFT SPI Path (J3 -> U2) ---")
tft_nets = ['TFT_SCLK', 'TFT_MOSI', 'TFT_CS', 'TFT_DC', 'TFT_RST']
for net in tft_nets:
    net_pads = [p for p in pads if p['net'] == net]
    print(f"\nNet {net}:")
    for p in net_pads:
        print(f"  {p['ref']:6} pin {p['pad']:2} ({p['layer']:4}) at ({p['x']:6.2f}, {p['y']:6.2f})")

# Check items for AC #4: J8 -> U2 (UART)
print("\n--- AC #4: Ethernet UART Path (J8 -> U2) ---")
uart_nets = ['/MCU/UART_TX', '/MCU/UART_RX']
for net in uart_nets:
    net_pads = [p for p in pads if p['net'] == net]
    print(f"\nNet {net}:")
    for p in net_pads:
        print(f"  {p['ref']:6} pin {p['pad']:2} ({p['layer']:4}) at ({p['x']:6.2f}, {p['y']:6.2f})")

# Check items for AC #5: U3 (INA226) -> U2 (INA_ALERT, I2C)
print("\n--- AC #5: INA226 -> U2 (INA_ALERT, I2C) ---")
ina_nets = ['INA_ALERT', 'I2C_SDA_3V3', 'I2C_SCL_3V3', 'I2C_SDA', 'I2C_SCL']
for net in ina_nets:
    net_pads = [p for p in pads if p['net'] == net]
    print(f"\nNet {net}:")
    for p in net_pads:
        print(f"  {p['ref']:6} pin {p['pad']:2} ({p['layer']:4}) at ({p['x']:6.2f}, {p['y']:6.2f})")
