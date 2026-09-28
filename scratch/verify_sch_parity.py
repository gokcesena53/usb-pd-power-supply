import re
import os
import glob

def extract_symbols_from_sch(sch_path):
    with open(sch_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all (symbol ... (property "Reference" "XYZ") ... (property "Value" "VAL") ...)
    # In KiCad 7/8/9/10:
    # (symbol (lib_id "...") (at ...) (unit 1) ... (property "Reference" "R1" ...) (property "Value" "10k" ...) (property "Footprint" "...") ...)
    # Let's match symbols
    symbols = []
    # Split by (symbol (lib_id
    parts = re.split(r'\(symbol\s+\(lib_id', content)
    for p in parts[1:]:
        # extract Reference
        m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
        m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', p)
        m_fp = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', p)
        if m_ref:
            ref = m_ref.group(1)
            val = m_val.group(1) if m_val else ""
            fp = m_fp.group(1) if m_fp else ""
            symbols.append({
                'ref': ref,
                'val': val,
                'footprint': fp,
                'file': os.path.basename(sch_path)
            })
    return symbols

def check_parity():
    sch_files = glob.glob('hardware/*.kicad_sch')
    all_sch_rc = []
    for sf in sch_files:
        syms = extract_symbols_from_sch(sf)
        for s in syms:
            ref = s['ref']
            if ref.startswith('R') or ref.startswith('C') or ref.startswith('RShunt'):
                all_sch_rc.append(s)

    print(f"Total R/C in schematics: {len(all_sch_rc)}")
    
    # Load PCB R/C
    import json
    with open('scratch/all_rc_extracted.json', 'r', encoding='utf-8') as f:
        pcb_rc = json.load(f)

    pcb_refs = {x['ref']: x for x in pcb_rc}
    sch_refs = {x['ref']: x for x in all_sch_rc}

    print(f"Total R/C in PCB: {len(pcb_refs)}")

    missing_in_pcb = set(sch_refs.keys()) - set(pcb_refs.keys())
    extra_in_pcb = set(pcb_refs.keys()) - set(sch_refs.keys())

    print(f"Missing in PCB: {missing_in_pcb} (Count: {len(missing_in_pcb)})")
    print(f"Extra in PCB: {extra_in_pcb} (Count: {len(extra_in_pcb)})")

    # Check value match
    val_mismatches = []
    for ref in sorted(pcb_refs.keys()):
        if ref in sch_refs:
            sch_val = sch_refs[ref]['val']
            pcb_val = pcb_refs[ref]['val']
            if sch_val != pcb_val:
                val_mismatches.append((ref, sch_val, pcb_val))

    print(f"Value mismatches: {val_mismatches} (Count: {len(val_mismatches)})")

if __name__ == '__main__':
    check_parity()
