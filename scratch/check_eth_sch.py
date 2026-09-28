import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/mcu.kicad_sch', 'r', encoding='utf-8') as f:
    mcu_sch = f.read()

for target in ['ETH_CFG0', 'ETH_PWR_EN', 'ETH_RUN', 'UART_TX', 'UART_RX']:
    matches = re.findall(rf'.{{0,50}}{target}.{{0,50}}', mcu_sch)
    print(f"=== {target} ===")
    for m in matches[:5]:
        print(" ", m.strip())
