# USB-C / PD input placement — önceki üst kenar aşaması

**Güncel yerleşim:** J7 artık sol alt kenarda, B.Cu `(28.179, 120.278667)`, 90°; PCB Edge referansı X=24.504 ile eşleşir ve kablo sola takılır. U2 sol üstte, J3 sağa kaydırılmıştır. U10 `(30,113.2)`, D3 `(39,116)` konumundadır. Bu dosyanın aşağıdaki koordinat, yakınlık ve DRC tabloları önceki üst kenar aşamasının tarihsel kaydıdır. [Güncel ortak mekanik rapor](LCD_J3_placement.md) ve [güncel PCB](../gopo.kicad_pcb) esas alınmalıdır. Güncel DRC **266 ihlal, 332 açık bağlantı, 8 parite bulgusu**; CC ve VBUS güç yolu henüz çizilmedi.

Saved in `../gopo.kicad_pcb`. This is a placement milestone; the board remains unrouted.

## Connector and mechanical reference

- Active receptacle: **J7**, `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`. The older JAE PDFs and J1-specific rules do not describe this installed connector.
- New origin: **X=52.700 mm, Y=92.072 mm, 0°, B.Cu**. The opening faces the top edge, toward decreasing board Y. A plug approaches from outside that edge.
- Existing Edge.Cuts is at **Y=88.397 mm**. The footprint's explicit `PCB Edge` line is at local Y=+3.675 mm; after flipping to B.Cu it lies at global Y=92.072−3.675=88.397 mm.
- The installed footprint's front body face and recommended edge reference coincide: **nominal overhang is 0.000 mm for this footprint**. All pad, hole, courtyard and body dimensions were preserved.
- The installed KiCad STEP model agrees: width 8.94 mm, height 3.31 mm, front plane at local 3.675 mm. Its exported mesh bounds were checked. Closest J7 copper-to-edge distance is approximately **1.70 mm**, above the project's 0.50 mm minimum.
- This edge is close to the existing PD controller and MOSFETs. B.Cu mounting also avoids the LCD rear plane 3.00 mm above F.Cu: the 3.31 mm USB body would overlap that envelope if kept on the front underneath the LCD.
- Enclosure wall/opening dimensions are unavailable. The opening must expose the mouth and admit the plug overmould without preventing full insertion. Edge.Cuts was not changed.

## Local changes

U1 retains its centre and rotates from −90° to +90°, bringing CC1/CC2 toward J7. U10 moves directly behind J7 on B.Cu. D3 moves nearby on F.Cu, retaining its layer and polarity. Its future short layer transition is a TVS shunt connection, not a series transition in the main VBUS path.

The moved group comprises J7, U10, D3, U1, C1–C4, TH1, R12/R13/R21, Q1/Q2, R4–R9, R14 and D1. The pullups, level shifters and indicator parts clear the new connector and keep the local PD network together. Q3/Q4, R11, current sensing/output, MCU, LCD/J3, battery and unrelated components retain their positions.

## Routing consequences

| Connection | Before | After |
|---|---:|---:|
| J7 CC1 to U1 CC1 | about 25.9 mm | about 5.9 mm |
| J7 CC2 to U1 CC2 | about 28.2 mm | about 5.3 mm |
| Nearest J7 VBUS pad to R11 USB_VBUS pad | about 24.5 mm | about 5.4 mm |

These are straight pad-to-pad distances, **not routed lengths**. J7, U10 and U1 share B.Cu. Route CC through the protection area and check the final fanout/crossings. The main VBUS feed can stay on B.Cu toward R11 and the existing MOSFET group. Use both physical VBUS land groups; avoid feeding 5 A through one pin escape.

Existing `MAIN_5A` specifies 3.0 mm width and 0.20 mm clearance. Pad escapes need short transitions to wider copper. Copper thickness, temperature rise and final bottlenecks remain to be verified; net-class width alone is not a thermal sign-off.

**No traces, vias or zones existed at the start; none were added.** There is no existing GND plane to claim as verified. No plane split was introduced. Subsequent routing should establish a continuous GND reference and short connections for J7 shell/ground pads, U10 and U1 exposed pad.

## Verification / remaining work

