import json

with open('hardware/gopo.kicad_pro', 'r', encoding='utf-8') as f:
    pro = json.load(f)

board_setup = pro.get('board', {})
rules = board_setup.get('design_settings', {}).get('rules', {})
print(json.dumps(rules, indent=2))
