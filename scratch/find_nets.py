import re
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

sch_files = glob.glob('hardware/*.kicad_sch')

for net in ['+3.3V', 'V_PRE', 'OUT_POS', 'SW_EN']:
    print(f"==================== NET: {net} ====================")
    for sf in sch_files:
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find labels or global_labels
        labels = re.findall(rf'\((?:label|global_label|hierarchical_label)\s+"{re.escape(net)}".*?\(at\s+([-\d.]+)\s+([-\d.]+)', content, re.DOTALL)
        if labels:
            print(f"  In {sf}: found {len(labels)} labels at {labels}")
        if net == '+3.3V':
            # Also find power symbols for +3.3V
            pwr = re.findall(r'\(symbol\s+\(lib_id\s+"power:\+3\.3V"\).*?\(at\s+([-\d.]+)\s+([-\d.]+)', content, re.DOTALL)
            if pwr:
                print(f"  In {sf}: found {len(pwr)} power:+3.3V symbols")