- DRC: **265 → 255 violations**. Comparison by type, description and item UUID found **zero new violations and ten removed violations**.
- Unconnected report: **330 → 332**. These describe physical connectivity in an unrouted board. All pad-to-net assignments are identical.
- Schematic parity remains **8 findings**: six existing footprint mismatches plus missing Q5/Q6.
- All 130 footprint identities, schematic paths and net assignments were preserved. Edge.Cuts and LCD/J3 placement are unchanged. Only the listed 22 input/PD footprints changed position, orientation or side.
- Native copper/courtyard plots and bottom 3D view were inspected. J7 has no reported clearance, courtyard, board-edge or PTH interference violation.
- Q4/J7 courtyards have approximately 0.09 mm separation. The rear right shell pad is also close to J3's opposite-side courtyard. DRC passes; check assembly tolerances, selected shell-stake length and opposite-side solder fillets.
- **R11 remains 0402 on PCB despite the schematic assigning 2512 to the 5 mΩ / 1 W shunt. C3 remains 0402 instead of schematic 0805.** Resolve these existing mismatches before power routing/manufacturing. Package selections were preserved in this repositioning task.
- The 3D preview omits staged off-board components only in a temporary render copy. Some custom model paths, including J3, are missing; this is not a complete enclosure/interference sign-off.

## Sources

- Installed KiCad USB4105 footprint: explicit `PCB Edge` reference and unchanged land pattern.
- Installed KiCad USB4105 STEP model: exported mesh bounds and visual orientation check.
- [GCT USB4105 drawing](https://gct.co/files/drawings/usb4105.pdf), referenced by the footprint.
- [GCT USB4105 specification Rev A3](https://gct.co/files/specs/usb4105-spec.pdf): 5 A collectively across VBUS contacts.

## Exact placement changes

Coordinates are mm in the original board coordinate system.

| Component | Before X / Y | After X / Y | Angle / side |
|---|---|---|---|
| C1 | 57.2290 / 104.8325 | 49.5000 / 101.6500 | 180 / B.Cu |
| C2 | 53.6450 / 106.6105 | 54.6500 / 99.5500 | 0 / B.Cu |
| C3 | 52.3590 / 99.9990 | 47.9500 / 98.8000 | 0 / B.Cu |
| C4 | 49.7080 / 107.4995 | 56.7000 / 98.3555 | 0 / B.Cu |
| D1 | 59.3370 / 101.4035 | 61.8000 / 110.2000 | 180 / B.Cu |
| D3 | 36.9590 / 119.9240 | 52.7000 / 98.4000 | 180 / F.Cu |
| J7 | 28.2530 / 121.6680 | 52.7000 / 92.0720 | 0 / B.Cu |
| Q1 | 56.3100 / 97.5935 | 60.2000 / 106.0000 | -90 / B.Cu |
| Q2 | 52.6270 / 97.5935 | 60.2000 / 100.9000 | -90 / B.Cu |
| R12 | 49.5830 / 103.9435 | 57.1990 / 101.9115 | 0 / B.Cu |
| R13 | 49.5810 / 102.8005 | 57.2010 / 103.0545 | 180 / B.Cu |
| R14 | 57.2010 / 101.4035 | 59.6000 / 110.2000 | 0 / B.Cu |
| R21 | 57.1990 / 103.6895 | 49.5000 / 103.2000 | 0 / B.Cu |
| R4 | 57.3260 / 94.2935 | 61.5000 / 103.4500 | 0 / B.Cu |
| R5 | 55.3000 / 94.3630 | 59.3000 / 103.4500 | 0 / B.Cu |
| R6 | 51.6110 / 94.3610 | 58.8000 / 98.1000 | 0 / B.Cu |
| R7 | 53.5160 / 94.3610 | 61.0000 / 98.1000 | 0 / B.Cu |
| R8 | 57.1990 / 102.5465 | 58.5000 / 109.0000 | 0 / B.Cu |
| R9 | 59.3600 / 102.5465 | 60.7000 / 109.0000 | 0 / B.Cu |
| TH1 | 54.6610 / 106.6085 | 52.1200 / 99.5500 | 0 / B.Cu |
| U1 | 53.3910 / 102.9275 | 53.3910 / 102.9275 | 90 / B.Cu |
| U10 | 35.0840 / 124.8330 | 53.3910 / 97.9500 | 90 / B.Cu |
