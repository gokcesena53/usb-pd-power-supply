import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

groups = re.findall(r'\(group\s+"([^"]+)".*?\(members\s+(.*?)\)\s*\)', text, re.DOTALL)
for gname, members in groups:
    m_list = re.findall(r'"([^"]+)"', members)
    print(f"Group: '{gname}' ({len(m_list)} members)")
    if 'TEST' in gname:
        print("  Members:", m_list)
