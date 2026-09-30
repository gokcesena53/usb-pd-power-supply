import json
import math
import re

def load_data():
    with open('scratch/all_rc_extracted.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {x['ref']: x for x in data}

rc_dict = load_data()

# Let's inspect all R and C references and their nets to understand every single one
print(f"Loaded {len(rc_dict)} components.")
for ref, item in sorted(rc_dict.items(), key=lambda x: (x[0][0], int(re.sub(r'\D', '', x[0])) if re.sub(r'\D', '', x[0]) else 0)):
    p1 = item['p1']
    p2 = item['p2']
    print(f"{ref:8} {item['val']:10} {item['layer']:4} ({item['pos'][0]:6.2f}, {item['pos'][1]:6.2f}, {item['pos'][2]:5.1f}) | P1: {p1['net'][:20]:20} | P2: {p2['net'][:20]:20}")
