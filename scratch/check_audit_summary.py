import json

with open('hardware/docs/reports/task-097-20260928/rc_pin_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    ref = item['ref']
    t = item.get('target_info', {})
    dist = t.get('dist_mm', 0)
    print(f"{ref:8} | {item['verdict']:16} | {item['layer']:4} | {item['block'][:25]:25} | dist: {dist:5.2f} mm | {item['function'][:35]}")
