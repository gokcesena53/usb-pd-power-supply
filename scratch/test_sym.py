with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Power_Path_Custom:SMBJ30A')
print(text[idx:idx+1500])
