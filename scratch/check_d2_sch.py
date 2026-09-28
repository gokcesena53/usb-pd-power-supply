import re

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# let's see wires and labels near (271.78, 195.58)
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'bd022141-0333-4f72-b735-3c00d74825ce' in line: # D2 uuid
        print('\n'.join(lines[max(0, i-20):min(len(lines), i+40)]))
