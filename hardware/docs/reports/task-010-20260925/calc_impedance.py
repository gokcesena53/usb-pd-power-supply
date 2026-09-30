import math

def microstrip_z0(w_mm, h_mm, t_mm, er):
    w_eff = w_mm + (t_mm / math.pi) * (1 + math.log(2 * h_mm / t_mm)) if t_mm > 0 else w_mm
    return (87 / math.sqrt(er + 1.41)) * math.log(5.98 * h_mm / (0.8 * w_eff + t_mm))

def edge_coupled_diff_z(w_mm, s_mm, h_mm, t_mm, er):
    z0 = microstrip_z0(w_mm, h_mm, t_mm, er)
    z_diff = 2 * z0 * (1 - 0.48 * math.exp(-0.96 * s_mm / h_mm))
    return z0, z_diff

print("=== Case 1: H = 0.100 mm, er = 4.2 ===")
for w in [0.10, 0.12, 0.15, 0.18, 0.20]:
    for s in [0.15, 0.18, 0.20, 0.25]:
        z0, zd = edge_coupled_diff_z(w, s, 0.100, 0.035, 4.2)
        print(f"  W={w:.2f}, S={s:.2f} -> Z0={z0:.1f}, Zdiff={zd:.1f}")

print("\n=== Case 2: H = 0.210 mm, er = 4.6 ===")
for w in [0.20, 0.25, 0.30]:
    for s in [0.15, 0.18, 0.20, 0.22, 0.25]:
        z0, zd = edge_coupled_diff_z(w, s, 0.210, 0.035, 4.6)
        print(f"  W={w:.2f}, S={s:.2f} -> Z0={z0:.1f}, Zdiff={zd:.1f}")
