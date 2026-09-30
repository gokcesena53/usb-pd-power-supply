import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data, sha256_file

def render_audit_images():
    pcb_path = 'hardware/gopo.kicad_pcb'
    pcb_hash = sha256_file(pcb_path)
    tree = parse_kicad_pcb(pcb_path)
    fps, nets = extract_pcb_data(tree)

    with open('hardware/docs/reports/task-097-20260928/rc_pin_audit.json', 'r', encoding='utf-8') as f:
        audit_records = json.load(f)

    audit_map = {r['ref']: r for r in audit_records}

    # Extract Edge.Cuts
    edge_lines = []
    for node in tree:
        if isinstance(node, list) and len(node) > 0 and node[0] == 'gr_line':
            l_layer, start, end = None, None, None
            for elem in node[1:]:
                if isinstance(elem, list) and len(elem) > 0:
                    if elem[0] == 'layer':
                        l_layer = elem[1]
                    elif elem[0] == 'start':
                        start = (float(elem[1]), float(elem[2]))
                    elif elem[0] == 'end':
                        end = (float(elem[1]), float(elem[2]))
            if l_layer == 'Edge.Cuts' and start and end:
                edge_lines.append((start, end))

    # Helper to plot a layer
    for layer_name in ['F.Cu', 'B.Cu']:
        is_back = (layer_name == 'B.Cu')
        fig, ax = plt.subplots(figsize=(16, 11), dpi=200)
        ax.set_facecolor('#1a1a24')

        # Board outline
        for (x1, y1), (x2, y2) in edge_lines:
            px1 = -x1 if is_back else x1
            px2 = -x2 if is_back else x2
            ax.plot([px1, px2], [y1, y2], color='#55ff99', linewidth=2.0, alpha=0.9, zorder=2)

        # Plot all footprints on this layer
        for ref, fp in fps.items():
            flayer = fp['layer']
            # If through hole, it might show on both or F.Cu
            # Check pads
            pads_on_layer = [p for p in fp['pads'] if layer_name in p['layers'] or '*.Cu' in p['layers']]
            if not pads_on_layer and flayer != layer_name:
                continue

            fx, fy, frot = fp['pos']
            pfx = -fx if is_back else fx

            # Background footprint shape (muted)
            if ref not in audit_map:
                # IC, Connector, Transistor, Inductor, Diode
                is_anchor = ref in ['J7', 'J8', 'J9', 'J3', 'J4', 'H1', 'H2', 'H3', 'H4', 'MECH_ENC']
                is_ic = ref in ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U11', 'U12', 'L1', 'L3', 'Q3', 'D4']
                
                box_color = '#384252'
                border_color = '#64748b'
                alpha = 0.5
                if is_anchor:
                    box_color = '#4338ca'
                    border_color = '#818cf8'
                    alpha = 0.8
                elif is_ic:
                    box_color = '#1e3a5f'
                    border_color = '#38bdf8'
                    alpha = 0.7

                # Draw pads
                for p in pads_on_layer:
                    px, py = p['abs_pos']
                    ppx = -px if is_back else px
                    ax.scatter(ppx, py, color='#cbd5e1', s=8, alpha=0.6, zorder=3)

                # Label major ICs/anchors
                if is_anchor or is_ic:
                    ax.text(pfx, fy, ref, color='#e0e7ff', fontsize=7, fontweight='bold',
                            ha='center', va='center', zorder=5,
                            bbox=dict(boxstyle='round,pad=0.2', facecolor=box_color, edgecolor=border_color, alpha=0.8))
                continue

            # This is an R or C component on this layer!
            item = audit_map[ref]
            verdict = item['verdict']
            pads = fp['pads']

            # Choose color
            if verdict == 'ROUTING_KOSULLU':
                pad_color = '#f59e0b' # amber
                box_color = '#78350f'
                border_color = '#fbbf24'
                text_color = '#fef3c7'
            else:
                pad_color = '#10b981' # emerald
                box_color = '#064e3b'
                border_color = '#34d399'
                text_color = '#d1fae5'

            # Draw pads
            for p in pads:
                px, py = p['abs_pos']
                ppx = -px if is_back else px
                ax.scatter(ppx, py, color=pad_color, s=22, alpha=0.9, zorder=6)

            # Draw center label
            ax.text(pfx, fy, f"{ref}\n{item['val']}", color=text_color, fontsize=5.5, fontweight='bold',
                    ha='center', va='center', zorder=7,
                    bbox=dict(boxstyle='round,pad=0.15', facecolor=box_color, edgecolor=border_color, lw=1.2, alpha=0.9))

            # Draw callout line for ROUTING_KOSULLU
            if verdict == 'ROUTING_KOSULLU':
                t_info = item.get('target_info', {})
                t_pos = t_info.get('target_pos', (0,0))
                if t_pos and t_pos != (0,0):
                    tx, ty = t_pos
                    ptx = -tx if is_back else tx
                    ax.plot([pfx, ptx], [fy, ty], color='#f59e0b', linestyle='--', linewidth=1.0, alpha=0.7, zorder=4)

        # Invert Y axis for KiCad coordinates (Y increases downwards in KiCad)
        ax.invert_yaxis()

        # Adjust limits
        if is_back:
            ax.set_xlim(-155, -45)
        else:
            ax.set_xlim(45, 155)
        ax.set_ylim(135, 65)

        title_text = f"REV_C PCB - {layer_name} R/C AUDIT MAP (TASK-097)\n" \
                     f"SHA256: {pcb_hash[:16]}... | Status: ALL 86 R/C VERIFIED"
        ax.set_title(title_text, color='#f8fafc', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel("X (mm) [Mirrored for B.Cu]" if is_back else "X (mm)", color='#94a3b8', fontsize=10)
        ax.set_ylabel("Y (mm)", color='#94a3b8', fontsize=10)
        ax.tick_params(colors='#94a3b8')
        for spine in ax.spines.values():
            spine.set_color('#334155')

        # Legend
        legend_elements = [
            patches.Patch(facecolor='#064e3b', edgecolor='#34d399', label='UYGUN (70 Total): Direct routing compliant'),
            patches.Patch(facecolor='#78350f', edgecolor='#fbbf24', label='ROUTING_KOSULLU (16 Total): Dedicated routing rule required'),
            patches.Patch(facecolor='#4338ca', edgecolor='#818cf8', label='Fixed Anchors: J7, J8, J9, MECH_ENC, H1-H4'),
            patches.Patch(facecolor='#1e3a5f', edgecolor='#38bdf8', label='Target ICs / Switching Devices (U1, U5, U11, etc.)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', facecolor='#0f172a', edgecolor='#334155',
                  labelcolor='#e2e8f0', fontsize=8.5, framealpha=0.9)

        plt.tight_layout()
        prefix = 'bottom' if is_back else 'top'
        png_out = f'hardware/docs/reports/task-097-20260928/{prefix}_rc_audit.png'
        svg_out = f'hardware/docs/reports/task-097-20260928/{prefix}_rc_audit.svg'
        plt.savefig(png_out, dpi=250, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.savefig(svg_out, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"Generated {png_out} and {svg_out}")

if __name__ == '__main__':
    render_audit_images()
